from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_setup_cannot_restart_or_silently_launch_senpai():
    source = (ROOT / "installer" / "Senpai_Bot.iss").read_text(encoding="utf-8")
    run_section = source.split("[Run]", 1)[1]

    assert "SetupMutex=DevilMedlar.Senpai_Bot.Setup" in source
    assert "RestartApplications=no" in source
    assert "RestartApplications=yes" not in source
    assert run_section.count('Filename: "{app}\\{#MyAppExeName}"') == 1
    for required_flag in ("postinstall", "skipifsilent", "unchecked", "nowait"):
        assert required_flag in run_section


def test_setup_logging_is_enabled_for_duplicate_launch_diagnostics():
    source = (ROOT / "installer" / "Senpai_Bot.iss").read_text(encoding="utf-8")
    assert "SetupLogging=yes" in source
