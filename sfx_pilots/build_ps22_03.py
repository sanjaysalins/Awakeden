"""Ambient/SFX bed for Psalm 22 short #03 'The Forsaken Cry' (Level A, no music, $0).

Standing rule (feedback-ambient-sfx-default). Theme = forsakenness, dark -> light (Ps 22:1 / Matt 27:46):
a prominent hollow desolation; a deep dark sub-weight through the two forsaken cries; a low thunder
roll for the darkness at the ninth hour; then the turn to a warm dawn + a reverent grace bed as the
way home opens 'from the dark'. The bed walks the dark-to-light arc of the cut.
Anchor times from the captioned word board (cut 51.84s).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross"
           r"\v1\shorts\03_The_Forsaken_Cry\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("desolation", "air_hollow_desolate", "loop",    0.0, 51.8, -33.0, fout=4.0),                          # forsakenness
    layer("dark",       "rumble_deep_sub",     "loop",    0.0, 34.0, -37.0, filt="lowpass=f=600", fout=5.0),    # the dark weight under the cries
    layer("ninth",      "thunder_low_roll",    "oneshot",19.8,  6.0, -30.0, filt="lowpass=f=1500"),             # darkness at the ninth hour (before Jesus' cry 21.6)
    layer("dawn",       "dawn_morning_warm",   "loop",   42.5,  9.3, -32.0, filt="lowpass=f=3000", fin=3.5),    # forsaken so you never will be / way home open
    layer("grace",      "score_reverent_grace","loop",   44.0,  7.8, -35.0, fin=3.0, fout=2.0),                 # he opened it from the dark
]

if __name__ == "__main__":
    sfxlib.show_plan("03 The Forsaken Cry", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
