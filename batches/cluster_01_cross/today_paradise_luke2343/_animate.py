#!/usr/bin/env python
"""Today in Paradise (Luke 23:43) — 5 hero Kling clips at 9:16 (~$3.25). Idempotent, INK camera-only."""
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
    "mocker_thief_face":    "ONE slow, steady, continuous push-in toward the shouting man's twisted face",
    "penitent_thief_face":  "ONE slow, steady, continuous push-in toward the bound man's tearful turned face",
    "thief_looks_to_jesus": "ONE slow, steady, continuous push-in past the man's shoulder toward the far cross",
    "jesus_turns_to_thief": "ONE slow, steady, continuous push-in toward the thorn-crowned face turned in compassion",
    "paradise_dawn":        "ONE slow, steady, continuous push-in up the garden path toward the figure in the dawn light",
    "two_thieves_wide":     "ONE slow, steady, continuous push-in up the hill toward the three crosses against the storm",
}
for slug, move in MOTION.items():
    still, out = POOL / f"{slug}.png", CLIPS / f"{slug}.mp4"
    if out.exists() and out.stat().st_size > 0:
        print(f"[skip] {slug}"); continue
    ok = hf_animate(still, out, INK_BASE.format(move=move), 5, aspect_ratio="9:16")
    print(f"SAVED {slug}" if ok else f"FAILED {slug}")
print("DONE")
