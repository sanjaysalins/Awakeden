"""Ambient/SFX bed for Psalm 22 short #04 'Declared To The Brethren' (Level A, no music, $0).

Standing rule (feedback-ambient-sfx-default). Theme = the resurrection turn (Ps 22:22 / Heb 2:12):
the cut moves from the grave to praise to the risen Christ to family. A hollow grave-tone opens and
fades as the psalm turns; a warm dawn carries the whole resurrection arc; a reverent grace bed swells
on 'declare thy name... praise thee in the congregation'; a warm gathered murmur on the brethren/family
beat; a grace bed lands on 'calling you into that family'. The warmest of the four.
Anchor times from the captioned word board (cut 58.31s).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross"
           r"\v1\shorts\04_Declared_To_The_Brethren\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("grave",    "air_hollow_desolate",  "loop",    0.0, 14.0, -35.0, fout=4.0),                          # stop at the cross / grave
    layer("turn",     "dawn_morning_warm",    "loop",   12.0, 46.0, -33.0, filt="lowpass=f=3000", fin=4.0),    # anguish -> praise -> risen -> family
    layer("praise",   "score_reverent_grace", "loop",   16.0, 16.0, -33.0, fin=3.0, fout=4.0),                 # declare thy name / praise in the congregation
    layer("gathered", "crowd_murmur_distant", "loop",   42.0,  9.0, -37.0, filt="lowpass=f=2200", fin=2.0, fout=3.0),  # brethren / brothers / family
    layer("calling",  "score_reverent_grace", "loop",   50.0,  8.3, -34.0, fin=3.0),                           # calling you into that family
]

if __name__ == "__main__":
    sfxlib.show_plan("04 Declared To The Brethren", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
