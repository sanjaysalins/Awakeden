"""living-sketchbook -- Moses repo-level cast anchor (Bronze Serpent episode).

Extends the same repo-level cast-bible system _r1_worldbible.py built for
Jesus/Disciples/Boat with a fourth anchor: MOSES, needed because Round 9's
Bronze Serpent (Numbers 21) beat plan shows Moses at narrative scale across
seven spreads (s01/s02/s05/s06/s07/s09) -- without a locked anchor he drifts
face-to-face across the episode, the same failure mode the cast-bible
discipline exists to prevent (see
poc_living_sketchbook/_FABLE_ROUND9_BRONZESERPENT_E2E_PLAN.md section A3 +
the honest-flags list at the end of section D).

Canon note: this is Moses ~40 years after the Exodus (Numbers 21 is near the
end of the wilderness wandering) -- elderly, NOT the young Moses of
Exodus/burning-bush imagery.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_r2_moses_anchor.py
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
EPISODE = "LS_BronzeSerpent"

MOSES_CANON = (
    "Moses: an elderly Hebrew man in his eighties, forty years into the "
    "wilderness wandering -- the aged lawgiver of Numbers, NOT the young "
    "Moses of the Exodus/burning-bush years. Face geometry: a broad "
    "weathered forehead, deep-set eyes beneath heavy grey brows, hollowed "
    "cheeks, a strong jaw beneath the beard. Hair: long white and grey "
    "hair swept back off the forehead, thinning at the crown. Beard: "
    "long, full, white streaked with iron-grey, a patriarch's beard "
    "reaching mid-chest. Skin: deeply sun-weathered, creased and leathery "
    "from decades in the wilderness sun. Build: an old man's spare, "
    "sinewed frame -- still upright and strong-shouldered, not frail, "
    "never youthful. Eyes: dark, steady, weighted with authority and "
    "grief. Hands: large, veined, weathered elder's hands. Garment: a "
    "plain undyed woolen robe with a coarse mantle draped over one "
    "shoulder, a woven cord girdle at the waist, plain leather sandals -- "
    "a shepherd-prophet's dress, nothing ornamented, nothing modern. "
    "Signature prop: a tall wooden staff, worn smooth by decades of use, "
    "always at his side or in hand -- the same every appearance."
)

ANCHORS = [
    ("moses_ref", MOSES_CANON,
     "Editorial portrait, head to mid-chest, three-quarter view, calm "
     "weathered expression, warm light from one side -- the figure fills "
     "nearly the whole frame, minimal surrounding blank paper.", "1:1"),
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
    (CAST / "MOSES.md").write_text(f"""# MOSES -- cast canon sheet (sketch-style family, repo-level)

Built 2026-07-31 for the Bronze Serpent episode (Numbers 21), following the
same repo-level /cast-bible pattern `_r1_worldbible.py` used for JESUS/
DISCIPLES/BOAT. Anchor: `cast/moses_ref.png` -- a regenerated portrait is a
DIFFERENT face, never lose the anchor.

**This is Moses ~40 years after the Exodus** (Numbers 21 is near the end of
the wilderness wandering) -- elderly, NOT the young Moses of the
Exodus/burning-bush years. Needed because the Bronze Serpent episode shows
Moses at narrative scale across seven spreads (s01/s02/s05/s06/s07/s09,
per `_FABLE_ROUND9_BRONZESERPENT_E2E_PLAN.md` section A3) -- without a
locked anchor he drifts face-to-face across the episode, the same failure
mode this cast discipline exists to prevent.

## Canon description (paste VERBATIM into every prompt that shows Moses)

> {MOSES_CANON}

## Usage
Chain the anchor via --image + append: "the SAME man as the reference image
-- identical face, beard, hair, and clothing." For an episode where Moses
appears in >1 dramatically different pose (Bronze Serpent's seven
narrative-scale spreads qualify), chain the first APPROVED in-episode
render as a SECOND reference alongside this anchor for every later
appearance (multi-pose identity lock, SKILL.md sec.2).
""", encoding="utf-8")
    print("[sheet] MOSES.md written")

    for name, canon, framing, ar in ANCHORS:
        out = CAST / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        prompt = E.STYLE + "\n\nSCENE: " + canon + " " + framing
        print(f"[ref] {name} ...", flush=True)
        ok = run(prompt, out, ar)
        if not ok:
            ok = run(prompt, out, ar)
        if ok:
            cost.record_hf(EPISODE, "short", "cast_anchor", E.MODEL, note=f"[bronzeserpent] {name}")
            print("   ok")
        else:
            print("   FAILED")


if __name__ == "__main__":
    main()
