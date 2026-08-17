from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from collections.abc import Callable

import httpx

from .settings import LOCAL_OLLAMA_URL


LOCAL_OLLAMA_HOST = "127.0.0.1:11434"


class OllamaError(RuntimeError):
    pass


class OllamaManager:
    def __init__(self, base_url: str, model: str):
        normalized_url = base_url.rstrip("/")
        if normalized_url != LOCAL_OLLAMA_URL:
            raise OllamaError(
                "Senpai_Bot only permits the local Ollama endpoint at "
                f"{LOCAL_OLLAMA_URL}."
            )
        self.base_url = normalized_url
        self.model = model
        self._owned_process: subprocess.Popen[bytes] | None = None

    def _client(self, timeout: float | None) -> httpx.Client:
        return httpx.Client(base_url=self.base_url, timeout=timeout, trust_env=False)

    @staticmethod
    def is_local_model_name(model: str) -> bool:
        return bool(model) and not model.casefold().endswith("-cloud")

    def is_ready(self) -> bool:
        try:
            with self._client(1.5) as client:
                return client.get("/api/tags").is_success
        except httpx.HTTPError:
            return False

    def start_hidden(self, timeout: float = 20) -> bool:
        if self.is_ready():
            return False
        executable = shutil.which("ollama")
        if not executable:
            raise OllamaError("Ollama is not installed or is not available on PATH.")
        flags = 0
        startupinfo = None
        if os.name == "nt":
            flags = subprocess.CREATE_NO_WINDOW
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        environment = os.environ.copy()
        environment["OLLAMA_HOST"] = LOCAL_OLLAMA_HOST
        environment["OLLAMA_NO_CLOUD"] = "1"
        self._owned_process = subprocess.Popen(
            [executable, "serve"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=flags,
            startupinfo=startupinfo,
            env=environment,
        )
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.is_ready():
                return True
            if self._owned_process.poll() is not None:
                break
            time.sleep(0.25)
        self.stop_owned()
        raise OllamaError("Ollama did not become ready in time.")

    def owns_process(self) -> bool:
        return self._owned_process is not None and self._owned_process.poll() is None

    def stop_owned(self, timeout: float = 3.0) -> bool:
        """Stop only the Ollama server process launched by this manager."""
        process = self._owned_process
        self._owned_process = None
        if process is None or process.poll() is not None:
            return False
        process.terminate()
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=2.0)
        return True

    def installed_models(self) -> set[str]:
        with self._client(10) as client:
            response = client.get("/api/tags")
            response.raise_for_status()
            return {
                item["name"]
                for item in response.json().get("models", [])
                if self.is_local_model_name(item.get("name", ""))
            }

    def pull_model(self, model: str, progress: Callable[[str], None] | None = None) -> None:
        if not model or any(character.isspace() for character in model):
            raise OllamaError("Enter a valid Ollama model name without spaces.")
        if not self.is_local_model_name(model):
            raise OllamaError("Ollama cloud models are disabled; choose a model stored locally.")
        with self._client(None) as client:
            with client.stream(
                "POST",
                "/api/pull",
                json={"name": model, "stream": True},
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
        if not self.is_local_model_name(self.model):
            raise OllamaError("Ollama cloud models are disabled; choose a model stored locally.")
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "options": {"temperature": 0.8, "num_ctx": 16384},
        }
        with self._client(None) as client:
            with client.stream("POST", "/api/chat", json=payload) as response:
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
