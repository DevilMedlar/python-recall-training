from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_updater_cannot_download_or_execute_an_installer():
    update_source = (ROOT / "src" / "senpai_bot" / "update.py").read_text(encoding="utf-8")
    window_source = (ROOT / "src" / "senpai_bot" / "ui" / "main_window.py").read_text(encoding="utf-8")
    assert "download_verified_installer" not in update_source
    assert "download_verified_installer" not in window_source
    assert "startDetached" not in window_source
    assert "_install_downloaded_update" not in window_source


def test_manual_update_check_remains_available():
    window_source = (ROOT / "src" / "senpai_bot" / "ui" / "main_window.py").read_text(encoding="utf-8")
    assert 'QAction("Check for updates…", self)' in window_source
    assert "_start_update_check(announce_current=True)" in window_source


def test_no_release_workflow_or_legacy_manifest_exists():
    assert not (ROOT / "update.json").exists()
    assert not (ROOT.parent / ".github" / "workflows").exists()

