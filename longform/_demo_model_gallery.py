"""Model-driven gallery hard-cut test: the rich painting is the START IMAGE; the PROMPT
directs Kling to PLACE the camera at named framings and HARD-CUT between them, each
rendered at full native resolution (no ffmpeg upscaling). Two prompt techniques to compare.
~$1.30-2."""
import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import video_render

D = ROOT / "longform/EW01_Two_Goats/v1/short/visual_9x16_test/gallery_demo"
png = D / "rich_atonement.png"
config.VIDEO_HF_MODEL = "kling3_0"; config.VIDEO_HF_ASPECT = "9:16"
config.VIDEO_HF_MODE = "pro"; config.VIDEO_HF_SOUND = "off"

# Technique A — explicit placed-camera HARD-CUT gallery edit on named elements
HARDCUT = (
 "Treat this exact Baroque oil painting as a finished canvas and film it as a fast VIRAL "
 "GALLERY EDIT built only from clean HARD CUTS between FIXED camera framings. The camera is "
 "PLACED on each spot and holds still; it then HARD-CUTS to the next placement. NO zoom, NO "
 "pan, NO dolly, NO slow push between or during shots. "
 "Shot 1: the WHOLE painting, wide. HARD CUT. "
 "Shot 2: a tight fixed framing on the kneeling high priest's lifted face and raised hands. HARD CUT. "
 "Shot 3: a tight fixed framing on the two goats beside the altar. HARD CUT. "
 "Shot 4: a tight fixed framing on the smoking stone altar. HARD CUT. "
 "Shot 5: a tight fixed framing on the burning oil lamp on the floor. HARD CUT. "
 "Shot 6: the WHOLE painting again, wide. "
 "Each framing shows ONLY what is already painted in that part of this image, at full detail "
 "— invent nothing, add no new elements, do not morph faces or hands. The painting itself "
 "never moves; only the EDIT cuts between placements. Subtle life allowed: smoke and flame "
 "may flicker. No glitter, no sparkles.")

for tag, prompt, dur in [("hardcut10", HARDCUT, 10)]:
    out = D / f"model_{tag}.mp4"
    print(f"[anim] {tag} Kling pro 9:16 {dur}s ...", flush=True); t = time.time()
    try:
        video_render.HFVideoProvider().animate(png, out, prompt, dur)
        print(f"[anim] {out}  ({out.stat().st_size:,} b, {time.time()-t:.0f}s)")
    except Exception as e:
        print(f"[anim] FAIL {tag}: {e}")
