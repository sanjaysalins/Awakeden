#!/usr/bin/env python
"""Thirty Pieces (Zech 11) — 6 hero Kling clips at 9:16 (~$3.90). Idempotent, INK camera-only."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from _hf_animate_short import hf_animate

POOL = HERE / "visual"
CLIPS = POOL / "clips"
CLIPS.mkdir(exist_ok=True)

INK_BASE = ("A finished inked graphic-novel comic panel — flat printed art with bold black ink "
            "outlines, cel-flat color and cross-hatching. Animate it as {move}. The drawing itself "
            "never moves, redraws, repaints, breathes or changes; the ink lines and flat colors stay "
            "exactly as printed; only the camera moves. No hard cuts, no dissolves, no morphing, no "
            "subject motion, no limbs moving, no new lines drawn. INVENT NOTHING: show ONLY what is "
            "already inked in this exact panel. Keep the subject whole in frame.")

MOTION = {
    "thirty_coins_scatter":   "ONE slow, steady, continuous push-in low across the stone floor toward the falling coins",
    "weighing_scales_silver": "ONE slow, steady, continuous push-in toward the scale pan heavy with silver",
    "judas_bag_priests":      "ONE slow, steady, continuous push-in toward the bowed man clutching the money bag",
    "judas_casting_coins":    "ONE slow, steady, continuous push-in rising toward the coins flung in mid-air",
    "potter_at_wheel":        "ONE slow, steady, continuous push-in toward the clay vessel forming between the hands",
    "silver_and_blood":       "ONE slow, steady, continuous push-in following the dark red stream between the coins",
}
for slug, move in MOTION.items():
    still, out = POOL / f"{slug}.png", CLIPS / f"{slug}.mp4"
    if out.exists() and out.stat().st_size > 0:
        print(f"[skip] {slug}"); continue
    ok = hf_animate(still, out, INK_BASE.format(move=move), 5, aspect_ratio="9:16")
    print(f"SAVED {slug}" if ok else f"FAILED {slug}")
print("DONE")
