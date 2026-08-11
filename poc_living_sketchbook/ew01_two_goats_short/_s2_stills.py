"""EW01 Two Goats short -- Stage 2, stills. First real production build on
the Stationer (MEDIUM_SELECTION.md): style_for() looks up a per-spread
MEDIUM first (a tipped-in paper style, from pipeline/medium_registry.py),
falling back to the frozen living-sketchbook home STYLE block. Per
_PLAN.md, only s06_scapegoat carries a medium (md_survey_plate) -- every
other spread stays home.

Cast (both reused, $0): Aaron/Priest (poc_living_sketchbook/two_goats/cast/
priest_sketch_ref.png) and Jesus (poc_castbible_look/episode_door/cast/
jesus_sketch_ref.png).
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
from pipeline.medium_registry import MEDIUMS

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "EW01_TwoGoats_Sketchbook_Pilot"
HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
STILLS.mkdir(exist_ok=True)

CAST_DIR = ROOT / "poc_living_sketchbook"
AARON_REF = CAST_DIR / "two_goats" / "cast" / "priest_sketch_ref.png"
# Repo-level canonical Jesus anchor (cast/JESUS.md, promoted 2026-07-29 from
# the older single-roll Door-episode anchor with full /cast-bible rigor --
# "early thirties" explicit, richer face geometry). This is the anchor used
# everywhere else in current production (Bronze Serpent Long, Storm, Day of
# Atonement); the Door-episode anchor is a stale pointer, not the current one.
JESUS_REF = CAST_DIR / "cast" / "jesus_ref.png"

AARON = (
    "The Priest: an aging Hebrew man in his sixties -- deep-set solemn eyes, "
    "a long grey beard, a weathered careworn face marked by decades of duty; "
    "dressed ENTIRELY in plain undyed white linen for the Day of Atonement -- "
    "a plain linen coat, linen breeches, a linen girdle, a linen turban -- no "
    "gold, no jewels, no embroidered breastplate of any kind; bare feet. the "
    "SAME man as the reference image -- identical face, hair, and clothing."
)
JESUS = (
    "Jesus: a Judean man in his early thirties. Face geometry: a strong "
    "straight nose, defined cheekbones, a broad calm forehead, an angular "
    "jaw beneath the beard. Hair: long dark wavy hair falling past the "
    "shoulders, parted center. Beard: short, close-cropped, dark, "
    "well-kept. Skin: sun-weathered olive Mediterranean complexion. Build: "
    "lean and wiry-strong, a carpenter's and traveler's frame. Eyes: warm "
    "deep brown, level and calm, looking in the same direction, never wide "
    "or staring. Hands: strong, calloused, a craftsman's hands. Garment: "
    "simple undyed homespun ankle-length tunic with a woven cord sash, "
    "leather sandals -- the same every appearance. the SAME man as the "
    "reference image -- identical face, beard, hair, and clothing."
)

HOME_STYLE = (
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
FULLBLEED = (
    "CRITICAL FRAMING: zoom in close enough that the illustrated subject and "
    "its immediate surroundings occupy the ENTIRE frame, corner to corner. "
    "No large empty paper region anywhere inside the frame."
)


def assemble_prompt(medium_id: str | None, scene: str) -> str:
    """None = home (frozen STYLE block, its own no-lettering clause already
    baked in). An id = the Stationer medium REPLACES the block -- and MUST
    go through Medium.prompt(), never the raw anchor_text, because that is
    the only path that appends the GUARDRAIL suffix (the one clause that
    bans legible text/numerals). Skipping it is exactly what let
    s06_scapegoat's first render come back as a labeled geology diagram."""
    if medium_id is None:
        return f"{HOME_STYLE}\n\nSCENE: {scene}"
    return MEDIUMS[medium_id].prompt(f"SCENE: {scene}")


