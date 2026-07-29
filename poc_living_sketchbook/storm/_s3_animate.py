"""Storm episode — step 3: animate all 13 spreads. Camera-locked INVENT-
NOTHING prompts, named ambient motion only -- EXCEPT s06, the one designed
ACTING spread (SKILL.md SS4): the fisherman's hand completes a grip then
holds. s09/s10 are the multi-stage hard-cut pair (storm -> calm) -- BOTH get
ambient-only motion; the CUT between the two stills carries the event, not
in-clip animation (SKILL.md SS3). Kling for multi-figure/action/faces-under-
pressure (s03, s06, s09); Seedance everywhere else.

  .venv\\Scripts\\python.exe poc_living_sketchbook/storm/_s3_animate.py
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
A.EPISODE = "LS_Storm"
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
    ("s01_waves", "seedance", 4,
     "The boat holds its exact position and angle, it does not rock or pitch "
     "further. Only: the black storm clouds churn slowly overhead, spray "
     "continues flying off the near wave crest. Nothing else changes."),

    ("s02_water", "seedance", 4,
     "The rope and the boat planks hold perfectly still. Only: the dark "
     "water sloshes gently back and forth past the feet, a little spray "
     "drifts in the air. Nothing else changes."),

    ("s03_screaming", "kling", 5,
     "All three figures stay frozen in their exact braced, straining poses -- "
     "no new grip, no stepping, no change of expression. INVENT NOTHING new. "
     "Only: the towering wave behind them continues to curl and break, spray "
     "flies past. Nothing else in the frame changes."),

    ("s04_asleep", "seedance", 8,
     "Jesus holds his exact sleeping pose, perfectly still -- no stirring, "
     "no shifting. Only: the small pocket of warm light around him breathes "
     "gently, " + NOGLITTER + "the dark water beyond the rail continues its "
     "heavy swell. Nothing else changes."),

    ("s05_hands", "seedance", 4,
     "The hand holds its exact open, relaxed position. Only: the storm "
     "water blurred beyond the rail continues its motion softly out of "
     "focus. Nothing else changes."),

    ("s06_shaken", "kling", 5,
     "The fisherman's hand, already reaching toward the shoulder, completes "
     "ONE smooth firm grip onto Jesus's shoulder within the first two "
     "seconds, then holds that exact grip perfectly still for the rest of "
     "the clip -- no shaking, no repeated motion, no further gripping. "
     "Jesus's face and body do not move or react at all. INVENT NOTHING "
     "beyond this one completed grip. Only: storm spray continues flying "
     "past in the background. Nothing else in the frame changes."),

    ("s07_eyes", "seedance", 4,
     "Jesus's face holds its exact expression, eyes already open -- no "
     "further blink, no head turn, no new movement. Only: the faint cold "
     "storm light on one side of his face breathes very gently. Nothing "
     "else changes."),

    ("s08_verse", "seedance", 8,
     "Jesus holds his exact seated, mid-speech pose and expression -- no "
     "further mouth movement, no gesture change. Only: the storm in soft "
     "focus behind him continues faintly, the warm lamplight on his face "
     "breathes gently, " + NOGLITTER + "Nothing else changes."),

    ("s09_rebuke", "kling", 5,
     "Jesus stays perfectly frozen like a statue in his exact standing pose, "
     "arm already extended toward the storm -- no further gesture, no step, "
     "no change of expression. The disciples below stay frozen, watching. "
     "INVENT NOTHING new. Only: the towering dark wave and torn storm "
     "clouds continue their motion around the boat. Nothing else in the "
     "frame changes."),

    ("s10_calm", "seedance", 4,
     "Jesus and the disciples hold their exact positions, perfectly still -- "
     "no movement, no gesture. Only: the now-glassy sea breathes with a very "
     "gentle ripple, the warm light breaking through the clearing clouds "
     "pulses softly and evenly, " + NOGLITTER + "Nothing else changes."),

    ("s11_exactly", "seedance", 4,
     "The boat holds its exact position on the water. Only: the calm sea's "
     "surface breathes with a very gentle ripple, the warm gold light "
     "through the parting clouds pulses softly and evenly, " + NOGLITTER +
     "Nothing else changes."),

    ("s12_knees", "seedance", 8,
     "The fisherman holds his exact seated pose and searching expression, "
     "perfectly still -- no head turn, no blink. Only: the calm water at "
     "his ankles breathes with a very gentle ripple, the soft warm light on "
     "his face breathes gently. Nothing else changes."),

    # Seedance invented a trail extending past the tear's boundary here on
    # the first render -- a real content failure on the most sensitive
    # spread in the episode. Fix per the project's proven pattern (Jericho's
    # blood-pool bug): switch tier to Kling AND lock the boundary explicitly
    # -- pixel-identical, no drip-adjacent vocabulary at all.
    ("s13_landing", "kling", 10,
     "The torn edge, the blue wash ring, the golden light, the silhouette "
     "figure, and the small boat all hold their EXACT current shape and "
     "outer boundary, pixel-for-pixel identical, for the entire clip -- "
     "nothing grows, extends, or spreads beyond where it already is. INVENT "
     "NOTHING new. Only: the golden light within the tear breathes very "
     "slightly brighter and dimmer, a steady even glow -- " + NOGLITTER +
     "Nothing else in the frame moves."),
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
