"""Jericho (/living-sketchbook full build) — step 1: RAHAB cast anchor.

  .venv\\Scripts\\python.exe poc_living_sketchbook/jericho/_j1_anchor.py
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
EPISODE = "LS_Jericho"

RAHAB_CANON = (
    "Rahab: a Canaanite woman of Jericho in her mid-thirties -- a strong, "
    "handsome, weathered face with dark watchful eyes and dark brows; long "
    "dark hair in a loose braid under a simple cloth head wrap; layered "
    "earth-toned Canaanite wool dress with a deep scarlet sash at the "
    "waist; a coil of scarlet cord held in her capable work-worn hands."
)

(CAST / "RAHAB.md").write_text(f"""# RAHAB — cast canon sheet (sketch-style family)

Created 2026-07-28 for the Jericho /living-sketchbook build.
KJV constraints: dwelt upon the town wall (Josh 2:15); received the spies in
peace (Heb 11:31); the scarlet line in the window (Josh 2:18); in the family
line of Jesus as "Rachab" (Matt 1:5). Everything else is deliberate invention
for consistency, period-honest. Anchor: `cast/rahab_sketch_ref.png` — a
regenerated portrait is a DIFFERENT face, never lose the anchor.

## Canon description (paste VERBATIM into every prompt that shows Rahab)

> {RAHAB_CANON}

## Usage
Chain the anchor via --image + append: "the SAME woman as the reference
image -- identical face, hair, and clothing."
""", encoding="utf-8")
print("[sheet] RAHAB.md")

out = CAST / "rahab_sketch_ref.png"
if not out.exists():
    prompt = (E.STYLE + "\n\nSCENE: " + RAHAB_CANON +
              " Close editorial portrait, head and shoulders, three-quarter "
              "view, quiet watchful resolve in the face, warm lamp light from "
              "one side, plain aged-paper backdrop.")
    print("[anchor] rahab_sketch_ref ...", flush=True)
    ok = E.run(prompt, out)
    if not ok:
        ok = E.run(prompt, out)
    if ok:
        cost.record_hf(EPISODE, "short", "cast_anchor", E.MODEL, note="[jericho] rahab anchor")
        print("   ok")
    else:
        raise SystemExit("FAILED")
else:
    print("[skip] anchor exists")
