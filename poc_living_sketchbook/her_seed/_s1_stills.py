"""Her Seed (Seed of the Woman short #2, Galatians 4:4)
-- step 1: 8 spreads, 9:16. Adam/Eve/Christ REUSED from repo-level cast
anchors. Mary gets NO fixed cast anchor (the long's own §5 decision: face
always averted, no identity lock) -- s06 self-chains from s04's own
output instead. s03/s05 pass the LOCKED long's own s26/s27 stills as
DESIGN-reference only (16:9 source, this short renders 9:16 -- same
"reference, not cropped panel" pattern short #1 used for its serpent
chain, see `vertical-panels-cross-aspect-reuse`'s own scope).

kling_omni_image is the proven cheap default for this cluster (0.5cr);
seedream_v4_5 for the hero/consistency/landing shots (s04, s06, s08).

Run all (idempotent, skips existing):
  .venv\\Scripts\\python.exe poc_living_sketchbook/her_seed/_s1_stills.py
Run specific shots only:
  .venv\\Scripts\\python.exe poc_living_sketchbook/her_seed/_s1_stills.py s01_eden_coming_apart s08_landing_christ
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
EPISODE = "LS_HerSeed"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

SEED_STILLS = ROOT / "poc_living_sketchbook" / "seed_of_the_woman" / "stills"
STUDY_PAGE_DESIGN_REF = SEED_STILLS / "s26_her_seed_study.png"
LINE_OF_FATHERS_DESIGN_REF = SEED_STILLS / "s27_line_of_fathers.png"
ADAM_REF = ROOT / "poc_living_sketchbook" / "cast" / "adam_ref.png"
EVE_REF = ROOT / "poc_living_sketchbook" / "cast" / "eve_ref.png"
JESUS_REF = ROOT / "poc_living_sketchbook" / "cast" / "jesus_ref.png"
MARY_S04_OUTPUT = OUT / "s04_mary_annunciation.png"

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
    "Near-Eastern complexion. Garment: a crude covering of stitched fig "
    "leaves wrapped and tied to cover the body, modestly but roughly "
    "covered -- THE SAME woman as the reference image, identical face, "
    "hair, and clothing."
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

MARY = (
    "A young woman of Nazareth, modest and plain, no halo, no crown, no "
    "royal dress. Garment: a simple pale homespun robe with a plain veil "
    "covering her hair, drawn loosely over her head and shoulders. Her "
    "face stays AVERTED and bowed, looking down and away -- never turned "
    "to face the viewer, never a clear frontal likeness."
)


# (name, refs, model, scene)
SHOTS = [
    ("s01_eden_coming_apart", [ADAM_REF, EVE_REF], MODEL,
     f"{ADAM} {EVE} A vertical portrait composition, right-side up, "
     "not rotated. Both Adam and Eve stand upright side by side, feet "
     "near the bottom of the frame, heads near the top, facing forward "
     "into the scene, both figures present together. A forest clearing "
     "fills the ENTIRE frame edge to edge -- no blank sky, no empty "
     "paper margin, no inset panel, the trees and undergrowth reach "
     "every edge of the image. Both figures appear at a MODERATE, "
     "clearly visible size in the middle distance among the trees -- "
     "not a tight close portrait, but not tiny or distant either, both "
     "plainly readable, standing together. Leaves fall visibly FROM "
     "the trees and drift down THROUGH the canopy around and past the "
     "two figures, part of the living forest, never floating over open "
     "blank space. The whole forest -- leaves, bark, undergrowth, "
     "canopy -- is rendered in cold desaturated grey-green tones, "
     "visibly draining of its earlier warm color. Tucked in one corner "
     "of the frame, small and easy to miss, one thin faint thread of "
     "warm gold light."),

    ("s02_promise_spoken_over_eve", [EVE_REF], MODEL,
     f"{EVE} WIDE: Eve standing alone in the garden, her face and "
     "expression calm and peaceful, listening -- not afraid, not wary. "
     "A CLEARLY VISIBLE soft column of warm golden light descends from "
     "directly above and pools visibly on her face, shoulders, and the "
     "ground at her feet, noticeably brighter and warmer than the rest "
     "of the dim garden around her. No human or divine figure represents "
     "the light itself -- light only, but the light itself must be "
     "obviously, unmistakably present and glowing in the image."),

    ("s03_already_written_page", [STUDY_PAGE_DESIGN_REF], MODEL,
     "CLOSE object-insert, portrait framing: a single old open page "
     "resting on a wooden desk, already filled edge to edge with fine "
     "ancient handwritten ink, settled and old -- not being written now, "
     "already finished long ago. One small warm oil lamp glows beside "
     "it, its light falling on the page. No hand, no pen, no quill "
     "anywhere in frame."),

    ("s04_mary_annunciation", [], "seedream_v4_5",
     f"{MARY} ACTING spread, portrait framing: a young woman, veiled, "
     "bowed and face averted downward, both hands gathering together "
     "at her heart -- a soft unseen radiant warm light falling on her "
     "from directly above. No angel figure visible anywhere -- the "
     "light itself is the only sign of a presence."),

    ("s05_line_of_fathers_vertical", [], MODEL,
     "A vertical GENEALOGY LINE device, portrait framing. EVERY figure "
     "stands NORMALLY UPRIGHT -- feet at the bottom, head at the top, "
     "exactly like a person standing on the ground; the image itself is "
     "NOT rotated or sideways. 5 small anonymous SOLID SILHOUETTED "
     "men's figures -- flat solid dark ink silhouettes only, no facial "
     "features, no visible clothing color or pattern, no individual "
     "detail distinguishing one figure from another -- arranged in a "
     "vertical stack of 5 separate rows one below another going DOWN "
     "the page. One single continuous thin drawn line zigzags DOWNWARD "
     "through the page, touching each upright silhouette in turn as it "
     "descends from the top row to the bottom row, like a family line "
     "passed down through father after father. absolutely NO numbers, "
     "NO digits, NO measurements, NO labels, NO text or lettering of "
     "any kind anywhere in the image -- this is a plain silhouette "
     "genealogy line, not a diagram or chart."),

    ("s06_mary_close", [MARY_S04_OUTPUT], "seedream_v4_5",
     f"{MARY} Mary stands in the foreground at a respectful distance, "
     "veiled, her face raised upward toward something unseen ahead of "
     "her -- quiet grief held with reverence, calm contained sorrow, "
     "not despair, not weeping openly. Her hands stay low and close, "
     "clasped quietly together at her waist or held gently against "
     "herself -- NOT raised, NOT outstretched, NOT open to the sky, no "
     "wide gesture of any kind, her whole posture still and folded "
     "inward, a mother's silent grief, not a triumphant or worshipful "
     "pose. Far behind her, a plain wooden cross rises against a "
     "darkening dusk sky -- the cross itself EMPTY, bare, no figure on "
     "it or near it, just the bare wooden cross alone against the sky. "
     "The whole scene is hushed and muted -- deep dusky blues and "
     "violets in the sky, the ground in soft shadow."),

    ("s07_hands_reaching", [], MODEL,
     "EXTREME CLOSE object-insert, hands and forearms ONLY: two human "
     "hands and forearms reaching gently forward into the frame, "
     "fingers loosely open and extended, yearning and hopeful rather "
     "than clawing or grasping. The image is cropped tightly at the "
     "wrist and lower forearm -- absolutely no shoulders, neck, chest, "
     "or head anywhere in the frame, no face, nothing above the "
     "forearms."),

    ("s08_landing_christ", [JESUS_REF], "seedream_v4_5",
     f"{JESUS} LANDING, sacred stillness, portrait framing: Christ "
     "standing in radiant warm gold light, seen from a respectful "
     "distance, calm and reverent, the light surrounding His whole "
     "figure, held as a single iconic image, no cross needed here -- "
     "just His radiant presence, already arrived."),
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
                cost.record_hf(EPISODE, "short", "stills", model, note=f"[her-seed] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
