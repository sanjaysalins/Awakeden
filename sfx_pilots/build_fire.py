"""Ambient/SFX bed for 'The Fire Jesus Built' (John 21:15-17, $0 reuse).

Kept light because a bespoke ElevenLabs Cinematic-Orchestral SCORE is layered on top.
SFX = ambience + accents: a distant night-courtyard murmur at the denial fire, the charcoal
fire crackling through the shore scene (the fire He built), soft dawn sea-waves on the Galilee
shore, a single lamb under 'Feed my lambs', a closer crackle at the empty place by the fire, a
soft heavenly choir under the re-commission, and warm dawn into the close. Beat times from the
assembly phrase board (cut 59.02s).
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\16 The Fire Jesus Built\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("courtyard","crowd_murmur_distant","loop",     0.0,  4.0, -39.0, filt="lowpass=f=2400", fin=1.0, fout=2.0),  # the denial fire at night
    layer("fire",     "fire_crackling",      "loop",     1.5, 40.0, -37.0, fin=2.0, fout=4.0),                         # the charcoal fire He built
    layer("shore",    "sea_waves_shore",     "loop",     6.5, 11.0, -38.0, filt="lowpass=f=4000", fin=2.0, fout=3.0),  # dawn on the Galilee shore
    layer("lamb",     "flock_sheep_field",   "oneshot", 21.4,  3.2, -30.0),                                            # Feed my lambs
    layer("fire2",    "fire_crackling",      "oneshot", 43.4,  4.0, -32.0),                                            # the empty place by the fire
    layer("dawn",     "dawn_morning_warm",   "loop",    52.0,  7.0, -35.0, filt="lowpass=f=3400", fin=3.0),            # close — He is asking you now
]

if __name__ == "__main__":
    sfxlib.show_plan("The Fire Jesus Built", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
