from __future__ import annotations

import hashlib
import re
import tempfile
from collections.abc import Callable
from pathlib import Path
from urllib.parse import urlparse


LATEST_RELEASE_API = "https://api.github.com/repos/DevilMedlar/python-recall-training/releases/latest"
ALLOWED_PAGE_HOSTS = {"github.com", "www.github.com"}
ALLOWED_DOWNLOAD_HOSTS = {
    "github.com",
    "objects.githubusercontent.com",
    "release-assets.githubusercontent.com",
}
SHA256_RE = re.compile(r"\b([0-9a-fA-F]{64})\b")


def version_tuple(version: str) -> tuple[int, int, int]:
    parts = version.strip().removeprefix("v").split(".")
    if not 1 <= len(parts) <= 3 or any(not part.isdigit() for part in parts):
        raise ValueError(f"Invalid application version: {version!r}")
    return tuple(int(part) for part in (*parts, *(["0"] * (3 - len(parts)))))


def is_newer_version(candidate: str, current: str) -> bool:
    return version_tuple(candidate) > version_tuple(current)


def _require_https_host(url: str, allowed_hosts: set[str]) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in allowed_hosts:
        raise ValueError(f"Unapproved update URL: {url}")


def parse_release(release: dict, current_version: str) -> dict[str, str] | None:
    tag = release.get("tag_name")
    page_url = release.get("html_url")
    notes = release.get("body") or "A newer Senpai_Bot release is available."
    assets = release.get("assets")
    if not isinstance(tag, str) or not isinstance(page_url, str) or not isinstance(notes, str):
        raise ValueError("GitHub returned an invalid release record.")
    version = tag.removeprefix("v")
    version_tuple(version)
    _require_https_host(page_url, ALLOWED_PAGE_HOSTS)
    if not is_newer_version(version, current_version):
        return None

    result = {"version": version, "url": page_url, "notes": notes[:3000]}
    installer_name = f"Senpai_Bot_Setup_{version}.exe"
    checksum_name = f"{installer_name}.sha256"
    if isinstance(assets, list):
        by_name = {
            asset.get("name"): asset.get("browser_download_url")
            for asset in assets
            if isinstance(asset, dict)
        }
        installer_url = by_name.get(installer_name)
        checksum_url = by_name.get(checksum_name)
        if isinstance(installer_url, str) and isinstance(checksum_url, str):
            _require_https_host(installer_url, ALLOWED_DOWNLOAD_HOSTS)
            _require_https_host(checksum_url, ALLOWED_DOWNLOAD_HOSTS)
            result["installer_url"] = installer_url
            result["checksum_url"] = checksum_url
    return result


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


def download_verified_installer(
    update: dict[str, str],
    progress: Callable[[str], None] | None = None,
) -> Path:
    import httpx

    version = update["version"]
    installer_url = update["installer_url"]
    checksum_url = update["checksum_url"]
    _require_https_host(installer_url, ALLOWED_DOWNLOAD_HOSTS)
    _require_https_host(checksum_url, ALLOWED_DOWNLOAD_HOSTS)

    checksum_response = httpx.get(checksum_url, timeout=20, follow_redirects=True)
    checksum_response.raise_for_status()
    _require_https_host(str(checksum_response.url), ALLOWED_DOWNLOAD_HOSTS)
    match = SHA256_RE.search(checksum_response.text)
    if not match:
        raise ValueError("The release checksum file is invalid.")
    expected_hash = match.group(1).lower()

    update_dir = Path(tempfile.gettempdir()) / "Senpai_Bot" / "updates"
    update_dir.mkdir(parents=True, exist_ok=True)
    destination = update_dir / f"Senpai_Bot_Setup_{version}.exe"
    partial = destination.with_suffix(".exe.part")
    digest = hashlib.sha256()
    received = 0
    try:
        with httpx.stream("GET", installer_url, timeout=None, follow_redirects=True) as response:
            response.raise_for_status()
            _require_https_host(str(response.url), ALLOWED_DOWNLOAD_HOSTS)
            total = int(response.headers.get("Content-Length", "0") or 0)
            with partial.open("wb") as output:
                for chunk in response.iter_bytes(1024 * 1024):
                    output.write(chunk)
                    digest.update(chunk)
                    received += len(chunk)
                    if progress:
                        if total:
                            progress(f"Downloading update… {received * 100 // total}%")
                        else:
                            progress(f"Downloading update… {received // (1024 * 1024)} MB")
        if digest.hexdigest().lower() != expected_hash:
            raise ValueError("The downloaded installer failed SHA-256 verification.")
        partial.replace(destination)
    except Exception:
        partial.unlink(missing_ok=True)
        raise
    if progress:
        progress("Update verified. Starting installer…")
    return destination
