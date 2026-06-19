"""Ambient/SFX bed for Psalm 22 short #07 'The Body Foretold' (Level A, no music, $0).

Standing rule (feedback-ambient-sfx-default). The body theme: a low hollow desolation
under the whole dying-body description; a deep sub-weight as the body is poured out and
pulled out of joint; a distant murmur of onlookers as they look and stare; ONE soft nail
strike on 'bears the marks of one' (the nailed hand); warm dawn for the gospel landing.
Beat times from the assembly phrase board (narration 60.07s).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross"
           r"\v1\shorts\07_The_Body_Foretold\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("hollow", "air_hollow_desolate",   "loop",    0.0, 67.0, -34.0, fout=3.0),                          # desolation under the dying body (extended to 67s)
    layer("weight", "rumble_deep_sub",       "loop",   14.0, 26.0, -37.0, filt="lowpass=f=600",  fin=3.0, fout=4.0),  # poured out / out of joint
    layer("stare",  "crowd_murmur_distant",  "loop",   28.5,  9.5, -35.0, filt="lowpass=f=2000", fin=2.0, fout=2.5),  # they look and stare upon me
    layer("nail",   "nail_strike_single",    "oneshot", 43.9,  3.0, -26.0, filt="lowpass=f=2600"),            # bears the marks of one (nailed hand)
    layer("dawn",   "dawn_morning_warm",     "loop",   48.0, 19.0, -33.0, filt="lowpass=f=3000", fin=3.0),    # to bring you home / gospel landing (extended to 67s)
]

if __name__ == "__main__":
    sfxlib.show_plan("07 The Body Foretold", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
