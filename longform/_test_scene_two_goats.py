"""Render ONE 16:9 long-form test scene for EW01 Two Goats — the scapegoat
vanishing into the wilderness — to confirm the period-documentary Baroque look,
16:9 aspect, veo3_1_lite ATMOSPHERIC motion (animate the air, not the subject),
and the REAL per-clip cost before the full batch. Reuses the NBP image provider
+ HF veo video provider. Spends ~$1-2."""
import sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render, video_render

V1 = ROOT / "longform" / "EW01_Two_Goats" / "v1"
OUT = V1 / "visual_16x9_test"
OUT.mkdir(exist_ok=True)

# --- 16:9 Baroque period-documentary style (override the shorts 9:16 defaults) ---
config.VISUAL_STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and "
    "Rembrandt lighting, deep shadow and warm golden light, reverent sacred art, muted "
    "earth tones, fine visible brushwork")
config.VISUAL_STYLE_TAIL = "no text, no modern elements, cinematic 16:9 widescreen composition"

SUBJECT = (
    "A vast bleached desert wadi stretching to a hazy horizon under an immense pale sky. "
    "In the mid-distance, walking away from the viewer down the cracked dry valley floor, "
    "a single small goat reduced almost to a dark speck, carrying the weight of the whole "
    "frame. At the near edge of the frame, seen from behind with his back fully to us, a "
    "lone robed man in dusty ancient Near-Eastern linen stands and watches it go, dwarfed "
    "by the emptiness. Heat shimmer rising off the distant ground; thin drifting dust "
    "hanging in the low golden light; a few high pale streaked clouds across the enormous "
    "sky. Ancient biblical-period Judean wilderness, no structures. The overwhelming scale "
    "of barren land swallowing the small living thing being sent away."
)

scene = Scene(
    index=1, slug="hero_scapegoat_wilderness",
    title="Into a land not inhabited",
    scene_type="single", arc_position="climax", framing="wide",
    purpose="the scapegoat carried away into the wilderness — the guilt borne off",
    rationale="signature image of the Two Goats; proves atmospheric-only motion",
    visible_elements=("vast bleak Judean wilderness, one small lone goat far off walking "
        "away, a robed man seen from behind watching, immense empty sky, heat-haze, "
        "wind-blown dust"),
    emotional_tone="lonely, vast, solemn, awed",
    subject_block=SUBJECT,
    mood_block="lonely, vast, reverent, solemn, period-documentary",
    jesus_variant=None,
)

# --- image (HF nano_banana_2, 16:9 — NBP key is over its monthly cap; this
#     scene has no Christ face so NBP's ref-consistency isn't needed) ---
visual_render.HFProvider.ASPECT = "16:9"
prov = visual_render.HFProvider()
png = OUT / "test_hero.png"
print("[img ] rendering hero scapegoat (HF nano_banana_2, 16:9 Baroque) ...", flush=True)
t = time.time()
png.write_bytes(prov.generate(scene))
print(f"[img ] {png}  ({png.stat().st_size:,} bytes, {time.time()-t:.0f}s)")

# --- animate (veo3_1_lite, 16:9, 8s, ATMOSPHERE-ONLY motion) ---
config.VIDEO_HF_MODEL = "veo3_1_lite"
config.VIDEO_HF_ASPECT = "16:9"
motion = ("Cinematic very slow push-in on a frozen Baroque oil painting tableau. The ONLY "
    "motion is atmospheric: drifting desert dust, shimmering heat-haze rising off the far "
    "ground, and slow high clouds. The goat, the man, and the land stay perfectly still — "
    "do NOT move the goat's legs, do NOT turn the man, no morphing, no new elements, no "
    "invented motion. Period-documentary stillness.")
mp4 = OUT / "test_hero.mp4"
print("[anim] veo3_1_lite 16:9 8s (atmosphere-only) ...", flush=True)
t = time.time()
vp = video_render.HFVideoProvider()
vp.animate(png, mp4, motion, 8)
print(f"[anim] {mp4}  ({mp4.stat().st_size:,} bytes, {time.time()-t:.0f}s)")
print("\nDONE. Review the PNG + MP4; check the hf output above for the real credit cost.")
