"""Seed of the Woman LONG -- stills stage. Spreads 1-5 promoted from the
POC30 process-validation test (memory `day-of-atonement-retro-learnings`);
extend SPREAD_SHOTS as the full plan is authored. Follows the exact
code pattern of day_of_atonement/_s2_stills.py (same STYLE constant, same
repo-level cast-bible anchor chaining, same FULLBLEED framing note, same
run()/resolve_refs()/main() shape) -- fix #9 (check the sibling episode's
real script chain before assuming a generic skill applies).

Renders, in order: 3 anchors (Adam, Eve, Eden world -- new cast/world dir,
$0 cross-style reuse is not possible per the locked provider-split rule),
then the 5 spread stills chained to those anchors. Every prompt authored
per the fix #7 discipline (camera-angle/shot-type from _PREFLIGHT.md,
period-accurate detail -- fig-leaf aprons per Gen 3:7, not skin coats,
which come later at 3:21) BEFORE the first render, not learned via re-roll.

  .venv\\Scripts\\python.exe poc_living_sketchbook/seed_of_the_woman/_s2_stills.py
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
MODEL = "nano_banana_pro"
EPISODE = "SeedOfTheWoman"
HERE = Path(__file__).resolve().parent
CAST = HERE.parent / "cast"
WORLD = HERE.parent / "world"
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

ADAM_REF = CAST / "adam_ref.png"
EVE_REF = CAST / "eve_ref.png"
EDEN_REF = WORLD / "eden_ref.png"

REF_MAP = {"adam": ADAM_REF, "eve": EVE_REF, "eden": EDEN_REF}

# ---- canon text, matching cast/AARON.md's level of detail ----

ADAM = (
    "Adam: the first man, freshly made that same day (Genesis 2:7) -- a "
    "man in the full prime of life, never old, never a boy. Face geometry: "
    "a strong open brow, straight nose, firm jaw, unweathered skin -- a "
    "face with no lines of age yet, only the new shock of fear and shame. "
    "Hair: dark brown, short, natural, uncut (no barber has ever touched "
    "it). Beard: short, close, natural growth, never groomed or shaped by "
    "a blade. Skin: warm olive Near-Eastern complexion, entirely "
    "unweathered -- this is the FIRST day anyone has ever been afraid. "
    "Build: powerfully made, broad-shouldered, an unspoiled human frame in "
    "its prime. Eyes: wide, stricken, ashamed -- a man who has never once "
    "before felt fear. Garment: a crude covering of stitched fig leaves "
    "tied at the waist as an apron (Genesis 3:7) -- NOT a coat of animal "
    "skin (that comes later, Genesis 3:21, after this scene) -- otherwise "
    "bare-chested, no other clothing of any kind."
)

EVE = (
    "Eve: the first woman, freshly made that same day (Genesis 2:22) -- a "
    "woman in the full prime of life, never old, never a girl. Face "
    "geometry: soft even features, wide clear eyes, a face with no lines "
    "of age yet, only the new shock of fear and shame. Hair: long, dark, "
    "loose and natural, uncut and unbound by any ornament (no comb, no "
    "clasp, no ribbon has ever touched it). Skin: warm olive Near-Eastern "
    "complexion, entirely unweathered. Build: an unspoiled human frame in "
    "its prime. Eyes: wide, stricken, ashamed -- a woman who has never "
    "once before felt fear. Garment: a crude covering of stitched fig "
    "leaves (Genesis 3:7) wrapped and tied to cover the body -- NOT a coat "
    "of animal skin (that comes later, Genesis 3:21, after this scene) -- "
    "modestly but roughly covered, nothing woven, nothing dyed, nothing "
    "ornamental."
)

EDEN = (
    "The garden of Eden at the cool of the day (Genesis 3:8): dense, "
    "unspoiled, ancient trees with heavy dark-green canopy, dappled "
    "warm-gold late-afternoon light breaking through in shafts, thick "
    "underbrush and broad-leafed plants at ground level offering places to "
    "hide, no path, no cultivation lines, no structure of any kind visible "
    "-- a wild, lush, pre-agricultural paradise, now carrying the FIRST "
    "shadow it has ever had to carry: the light still golden but the mood "
    "gone wrong, a faint coolness/greyness creeping in at the forest's "
    "deep background edges as if the garden itself senses the fall."
)

STYLE = (
    "Editorial documentary sketch illustration: loose confident graphite-and-ink "
    "linework with muted watercolor wash, drawn on aged warm cream paper. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured stock, "
    "torn and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile hand-made "
    "feel, muted ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge. CRITICAL: absolutely NO lettering, numerals, words, newsprint, "
    "printed book-page text, handwriting, ruler markings, dates, or captions "
    "ANYWHERE on ANY layer -- every paper surface is BLANK textured stock."
)

LORD_PRESENCE = (
    "the presence of the LORD: no figure, no face, no human or angelic "
    "form of any kind -- only a low warm golden light moving gently among "
    "the trees, felt as an overwhelming approaching presence rather than "
    "seen as a person."
)

FULLBLEED = (
    "CRITICAL FRAMING: zoom in close enough that the illustrated subject "
    "and its immediate surroundings occupy the ENTIRE frame, corner to "
    "corner, no wide empty margins of bare paper around the main subject."
)

# ---- anchors (eden_ref FIRST -- adam/eve chain to it for a consistent
# background; order matters, resolve_refs() only finds refs already on disk) ----
ANCHOR_SHOTS = [
    ("eden_ref", STYLE, "",
     f"{EDEN} Wide establishing view, eye-level, no figures present. "
     f"{FULLBLEED}"),
    ("adam_ref", STYLE, "eden",
     f"Portrait, medium shot, eye-level: {ADAM}, standing among the trees "
     f"of the same garden, caught mid-motion trying to hide, looking "
     f"back over his shoulder toward the camera with dawning fear. "
     f"{FULLBLEED}"),
    ("eve_ref", STYLE, "eden",
     f"Portrait, medium shot, eye-level: {EVE}, standing among the trees "
     f"of the same garden, caught mid-motion trying to hide, looking "
     f"back over her shoulder toward the camera with dawning fear. "
     f"{FULLBLEED}"),
]

# ---- the 5 real spreads ----
SPREAD_SHOTS = [
    ("s01_something_wrong", STYLE, "adam,eve,eden",
     f"HIGH-ANGLE wide view looking down into the garden: {ADAM} and "
     f"{EVE}, small and distant in the frame against the vast unspoiled "
     f"canopy of {EDEN.split(':')[0]}, both crouched low near a dense "
     f"thicket, backs turned to the camera, isolated and small against "
     f"the scale of the garden -- the first faint wrongness showing only "
     f"as a cool greyness bleeding in at the frame's far edges. "
     f"{FULLBLEED}"),
    ("s02_the_hiding", STYLE, "adam,eve,eden",
     f"MEDIUM shot, eye-level, camera positioned low among broad-leafed "
     f"undergrowth as if hiding alongside them: {ADAM} and {EVE} pressed "
     f"close together behind a thick tree trunk and heavy foliage, "
     f"genuinely concealed (not merely standing near cover), both facing "
     f"AWAY from camera toward unseen approaching light, tense stillness. "
     f"{FULLBLEED}"),
    ("s04_god_walking", STYLE, "eden",
     f"WIDE-ANGLE, LOW angle looking UP through the tree canopy: "
     f"{LORD_PRESENCE} moving gently through {EDEN.split(':')[0]}, "
     f"golden light catching the undersides of leaves and drifting motes "
     f"of pollen/dust in the beams, no figure of any kind, the whole "
     f"canopy responding to the light's slow movement. {FULLBLEED}"),
    ("s05_where_art_thou", STYLE, "eden",
     f"Close, held, eye-level: {LORD_PRESENCE} now still, resting low "
     f"and warm in a gap between two tree trunks, framed by dark "
     f"foliage on both sides so the light itself is the entire subject "
     f"of the frame, quiet and waiting. {FULLBLEED}"),
]


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "16:9", "--resolution", "2k", "--wait"]
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


def resolve_refs(tag):
    refs = []
    for t in tag.split(","):
        t = t.strip()
        if t and REF_MAP.get(t) and REF_MAP[t].exists():
            refs.append(REF_MAP[t])
    return refs


ANCHOR_DEST = {"adam_ref": CAST, "eve_ref": CAST, "eden_ref": WORLD}


def render_set(shots, dest_of, label):
    for name, style, tag, scene in shots:
        out_dir = dest_of(name)
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        refs = resolve_refs(tag)
        prompt = style + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(refs)}) ...", flush=True)
        ok = run(prompt, out, refs)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, refs)
        if ok:
            try:
                cost.record_hf(EPISODE, "long", label, MODEL, note=f"[seed_of_the_woman] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")


def main():
    print("=== anchors ===")
    render_set(ANCHOR_SHOTS, lambda name: ANCHOR_DEST[name], "anchors")
    print("=== spreads ===")
    render_set(SPREAD_SHOTS, lambda name: OUT, "spreads")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
