"""Ambient/SFX bed for '28 What Manner of Man' (Matthew 8:23-27 — Jesus calms the storm).

Kept light because a cinematic music_library SCORE is layered on top (SFX = ambience/accents
only, NEVER a musical/choir pad under the score). Arc: a heavy tempest under the hook (crashing
sea, low thunder, the deep, the boat straining), the storm draining out at the rebuke / the great
calm, then a gentle calmed sea + a warm dawn through the marvel and the landing on Christ.
Beat times from the 61.05s cut.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\28 What Manner of Man\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("tempest", "sea_waves_shore",  "loop", 0.0, 26.0, -33.0, fin=0.5, fout=6.0),                       # the storm — crashing sea
    layer("thunder", "thunder_low_roll", "loop", 1.0, 20.0, -38.0, fin=1.0, fout=5.0),                       # low rolling thunder
    layer("deep",    "rumble_deep_sub",  "loop", 0.0, 24.0, -41.0, filt="lowpass=f=600", fin=2.0, fout=6.0),  # the deep heaving
    layer("boat",    "boat_creak_oars",  "loop", 3.0, 20.0, -43.0, filt="lowpass=f=3000", fin=1.5, fout=4.0), # the ship straining
    layer("calm",    "sea_waves_shore",  "loop", 30.0, 31.0, -44.0, filt="lowpass=f=2600", fin=6.0),          # the great calm — gentle wash
    layer("dawn",    "dawn_morning_warm","loop", 40.0, 21.0, -37.0, filt="lowpass=f=3400", fin=7.0),          # the marvel -> the Lord -> His name is Jesus
]

if __name__ == "__main__":
    sfxlib.show_plan("28 What Manner of Man", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
