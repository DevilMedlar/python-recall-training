from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass

OFFICIAL_MODEL_LIBRARY_URL = "https://ollama.com/search"


@dataclass(frozen=True)
class ModelOption:
    name: str
    title: str
    purpose: str
    approximate_download_gb: float
    publisher: str
    license_name: str
    official_url: str
    memory_note: str

    @property
    def display_text(self) -> str:
        return f"{self.title} — about {self.approximate_download_gb:g} GB"


RECOMMENDED_MODELS = (
    ModelOption(
        name="llama3.1:8b",
        title="Llama 3.1 8B (balanced tutor)",
        purpose="Balanced general conversation, tutoring, and Python explanations.",
        approximate_download_gb=4.9,
        publisher="Meta",
        license_name="Llama 3.1 Community License",
        official_url="https://ollama.com/library/llama3.1:8b",
        memory_note="The lightest balanced default in this list.",
    ),
    ModelOption(
        name="qwen2.5-coder:7b",
        title="Qwen 2.5 Coder 7B (coding focused)",
        purpose="Code explanation, code reasoning, generation, and repair.",
        approximate_download_gb=4.7,
        publisher="Alibaba Cloud",
        license_name="Apache License 2.0",
        official_url="https://ollama.com/library/qwen2.5-coder:7b",
        memory_note="Similar download size to the balanced default, with a stronger coding focus.",
    ),
    ModelOption(
        name="qwen2.5-coder:14b",
        title="Qwen 2.5 Coder 14B (stronger coding)",
        purpose="Stronger local code reasoning when the computer has enough memory.",
        approximate_download_gb=9.0,
        publisher="Alibaba Cloud",
        license_name="Apache License 2.0",
        official_url="https://ollama.com/library/qwen2.5-coder:14b",
        memory_note="Larger and usually slower; intended for machines with more available RAM or VRAM.",
    ),
)


def model_by_name(name: str) -> ModelOption | None:
    return next((model for model in RECOMMENDED_MODELS if model.name == name), None)


def canonical_installed_model(requested: str, installed: Collection[str]) -> str | None:
    if requested in installed:
        return requested
    implicit_latest = f"{requested}:latest" if ":" not in requested else ""
    return implicit_latest if implicit_latest in installed else None
