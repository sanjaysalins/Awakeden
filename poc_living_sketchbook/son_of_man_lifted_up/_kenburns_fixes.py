"""Even So Must the Son of Man Be Lifted Up -- $0 Ken Burns fallback for 3
clips that kept inventing motion/blood despite locked prompts:
  s04_ot_echo / s06_serpent_healed_gaze -- the bronze serpent's head raised
    and its mouth opened/tongue extended, the SAME failure mode Look and
    Live's own s08 hit twice this session on the same chained object.
  s09_nailed_hand_insert -- the fingers curled and blood gushed down the
    spike, despite "hold perfectly still, no blood" -- the same wound this
    episode's own STILL needed 5 rounds to get clean of blood in the first
    place.
User's call (after seeing the pattern repeat on demonstrated failures):
$0 dynamic_cam3d push for all 3 rather than more paid AI attempts.

panel_animator/dynamic_cam3d.py hard-codes 16:9 (1920x1080); this project's
shorts are 9:16 -- patches OUT_W/OUT_H before calling render_move, same
approach as look_and_live/_s08_kenburns.py.

  .venv\\Scripts\\python.exe poc_living_sketchbook/son_of_man_lifted_up/_kenburns_fixes.py
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

# (name, move, duration, focus)
JOBS = [
    ("s04_ot_echo", "push", 4.0, (0.5, 0.40)),
    ("s06_serpent_healed_gaze", "push", 4.0, (0.5, 0.45)),
    ("s09_nailed_hand_insert", "push", 4.0, (0.5, 0.50)),
]


def main():
    for name, move, dur, focus in JOBS:
        still = STILLS / f"{name}.png"
        dest = CLIPS / f"{name}.mp4"
        if not still.exists():
            print(f"[HOLD] {name}: missing still")
            continue
        out = DC.render_move(still, move, duration=dur, focus=focus, dest=dest)
        print(f"[ok] {name} -> {out}")


if __name__ == "__main__":
    main()
