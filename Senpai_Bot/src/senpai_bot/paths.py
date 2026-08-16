from __future__ import annotations

import os
import sys
from pathlib import Path

from platformdirs import user_data_path


APP_NAME = "Senpai_Bot"


def bundle_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS"))
    return Path(__file__).resolve().parents[2]


def contract_dir() -> Path:
    override = os.getenv("SENPAI_CONTRACT_DIR")
    return Path(override).resolve() if override else bundle_root()


def data_dir() -> Path:
    path = user_data_path(APP_NAME, "DevilMedlar", ensure_exists=True)
    return Path(path)
