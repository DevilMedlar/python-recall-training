"""FastAPI backend for the local Senpai Studio."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Add Senpai_Bot to sys.path so the backend can import the package when this
# file is launched directly by start_studio.py.
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from senpai_bot import state
from senpai_bot.config import load_config
from senpai_bot.context import build_startup_context
from senpai_bot.ollama_client import OllamaClient, OllamaError
from senpai_bot.tools import TOOL_SCHEMAS, WorkspaceTools

MAX_TOOL_ROUNDS = 8

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

cfg = load_config()
client = OllamaClient(
    cfg.ollama_host,
    cfg.model,
    cfg.request_timeout,
    num_ctx=cfg.num_ctx,
)
workspace_tools = WorkspaceTools(cfg.repo_root)

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


class ChatRequest(BaseModel):
    message: str


class FileWriteRequest(BaseModel):
    path: str
    content: str


def _persona_prompt() -> str:
    if not cfg.system_prompt_file.is_file():
        return ""
    return cfg.system_prompt_file.read_text(encoding="utf-8", errors="replace")


def _prepare_chat_messages() -> list[dict]:
    system_content = build_startup_context(
        cfg.repo_root,
        _persona_prompt(),
        context_mode=cfg.context_mode,
    )
    messages, reset_history = state.prepare_messages(
        state.load_messages(cfg.state_file),
        system_content,
        cfg.max_history_messages,
    )
    if reset_history:
        logger.info("Reset stale or oversized persisted chat history")
        state.save_messages(cfg.state_file, messages)
    return messages


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.get("/api/config")
async def get_config():
    return {
        "model": cfg.model or "Not configured",
        "repo_root": str(cfg.repo_root),
        "context_mode": cfg.context_mode,
        "problems": cfg.validate(),
    }


@app.get("/api/files")
async def list_files(path: str = "."):
    try:
        return workspace_tools.list_dir(path)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/files/read")
async def read_file(path: str):
    try:
        return {"content": workspace_tools.read_file(path)}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/files/write")
async def write_file(req: FileWriteRequest):
    try:
        return {"message": workspace_tools.write_file(req.path, req.content)}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/chat/reset")
async def reset_chat():
    state.clear(cfg.state_file)
    return {"message": "Session cleared."}


@app.post("/api/chat")
async def chat(req: ChatRequest):
    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    problems = cfg.validate()
    if problems:
        raise HTTPException(status_code=503, detail=" ".join(problems))

    logger.info("Received chat request (%d characters)", len(message))
    messages = _prepare_chat_messages()
    messages.append({"role": "user", "content": message})

    try:
        for _ in range(MAX_TOOL_ROUNDS):
            assistant_message = client.chat(messages, tools=TOOL_SCHEMAS)
            messages.append(assistant_message)

            tool_calls = assistant_message.get("tool_calls") or []
            if not tool_calls:
                content = assistant_message.get("content", "")
                if not content.strip():
                    raise OllamaError("Ollama returned an empty assistant reply.")
                state.save_messages(cfg.state_file, messages)
                return {"role": "assistant", "content": content}

            for call in tool_calls:
                function = call.get("function", {})
                name = function.get("name", "")
                arguments = function.get("arguments", {})
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        arguments = {}

                logger.info("Dispatching tool call: %s", name)
                result = workspace_tools.dispatch(name, arguments)
                messages.append({"role": "tool", "content": result})

        raise OllamaError(
            "The model exceeded the tool-call limit without producing a final reply."
        )
    except OllamaError as exc:
        logger.error("Ollama error: %s", exc)
        raise HTTPException(status_code=502, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
