import pytest

from senpai_bot.ollama import LOCAL_OLLAMA_HOST, LOCAL_OLLAMA_URL, OllamaError, OllamaManager


class FakeProcess:
    def __init__(self):
        self.returncode = None
        self.terminated = False
        self.killed = False

    def poll(self):
        return self.returncode

    def terminate(self):
        self.terminated = True
        self.returncode = 0

    def kill(self):
        self.killed = True
        self.returncode = -9

    def wait(self, timeout=None):
        return self.returncode


def test_remote_ollama_endpoint_is_rejected():
    with pytest.raises(OllamaError, match="only permits the local Ollama endpoint"):
        OllamaManager("https://remote.example.invalid", "llama3.1:latest")


def test_existing_ollama_server_is_not_owned(monkeypatch):
    manager = OllamaManager(LOCAL_OLLAMA_URL, "llama3.1:latest")
    monkeypatch.setattr(manager, "is_ready", lambda: True)
    assert manager.start_hidden() is False
    assert manager.owns_process() is False
    assert manager.stop_owned() is False


def test_spawned_ollama_is_cloud_disabled_and_stopped(monkeypatch):
    manager = OllamaManager(LOCAL_OLLAMA_URL, "llama3.1:latest")
    readiness = iter((False, True))
    monkeypatch.setattr(manager, "is_ready", lambda: next(readiness))
    monkeypatch.setattr("senpai_bot.ollama.shutil.which", lambda _name: "ollama")
    captured = {}
    process = FakeProcess()

    def fake_popen(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return process

    monkeypatch.setattr("senpai_bot.ollama.subprocess.Popen", fake_popen)
    assert manager.start_hidden(timeout=0.1) is True
    assert manager.owns_process() is True
    assert captured["kwargs"]["env"]["OLLAMA_HOST"] == LOCAL_OLLAMA_HOST
    assert captured["kwargs"]["env"]["OLLAMA_NO_CLOUD"] == "1"

    assert manager.stop_owned() is True
    assert process.terminated is True
    assert manager.owns_process() is False


def test_no_automatic_model_bootstrap_method_exists():
    assert not hasattr(OllamaManager, "ensure_model")


def test_cloud_model_names_are_rejected():
    manager = OllamaManager(LOCAL_OLLAMA_URL, "gpt-oss:120b-cloud")
    with pytest.raises(OllamaError, match="cloud models are disabled"):
        manager.stream_chat([], lambda _token: None)
