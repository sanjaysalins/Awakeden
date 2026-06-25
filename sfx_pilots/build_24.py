"""Ambient/SFX bed for '24 The Answer Was a Gift' (Matthew 16:15-17 — Peter's confession).

Light bed under a cinematic music_library score (SFX = ambience/accents only, no choir/musical pad).
Arc: a clamoring crowd + bleak cliff wind under the poll/hook, a hollow cave accent, then a WARM
DAWN turn as the Father reveals the Son (the heavens-torn-open / the gift / the grace / the hero
close), with a fire-crackle accent under the chariots-of-fire OT echo. Beat times from the 59.04s cut.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\24 The Answer Was a Gift\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("crowd", "crowd_murmur_distant", "loop", 0.0, 19.0, -36.0, fin=0.5, fout=4.0),                         # the poll — a clamoring multitude
    layer("wind",  "wind_desert_bleak",    "loop", 0.0, 19.0, -39.0, fin=0.5, fout=4.0),                         # the bleak Caesarea cliff
    layer("hollow","air_hollow_desolate",  "loop", 8.0, 9.0,  -41.0, filt="lowpass=f=3000", fin=1.5, fout=3.0),  # the Gates of Hades cave
    layer("dawn",  "dawn_morning_warm",    "loop", 24.0, 35.0,-36.0, filt="lowpass=f=3400", fin=5.0),            # the reveal -> gift -> grace -> hero
    layer("fire",  "fire_crackling",       "loop", 41.5, 6.0, -40.0, filt="lowpass=f=4200", fin=1.0, fout=2.0),  # the chariots of fire (OT echo)
]

if __name__ == "__main__":
    sfxlib.show_plan("24 The Answer Was a Gift", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
