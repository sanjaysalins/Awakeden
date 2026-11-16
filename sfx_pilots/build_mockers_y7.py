"""Ambient/SFX bed + reused score for Living Comic Piece 2 'The Mockers' Words' Y7 ($0 reuse from sound_library).
Times from the Y7 recording (narration 73.4s + 3s hold = 76.4s film)."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_living_comic\out\_y7_padded.mp4")
OUT = CUT.with_name("the_mockers_y7_sfx.mp4")

LAYERS = [
    layer("crowd1",  "crowd_murmur_distant", "loop",      0.0, 12.0, -41.0, fin=1.0, fout=2.5),             # leaders shout
    layer("shout1",  "crowd_shout_mob",      "oneshot",   8.0,  4.0, -40.0, filt="lowpass=f=2500"),         # mocker line 1
    layer("wind",    "wind_desert_bleak",    "loop",     12.5, 17.0, -40.0, fin=2.0, fout=3.0),             # back to David
    layer("crowd2",  "crowd_murmur_distant", "loop",     31.0, 14.0, -41.0, fin=1.5, fout=3.0),             # passers-by shout
    layer("shout2",  "crowd_shout_mob",      "oneshot",  40.2,  4.0, -40.0, filt="lowpass=f=2500"),         # come down
    layer("score",   "score_reverent_grace", "oneshot",  46.0, 30.4, -32.0, fin=4.0, fout=5.0),             # He stayed -> landing (reused score)
    layer("thunder", "thunder_low_roll",     "oneshot",  63.0,  6.0, -36.0, filt="lowpass=f=900"),          # He died there
    layer("quake",   "rumble_deep_sub",      "oneshot",  68.5,  4.0, -37.0, filt="lowpass=f=300"),          # the earthquake
]

if __name__ == "__main__":
    sfxlib.show_plan("Mockers Y7", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT, [("narr 0-8", 0, 8), ("prayer 56-59", 56, 59), ("died 63-67", 63, 67), ("tail 73-76", 73, 76.4)])
