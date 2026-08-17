import re
import tomllib
from pathlib import Path

from senpai_bot import __version__


ROOT = Path(__file__).parents[1]


def test_application_versions_match():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    installer = (ROOT / "installer" / "Senpai_Bot.iss").read_text(encoding="utf-8")
    installer_version = re.search(r'#define MyAppVersion "([^"]+)"', installer)
    assert installer_version is not None
    assert {project["project"]["version"], installer_version.group(1), __version__} == {"0.0.4"}


def test_whats_new_is_bundled_by_pyinstaller():
    spec = (ROOT / "Senpai_Bot.spec").read_text(encoding="utf-8")
    assert 'root / "WHATS_NEW.md"' in spec
    assert (ROOT / "WHATS_NEW.md").is_file()
