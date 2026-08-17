from senpai_bot.model_catalog import (
    OFFICIAL_MODEL_LIBRARY_URL,
    RECOMMENDED_MODELS,
    canonical_installed_model,
)
from senpai_bot.settings import Settings


def test_recommended_models_are_exact_local_ollama_names():
    names = {model.name for model in RECOMMENDED_MODELS}

    assert Settings().model == "llama3.1:8b"
    assert "llama3.1:8b" in names
    assert all(":latest" not in name for name in names)
    assert all(not name.casefold().endswith("-cloud") for name in names)
    assert all(
        model.official_url.startswith("https://ollama.com/library/")
        for model in RECOMMENDED_MODELS
    )
    assert OFFICIAL_MODEL_LIBRARY_URL == "https://ollama.com/search"


def test_tagless_advanced_name_resolves_to_ollamas_canonical_latest_tag():
    assert canonical_installed_model("mistral", {"mistral:latest"}) == "mistral:latest"
    assert canonical_installed_model("mistral:7b", {"mistral:latest"}) is None
