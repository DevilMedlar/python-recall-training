from __future__ import annotations

from urllib.parse import urlparse


UPDATE_MANIFEST_URL = (
    "https://raw.githubusercontent.com/DevilMedlar/"
    "python-recall-training/main/Senpai_Bot/update.json"
)
ALLOWED_UPDATE_HOSTS = {"github.com", "www.github.com"}


def version_tuple(version: str) -> tuple[int, int, int]:
    parts = version.strip().split(".")
    if not 1 <= len(parts) <= 3 or any(not part.isdigit() for part in parts):
        raise ValueError(f"Invalid application version: {version!r}")
    return tuple(int(part) for part in (*parts, *(["0"] * (3 - len(parts)))))


def is_newer_version(candidate: str, current: str) -> bool:
    return version_tuple(candidate) > version_tuple(current)


def check_for_update(current_version: str, manifest_url: str = UPDATE_MANIFEST_URL) -> dict[str, str] | None:
    import httpx

    response = httpx.get(manifest_url, timeout=5, follow_redirects=True)
    response.raise_for_status()
    manifest = response.json()
    version = manifest.get("version")
    url = manifest.get("url")
    notes = manifest.get("notes", "")
    if not isinstance(version, str) or not isinstance(url, str) or not isinstance(notes, str):
        raise ValueError("The update manifest has invalid fields.")
    target = urlparse(url)
    if target.scheme != "https" or target.hostname not in ALLOWED_UPDATE_HOSTS:
        raise ValueError("The update link is not an approved HTTPS GitHub URL.")
    if not is_newer_version(version, current_version):
        return None
    return {"version": version, "url": url, "notes": notes}
