"""Look and Live (Bronze Serpent short #1) -- step 2: animate all 13 spreads.
Camera-locked INVENT-NOTHING prompts, only named ambient motion. Seedance
for calm/single-subject; Kling for multi-figure gesture (s06) and the one
designed acting spread (s07) and the sacred Christ landing frame (s12b) --
same "multi-figure/action/faces under pressure" split two_goats/piece1 used.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_s2_animate.py
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
A.EPISODE = "LS_LookAndLive"
A.OUT = HERE / "clips"
A.OUT.mkdir(exist_ok=True)

STILLS = HERE / "stills"

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, torn edges, and every sketch line hold perfectly still. ")
NOGLITTER = ("the light stays a steady, even glow -- it does not sparkle, "
             "flicker into particles, or scatter into glitter. ")

# (name, provider, duration, motion)
JOBS = [
    ("s01_hook", "seedance", 4,
     "Every figure holds their exact pose and position, perfectly still -- "
     "no one takes a step, no arm changes position. Only: the ochre dust "
     "haze drifts faintly, the torn tent cloth stirs very slightly. Nothing "
     "else changes."),

    ("s02_object_reveal", "seedance", 4,
     "The serpent-on-pole holds its exact shape and position, perfectly "
     "still. Only: the dusk sky breathes very faintly. Nothing else "
     "changes."),

    ("s03_unused_remedy", "kling", 5,
     "The jar, herbs, and cloth hold their exact positions and exact "
     "distance from camera, perfectly still -- the framing and scale never "
     "change, no push-in, no zoom. Only: a faint dust settles gently. "
     "Nothing else changes."),

    ("s04_bitten_arm", "kling", 5,
     "The bandaged arm, the wound, and the small existing mark hold their "
     "EXACT current appearance, perfectly still -- no flexing, no "
     "movement, no new blood, no bleeding, nothing drips or flows, the "
     "wound never changes from how it already looks in this image. INVENT "
     "NOTHING new. Only: the light across the linen breathes very gently. "
     "Nothing else changes."),

    ("s05_eye_reflection", "seedance", 4,
     "The eye holds its exact open position -- no blink, no eye movement. "
     "INVENT NOTHING new. Only: the light breathes very faintly. Nothing "
     "else changes."),

    ("s06_verse_backdrop", "kling", 5,
     "Every figure stays perfectly frozen like statues -- no arm, hand, or "
     "head moves from its exact current position, no gestures complete or "
     "change, no steps are taken. INVENT NOTHING new. Only: the dust haze "
     "over the cracked ground drifts very faintly. Nothing else in the "
     "frame changes."),

    ("s07_look_and_live_acting", "kling", 5,
     "The figure's head and shoulder complete ONE slow motion: continuing "
     "to lift and turn upward, exactly as already begun in this image, then "
     "holding that raised position still for the rest of the clip -- no "
     "further movement after that. INVENT NOTHING new otherwise. The warm "
     "light on their face and shoulder breathes gently brighter. Nothing "
     "else in the frame changes."),

    ("s08_crowd_healing", "seedance", 4,
     "Every figure holds their exact head position and pose, perfectly "
     "still. The serpent's tongue holds its EXACT current short curved "
     "shape -- it does not extend, whip, lash, lengthen, or change shape at "
     "all. INVENT NOTHING new, no one moves or turns further. Only: the "
     "warm glow touching the nearer faces breathes gently. Nothing else "
     "changes."),

    ("s09_atmosphere_dawn", "seedance", 4,
     "The kneeling figure holds his exact bowed prayer pose, perfectly "
     "still -- no movement, no shifting. Only: the pale dawn light over the "
     "mountains breathes very gently. Nothing else changes."),

    ("s10_own_cure", "seedance", 4,
     "The hands hold their exact grip on the herb-pouch, perfectly still. "
     "Only: the warm foreground light breathes gently. Nothing else "
     "changes."),

    ("s11_plain_sight", "seedance", 8,
     "Every figure holds their exact position and task, perfectly still -- "
     "no one completes a new action. Only: the cooking-fires flicker "
     "gently, faint dust drifts between the tents. Nothing else changes."),

    ("s12a_torn_to_gold", "seedance", 4,
     "The torn paper hole holds its EXACT current shape and edges -- it "
     "does not widen or tear further. INVENT NOTHING new. Only: the "
     "radiant gold light pouring through breathes softly and evenly -- "
     + NOGLITTER + "Nothing else changes."),

    ("s12b_landing_gold", "kling", 5,
     "The figure on the cross stays perfectly frozen like a statue -- His "
     "exact pose, head, and arms never change, no movement at all. INVENT "
     "NOTHING new. The torn paper edges hold their exact shape. Only: the "
     "radiant gold light surrounding Him breathes softly and evenly -- "
     + NOGLITTER + "Nothing else in the frame changes."),
]


def main():
    results = []
    for name, provider, dur, motion in JOBS:
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
