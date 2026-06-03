"""Tiny, dependency-free .env loader.

Looks for FAL_KEY in (in order): the current environment, ``veed_io/.env``, and
the repo-root ``.env``. The first hit wins and is exported into ``os.environ``.
Existing environment values are never overwritten.
"""

from __future__ import annotations

import os
from pathlib import Path

_PKG_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _PKG_DIR.parent

# Search order: package-local first, then repo root.
_CANDIDATES = (_PKG_DIR / ".env", _REPO_ROOT / ".env")


def _parse_env_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            out[key] = value
    return out


def load_env(*keys: str) -> None:
    """Populate ``os.environ`` with ``keys`` found in the candidate .env files.

    With no ``keys``, loads every variable found. Never overwrites a value that
    is already set in the environment.
    """
    wanted = set(keys)
    for path in _CANDIDATES:
        for key, value in _parse_env_file(path).items():
            if wanted and key not in wanted:
                continue
            os.environ.setdefault(key, value)


def ensure_fal_key() -> bool:
    """Best-effort load of FAL_KEY from .env files. Returns True if now set."""
    if not os.environ.get("FAL_KEY"):
        load_env("FAL_KEY")
    return bool(os.environ.get("FAL_KEY"))
