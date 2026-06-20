"""Ambient/SFX bed for Psalm 22 short #08 'I Thirst' (Level A, no music, $0).

Standing rule (feedback-ambient-sfx-default). Theme = thirst -> living water (Ps 22:15 / John 19:28).
A dry desert wind runs under the whole; a dry hollow desolation + deep sub-weight under the psalm's
dying images (potsherd / tongue cleaving / dust of death); then WATER finally enters as the
conviction turns — a well/spring under 'the One who made every river... living water... drink and
never thirst'; a warm dawn lands on 'that water is Himself'. The bed walks thirst into living water.
Beat times from the assembly phrase board (cut 67.06s).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross"
           r"\v1\shorts\08_I_Thirst\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("wind",   "wind_desert_bleak",   "loop",    0.0, 70.9, -34.0, fout=3.0),                          # parched wilderness under it all
    layer("hollow", "air_hollow_desolate", "loop",   13.0, 21.0, -37.0, filt="lowpass=f=3000", fin=3.0, fout=4.0),  # the dying-body images (13->34)
    layer("dust",   "rumble_deep_sub",     "loop",   20.0, 14.0, -38.0, filt="lowpass=f=600", fin=3.0, fout=4.0),   # the dust of death (20->34)
    layer("water",  "river_well_water",    "loop",   44.0, 20.0, -32.0, filt="lowpass=f=2500", fin=2.5, fout=3.0),  # every river / living water / drink (44->64)
    layer("dawn",   "dawn_morning_warm",   "loop",   62.0,  8.9, -33.0, filt="lowpass=f=3000", fin=3.0),    # that water is Himself (62->71)
]

if __name__ == "__main__":
    sfxlib.show_plan("08 I Thirst", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
