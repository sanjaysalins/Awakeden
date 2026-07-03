#!/usr/bin/env python
"""Into Thy Hands - 4 hero Kling clips at 9:16 (~$2.60). Idempotent, INK camera-only.
psalm_scroll_night is WRITING -> dyncam only, never Kling."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from _hf_animate_short import hf_animate

POOL = HERE / "visual"
CLIPS = POOL / "clips"
CLIPS.mkdir(exist_ok=True)

INK_BASE = ("A finished inked graphic-novel comic panel - flat printed art with bold black ink "
            "outlines, cel-flat color and cross-hatching. Animate it as {move}. The drawing itself "
            "never moves, redraws, repaints, breathes or changes; the ink lines and flat colors stay "
            "exactly as printed; only the camera moves. No hard cuts, no dissolves, no morphing, no "
            "subject motion, no limbs moving, no new lines drawn. INVENT NOTHING: show ONLY what is "
            "already inked in this exact panel. Keep the subject whole in frame.")

MOTION = {
    "child_sleeping_lamp":         "ONE slow, steady, continuous push-in toward the sleeping child's face in the lamp glow",
    "father_holds_sleeping_child": "ONE slow, steady, continuous push-in toward the father and the sleeping child",
    "hands_of_light_open":         "ONE slow, steady, continuous push-in toward the open hands of light",
    "child_waking_dawn":           "ONE slow, steady, continuous push-in toward the waking child in the dawn light",
    "father_hand_childs_hand":     "ONE slow, steady, continuous push-in toward the small hand resting in the large hand",
    "child_eyes_closing":          "ONE slow, steady, continuous push-in toward the sleeping child's peaceful face",
    "cross_at_dawn":               "ONE slow, steady, continuous push-in toward the cross against the sunrise",
}
for slug, move in MOTION.items():
    still, out = POOL / f"{slug}.png", CLIPS / f"{slug}.mp4"
    if out.exists() and out.stat().st_size > 0:
        print(f"[skip] {slug}"); continue
    ok = hf_animate(still, out, INK_BASE.format(move=move), 5, aspect_ratio="9:16")
    print(f"SAVED {slug}" if ok else f"FAILED {slug}")
print("DONE")
