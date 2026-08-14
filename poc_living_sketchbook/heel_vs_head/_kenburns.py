"""Heel vs Head -- $0 devices for the 3 spreads that genuinely don't need
generated motion, decided per the standing rule (CLAUDE.md's "creative
device default over line_boil/Ken Burns"): each of these 3 has a real
camera-movement rationale, not a default fallback.
  s01 -- STATIC HOLD (revised from a push): the wide two-figure standoff
    kept losing one figure to the crop even at reduced amplitude -- the
    push mechanism doesn't suit this composition's full horizontal
    extent, and the standoff already reads fine held still.
  s02 -- a push toward the cracked stone draws the eye from the calm
    footprint to the real point of the shot (the crack).
  s05 -- the whole point is stillness/aftermath; ANY invented motion
    risks reading as the serpent still being alive (the exact defect
    this shot took 6 rounds to fix) -- a slow respectful push is the
    safest and most tonally correct choice, not a lazy default.

panel_animator/dynamic_cam3d.py hard-codes 16:9; patches OUT_W/OUT_H to
9:16 before calling render_move, same pattern as every other Ken Burns
fallback this project has used.

  .venv\\Scripts\\python.exe poc_living_sketchbook/heel_vs_head/_kenburns.py
"""
import subprocess
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

W, H, FPS, DUR = 1080, 1920, 30, 4.0

# (name, move, duration, focus) -- move=None means a plain static hold, no
# camera motion at all. s01's wide two-figure standoff kept losing one
# figure to the crop even at reduced push amplitude (0.35) -- the push
# mechanism doesn't suit this composition's full horizontal extent, and
# the composition (torn paper, the standoff itself) already reads fine
# held still, so a static hold is the safer, correct call here, not a
# lazy default (see CLAUDE.md's creative-device-over-Ken-Burns rule).
JOBS = [
    ("s01_duel_motif", None, 4.0, None),
    ("s02_bruise_vs_crush_split", "push", 4.0, (0.55, 0.50)),
    ("s05_heel_and_head_insert", "push", 4.0, (0.45, 0.55)),
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
        if move is None:
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(still), "-t", f"{dur:.3f}",
                 "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                 "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)],
                check=True)
            print(f"[ok] {name} -> {dest} (static hold)")
            continue
        out = DC.render_move(still, move, duration=dur, focus=focus, dest=dest)
        print(f"[ok] {name} -> {out}")


if __name__ == "__main__":
    main()
