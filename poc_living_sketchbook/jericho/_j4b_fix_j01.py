"""Jericho — patch: j01_walls hit NSFW-REJECTED twice on Seedance (still is
clean; false-positive on the crowd-scene motion prompt). Re-tier to Kling
per the locked action/crowd rule (this shot has a marching crowd).

  .venv\\Scripts\\python.exe poc_living_sketchbook/jericho/_j4b_fix_j01.py
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

STILL = HERE / "stills" / "j01_walls.png"
PROMPT = (
    "The camera does not move, zoom, or change angle at all. INVENT NOTHING "
    "new -- no new figures, objects, or marks appear; the paper texture, "
    "torn edges, and every sketch line hold perfectly still, the walls and "
    "sky frozen. All marching figures hold their exact silhouette poses -- "
    "no new steps, no limb movement. Only: the whole distant column drifts "
    "very slowly forward along its path as one group, faint dust hangs "
    "above them, the dawn light breathes gently. Nothing else changes."
)


def main():
    out = A.OUT / "j01_walls.mp4"
    ok = A.run_job("j01_walls", "kling", STILL, "9:16", PROMPT, duration=5)
    if not ok:
        ok = A.run_job("j01_walls", "kling", STILL, "9:16", PROMPT, duration=5)
    if not ok:
        raise SystemExit("FAILED")
    print(f"[ok] {out}")


if __name__ == "__main__":
    main()
