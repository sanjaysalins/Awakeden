"""Ambient/SFX bed for the v2 consistency short 'The Mockers' Words' (Ps 22:7-8, Level A, $0).

Theme = the jeer that was foretold -> the King who would not come down. A distant scornful
crowd-murmur runs under the mockery; a low hollow weight under the enduring Christ; a single
soft shofar / held swell as the 'He could have come down' power-restraint turns; a warm dawn +
reverent grace-swell carry the landing ('to win you... come to the One who would not come down').
Beat times from the assembly phrase board (cut ~70s).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\v2\pilot"
           r"\mockers_words_ps22\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("scorn",  "crowd_shout_mob",     "loop",    0.0, 20.0, -33.0, filt="lowpass=f=3200", fin=1.5, fout=5.0),  # the mockery
    layer("murmur", "crowd_murmur_distant","loop",   18.0, 22.0, -35.0, filt="lowpass=f=2800", fin=3.0, fout=4.0),  # the recited taunt
    layer("weight", "rumble_deep_sub",     "loop",   12.0, 16.0, -38.0, filt="lowpass=f=600", fin=3.0, fout=4.0),   # the enduring Christ
    layer("shofar", "shofar_blast",        "oneshot",45.4,  4.0, -28.0, filt="lowpass=f=2600"),                     # He could have come down (held power)
    layer("grace",  "score_reverent_grace","loop",   55.0, 15.0, -34.0, fin=3.0, fout=4.0),                          # the King who stayed
    layer("dawn",   "dawn_morning_warm",   "loop",   62.0,  8.0, -33.0, filt="lowpass=f=3200", fin=3.0),            # come to Him
]

if __name__ == "__main__":
    sfxlib.show_plan("v2 The Mockers' Words", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
