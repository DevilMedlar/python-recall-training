"""Interactive CLI loop wiring together config, context, tools, and Ollama."""

from __future__ import annotations

import sys

from . import state
from .config import Config, load_config
from .context import build_startup_context
from .ollama_client import OllamaClient, OllamaError
from .tools import TOOL_SCHEMAS, WorkspaceTools

MAX_TOOL_ROUNDS = 8


def _read_persona_prompt(cfg: Config) -> str:
    if cfg.system_prompt_file.is_file():
        return cfg.system_prompt_file.read_text(encoding="utf-8", errors="replace")
    return ""


def _run_turn(
    client: OllamaClient,
    tools: WorkspaceTools,
    messages: list[dict],
) -> str:
    """Send messages to the model, transparently resolving tool calls."""
    for _ in range(MAX_TOOL_ROUNDS):
        assistant_message = client.chat(messages, tools=TOOL_SCHEMAS)
        messages.append(assistant_message)

        tool_calls = assistant_message.get("tool_calls") or []
        if not tool_calls:
            return assistant_message.get("content", "")

        for call in tool_calls:
            fn = call.get("function", {})
            name = fn.get("name", "")
            arguments = fn.get("arguments", {})
            if isinstance(arguments, str):
                import json

                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {}
            print(f"  [tool call] {name}({arguments})", file=sys.stderr)
            result = tools.dispatch(name, arguments)
            messages.append({"role": "tool", "content": result})

    return "[Stopped after too many chained tool calls without a final reply.]"


def main() -> None:
    cfg = load_config()
    problems = cfg.validate()
    if problems:
        for p in problems:
            print(f"Config problem: {p}", file=sys.stderr)
        sys.exit(1)

    client = OllamaClient(cfg.ollama_host, cfg.model, cfg.request_timeout)
    tools = WorkspaceTools(cfg.repo_root)

    try:
        available = client.list_models()
    except OllamaError as exc:
        print(f"[warning] {exc}", file=sys.stderr)
        available = None

    if available is not None and cfg.model not in available:
        print(
            f"[warning] Model '{cfg.model}' not found in `ollama list` output: {available}",
            file=sys.stderr,
        )

    messages = state.load_messages(cfg.state_file)

    if not messages:
        persona_prompt = _read_persona_prompt(cfg)
        system_content = build_startup_context(cfg.repo_root, persona_prompt)
        messages = [{"role": "system", "content": system_content}]

    print(f"Senpai Bot harness -- model: {cfg.model} -- host: {cfg.ollama_host}")
    print("Commands: /reset (clear session), /quit (exit)\n")

    while True:
        try:
            user_input = input("Daddy> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input in ("/quit", "/exit"):
            break
        if user_input == "/reset":
            state.clear(cfg.state_file)
            messages = messages[:1]  # keep the system message, drop history
            print("[session cleared]")
            continue

        messages.append({"role": "user", "content": user_input})
        try:
            reply = _run_turn(client, tools, messages)
        except OllamaError as exc:
            print(f"[error] {exc}", file=sys.stderr)
            messages.pop()  # don't persist a turn that never got a reply
            continue

        print(f"\nSenpai> {reply}\n")
        state.save_messages(cfg.state_file, messages)


if __name__ == "__main__":
    main()
