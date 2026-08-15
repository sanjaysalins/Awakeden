"""The Serpent-Crusher Promised -- $0 devices for the spreads that don't
need generated motion, per the standing rule (CLAUDE.md's "creative device
default over line_boil/Ken Burns"):
  s02 -- a push toward the suspended keystone/gap draws the eye to the
    real point of the shot (the arch waiting to be finished) -- same
    device as heel_vs_head's own s02 (push toward the crack).
  s04 -- 2026-08-15: swapped from paid Kling (per the user's own explicit
    call, after already re-verifying it showed a genuine pen-stroke
    gesture) to a plain push toward the pen tip on the parchment -- the
    hand/quill/ink detail carries the shot on its own, old clip kept as
    clips/s04_pauls_letter.kling.bak.mp4.
  s05 -- HERO/KJV-quote shot, aftermath stillness is the whole point.
    This exact serpent design took multiple rounds this session to read
    as genuinely dead, not alive -- ANY invented motion risks undoing
    that. A slow respectful push toward the feet is the safe, tonally
    correct choice, matching heel_vs_head's own s05 precedent for the
    identical risk.

  .venv\\Scripts\\python.exe poc_living_sketchbook/serpent_crusher_promised/_kenburns.py
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
    ("s02_unfinished_arch", "push", 4.0, (0.50, 0.35)),
    ("s04_pauls_letter", "push", 5.0, (0.48, 0.50)),
    ("s05_feet_on_crushed_head", "push", 4.0, (0.50, 0.60)),
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
