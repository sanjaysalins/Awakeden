"""Two Goats — step 3: animate all 14 spreads. Camera-locked INVENT-NOTHING
prompts, only named ambient motion. Veil-tear stages get ambient-only motion
(the CUT carries the event, not the animation). Kling for figures/faces
under pressure (priest closeups, Jesus pivot); Seedance for calm/no-figure.

  .venv\\Scripts\\python.exe poc_living_sketchbook/two_goats/_g3_animate.py
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
A.EPISODE = "LS_TwoGoats"
A.OUT = HERE / "clips"
A.OUT.mkdir(exist_ok=True)

STILLS = HERE / "stills"

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, torn edges, and every sketch line hold perfectly still. ")
NOGLITTER = ("the light stays a steady, even glow -- it does not sparkle, "
             "flicker into particles, or scatter into glitter. ")

JOBS = [
    ("g01_hook", "seedance", 4,
     "The figure holds his exact braced pose, perfectly still. Only: the "
     "single oil lamp's flame breathes gently, faint dust drifts in its "
     "light. Nothing else changes."),
    ("g02_bloodgoat", "seedance", 4,
     "The hands hold their exact grip on the curtain fabric, perfectly "
     "still -- no further pulling, no stepping through. Only: the deep "
     "shadow beyond the gap breathes very faintly. Nothing else changes."),
    ("g03_scapegoat", "kling", 5,
     "Both figure and goat stay perfectly frozen like statues -- no head "
     "movement, no leg movement, no new poses. INVENT NOTHING. Only: the "
     "wide pale sky breathes almost imperceptibly, faint dust drifts on the "
     "ground. Nothing else changes."),
    ("g04_intodesert", "seedance", 8,
     "The goat holds its exact walking pose and position -- it does not "
     "take further steps or move from its spot. Only: heat-shimmer drifts "
     "faintly above the sand, faint dust stirs at its feet. Nothing else "
     "changes."),
    ("g05_onepay_onecarry", "seedance", 4,
     "Both goats and the thread hold their exact positions. Only: the gold "
     "thread connecting them breathes gently, " + NOGLITTER + "Nothing else "
     "changes."),
    ("g06_yearsasked", "seedance", 4,
     "The figure holds his exact seated pose and expression, perfectly "
     "still. Only: the lamplight breathes gently, faint dust drifts. "
     "Nothing else changes."),
    ("g07_bothhalves", "seedance", 4,
     "Both threads hold their exact split shape and position. Only: a soft "
     "blue-wash shadow breathes very faintly around them. Nothing else "
     "changes."),
    ("g08_jesuspivot", "kling", 5,
     "The figure stays perfectly frozen like a statue -- his exact pose, "
     "arms, and expression never change, no steps, no head turn. INVENT "
     "NOTHING new. The gold seam along his edge stays a steady, unbroken, "
     "glowing line -- " + NOGLITTER + "Only: the radiant gold light "
     "breathes softly and evenly, faint dust motes drift through the "
     "light. Nothing else in the frame changes."),
    ("g09_isaiah536", "seedance", 4,
     "The scarlet thread holds its exact shape, perfectly still. Only: a "
     "soft warm light across the paper breathes very gently. Nothing else "
     "changes."),
    ("g10_finished", "seedance", 8,
     "The figure holds his exact seated resting pose, perfectly still -- no "
     "movement, no shifting. Only: the radiant doorway light behind him "
     "pulses softly and evenly, " + NOGLITTER + "faint dust drifts in the "
     "light. Nothing else changes."),
    ("g11_veil_whole", "seedance", 4,
     "The curtain holds its exact whole, unbroken shape -- it does not "
     "move, sway, or begin to tear. Only: the dim lamplight on its woven "
     "surface breathes very faintly. Nothing else changes."),
    ("g12_veil_tearing", "seedance", 4,
     "The tear in the curtain holds its EXACT current width and shape -- it "
     "does not widen or tear further, nothing continues to rip. INVENT "
     "NOTHING new. Only: the shaft of light through the gap breathes "
     "gently, loose threads at the tear's edge tremble almost "
     "imperceptibly. Nothing else changes."),
    ("g13_veil_torn", "seedance", 8,
     "Both curtain halves hold their exact torn positions -- they do not "
     "move, swing, or separate further. Only: the radiant light flooding "
     "through the gap pulses softly and evenly, " + NOGLITTER + "dust "
     "drifts in the light. Nothing else changes."),
    ("g14_landing", "seedance", 8,
     "The torn paper edges, the faint curtain-halves, and the scarlet "
     "thread hold perfectly still. Only: the warm gold glow beneath the "
     "torn page breathes very slowly, " + NOGLITTER + "Nothing else "
     "changes."),
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
