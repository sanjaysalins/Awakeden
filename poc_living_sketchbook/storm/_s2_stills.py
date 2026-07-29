"""Storm episode — step 2 (v2, full redo). 13 spreads, 9:16, world-bible
anchored + vector-ready + full-bleed framing.

v1 defects this fixes (found on user review after the v1 cut):
- Jesus anchor was a single-roll ad-hoc portrait -- now chains the proper
  repo-level /cast-bible jesus_ref.png (poc_living_sketchbook/_r1_worldbible.py).
- Boat design drifted (masted in some shots, oar-only in others, no lock)
  -- now every boat shot chains world/boat_ref.png.
- Background disciples were unref'd, inventing a new face each render, and
  s09/s10 rendered 5-6 sharply-detailed faces -- a direct T5 render-
  guardrail violation (data/render_guardrails.md: <=3 sharp faces or the
  animator hallucinates on push-in). Now chains cast/disciples_ref.png,
  capped at exactly 3.
- Stills left large blank paper margins around a small inset scene -- each
  SCENE below now explicitly asks the illustration to fill the page edge
  to edge ("use the page"), matching what already worked on the ref anchors.

  .venv\\Scripts\\python.exe poc_living_sketchbook/storm/_s2_stills.py
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
EPISODE = "LS_Storm_v2"
HERE = Path(__file__).resolve().parent
CAST = HERE / "cast"
WORLD_CAST = HERE.parent / "cast"
WORLD = HERE / "world"
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

JESUS_REF = WORLD_CAST / "jesus_ref.png"
DISCIPLES_REF = WORLD_CAST / "disciples_ref.png"
BOAT_REF = WORLD / "boat_ref.png"
FISHERMAN_REF = CAST / "fisherman_sketch_ref.png"
# PHASE B: after s04 is eye-approved, point this at stills/s04_asleep.png so
# every later Jesus still chains BOTH the repo anchor and the approved
# in-episode pose (SKILL.md sec.2 multi-pose identity lock).
JESUS_REF2 = OUT / "s04_asleep.png"

JESUS = (
    "Jesus: a Judean man in his early thirties, long dark wavy hair past "
    "the shoulders parted center, short close-cropped dark beard, a "
    "strong straight nose and defined cheekbones, warm deep brown eyes "
    "level and calm, sun-weathered olive skin, lean wiry-strong build, "
    "simple undyed homespun ankle-length tunic with a woven cord sash, "
    "leather sandals. the SAME man as the reference image(s) -- identical "
    "face, beard, hair, and clothing."
)
DISCIPLES = (
    "EXACTLY three Galilean fishermen and no more -- count them: (1) an "
    "older man with a grey-streaked beard, (2) a robust dark-curly-haired "
    "man in his thirties, (3) a lean younger man in his twenties -- the "
    "SAME three men as the reference image, identical faces. There is NO "
    "fourth person, no partial figure, no extra head or body visible "
    "anywhere in the frame, even partially hidden or turned away -- only "
    "these three men and no one else are present."
)
FISHERMAN = (
    "The Fisherman: a sun-weathered Galilean man in his forties -- "
    "short-cropped dark hair (NOT long or wavy), a thick rough dark beard, "
    "a hard deeply-lined weathered face, a broader stockier build, "
    "rope-callused hands; a single plain undyed knee-length tunic hitched "
    "up and belted for boat work -- ONE continuous garment ending above "
    "the knee, never separate trouser legs; bare feet. the SAME man as the "
    "reference image -- identical face, hair, and clothing."
)
BOAT = (
    "the SAME small open wooden Galilean fishing boat as the reference "
    "image -- identical hull shape, single mast, rigging, and oars"
)
FULLBLEED = (
    "CRITICAL FRAMING: zoom in close enough that the illustrated subject "
    "and its immediate surroundings occupy the ENTIRE frame, corner to "
    "corner. There must be NO large empty cream-paper or kraft-paper "
    "region anywhere inside the frame, and no blank kraft-paper rectangle "
    "or sticky-note patch used as filler -- the torn-edge collage texture "
    "is only a narrow border treatment along the outermost margin, never a "
    "wide blank zone."
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

# (name, refs-tag, scene)
SHOTS_ALL = [
    ("s01_waves", "boat",
     f"A close low-angle view across a night-dark, storm-tossed Sea of "
     f"Galilee: {BOAT} fills most of the frame, black water breaking in "
     f"heavy swells over its near rail, no figures visible, roiling "
     f"ink-blue storm clouds crowding the sky right down to the boat, "
     f"cold blue-wash spray catching a thin edge of moonlight. {FULLBLEED}"),

    ("s02_water", "fisherman",
     f"Extreme close, low angle inside the boat: dark water sloshing past "
     f"bare ankles and feet braced on wet planks, the hem of a single "
     f"undyed knee-length tunic hitched up above the knee -- ONE "
     f"continuous garment, never two separate trouser legs -- a coil of "
     f"wet rope afloat, spray in the air; cold blue-wash light, no face "
     f"visible. {FULLBLEED}"),

    ("s03_screaming", "disciples+boat",
     f"Wide shot inside the pitching boat: {DISCIPLES} straining at a line "
     f"and oars in {BOAT}, faces twisted in terror, soaked tunics, black "
     f"waves towering over the low rail behind them; harsh cold blue-wash "
     f"spray and darkness. {FULLBLEED}"),

    ("s04_asleep", "jesus1+boat",
     f"{JESUS} He lies asleep in the stern of {BOAT} on a folded cloak, one "
     f"arm beneath his head, face utterly at peace; storm spray and heaving "
     f"black water fill the frame around him, but a small pocket of calm "
     f"lamplit warmth surrounds only his sleeping form. {FULLBLEED}"),

    ("s05_hands", "jesus2",
     f"Extreme close on Jesus's SINGLE resting hand only -- only ONE hand "
     f"visible anywhere in the frame, palm open and relaxed against the "
     f"folded cloak, no second hand, no other arm or hand in view -- "
     f"{JESUS} storm water and dark spray blurred and out of focus beyond "
     f"the boat's rail in the background. {FULLBLEED}"),

    ("s06_shaken", "jesus2+fisherman+boat",
     f"Close, urgent framing inside {BOAT}: a fisherman's wet rope-callused "
     f"hand ({FISHERMAN}) gripping Jesus's shoulder to wake him, {JESUS} "
     f"his eyes still closed, spray flying, dark storm chaos pressing in "
     f"from the edges of the frame. {FULLBLEED}"),

    ("s07_eyes", "jesus2+boat",
     f"Mid-shot editorial portrait, pulled back enough to show him seated "
     f"in {BOAT} at correct human scale against the boat's rail and bench "
     f"-- his head must NOT dominate the frame or dwarf the boat, the boat "
     f"structure stays clearly bigger than he is: {JESUS} His eyes just "
     f"opening, face calm and unhurried against the chaos, faint cold "
     f"blue-wash storm light catching one side of his face. {FULLBLEED}"),

    ("s08_verse", "jesus2+boat",
     f"{JESUS} Seated upright now in {BOAT}, face calm and mid-speech, "
     f"storm still raging in soft-focus behind him; warm lamplight on his "
     f"face against the cold blue-wash night. {FULLBLEED}"),

    ("s09_rebuke", "jesus2+disciples+boat",
     f"Wide shot: {JESUS} standing tall in the stern of {BOAT}, one arm "
     f"extended outward toward the black storm, face set and certain; "
     f"below him in the boat, {DISCIPLES} watching, faces turned up toward "
     f"him; towering dark waves and torn storm clouds still raging around "
     f"the boat. {FULLBLEED}"),

    ("s10_calm", "jesus2+disciples+boat",
     f"The SAME wide composition and camera angle as the previous spread, "
     f"{JESUS} still standing with arm extended in the stern of {BOAT}, "
     f"{DISCIPLES} still seated below him, but now the sea lies flat and "
     f"glassy under a clearing sky, soft warm light breaking through "
     f"parting storm clouds. {FULLBLEED}"),

    ("s11_exactly", "boat",
     f"A no-figure spread filling the entire page edge to edge: the "
     f"now-calm sea at dusk fills the whole frame close-up, glassy water "
     f"perfectly mirroring a break of warm gold light through parting "
     f"storm clouds that crowd the sky right to the frame's top edge, "
     f"{BOAT} resting still and LARGE in the middle-foreground, clearly "
     f"detailed, not a tiny distant speck. The watercolor wash itself IS "
     f"the page -- one continuous painted surface from edge to edge."),

    ("s12_knees", "fisherman+boat",
     f"Mid-shot editorial portrait, pulled back enough to show him seated "
     f"in {BOAT} at correct human scale against the boat's hull, bench, "
     f"and rail -- his body must NOT dominate the frame or dwarf the "
     f"boat, the boat structure stays clearly bigger than he is: "
     f"{FISHERMAN} his face uncertain and searching, the hem of his "
     f"single knee-length tunic visible above the water -- ONE continuous "
     f"garment, never separate trouser legs -- calm water now only at his "
     f"ankles in the boat, soft warm light from the clearing sky on one "
     f"side of his face. {FULLBLEED}"),

    ("s13_landing", "boat",
     f"A wide quiet spread: the calm sea's horizon rendered as a TORN HOLE "
     f"in the aged paper itself, radiant warm gold light glowing from "
     f"beneath the page through the tear, a small still silhouette of a "
     f"robed figure standing within the golden light; {BOAT} resting dark "
     f"and quiet in the foreground. {FULLBLEED}"),
]


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
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
    if "jesus1" in tag:
        refs.append(JESUS_REF)
    if "jesus2" in tag:
        refs.append(JESUS_REF)
        if JESUS_REF2.exists():
            refs.append(JESUS_REF2)
    if "disciples" in tag:
        refs.append(DISCIPLES_REF)
    if "fisherman" in tag:
        refs.append(FISHERMAN_REF)
    if "boat" in tag:
        refs.append(BOAT_REF)
    return refs


def main(only=None):
    shots = SHOTS_ALL if only is None else [s for s in SHOTS_ALL if s[0] in only]
    for name, tag, scene in shots:
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        refs = resolve_refs(tag)
        prompt = STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(refs)}) ...", flush=True)
        ok = run(prompt, out, refs)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, refs)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[storm-v2] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    import sys as _sys
    only = _sys.argv[1].split(",") if len(_sys.argv) > 1 else None
    main(only)
