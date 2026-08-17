from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from collections.abc import Callable

import httpx


class OllamaError(RuntimeError):
    pass


class OllamaManager:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self._owned_process: subprocess.Popen[bytes] | None = None

    def is_ready(self) -> bool:
        try:
            return httpx.get(f"{self.base_url}/api/tags", timeout=1.5).is_success
        except httpx.HTTPError:
            return False

    def start_hidden(self, timeout: float = 20) -> None:
        if self.is_ready():
            return
        executable = shutil.which("ollama")
        if not executable:
            raise OllamaError("Ollama is not installed or is not available on PATH.")
        flags = 0
        startupinfo = None
        if os.name == "nt":
            flags = subprocess.CREATE_NO_WINDOW
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self._owned_process = subprocess.Popen(
            [executable, "serve"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=flags,
            startupinfo=startupinfo,
        )
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.is_ready():
                return
            if self._owned_process.poll() is not None:
                break
            time.sleep(0.25)
        raise OllamaError("Ollama did not become ready in time.")

    def installed_models(self) -> set[str]:
        response = httpx.get(f"{self.base_url}/api/tags", timeout=10)
        response.raise_for_status()
        return {item["name"] for item in response.json().get("models", [])}

    def ensure_model(self, progress: Callable[[str], None] | None = None) -> None:
        models = self.installed_models()
        if self.model in models or self.model.removesuffix(":latest") in models:
            return
        self.pull_model(self.model, progress)

    def pull_model(self, model: str, progress: Callable[[str], None] | None = None) -> None:
        if not model or any(character.isspace() for character in model):
            raise OllamaError("Enter a valid Ollama model name without spaces.")
        with httpx.stream(
            "POST",
            f"{self.base_url}/api/pull",
            json={"name": model, "stream": True},
            timeout=None,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line:
                    continue
                data = json.loads(line)
                if progress:
                    progress(data.get("status", "Downloading model…"))
                if data.get("error"):
                    raise OllamaError(data["error"])

    def stream_chat(self, messages: list[dict[str, str]], on_token: Callable[[str], None]) -> None:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "options": {"temperature": 0.8, "num_ctx": 16384},
        }
        with httpx.stream("POST", f"{self.base_url}/api/chat", json=payload, timeout=None) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line:
                    continue
                data = json.loads(line)
                if data.get("error"):
                    raise OllamaError(data["error"])
                token = data.get("message", {}).get("content", "")
                if token:
                    on_token(token)
