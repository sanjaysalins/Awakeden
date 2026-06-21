"""Ambient/SFX bed for '35 Manna Fulfilled' (John 6 / Exodus manna, $0 reuse).

Light bed under a cinematic-orchestral score (ambience/accents only, no musical/choir pad).
A bleak desert wind over the manna in the wilderness, a hollow desolate air through the cross
and the longing, and a warm dawn into the risen-Christ-at-the-tomb close. Times from the 65.2s cut.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\35_Manna_Fulfilled\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("wind",   "wind_desert_bleak",   "loop",     0.0, 24.0, -38.0, fin=2.0, fout=4.0),                  # manna in the wilderness
    layer("hollow", "air_hollow_desolate", "loop",    28.0, 20.0, -40.0, fin=3.0, fout=4.0),                  # the cross / the longing
    layer("dawn",   "dawn_morning_warm",   "loop",    57.0,  8.0, -35.0, filt="lowpass=f=3400", fin=3.0),     # risen at the tomb
]

if __name__ == "__main__":
    sfxlib.show_plan("35 Manna Fulfilled", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
