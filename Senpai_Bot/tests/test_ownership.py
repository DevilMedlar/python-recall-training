import json

from senpai_bot.ownership import ComponentRecord, OwnershipManifest


def test_manifest_round_trip_and_backup(tmp_path):
    path = tmp_path / "ownership.json"
    manifest = OwnershipManifest.load(path, "0.0.4")
    manifest.record(
        ComponentRecord(
            component_id="ollama",
            kind="runtime",
            version="0.32.14",
            source="winget:Ollama.Ollama",
            install_method="winget-exact-package",
            installed_by_senpai=True,
            path=r"C:\Ollama\ollama.exe",
        )
    )

    loaded = OwnershipManifest.load(path, "0.0.4")
    record = loaded.get("ollama")
    assert record is not None
    assert record.installed_by_senpai is True
    assert record.installed_at_utc

    loaded.record(
        ComponentRecord(
            component_id="ollama-model:llama3.1:8b",
            kind="model",
            version="llama3.1:8b",
            installed_by_senpai=True,
        )
    )
    backup = path.with_suffix(".json.bak")
    assert backup.is_file()
    backup_values = json.loads(backup.read_text(encoding="utf-8"))
    assert set(backup_values["components"]) == {"ollama"}
    assert not path.with_name(".ownership.json.tmp").exists()


def test_corrupt_manifest_fails_closed_to_no_owned_components(tmp_path):
    path = tmp_path / "ownership.json"
    path.write_text("not json", encoding="utf-8")

    manifest = OwnershipManifest.load(path, "0.0.4")

    assert manifest.components == {}


def test_newer_valid_temporary_manifest_is_recovered(tmp_path):
    path = tmp_path / "ownership.json"
    path.write_text("not json", encoding="utf-8")
    temporary = path.with_name(".ownership.json.tmp")
    temporary.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "app_version": "0.0.4",
                "updated_at_utc": "2026-08-17T00:00:00+00:00",
                "components": {
                    "ollama": {
                        "component_id": "ollama",
                        "kind": "runtime",
                        "installed_by_senpai": True,
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    manifest = OwnershipManifest.load(path, "0.0.4")

    assert manifest.get("ollama") is not None
