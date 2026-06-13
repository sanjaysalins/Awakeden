"""Ambient/SFX bed for Psalm 22 short #06 'The Ends of the Earth' (Level A, no music, $0).

Standing rule (feedback-ambient-sfx-default). The global reach of the cross: the wind of
a vast world; a shofar as the song throws its arms open to every nation; a low murmur of
many peoples turning; the sea as the gospel goes out; warm dawn for the worldwide turning.
Beat times from the assembly phrase board (narration 61.82s).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross"
           r"\v1\shorts\06_The_Ends_Of_The_Earth\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("world",  "wind_desert_bleak",     "loop",    0.0, 61.8, -34.0, fout=3.0),
    layer("nations","shofar_blast",          "oneshot", 7.8,  6.0, -28.0, filt="lowpass=f=2500"),  # song opens to every nation
    layer("peoples","crowd_murmur_distant",  "loop",   14.5, 26.0, -35.0, fin=2.5, fout=3.0),       # kindreds -> nation after nation
    layer("sea",    "sea_waves_shore",       "loop",   29.0,  9.5, -35.0, filt="lowpass=f=2200", fin=2.0, fout=2.5),  # gospel goes out
    layer("dawn",   "dawn_morning_warm",     "loop",   47.0, 14.8, -34.0, filt="lowpass=f=3000", fin=3.0),  # worldwide turning / come home
]

if __name__ == "__main__":
    sfxlib.show_plan("06 The Ends of the Earth", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
