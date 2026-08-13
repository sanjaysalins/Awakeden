"""The First Gospel in the Curse -- $0 Ken Burns pushes for the 3 spreads
that ended up here after real scrutiny, not just caution:
  s01 (hook hands) -- 2 Seedance attempts came back static; a 3rd on Kling
    ("tighten the grip") did produce motion, but also invented a visible
    double-band wrap around both wrists that wasn't in the source still --
    a real INVENT NOTHING violation, reverted.
  s05 (heel/head insert) -- a Seedance attempt asked to stir the
    surrounding grass instead rotated the whole foot to a different pose/
    angle mid-clip -- also reverted.
  s08b (open hands) -- deliberate: stillness/release IS the point, the
    contrast with s01's earlier tense grip. Motion here would undercut it.

Every other spread this episode is real generated motion (see
_s2_animate.py) -- these 3 are the disciplined $0 calls, not the default.

panel_animator/dynamic_cam3d.py hard-codes 16:9; patches OUT_W/OUT_H to
9:16 before calling render_move, same pattern as every other Ken Burns
fallback this project has used.

  .venv\\Scripts\\python.exe poc_living_sketchbook/first_gospel_in_the_curse/_kenburns.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
import dynamic_cam3d as DC  # noqa: E402

DC.OUT_W, DC.OUT_H = 1080, 1920

HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
CLIPS = HERE / "clips"
CLIPS.mkdir(exist_ok=True)

# (name, move, duration, focus)
JOBS = [
    ("s01_hook_hands", "push", 4.0, (0.50, 0.42)),
    ("s05_heel_and_head_insert", "push", 4.0, (0.50, 0.55)),
    ("s08b_open_hands", "push", 4.0, (0.50, 0.50)),
]


def main():
    for name, move, dur, focus in JOBS:
        still = STILLS / f"{name}.png"
        dest = CLIPS / f"{name}.mp4"
        if dest.exists():
            print(f"[skip] {name}")
            continue
        if not still.exists():
            print(f"[HOLD] {name}: missing still")
            continue
        out = DC.render_move(still, move, duration=dur, focus=focus, dest=dest)
        print(f"[ok] {name} -> {out}")


if __name__ == "__main__":
    main()
