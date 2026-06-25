"""Ambient/SFX bed for '19 The Cliff of Rival Gods' (Matthew 16:13-15 — Caesarea Philippi).

Kept light because a cinematic music_library SCORE is layered on top (SFX = ambience/accents
only, NEVER a musical/choir pad under the score). Arc: a cold oppressive cliff of dead gods under
the hook — bleak wind over stone, hollow desolate air, a deep cave rumble (the Gates of Hades),
a pagan altar-fire crackle on the verdict-altar — then a WARM DAWN turn as the living Christ is
revealed and the cut lands on His face. Beat times from the 60.02s cut.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\19 The Cliff of Rival Gods\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("wind",   "wind_desert_bleak",  "loop", 0.0, 27.0, -34.0, fin=0.5, fout=6.0),                         # bleak cliff wind over the skyline of dead gods
    layer("hollow", "air_hollow_desolate","loop", 0.0, 24.0, -39.0, filt="lowpass=f=3200", fin=1.5, fout=5.0),  # the lifeless dead-gods air
    layer("deep",   "rumble_deep_sub",    "loop", 16.0, 10.0, -41.0, filt="lowpass=f=600", fin=2.0, fout=5.0),  # the Gates of Hades cave — deep heaving
    layer("altar",  "fire_crackling",     "loop", 15.0, 6.0,  -40.0, filt="lowpass=f=4200", fin=1.0, fout=2.0), # the verdict-altar flame
    layer("steps",  "footsteps_stone",    "loop", 11.0, 4.0,  -43.0, filt="lowpass=f=3000", fin=0.8, fout=1.5), # 'He marched them' to the cliff
    layer("dawn",   "dawn_morning_warm",  "loop", 30.0, 30.0, -36.0, filt="lowpass=f=3400", fin=7.0),           # the living Christ -> hero close -> 'open my eyes to your Son'
]

if __name__ == "__main__":
    sfxlib.show_plan("19 The Cliff of Rival Gods", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
