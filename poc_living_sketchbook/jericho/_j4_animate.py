"""Jericho — step 4: animate 11 spreads (j03 laps-map + j04 hunt-and-lock are
$0 deterministic camera work in the assembler, no i2v). Stages j08-j10 get
ambient motion ONLY — the hard cuts carry the collapse.

  .venv\\Scripts\\python.exe poc_living_sketchbook/jericho/_j4_animate.py
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
A.EPISODE = "LS_Jericho"
A.OUT = HERE / "clips"
A.OUT.mkdir(exist_ok=True)

STILLS = HERE / "stills"

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, torn edges, and every sketch line hold perfectly still. ")
NOGLITTER = ("the light stays a steady, even glow -- it does not sparkle, "
             "flicker into particles, or scatter into glitter. ")

JOBS = [
    ("j01_walls", "seedance", 4,
     "Only: the distant column of marching silhouettes drifts very slowly "
     "forward along its path, faint dust hangs above them, the dawn light "
     "breathes gently. The walls and sky hold perfectly still. Nothing "
     "else changes."),
    ("j02_feet", "seedance", 4,
     "Only: low dust drifts across the ground, the long morning shadows "
     "hold, the hanging robe hems sway very slightly. The feet themselves "
     "stay frozen mid-stride. Nothing else changes."),
    ("j05_rahab", "seedance", 8,
     "The woman holds her exact pose and expression, hands frozen on the "
     "cord at the window bar -- no head turn, no new hand movement. Only: "
     "the warm lamplight on her face breathes gently, " + NOGLITTER +
     "the hanging end of the scarlet cord sways very slightly in the "
     "night air. Nothing else changes."),
    ("j06_thread", "seedance", 4,
     "The scarlet thread holds perfectly still. Only: a soft warm light "
     "across the paper breathes very gently, " + NOGLITTER + "Nothing "
     "else changes."),
    ("j07_trumpets", "kling", 5,
     "All the silhouetted figures stay perfectly frozen like statues -- "
     "no arms move, no heads turn, the raised trumpets hold their exact "
     "positions. INVENT NOTHING new, no new figures appear. Only: the "
     "line of gold dawn light along the horns and robes brightens slowly "
     "and steadily, " + NOGLITTER + "faint dust drifts low. Nothing else "
     "changes."),
    ("j08_stage_a", "seedance", 4,
     "The wall, its cracks, and the scarlet cord hold their exact "
     "positions -- the cracks do NOT grow, nothing falls. Only: fine dust "
     "sifts gently from the crack joints, the light breathes faintly. "
     "Nothing else changes."),
    ("j09_stage_b", "seedance", 4,
     "The falling slabs stay frozen exactly where they hang in the air -- "
     "nothing continues to fall, nothing lands. Only: the great dust "
     "plumes billow and churn slowly, thickening. Nothing else changes."),
    ("j10_stage_c", "seedance", 4,
     "The rubble field, the standing wall fragment, the window, and the "
     "scarlet cord hold perfectly still. Only: settling dust drifts "
     "slowly across the scene, the first warm light on the fragment "
     "breathes gently. Nothing else changes."),
    ("j11_spared", "seedance", 8,
     "The woman and the family figures behind her stay perfectly frozen "
     "like statues -- no steps, no head turns, no face changes. Only: the "
     "morning gold light breaking over them pulses softly and evenly, "
     + NOGLITTER + "the hanging scarlet cord sways very slightly, faint "
     "dust drifts in the light. Nothing else changes."),
    ("j12_line", "seedance", 8,
     "The scarlet thread and every faint generation sketch hold perfectly "
     "still. Only: the warm gold glow at the right edge breathes slowly, "
     + NOGLITTER + "Nothing else changes."),
    ("j13_landing", "seedance", 8,
     "The torn paper edges, the scarlet thread, and the faint cross "
     "silhouette hold perfectly still. Only: the warm gold glow beneath "
     "the torn page breathes very slowly, " + NOGLITTER + "Nothing else "
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
