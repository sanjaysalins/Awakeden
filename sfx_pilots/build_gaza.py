"""Ambient/SFX bed for 'The Question on the Gaza Road' (Isaiah 53 / Acts 8, $0 reuse).

Kept light because a bespoke ElevenLabs Cinematic-Orchestral SCORE is layered on top.
SFX = ambience: a dry desert wind on the Gaza road under the hook, a soft distant lamb under
the silent-lamb line, a hollow desolate air under the wounds + the question, a soft heavenly
choir as the silent Lamb is named Jesus in the landing, and warm dawn into 'come to Him'.
Beat times from the assembly phrase board (cut 61.96s).
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\25 The Question on the Gaza Road\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("desert", "wind_desert_bleak",   "loop",     0.0, 13.0, -38.0, fin=2.0, fout=4.0),                   # the Gaza road
    layer("lamb",   "flock_sheep_field",   "oneshot", 10.5,  6.0, -33.0, filt="lowpass=f=4000"),               # the silent lamb
    layer("hollow", "air_hollow_desolate", "loop",    17.0, 18.0, -39.0, fin=3.0, fout=4.0),                   # the wounds + the question
    layer("choir",  "heavenly_choir_soft", "loop",    39.5, 15.0, -34.0, fin=3.0, fout=4.0),                   # the silent Lamb named Jesus
    layer("dawn",   "dawn_morning_warm",   "loop",    54.0,  8.0, -34.0, filt="lowpass=f=3400", fin=3.0),      # come to Him
]

if __name__ == "__main__":
    sfxlib.show_plan("The Question on the Gaza Road", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
