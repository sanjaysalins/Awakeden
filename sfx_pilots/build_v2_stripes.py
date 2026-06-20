"""Ambient/SFX bed for the v2 A/B short 'With His Stripes' (Isaiah 53:5, Level A, no music, $0).

Standing rule (feedback-ambient-sfx-default). Theme = an unhealed wound -> the stripes that heal
-> the finished cross. A hollow desolate ache + deep sub-weight runs under the hook (the guilt that
won't close); a distant flock under 'all we like sheep'; a single muffled nail-strike lands near
'in his own body on the tree'; a soft veil-tear on 'it was finished at the cross'; a warm dawn +
reverent grace-swell carry the healing landing ('He has already closed... come to Him, and receive it').
Beat times from the assembly phrase board (cut ~70s).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\v2\pilot"
           r"\isaiah_53_5_with_his_stripes\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("hollow", "air_hollow_desolate", "loop",    0.0, 24.0, -34.0, fin=2.0, fout=5.0),                       # the wound that won't close
    layer("weight", "rumble_deep_sub",     "loop",   13.0, 17.0, -38.0, filt="lowpass=f=600", fin=3.0, fout=4.0), # under the stripes / wounds
    layer("flock",  "flock_sheep_field",   "loop",    7.0,  7.0, -37.0, filt="lowpass=f=3000", fin=2.0, fout=3.0),# 'all we like sheep'
    layer("nail",   "nail_strike_single",  "oneshot",34.8,  3.0, -25.0),                                          # 'in his own body on the tree'
    layer("veil",   "veil_tearing",        "oneshot",62.0,  3.0, -27.0, filt="lowpass=f=3500"),                   # 'it was finished at the cross' (74s timeline)
    layer("grace",  "score_reverent_grace","loop",   53.0, 21.0, -34.0, fin=3.0, fout=4.0),                       # the grace landing -> end
    layer("dawn",   "dawn_morning_warm",   "loop",   63.0, 11.0, -33.0, filt="lowpass=f=3200", fin=3.0),          # come to Him, receive it
]

if __name__ == "__main__":
    sfxlib.show_plan("v2 With His Stripes", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
