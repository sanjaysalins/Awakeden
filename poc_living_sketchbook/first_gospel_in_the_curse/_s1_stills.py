"""The First Gospel in the Curse (Seed of the Woman short #1, Genesis 3:15)
-- step 1: 11 spreads, 9:16. Adam/Eve/Christ REUSED from repo-level cast
anchors; the serpent object chains from Seed of the Woman LONG's own
approved design (s18_turns_to_serpent.png) -- same "distilled from the
locked long" continuity this cluster's own manifest blurb calls for.
God's presence is NEVER a human figure (locked rule) -- unseen radiant
light only, matching the LONG's own "where-art-thou" convention.

kling_omni_image is the proven cheap default for this cluster (0.5cr);
seedream_v4_5 for the compositionally complex shots (s07's atmosphere
metaphor, s09's transition device, s10's landing).

Run all (idempotent, skips existing):
  .venv\\Scripts\\python.exe poc_living_sketchbook/first_gospel_in_the_curse/_s1_stills.py
Run specific shots only:
  .venv\\Scripts\\python.exe poc_living_sketchbook/first_gospel_in_the_curse/_s1_stills.py s01_hook s10_landing_christ
"""
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "kling_omni_image"
EPISODE = "LS_FirstGospelInTheCurse"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

SEED_STILLS = ROOT / "poc_living_sketchbook" / "seed_of_the_woman" / "stills"
SERPENT_REF = SEED_STILLS / "s18_turns_to_serpent.png"
ADAM_REF = ROOT / "poc_living_sketchbook" / "cast" / "adam_ref.png"
EVE_REF = ROOT / "poc_living_sketchbook" / "cast" / "eve_ref.png"
JESUS_REF = ROOT / "poc_living_sketchbook" / "cast" / "jesus_ref.png"

STYLE = (
    "Editorial documentary sketch illustration: loose confident graphite-and-ink "
    "linework with muted watercolor wash, drawn on aged warm cream paper. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured stock, "
    "torn and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile hand-made "
    "feel, muted ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge."
)

ADAM = (
    "Adam: the first man, in the full prime of life, never old, never a boy. "
    "Face geometry: a strong open brow, straight nose, firm jaw, unweathered "
    "skin. Hair: dark brown, short, natural. Beard: short, close, natural. "
    "Skin: warm olive Near-Eastern complexion. Build: powerfully made, "
    "broad-shouldered. Eyes: wide, stricken, ashamed. Garment: a crude "
    "covering of stitched fig leaves tied at the waist as an apron, "
    "otherwise bare-chested -- THE SAME man as the reference image, "
    "identical face, hair, beard, and clothing."
)

EVE = (
    "Eve: the first woman, in the full prime of life, never old, never a "
    "girl. Face geometry: soft even features, wide clear eyes. Hair: long, "
    "dark, loose and natural, uncut and unbound. Skin: warm olive "
    "Near-Eastern complexion. Eyes: wide, stricken, ashamed. Garment: a "
    "crude covering of stitched fig leaves wrapped and tied to cover the "
    "body, modestly but roughly covered -- THE SAME woman as the reference "
    "image, identical face, hair, and clothing."
)

JESUS = (
    "Jesus: a Judean man in his early thirties. Face geometry: a strong "
    "straight nose, defined cheekbones, a broad calm forehead, an angular "
    "jaw beneath the beard. Hair: long dark wavy hair falling past the "
    "shoulders, parted center. Beard: short, close-cropped, dark, well-kept. "
    "Skin: sun-weathered olive Mediterranean complexion. Build: lean and "
    "wiry-strong. Eyes: warm deep brown, level and calm. Garment: simple "
    "undyed homespun ankle-length tunic with a woven cord sash -- THE SAME "
    "man as the reference image, identical face, beard, hair, and clothing."
)

