"""Render assets for the 3-variant SHORT energy test (EW01 hook + strange-thing).
Stills: 4 new painterly 9:16 (+ reuse the existing hook.png). Clips: V1 viral
gallery-tour + V2 parallax-depth, both via the LOCKED shorts path (Kling 3.0 pro 9:16).
V3 reuses V1's clips at assembly. ~$8."""
import sys, time, importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render
sh = importlib.import_module("_hf_animate_short")   # viral_prompt + hf_animate (kling3_0 pro)

TEST = ROOT / "longform" / "EW01_Two_Goats" / "v1" / "short" / "visual_9x16_test"
OUT = TEST / "variants"
OUT.mkdir(parents=True, exist_ok=True)

config.VISUAL_STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and "
    "Rembrandt lighting, deep shadow and warm golden light, reverent sacred art, muted "
    "earth tones, fine visible brushwork")
config.VISUAL_STYLE_TAIL = "no text, no modern elements, vertical 9:16 composition"

# id, subject_block, macro_elements (expressive anchors for the viral gallery-tour)
STILLS = [
 ("s2_two_goats",
  "Two goats standing side by side before a rough stone altar in an ancient tabernacle "
  "court at dawn; one goat turned toward the smoking altar, the other toward an open "
  "desert gate; a white-linen priest's hand resting near them; deep shadow, golden light.",
  ["the two goats' heads", "the stone altar flame", "the priest's hand"]),
 ("s3_blood_veil",
  "A priest in plain white linen carrying a shallow bronze basin of blood through thick "
  "darkness toward a faint golden glow of the mercy seat, his arm raised to sprinkle; the "
  "blood catching the light; seen from behind and side.",
  ["the bronze basin of blood", "the priest's raised hand", "the golden glow"]),
 ("s4_hands_confess",
  "A white-linen priest laying both hands upon the head of a living goat, his own head "
  "bowed low in confession; the edge of the camp and the open pale desert behind; "
  "half-shadowed, solemn.",
  ["the priest's hands on the goat's head", "the priest's bowed face", "the goat's eye"]),
 ("s5_scapegoat_desert",
  "A single small goat walking away down a cracked desert valley into a vast bleached "
  "wilderness under an immense pale sky; at the near edge, seen from behind, a lone robed "
  "man watches it go, dwarfed by the emptiness; heat-haze, drifting dust.",
  ["the small distant goat", "the watching man's back", "the empty desert horizon"]),
]

# S1 hook reuses the already-rendered still
hook = TEST / "hook.png"
scenes = [("s1_hook", hook, ["the priest's hand gripping the curtain",
                             "the dark gap and golden glow beyond", "the oil lamp flame"])]

prov = visual_render.HFProvider()   # 9:16 default
for sid, subj, macros in STILLS:
    sc = Scene(index=0, slug=sid, title=sid, scene_type="single", arc_position="body",
        framing="medium", purpose=sid, rationale="variant test",
        visible_elements=subj[:180], emotional_tone="reverent",
        subject_block=subj, mood_block="reverent, period, vertical", jesus_variant=None)
    png = OUT / f"{sid}.png"
    if png.exists():
        print(f"[img ] skip {sid}"); scenes.append((sid, png, macros)); continue
    print(f"[img ] {sid} (HF 9:16) ...", flush=True); t = time.time()
    png.write_bytes(prov.generate(sc))
    print(f"[img ] {png}  ({png.stat().st_size:,} b, {time.time()-t:.0f}s)")
    scenes.append((sid, png, macros))

PARALLAX = ("A still finished Baroque oil painting on flat canvas, filmed with a strong "
    "cinematic 3D PARALLAX dolly: the camera glides slowly sideways and inward while the "
    "foreground separates from the background with real depth, layers sliding at different "
    "speeds. The painting never moves, breathes or morphs; only the camera. INVENT NOTHING "
    "not already painted. Steady light, no sparkles, no glitter, no bloom.")

for sid, png, macros in scenes:
    v1 = OUT / f"{sid}.v1_viral.mp4"
    v2 = OUT / f"{sid}.v2_parallax.mp4"
    if not v1.exists():
        pr = sh.viral_prompt({"macro_elements": macros})
        print(f"[V1 viral   ] {sid} ...", flush=True); t = time.time()
        ok = sh.hf_animate(png, v1, pr, 5)
        print(f"   {'ok' if ok else 'FAIL'} ({time.time()-t:.0f}s)")
    if not v2.exists():
        print(f"[V2 parallax ] {sid} ...", flush=True); t = time.time()
        ok = sh.hf_animate(png, v2, PARALLAX, 5)
        print(f"   {'ok' if ok else 'FAIL'} ({time.time()-t:.0f}s)")

print("\nDONE. stills + V1/V2 clips in", OUT)
