"""Ambient/SFX bed for the v2 reuse+music test 'The One They Pierced' (Zech 12:10, $0).

Kept light because a bespoke ElevenLabs SCORE is layered on top. SFX = event accents +
ambience only: a low spear-impact at the hook, a hollow weight under the piercing, a soft
choir at 'grace poured out', a distant murmur as the people look-and-mourn, warm dawn on
'look at Him and live'. Beat times from the assembly phrase board (cut ~70s).
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\v2\pilot"
           r"\zechariah_12_10_pierced\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("spear",  "impact_low_boom",     "oneshot", 1.2,  3.0, -26.0, filt="lowpass=f=1800"),               # the spear
    layer("hollow", "air_hollow_desolate", "loop",    0.0, 20.0, -36.0, fin=2.0, fout=5.0),                    # the death/piercing
    layer("weight", "rumble_deep_sub",     "loop",   17.0, 16.0, -39.0, filt="lowpass=f=600", fin=3.0, fout=4.0),
    layer("choir",  "heavenly_choir_soft", "loop",   45.0, 14.0, -35.0, fin=3.0, fout=4.0),                    # grace poured out
    layer("murmur", "crowd_murmur_distant","loop",   52.0,  9.0, -37.0, filt="lowpass=f=2600", fin=2.0, fout=3.0), # they look and mourn
    layer("dawn",   "dawn_morning_warm",   "loop",   62.0,  8.0, -34.0, filt="lowpass=f=3200", fin=3.0),       # look at Him and live
]

if __name__ == "__main__":
    sfxlib.show_plan("v2 The One They Pierced", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
