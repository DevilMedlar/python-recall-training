from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


LOCAL_OLLAMA_URL = "http://127.0.0.1:11434"


@dataclass
class Settings:
    model: str = "llama3.1:latest"
    temperature: float = 0.8
    max_history_messages: int = 24
    workspace: str = ""
    check_updates_on_launch: bool = False
    model_setup_prompted: bool = False

    @property
    def ollama_url(self) -> str:
        """Return the only AI endpoint Senpai_Bot is permitted to use."""
        return LOCAL_OLLAMA_URL

    @classmethod
    def load(cls, path: Path) -> "Settings":
        if not path.exists():
            return cls()
        try:
            values = json.loads(path.read_text(encoding="utf-8"))
            return cls(**{key: value for key, value in values.items() if key in cls.__annotations__})
        except (OSError, ValueError, TypeError):
            return cls()

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
