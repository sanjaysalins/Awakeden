"""Ambient/SFX bed for the Drawing Office Two Goats POC (Leviticus 16).

Kept light -- a cinematic music_library SCORE is already muxed in; SFX here
is ambience/accent only. Arc: distant waiting-crowd murmur under the two
goats beat, desert wind rising under the departure insert, the veil_tearing
one-shot right on the tear, hollow air under the torn-open threshold.
Beat times from commission.json's real word-timed beat_plan.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible"
           r"\drawing_office\episodes\two_goats\cut_v2_scored.mp4")
OUT = CUT.with_name("cut_v3_sfx.mp4")

LAYERS = [
    layer("crowd",    "crowd_murmur_distant", "loop", 0.0,  19.8,  -33.0, fin=1.0, fout=3.0),   # the waiting people, outer court
    layer("wind",      "wind_desert_bleak",     "loop", 19.8, 5.0,   -30.0, fin=0.6, fout=2.0),   # the goat driven into the desert
    layer("tear",      "veil_tearing",          "oneshot", 52.5, 4.0, -22.0, fin=0.2, fout=1.5),  # the curtain itself
    layer("hollow",    "air_hollow_desolate",   "loop", 56.9, 13.5, -36.0, fin=1.5, fout=2.0),    # the torn-open threshold, held
]

if __name__ == "__main__":
    sfxlib.show_plan("Two Goats -- The Undivided (Drawing Office POC)", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
