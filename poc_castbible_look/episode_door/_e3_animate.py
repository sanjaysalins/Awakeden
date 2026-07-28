"""Door episode sketch POC — step 3: animate all 12 spreads.
Camera-locked INVENT-NOTHING prompts, only named motion (flame, light, dust,
wash, leaves). Seedance everywhere; Kling for d11 (two figures + faces).
Durations: 4s default, 8s where the shot window needs it (d06/d09/d12).

  .venv\\Scripts\\python.exe poc_castbible_look/episode_door/_e3_animate.py
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
A.EPISODE = "POC_Door_Sketch"
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
    ("d01_hook", "seedance", 4,
     "Only: the lamp flame breathes gently, the warm light under the door "
     "breathes with it, faint dust drifts in the pool of light. The figure "
     "and his shadow hold perfectly still. Nothing else changes."),
    ("d02_record", "seedance", 4,
     "Only: the warm thread of light along the door's bottom gap breathes "
     "gently, faint dust drifts. The hands and scroll hold perfectly still. "
     "Nothing else changes."),
    ("d03_rehearsing", "seedance", 4,
     "Only: the lamp flame flickers softly, the warm rim light on the "
     "figure's mantle breathes with it. The figure holds perfectly still. "
     "Nothing else changes."),
    ("d04_answered", "seedance", 4,
     "The door does not move and does not open any further. Only: the blade "
     "of gold light through the gap brightens and dims gently, dust motes "
     "drift slowly in the beam. Nothing else changes."),
    ("d05_hiswords", "seedance", 4,
     "The face holds its exact expression -- no new mouth movement, no "
     "blink, no head turn. Only: the warm light on his face breathes "
     "gently, " + NOGLITTER + "faint dust drifts. Nothing else changes."),
    ("d06_verse", "seedance", 8,
     "The figure stays perfectly frozen like a statue, his extended hand "
     "holding its exact position, face unchanged. Only: the radiant gold "
     "light flooding past him pulses softly and evenly like a steady flame, "
     + NOGLITTER + "dust motes drift slowly through the light. Nothing else "
     "changes."),
    ("d07_exception", "seedance", 4,
     "The figure holds his exact turned-away pose, perfectly still. Only: a "
     "few drifted leaves stir faintly on the flagstones, the door's warm "
     "light-line breathes gently. Nothing else changes."),
    ("d08_toofargone", "seedance", 4,
     "The parchment scroll holds perfectly still. Only: the dark ink wash "
     "creeps VERY slowly inward from the spread's corners, gaining almost "
     "imperceptibly. Nothing else changes."),
    ("d09_nailed", "seedance", 8,
     "The nail and the scroll never move -- no strike, no impact, nothing "
     "is driven or moves into place. Only: a very slow gentle camera drift "
     "may occur, the parchment's curled edge trembles almost imperceptibly, "
     "the warm glow behind the beam breathes. Nothing else changes."),
    ("d10_opendoor", "seedance", 4,
     "The door and its hanging bar-latch do not move at all. Only: the "
     "radiant light beam from the doorway pulses softly and evenly, "
     + NOGLITTER + "dust drifts slowly through the beam. Nothing else "
     "changes."),
    ("d11_welcome", "kling", 5,
     "Both figures stay perfectly frozen the entire time -- no limbs move, "
     "no steps, no head turns, no faces change, no clothing shifts, and no "
     "new figures or objects appear. INVENT NOTHING -- both figures stay "
     "pixel-for-pixel identical to this exact image, holding their poses "
     "like statues. Only: the radiant gold light surrounding them pulses "
     "softly and evenly like a steady flame, " + NOGLITTER + "a few dust "
     "motes drift slowly through the light. Nothing else in the frame "
     "changes."),
    ("d12_landing", "seedance", 8,
     "The dove, the scroll, the gold thread, and the torn paper edges hold "
     "perfectly still. Only: the warm gold glow beneath the torn page "
     "breathes very slowly, " + NOGLITTER + "Nothing else changes."),
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
