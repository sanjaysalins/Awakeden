"""Ambient/SFX bed for '36 In No Wise Cast Out' (John 6:37, $0 reuse).

Light bed under a cinematic-orchestral score (ambience/accents only, no musical/choir pad).
A hollow cold air at the door of fear, a soft door opening as the welcome comes, and a warm
dawn into the open-door close ('the door was never locked'). Times from the 54.6s cut.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\36_In_No_Wise_Cast_Out\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("hollow", "air_hollow_desolate", "loop",     0.0, 26.0, -38.0, fin=2.0, fout=4.0),                  # the fear at the door
    layer("door",   "door_gate_creak",     "oneshot", 44.0,  3.5, -36.0, filt="lowpass=f=3000"),              # the door of welcome opens
    layer("dawn",   "dawn_morning_warm",   "loop",    47.0,  8.0, -35.0, filt="lowpass=f=3400", fin=3.0),     # the door was never locked
]

if __name__ == "__main__":
    sfxlib.show_plan("36 In No Wise Cast Out", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
