"""The First Gospel in the Curse -- step 2: animate the 7 spreads whose
intended effect genuinely needs generated motion (the other 4 -- s02, s04,
s05, s08b -- are $0 dynamic_cam3d pushes, see _kenburns.py, since their
effect IS a camera move, not real generated life).

Design pass per shot (not a mechanical wide=veo/close=seedance split):
  s01 -- the trembling itself is the content -> Seedance, explicit tremor.
  s03 -- an unseen presence arriving, atmosphere only, no body gesture ->
    veo (its proven strength; also the serpent object itself never has to
    move, sidestepping this project's own history of invented serpent
    motion on paid renders).
  s06 -- a REAL cued gesture (Adam and Eve turning to face the light) ->
    Kling (veo does not reliably execute designed/cued motion, per the
    2026-08-13 bake-off).
  s07 -- atmosphere only, no face -> veo.
  s08a -- Eve's internal shift, worth a touch of real life, face-fidelity
    matters -> Seedance (veo softened face fidelity on a portrait in the
    same bake-off).
  s09 -- the tear/light-pour needs to feel alive, atmosphere -> veo.
  s10 -- reverent radiant hold, veo's clearest proven win -> veo,
    POSITIVE-ONLY glow phrasing (the known glitter gotcha).

  .venv\\Scripts\\python.exe poc_living_sketchbook/first_gospel_in_the_curse/_s2_animate.py
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
A.EPISODE = "LS_FirstGospelInTheCurse"
A.OUT = HERE / "clips"
A.OUT.mkdir(exist_ok=True)

STILLS = HERE / "stills"

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, torn edges, and every sketch line hold perfectly still. ")

# (name, provider, duration, motion)
JOBS = [
    # ROUND 2 (user: too many Ken Burns, re-fight the important ones with
    # different providers/redesigned prompts rather than accept the $0
    # fallback everywhere). s01 and s05 tried here too but reverted back to
    # _kenburns.py after real defects on inspection: s01 (Kling) invented a
    # visible double-band wrap around both wrists that wasn't in the
    # source still; s05 (Seedance) rotated the whole foot to a different
    # pose/angle mid-clip instead of just stirring the grass. Neither is a
    # hero shot, so $0 stayed the disciplined choice once the paid retry
    # showed a real violation rather than a clean win.

    ("s02_waiting_in_trees", "seedance", 4,
     "Adam and Eve hold their exact positions and poses, perfectly "
     "still -- only a single slow, natural blink from each of them, and "
     "the leaves and hanging branches around them stirring very faintly "
     "as if in a light breeze. INVENT NOTHING new otherwise. Nothing "
     "else changes."),

    ("s04_serpent_in_light", "veo", 4,
     "The serpent holds its exact shape and position, perfectly still "
     "-- it does not move, coil, or change shape at all. Only: the soft "
     "light falling on it breathes very gently brighter and dimmer. "
     "Nothing else in the frame changes."),

    ("s03_turns_to_serpent", "veo", 4,
     "The serpent holds its exact shape and position, perfectly still -- "
     "it does not move, coil, or change shape at all. Only: the soft "
     "unseen light falling on it breathes and intensifies very gently, "
     "as if an unseen presence has just arrived and is watching. Nothing "
     "else in the frame changes."),

    ("s06_turn_to_eve_adam", "kling", 5,
     "Adam and Eve's heads and shoulders complete ONE slow, small "
     "motion -- both turning slightly toward the light now falling on "
     "them -- then holding that turned position still for the rest of "
     "the clip. INVENT NOTHING new otherwise. Nothing else in the frame "
     "changes."),

    ("s07_gold_thread_in_curse", "veo", 4,
     "The dark storm clouds and the thin gold thread of light running "
     "through them hold their exact shape, perfectly still overall -- "
     "only the gold light itself breathes very gently brighter and "
     "dimmer, alive and persistent against the dark. Nothing else in "
     "the frame changes."),

    ("s08a_eve_face_conviction", "seedance", 4,
     "Eve's face holds its exact position, perfectly still -- only a "
     "single slow, natural blink, and her expression softening very "
     "slightly, quietly, as the weight of what she's just understood "
     "settles in. INVENT NOTHING new otherwise. Nothing else changes."),

    ("s09_landing_transition", "kling", 5,
     "Christ and the torn paper edges hold their exact position and "
     "shape, perfectly still -- His pose never changes. The small, pale, "
     "simple serpent sketch-outline in the upper left holds its EXACT "
     "current small size and plain coiled shape -- it does NOT grow "
     "larger, does NOT gain new detail or scales, does NOT raise a hood, "
     "does NOT become a cobra, does NOT change in any way. Only: the "
     "warm gold light pouring through the tear breathes and grows very "
     "gently brighter, alive. Nothing else in the frame changes."),

    ("s10_landing_christ", "veo", 4,
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
