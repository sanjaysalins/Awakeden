#!/usr/bin/env python
"""One-off: the 4 extra Kling heroes for the living-page test (~$0.65 each, 16:9, INK camera-only).
Idempotent; HF 500s just print FAILED and the living-page build falls back to $0 dyncam."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from _hf_animate_short import hf_animate

POOL = HERE / "v1" / "visual_16x9_inked"
CLIPS = POOL / "clips"

INK_BASE = ("A finished inked graphic-novel comic panel — flat printed art with bold black ink "
            "outlines, cel-flat color and cross-hatching. Animate it as {move}. The drawing itself "
            "never moves, redraws, repaints, breathes or changes; the ink lines and flat colors stay "
            "exactly as printed; only the camera moves. No hard cuts, no dissolves, no morphing, no "
            "subject motion, no limbs moving, no new lines drawn. INVENT NOTHING: show ONLY what is "
            "already inked in this exact panel. Keep the subject whole in frame.")

MOTION = {
    "pierced_feet":         "ONE slow, steady, continuous push-in toward the nailed feet on the wood",
    "lots_dice_closeup":    "ONE slow, steady, continuous push-in toward the cast lots on the ground",
    "cross_hill_pullback":  "ONE slow, steady, continuous pull-back that starts on the cross on the hill and reveals the whole panel",
    "face_anguish_closeup": "ONE slow, steady, continuous push-in toward the crying upturned face",
}

for slug, move in MOTION.items():
    still, out = POOL / f"{slug}.png", CLIPS / f"{slug}.mp4"
    if out.exists() and out.stat().st_size > 0:
        print(f"[skip] {slug}"); continue
    ok = hf_animate(still, out, INK_BASE.format(move=move), 5, aspect_ratio="16:9")
    print(f"SAVED {slug}" if ok else f"FAILED {slug}")
print("DONE")
