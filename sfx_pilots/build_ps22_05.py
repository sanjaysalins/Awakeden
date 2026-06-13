"""Ambient/SFX bed for Psalm 22 short #05 'He Hath Done This' (Level A, no music, $0).

Standing rule (feedback-ambient-sfx-default): every finished clip gets a forced-aligned
ambient bed from sound_library, sidechain-ducked under the voice. Beat times from the
assembly phrase board (narration 43.91s).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross"
           r"\v1\shorts\05_He_Hath_Done_This\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

# He Hath Done This — the finished work. Hollow stillness through the finished hour;
# a low weight under "It is finished" (24.58); a soft veil-tear as the torn veil lands
# "a finished work" (32.80); warm dawn under the landing / bare-cross-at-dawn (34.6-43.9).
LAYERS = [
    layer("still", "air_hollow_desolate", "loop",    0.0, 43.9, -34.0, fout=3.0),
    layer("weight", "rumble_deep_sub",    "loop",   23.8,  5.4, -33.0, fin=1.5, fout=2.5),  # "It is finished"
    layer("veil",  "veil_tearing",        "oneshot", 32.3,  4.0, -27.0),                     # torn veil -> "a finished work"
    layer("dawn",  "dawn_morning_warm",   "loop",   35.4,  8.5, -34.0, filt="lowpass=f=3000", fin=3.0),  # come home
]

if __name__ == "__main__":
    sfxlib.show_plan("05 He Hath Done This", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
