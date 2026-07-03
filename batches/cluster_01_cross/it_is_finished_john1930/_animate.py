#!/usr/bin/env python
"""It Is Finished - 6 hero Kling clips at 9:16 (~$3.90). Idempotent, INK camera-only."""
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
    "eden_garden_finished": "ONE slow, steady, continuous push-in down the river valley toward the rising sun",
    "jesus_prays_night":    "ONE slow, steady, continuous push-in toward the praying figure's moonlit face",
    "vinegar_sponge_reed":  "ONE slow, steady, continuous push-in rising along the reed toward the crucified figure",
    "bowed_head_finished":  "ONE slow, steady, continuous push-in toward the bowed thorn-crowned head",
    "tomb_stone_sealed":    "ONE slow, steady, continuous push-in toward the sealed round stone",
    "first_day_morning":    "ONE slow, steady, continuous push-in toward the light bursting from the open tomb",
    "hands_shaping_light":  "ONE slow, steady, continuous push-in toward the sphere of light between the hands",
    "carpenter_bench_rest": "ONE slow, steady, continuous push-in toward the finished stool on the workbench",
    "man_lifting_face_dawn": "ONE slow, steady, continuous push-in toward the lifted face in the dawn light",
}
for slug, move in MOTION.items():
    still, out = POOL / f"{slug}.png", CLIPS / f"{slug}.mp4"
    if out.exists() and out.stat().st_size > 0:
        print(f"[skip] {slug}"); continue
    ok = hf_animate(still, out, INK_BASE.format(move=move), 5, aspect_ratio="9:16")
    print(f"SAVED {slug}" if ok else f"FAILED {slug}")
print("DONE")
