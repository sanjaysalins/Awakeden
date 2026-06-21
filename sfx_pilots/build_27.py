"""Ambient/SFX bed for '27 A List of Dead Men' (Matt 16:13-17, $0 reuse).

Kept light because a bespoke ElevenLabs Cinematic-Orchestral SCORE is layered on top
(SFX = ambience/accents only, NEVER a musical/choir pad under the score).
Bed: a hollow desolate air under the 'list of dead men' hook + the question (the archival,
filed-away weight), a soft distant crowd as the crowd reaches for names from the past, and
a warm dawn into the living-One landing + the cross close. Beat times from the 59.03s cut.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\27 A List of Dead Men\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("hollow", "air_hollow_desolate", "loop",     0.0, 28.0, -38.0, fin=2.0, fout=4.0),                  # the list of dead men + the question
    layer("crowd",  "crowd_murmur_distant","loop",    17.5,  7.0, -41.0, filt="lowpass=f=3000", fin=1.5, fout=2.5),  # the crowd reaches for names
    layer("dawn",   "dawn_morning_warm",   "loop",    50.0,  9.0, -35.0, filt="lowpass=f=3400", fin=3.0),     # off the list, alive -> the cross
]

if __name__ == "__main__":
    sfxlib.show_plan("27 A List of Dead Men", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