# (slug, medium_id_or_None, ref_path_or_None, scene_text)
JOBS = [
    ("s01_hook", "md_night_ink", AARON_REF,
     f"{AARON} A low-angle shot from just behind Aaron's shoulder, standing "
     "at the threshold of a heavy woven curtain inside a dark stone "
     "sanctuary, one hand raised to draw it back, his face turned toward "
     "the black gap beyond, tense and solemn -- a doorway into the dark he "
     f"is not certain he will return from. {FULLBLEED}"),

    ("s02_two_goats", None, AARON_REF,
     f"{AARON} An eye-level wide shot: two live goats tethered side by side "
     "before a plain stone altar in an open courtyard, Aaron standing beside "
     "them with one hand resting on the nearer goat's back, morning light, "
     f"plain sanctuary walls behind. {FULLBLEED}"),

    ("s03_blood_veil", None, AARON_REF,
     f"{AARON} A low mid-shot: Aaron carrying a plain clay basin before him "
     "with both hands, dark liquid within, walking toward a heavy woven "
     f"curtain, his eyes fixed ahead, solemn. {FULLBLEED}"),

    ("s04_hands_head", None, AARON_REF,
     f"{AARON} A close mid-shot: Aaron's two weathered hands pressed firmly "
     "on the head of a second, living goat, his head bowed low over the "
     f"animal, lips slightly parted mid-word, the goat calm and still. {FULLBLEED}"),

    ("s05_confess", None, AARON_REF,
     "An extreme close-up insert: a pair of weathered old man's hands alone, "
     "pressing on coarse goat fur, one hand's knuckles whitened with "
     f"pressure, no face visible, morning light catching the hands only. {FULLBLEED}"),

    ("s06_scapegoat", "md_survey_plate", None,
     "A wide, high-angled view across a vast dry wilderness surface: a "
     "single small goat, a tiny distant mark against the scale of the land, "
     "walking alone away from the viewer into open desert scrubland, a "
     "faint trail of hoofprints receding behind it, the horizon distant and "
     "empty, pale heat-hazed sky. One single continuous illustrated ground "
     "surface only -- absolutely NOT an underground cutaway, NOT a cross-"
     "section showing soil layers or strata, NOT a scientific or geological "
     "diagram, no compass rose, no scale bar, no callout labels of any kind. "
     f"{FULLBLEED}"),

    ("s07_one_one", None, AARON_REF,
     f"{AARON} An eye-level composition: one goat lying still at the "
     "altar's base in the foreground, a second goat already small and "
     "departing across the yard in the distance behind, Aaron standing "
     f"between them, one hand extended toward each. {FULLBLEED}"),

    ("s08_why_two", None, AARON_REF,
     f"{AARON} A mid-shot: Aaron seated alone on a stone step inside a "
     "plain chamber, staring down at his own open hands resting in his lap, "
     f"lamp-lit, still, years etched in his face. {FULLBLEED}"),

    ("s09_turn", None, AARON_REF,
     f"{AARON} A low-angle shot: Aaron standing, his head lifting upward, "
     "his face catching new light from an unseen source above, both hands "
     f"slowly opening at his sides, a dawning understanding on his face. {FULLBLEED}"),

    ("s10_jesus_intro", None, JESUS_REF,
     f"{JESUS} An eye-level mid-shot: Jesus walking forward along a dusty "
     "road at dawn, His expression calm and certain, morning light behind "
     f"Him, no other figures present. {FULLBLEED}"),

    ("s11_price_guilt", None, JESUS_REF,
     f"{JESUS} A close mid-shot: Jesus standing still, His arms lowered at "
     "His sides, palms faintly turned outward, His face calm but bearing a "
     f"quiet weight, soft overcast light. {FULLBLEED}"),

    ("s12_scripture", "md_scroll", None,
     "A close view of a single ancient scroll fragment, partially unrolled "
     "across a plain wooden reading surface. The visible papyrus surface is "
     "OVERWHELMINGLY BARE aged parchment texture with visible fiber grain "
     "and age-staining -- NOT covered in writing, NOT rows of script, NOT "
     "columns of text, NOT dense handwriting, NOT cursive lines filling the "
     "page. At most 3-4 isolated, sparse, disconnected ink marks or dashes "
     "near one edge, small and incidental, never forming continuous lines "
     "or a readable pattern. A single thin shaft of light falling across "
     "the mostly-blank parchment, reverent stillness, no figure present, "
     f"the scroll's own aged surface as the subject. {FULLBLEED}"),

    ("s13_sat_down", None, JESUS_REF,
     f"{JESUS} A calm eye-level mid-shot: Jesus seated on a plain stone "
     "seat, hands resting open on His knees, His expression settled and at "
     f"rest, soft warm light. {FULLBLEED}"),

    ("s14_tore", None, None,
     "A high overhead-angled view of a heavy woven temple curtain, shown "
     "taut, a fine hairline tear just beginning at its top edge, dim "
     f"sanctuary light around it, fine dust drifting in the air. {FULLBLEED}"),

    ("s15_sign_substance", None, AARON_REF,
     f"{AARON} A mid-shot: Aaron standing with one open hand gesturing "
     "toward something unseen beyond the frame, his face open and "
     f"unguarded, plain sanctuary interior. {FULLBLEED}"),

    ("s16_torn_top_bottom", None, None,
     "A low-angle view of a heavy woven temple curtain now torn fully from "
     "top to bottom, the two torn halves hanging apart, warm light pouring "
     f"through the gap between them, fine dust drifting in the light shaft. {FULLBLEED}"),

    ("s17_landing", None, JESUS_REF,
     f"{JESUS} THE LANDING: a torn hole in the paper itself where the "
     "curtain's gap sits, warm gold light rising from beneath the page "
     "through the tear, Jesus standing just within the light, arms open in "
     f"welcome, low-angle, sacred stillness. {FULLBLEED}"),
]

_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)


def run(prompt: str, out: Path, ref: Path | None) -> bool:
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    if ref is not None:
        cmd += ["--image", str(ref)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


if __name__ == "__main__":
    only = None
    if "--only" in sys.argv[1:]:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))

    for slug, medium_id, ref, scene in JOBS:
        if only and slug not in only:
            continue
        out = STILLS / f"{slug}.png"
        if out.exists():
            print(f"[skip] {slug}.png")
            continue
        prompt = assemble_prompt(medium_id, scene)
        print(f"[{MODEL}] {slug} (medium={medium_id or 'home'}) ...", flush=True)
        ok = run(prompt, out, ref)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, ref)
        if ok:
            try:
                cost.record_hf(EPISODE, "still", "render", MODEL, note=slug)
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print(f"   -> {out.name} ({out.stat().st_size:,} bytes)")
        else:
            print("   FAILED")
