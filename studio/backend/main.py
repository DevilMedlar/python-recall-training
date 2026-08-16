from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
import json
from pathlib import Path

# Add the parent directory to sys.path so we can import senpai_bot
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from senpai_bot.config import load_config
from senpai_bot.ollama_client import OllamaClient, OllamaError
from senpai_bot.tools import WorkspaceTools, TOOL_SCHEMAS
from senpai_bot.context import build_startup_context
from senpai_bot import state

app = FastAPI()

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cfg = load_config()
client = OllamaClient(cfg.ollama_host, cfg.model, cfg.request_timeout)
tools = WorkspaceTools(cfg.repo_root)

# Create templates directory
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
TEMPLATES_DIR.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

class ChatRequest(BaseModel):
    message: str

class FileWriteRequest(BaseModel):
    path: str
    content: str

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"request": request}
    )

@app.get("/api/config")
async def get_config():
    return {
        "model": cfg.model,
        "repo_root": str(cfg.repo_root)
    }

@app.get("/api/files")
async def list_files(path: str = "."):
    try:
        return tools.list_dir(path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/files/read")
async def read_file(path: str):
    try:
        return {"content": tools.read_file(path)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/files/write")
async def write_file(req: FileWriteRequest):
    try:
        return {"message": tools.write_file(req.path, req.content)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

import logging

logging.basicConfig(level=logging.INFO)

@app.post("/api/chat")
async def chat(req: ChatRequest):
    logging.info(f"Received chat request: {req.message}")
    messages = state.load_messages(cfg.state_file)
    
    if not messages:
        persona_path = cfg.system_prompt_file
        persona_prompt = ""
        if persona_path.is_file():
            persona_prompt = persona_path.read_text(encoding="utf-8")
        
        system_content = build_startup_context(cfg.repo_root, persona_prompt)
        messages = [{"role": "system", "content": system_content}]
    
    messages.append({"role": "user", "content": req.message})
    logging.info(f"Sending messages to Ollama: {messages}")
    
    try:
        # Run the tool-calling loop
        for _ in range(8):
            assistant_message = client.chat(messages, tools=TOOL_SCHEMAS)
            logging.info(f"Received from Ollama: {assistant_message}")
            messages.append(assistant_message)
            
            tool_calls = assistant_message.get("tool_calls") or []
            if not tool_calls:
                state.save_messages(cfg.state_file, messages)
                return assistant_message
            
            for call in tool_calls:
                fn = call.get("function", {})
                name = fn.get("name", "")
                args = fn.get("arguments", {})
                if isinstance(args, str):
                    args = json.loads(args)
                
                logging.info(f"Dispatching tool call: {name}({args})")
                result = tools.dispatch(name, args)
                logging.info(f"Tool result: {result}")
                messages.append({"role": "tool", "content": result})
        
        return {"role": "assistant", "content": "[Too many tool calls]"}
    except OllamaError as e:
        logging.error(f"Ollama error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
