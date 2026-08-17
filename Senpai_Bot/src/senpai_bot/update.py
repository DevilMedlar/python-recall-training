from __future__ import annotations

from urllib.parse import urlparse


LATEST_RELEASE_API = "https://api.github.com/repos/DevilMedlar/python-recall-training/releases/latest"
ALLOWED_PAGE_HOSTS = {"github.com", "www.github.com"}
APPROVED_RELEASE_PATH = "/DevilMedlar/python-recall-training/releases/"


def version_tuple(version: str) -> tuple[int, int, int]:
    parts = version.strip().removeprefix("v").split(".")
    if not 1 <= len(parts) <= 3 or any(not part.isdigit() for part in parts):
        raise ValueError(f"Invalid application version: {version!r}")
    return tuple(int(part) for part in (*parts, *(["0"] * (3 - len(parts)))))


def is_newer_version(candidate: str, current: str) -> bool:
    return version_tuple(candidate) > version_tuple(current)


def _require_https_host(url: str, allowed_hosts: set[str]) -> None:
    parsed = urlparse(url)
    if (
        parsed.scheme != "https"
        or parsed.hostname not in allowed_hosts
        or not parsed.path.startswith(APPROVED_RELEASE_PATH)
    ):
        raise ValueError(f"Unapproved update URL: {url}")


def parse_release(release: dict, current_version: str) -> dict[str, str] | None:
    tag = release.get("tag_name")
    page_url = release.get("html_url")
    notes = release.get("body") or "A newer Senpai_Bot release is available."
    if not isinstance(tag, str) or not isinstance(page_url, str) or not isinstance(notes, str):
        raise ValueError("GitHub returned an invalid release record.")
    version = tag.removeprefix("v")
    version_tuple(version)
    _require_https_host(page_url, ALLOWED_PAGE_HOSTS)
    if not is_newer_version(version, current_version):
        return None

    return {"version": version, "url": page_url, "notes": notes[:3000]}


def check_for_update(current_version: str, release_api: str = LATEST_RELEASE_API) -> dict[str, str] | None:
    import httpx

    response = httpx.get(
        release_api,
        timeout=8,
        follow_redirects=True,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "Senpai_Bot-Updater"},
    )
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return parse_release(response.json(), current_version)
