"""Bronze Serpent LONG -- step 4c: the 2 insert-page reading-order pans
(s43 Scholar's-Margin typology diagram, s67 Gilded Proclamation) -- the
last 2 of the 3 "$0 by design" spreads that never go to generative
animation (baked lettering never goes to a generative animator, per
`feedback-never-animate-writing`). Same InsertPageCamera engine as
`_s4b_fallback_clips.py`, at each spread's REAL _PLAN.md window duration
so assembly never needs to bounce these. (s68_landing is the 3rd $0-by-
design spread but gets NO pan of its own -- it's a static held frame
revealed by the tear_hole transition at assembly time.)

Framing notes (checked against the actual full-res stills):
  - s43 (13.6s): two-panel diagram, LEFT = Moses + bronze-serpent-on-pole
    (Numbers 21), RIGHT = Jesus teaching Nicodemus by lamplight (John 3).
    Reading-order pan: full view -> settle+hold on the Numbers panel ->
    glide+hold on the John panel -> pull back to full for the lift_away
    handoff into s44.
  - s67 (9.0s): dull bronze serpent on its stick (foreground) below
    Christ radiant, arms open, against the gold-leaf ground. A single
    slow reverent push toward Christ's face/torso, SETTLED (camera fully
    stopped) well before the window ends so the tear_hole transition into
    s68 grabs a static frame, not a still-moving one.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s4c_insert_pans.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "panel_animator"))
from insert_page_camera import InsertPageCamera  # noqa: E402

HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
OUT = HERE / "clips"
OUT.mkdir(exist_ok=True)

OUT_W, OUT_H = 2752, 1536  # native still resolution, 16:9

JOBS = [
    ("s43_insert_scholars_margin2", 13.6, [
        {"t": 0.00, "cx": 0.50, "cy": 0.48, "zoom": 1.00, "hold_s": 0.5},
        {"t": 0.32, "cx": 0.27, "cy": 0.40, "zoom": 1.75, "hold_s": 2.8},
        {"t": 0.68, "cx": 0.66, "cy": 0.42, "zoom": 1.65, "hold_s": 2.8},
        {"t": 1.00, "cx": 0.50, "cy": 0.48, "zoom": 1.00, "hold_s": 0.0},
    ]),
    ("s67_insert_gilded_proclamation2", 9.0, [
        {"t": 0.00, "cx": 0.50, "cy": 0.50, "zoom": 1.00, "hold_s": 0.0},
        {"t": 0.72, "cx": 0.50, "cy": 0.40, "zoom": 1.15, "hold_s": 0.0},
        {"t": 1.00, "cx": 0.50, "cy": 0.40, "zoom": 1.15, "hold_s": 0.0},
    ]),
]


def main():
    names = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    for name, duration_s, keyframes in JOBS:
        if names and name not in names:
            continue
        out_mp4 = OUT / f"{name}.mp4"
        if out_mp4.exists():
            print(f"[skip] {out_mp4.name} already exists -- remove it first")
            continue
        still = STILLS / f"{name}.png"
        if not still.exists():
            print(f"[MISSING STILL] {still} -- skipping {name}")
            continue
        cam = InsertPageCamera(still, keyframes=keyframes, duration_s=duration_s,
                                apply_raking_light=False, out_w=OUT_W, out_h=OUT_H)
        cam.render_clip(out_mp4)


if __name__ == "__main__":
    main()
