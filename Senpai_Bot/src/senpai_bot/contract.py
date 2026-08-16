from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


CONTRACT_FILES = ("rules.md", "SECURITY.md", "README.md")
TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_'-]{2,}")


@dataclass(frozen=True)
class Section:
    source: str
    heading: str
    text: str
    tokens: frozenset[str]


class ContractStore:
    """Loads the unmodified contract and retrieves request-relevant sections."""

    def __init__(self, root: Path):
        self.root = root
        self.documents: dict[str, str] = {}
        self.sections: list[Section] = []
        self.reload()

    def reload(self) -> None:
        documents: dict[str, str] = {}
        sections: list[Section] = []
        for name in CONTRACT_FILES:
            path = self.root / name
            if not path.is_file():
                raise FileNotFoundError(f"Required contract file is missing: {path}")
            text = path.read_text(encoding="utf-8")
            documents[name] = text
            sections.extend(self._split(name, text))
        self.documents = documents
        self.sections = sections

    @staticmethod
    def _tokens(text: str) -> frozenset[str]:
        return frozenset(token.lower() for token in TOKEN_RE.findall(text))

    def _split(self, source: str, text: str) -> list[Section]:
        parts = re.split(r"(?m)(?=^#{1,4}\s+)", text)
        result: list[Section] = []
        for index, part in enumerate(parts):
            cleaned = part.strip()
            if not cleaned:
                continue
            first = cleaned.splitlines()[0]
            heading = first.lstrip("# ") if first.startswith("#") else f"Preamble {index + 1}"
            result.append(Section(source, heading, cleaned, self._tokens(cleaned)))
        return result

    @property
    def persona_core(self) -> str:
        wanted = {
            "Tutor persona",
            "Mandatory startup protocol for the Senpai",
            "Factual integrity",
            "Security exception",
            "Rule 14 - Persona is mandatory, but technical clarity wins",
            "Persona integration",
            "Adult reward and scene content",
            "Technical and factual boundary",
        }
        chunks = [s.text for s in self.sections if s.heading in wanted]
        return "\n\n".join(chunks)

    def relevant_context(self, query: str, limit: int = 6, max_chars: int = 18_000) -> str:
        query_tokens = self._tokens(query)
        scored: list[tuple[float, Section]] = []
        for section in self.sections:
            overlap = query_tokens & section.tokens
            if not overlap:
                continue
            title_hits = len(query_tokens & self._tokens(section.heading))
            score = len(overlap) / max(len(query_tokens), 1) + title_hits * 0.75
            scored.append((score, section))
        scored.sort(key=lambda item: item[0], reverse=True)
        selected: list[str] = []
        used = 0
        for _, section in scored[:limit]:
            block = f"[Contract: {section.source} — {section.heading}]\n{section.text}"
            if used + len(block) > max_chars:
                break
            selected.append(block)
            used += len(block)
        return "\n\n".join(selected)

    def full_contract(self) -> str:
        return "\n\n".join(f"===== {name} =====\n{text}" for name, text in self.documents.items())
