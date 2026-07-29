"""Storm episode — step 1: FISHERMAN cast anchor (sketch-style family). Jesus
reuses the Door episode's existing anchor ($0, same style family, no new
render) — chained alongside the S04 asleep still once that's approved
(SKILL.md §2 multi-pose identity lock).

  .venv\\Scripts\\python.exe poc_living_sketchbook/storm/_s1_anchor.py
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
EPISODE = "LS_Storm"

# Galilean fishermen (Peter/Andrew/James/John's trade) worked their own boats
# for a living -- practical dress for wet, physical work, not formal wear.
# No names given in this pericope (Matt 8:23-27 / Mark 4:35-41), so an
# anonymous every-fisherman fits the format's own convention (viewer
# surrogate, same pattern as episode_door's SEEKER).
FISHERMAN_CANON = (
    "The Fisherman: a sun-weathered Galilean man in his forties -- "
    "short-cropped dark hair (NOT long or wavy, unlike Jesus), a thick "
    "rough dark beard, a hard deeply-lined weathered face, a broader "
    "stockier build than Jesus, rope-callused hands; a single plain "
    "undyed knee-length tunic hitched up and belted for boat work -- ONE "
    "continuous garment ending above the knee, never separate trouser "
    "legs; bare feet, no sandals."
)

(CAST / "FISHERMAN.md").write_text(f"""# FISHERMAN (the Witness) — cast canon sheet (sketch-style family)

Created 2026-07-29 for the Storm /living-sketchbook build. Matthew 8:23-27 /
Mark 4:35-41 name no disciple individually in this pericope -- anonymous
every-fisherman, the viewer's surrogate in the boat (same convention as
episode_door's SEEKER). Anchor: `cast/fisherman_sketch_ref.png` — a
regenerated portrait is a DIFFERENT face, never lose the anchor.

## Canon description (paste VERBATIM into every prompt that shows the Fisherman)

> {FISHERMAN_CANON}

## Usage
Chain the anchor via --image + append: "the SAME man as the reference image
-- identical face, hair, and clothing."

## Jesus in this episode
Reuses the EXISTING sketch-family anchor from the Door episode
(`poc_castbible_look/episode_door/cast/jesus_sketch_ref.png` / `JESUS.md`) —
same style family, $0, no new render. Appears in more poses than any prior
episode; per SKILL.md §2 multi-pose identity lock, the S04 (asleep) still is
rendered FIRST, eye-approved, then chained as a SECOND reference alongside
this anchor for every later Jesus still.
""", encoding="utf-8")
print("[sheet] FISHERMAN.md")

out = CAST / "fisherman_sketch_ref.png"
if not out.exists():
    prompt = (E.STYLE + "\n\nSCENE: " + FISHERMAN_CANON +
              " Close editorial portrait, head and shoulders, three-quarter "
              "view, wary alert eyes scanning open water, harsh midday sun "
              "from one side, plain aged-paper backdrop.")
    print("[anchor] fisherman_sketch_ref ...", flush=True)
    ok = E.run(prompt, out)
    if not ok:
        ok = E.run(prompt, out)
    if ok:
        cost.record_hf(EPISODE, "short", "cast_anchor", E.MODEL, note="[storm] fisherman anchor")
        print("   ok")
    else:
        raise SystemExit("FAILED")
else:
    print("[skip] anchor exists")
