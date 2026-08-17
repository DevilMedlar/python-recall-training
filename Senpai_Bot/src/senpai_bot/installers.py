from __future__ import annotations

import os
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from .dependencies import (
    OLLAMA_OFFICIAL_URL,
    PYTHON_OFFICIAL_URL,
    DependencyStatus,
    detect_ollama,
    detect_python,
)
from .ownership import ComponentRecord, OwnershipManifest

OLLAMA_PACKAGE_ID = "Ollama.Ollama"
PYTHON_MANAGER_PRODUCT_ID = "9NQ7512CXL7T"
WINGET_SOURCE = "winget"
MSSTORE_SOURCE = "msstore"

CommandRunner = Callable[[list[str], float], subprocess.CompletedProcess[str]]
Detector = Callable[[str], DependencyStatus]


class InstallError(RuntimeError):
    pass


@dataclass(frozen=True)
class InstallOutcome:
    component_id: str
    detail: str
    path: str
    version: str
    installed: bool


def run_install_command(
    command: list[str],
    timeout: float = 1800.0,
) -> subprocess.CompletedProcess[str]:
    process_options: dict[str, object] = {}
    if os.name == "nt":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process_options = {
            "creationflags": subprocess.CREATE_NO_WINDOW,
            "startupinfo": startupinfo,
        }
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        **process_options,
    )


def _failure_detail(process: subprocess.CompletedProcess[str]) -> str:
    text = (
        process.stderr or process.stdout or "No installer output was returned."
    ).strip()
    return text[-3000:]


def _existing_file(candidates: list[str | Path | None]) -> str | None:
    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate)
        if path.is_file():
            return str(path.resolve())
    return None


