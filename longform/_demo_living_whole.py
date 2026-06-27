"""Animate the rich painting ONCE with a LOCKED camera (atmospheric life only) via the
shorts path (Kling 3.0 pro 9:16). Hard-cut framings get cropped out of this living clip."""
import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import video_render

OUT = ROOT / "longform/EW01_Two_Goats/v1/short/visual_9x16_test/gallery_demo"
png = OUT / "rich_atonement.png"
config.VIDEO_HF_MODEL = "kling3_0"; config.VIDEO_HF_ASPECT = "9:16"
config.VIDEO_HF_MODE = "pro"; config.VIDEO_HF_SOUND = "off"

motion = ("Absolutely LOCKED static camera — NO camera movement whatsoever, no pan, no "
    "zoom, no push, no drift. The painting stays a frozen Baroque oil tableau; the ONLY "
    "motion is gentle atmospheric life: the altar smoke drifting slowly upward, the oil-lamp "
    "flame and the altar fire flickering softly, a faint warm light shimmer. The goats, the "
    "priest, the veil and the desert stay perfectly still. No morphing, no new elements, no "
    "glitter, no sparkles.")
out = OUT / "living_whole.mp4"
print("[anim] Kling 3.0 pro 9:16 5s (locked-camera life) ...", flush=True); t = time.time()
video_render.HFVideoProvider().animate(png, out, motion, 5)
print(f"[anim] {out}  ({out.stat().st_size:,} b, {time.time()-t:.0f}s)")
