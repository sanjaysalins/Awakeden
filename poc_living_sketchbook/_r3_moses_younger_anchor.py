"""living-sketchbook -- Moses YOUNGER repo-level cast anchor (Bronze Serpent
LONG pilot).

Extends the repo-level cast-bible system alongside `_r2_moses_anchor.py`
(elder MOSES, Numbers 21 era) with a SECOND, younger Moses anchor needed
because `bronze_serpent_long/_PLAN.md` section 4 item 4 flags spread 37 (the
golden-calf flashback, Exodus 32) as ~40 years BEFORE the elderly Numbers-21
Moses that `cast/MOSES.md` is explicitly locked to. `cast/MOSES.md` says in
its own words: "NOT the young Moses of the Exodus/burning-bush years" -- so
the golden-calf incident needs its own age-lock, not a reuse of the elder
anchor.

Canon note: this is Moses in his mid-to-late 30s, at the time of the golden
calf (Exodus 32) -- NOT the elderly eighty-year-old Numbers-21 Moses in
`cast/MOSES.md`. Face geometry deliberately shares the elder canon's
broad-forehead / strong-jaw / dark-steady-eyes description (same man, same
family resemblance) while every age marker (hair, beard, skin, build)
differs.

Rendered WITHOUT chaining `cast/moses_ref.png` as a reference image -- pure
text-description, on purpose. Chaining the ELDER reference risks the model
anchoring on the old-age face/grey hair despite the "younger" wording (a
known failure mode elsewhere in this project when an age-instruction fights
a reference image); the family resemblance is carried by describing the
SAME facial geometry in words instead. If the rendered result does not
plausibly read as a younger version of the same man, that is flagged
honestly in the task report rather than silently accepted.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_r3_moses_younger_anchor.py
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
EPISODE = "LS_BronzeSerpentLong"

MOSES_YOUNGER_CANON = (
    "Moses: a Hebrew man in his mid-to-late thirties, at the time of the "
    "golden calf at Sinai (Exodus 32) -- roughly forty years before the "
    "aged lawgiver of Numbers 21, NOT that elderly figure. Face geometry "
    "shares clear family resemblance with his elder self: the same broad "
    "forehead, the same strong jaw beneath the beard, the same dark, "
    "steady eyes -- but weighted now with the anger and grief of a younger "
    "man, not an old man's authority. Hair: full, dark brown-black hair, "
    "no grey. Beard: a shorter, fuller dark beard -- not yet long, not yet "
    "touched with white. Skin: unweathered and largely unlined, smooth at "
    "the eyes and brow, only lightly sun-marked. Build: a physically "
    "robust, upright, broad-shouldered frame in the prime of life -- more "
    "muscular and vigorous than his elder self, never slight or frail. "
    "Hands: strong, capable hands, not yet an elder's veined hands. "
    "Garment: a plain undyed woolen robe with a coarse mantle draped over "
    "one shoulder, a woven cord girdle at the waist, plain leather sandals "
    "-- the same shepherd-prophet's dress as his elder self. Signature "
    "prop: the same tall wooden staff, worn smooth with use, carried at "
    "his side or in hand -- the identical prop across both ages, the "
    "continuity device."
)

ANCHORS = [
    ("moses_younger_ref", MOSES_YOUNGER_CANON,
     "Editorial portrait, head to mid-chest, three-quarter view, calm "
     "resolute expression, warm light from one side -- the figure fills "
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
    (CAST / "MOSES_YOUNGER.md").write_text(f"""# MOSES_YOUNGER -- cast canon sheet (sketch-style family, repo-level)

Built 2026-08-01 for the Bronze Serpent LONG pilot (`bronze_serpent_long/
_PLAN.md` section 4 item 4), spread 37 -- the golden-calf flashback
(Exodus 32), which happens ~40 years BEFORE the Numbers-21 events the
existing `cast/MOSES.md` / `cast/moses_ref.png` anchor is locked to.
Anchor: `cast/moses_younger_ref.png` -- a regenerated portrait is a
DIFFERENT face, never lose the anchor.

**This is Moses in his mid-to-late 30s, at the time of the golden calf**
(Exodus 32) -- dark hair, a shorter fuller dark beard, unweathered skin, a
more physically robust/upright build. **NOT** the elderly eighty-year-old
Numbers-21 Moses in `cast/MOSES.md` / `cast/moses_ref.png` -- do not
substitute one anchor for the other.

Rendered WITHOUT chaining the elder `moses_ref.png` as a reference --
pure text-description, deliberately, to avoid the age-instruction-vs-
reference-image failure mode. Family resemblance to the elder canon is
carried by matching facial GEOMETRY in words (same broad forehead, same
jaw structure, same dark steady eyes), not by image chaining.

## Canon description (paste VERBATIM into every prompt that shows younger Moses)

> {MOSES_YOUNGER_CANON}

## Usage
Chain the anchor via --image + append: "the SAME man as the reference image
-- identical face, beard, hair, and clothing." Do NOT mix this anchor with
`cast/moses_ref.png` in the same render -- they are two different ages of
the same man and chaining both risks a blended, ambiguous face.
""", encoding="utf-8")
    print("[sheet] MOSES_YOUNGER.md written")

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
            cost.record_hf(EPISODE, "long", "cast_anchor", E.MODEL, note=f"[bronzeserpentlong] {name}")
            print("   ok")
        else:
            print("   FAILED")


if __name__ == "__main__":
    main()
