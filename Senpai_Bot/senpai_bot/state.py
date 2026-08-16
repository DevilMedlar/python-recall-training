"""Local session persistence (technical, not curriculum state).

Stores the running message list in senpai_bot/state.json (gitignored) so a
conversation survives closing and reopening the terminal. This is separate
from the curriculum's own persistent records (overall_grades.md, stage
grades files), which the model maintains itself via the write_file tool.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_messages(state_file: Path) -> list[dict[str, Any]]:
    if not state_file.is_file():
        return []
    try:
        data = json.loads(state_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data.get("messages", [])


def save_messages(state_file: Path, messages: list[dict[str, Any]]) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps({"messages": messages}, indent=2), encoding="utf-8")


def prepare_messages(
    messages: list[dict[str, Any]],
    system_content: str,
    max_history_messages: int,
) -> tuple[list[dict[str, Any]], bool]:
    """Install the current system prompt and bound persisted chat history.

    History created under a different system prompt is discarded. Keeping it
    would continue reinforcing stale persona/context behavior after an update.
    """
    system_message = {"role": "system", "content": system_content}
    if not messages:
        return [system_message], False

    first = messages[0]
    if first.get("role") != "system" or first.get("content") != system_content:
        return [system_message], True

    history = messages[1:]
    if len(history) <= max_history_messages:
        return [system_message, *history], False

    history = history[-max_history_messages:]
    while history and history[0].get("role") != "user":
        history.pop(0)
    return [system_message, *history], True


def clear(state_file: Path) -> None:
    if state_file.is_file():
        state_file.unlink()
