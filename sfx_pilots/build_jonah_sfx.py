"""Ambient/SFX bed for 'The Sign of Jonah' (Jonah 1-2 + Matt 12:40) — cluster-2 pilot.

Arc: raging sea + thunder + ship creak under the storm act (the storm ceases only
when Jonah goes over), a deep sub plunge at overboard, the hollow living dark of
the belly (spanning the Matt 12:40 bar into the tomb — the deep and the grave are
the same room in this piece), temple-court murmur under the scribes, bleak wind
through the burial, a single STONE ROLL under the HE-ROSE border-break, then warm
dawn through mercy -> turn -> risen close. SFX = ambience/accents only; the
dark->grace score carries the emotion (no choir pad). Beat times from the 69.52s cut.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\batches\cluster_02_resurrection"
           r"\sign_of_jonah_matt1240\visual\sign_of_jonah_matt1240_scored.mp4")
OUT = CUT.with_name("sign_of_jonah_matt1240_sfx.mp4")

LAYERS = [
    # the storm act (Jonah 1) — sea rage + thunder + the groaning ship
    layer("sea",     "sea_waves_shore",     "loop",    0.0, 21.4, -35.0, fin=0.3, fout=2.5),
    layer("thunder1","thunder_low_roll",    "oneshot", 0.3, 4.0,  -30.0, fout=2.0),
    layer("thunder2","thunder_low_roll",    "oneshot", 14.7, 4.0, -33.0, fout=2.5),
    layer("creak",   "boat_creak_oars",     "loop",    5.3, 13.2, -40.0, fin=1.0, fout=2.0),
    # overboard — the deep swallows him (storm ceases with him, Jonah 1:15)
    layer("plunge",  "rumble_deep_sub",     "oneshot", 18.5, 4.5, -32.0, fin=0.2, fout=2.5),
    # the belly / the grave — one hollow room from the fish to the tomb
    layer("hollow1", "air_hollow_desolate", "loop",    21.4, 4.1, -38.0, filt="lowpass=f=3000", fin=1.2, fout=1.0),
    layer("murmur",  "crowd_murmur_distant","loop",    25.5, 5.4, -38.0, fin=0.8, fout=1.2),   # scribes demand
    layer("hollow2", "air_hollow_desolate", "loop",    30.9, 18.6,-38.0, filt="lowpass=f=3000", fin=1.5, fout=2.0),
    layer("wind",    "wind_desert_bleak",   "loop",    44.4, 9.0, -41.0, fin=2.0, fout=1.5),   # the burial
    # HE ROSE — the stone (border-break at 53.4)
    layer("stone",   "stone_roll_tomb",     "oneshot", 53.3, 2.2, -27.0, fout=0.8),
    # resurrection warmth through mercy -> turn -> risen close
    layer("dawn",    "dawn_morning_warm",   "loop",    53.8, 15.7,-36.0, filt="lowpass=f=3400", fin=3.0),
]

if __name__ == "__main__":
    sfxlib.show_plan("The Sign of Jonah (Matt 12:40)", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
