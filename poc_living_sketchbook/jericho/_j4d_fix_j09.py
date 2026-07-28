"""Jericho — patch round 2: j09_stage_b failed TWICE on Seedance (r1 pooled
the cord into a blood-like puddle; r2's hardened "never drips/pools" prompt
made it WORSE -- two windows now bleed, exactly the failure named to forbid
it drew it in, per this project's own locked positive-only-wording rule).
Per the stuck-shot rule (2 real content failures = switch model), moving to
Kling with PURE POSITIVE wording -- the cord is never described near
liquid verbs at all, only "a thin steady red line, unmoving."

  .venv\\Scripts\\python.exe poc_living_sketchbook/jericho/_j4d_fix_j09.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
HERE = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location(
    "_anim", ROOT / "poc_comic_page" / "_animate_piece1_v2.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
A.EPISODE = "LS_Jericho"
A.OUT = HERE / "clips"

STILL = HERE / "stills" / "j09_stage_b.png"
PROMPT = (
    "This is a single frozen photograph -- a tableau of stone frozen at one "
    "instant, like a museum diorama. The camera does not move, zoom, or "
    "change angle at all. Every stone slab, every crack, and the thin "
    "scarlet cord hanging from the window all hold their exact drawn shapes "
    "and positions perfectly, unmoving, for the entire clip -- a still-life "
    "painting come only barely to life. INVENT NOTHING new -- no new "
    "figures, objects, or marks. Only ONE thing in this frame has any "
    "motion at all: soft grey dust drifting gently in the open air well "
    "away from the wall and away from the cord. Everything else, every "
    "line on the page, is exactly as still as a photograph."
)


def main():
    out = A.OUT / "j09_stage_b.mp4"
    ok = A.run_job("j09_stage_b", "kling", STILL, "9:16", PROMPT, duration=5)
    if not ok:
        ok = A.run_job("j09_stage_b", "kling", STILL, "9:16", PROMPT, duration=5)
    if not ok:
        raise SystemExit("FAILED")
    print(f"[ok] {out}")


if __name__ == "__main__":
    main()
