"""Ambient/SFX bed for '31 The Light You Can Stand In' (John 8:11-12).

Kept light because a bespoke ElevenLabs Cinematic-Orchestral SCORE is layered on top
(SFX = ambience/accents only, NEVER a musical/choir pad under the score).
Bed: a tense low court murmur under the hook (the ring of accusers, raised stones),
the accusers' footsteps filing out across the temple stone (oldest first), then the
hush of the emptied court (the woman alone with Jesus in the light), warming into a
risen dawn through "Neither do I condemn thee" -> "I am the light of the world" -> the
landing on the open-armed risen Christ ("where the guilty get to stand").
Beat times from the 59.02s cut.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\31 The Light You Can Stand In\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("court",  "crowd_murmur_distant", "loop",  0.0,  9.0, -40.0, fin=0.5, fout=3.5),                      # the ring of accusers, raised stones
    layer("leave",  "footsteps_stone",      "loop",  5.0,  8.0, -44.0, filt="lowpass=f=3000", fin=1.5, fout=3.0),  # accusers file out, oldest first
    layer("hush",   "air_hollow_desolate",  "loop", 12.0, 18.0, -42.0, fin=4.0, fout=4.0),                      # the emptied court, woman alone in the light
    layer("dawn",   "dawn_morning_warm",    "loop", 28.0, 40.0, -36.0, filt="lowpass=f=3400", fin=6.0),         # pardon -> go and sin no more -> follow into light of life -> risen close
]

if __name__ == "__main__":
    sfxlib.show_plan("31 The Light You Can Stand In", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