# (name, refs, model, scene)
SHOTS = [
    ("s01_hook_hands", [], MODEL,
     "EXTREME CLOSE object-insert: two human hands, shaking slightly, "
     "tying a crude cord of stitched fig leaves at a waist, tense and "
     "afraid, no face in frame, soft raking light on the leaves and skin."),

    ("s02_waiting_in_trees", [ADAM_REF, EVE_REF], MODEL,
     f"{ADAM} {EVE} WIDE: Adam and Eve standing together among dense "
     "garden trees, both stricken with fear, half-hidden among broad "
     "leaves and trunks, waiting, the garden dim around them."),

    ("s03_turns_to_serpent", [SERPENT_REF], "seedream_v4_5",
     "WIDE: THE SAME pale grey-tan serpent as the reference image, coiled "
     "low among tree roots -- a soft unseen radiant light breaks low "
     "through the garden trees and falls directly onto the serpent, "
     "singling it out, the rest of the garden dim around it. No human or "
     "divine figure visible anywhere -- the light itself is the only sign "
     "of a presence."),

    ("s04_serpent_in_light", [SERPENT_REF], MODEL,
     "CLOSE: THE SAME pale grey-tan serpent as the reference image, held "
     "still in a soft unseen radiant light, its head slightly lifted as "
     "if listening. No human or divine figure visible -- light only."),

    ("s05_heel_and_head_insert", [], MODEL,
     "CLOSE-UP narrative garden scene: a bare human foot and ankle, warm "
     "olive Near-Eastern skin, stepping down through tall grass and dark "
     "damp garden soil at the base of a tree, low green foliage and a few "
     "fallen leaves brushing against the ankle and partly covering the "
     "lower foot -- this is a moment in a story, a person walking through "
     "a garden, not a study of the foot alone. One small, faint, dark "
     "reddish-brown mark on the heel itself, like a faint bruise, "
     "tasteful and non-graphic. Soft raking light."),

    ("s06_turn_to_eve_adam", [ADAM_REF, EVE_REF], MODEL,
     f"{ADAM} {EVE} WIDE: the same soft unseen radiant light now shifts "
     "away from the serpent and falls on Adam and Eve instead, both "
     "turning to face it, stricken, their own judgment arriving. No "
     "human or divine figure represents the light itself."),

    ("s07_gold_thread_in_curse", [], "seedream_v4_5",
     "WIDE, no figure: a wide view of the dim, shadowed garden at dusk, "
     "heavy dark storm-colored clouds low over the trees -- and running "
     "through the very center of that darkness, one single thin, "
     "continuous thread of warm gold light, woven through the shadow "
     "like a seam sewn into the fabric of the dark clouds themselves, "
     "faint but unbroken, the only warmth in the whole frame."),

    ("s08a_eve_face_conviction", [EVE_REF], MODEL,
     f"{EVE} CLOSE portrait, Eve's face alone, processing something "
     "quietly overwhelming -- not fear now but a stunned, grateful "
     "disbelief, soft even light."),

    ("s08b_open_hands", [], MODEL,
     "CLOSE object-insert: two human hands, open and empty, palms "
     "upward, resting still and unclenched -- the same hands from the "
     "opening shot but no longer shaking, no longer tying anything, "
     "simply open. No face in frame."),

    ("s09_landing_transition", [SERPENT_REF, JESUS_REF], "seedream_v4_5",
     f"{JESUS} A landing-device spread: the dim garden and THE SAME pale "
     "serpent-on-the-ground as the reference image dissolve and tear away "
     "like old paper at the center of the frame, and through that torn "
     "opening, warm gold light pours out -- and within the light, Christ "
     "is beginning to appear, seen from a respectful distance, radiant, "
     "the type becoming the antitype. The torn paper's fibrous edges are "
     "lit warm gold from behind."),

    ("s10_landing_christ", [JESUS_REF], "seedream_v4_5",
     f"{JESUS} LANDING, sacred stillness: Christ standing in radiant warm "
     "gold light, seen from a respectful distance, calm and reverent, "
     "the light surrounding His whole figure, held as a single iconic "
     "image, no cross needed here -- just His radiant presence answering "
     "the garden's own darkness."),
]


def run(prompt, out, refs, model=MODEL):
    cmd = [HF, "generate", "create", model, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--wait"]
    cmd += ["--quality", "high"] if model == "seedream_v4_5" else ["--resolution", "2k"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    only = set(sys.argv[1:]) or None
    for name, refs, model, scene in SHOTS:
        if only and name not in only:
            continue
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        prompt = STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (model={model}, refs={len(refs)}) ...", flush=True)
        ok = run(prompt, out, refs, model=model)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, refs, model=model)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "stills", model, note=f"[first-gospel-in-the-curse] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
