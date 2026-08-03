"""Bronze Serpent LONG -- step 4c: Ken Burns replacements for s49 and s65.

User's own eye-check (2026-08-03) caught residual invented motion on BOTH
generative attempts -- Christ's figure still reads as "dancing" even after a
prior reroll (s49 is already on its 2nd/3rd generative attempt per the
v1_reject/v2_dancing_reject/v3_pre_richness files in clips/; s65 already had
a v1 robe-sway reject before this). Rather than a 3rd generative roll, same
call the project already made for the SHORT's own s06_forge (2x Kling + 1x
Seedance all invented motion -> switched to a deterministic push instead)
and for 8 other LONG spreads via _s4b_fallback_clips.py: swap to the
InsertPageCamera pure PIL crop+resize push over the already-approved still,
where invented motion is categorically impossible.

Old generative clips renamed (not deleted) to
s49_christ_radiant_begin.v2_dancing_reject.mp4 /
s65_christ_open_invite.v2_dancing_reject.mp4.

Rendered at each spread's REAL _PLAN.md window duration (row 49 = 8.8s, row
65 = 6.0s) -- same reasoning as every other InsertPageCamera fallback in this
episode: avoids assembly's ping-pong frame-hold ever needing to bounce a
push backward into a pull.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s4c_kenburns_s49_s65.py
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

OUT_W, OUT_H = 2752, 1536  # native still resolution, 16:9

JOBS = [
    # s49: crucifixion, arms wide near the top third -- mild centered push,
    # same treatment as s51_christ_draw_all_men's fallback (also Christ-on-
    # cross content) so it doesn't stand out as differently handled.
    ("s49_christ_radiant_begin", 8.8, [
        {"t": 0.00, "cx": 0.50, "cy": 0.45, "zoom": 1.00, "hold_s": 0.0},
        {"t": 1.00, "cx": 0.50, "cy": 0.42, "zoom": 1.08, "hold_s": 0.0},
    ]),
    # s65: standing full-figure, generous blank margin either side -- safe
    # to push a little further in toward the face/chest without any risk of
    # cropping hands or feet.
    ("s65_christ_open_invite", 6.0, [
        {"t": 0.00, "cx": 0.50, "cy": 0.48, "zoom": 1.00, "hold_s": 0.0},
        {"t": 1.00, "cx": 0.50, "cy": 0.44, "zoom": 1.10, "hold_s": 0.0},
    ]),
]


def main():
    for name, duration_s, keyframes in JOBS:
        out_mp4 = OUT / f"{name}.mp4"
        still = STILLS / f"{name}.png"
        if not still.exists():
            print(f"[MISSING STILL] {still} -- skipping {name}")
            continue
        cam = InsertPageCamera(still, keyframes=keyframes, duration_s=duration_s,
                                apply_raking_light=False, out_w=OUT_W, out_h=OUT_H)
        cam.render_clip(out_mp4)
        print(f"[done] {out_mp4.name}")


if __name__ == "__main__":
    main()
