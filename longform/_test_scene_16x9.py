"""Render ONE 16:9 long-form test scene (image + veo clip) to confirm the Baroque
look, the 16:9 aspect, veo3_1_lite motion, and the REAL per-clip cost before any batch.
Reuses the existing NBP image provider + HF veo video provider. Spends ~$1."""
import sys, time, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render, video_render

V1 = ROOT / "longform" / "01_Isaiah_53_Suffering_Servant" / "v1"
OUT = V1 / "visual_16x9"
OUT.mkdir(exist_ok=True)

# --- 16:9 Baroque style (override the shorts 9:16 defaults) ---
config.VISUAL_STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and "
    "Rembrandt lighting, deep shadow and warm golden light, reverent sacred art, muted "
    "earth tones, fine visible brushwork")
config.VISUAL_STYLE_TAIL = "no text, no modern elements, cinematic 16:9 widescreen composition"

plan = json.loads((OUT / "scene_plan.json").read_text(encoding="utf-8"))
s = next(x for x in plan["scenes"] if x["id"] == 1)

scene = Scene(
    index=s["id"], slug="s01_wilderness", title=s["title"], scene_type="single",
    arc_position="opening", framing="wide",
    purpose="open the report on the lonely prophet in the wilderness",
    rationale="sets the 700-years-before cold open",
    visible_elements="vast bleak Judean wilderness, one small lone prophet figure far off, immense empty sky, wind-blown dust",
    emotional_tone="lonely, vast, solemn",
    subject_block=s["subject_block"], mood_block="lonely, vast, reverent, solemn",
    jesus_variant=None,
)

# --- image (NBP, 16:9) ---
visual_render.NBPProvider.ASPECT_RATIO = "16:9"
prov = visual_render.NBPProvider()
png = OUT / "test_s01.png"
print("[img ] rendering S1 (NBP, 16:9 Baroque) ...", flush=True)
t = time.time()
png.write_bytes(prov.generate(scene))
print(f"[img ] {png}  ({png.stat().st_size:,} bytes, {time.time()-t:.0f}s)")

# --- animate (veo3_1_lite, 16:9, 8s, slow camera on the frozen tableau) ---
config.VIDEO_HF_MODEL = "veo3_1_lite"
config.VIDEO_HF_ASPECT = "16:9"
motion = ("Cinematic very slow push-in. Keep it a frozen Baroque oil painting tableau; "
    "only a gentle camera move and subtle atmospheric drift of dust and light. "
    "No new elements, no morphing, no invented motion.")
mp4 = OUT / "test_s01.mp4"
print("[anim] veo3_1_lite 16:9 8s ...", flush=True)
t = time.time()
vp = video_render.HFVideoProvider()
vp.animate(png, mp4, motion, 8)
print(f"[anim] {mp4}  ({mp4.stat().st_size:,} bytes, {time.time()-t:.0f}s)")
print("\nDONE. Review the PNG + MP4; check the hf output above for the real credit cost.")
