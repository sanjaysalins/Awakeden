"""~$3 9:16 SHORT proof for EW01 Two Goats — does the painterly period look transfer to
vertical, and is Kling-pro motion worth it over $0 Ken Burns? Renders the punchy short's
two bookend stills (hook + Christ landing) at 9:16 via HF, animates the Christ landing with
the LOCKED shorts path (Kling 3.0 --mode pro 9:16), and Ken-Burns the hook with ffmpeg ($0).
NO veo (veo is long-form only). ~$1.3-1.7."""
import sys, time, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render, video_render

OUT = ROOT / "longform" / "EW01_Two_Goats" / "v1" / "short" / "visual_9x16_test"
OUT.mkdir(parents=True, exist_ok=True)

config.VISUAL_STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and "
    "Rembrandt lighting, deep shadow and warm golden light, reverent sacred art, muted "
    "earth tones, fine visible brushwork")
config.VISUAL_STYLE_TAIL = "no text, no modern elements, vertical 9:16 composition"

HOOK = (
    "A lone figure in plain white linen — the high priest Aaron — seen from behind and "
    "small at the foot of an immense temple veil that towers up out of the top of the "
    "frame; through a narrow parting in the heavy embroidered curtain, thick darkness and "
    "a single faint golden glow of the mercy seat beyond; oil-lamp light catching the "
    "folds; deep shadow; the held breath of dread before going in. Tall vertical "
    "composition, the great curtain filling the height.")
CHRIST = (
    "The risen Christ stands full-length in the open doorway of a torn temple veil, "
    "brilliant warm light pouring out behind him into the dark; one hand extended toward "
    "the viewer in welcome; the heavy curtain torn and hanging to either side; his face "
    "calm, kind and dignified; reverent and worthy. Tall vertical hero composition, the "
    "figure centred and filling the frame.")

scenes = {
    "hook": Scene(index=1, slug="hook_aaron_veil", title="Behind the curtain",
        scene_type="single", arc_position="opening", framing="medium",
        purpose="the dread of going in", rationale="punchy short hook",
        visible_elements="white-linen priest small before a towering temple veil, golden glow beyond",
        emotional_tone="dread, awe", subject_block=HOOK,
        mood_block="reverent, ominous, intimate, vertical", jesus_variant=None),
    "christ": Scene(index=2, slug="christ_landing", title="Walk in",
        scene_type="single", arc_position="climax", framing="medium",
        purpose="the CTA — come to Jesus", rationale="punchy short landing",
        visible_elements="risen Christ in torn-veil doorway, hand extended, light pouring",
        emotional_tone="warm, inviting, holy", subject_block=CHRIST,
        mood_block="reverent, radiant, inviting, vertical", jesus_variant=None),
}

prov = visual_render.HFProvider()           # ASPECT defaults to 9:16 (shorts)
pngs = {}
for key, sc in scenes.items():
    png = OUT / f"{key}.png"
    print(f"[img ] {key} (HF nano_banana_2, 9:16) ...", flush=True)
    t = time.time()
    png.write_bytes(prov.generate(sc))
    print(f"[img ] {png}  ({png.stat().st_size:,} b, {time.time()-t:.0f}s)")
    pngs[key] = png

# --- Christ landing -> LOCKED shorts path: Kling 3.0 --mode pro 9:16 (reverent push-in) ---
config.VIDEO_HF_MODEL = "kling3_0"
config.VIDEO_HF_ASPECT = "9:16"
config.VIDEO_HF_MODE = "pro"
config.VIDEO_HF_SOUND = "off"
motion = ("Cinematic slow reverent push-in toward the standing figure of Christ. Frozen "
    "Baroque oil painting tableau — preserve the exact face and hands, NO morphing, NO new "
    "elements, NO invented motion; only a gentle camera push and faint warm light. Steady "
    "light only, no sparkles, no glitter, no bloom.")
mp4_k = OUT / "christ_klingpro.mp4"
print("[anim] christ -> Kling 3.0 pro 9:16 5s ...", flush=True)
t = time.time()
try:
    video_render.HFVideoProvider().animate(pngs["christ"], mp4_k, motion, 5)
    print(f"[anim] {mp4_k}  ({mp4_k.stat().st_size:,} b, {time.time()-t:.0f}s)")
except Exception as e:
    print(f"[anim] Kling FAIL: {e}")

# --- Hook -> $0 ffmpeg Ken Burns slow push-in ---
mp4_kb = OUT / "hook_kenburns.mp4"
print("[anim] hook -> ffmpeg Ken Burns (0$) ...", flush=True)
vf = ("scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
      "zoompan=z='min(zoom+0.0009,1.18)':d=150:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
      "s=1080x1920:fps=30,format=yuv420p")
subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-i",str(pngs["hook"]),
    "-vf",vf,"-t","5","-r","30",str(mp4_kb)], check=True)
print(f"[anim] {mp4_kb}  ({mp4_kb.stat().st_size:,} b)")

print("\nDONE. Compare christ_klingpro.mp4 (paid) vs hook_kenburns.mp4 ($0), 9:16.")
