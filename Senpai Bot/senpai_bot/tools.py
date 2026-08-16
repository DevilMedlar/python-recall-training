"""Sandboxed workspace tools exposed to the model via Ollama tool-calling.

These let the model actually inspect and update repository/training-state
files at runtime (Rule 0 / Rule 3 / Rule 4 of rules.md require grading from
real current file state, not memory). All paths are resolved and clamped to
stay inside the repository root -- no path may escape it.

The core contract files are protected from being overwritten by the model,
since rules.md Rule 5 distinguishes tutor-owned training-state files (grade
records, weakness tracking, challenge instructions) from the contract itself.
"""

from __future__ import annotations

import json
from pathlib import Path

PROTECTED_FILES = {"README.md", "rules.md", "SECURITY.md", "gitignore.txt"}


class ToolError(RuntimeError):
    pass


class WorkspaceTools:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root.resolve()

    def _resolve(self, rel_path: str) -> Path:
        candidate = (self.repo_root / rel_path).resolve()
        try:
            candidate.relative_to(self.repo_root)
        except ValueError:
            raise ToolError(f"Path '{rel_path}' escapes the repository root; refused.")
        return candidate

    def read_file(self, path: str) -> str:
        target = self._resolve(path)
        if not target.is_file():
            raise ToolError(f"File not found: {path}")
        return target.read_text(encoding="utf-8", errors="replace")

    def list_dir(self, path: str = ".") -> list[str]:
        target = self._resolve(path)
        if not target.is_dir():
            raise ToolError(f"Not a directory: {path}")
        entries = []
        for child in sorted(target.iterdir()):
            suffix = "/" if child.is_dir() else ""
            entries.append(str(child.relative_to(self.repo_root)).replace("\\", "/") + suffix)
        return entries

    def write_file(self, path: str, content: str) -> str:
        rel_norm = path.replace("\\", "/").lstrip("./")
        if rel_norm in PROTECTED_FILES:
            raise ToolError(
                f"Refused: '{path}' is a protected contract file and cannot be modified by the tutor."
            )
        target = self._resolve(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} characters to {path}"

    def dispatch(self, name: str, arguments: dict) -> str:
        try:
            if name == "read_file":
                return self.read_file(arguments["path"])
            if name == "list_dir":
                return json.dumps(self.list_dir(arguments.get("path", ".")))
            if name == "write_file":
                return self.write_file(arguments["path"], arguments["content"])
            raise ToolError(f"Unknown tool: {name}")
        except ToolError as exc:
            return f"ERROR: {exc}"
        except KeyError as exc:
            return f"ERROR: missing required argument {exc}"


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": (
                "Read the full current contents of a file in the repository, relative to "
                "the repository root. Use this to actually inspect overall_grades.md, "
                "stage grades files, challenge instructions, or Daddy's learner code "
                "before grading -- never rely on memory when the file can answer the question."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Repo-relative file path, e.g. 'overall_grades.md' or 'stages/01-foundations/attempt.py'.",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List files and folders in a repository-relative directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Repo-relative directory path. Defaults to the repository root.",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": (
                "Create or overwrite a tutor-owned training-state file (e.g. overall_grades.md, "
                "a stage grades file, challenge instructions, weakness-tracking records). "
                "Refused for the core contract files (README.md, rules.md, SECURITY.md) and for "
                "silently rewriting Daddy's own learner code into a passing solution."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Repo-relative file path to write."},
                    "content": {"type": "string", "description": "Full new file content."},
                },
                "required": ["path", "content"],
            },
        },
    },
]
