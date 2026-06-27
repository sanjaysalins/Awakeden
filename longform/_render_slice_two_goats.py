"""Render a 3-scene PROOF SLICE from the Two Goats scene_plan.json: still (HF, 16:9
Baroque) + veo3_1_lite animation with the scene's tagged green-palette camera move and
a glitter-kill negative. Scenes 1 (epic establishing), 6 (unified memory), 25 (Christ
hero on HF). ~$5-6."""
import sys, time, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render, video_render

V1 = ROOT / "longform" / "EW01_Two_Goats" / "v1"
OUT = V1 / "visual_16x9"
plan = json.loads((OUT / "scene_plan.json").read_text(encoding="utf-8"))
SLICE = [1, 6, 25]

config.VISUAL_STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and "
    "Rembrandt lighting, deep shadow and warm golden light, reverent sacred art, muted "
    "earth tones, fine visible brushwork")
config.VISUAL_STYLE_TAIL = "no text, no modern elements, cinematic 16:9 widescreen composition"
visual_render.HFProvider.ASPECT = "16:9"
config.VIDEO_HF_MODEL = "veo3_1_lite"
config.VIDEO_HF_ASPECT = "16:9"

CAM = {
    "pull_back": "Cinematic slow crane pull-back, the camera rising and drawing back to reveal the full scale",
    "smooth_cinematic": "Smooth cinematic camera movement, a gentle gliding drift with subtle parallax",
    "dolly_in": "Cinematic slow dolly push-in toward the subject",
    "dolly_shot": "Cinematic smooth dolly shot tracking steadily forward",
    "zoomed_in": "Cinematic slow telephoto zoom-in onto the subject",
    "tracking_drone_view": "Cinematic tracking drone glide forward over the scene",
}
GLITTER = (" Steady natural light only; absolutely no glowing particles, sparkles, dust "
    "motes, glitter, embers or floating lights; no lens bloom.")
LOCK = (" Keep it a frozen Baroque oil painting tableau; the subjects stay perfectly "
    "still; only the camera and faint {atmos} move; no morphing, no new elements, do not "
    "invent or duplicate any figure or face.")

imgp = visual_render.HFProvider()
vidp = video_render.HFVideoProvider()

for sid in SLICE:
    s = next(x for x in plan["scenes"] if x["id"] == sid)
    slug = f"slice_{sid:02d}"
    scene = Scene(
        index=sid, slug=slug, title=s["title"],
        scene_type="single", arc_position="body", framing=s["framing"],
        purpose=s["title"], rationale="proof slice",
        visible_elements=s["subject_block"][:200],
        emotional_tone=s.get("atmos", ""),
        subject_block=s["subject_block"],
        mood_block="reverent, period-documentary, " + s["framing"],
        jesus_variant=None,
    )
    png = OUT / f"{slug}.png"
    print(f"[img ] #{sid} {s['title']} (HF 16:9) ...", flush=True)
    t = time.time()
    png.write_bytes(imgp.generate(scene))
    print(f"[img ] {png}  ({png.stat().st_size:,} bytes, {time.time()-t:.0f}s)")

    motion = (CAM[s["camera"]] + ". " + LOCK.format(atmos=s["atmos"]) + GLITTER)
    mp4 = OUT / f"{slug}.mp4"
    print(f"[anim] #{sid} cam={s['camera']} (veo3_1_lite 8s) ...", flush=True)
    t = time.time()
    try:
        vidp.animate(png, mp4, motion, 8)
        print(f"[anim] {mp4}  ({mp4.stat().st_size:,} bytes, {time.time()-t:.0f}s)")
    except Exception as e:
        print(f"[anim] FAIL #{sid}: {e}")

print("\nDONE. Review slice_01 / slice_06 / slice_25 (png + mp4).")
