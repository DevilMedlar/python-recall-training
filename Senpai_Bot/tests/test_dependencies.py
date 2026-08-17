import json
import subprocess

from senpai_bot.dependencies import detect_ollama, detect_python


def _completed(command: list[str], stdout: str) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")


def test_configured_python_is_probed_and_accepted(tmp_path, monkeypatch):
    executable = tmp_path / "python.exe"
    executable.touch()
    monkeypatch.setattr(
        "senpai_bot.dependencies._safe_path_command", lambda _name: None
    )
    monkeypatch.setattr(
        "senpai_bot.dependencies._windows_python_candidates", lambda: []
    )

    def runner(command: list[str], _timeout: float):
        payload = {"path": str(executable), "version": [3, 14, 7], "bits": 64}
        return _completed(command, json.dumps(payload))

    status = detect_python(str(executable), runner)

    assert status.ready is True
    assert status.path == str(executable.resolve())
    assert status.version == "3.14.7"
    assert "64-bit" in status.detail


def test_unsupported_python_is_reported_without_installing(tmp_path, monkeypatch):
    executable = tmp_path / "python.exe"
    executable.touch()
    monkeypatch.setattr(
        "senpai_bot.dependencies._safe_path_command", lambda _name: None
    )
    monkeypatch.setattr(
        "senpai_bot.dependencies._windows_python_candidates", lambda: []
    )

    def runner(command: list[str], _timeout: float):
        payload = {"path": str(executable), "version": [3, 10, 9], "bits": 64}
        return _completed(command, json.dumps(payload))

    status = detect_python(str(executable), runner)

    assert status.state == "unsupported"
    assert "requires Python 3.11 or newer" in status.detail


def test_configured_ollama_is_probed_and_accepted(tmp_path, monkeypatch):
    executable = tmp_path / "ollama.exe"
    executable.touch()
    monkeypatch.setattr("senpai_bot.dependencies.shutil.which", lambda _name: None)
    monkeypatch.setattr(
        "senpai_bot.dependencies._windows_ollama_candidates", lambda: []
    )

    def runner(command: list[str], _timeout: float):
        return _completed(command, "ollama version 0.32.14\n")

    status = detect_ollama(str(executable), runner)

    assert status.ready is True
    assert status.path == str(executable.resolve())
    assert status.version == "ollama version 0.32.14"
