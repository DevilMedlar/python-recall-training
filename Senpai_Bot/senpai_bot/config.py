"""Configuration loading for the Senpai Bot harness.

Reads settings from environment variables, optionally populated from a
`senpai_bot/.env` file (gitignored). No third-party dependencies.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
ENV_FILE = PACKAGE_DIR / ".env"


def _load_env_file(path: Path) -> None:
    """Populate os.environ from a simple KEY=VALUE .env file.

    Existing environment variables are not overwritten. Lines that are
    blank or start with # are ignored.
    """
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_env_file(ENV_FILE)


def _optional_int(name: str) -> int | None:
    value = os.environ.get(name, "").strip()
    return int(value) if value else None


@dataclass(frozen=True)
class Config:
    ollama_host: str = field(default_factory=lambda: os.environ.get(
        "OLLAMA_HOST", "http://localhost:11434"
    ))
    model: str = field(default_factory=lambda: os.environ.get(
        "OLLAMA_MODEL", ""
    ))
    system_prompt_file: Path = field(default_factory=lambda: REPO_ROOT / os.environ.get(
        "SYSTEM_PROMPT_FILE", "persona_system_prompt.md"
    ))
    request_timeout: float = field(default_factory=lambda: float(os.environ.get(
        "OLLAMA_TIMEOUT", "120"
    )))
    context_mode: str = field(default_factory=lambda: os.environ.get(
        "OLLAMA_CONTEXT_MODE", "compact"
    ).strip().lower())
    num_ctx: int | None = field(default_factory=lambda: _optional_int(
        "OLLAMA_NUM_CTX"
    ))
    max_history_messages: int = field(default_factory=lambda: int(os.environ.get(
        "OLLAMA_MAX_HISTORY_MESSAGES", "24"
    )))
    state_file: Path = field(default_factory=lambda: PACKAGE_DIR / "state.json")
    repo_root: Path = field(default_factory=lambda: REPO_ROOT)

    def validate(self) -> list[str]:
        problems = []
        if not self.model:
            problems.append(
                "OLLAMA_MODEL is not set. Put it in senpai_bot/.env, e.g. OLLAMA_MODEL=llama3.1"
            )
        if self.context_mode not in {"compact", "full"}:
            problems.append(
                "OLLAMA_CONTEXT_MODE must be either 'compact' or 'full'."
            )
        if self.num_ctx is not None and self.num_ctx < 2048:
            problems.append("OLLAMA_NUM_CTX must be at least 2048 when set.")
        if self.max_history_messages < 2:
            problems.append("OLLAMA_MAX_HISTORY_MESSAGES must be at least 2.")
        return problems


def load_config() -> Config:
    return Config()
