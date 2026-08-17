import json

from senpai_bot.settings import LOCAL_OLLAMA_URL, Settings


def test_safety_defaults_disable_launch_update_checks():
    settings = Settings()
    assert settings.check_updates_on_launch is False
    assert settings.ollama_url == LOCAL_OLLAMA_URL


def test_legacy_remote_endpoint_is_ignored(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text(
        json.dumps(
            {
                "model": "llama3.1:latest",
                "ollama_url": "https://remote.example.invalid",
                "check_updates_on_launch": False,
            }
        ),
        encoding="utf-8",
    )
    settings = Settings.load(path)
    assert settings.ollama_url == LOCAL_OLLAMA_URL

    settings.save(path)
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert "ollama_url" not in saved

