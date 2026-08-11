"""Drawing Office POC -- Two Goats derived views ($0, code only)."""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "primitives"))
from relight import relight_split  # noqa: E402
from compose import tear_vertical  # noqa: E402
from PIL import Image

HERE = Path(__file__).resolve().parent
PLATES = HERE / "plates"
DERIVED = HERE / "derived"
DERIVED.mkdir(exist_ok=True)

if __name__ == "__main__":
    goats = Image.open(PLATES / "two_goats.png")

    d1 = relight_split(goats, split_x_frac=0.5, left_mode="cool_still",
                        right_mode="warm_departing", blend=0.0, feather_px=70)
    d1.save(DERIVED / "goats_split.png")
    print("[ok] goats_split.png (blend=0.0, split state)")

    d2 = relight_split(goats, split_x_frac=0.5, left_mode="cool_still",
                        right_mode="warm_departing", blend=1.0, feather_px=70)
    d2.save(DERIVED / "goats_unified.png")
    print("[ok] goats_unified.png (blend=1.0, unified state)")

    veil = Image.open(PLATES / "veil.png")
    d3 = tear_vertical(veil, tear_x_frac=0.5, jag_amplitude_px=22, gap_px=26)
    d3.save(DERIVED / "veil_torn.png")
    print("[ok] veil_torn.png")
