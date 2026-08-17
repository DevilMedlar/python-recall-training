import subprocess
import sys

import pytest

from senpai_bot.dependencies import DependencyStatus
from senpai_bot.installers import (
    MSSTORE_SOURCE,
    OLLAMA_PACKAGE_ID,
    PYTHON_MANAGER_PRODUCT_ID,
    WINGET_SOURCE,
    InstallCoordinator,
    InstallError,
)
from senpai_bot.ownership import OwnershipManifest


def _status(component_id: str, state: str, path: str = "", version: str = ""):
    return DependencyStatus(
        component_id=component_id,
        display_name=component_id,
        state=state,
        detail=state,
        path=path,
        version=version,
    )


def test_ollama_install_uses_exact_trusted_package_and_records_ownership(tmp_path):
    manifest = OwnershipManifest.load(tmp_path / "ownership.json", "0.0.4")
    statuses = iter(
        (
            _status("ollama", "missing"),
            _status("ollama", "ready", r"C:\Ollama\ollama.exe", "0.32.14"),
        )
    )
    commands: list[list[str]] = []

    def runner(command: list[str], _timeout: float):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="Installed", stderr="")

    coordinator = InstallCoordinator(
        manifest,
        runner=runner,
        which=lambda name: r"C:\Windows\winget.exe" if name == "winget" else None,
        ollama_detector=lambda _path: next(statuses),
        platform_name="nt",
    )
    outcome = coordinator.install_ollama()

    assert outcome.installed is True
    assert commands == [
        [
            r"C:\Windows\winget.exe",
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
    ]
    record = manifest.get("ollama")
    assert record is not None
    assert record.installed_by_senpai is True
    assert record.source == f"{WINGET_SOURCE}:{OLLAMA_PACKAGE_ID}"


def test_preexisting_ollama_is_never_claimed_or_reinstalled(tmp_path):
    manifest = OwnershipManifest.load(tmp_path / "ownership.json", "0.0.4")

    def must_not_run(_command: list[str], _timeout: float):
        raise AssertionError("must not run")

    coordinator = InstallCoordinator(
        manifest,
        runner=must_not_run,
        ollama_detector=lambda _path: _status(
            "ollama", "ready", r"C:\Ollama\ollama.exe", "0.32.14"
        ),
        platform_name="nt",
    )

    outcome = coordinator.install_ollama()

    assert outcome.installed is False
    assert manifest.get("ollama") is None


def test_successful_winget_step_is_journaled_when_executable_detection_is_delayed(
    tmp_path,
):
    manifest = OwnershipManifest.load(tmp_path / "ownership.json", "0.0.4")
    coordinator = InstallCoordinator(
        manifest,
        runner=lambda command, _timeout: subprocess.CompletedProcess(
            command, 0, stdout="Installed", stderr=""
        ),
        which=lambda name: r"C:\Windows\winget.exe" if name == "winget" else None,
        ollama_detector=lambda _path: _status("ollama", "missing"),
        platform_name="nt",
    )

    with pytest.raises(InstallError, match="could not verify ollama.exe"):
        coordinator.install_ollama()

    record = manifest.get("ollama")
    assert record is not None
    assert record.installed_by_senpai is True
    assert "pending" in record.verification


def test_python_runtime_uses_official_manager_and_explicit_version_tag(tmp_path):
    manifest = OwnershipManifest.load(tmp_path / "ownership.json", "0.0.4")
    manager = tmp_path / "pymanager.exe"
    manager.touch()
    statuses = iter(
        (
            _status("python-runtime", "missing"),
            _status("python-runtime", "ready", r"C:\Python\python.exe", "3.14.7"),
        )
    )
    commands: list[list[str]] = []

    def runner(command: list[str], _timeout: float):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="Installed", stderr="")

    def which(name: str):
        if name == "pymanager":
            return str(manager)
        if name == "winget":
            return r"C:\Windows\winget.exe"
        return None

    coordinator = InstallCoordinator(
        manifest,
        runner=runner,
        which=which,
        python_detector=lambda _path: next(statuses),
        platform_name="nt",
    )
    outcome = coordinator.install_python()

    expected_tag = f"{sys.version_info.major}.{sys.version_info.minor}"
    assert outcome.installed is True
    assert commands == [[str(manager.resolve()), "install", expected_tag]]
    assert manifest.get("python-install-manager") is None
    record = manifest.get("python-runtime")
    assert record is not None
    assert record.source == f"python-install-manager:{expected_tag}"
    assert MSSTORE_SOURCE == "msstore"
    assert PYTHON_MANAGER_PRODUCT_ID == "9NQ7512CXL7T"


def test_new_python_manager_is_recorded_before_runtime_install(tmp_path):
    manifest = OwnershipManifest.load(tmp_path / "ownership.json", "0.0.4")
    manager = tmp_path / "pymanager.exe"
    manager.touch()
    manager_lookups = 0

    def which(name: str):
        nonlocal manager_lookups
        if name == "winget":
            return r"C:\Windows\winget.exe"
        if name == "pymanager":
            manager_lookups += 1
            return None if manager_lookups == 1 else str(manager)
        return None

    def runner(command: list[str], _timeout: float):
        if command[-1] == "--version":
            return subprocess.CompletedProcess(
                command, 0, stdout="Python install manager 26.3"
            )
        if command[0] == str(manager.resolve()) and command[1] == "install":
            return subprocess.CompletedProcess(
                command, 1, stdout="", stderr="runtime failed"
            )
        return subprocess.CompletedProcess(command, 0, stdout="Installed", stderr="")

    coordinator = InstallCoordinator(
        manifest,
        runner=runner,
        which=which,
        python_detector=lambda _path: _status("python-runtime", "missing"),
        platform_name="nt",
    )

    with pytest.raises(InstallError, match="Python .* installation failed"):
        coordinator.install_python()

    record = manifest.get("python-install-manager")
    assert record is not None
    assert record.path == str(manager.resolve())
    assert record.version == "Python install manager 26.3"
    assert record.installed_by_senpai is True
