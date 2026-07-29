"""living-sketchbook — proper cast-bible world-bible build (repo-level).

Promotes the ad-hoc single-roll Door-episode Jesus anchor into a real
/cast-bible reference: full canon fields (face geometry, hair/beard shape,
skin, build, hands, signature garment), close-crop framing that USES the
page (not a small vignette on mostly blank paper), saved at
poc_living_sketchbook/cast/ for series-wide reuse (per SKILL.md sec.2's own
"promote to a repo-level cast/" item).

Also builds a DISCIPLES group reference (3 distinct mixed-age fishermen,
per feedback-peopled-stills-need-character-ref.md -- background/crowd faces
must not be left ref:null or they invent a new cast every scene) and a BOAT
world reference (episode-specific prop lock, per
feedback-episode-world-consistency.md's "World Bible" discipline).

  .venv\\Scripts\\python.exe poc_living_sketchbook/_r1_worldbible.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline import cost

spec = importlib.util.spec_from_file_location(
    "_e1", ROOT / "poc_castbible_look" / "episode_door" / "_e1_anchors.py")
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)

CAST = Path(__file__).resolve().parent / "cast"
CAST.mkdir(parents=True, exist_ok=True)
WORLD = Path(__file__).resolve().parent / "storm" / "world"
WORLD.mkdir(parents=True, exist_ok=True)
EPISODE = "LS_WorldBible"

JESUS_CANON = (
    "Jesus: a Judean man in his early thirties. Face geometry: a strong "
    "straight nose, defined cheekbones, a broad calm forehead, an angular "
    "jaw beneath the beard. Hair: long dark wavy hair falling past the "
    "shoulders, parted center. Beard: short, close-cropped, dark, "
    "well-kept. Skin: sun-weathered olive Mediterranean complexion. Build: "
    "lean and wiry-strong, a carpenter's and traveler's frame. Eyes: warm "
    "deep brown, level and calm, looking in the same direction, never wide "
    "or staring. Hands: strong, calloused, a craftsman's hands. Garment: "
    "simple undyed homespun ankle-length tunic with a woven cord sash, "
    "leather sandals -- the same every appearance."
)
DISCIPLES_CANON = (
    "Three Galilean fishermen of mixed ages and builds, standing together: "
    "(left) an older weathered man in his fifties, grey-streaked dark "
    "beard, deep sun-creased face; (center) a robust bearded man in his "
    "thirties, dark curly hair, broad shoulders; (right) a lean younger "
    "man in his twenties, short dark beard, alert watchful eyes. All "
    "sun-weathered skin, rope-callused hands, plain undyed short-sleeved "
    "fishermen's tunics hitched and belted for boat work, bare feet."
)
BOAT_CANON = (
    "A first-century Galilean fishing boat, based on the Sea of Galilee "
    "boat: a plank-built open hull about eight meters long, shallow draft, "
    "a single mast set slightly forward of center carrying one small "
    "furled square sail with simple rope rigging, three oar positions "
    "along each side with wooden oars shipped inside the hull, a flat "
    "raised stern for steering, weathered undecorated wood throughout -- "
    "no carvings, no modern fittings."
)

ANCHORS = [
    ("jesus_ref", JESUS_CANON,
     "Editorial portrait, head to mid-chest, three-quarter view, calm open "
     "expression, warm light from one side -- the figure fills nearly the "
     "whole frame, minimal surrounding blank paper.", "1:1"),
    ("disciples_ref", DISCIPLES_CANON,
     "Group editorial portrait, head to waist on all three figures, facing "
     "camera at slightly different angles, harsh midday light -- the three "
     "figures fill nearly the whole frame edge to edge, minimal surrounding "
     "blank paper.", "1:1"),
    ("boat_ref", BOAT_CANON,
     "A clean reference plate: the boat alone, empty, resting on calm "
     "water, three-quarter side view showing the mast/rigging/hull clearly "
     "-- the boat fills nearly the whole frame edge to edge, minimal "
     "surrounding blank paper, plain flat water and sky, no figures.",
     "4:3"),
]


def run(prompt, out, ar):
    import re
    import subprocess
    cmd = [E.HF, "generate", "create", E.MODEL, "--prompt", prompt,
           "--aspect_ratio", ar, "--resolution", "2k", "--wait"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    (CAST / "JESUS.md").write_text(f"""# JESUS — cast canon sheet (sketch-style family, repo-level)

Built 2026-07-29 with full /cast-bible rigor (promoted from the
single-roll Door-episode anchor per SKILL.md sec.2's own "promote to a
repo-level cast/" item). Anchor: `cast/jesus_ref.png` -- a regenerated
portrait is a DIFFERENT face, never lose the anchor. Fail-closed eye-QC on
every Jesus frame.

## Canon description (paste VERBATIM into every prompt that shows Jesus)

> {JESUS_CANON}

## Usage
Chain the anchor via --image + append: "the SAME man as the reference image
-- identical face, beard, hair, and clothing." For an episode where Jesus
appears in >1 dramatically different pose, chain the first APPROVED
in-episode render as a SECOND reference alongside this anchor for every
later appearance (multi-pose identity lock, SKILL.md sec.2).
""", encoding="utf-8")
    (CAST / "DISCIPLES.md").write_text(f"""# DISCIPLES — group cast canon sheet (sketch-style family, repo-level)

Group reference for background/crowd fishermen so they don't invent a new
cast every scene (feedback-peopled-stills-need-character-ref.md). Anchor:
`cast/disciples_ref.png`.

## Canon description (paste VERBATIM into every prompt showing background disciples)

> {DISCIPLES_CANON}

## Usage
Chain the anchor via --image for any scene with unnamed disciples/fishermen
in the background. The named viewer-surrogate figure (e.g. episode
FISHERMAN) is separate and gets its own anchor.
""", encoding="utf-8")
    (WORLD / "BOAT.md").write_text(f"""# BOAT — world/setting reference (Storm episode)

Locks the boat's design across every scene (feedback-episode-world-
consistency.md World Bible discipline) -- previously each still invented
its own rigging (mast present in some shots, absent in others). Anchor:
`storm/world/boat_ref.png`.

## Canon description (paste VERBATIM into every prompt showing the boat)

> {BOAT_CANON}

## Usage
Chain the anchor via --image for every boat scene in this episode.
""", encoding="utf-8")
    print("[sheets] JESUS.md, DISCIPLES.md, BOAT.md written")

    for name, canon, framing, ar in ANCHORS:
        out = (CAST if name != "boat_ref" else WORLD) / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        prompt = E.STYLE + "\n\nSCENE: " + canon + " " + framing
        print(f"[ref] {name} ...", flush=True)
        ok = run(prompt, out, ar)
        if not ok:
            ok = run(prompt, out, ar)
        if ok:
            cost.record_hf(EPISODE, "short", "cast_anchor", E.MODEL, note=f"[worldbible] {name}")
            print("   ok")
        else:
            print("   FAILED")


if __name__ == "__main__":
    main()
