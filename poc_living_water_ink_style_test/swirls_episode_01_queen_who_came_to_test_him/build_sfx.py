"""Ambient/SFX bed for episode 1, "The Queen Who Came to Test Him" (first
time this stage has been run on a swirls-of-life episode -- reuses the main
engine's own sfxlib.py mix pattern, $0, reuse-only from sound_library).

Layer map keyed to the locked unit timeline (from the final assembly's own
held durations): front 0-4.33, f01 4.33-12.37 (desert ridge, her doubt),
f02 12.37-20.70 (Solomon's hall), f03 20.70-29.00 (her confession, same
hall), f04 29.00-37.33 (homeward desert), f05 37.33-42.37 (Jerusalem
courtyard), f06 42.37-51.40 (the gospel pivot), f07 51.40-63.33 (Jesus'
direct address), back 63.33-70.03 (empty ridge + the 5s landing hold).

Design: two matched desert-wind bookends (open journey / homeward /
dusk landing) frame a quiet indoor hall-air bed for the throne-room pages,
one coin-clink accent on the gifts, a faint distant-crowd bed under the
courtyard scribes, and a single soft choir swell timed to the gospel claim
itself ("a greater than Solomon is here") -- not on her own confession, so
the two emotional beats don't compete for the same device.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "sfx_pilots"))
import sfxlib  # noqa: E402
from sfxlib import layer  # noqa: E402

CUT = HERE / "THE_QUEEN_WHO_CAME_TO_TEST_HIM_final.mp4"
OUT = HERE / "THE_QUEEN_WHO_CAME_TO_TEST_HIM_final_sfx.mp4"

LAYERS = [
    layer("desert_open", "wind_desert_bleak",     "loop",     0.0, 12.5, -38.0, fin=2.5, fout=1.5),
    layer("hall_air",     "air_hollow_desolate",   "loop",    12.0, 17.5, -42.0, fin=2.0, fout=2.0),
    layer("gold",         "coins_clinking",        "oneshot", 15.0,  4.0, -30.0, filt="lowpass=f=3000"),
    layer("desert_home",  "wind_desert_bleak",     "loop",    29.0,  8.5, -38.0, fin=2.0, fout=2.0),
    layer("courtyard",    "crowd_murmur_distant",  "loop",    37.3,  8.7, -40.0, filt="lowpass=f=2200", fin=2.0, fout=3.0),
    layer("claim_choir",  "heavenly_choir_soft",   "oneshot", 44.0,  7.0, -32.0, fin=1.5, fout=3.0),
    layer("desert_dusk",  "wind_desert_bleak",     "loop",    63.0,  7.03, -40.0, fin=2.5, fout=2.5),
]

if __name__ == "__main__":
    sfxlib.show_plan("Episode 1 -- The Queen Who Came to Test Him", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT, regions=[
        ("f01 desert", 4.33, 12.37), ("f02/f03 hall", 12.37, 29.0),
        ("f04 desert", 29.0, 37.33), ("f05/f06 court+claim", 37.33, 51.4),
        ("back+hold", 63.33, 70.03),
    ])
