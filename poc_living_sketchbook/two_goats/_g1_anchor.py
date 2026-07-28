"""Two Goats — step 1: PRIEST cast anchor (sketch-style family). Jesus reuses
the Door episode's existing anchor ($0, same style family, no new render).

  .venv\\Scripts\\python.exe poc_living_sketchbook/two_goats/_g1_anchor.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline import cost

spec = importlib.util.spec_from_file_location(
    "_e1", ROOT / "poc_castbible_look" / "episode_door" / "_e1_anchors.py")
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)

CAST = Path(__file__).resolve().parent / "cast"
CAST.mkdir(parents=True, exist_ok=True)
EPISODE = "LS_TwoGoats"

# Leviticus 16:4 -- on the Day of Atonement the high priest wears PLAIN LINEN,
# not his usual jeweled/golden vestments. Period-accuracy constraint, not an
# invention: "he shall put on the holy linen coat... linen breeches... girded
# with a linen girdle, and with the linen mitre shall he be attired: these
# are holy garments."
PRIEST_CANON = (
    "The Priest: an aging Hebrew man in his sixties -- deep-set solemn eyes, "
    "a long grey beard, a weathered careworn face marked by decades of duty; "
    "dressed ENTIRELY in plain undyed white linen for the Day of Atonement -- "
    "a plain linen coat, linen breeches, a linen girdle, a linen turban -- no "
    "gold, no jewels, no embroidered breastplate of any kind; bare feet."
)

(CAST / "PRIEST.md").write_text(f"""# PRIEST (the Witness) — cast canon sheet (sketch-style family)

Created 2026-07-28 for the Two Goats /living-sketchbook build. KJV constraint
(Leviticus 16:4): on the Day of Atonement the high priest wears PLAIN LINEN
only -- no gold, no jewels, no embroidered vestments (those are for other
duties, never this one). Anchor: `cast/priest_sketch_ref.png` — a
regenerated portrait is a DIFFERENT face, never lose the anchor.

## Canon description (paste VERBATIM into every prompt that shows the Priest)

> {PRIEST_CANON}

## Usage
Chain the anchor via --image + append: "the SAME man as the reference image
-- identical face, hair, and clothing."

## Jesus in this episode
Reuses the EXISTING sketch-family anchor from the Door episode
(`poc_castbible_look/episode_door/cast/jesus_sketch_ref.png` /
`JESUS.md`) — same style family, $0, no new render. Canon text unchanged.
""", encoding="utf-8")
print("[sheet] PRIEST.md")

out = CAST / "priest_sketch_ref.png"
if not out.exists():
    prompt = (E.STYLE + "\n\nSCENE: " + PRIEST_CANON +
              " Close editorial portrait, head and shoulders, three-quarter "
              "view, solemn weighted dread in the face, dim lamplight from "
              "one side, plain aged-paper backdrop.")
    print("[anchor] priest_sketch_ref ...", flush=True)
    ok = E.run(prompt, out)
    if not ok:
        ok = E.run(prompt, out)
    if ok:
        cost.record_hf(EPISODE, "short", "cast_anchor", E.MODEL, note="[two-goats] priest anchor")
        print("   ok")
    else:
        raise SystemExit("FAILED")
else:
    print("[skip] anchor exists")
