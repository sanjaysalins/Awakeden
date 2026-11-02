import sys
from pathlib import Path
H = Path(__file__).resolve().parent
ROOT = H.parents[2]
sys.path.insert(0, str(ROOT / "sfx_pilots"))
import sfxlib
from sfxlib import layer
CUT = H / "video" / "jacobs_ladder_v3.mp4"
OUT = H / "video" / "jacobs_ladder_v3_sfx.mp4"
LAYERS = [
    layer("flight_wind",   "wind_desert_bleak",   "loop",     0.0, 10.5, -36.0, fin=1.5, fout=3.0),
    layer("night_air",     "air_hollow_desolate", "loop",     9.0, 22.0, -44.0, fin=3.0, fout=4.0),
    layer("dawn_wind",     "wind_desert_bleak",   "loop",    29.9, 26.6, -34.0, fin=2.5, fout=3.5),
    layer("morning_birds", "dawn_morning_warm",   "loop",    32.0, 10.0, -33.0, fin=2.5, fout=3.0),
    layer("heaven_choir",  "heavenly_choir_soft", "oneshot", 43.0,  9.5, -31.0, fin=2.5, fout=4.0),
]
if __name__ == "__main__":
    sfxlib.show_plan("Jacob's Ladder v3", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print("[ok]", OUT)
    sfxlib.measure(OUT, regions=[("front", 0, 9.98), ("dream+promise", 13.3, 29.9), ("waking", 29.9, 37.4), ("jesus quote", 37.4, 50.4), ("landing", 50.4, 56.5)])
