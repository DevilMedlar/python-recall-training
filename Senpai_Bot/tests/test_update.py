from senpai_bot.update import is_newer_version, parse_release, version_tuple


def test_version_tuple_normalizes_short_versions():
    assert version_tuple("1.2") == (1, 2, 0)


def test_newer_version_comparison():
    assert is_newer_version("0.1.1", "0.1.0")
    assert not is_newer_version("0.1.1", "0.1.1")
    assert not is_newer_version("0.1.0", "0.1.1")


def test_release_parser_finds_verified_installer_pair():
    version = "0.0.5"
    installer = f"Senpai_Bot_Setup_{version}.exe"
    release = {
        "tag_name": f"v{version}",
        "html_url": "https://github.com/DevilMedlar/python-recall-training/releases/tag/v0.0.5",
        "body": "Test release",
        "assets": [
            {
                "name": installer,
                "browser_download_url": f"https://github.com/DevilMedlar/python-recall-training/releases/download/v{version}/{installer}",
            },
            {
                "name": f"{installer}.sha256",
                "browser_download_url": f"https://github.com/DevilMedlar/python-recall-training/releases/download/v{version}/{installer}.sha256",
            },
        ],
    }
    parsed = parse_release(release, "0.0.4")
    assert parsed is not None
    assert parsed["version"] == version
    assert parsed["installer_url"].endswith(installer)
    assert parsed["checksum_url"].endswith(".sha256")


def test_release_parser_ignores_current_version():
    release = {
        "tag_name": "v0.0.4",
        "html_url": "https://github.com/DevilMedlar/python-recall-training/releases/tag/v0.0.4",
        "body": "Current release",
        "assets": [],
    }
    assert parse_release(release, "0.0.4") is None
