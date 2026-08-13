"""The First Gospel in the Curse -- $0 Ken Burns pushes for the 4 spreads
whose intended effect IS a camera move, not generated life: s02 (dread
closing in), s04 (quiet attention on the serpent, and this project's own
serpent object has a real history of invented head/tongue motion on paid
renders -- a push is also the SAFE choice here), s05 (an ominous detail,
camera language is enough), s08b (stillness/release is the point, the
deliberate contrast with s01's trembling hands -- motion would undercut
it). Per the locked spend-only-for-cinematic-value principle: don't pay
for a shot that would only ever read as a push anyway.

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
    # s01 moved here after 2 straight Seedance fails: asked for a small,
    # visible finger tremor (the whole point of the shot -- fear made
    # physical), got a completely static hold both times, even with much
    # stronger language on the 2nd attempt. A push at least gives real
    # cinematic motion instead of paying twice for a static result.
    ("s01_hook_hands", "push", 4.0, (0.50, 0.42)),
    ("s02_waiting_in_trees", "push", 4.0, (0.50, 0.38)),
    ("s04_serpent_in_light", "push", 4.0, (0.50, 0.50)),
    ("s05_heel_and_head_insert", "push", 4.0, (0.50, 0.55)),
    ("s08b_open_hands", "push", 4.0, (0.50, 0.50)),
    # s09 moved here after 2 straight veo fails: both attempts invented a
    # full raised-hood cobra out of a small pale sketch-outline serpent in
    # the still, even with the 2nd attempt explicitly locking that exact
    # element by name. A push toward Christ still carries the "reveal"
    # feeling without the invented-content risk.
    ("s09_landing_transition", "push", 4.0, (0.50, 0.42)),
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
