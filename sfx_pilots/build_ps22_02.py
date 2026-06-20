"""Ambient/SFX bed for Psalm 22 short #02 'The Mockers' Words' (Level A, no music, $0).

Standing rule (feedback-ambient-sfx-default). Theme = the mockery (Ps 22:7-8 / Matt 27:43):
a hollow base under it all; a distant jeering murmur through the taunt; two restrained mob swells
on the wagging-heads jeer and on 'let him deliver him, they sneered'; a low weight as He is not
delivered; a warm turn on 'it was love / He chose to stay with you'.
Anchor times from the captioned word board (cut 60.02s).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross"
           r"\v1\shorts\02_The_Mockers_Words\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("hollow", "air_hollow_desolate",  "loop",    0.0, 65.0, -35.0, fout=3.0),                          # hollow base
    layer("jeer",   "crowd_murmur_distant", "loop",    0.0, 32.0, -35.0, filt="lowpass=f=2000", fout=3.0),   # the mocking through the first half
    layer("taunt1", "crowd_shout_mob",      "oneshot",24.5,  5.0, -30.0, filt="lowpass=f=1800"),             # wagging/jeering + the live taunt (P11-P14, 24-31)
    layer("taunt2", "crowd_shout_mob",      "oneshot",38.3,  2.5, -31.0, filt="lowpass=f=1800"),             # 'let him deliver him', they sneered (P18 38.0)
    layer("weight", "rumble_deep_sub",      "loop",   41.0,  9.0, -38.0, filt="lowpass=f=600", fin=3.0, fout=4.0),  # he wasn't delivered (41-50)
    layer("love",   "dawn_morning_warm",    "loop",   53.5, 11.5, -33.0, filt="lowpass=f=3000", fin=3.0),    # it was love / chose to stay with you (53.5-65)
]

if __name__ == "__main__":
    sfxlib.show_plan("02 The Mockers' Words", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
