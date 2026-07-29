"""v3: animate the hero landing still (Seedance calm hold) + extend to 6.8s
for the page5 full-bleed splash takeover.

  .venv\\Scripts\\python.exe poc_comic_page/_animate_v3_hero.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
HERE = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location("_anim_v2", HERE / "_animate_piece1_v2.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)

sys.path.insert(0, str(HERE / "rung1"))
import _extend_loop as EL  # noqa

STILL = HERE / "_piece1" / "stills_v2" / "p6_hero_landing.png"
PROMPT = (
    "The camera does not move, zoom, pull back, or change angle at all -- "
    "this exact low-angle framing holds for the entire clip. The figure "
    "stays perfectly frozen like a statue: his arms hold this exact "
    "position and never rise, spread, or move, no steps, no head turn, no "
    "hand movement, no clothing shift, no new figures or objects, the "
    "stone gateway's exact size and position never change. INVENT NOTHING "
    "new. The wide radiant gold seam along his edge stays a steady, "
    "unbroken, glowing line exactly where it already is -- it does not "
    "sparkle, flicker into particles, or scatter into glitter. Only these "
    "named things may move: the radiant morning-gold light flooding the "
    "stone gateway pulses softly and evenly like a steady flame, faint "
    "dust motes drift slowly through the light. Nothing else in the frame "
    "changes, the whole frame otherwise stays pixel-identical throughout."
)


def main():
    ok = A.run_job("p6_hero", "seedance", STILL, "9:16", PROMPT, duration=8)
    if not ok:
        print("retrying once ...")
        ok = A.run_job("p6_hero", "seedance", STILL, "9:16", PROMPT, duration=8)
    if not ok:
        raise SystemExit("FAILED")
    src = A.OUT / "p6_hero.mp4"
    out = HERE / "_piece1" / "clips_v2" / "extended" / "p6_hero.mp4"
    # 8s raw already covers the ~6.5s splash window -- no loop extension needed
    import shutil
    shutil.copy(src, out)
    print(f"[copy] {out} -> {EL.probe_duration(out):.2f}s")


if __name__ == "__main__":
    main()
