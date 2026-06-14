"""Ambient/SFX bed for Psalm 22 short #01 'The Crucifixion Foretold' (Level A, no music, $0).

Standing rule (feedback-ambient-sfx-default). Theme = the garments gambled (Ps 22:18 / John 19:24):
a low hollow gravity under the prophecy; deep weight as the dying man is poured out; the clink of
coins/lots on 'cast lots upon my vesture' and again on the soldiers' lots and the rolled dice; a
distant soldier-crowd at the cross; a warm turn on the landing (the plan / to win you back).
Anchor times from the captioned word board (cut 64.14s).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross"
           r"\v1\shorts\01_The_Crucifixion_Foretold\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("hollow", "air_hollow_desolate",  "loop",    0.0, 64.1, -34.0, fout=3.0),                          # gravity of the cross
    layer("weight", "rumble_deep_sub",      "loop",   14.0, 22.0, -38.0, filt="lowpass=f=600", fin=3.0, fout=4.0),  # life poured out
    layer("lots",   "coins_clinking",       "oneshot",25.2,  5.0, -27.0, filt="lowpass=f=3000"),             # cast lots upon my vesture (25.4)
    layer("crowd",  "crowd_murmur_distant", "loop",   33.0,  7.0, -35.0, filt="lowpass=f=2200", fin=2.0, fout=2.5),  # John at the cross / soldiers
    layer("dice",   "coins_clinking",       "oneshot",56.5,  3.0, -26.0, filt="lowpass=f=3000"),             # they rolled dice (56.9)
    layer("dawn",   "dawn_morning_warm",    "loop",   50.0, 14.1, -33.0, filt="lowpass=f=3000", fin=3.0),    # it was the plan / to win you back
]

if __name__ == "__main__":
    sfxlib.show_plan("01 The Crucifixion Foretold", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
