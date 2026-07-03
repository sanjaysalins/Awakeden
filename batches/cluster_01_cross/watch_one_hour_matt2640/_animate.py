#!/usr/bin/env python
"""Could Ye Not Watch One Hour - 5 hero Kling clips at 9:16 (~$3.25). Idempotent, INK camera-only."""
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
    "gethsemane_olives_night":    "ONE slow, steady, continuous push-in over the olive grove toward the moonlit city below",
    "jesus_praying_close":        "ONE slow, steady, continuous push-in toward the anguished praying face",
    "cup_moonlight":              "ONE slow, steady, continuous push-in toward the cup in the moonlight",
    "disciples_sleeping":         "ONE slow, steady, continuous push-in toward the sleeping men",
    "jesus_stands_over_sleepers": "ONE slow, steady, continuous push-in toward the standing figure looking down at the sleepers",
    "jesus_leads_three":          "ONE slow, steady, continuous push-in following the four walking figures up the moonlit path",
    "sleeping_peter_close":       "ONE slow, steady, continuous push-in toward the sleeping man's moonlit face",
    "kneeling_lamp_prayer":       "ONE slow, steady, continuous push-in toward the kneeling figure and the lamp glow",
    "same_prayer_again":          "ONE slow, steady, continuous push-in toward the low-bowed praying figure",
    "weak_flesh_hands":           "ONE slow, steady, continuous push-in toward the clasped trembling hands",
}
for slug, move in MOTION.items():
    still, out = POOL / f"{slug}.png", CLIPS / f"{slug}.mp4"
    if out.exists() and out.stat().st_size > 0:
        print(f"[skip] {slug}"); continue
    ok = hf_animate(still, out, INK_BASE.format(move=move), 5, aspect_ratio="9:16")
    print(f"SAVED {slug}" if ok else f"FAILED {slug}")
print("DONE")
