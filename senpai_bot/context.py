"""Builds the session's starting context out of the actual repository files.

Implements the mechanical half of README.md / rules.md Rule 0: the three
core contract files are read in full and injected verbatim every session so
the model is never relying on a paraphrase. overall_grades.md is included
too, when it exists, since Rule 0 requires reading it before the first
teaching/grading action. Everything else (stage grades files, active
challenge instructions, learner code) is left to the model's read_file /
list_dir tool calls, because that state changes during the session and must
be read fresh at grading time (Rule 3 / Rule 4), not baked in at startup.
"""

from __future__ import annotations

from pathlib import Path

CORE_CONTRACT_FILES = ["README.md", "rules.md", "SECURITY.md"]


def _read_if_exists(path: Path) -> str | None:
    if path.is_file():
        return path.read_text(encoding="utf-8", errors="replace")
    return None


def build_startup_context(repo_root: Path, persona_prompt: str) -> str:
    sections: list[str] = []

    if persona_prompt.strip():
        sections.append(persona_prompt.strip())

    sections.append(
        "The following files are the FULL, VERBATIM current contents of this repository's "
        "training contract, provided so you have actually read them rather than recalling "
        "them from memory (rules.md Rule 0 and Rule 3). Repository-state facts younger than "
        "this session start (grades, weaknesses, learner code) are NOT included below -- use "
        "the read_file / list_dir tools to inspect those before teaching or grading anything."
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
            "--- overall_grades.md ---\n[Does not exist yet. This is a fresh-start run per "
            "README.md's Fresh-start state section unless the learner says otherwise. Create "
            "this file the first time curriculum-level state needs to persist, per Rule 19.]"
        )

    return "\n\n".join(sections)
