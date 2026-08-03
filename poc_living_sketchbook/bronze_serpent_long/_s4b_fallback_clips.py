"""Bronze Serpent LONG -- step 4b: the 8 $0 deterministic fallback clips for
spreads that never got (or were never sent to) a generative animation attempt.
Same InsertPageCamera pattern as the SHORT's own proven fallbacks
(bronze_serpent/_s3c_static_s10.py for s10_golgotha, and s06_forge's push-in
resolution referenced throughout this episode's own _s4_animate.py/RESUME.md)
-- a pure PIL crop+resize push over the static, already-passed-content-audit
still, so invented motion is categorically impossible.

Per RESUME.md's own final accounting, these 8 spreads are excluded from
generative animation for two separate reasons:
  - s28_forge_acting, s55_hezekiah_breaks: excluded BEFORE ever attempting --
    known 3-strikes hammer-strike failure class (the short's own s06_forge:
    2x Kling + 1x Seedance all invented a completed swing).
  - s44_shadow_cross, s12_vc_wherefore: excluded after round 1 for doctrinal/
    plan-device reasons (s44's cross-shaped shadow is load-bearing content,
    not worth a generative roll; s12 is a verse card, insert_page_camera-
    style pan was the plan's own suggested device for it).
  - s18_moses_empty_hands, s14_serpent_hint, s46_thesis_pair,
    s51_christ_draw_all_men: failed twice each in the redo round, deferred
    per the pre-agreed 2-strikes rule.

Rendered at each spread's REAL _PLAN.md window duration (not a generic clip
length) so assembly's ping-pong frame-hold helper never needs to bounce these
backward to fill their window -- same reasoning as s10_golgotha's fallback
(a bounce would reverse the push into a pull, its own small motion-direction
risk). Resolution matches the stills natively (2752x1536, 16:9) via
InsertPageCamera's out_w/out_h params -- the engine defaults to the SHORT's
9:16 canvas, must override for this long-form pilot.

Framing notes (each checked against the actual full-res still before picking
keyframes, not guessed):
  - s44_shadow_cross: the ONE spread with an explicit caution in RESUME.md --
    "frame the push so the FULL shadow including the crossbar stays in view
    throughout." Kept to a very mild zoom (1.00->1.06) at near-dead-center so
    both the shadow (lower-left) and Moses+pole (right two-thirds) stay
    comfortably inside the crop at every frame.
  - s46_thesis_pair: the serpent-on-pole (left) and crucified Christ (right)
    are a deliberate PAIRED composition -- the film's thesis image. Kept to
    the mildest push of the whole batch (1.00->1.05, dead center) so neither
    half is ever at risk of drifting out of frame.
  - s51_christ_draw_all_men: red-letter/Christ content -- push stays mild and
    centered on Christ without cropping the nailed hands or the drawn-toward
    crowd below, both load-bearing to the verse's own meaning.
  - s14_serpent_hint: the only spread given a real directional drift (down/
    left toward the serpent sliding into the dust) rather than a plain push --
    matches the beat's own "something slides... first hint" reveal.
  - s55_hezekiah_breaks: this spread ALSO gets the plan's own impact-burst
    device (_PLAN.md row 55) layered on TOP at ASSEMBLY time, the same way
    the short layered candle-only onto s06_forge's push-in -- NOT baked in
    here. This script only produces the base camera-push plate.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s4b_fallback_clips.py
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

OUT_W, OUT_H = 2752, 1536  # native still resolution, 16:9 (NOT the engine's 9:16 default)

# (name, duration_s [real _PLAN.md window], keyframes)
JOBS = [
    ("s28_forge_acting", 7.02, [
        {"t": 0.00, "cx": 0.53, "cy": 0.50, "zoom": 1.00, "hold_s": 0.0},
        {"t": 1.00, "cx": 0.53, "cy": 0.50, "zoom": 1.06, "hold_s": 0.0},
    ]),
    ("s55_hezekiah_breaks", 7.40, [
        {"t": 0.00, "cx": 0.50, "cy": 0.50, "zoom": 1.00, "hold_s": 0.0},
        {"t": 1.00, "cx": 0.56, "cy": 0.50, "zoom": 1.10, "hold_s": 0.0},
    ]),
    ("s44_shadow_cross", 7.16, [
        {"t": 0.00, "cx": 0.55, "cy": 0.49, "zoom": 1.00, "hold_s": 0.0},
        {"t": 1.00, "cx": 0.55, "cy": 0.49, "zoom": 1.06, "hold_s": 0.0},
    ]),
    ("s12_vc_wherefore", 10.88, [
        {"t": 0.00, "cx": 0.52, "cy": 0.68, "zoom": 1.00, "hold_s": 0.0},
        {"t": 1.00, "cx": 0.52, "cy": 0.68, "zoom": 1.12, "hold_s": 0.0},
    ]),
    ("s18_moses_empty_hands", 6.61, [
        {"t": 0.00, "cx": 0.50, "cy": 0.55, "zoom": 1.00, "hold_s": 0.0},
        {"t": 1.00, "cx": 0.50, "cy": 0.55, "zoom": 1.12, "hold_s": 0.0},
    ]),
    ("s14_serpent_hint", 6.16, [
        {"t": 0.00, "cx": 0.50, "cy": 0.45, "zoom": 1.00, "hold_s": 0.0},
        {"t": 1.00, "cx": 0.45, "cy": 0.75, "zoom": 1.25, "hold_s": 0.0},
    ]),
    ("s46_thesis_pair", 5.00, [
        {"t": 0.00, "cx": 0.50, "cy": 0.50, "zoom": 1.00, "hold_s": 0.0},
        {"t": 1.00, "cx": 0.50, "cy": 0.50, "zoom": 1.05, "hold_s": 0.0},
    ]),
    ("s51_christ_draw_all_men", 6.88, [
        {"t": 0.00, "cx": 0.50, "cy": 0.50, "zoom": 1.00, "hold_s": 0.0},
        {"t": 1.00, "cx": 0.52, "cy": 0.48, "zoom": 1.08, "hold_s": 0.0},
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
