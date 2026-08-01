"""Style bake-off — animation tests on the 2 best controlled-animation
candidates (+1 honest stress test on the gesture style). Reuses the proven
run_job from poc_comic_page/_animate_piece1_v2.py (same as storm/_s3).

  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_bakeoff/_animate_tests.py
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
A.EPISODE = "LS_StyleBakeoff"
A.OUT = HERE

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, page edges, and every drawn line hold perfectly still. ")
NOGLITTER = ("a steady, even glow -- it does not sparkle, flicker into "
             "particles, or scatter into glitter. ")

# (name, provider, duration, motion)
JOBS = [
    ("style5_vigil_gethsemane", "seedance", 8,
     "Jesus holds his exact kneeling bowed pose, perfectly still -- no "
     "movement of body, head, or hands. The three sleeping figures behind "
     "him stay perfectly still in shadow. Only: the shaft of pale "
     "moonlight breathes very gently brighter and dimmer, " + NOGLITTER +
     "and the small olive leaves at the branch tips stir very faintly. "
     "Nothing else changes."),

    ("style6_gilded_transfiguration", "kling", 5,
     "Jesus's face, eyes, and expression stay perfectly still and "
     "unchanged; the two luminous flanking figures and the three fallen "
     "disciples below stay perfectly frozen in their exact poses. Only: "
     "the burnished gold ground breathes very gently brighter and dimmer "
     "as one even sheen across its whole surface, " + NOGLITTER +
     "Nothing else in the frame changes."),

    ("style2_gesture_temple", "seedance", 4,
     "Jesus and the two merchant figures stay perfectly frozen in their "
     "exact drawn poses like statues; the tilting table holds its exact "
     "angle and does not fall further. Only: the two doves each complete "
     "one slow gentle wingbeat and glide a short distance upward, and the "
     "scattered coins in the air drift slowly downward a short distance. "
     "Every charcoal line of the figures, the paper texture, and the "
     "drawn frame border hold perfectly still. Nothing else changes."),
]


def main():
    results = []
    for name, provider, dur, motion in JOBS:
        still = HERE / f"{name}.png"
        out = HERE / f"{name}.mp4"
        if out.exists():
            print(f"[skip] {name}")
            results.append((name, "cached"))
            continue
        prompt = LOCK + motion
        ok = A.run_job(name, provider, still, "9:16", prompt, duration=dur)
        if not ok:
            print("   retrying once ...")
            ok = A.run_job(name, provider, still, "9:16", prompt, duration=dur)
        results.append((name, "clean" if ok else "FAILED"))
    print("\n=== summary ===")
    for name, status in results:
        print(f"  {name}: {status}")


if __name__ == "__main__":
    main()
