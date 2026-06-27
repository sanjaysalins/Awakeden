"""Animate christ.png with a LOCKED camera (subtle light glow only) for the breathing CTA
close. Hard guard against the invented-flame problem. Kling 3.0 pro 9:16 10s. ~$1.30."""
import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import video_render

D = ROOT / "longform/EW01_Two_Goats/v1/short"
png = D / "visual_9x16_test/christ.png"
out = D / "gallery_clips/living_christ.mp4"
config.VIDEO_HF_MODEL = "kling3_0"; config.VIDEO_HF_ASPECT = "9:16"
config.VIDEO_HF_MODE = "pro"; config.VIDEO_HF_SOUND = "off"

motion = ("Absolutely LOCKED static camera — NO camera movement, no pan, no zoom, no push, "
    "no drift. The risen Christ stays a frozen Baroque oil painting; preserve his EXACT "
    "face, hands and robe with NO morphing and NO change. The ONLY motion is a gentle soft "
    "GLOW and shimmer of the warm light pouring through the torn veil behind him, and the "
    "faintest stir of the curtain edges. Absolutely NO fire, NO flame, NO sparks, NO embers, "
    "NO new elements, no glitter, no sparkles. Reverent, still, holy.")
print("[anim] living christ (Kling pro 9:16 10s, locked) ...", flush=True); t = time.time()
video_render.HFVideoProvider().animate(png, out, motion, 10)
print(f"[anim] {out}  ({out.stat().st_size:,} b, {time.time()-t:.0f}s)")
