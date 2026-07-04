#!/usr/bin/env python
"""Pierced (Zech 12:10) — 6 hero Kling clips at 9:16 (~$3.90). Idempotent, INK camera-only."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from _hf_animate_short import hf_animate

POOL = HERE / "visual"
CLIPS = POOL / "clips"

INK_BASE = ("A finished inked graphic-novel comic panel — flat printed art with bold black ink "
            "outlines, cel-flat color and cross-hatching. Animate it as {move}. The drawing itself "
            "never moves, redraws, repaints, breathes or changes; the ink lines and flat colors stay "
            "exactly as printed; only the camera moves. No hard cuts, no dissolves, no morphing, no "
            "subject motion, no limbs moving, no new lines drawn. INVENT NOTHING: show ONLY what is "
            "already inked in this exact panel. Keep the subject whole in frame.")

MOTION = {
    "spear_thrust_up":       "ONE slow, steady, continuous push-in rising along the spear toward the crucified figure above",
    "zechariah_night_scroll": "ONE slow, steady, continuous push-in toward the prophet's upturned face under the stars",
    "mourners_only_son":     "ONE slow, steady, continuous push-in toward the grieving parents",
    "look_up_faces":         "ONE slow, steady, continuous push-in toward the three upturned tearful faces",
    "grace_poured_sky":      "ONE slow, steady, continuous push-in toward the waterfall of light breaking the clouds",
    "blood_water_wood":      "ONE slow, steady, continuous push-in toward the stream running down the wood grain",
}
for slug, move in MOTION.items():
    still, out = POOL / f"{slug}.png", CLIPS / f"{slug}.mp4"
    if out.exists() and out.stat().st_size > 0:
        print(f"[skip] {slug}"); continue
    ok = hf_animate(still, out, INK_BASE.format(move=move), 5, aspect_ratio="9:16")
    print(f"SAVED {slug}" if ok else f"FAILED {slug}")
print("DONE")
