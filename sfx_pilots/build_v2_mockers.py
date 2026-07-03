"""Ambient/SFX bed for the v2 consistency short 'The Mockers' Words' (Ps 22:7-8, Level A, $0).

Theme = the jeer that was foretold -> the King who would not come down. A distant scornful
crowd-murmur runs under the mockery; a low hollow weight under the enduring Christ; a single
soft shofar / held swell as the 'He could have come down' power-restraint turns; a warm dawn +
reverent grace-swell carry the landing ('to win you... come to the One who would not come down').
Beat times from the assembly phrase board (cut ~70s).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\v2\pilot"
           r"\mockers_words_ps22\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    # 2026-07-03: cue times remapped to the RE-CUT 78s phrase board (panel-fixed text;
    # was a 69s cut — the full Matt 27:43 + verbatim 27:40 taunt shifted every beat).
    layer("scorn",  "crowd_shout_mob",     "loop",    0.0, 23.0, -33.0, filt="lowpass=f=3200", fin=1.5, fout=5.0),  # the mockery: hook + David's taunt + bridge (0-23.3s)
    layer("murmur", "crowd_murmur_distant","loop",   22.0, 24.0, -35.0, filt="lowpass=f=2800", fin=3.0, fout=4.0),  # the recited taunts, both mocker quotes (23.7-46.3s)
    layer("weight", "rumble_deep_sub",     "loop",   24.0, 22.0, -38.0, filt="lowpass=f=600", fin=3.0, fout=4.0),   # the enduring Christ under the taunts
    layer("grace",  "score_reverent_grace","loop",   60.0, 18.0, -34.0, fin=3.0, fout=4.0),                          # 'He stayed under scorn... to win the scorners' -> end (P33 63.1s)
    layer("dawn",   "dawn_morning_warm",   "loop",   68.0, 10.0, -33.0, filt="lowpass=f=3200", fin=3.0),            # the unfinished script -> 'Turn, and come' (P36 68.3s)
]

if __name__ == "__main__":
    sfxlib.show_plan("v2 The Mockers' Words", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
