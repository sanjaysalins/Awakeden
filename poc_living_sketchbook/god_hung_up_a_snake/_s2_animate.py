"""God Hung Up a Snake (Bronze Serpent short #2) -- step 2: animate all 13
spreads. Camera-locked INVENT-NOTHING prompts, only named ambient motion.
Kling for the designed acting spread (s05, the forge) and the sacred Christ
landing frame (s12b) -- same tiering as Look and Live; Seedance everywhere
else, including the aerial spreads (s04/s08) since figures are small/distant
there, low distortion risk.

  .venv\\Scripts\\python.exe poc_living_sketchbook/god_hung_up_a_snake/_s2_animate.py
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
A.EPISODE = "LS_GodHungUpASnake"
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
     "no one moves. Only: the dust haze drifts faintly, torn tent cloth "
     "stirs very slightly. Nothing else changes."),

    ("s02_pole_reveal", "kling", 5,
     "The camera's exact framing, distance, and zoom level never change at "
     "any point in the clip. The serpent-on-pole holds its exact shape and "
     "position, perfectly still. Only: the cold night sky breathes very "
     "faintly. Nothing else changes."),

    ("s03_texture_insert", "seedance", 4,
     "The coiled scales and the pole hold their exact position, perfectly "
     "still. Only: the cold moonlight breathes very faintly across the "
     "surface. Nothing else changes."),

    ("s04_camp_gathered", "seedance", 8,
     "Every tent and every tiny figure holds its exact position, perfectly "
     "still -- no one moves or walks. INVENT NOTHING new. Only: the warm "
     "glow at the center breathes very softly. Nothing else changes."),

    ("s05_forge_acting", "kling", 5,
     "His hammer arm completes ONE slow strike, exactly as already begun "
     "in this image, then holds still for the rest of the clip -- no "
     "further strikes after that. INVENT NOTHING new otherwise, no new "
     "sparks beyond what a single strike would throw. The forge's orange "
     "glow breathes gently. Nothing else in the frame changes."),

    ("s06_mother_child_look", "seedance", 4,
     "Both figures hold their exact pose and expression, perfectly still. "
     "Only: the light beginning to touch their faces breathes gently. "
     "Nothing else changes."),

    ("s07_moses_face", "kling", 5,
     "The camera's exact framing, distance, and zoom level never change at "
     "any point in the clip -- no push-in, no zoom. His exact expression "
     "and pose hold perfectly still -- no head movement, no change of "
     "expression. Only: the plain daylight breathes very faintly. Nothing "
     "else changes."),

    ("s08_raw_bronze_insert", "seedance", 4,
     "The bronze lumps and tools hold their exact positions, perfectly "
     "still. Only: the soft raking light breathes very gently across the "
     "stone. Nothing else changes."),

    ("s09_reaching_soft", "seedance", 4,
     "The hands hold their exact grip on the wreath and cloth, perfectly "
     "still. Only: the warm light on the hands breathes gently. Nothing "
     "else changes."),

    ("s10_heavy_sky", "seedance", 8,
     "The clouds hold their exact shapes and positions overall -- only a "
     "very slow, gentle drift of the cloud edges is visible, nothing "
     "reshapes suddenly. Nothing else changes."),

    ("s11_pole_night", "seedance", 4,
     "The serpent-on-pole and the resting camp hold their exact positions, "
     "perfectly still. Only: the deep blue-wash night breathes very "
     "faintly. Nothing else changes."),

    ("s12a_torn_to_gold", "seedance", 4,
     "The torn paper hole holds its EXACT current shape and edges -- it "
     "does not widen or tear further. INVENT NOTHING new. Only: the "
     "radiant gold light pouring through breathes softly and evenly -- "
     + NOGLITTER + "Nothing else changes."),

    ("s12b_landing_christ", "kling", 5,
     "The figure on the cross stays perfectly frozen like a statue -- His "
     "exact pose, head, and arms never change, no movement at all. INVENT "
     "NOTHING new. The small serpent below holds its exact position. Only: "
     "the radiant gold light surrounding Him breathes softly and evenly -- "
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
