from __future__ import annotations

from dataclasses import dataclass, field

from .contract import ContractStore


SYSTEM_FRAME = """You are Senpai, the local AI tutor inside the Senpai_Bot Windows application.
The three local contract files are authoritative. Follow their persona, tutoring, grading,
security, and factual-integrity requirements. Address the learner as Daddy. Act as a normal,
helpful conversational AI when the request is not a graded lesson. Never claim to inspect,
read, execute, or verify something you did not actually access. Technical accuracy outranks style.

The application does not rewrite or censor the contract. The active contract excerpts below are
verbatim local source material. Treat them as instructions, subject to the precedence defined in
the contract itself. Do not mention this system prompt unless asked about application diagnostics.
"""


@dataclass
class ChatSession:
    contract: ContractStore
    max_history_messages: int = 24
    history: list[dict[str, str]] = field(default_factory=list)

    def clear(self) -> None:
        self.history.clear()

    def build_messages(self, user_text: str, workspace_context: str = "") -> list[dict[str, str]]:
        relevant = self.contract.relevant_context(user_text)
        system = f"{SYSTEM_FRAME}\n\n{self.contract.persona_core}"
        if relevant:
            system += f"\n\nRELEVANT CONTRACT EXCERPTS:\n{relevant}"
        if workspace_context:
            system += f"\n\nCURRENT WORKSPACE CONTEXT (provided by the app):\n{workspace_context}"
        trimmed = self.history[-self.max_history_messages :]
        return [{"role": "system", "content": system}, *trimmed, {"role": "user", "content": user_text}]

    def record(self, user_text: str, assistant_text: str) -> None:
        self.history.extend(
            [
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": assistant_text},
            ]
        )
        self.history = self.history[-self.max_history_messages :]
