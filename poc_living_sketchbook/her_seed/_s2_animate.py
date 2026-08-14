"""Her Seed -- step 2: animate the 5 spreads whose intended effect
genuinely needs generated motion (s02/s03/s05 are $0 devices, see
_kenburns.py).

Design pass per shot (not a mechanical wide=veo/close=seedance split):
  s01 -- leaves continuing to drift is the content, calm, no cued gesture
    -> Seedance (matches the long's own "leaves drift, calm" treatment).
  s04 -- a REAL cued gesture (hands gathering at her heart, light
    brightening, then holds) -> Kling (veo does not reliably execute
    designed/cued motion, per this project's own bake-off).
  s06 -- REVISED post-lock: was a close portrait (Seedance tier); is now
    a wide two-element reverent hold (Mary + a distant bare cross), no
    cued gesture -> retiered to veo3_1_lite, matching s08's own tier.
  s07 -- reach, then release -- a real two-stage cued gesture -> Kling.
  s08 -- reverent radiant hold, veo's clearest proven win per short #1 ->
    veo, POSITIVE-ONLY glow phrasing (the known glitter gotcha).

  .venv\\Scripts\\python.exe poc_living_sketchbook/her_seed/_s2_animate.py
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
A.EPISODE = "LS_HerSeed"
A.OUT = HERE / "clips"
A.OUT.mkdir(exist_ok=True)

STILLS = HERE / "stills"

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, torn edges, and every sketch line hold perfectly still. ")

# (name, provider, duration, motion)
JOBS = [
    ("s01_eden_coming_apart", "seedance", 4,
     "Adam and Eve hold their exact positions and poses, perfectly "
     "still. Adam's head and face stay LOCKED at the exact same fixed "
     "angle and position for the entire clip -- his head does NOT turn, "
     "rotate, or tilt at any point, he does not look toward Eve or "
     "anywhere else -- the ONLY motion on his face is his eyelids "
     "closing and opening once for a single slow, natural blink, "
     "nothing else about his head or face moves even slightly. The "
     "leaves already drifting down through the canopy continue "
     "drifting, calm and natural, at the same gentle pace. Nothing "
     "else in the frame changes."),

    ("s04_mary_annunciation", "kling", 5,
     "Mary's hands complete ONE slow, small motion -- gathering closer "
     "together at her heart -- then holding that gathered position "
     "still for the rest of the clip, while the soft light above her "
     "breathes very gently brighter. INVENT NOTHING new otherwise. "
     "Nothing else in the frame changes."),

    ("s06_mary_close", "veo", 4,
     "Mary and the distant bare cross behind her hold their exact "
     "positions, perfectly still -- she does not move or change pose, "
     "the cross does not change. Only: the dusky sky breathes very "
     "gently, soft cloud drift, the light along the horizon glowing and "
     "dimming very gently. Nothing else in the frame changes."),

    ("s07_hands_reaching", "kling", 5,
     "The two clasped hands complete ONE slow, small motion -- the grip "
     "gently loosening and opening -- then holding that opened, "
     "relaxed position still for the rest of the clip. INVENT NOTHING "
     "new otherwise. Nothing else in the frame changes."),

    ("s08_landing_christ", "veo", 4,
     "Christ stays perfectly frozen in His exact pose, no movement at "
     "all. The radiant gold light surrounding Him stays exactly as warm "
     "and steady as it already is, breathing very gently brighter and "
     "softer, alive and unchanged in color. Nothing else in the frame "
     "changes."),
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
