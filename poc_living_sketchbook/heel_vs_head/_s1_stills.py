"""Heel vs Head (Seed of the Woman short #3, Genesis 3:15) -- step 1: 7
spreads, 9:16. No Adam/Eve this piece (narration never names them) --
Christ reused from repo cast anchor; the serpent chains as a DESIGN
reference from short #1's own approved art (`first_gospel_in_the_curse/
stills/s03_turns_to_serpent.png`, `s04_serpent_in_light.png`,
`s05_heel_and_head_insert.png` -- this piece is essentially a second pass
at that exact heel/head contrast).

kling_omni_image is the proven cheap default for this cluster (0.5cr);
seedream_v4_5 for the hero/consistency/landing shots (s04, s07).

Run all (idempotent, skips existing):
  .venv\\Scripts\\python.exe poc_living_sketchbook/heel_vs_head/_s1_stills.py
Run specific shots only:
  .venv\\Scripts\\python.exe poc_living_sketchbook/heel_vs_head/_s1_stills.py s01_duel_motif s07_landing_christ
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
EPISODE = "LS_HeelVsHead"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

FGC_STILLS = ROOT / "poc_living_sketchbook" / "first_gospel_in_the_curse" / "stills"
SERPENT_TURNS_REF = FGC_STILLS / "s03_turns_to_serpent.png"
SERPENT_LIGHT_REF = FGC_STILLS / "s04_serpent_in_light.png"
HEEL_HEAD_REF = FGC_STILLS / "s05_heel_and_head_insert.png"
JESUS_REF = ROOT / "poc_living_sketchbook" / "cast" / "jesus_ref.png"
SERPENT_S04_OUTPUT = OUT / "s04_serpent_pronouncement.png"

STYLE = (
    "Editorial documentary sketch illustration: loose confident graphite-and-ink "
    "linework with muted watercolor wash, drawn on aged warm cream paper. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured stock, "
    "torn and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile hand-made "
    "feel, muted ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge."
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
    ("s01_duel_motif", [], MODEL,
     "A SYMBOLIC WIDE composition, no serpent, no clear figures -- two "
     "opposing dark silhouetted shapes or forces face each other across "
     "the frame in a deliberately BALANCED, evenly-matched standoff, "
     "mirror-symmetric composition, equal size, equal weight on both "
     "sides -- an image of a fair fight or a tie, cold desaturated "
     "grey-blue tones, tense stillness."),

    ("s02_bruise_vs_crush_split", [], MODEL,
     "A CLOSE object-insert, portrait framing, the frame split cleanly "
     "into two halves by a hard vertical line down the center. Both "
     "halves show ONLY plain close-up skin texture, zoomed in so close "
     "that no larger body part, limb, or facial feature is recognizable "
     "-- purely abstract skin surface, like a macro photograph. LEFT "
     "half: a small, minor bruise mark on the plain skin texture, "
     "barely visible, healing, unremarkable. RIGHT half: the skin "
     "texture gives way to a deep fractured crack running through solid "
     "stone or bone underneath, severe and irreversible. Absolutely no "
     "eyes, no face, no recognizable body part anywhere in the image --"
     " texture and material only."),

    ("s03_serpent_judged", [SERPENT_TURNS_REF, SERPENT_LIGHT_REF], MODEL,
     "WIDE, portrait framing: a dark serpent coiled low in a garden "
     "clearing, THE SAME serpent as the reference images -- identical "
     "scale pattern, coloring, and coiled form. A soft unseen radiant "
     "column of warm light descends from directly above onto the "
     "serpent, arriving, present -- no human or divine figure, light "
     "only. The garden around it is shadowed, cold, still. No other "
     "creatures present."),

    ("s04_serpent_pronouncement", [SERPENT_TURNS_REF, SERPENT_LIGHT_REF], "seedream_v4_5",
     "HERO, CLOSE portrait framing, tighter than a wide shot: the same "
     "dark serpent, closer now, its head raised slightly as if hearing "
     "words spoken over it. The unseen radiant light is more intense "
     "and directive here, a focused beam rather than ambient glow, "
     "clearly falling ON the serpent -- a pronouncement being made, not "
     "just presence. No human or divine figure, light only. Held as a "
     "single iconic image."),

    ("s05_heel_and_head_insert", [HEEL_HEAD_REF], MODEL,
     "A CLOSE object-insert, portrait framing, design-reference from the "
     "attached image: two elements held together in one composition -- "
     "on one side, a serpent's head, LIFELESS and completely still, "
     "flattened and fractured under visible weight, its shape caved "
     "and broken -- eyes closed or empty, mouth fully closed, jaw "
     "slack, no fangs bared, no tongue extended, not coiled, not "
     "posed to strike, entirely limp and defeated, like a pressed "
     "flat object rather than a living creature. On the other side, a "
     "human heel and ankle, unbroken, a single small mark on it but "
     "whole and standing, calm and steady. The "
     "utterly destroyed, one intact."),

    ("s06_own_blow_straining", [], MODEL,
     "A CLOSE-TO-MEDIUM shot of a single generic human figure, face "
     "turned away or in shadow so no clear identity is visible, body "
     "straining and twisted mid-motion as if throwing a punch or blow "
     "at something unseen just out of frame -- tense muscles, exertion, "
     "alone in a bare dim space, no other figures, no serpent, no "
     "target visible, just the effort itself."),

    ("s07_landing_christ", [JESUS_REF], "seedream_v4_5",
     f"{JESUS} LANDING, sacred stillness, portrait framing: Christ on "
     "the cross, seen from a respectful reverent distance, arms "
     "extended along the crossbeam, head bowed, no visible wounds, no "
     "blood, radiant warm gold light surrounding the scene. Low near "
     "the base of the cross, small and still, a dark crushed serpent's "
     "head rests motionless on the ground -- the two facts held "
     "together in one image, held as a single iconic tableau."),
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
        if refs and any(not Path(r).exists() for r in refs):
            print(f"[HOLD] {name}: missing ref {[str(r) for r in refs if not Path(r).exists()]}")
            continue
        prompt = STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (model={model}, refs={len(refs)}) ...", flush=True)
        ok = run(prompt, out, refs, model=model)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, refs, model=model)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "stills", model, note=f"[heel-vs-head] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
