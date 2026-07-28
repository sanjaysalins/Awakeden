"""Jericho — patch: j12_line hit NSFW-REJECTED twice on Seedance (still is
clean -- mother+child, harpist, carpenter family; classifier false-positive,
same class as j01). Re-tier to Kling.

  .venv\\Scripts\\python.exe poc_living_sketchbook/jericho/_j4c_fix_j12.py
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

STILL = HERE / "stills" / "j12_line.png"
PROMPT = (
    "The camera does not move, zoom, or change angle at all. INVENT NOTHING "
    "new -- no new figures, objects, or marks appear; every figure holds "
    "their exact pose, perfectly still, like statues; the paper texture and "
    "torn edges hold still. The scarlet thread holds its exact shape. Only: "
    "the warm gold glow at the right edge breathes very slowly and evenly, "
    "it does not sparkle or scatter into glitter. Nothing else changes."
)


def main():
    out = A.OUT / "j12_line.mp4"
    ok = A.run_job("j12_line", "kling", STILL, "9:16", PROMPT, duration=5)
    if not ok:
        ok = A.run_job("j12_line", "kling", STILL, "9:16", PROMPT, duration=5)
    if not ok:
        raise SystemExit("FAILED")
    print(f"[ok] {out}")


if __name__ == "__main__":
    main()
