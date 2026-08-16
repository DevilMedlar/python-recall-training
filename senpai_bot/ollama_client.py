"""Minimal Ollama /api/chat client using only the standard library."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any


class OllamaError(RuntimeError):
    pass


class OllamaClient:
    def __init__(self, host: str, model: str, timeout: float = 120.0) -> None:
        self.host = host.rstrip("/")
        self.model = model
        self.timeout = timeout

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Send a chat request and return the assistant message dict.

        Non-streaming: simpler and reliable for a tool-calling loop.
        """
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }
        if tools:
            payload["tools"] = tools

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.host}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8")
        except urllib.error.URLError as exc:
            raise OllamaError(
                f"Could not reach Ollama at {self.host}. Is `ollama serve` running? ({exc})"
            ) from exc

        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:
            raise OllamaError(f"Ollama returned non-JSON response: {body[:500]}") from exc

        if "error" in parsed:
            raise OllamaError(f"Ollama error: {parsed['error']}")

        message = parsed.get("message")
        if not message:
            return {"role": "assistant", "content": ""}
        return message

    def list_models(self) -> list[str]:
        req = urllib.request.Request(f"{self.host}/api/tags", method="GET")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise OllamaError(
                f"Could not reach Ollama at {self.host}. Is `ollama serve` running? ({exc})"
            ) from exc
        return [m["name"] for m in body.get("models", [])]