class InstallCoordinator:
    """Run only explicitly approved, exact-package Windows dependency installs."""

    def __init__(
        self,
        manifest: OwnershipManifest,
        runner: CommandRunner = run_install_command,
        which: Callable[[str], str | None] = shutil.which,
        python_detector: Detector = detect_python,
        ollama_detector: Detector = detect_ollama,
        platform_name: str | None = None,
    ):
        self.manifest = manifest
        self.runner = runner
        self.which = which
        self.python_detector = python_detector
        self.ollama_detector = ollama_detector
        self.platform_name = platform_name or os.name

    def _winget(self) -> str:
        winget = self.which("winget")
        if not winget:
            raise InstallError(
                "Windows Package Manager (winget) is unavailable. "
                "Use the official manual-install link instead."
            )
        return winget

    def install_ollama(self, configured_path: str = "") -> InstallOutcome:
        existing = self.ollama_detector(configured_path)
        if existing.ready:
            return InstallOutcome(
                component_id="ollama",
                detail="Ollama was already installed; Senpai did not claim ownership.",
                path=existing.path,
                version=existing.version,
                installed=False,
            )
        if self.platform_name != "nt":
            raise InstallError(
                "Automatic Ollama installation is supported only on Windows."
            )
        command = [
            self._winget(),
            "install",
            "--id",
            OLLAMA_PACKAGE_ID,
            "--exact",
            "--source",
            WINGET_SOURCE,
            "--accept-source-agreements",
            "--accept-package-agreements",
            "--disable-interactivity",
        ]
        process = self.runner(command, 1800.0)
        installed = self.ollama_detector("")
        if not installed.ready:
            if process.returncode == 0:
                self.manifest.record(
                    ComponentRecord(
                        component_id="ollama",
                        kind="runtime",
                        source=f"{WINGET_SOURCE}:{OLLAMA_PACKAGE_ID}",
                        install_method="winget-exact-package",
                        installed_by_senpai=True,
                        previously_present=False,
                        verification=(
                            "WinGet reported installation success; executable verification "
                            "is pending"
                        ),
                        removal_policy="confirmation-required",
                        metadata={"official_url": OLLAMA_OFFICIAL_URL},
                    )
                )
            if process.returncode != 0:
                raise InstallError(
                    f"Ollama installation failed.\n\n{_failure_detail(process)}"
                )
            raise InstallError(
                "WinGet reported success, but Senpai could not verify ollama.exe. "
                "Rescan after restarting Senpai or choose the executable manually."
            )
        self.manifest.record(
            ComponentRecord(
                component_id="ollama",
                kind="runtime",
                version=installed.version,
                source=f"{WINGET_SOURCE}:{OLLAMA_PACKAGE_ID}",
                install_method="winget-exact-package",
                installed_by_senpai=True,
                previously_present=False,
                path=installed.path,
                verification="WinGet exact package identity and manifest SHA-256 verification",
                removal_policy="confirmation-required",
                metadata={"official_url": OLLAMA_OFFICIAL_URL},
            )
        )
        return InstallOutcome(
            component_id="ollama",
            detail=(
                "Official Ollama installation verified."
                if process.returncode == 0
                else "Ollama was verified despite a WinGet warning."
            ),
            path=installed.path,
            version=installed.version,
            installed=True,
        )

    def _python_manager(self) -> str | None:
        local_app_data_value = os.environ.get("LOCALAPPDATA")
        local_app_data = Path(local_app_data_value) if local_app_data_value else None
        return _existing_file(
            [
                self.which("pymanager"),
                local_app_data / "Microsoft" / "WindowsApps" / "pymanager.exe"
                if local_app_data
                else None,
                (
                    local_app_data
                    / "Microsoft"
                    / "WindowsApps"
                    / "PythonSoftwareFoundation.PythonManager_3847v3x7pw1km"
                    / "pymanager.exe"
                )
                if local_app_data
                else None,
                (
                    local_app_data
                    / "Microsoft"
                    / "WindowsApps"
                    / "PythonSoftwareFoundation.PythonManager_qbz5n2kfra8p0"
                    / "pymanager.exe"
                )
                if local_app_data
                else None,
            ]
        )

    def _python_manager_version(self, manager: str) -> str:
        try:
            process = self.runner([manager, "--version"], 30.0)
        except (OSError, subprocess.SubprocessError):
            return ""
        if process.returncode != 0:
            return ""
        output = (process.stdout or process.stderr).strip().splitlines()
        return output[-1].strip() if output else ""

    def _record_python_manager(self, manager: str, verification: str) -> None:
        self.manifest.record(
            ComponentRecord(
                component_id="python-install-manager",
                kind="package-manager",
                version=self._python_manager_version(manager) if manager else "",
                source=f"{MSSTORE_SOURCE}:{PYTHON_MANAGER_PRODUCT_ID}",
                install_method="winget-exact-product",
                installed_by_senpai=True,
                previously_present=False,
                path=manager,
                verification=verification,
                removal_policy="advanced-confirmation-required",
                metadata={"official_url": PYTHON_OFFICIAL_URL},
            )
        )

    def install_python(self, configured_path: str = "") -> InstallOutcome:
        existing = self.python_detector(configured_path)
        if existing.ready:
            return InstallOutcome(
                component_id="python-runtime",
                detail="A compatible Python was already installed; Senpai did not claim ownership.",
                path=existing.path,
                version=existing.version,
                installed=False,
            )
        if self.platform_name != "nt":
            raise InstallError(
                "Automatic Python installation is supported only on Windows."
            )

        manager = self._python_manager()
        if manager is None:
            command = [
                self._winget(),
                "install",
                PYTHON_MANAGER_PRODUCT_ID,
                "--exact",
                "--source",
                MSSTORE_SOURCE,
                "--accept-source-agreements",
                "--accept-package-agreements",
                "--disable-interactivity",
            ]
            process = self.runner(command, 1800.0)
            manager = self._python_manager()
            if manager is None:
                if process.returncode == 0:
                    self._record_python_manager(
                        "",
                        "WinGet reported installation success; executable verification is pending",
                    )
                if process.returncode != 0:
                    raise InstallError(
                        f"Python Install Manager setup failed.\n\n{_failure_detail(process)}"
                    )
                raise InstallError(
                    "WinGet reported success, but pymanager.exe was not found. "
                    "Restart Senpai and rescan, or use the official Python page."
                )
            self._record_python_manager(
                manager,
                "Microsoft Store exact product identity and package verification",
            )

        python_tag = f"{sys.version_info.major}.{sys.version_info.minor}"
        process = self.runner([manager, "install", python_tag], 1800.0)
        installed = self.python_detector("")
        if not installed.ready:
            if process.returncode != 0:
                raise InstallError(
                    f"Python {python_tag} installation failed.\n\n{_failure_detail(process)}"
                )
            raise InstallError(
                "Python Install Manager reported success, but Senpai could not verify the runtime. "
                "Rescan after restarting Senpai or choose python.exe manually."
            )

        self.manifest.record(
            ComponentRecord(
                component_id="python-runtime",
                kind="runtime",
                version=installed.version,
                source=f"python-install-manager:{python_tag}",
                install_method="pymanager-explicit-tag",
                installed_by_senpai=True,
                previously_present=False,
                path=installed.path,
                verification="Runtime installed by the official Python Install Manager",
                removal_policy="advanced-confirmation-required",
                metadata={"official_url": PYTHON_OFFICIAL_URL, "tag": python_tag},
            )
        )
        return InstallOutcome(
            component_id="python-runtime",
            detail=(
                f"Official Python {installed.version} installation verified."
                if process.returncode == 0
                else (
                    f"Python {installed.version} was verified despite an install-manager warning."
                )
            ),
            path=installed.path,
            version=installed.version,
            installed=True,
        )
