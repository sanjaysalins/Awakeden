"""$0 deterministic fallback for s10_golgotha, after TWO real generative
failures (matches s06_forge's own precedent for when to stop paying for
re-rolls and go static):

  v1 (clips/_rejected/s10_golgotha.v1_body_sway_reject.mp4): standard camera-
     lock prompt. Full-duration frame tracking (not just first/last) showed
     the crossbeam pixel-locked the whole clip (dx=dy=0 throughout -- proof
     the CAMERA never moved) while Christ's head oscillated up to 44px side-
     to-side and His chest bobbed +/-20px vertically, two full cycles across
     4s -- exactly the "doing a bit of a dance" the user caught by eye.

  v2 (clips/_rejected/s10_golgotha.v2_head_drift_reject.mp4): ONE re-roll,
     same provider (Seedance -- switching to Kling would trade the sway risk
     for the worse, doctrinally-sensitive wound-regeneration risk documented
     in living-light-no-fresh-blood), tightened prompt explicitly naming and
     forbidding left-right head tilt and up-down chest bob. Re-verified with
     the same full-duration tracking: the oscillation was gone, but the head
     still visibly rotated/tilted away from its starting pose over the first
     ~2s and then HELD the new, wrong position for the rest of the clip --
     a settle-and-drift, not a return-to-start dance, but still a real
     violation of "hold their EXACT current position, perfectly still."
     Two real content failures on the same subject = stop per SKILL.md's own
     escalation discipline, same threshold precedent as s06_forge.

Fallback (this script): InsertPageCamera (panel_animator/insert_page_camera.py)
over the static, already-passed-content-audit still -- a pure PIL crop+resize
of ONE frame, so body sway is categorically impossible (there is no
generative content to sway). Per the task's explicit steer for this specific
spread ("reverence and stillness should win over any motion risk here
specifically, more so than on s06's forge"), the push is far gentler than
s06's (zoom 1.00 -> 1.35): a barely-perceptible zoom 1.00 -> 1.05, dead
center, single monotonic direction only (never eases back, so it cannot even
resemble a push-pull sway) -- just enough held motion that a 6s+ shot doesn't
read as a frozen glitch in an otherwise "genuinely moving" living-sketchbook
episode, while keeping the crucifixion beat as still and reverent as
possible.

Rendered at the REAL assembly window's own duration (6.20s, s10_golgotha's
SHOTS window in _s4_assemble.py runs 46.386-52.572s = 6.186s, +0.014s
margin) rather than the original 4.0s clip length, specifically so the
assembly's ping-pong frame-hold helper never needs to bounce this clip
backward to fill its window -- a bounce would replay the push-in in reverse
(a pull-out), which is its own small motion-direction risk this fallback is
specifically trying to avoid. Rendering to the window's exact length means
_s4_assemble.py's shot_frame() just plays forward through it once, no bounce
required.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_s3c_static_s10.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "panel_animator"))
from insert_page_camera import InsertPageCamera  # noqa: E402

HERE = Path(__file__).resolve().parent
STILL = HERE / "stills" / "s10_golgotha.png"
OUT = HERE / "clips" / "s10_golgotha.mp4"

# s10_golgotha's real SHOTS window in _s4_assemble.py: (46.386, 52.572) = 6.186s.
DURATION_S = 6.20

KEYFRAMES = [
    {"t": 0.00, "cx": 0.5, "cy": 0.5, "zoom": 1.00, "hold_s": 0.0},
    {"t": 1.00, "cx": 0.5, "cy": 0.5, "zoom": 1.05, "hold_s": 0.0},
]


def main():
    if OUT.exists():
        print(f"[skip] {OUT} already exists -- remove it first")
        return
    if not STILL.exists():
        raise SystemExit(f"missing still: {STILL}")
    cam = InsertPageCamera(STILL, keyframes=KEYFRAMES, duration_s=DURATION_S,
                            apply_raking_light=False)
    cam.render_clip(OUT)


if __name__ == "__main__":
    main()
