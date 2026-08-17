from __future__ import annotations

import json
import os
import shutil
import struct
import subprocess
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

import httpx

from .settings import LOCAL_OLLAMA_URL

PYTHON_MINIMUM = (3, 11)
PYTHON_OFFICIAL_URL = "https://www.python.org/downloads/windows/"
OLLAMA_OFFICIAL_URL = "https://ollama.com/download/windows"
OLLAMA_MODELS_URL = "https://ollama.com/search"

CommandRunner = Callable[[list[str], float], subprocess.CompletedProcess[str]]


@dataclass(frozen=True)
class DependencyStatus:
    component_id: str
    display_name: str
    state: str
    detail: str
    path: str = ""
    version: str = ""
    can_auto_install: bool = False
    official_url: str = ""

    @property
    def ready(self) -> bool:
        return self.state == "ready"


@dataclass(frozen=True)
class EnvironmentReport:
    python: DependencyStatus
    ollama: DependencyStatus
    ollama_api: DependencyStatus
    models: tuple[str, ...]
    free_disk_bytes: int

    @property
    def python_ready(self) -> bool:
        return self.python.ready

    @property
    def chat_ready(self) -> bool:
        return self.ollama.ready and self.ollama_api.ready and bool(self.models)


def _hidden_process_kwargs() -> dict[str, object]:
    if os.name != "nt":
        return {}
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return {
        "creationflags": subprocess.CREATE_NO_WINDOW,
        "startupinfo": startupinfo,
    }


def run_probe(
    command: list[str], timeout: float = 8.0
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        **_hidden_process_kwargs(),
    )


def _unique_existing_paths(paths: Iterable[str | Path | None]) -> list[Path]:
    found: list[Path] = []
    seen: set[str] = set()
    for candidate in paths:
        if not candidate:
            continue
        path = Path(candidate).expanduser()
        try:
            resolved = path.resolve()
        except OSError:
            resolved = path.absolute()
        key = os.path.normcase(str(resolved))
        if key in seen or not resolved.is_file():
            continue
        seen.add(key)
        found.append(resolved)
    return found


def _windows_python_candidates() -> list[Path]:
    if os.name != "nt":
        return []
    local_app_data = os.environ.get("LOCALAPPDATA")
    program_files = os.environ.get("PROGRAMFILES")
    roots = []
    if local_app_data:
        roots.extend(
            [
                Path(local_app_data) / "Programs" / "Python",
                Path(local_app_data) / "Python",
            ]
        )
    if program_files:
        roots.append(Path(program_files))
    candidates: list[Path] = []
    for root in roots:
        if not str(root) or not root.is_dir():
            continue
        for pattern in ("Python*/python.exe", "pythoncore-*/python.exe"):
            candidates.extend(root.glob(pattern))
    return candidates


def _safe_path_command(name: str) -> str | None:
    candidate = shutil.which(name)
    if not candidate:
        return None
    # Executing the Microsoft Store aliases can begin an installation. Detection must be read-only.
    if os.name == "nt" and "\\microsoft\\windowsapps\\" in candidate.casefold():
        return None
    return candidate


def detect_python(
    configured_path: str = "",
    runner: CommandRunner = run_probe,
) -> DependencyStatus:
    candidates = _unique_existing_paths(
        [
            configured_path,
            _safe_path_command("python"),
            _safe_path_command("python3"),
            *_windows_python_candidates(),
        ]
    )
    unsupported: tuple[Path, tuple[int, int, int]] | None = None
    probe = (
        "import json, struct, sys; "
        "print(json.dumps({'path': sys.executable, "
        "'version': list(sys.version_info[:3]), 'bits': struct.calcsize('P') * 8}))"
    )
    for candidate in candidates:
        try:
            process = runner([str(candidate), "-c", probe], 8.0)
            if process.returncode != 0:
                continue
            values = json.loads(process.stdout.strip().splitlines()[-1])
            version_values = values.get("version", [])
            version = tuple(int(value) for value in version_values[:3])
            if len(version) != 3:
                continue
            executable = Path(str(values.get("path", candidate))).resolve()
            bits = int(values.get("bits", struct.calcsize("P") * 8))
            if version[:2] >= PYTHON_MINIMUM:
                version_text = ".".join(str(value) for value in version)
                return DependencyStatus(
                    component_id="python-runtime",
                    display_name="Python runtime",
                    state="ready",
                    detail=f"Python {version_text} ({bits}-bit)",
                    path=str(executable),
                    version=version_text,
                    can_auto_install=True,
                    official_url=PYTHON_OFFICIAL_URL,
                )
            unsupported = (executable, version)
        except (
            IndexError,
            json.JSONDecodeError,
            OSError,
            subprocess.SubprocessError,
            TypeError,
            ValueError,
        ):
            continue
    if unsupported:
        executable, version = unsupported
        version_text = ".".join(str(value) for value in version)
        return DependencyStatus(
            component_id="python-runtime",
            display_name="Python runtime",
            state="unsupported",
            detail=f"Python {version_text} is installed; Senpai requires Python 3.11 or newer.",
            path=str(executable),
            version=version_text,
            can_auto_install=True,
            official_url=PYTHON_OFFICIAL_URL,
        )
    return DependencyStatus(
        component_id="python-runtime",
        display_name="Python runtime",
        state="missing",
        detail="Python 3.11 or newer was not found. Editing works, but Run Python File is disabled.",
        can_auto_install=os.name == "nt",
        official_url=PYTHON_OFFICIAL_URL,
    )


