from senpai_bot.update import is_newer_version, version_tuple


def test_version_tuple_normalizes_short_versions():
    assert version_tuple("1.2") == (1, 2, 0)


def test_newer_version_comparison():
    assert is_newer_version("0.1.1", "0.1.0")
    assert not is_newer_version("0.1.1", "0.1.1")
    assert not is_newer_version("0.1.0", "0.1.1")
