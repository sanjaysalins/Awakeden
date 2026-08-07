"""Seed of the Woman LONG -- animate stage. Spreads 1-5 promoted from the
POC30 process-validation test (memory `day-of-atonement-retro-learnings`);
extend JOBS as the full plan is authored. Reuses the shared
driver from poc_comic_page/_animate_piece1_v2.py (run_job_with_fallback),
same pattern day_of_atonement/_s4_animate.py follows -- fix #9 (check the
sibling episode's real script chain, don't assume a generic skill applies).
Only 2 clips for this tiny excerpt: s02 (multi-figure -> Kling, per the
locked comic-grid cost-tiering) and s04 (calm single light-presence ->
Seedance).

  .venv\\Scripts\\python.exe poc_living_sketchbook/seed_of_the_woman/_s4_animate.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "poc_comic_page"))
import _animate_piece1_v2 as driver  # noqa: E402

HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
driver.OUT = HERE / "clips"
driver.OUT.mkdir(parents=True, exist_ok=True)
driver.EPISODE = "SeedOfTheWoman"

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the "
        "paper texture, torn edges, and every sketch line hold perfectly "
        "still. ")
PAGE = ("A finished ink-and-watercolor drawing on an aged sketchbook page, "
        "filmed as a perfectly still page under steady light. The framing "
        "stays fixed and locked for the entire clip. The drawing is "
        "finished and dry: every figure, face, hand, and object in it is "
        "ink on paper and stays exactly as drawn from the first frame to "
        "the last. ")

JOBS = [
    ("s02_the_hiding", "kling", 5,
     PAGE + LOCK +
     "Both figures hold their exact crouched positions and postures, "
     "perfectly still -- neither turns, stands, or shifts weight. Only: "
     "the surrounding leaves and ferns stir very slightly in a light "
     "breeze, and the light breathes very gently. Nothing else changes."),
    ("s04_god_walking", "seedance", 4,
     PAGE + LOCK +
     "The trees, canopy, and ground hold their exact shapes and "
     "positions, perfectly still -- no figure of any kind ever appears. "
     "Only: the golden light drifts and breathes gently through the "
     "canopy, and a few motes of dust/pollen drift slowly in the beams. "
     "Nothing else changes."),
]


def main():
    for name, provider, duration, prompt in JOBS:
        out = driver.OUT / f"{name}.mp4"
        if out.exists():
            print(f"[skip] {name}")
            continue
        still = STILLS / f"{name}.png"
        ok, used = driver.run_job_with_fallback(name, provider, still, "16:9", prompt, duration=duration)
        print(f"  -> {'ok' if ok else 'FAILED'} (provider={used})")


if __name__ == "__main__":
    main()
