"""Ambient/SFX bed for 'The Empty Tomb' (John 20:8) — cluster-2, v5 retimed cut.

Arc: bleak pre-dawn garden wind under the hook and the dark tomb, Mary's running
feet on the dirt path, the two disciples on the stone path, then the hollow living
dark of the chamber for the linen/napkin evidence act (the heartbeat in the score
carries "No angel..."), a soft single footfall as John steps in, first dawn warmth
as belief lands ("his Lord was risen"), a low lamplit crackle for the Thomas room,
and full dawn warmth from the red-letter blessing through the CTA to the risen
close. SFX = ambience/accents only; the dark->grace score carries the emotion
(no choir pad). Beat times from the 79.07s v5 cut (+1.5s outro hold = 80.57s).
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\batches\cluster_02_resurrection"
           r"\empty_tomb_john208\visual\empty_tomb_john208_scored.mp4")
OUT = CUT.with_name("empty_tomb_john208_sfx.mp4")

LAYERS = [
    # pre-dawn garden — hook + "while it was still dark" (beats 1-4)
    layer("wind",    "wind_desert_bleak",    "loop",    0.0, 16.2, -40.0, fin=1.5, fout=1.5),
    # Mary runs to Peter and John (beat 3)
    layer("maryrun", "footsteps_dirt_approach", "oneshot", 9.5, 1.8, -34.0, fout=0.6),
    # "They ran." — the stone path to the tomb (beat 5)
    layer("theyran", "footsteps_stone",      "oneshot", 16.2, 2.4, -33.0, fout=0.8),
    # inside the chamber — linen + napkin evidence (beats 6-8)
    layer("hollow1", "air_hollow_desolate",  "loop",    18.7, 12.2, -38.0, filt="lowpass=f=3000", fin=1.2, fout=1.0),
    # John steps inside (beat 9) — one soft footfall into the hollow
    layer("johnin",  "footsteps_stone",      "oneshot", 30.9, 1.6, -38.0, fout=0.6),
    # "No angel... only the linen" — the held-breath stretch (score heartbeat lives here)
    layer("hollow2", "air_hollow_desolate",  "loop",    33.2, 11.2, -40.0, filt="lowpass=f=3000", fin=1.5, fout=2.0),
    # belief lands — "his Lord was risen" (beat 13): first warmth, then it recedes
    layer("dawn1",   "dawn_morning_warm",    "loop",    44.4, 8.8, -38.0, filt="lowpass=f=3400", fin=2.5, fout=2.0),
    # the Thomas room, lamplit, doors shut (beats 15-16)
    layer("lamp",    "fire_crackling",       "loop",    53.2, 8.2, -42.0, filt="lowpass=f=2800", fin=1.5, fout=1.5),
    # red-letter blessing -> CTA -> risen close (beats 17-20 + outro)
    layer("dawn2",   "dawn_morning_warm",    "loop",    61.4, 19.2, -36.0, filt="lowpass=f=3400", fin=3.0),
]

if __name__ == "__main__":
    sfxlib.show_plan("The Empty Tomb (John 20:8)", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
