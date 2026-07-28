"""cast-bible look POC — step 3: the ONE paid motion clip (Seedance 4s):
rain falls over the s2 still, everything else frozen, camera locked.

  .venv\\Scripts\\python.exe poc_castbible_look/_03_rain_clip.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
HERE = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location(
    "_anim", ROOT / "poc_comic_page" / "_animate_piece1_v2.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)

A.EPISODE = "POC_CastBible_Look"
STILL = HERE / "stills" / "s2_rain.png"
OUTDIR = HERE / "clips"
OUTDIR.mkdir(exist_ok=True)

PROMPT = (
    "The camera does not move, zoom, or change angle at all. Only the rain "
    "moves: long graphite rain streaks fall steadily down the whole frame, and "
    "the dark ink-wash storm sky breathes very subtly. The figure, his clothing, "
    "the wooden hull, the paper texture, the torn paper edges, and every sketch "
    "line hold perfectly still, pixel-identical throughout. INVENT NOTHING new. "
    "Nothing else in the frame changes."
)


def main():
    out = OUTDIR / "s2_rain.mp4"
    A.OUT = OUTDIR  # redirect the borrowed runner's output dir
    ok = A.run_job("s2_rain", "seedance", STILL, "16:9", PROMPT, duration=4)
    if not ok:
        print("retrying once ...")
        ok = A.run_job("s2_rain", "seedance", STILL, "16:9", PROMPT, duration=4)
    if not ok:
        raise SystemExit("FAILED")
    print(f"[ok] {out}")


if __name__ == "__main__":
    main()
