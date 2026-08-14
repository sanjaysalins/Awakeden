"""Her Seed -- $0 devices for the 3 spreads that genuinely don't need
generated motion, decided BEFORE rendering (see _PLAN.md's own tiering
rationale, not a paid-then-reverted fallback):
  s02 -- light arriving on a still figure needs no invented motion -> $0
    dynamic_cam3d push toward Eve's face.
  s03 -- an old page already filled with ink, nothing left to animate ->
    $0 line_boil hold (held frame + grain wobble), the SAME device
    seed_of_the_woman's own build_s27 used for its line-of-fathers art.
  s05 -- the descent-line device is already drawn INTO the still's own
    art, same reasoning -> $0 line_boil hold.

panel_animator/dynamic_cam3d.py hard-codes 16:9; patches OUT_W/OUT_H to
9:16 before calling render_move, same pattern as every other Ken Burns
fallback this project has used.

  .venv\\Scripts\\python.exe poc_living_sketchbook/her_seed/_kenburns.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
import dynamic_cam3d as DC  # noqa: E402
import line_boil  # noqa: E402

DC.OUT_W, DC.OUT_H = 1080, 1920

HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
CLIPS = HERE / "clips"
CLIPS.mkdir(exist_ok=True)

W, H, FPS, DUR = 1080, 1920, 30, 4.0

# (name, move, duration, focus)
PUSH_JOBS = [
    ("s02_promise_spoken_over_eve", "push", DUR, (0.50, 0.40)),
]

LINE_BOIL_JOBS = [
    "s03_already_written_page",
    "s05_line_of_fathers_vertical",
]


def main():
    for name, move, dur, focus in PUSH_JOBS:
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

    for name in LINE_BOIL_JOBS:
        still = STILLS / f"{name}.png"
        dest = CLIPS / f"{name}.mp4"
        if dest.exists():
            print(f"[skip] {name}")
            continue
        if not still.exists():
            print(f"[HOLD] {name}: missing still")
            continue
        held = dest.parent / (dest.stem + "_held.mp4")
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(still), "-t", f"{DUR:.3f}",
             "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
             "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(held)],
            check=True)
        line_boil.render(held, dest, 0.5)
        held.unlink(missing_ok=True)
        print(f"[ok] {name} -> {dest}")


if __name__ == "__main__":
    main()
