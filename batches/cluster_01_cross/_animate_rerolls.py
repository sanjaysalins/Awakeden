#!/usr/bin/env python
"""Re-roll batch - 5 Kling clips at 9:16 (~$3.25) across the 3 legacy re-roll pieces.
david_writing_psalm + psalm_scroll_night are WRITING -> dyncam only, never Kling."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from _hf_animate_short import hf_animate

INK_BASE = ("A finished inked graphic-novel comic panel - flat printed art with bold black ink "
            "outlines, cel-flat color and cross-hatching. Animate it as {move}. The drawing itself "
            "never moves, redraws, repaints, breathes or changes; the ink lines and flat colors stay "
            "exactly as printed; only the camera moves. No hard cuts, no dissolves, no morphing, no "
            "subject motion, no limbs moving, no new lines drawn. INVENT NOTHING: show ONLY what is "
            "already inked in this exact panel. Keep the subject whole in frame.")

JOBS = [
    ("crucifixion_foretold_ps2218", "john_watching",       "ONE slow, steady, continuous push-in toward the watching disciple's face"),
    ("forsaken_cry_ps221",          "ninth_hour_darkness", "ONE slow, steady, continuous push-in toward the three crosses under the darkened sun"),
    ("i_thirst_john1928",           "ocean_creation_wide", "ONE slow, steady, continuous push-in into the great curling wave against the dawn"),
    ("i_thirst_john1928",           "potsherd_dry_clay",   "ONE slow, steady, continuous push-in toward the broken clay shard on the cracked earth"),
    ("i_thirst_john1928",           "living_water_stream", "ONE slow, steady, continuous push-in toward the sparkling falling water"),
    ("forsaken_cry_ps221",          "father_lamp_doorway", "ONE slow, steady, continuous push-in toward the lamp-lit open doorway"),
    ("crucifixion_foretold_ps2218", "lots_cup_close",      "ONE slow, steady, continuous push-in toward the two knucklebone lots on the stone"),
]
for piece, slug, move in JOBS:
    pool = HERE / piece / "visual"
    still, out = pool / f"{slug}.png", pool / "clips" / f"{slug}.mp4"
    if out.exists() and out.stat().st_size > 0:
        print(f"[skip] {piece}/{slug}"); continue
    ok = hf_animate(still, out, INK_BASE.format(move=move), 5, aspect_ratio="9:16")
    print(f"SAVED {piece}/{slug}" if ok else f"FAILED {piece}/{slug}")
print("DONE")
