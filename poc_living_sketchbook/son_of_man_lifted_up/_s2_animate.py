"""Even So Must the Son of Man Be Lifted Up (Bronze Serpent short #3) --
step 2: animate all 13 spreads. Camera-locked INVENT-NOTHING prompts, only
named ambient motion. Seedance for calm/single-subject; Kling for the one
designed acting spread (s05), the hero cross shot (s08), and the sacred
landing (s13) -- same "acting/hero/landing" tiering #1/#2 used, quoted to
the user at ~$10.58 (10 Seedance x4.8cr + 3 Kling x7.5cr = 70.5cr).

s04/s06 (the bronze serpent object) get EXPLICIT shape-lock language on the
serpent itself, not just the human figures -- Look and Live's own s08 this
cluster had Seedance invent a tongue-whip and a head-bend on the SAME
object across 2 straight tries before falling back to a $0 camera push;
locking the serpent's own shape here up front, not after a failure.

  .venv\\Scripts\\python.exe poc_living_sketchbook/son_of_man_lifted_up/_s2_animate.py
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
A.EPISODE = "LS_SonOfManLiftedUp"
A.OUT = HERE / "clips"
A.OUT.mkdir(exist_ok=True)

STILLS = HERE / "stills"

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, torn edges, and every sketch line hold perfectly still. ")
NOGLITTER = ("the light stays a steady, even glow -- it does not sparkle, "
             "flicker into particles, or scatter into glitter. ")
SERPENT_LOCK = ("The serpent-on-pole holds its EXACT current shape and "
                 "position, perfectly still -- its coils, head, and tongue "
                 "do not move, extend, whip, or change shape at all. ")

# (name, provider, duration, motion)
JOBS = [
    ("s01_hook", "seedance", 4,
     "Both men hold their exact seated poses and positions, perfectly "
     "still -- no gesture, no head turn. Only: the small oil lamp's flame "
     "flickers gently, faint stars in the night sky twinkle subtly. "
     "Nothing else changes."),

    ("s02_close_faces", "seedance", 4,
     "Both men hold their exact expressions and head positions, "
     "perfectly still -- no gesture, no blink. Only: the lamp-light "
     "between them breathes gently warmer. Nothing else changes."),

    ("s03_jesus_split_light", "seedance", 4,
     "Jesus holds his exact expression and head position, perfectly "
     "still -- no blink, no head turn. Only: the lamp's flame flickers "
     "gently, the warm light breathes softly. Nothing else changes."),

    ("s04_ot_echo", "seedance", 4,
     SERPENT_LOCK + "Every Israelite figure holds their exact position, "
     "perfectly still. INVENT NOTHING new, no one moves or turns further. "
     "Only: the dusk sky and dust haze drift very faintly. Nothing else "
     "changes."),

    ("s05_acting_memory_bleed", "kling", 5,
     "Jesus's head and hand complete ONE slow, small motion -- gesturing "
     "gently as He speaks, His hand lifting slightly -- then holding that "
     "position still for the rest of the clip. Nicodemus holds his exact "
     "listening pose, perfectly still. The memory-bleed wilderness/"
     "serpent scene behind Him holds its exact translucent shape, "
     "unmoving. INVENT NOTHING new otherwise. Nothing else in the frame "
     "changes."),

    ("s06_serpent_healed_gaze", "seedance", 4,
     SERPENT_LOCK + "The kneeling figure holds his exact lifted-gaze "
     "pose, perfectly still. INVENT NOTHING new. Only: the dusk light "
     "breathes very faintly. Nothing else changes."),

    ("s07_nicodemus_skeptic", "seedance", 4,
     "Nicodemus holds his exact expression and head position, perfectly "
     "still -- no blink, no head turn. Only: the lamp-glow on his face "
     "breathes very faintly. Nothing else changes."),

    ("s08_cross_hero", "kling", 5,
     "The figure on the cross stays perfectly frozen like a statue -- "
     "His exact pose, head, and arms never change, no movement at all. "
     "INVENT NOTHING new. Only: the storm clouds behind Him drift and "
     "shift very slowly, the light breathes softly. Nothing else in the "
     "frame changes."),

    ("s09_nailed_hand_insert", "seedance", 4,
     "The hand and the spike hold their exact current position and "
     "shape, perfectly still -- no movement, no new marks, no blood, "
     "nothing changes about the wound. INVENT NOTHING new. Only: the "
     "light across the wood breathes very gently. Nothing else changes."),

    ("s10_crowd_multivignette", "seedance", 4,
     "Every figure holds their exact position and pose, perfectly still "
     "-- no one turns or gestures further. INVENT NOTHING new. Only: the "
     "light breathes very faintly. Nothing else changes."),

    ("s11_christ_face_reverent", "seedance", 4,
     "Christ's face holds its exact bowed position, perfectly still -- "
     "no movement. INVENT NOTHING new. Only: the light breathes softly "
     "and evenly. Nothing else changes."),

    ("s12_nicodemus_tomb_daylight", "seedance", 4,
     "Nicodemus and the other mourners hold their exact positions and "
     "poses, perfectly still -- no one moves or turns further. INVENT "
     "NOTHING new. Only: the daylight breathes very faintly. Nothing "
     "else changes."),

    ("s13_landing_christ_glory", "kling", 5,
     "The figure on the cross stays perfectly frozen like a statue -- "
     "His exact pose, head, and arms never change, no movement at all. "
     "INVENT NOTHING new. Only: the radiant gold light surrounding Him "
     "breathes softly and evenly -- " + NOGLITTER + "Nothing else in the "
     "frame changes."),
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
