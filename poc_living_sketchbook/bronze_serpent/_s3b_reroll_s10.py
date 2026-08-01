"""One-off re-roll of s10_golgotha after the user caught real body sway in the
finished cut ("the Jesus on the cross is doing a bit of a dance"). The
existing first/last-frame audit passed because the clip returns close to its
start pose by the end; a full-duration frame-by-frame + rigid-point-tracking
re-check (comparing Christ's head/chest against the fixed crossbeam, which
DOES stay pixel-locked at dx=dy=0 the whole clip) showed the head oscillating
up to 44px side-to-side and the chest bobbing +/-20px vertically, two full
cycles across the 4s clip -- classic sway-and-return, invisible to a
start/end-only check.

v1 (now clips/_rejected/s10_golgotha.v1_body_sway_reject.mp4) used the
standard camera-lock + "hold exact position" language, same as every other
job in _s3_animate.py's JOBS list, and it wasn't enough for Seedance on this
particular figure. Per the task's escalation discipline (name the specific
defect and forbid it explicitly, same move as s06_forge's v2 attempt): this
prompt adds an explicit head/torso sway ban naming the exact axes observed
(left-right head tilt, up-down chest bob) on top of the original language.
Staying on Seedance (not switching to Kling) -- the wound-regeneration risk
that put this job on Seedance in the first place (living-light-no-fresh-blood
memory: Kling has regenerated blood from crucifixion iconography even on a
clean still) outweighs the sway risk; switching providers to chase the sway
fix would reintroduce a worse, doctrinally-sensitive risk.

ONE re-roll only, per the task brief -- if this also shows sway on the same
full-duration check, next step is the $0 deterministic static fallback
(matches s06_forge's precedent), not a second paid attempt.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_s3b_reroll_s10.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
HERE = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location(
    "_anim", ROOT / "poc_comic_page" / "_animate_piece1_v2.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
A.EPISODE = "LS_BronzeSerpent"
A.OUT = HERE / "clips"
A.OUT.mkdir(exist_ok=True)

STILLS = HERE / "stills"

PROMPT = (
    "The camera does not move, zoom, or change angle at all. Christ's "
    "entire body, the cross, and His head, arms, hands, and feet hold "
    "their EXACT current position and shape, perfectly still -- His hands "
    "and feet stay exactly as drawn, with no wound, no blood, no red mark, "
    "no nail, no puncture appearing or growing anywhere on them at any "
    "point in the clip. His head does not tilt, rock, or shift left or "
    "right at any point in the clip. His torso and chest do not rise, "
    "sink, or bob up or down at any point in the clip. Both His hands and "
    "shoulders stay pixel-locked to their exact grip on the crossbeam the "
    "entire time -- no swaying, no rocking, no oscillating back and forth, "
    "not even briefly before returning. INVENT NOTHING new -- no new "
    "figures, marks, or objects appear anywhere in the frame. Only: the "
    "dark clouds in the sky behind Him drift very slowly and evenly. "
    "Nothing else in the frame moves, including His own body."
)

import contextlib


@contextlib.contextmanager
def _note_override(note):
    orig = A.cost.record_hf
    def patched(*a, **kw):
        kw["note"] = note
        return orig(*a, **kw)
    A.cost.record_hf = patched
    try:
        yield
    finally:
        A.cost.record_hf = orig


def main():
    still = STILLS / "s10_golgotha.png"
    out = A.OUT / "s10_golgotha.mp4"
    if out.exists():
        print(f"[skip] s10_golgotha.mp4 already exists at {out} -- remove it first")
        return
    with _note_override("[bronzeserpent] s10_golgotha v2 (sway re-roll)"):
        ok = A.run_job("s10_golgotha", "seedance", still, "9:16", PROMPT, duration=4)
    print("clean" if ok else "FAILED")


if __name__ == "__main__":
    main()
