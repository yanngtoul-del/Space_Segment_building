"""Resource path helpers (work from source tree and from a PyInstaller bundle)."""

import sys
from pathlib import Path


def resource_root() -> Path:
    """Root folder containing 'data/' (bundle dir when frozen, repo root otherwise)."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).resolve().parents[3]


def data_dir() -> Path:
    return resource_root() / "data"


def catalogs_dir() -> Path:
    return data_dir() / "catalogs"


def images_dir() -> Path:
    return data_dir() / "images"


def missions_dir() -> Path:
    return data_dir() / "missions"
