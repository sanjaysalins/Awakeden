"""Test the Higgsfield camera-preset MOVES as prompt phrases on the same Two Goats
hero still, on the locked veo3_1_lite model — build a vetted reusable camera palette.
Same still = camera is the only variable. ~$1-1.5 per clip via HF. ~$6-9 total."""
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

LOCK = (" Keep it a frozen Baroque oil painting tableau; the man, the goat and the land "
    "stay perfectly still; only the camera and subtle drifting dust and heat-haze move. "
    "Do not turn the man toward us or invent his face, no morphing, no new elements.")

VARIANTS = {
    "aerial_view": (
        "Cinematic high aerial view looking down across the vast wilderness from above, "
        "the lone robed figure and the goat tiny in the immense cracked valley." + LOCK),
    "tracking_drone_view": (
        "Cinematic tracking drone shot gliding slowly forward and out over the wilderness "
        "valley, smooth aerial motion revealing the depth toward the hazy horizon." + LOCK),
    "pan": (
        "Cinematic slow lateral pan sweeping across the wilderness, from the lone figure "
        "toward the distant goat and the open valley beyond." + LOCK),
    "dolly_shot": (
        "Cinematic smooth dolly shot tracking slowly and steadily forward into the valley, "
        "even cinematic motion with gentle parallax." + LOCK),
    "zoomed_in": (
        "Cinematic slow telephoto zoom-in compressing the distance toward the small goat "
        "in the valley, the layered background flattening behind it." + LOCK),
    "smooth_cinematic": (
        "Smooth cinematic camera movement, a gentle gliding drift across the scene with "
        "subtle 3D parallax between the foreground ridge and the far valley." + LOCK),
}

vp = video_render.HFVideoProvider()
results = []
for name, motion in VARIANTS.items():
    mp4 = OUT / f"palette_{name}.mp4"
    print(f"[anim] {name} (veo3_1_lite 16:9 8s) ...", flush=True)
    t = time.time()
    try:
        vp.animate(PNG, mp4, motion, 8)
        print(f"[anim] OK  {mp4}  ({mp4.stat().st_size:,} bytes, {time.time()-t:.0f}s)")
        results.append(name)
    except Exception as e:
        print(f"[anim] FAIL {name}: {e}")

print(f"\nDONE. {len(results)}/{len(VARIANTS)} ok: {', '.join(results)}")