def _windows_ollama_candidates() -> list[Path]:
    if os.name != "nt":
        return []
    local_app_data_value = os.environ.get("LOCALAPPDATA")
    if not local_app_data_value:
        return []
    local_app_data = Path(local_app_data_value)
    return [
        local_app_data / "Programs" / "Ollama" / "ollama.exe",
        local_app_data / "Ollama" / "ollama.exe",
    ]


def detect_ollama(
    configured_path: str = "",
    runner: CommandRunner = run_probe,
) -> DependencyStatus:
    candidates = _unique_existing_paths(
        [configured_path, shutil.which("ollama"), *_windows_ollama_candidates()]
    )
    for candidate in candidates:
        try:
            process = runner([str(candidate), "--version"], 8.0)
            if process.returncode != 0:
                continue
            output = (process.stdout or process.stderr).strip().splitlines()
            version_text = output[-1].strip() if output else "Installed"
            return DependencyStatus(
                component_id="ollama",
                display_name="Ollama",
                state="ready",
                detail=version_text,
                path=str(candidate),
                version=version_text,
                can_auto_install=True,
                official_url=OLLAMA_OFFICIAL_URL,
            )
        except (OSError, subprocess.SubprocessError):
            continue
    return DependencyStatus(
        component_id="ollama",
        display_name="Ollama",
        state="missing",
        detail="Ollama was not found. The editor remains available, but local AI chat is disabled.",
        can_auto_install=os.name == "nt",
        official_url=OLLAMA_OFFICIAL_URL,
    )


def detect_ollama_api(
    base_url: str = LOCAL_OLLAMA_URL,
) -> tuple[DependencyStatus, tuple[str, ...]]:
    try:
        with httpx.Client(base_url=base_url, timeout=2.0, trust_env=False) as client:
            response = client.get("/api/tags")
            response.raise_for_status()
            models = tuple(
                sorted(
                    {
                        str(item.get("name", ""))
                        for item in response.json().get("models", [])
                        if item.get("name")
                        and not str(item.get("name")).casefold().endswith("-cloud")
                    },
                    key=str.casefold,
                )
            )
        detail = (
            "Local API ready"
            if models
            else "Local API ready; no local model is installed"
        )
        return (
            DependencyStatus(
                component_id="ollama-api",
                display_name="Ollama local service",
                state="ready",
                detail=detail,
                path=base_url,
            ),
            models,
        )
    except (httpx.HTTPError, TypeError, ValueError):
        return (
            DependencyStatus(
                component_id="ollama-api",
                display_name="Ollama local service",
                state="stopped",
                detail=f"Nothing is responding at {base_url}.",
                path=base_url,
            ),
            (),
        )


def scan_environment(
    configured_python: str = "",
    configured_ollama: str = "",
    disk_path: Path | None = None,
    runner: CommandRunner = run_probe,
) -> EnvironmentReport:
    python = detect_python(configured_python, runner)
    ollama = detect_ollama(configured_ollama, runner)
    ollama_api, models = detect_ollama_api()
    target = disk_path or Path.home()
    try:
        free_disk_bytes = shutil.disk_usage(target).free
    except OSError:
        free_disk_bytes = 0
    return EnvironmentReport(
        python=python,
        ollama=ollama,
        ollama_api=ollama_api,
        models=models,
        free_disk_bytes=free_disk_bytes,
    )
