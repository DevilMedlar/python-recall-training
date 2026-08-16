"""Build the local model's startup context.

Compact mode keeps the persona active and retrieves repository state on
demand. Full mode retains verbatim contract injection for models configured
with a sufficiently large context window.
"""

from __future__ import annotations

from pathlib import Path

CORE_CONTRACT_FILES = ["README.md", "rules.md", "SECURITY.md"]

CHAT_BEHAVIOR_ANCHOR = """You are in an interactive chat session.
- Respond to every ordinary user message with a natural, useful assistant reply in the active Senpai persona.
- Greetings, check-ins, and casual conversation never require a tool call.
- Use repository tools only when current file state, code execution, grading evidence, or a requested file change is actually needed.
- Never describe tool-calling mechanics as the answer to Daddy; after any tool call, return a normal conversational response.
- Keep technical explanations accurate and clear while maintaining the persona."""


def _read_if_exists(path: Path) -> str | None:
    if path.is_file():
        return path.read_text(encoding="utf-8", errors="replace")
    return None


def build_startup_context(
    repo_root: Path,
    persona_prompt: str,
    context_mode: str = "compact",
) -> str:
    """Build a system prompt sized for the configured local model.

    ``compact`` keeps the chat/persona instructions in the active context and
    leaves the large contract files available through repository tools.
    ``full`` preserves the original verbatim-injection behavior for models
    configured with a sufficiently large context window.
    """
    sections: list[str] = []

    if context_mode == "full":
        sections.append(
            "The following files are the FULL, VERBATIM current contents of this repository's "
            "training contract. Repository-state facts younger than this session start are "
            "not included; use repository tools to inspect them before teaching or grading."
        )

        for filename in CORE_CONTRACT_FILES:
            content = _read_if_exists(repo_root / filename)
            if content is None:
                sections.append(f"--- {filename} ---\n[File not found in repository root.]")
            else:
                sections.append(f"--- {filename} ---\n{content}")

        grades = _read_if_exists(repo_root / "overall_grades.md")
        if grades is not None:
            sections.append(f"--- overall_grades.md ---\n{grades}")
        else:
            sections.append(
                "--- overall_grades.md ---\n[Does not exist yet. This is a fresh-start run. "
                "Create it when curriculum-level state first needs to persist.]"
            )
    else:
        sections.append(
            "The repository's full training contract is stored in README.md, rules.md, and "
            "SECURITY.md. This session uses compact context so the local model can remain "
            "responsive. Before teaching, grading, or changing curriculum state, use read_file "
            "and list_dir to inspect the specific current contract, grade, challenge, and learner "
            "files required for that action. Never invent repository state."
        )

    # Keep the active identity and conversational behavior at the end. Many
    # local models truncate the oldest tokens when a prompt exceeds num_ctx.
    if persona_prompt.strip():
        sections.append(persona_prompt.strip())
    sections.append(CHAT_BEHAVIOR_ANCHOR)

    return "\n\n".join(sections)
