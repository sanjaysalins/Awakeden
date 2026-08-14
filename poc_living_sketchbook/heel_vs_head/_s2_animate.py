"""Heel vs Head -- step 2: animate the 4 spreads whose intended effect
genuinely needs generated motion (s01/s02/s05 are $0 devices, see
_kenburns.py).

Design pass per shot (not a mechanical wide=veo/close=seedance split):
  s03 -- serpent + unseen light arriving, no body gesture -> veo3_1_lite
    (atmospheric light breathing, this cluster's own proven strength).
  s04 -- serpent + a more intense pronouncement light, no body gesture
    (the head's raised pose is already baked into the still) ->
    veo3_1_lite, same reasoning as s03.
  s06 -- a real cued gesture: hands gripping tighter under tension ->
    Kling (veo does not reliably execute designed/cued motion, per this
    project's own bake-off).
  s07 -- reverent radiant hold, veo's clearest proven win per this
    cluster's own precedent -> veo3_1_lite, POSITIVE-ONLY glow phrasing
    (the known glitter gotcha).

  .venv\\Scripts\\python.exe poc_living_sketchbook/heel_vs_head/_s2_animate.py
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
A.EPISODE = "LS_HeelVsHead"
A.OUT = HERE / "clips"
A.OUT.mkdir(exist_ok=True)

STILLS = HERE / "stills"

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, torn edges, and every sketch line hold perfectly still. ")

# (name, provider, duration, motion)
JOBS = [
    ("s03_serpent_judged", "veo", 4,
     "The serpent holds its exact shape and position, perfectly still "
     "-- it does not move, coil, or change shape at all. Only: the "
     "soft unseen light falling on it breathes very gently brighter "
     "and dimmer, as if an unseen presence has just arrived. Nothing "
     "else in the frame changes."),

    ("s04_serpent_pronouncement", "veo", 4,
     "The serpent holds its exact shape and position, perfectly still "
     "-- it does not move, coil, raise its head further, or change "
     "shape at all. Only: the focused light beam falling on it "
     "breathes and intensifies very gently, alive and persistent. "
     "Nothing else in the frame changes."),

    ("s06_own_blow_straining", "kling", 5,
     "The figure's clasped hands complete ONE slow, small motion -- "
     "gripping together noticeably tighter, knuckles tensing -- then "
     "holding that tighter grip still for the rest of the clip. The "
     "head stays bowed the whole time, no other movement. INVENT "
     "NOTHING new otherwise. Nothing else in the frame changes."),

    ("s07_landing_christ", "veo", 4,
     "Christ stays perfectly frozen in His exact pose, no movement at "
     "all. The radiant gold light surrounding Him stays exactly as "
     "warm and steady as it already is, breathing very gently brighter "
     "and softer, alive and unchanged in color. Nothing else in the "
     "frame changes."),
]


def main():
    only = set(sys.argv[1:]) or None
    results = []
    for name, provider, dur, motion in JOBS:
        if only and name not in only:
            continue
        still = STILLS / f"{name}.png"
        out = A.OUT / f"{name}.mp4"
        if out.exists():
            print(f"[skip] {name}")
            results.append((name, "cached"))
            continue
        if not still.exists():
            print(f"[HOLD] {name}: still missing")
            results.append((name, "NO-STILL"))
            continue
        prompt = LOCK + motion
        ok, used = A.run_job_with_fallback(name, provider, still, "9:16", prompt, duration=dur)
        results.append((name, f"clean ({used})" if ok else "FAILED"))
    print("\n=== summary ===")
    for name, status in results:
        print(f"  {name}: {status}")


if __name__ == "__main__":
    main()
