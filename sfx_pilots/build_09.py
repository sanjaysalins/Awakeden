"""Ambient/SFX bed for '09 The Father Who Ran' (Luke 15:20, prodigal).

Kept light because a bespoke ElevenLabs Cinematic-Orchestral SCORE is layered on top
(SFX = ambience/accents only, NEVER a musical/choir pad under the score).
Bed: a bleak dusty-road wind under the hook (the long road home + the son trudging),
the father's running footsteps on dirt as the hook turns, then a warm dawn rising from
the embrace through the conviction and the landing (homecoming -> the running of God).
Beat times from the 60.02s cut.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\09 The Father Who Ran\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("road",  "wind_desert_bleak",       "loop", 0.0, 22.0, -39.0, fin=2.0, fout=5.0),                       # the long road home + the son walking slow
    layer("run",   "footsteps_dirt_approach", "loop", 3.0,  7.0, -43.0, filt="lowpass=f=3000", fin=1.0, fout=2.5),  # the father runs
    layer("dawn",  "dawn_morning_warm",        "loop", 26.0, 34.0, -35.0, filt="lowpass=f=3400", fin=5.0),         # the embrace -> conviction -> landing warmth
]

if __name__ == "__main__":
    sfxlib.show_plan("09 The Father Who Ran", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
