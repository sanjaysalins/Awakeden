"""Ambient/SFX bed for '34 The Hunger Bread Can't Fill' (John 6, $0 reuse).

Light bed under a cinematic-orchestral score (SFX = ambience/accents only, no musical/choir pad).
A hollow desolate air under the laden-but-empty feast + the grasping for coins/fruit, a soft
diegetic bread-break at the breaking-of-bread beat, and a warm dawn into the Bread-of-Life close.
Beat times from the 52.89s cut.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\34_The_Hunger_Bread_Cant_Fill\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("hollow", "air_hollow_desolate", "loop",     0.0, 30.0, -38.0, fin=2.0, fout=4.0),                  # the unfilled hunger
    layer("bread",  "bread_tearing",       "oneshot", 23.5,  3.0, -32.0),                                     # the breaking of bread
    layer("dawn",   "dawn_morning_warm",   "loop",    45.0,  8.0, -35.0, filt="lowpass=f=3400", fin=3.0),     # the Bread of Life
]

if __name__ == "__main__":
    sfxlib.show_plan("34 The Hunger Bread Can't Fill", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
