"""Bake-off of 4 prompting techniques for the model-driven gallery HARD-CUT edit, same
rich painting, Kling 3.0 pro 9:16 10s. Find the prompt that best: opens wide, does TRUE
hard cuts, hits the named elements, and invents nothing. ~$5."""
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

GUARD = (" INVENT NOTHING — add no new elements, do NOT duplicate the single oil lamp, do "
 "not morph faces or hands; show only what is already painted in this exact image. The "
 "painting itself never moves; only the EDIT changes framing. Subtle life only: smoke and "
 "flame may flicker. No glitter, no sparkles.")

V1 = ("Film this exact Baroque oil painting as a VIRAL GALLERY EDIT made only of clean HARD "
 "CUTS between FROZEN, locked-off camera framings. Each shot is a motionless still held "
 "briefly, then an INSTANT hard cut — no zoom, no pan, no push, no dissolve — to the next. "
 "Begin on the FULL WIDE whole painting. HARD CUT to the kneeling priest's lifted face and "
 "raised hands. HARD CUT to the two goats by the altar. HARD CUT to the smoking stone "
 "altar. HARD CUT to the single burning oil lamp on the floor. HARD CUT back to the FULL "
 "WIDE whole painting." + GUARD)

V2 = ("Film this exact Baroque oil painting as a fast edited sequence with these EXACT cuts, "
 "each a fixed locked framing with an instant hard cut between them and NO movement within "
 "or between shots: 0.0 to 2.0 seconds the FULL WIDE whole painting; at 2.0 cut to the two "
 "goats by the altar; at 4.0 cut to the smoking stone altar; at 6.0 cut to the single "
 "burning oil lamp; at 8.0 cut to the priest's lifted face and raised hands; at 9.0 cut "
 "back to the FULL WIDE whole painting until 10.0." + GUARD)

V3 = ("Render this exact Baroque oil painting as a rapid SLIDESHOW of separate still "
 "PHOTOGRAPHS of the one painting — each photograph a different fixed crop, shown for about "
 "one second, then replaced by the next with a clean instantaneous cut, like flipping "
 "through printed photos. There is NO camera motion at all, ever — only the photo changes. "
 "Photo 1: the whole wide painting. Photo 2: the priest's face and raised hands. Photo 3: "
 "the two goats. Photo 4: the smoking altar. Photo 5: the single oil lamp. Photo 6: the "
 "whole wide painting." + GUARD)

V4 = ("You are a film editor cutting a fast title sequence from ONE static painting. Use only "
 "JUMP CUTS between locked-off shots — the camera is bolted down at each placement and "
 "never moves; every cut is instantaneous. Open WIDE on the whole painting, then jump-cut "
 "tight to: the priest's face and raised hands; then the two goats; then the smoking altar; "
 "then the single oil lamp; then jump-cut back to the whole wide painting." + GUARD)

for tag, prompt in [("v1_holdcut", V1), ("v2_timecoded", V2),
                    ("v3_photoslides", V3), ("v4_jumpcut", V4)]:
    out = D / f"bakeoff_{tag}.mp4"
    if out.exists():
        print(f"[skip] {tag}"); continue
    print(f"[anim] {tag} Kling pro 9:16 10s ...", flush=True); t = time.time()
    try:
        video_render.HFVideoProvider().animate(png, out, prompt, 10)
        print(f"[anim] {out.name}  ({out.stat().st_size:,} b, {time.time()-t:.0f}s)")
    except Exception as e:
        print(f"[anim] FAIL {tag}: {e}")
print("\nDONE bake-off.")
