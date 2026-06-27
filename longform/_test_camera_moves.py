"""Animate the SAME existing Two Goats hero still 3 ways to compare camera moves
(orbit / crane pull-back / parallax push) without re-rendering the still — isolates
the camera as the only variable. ~$1-1.5 per clip via veo3_1_lite (HF). ~$3-4 total."""
import sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import video_render

OUT = ROOT / "longform" / "EW01_Two_Goats" / "v1" / "visual_16x9_test"
PNG = OUT / "test_hero.png"
assert PNG.exists(), f"missing still: {PNG}"

config.VIDEO_HF_MODEL = "veo3_1_lite"
config.VIDEO_HF_ASPECT = "16:9"

VARIANTS = {
    "A_orbit": (
        "Dynamic cinematic camera that slowly arcs and orbits laterally around the "
        "standing robed man, parallax sliding the foreground ridge past to reveal depth "
        "between him, the goat and the valley. Keep it a Baroque oil painting tableau; the "
        "man, the goat and the land hold perfectly still, only the camera moves, plus "
        "subtle drifting dust and heat-haze. Do NOT turn the man toward us, do NOT invent "
        "his face, no morphing, no new elements."
    ),
    "B_crane_pullback": (
        "Cinematic crane shot: the camera slowly rises and pulls back, the lone figure and "
        "the goat shrinking as the immense wilderness opens up around them. Frozen Baroque "
        "oil painting tableau; the subjects stay perfectly still; only the camera moves "
        "plus atmospheric drifting dust and slow clouds. No morphing, no new elements."
    ),
    "C_parallax_push": (
        "Dynamic cinematic slow push-in with strong 3D parallax, the dark foreground ridge "
        "sliding past the frame to reveal the depth of the valley beyond. Frozen Baroque "
        "oil painting tableau; the man, goat and land hold still; only the camera and "
        "subtle dust and heat-haze move. No morphing, no invented motion, no new elements."
    ),
}

vp = video_render.HFVideoProvider()
for name, motion in VARIANTS.items():
    mp4 = OUT / f"cam_{name}.mp4"
    print(f"[anim] {name} (veo3_1_lite 16:9 8s) ...", flush=True)
    t = time.time()
    vp.animate(PNG, mp4, motion, 8)
    print(f"[anim] {mp4}  ({mp4.stat().st_size:,} bytes, {time.time()-t:.0f}s)")

print("\nDONE. Compare cam_A_orbit / cam_B_crane_pullback / cam_C_parallax_push.")
