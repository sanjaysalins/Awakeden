"""Two Goats — patch: re-animate g10_finished from the identity-corrected
still (a still re-roll invalidates its clip -- re-animate in the same pass).

  .venv\\Scripts\\python.exe poc_living_sketchbook/two_goats/_g3b_fix_g10_clip.py
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
A.EPISODE = "LS_TwoGoats"
A.OUT = HERE / "clips"

STILL = HERE / "stills" / "g10_finished.png"
NOGLITTER = ("the light stays a steady, even glow -- it does not sparkle, "
             "flicker into particles, or scatter into glitter. ")
PROMPT = (
    "The camera does not move, zoom, or change angle at all. INVENT "
    "NOTHING new. The figure holds his exact seated resting pose, "
    "perfectly still -- no movement, no shifting. Only: the radiant "
    "doorway light behind him pulses softly and evenly, " + NOGLITTER +
    "faint dust drifts in the light. Nothing else changes."
)


def main():
    out = A.OUT / "g10_finished.mp4"
    ok = A.run_job("g10_finished", "seedance", STILL, "9:16", PROMPT, duration=8)
    if not ok:
        ok = A.run_job("g10_finished", "seedance", STILL, "9:16", PROMPT, duration=8)
    if not ok:
        raise SystemExit("FAILED")
    print(f"[ok] {out}")


if __name__ == "__main__":
    main()
