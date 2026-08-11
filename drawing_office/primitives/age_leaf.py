"""Age Leaf -- thin wrapper around panel_animator/elder_leaf.py's foxed-paper
treatment ($0 deterministic elder stock: mottling, foxing, deckled edge).

LOWER PRIORITY stub -- panel_animator/elder_leaf.py owns the real logic
(make_elder_stock / compose_elder_leaf / apply_elder_leaf); this module just
exposes the plain aged-stock generator as a drawing_office primitive so
callers don't need to know panel_animator's import path.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

_PANEL_ANIMATOR_DIR = Path(__file__).resolve().parents[2] / "panel_animator"
if str(_PANEL_ANIMATOR_DIR) not in sys.path:
    sys.path.insert(0, str(_PANEL_ANIMATOR_DIR))

from elder_leaf import make_elder_stock  # noqa: E402


def age_leaf(w: int, h: int, seed: int = 21) -> Image.Image:
    """Return a deterministic aged/foxed paper stock (RGBA, deckle-edged
    alpha) of size (w, h). Reuses elder_leaf.make_elder_stock() verbatim."""
    return make_elder_stock(w, h, seed=seed)
