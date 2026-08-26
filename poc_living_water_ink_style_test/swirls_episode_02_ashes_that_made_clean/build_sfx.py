"""Ambient/SFX bed for episode 2, "The Ashes That Made Clean" (Numbers 19 +
Hebrews 9:14) -- retrofit pass, reuses the shared sfxlib.py mix pattern
first built for episode 1, $0, reuse-only from sound_library.

Layer map keyed to the locked unit timeline (from THE_ASHES_BOOK_final.mp4's
own held durations, cross-checked against _assembly/concat.txt + the +3.0s
INV-26 landing hold): front 0-7.9 (the reaching hand, the instant of
contact), f01 7.9-16.93 (the priest burning the heifer outside the camp),
f02 16.93-30.1 (the unclean man alone, counting the days -- carries the
Numbers 19 KJV quote), f03 30.1-40.27 (kneeling at the grave, the water
vessel untouched, "a stain water alone can't reach"), f04 40.27-50.43 (the
hyssop, the water, the ash visibly rinsing away -- carries the Hebrews 9:14
KJV quote), back 50.43-62.0 (Christ's hand meeting the marked hand, gold
light breaking through grey, the gospel pivot + CTA + the 3s landing hold).

Design: the whole piece lives in ONE bleak, wind-scoured wilderness (the
priest's own prompt calls it that verbatim), so a single wind bed runs
almost the whole length rather than cutting scene to scene. The fire under
the heifer's burning gets its own brief crackle. The water/hyssop scene
gets real trickling water, carried into the back cover so the ash's actual
rinsing-away is heard, not just seen. The one heavenly-choir swell is
reserved for the single gospel-pivot line ("he touched what makes us
unclean, and did not become unclean -- so we could finally be") + the CTA,
matching the pilot/episode-1 discipline of one swell, saved for Christ.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "sfx_pilots"))
import sfxlib  # noqa: E402
from sfxlib import layer  # noqa: E402

CUT = HERE / "THE_ASHES_BOOK_final.mp4"
OUT = HERE / "THE_ASHES_BOOK_final_sfx.mp4"

LAYERS = [
    layer("wilderness_wind",   "wind_desert_bleak",   "loop",     0.0, 55.0, -38.0, fin=1.5, fout=4.0),
    layer("heifer_fire",       "fire_crackling",      "loop",     7.9,  9.0, -33.0, fin=1.5, fout=2.0),
    layer("purification_water", "river_well_water",   "loop",    39.5, 13.0, -32.0, fin=2.0, fout=3.0),
    layer("landing_choir",     "heavenly_choir_soft", "oneshot", 53.0,  9.0, -31.0, fin=2.5, fout=4.0),
]

if __name__ == "__main__":
    sfxlib.show_plan("Episode 2 -- The Ashes That Made Clean", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT, regions=[
        ("front contact", 0.0, 7.9), ("f01 burning", 7.9, 16.93),
        ("f02 unclean/quote", 16.93, 30.1), ("f03 the grave", 30.1, 40.27),
        ("f04 rinsing/Hebrews", 40.27, 50.43), ("back landing+hold", 50.43, 62.0),
    ])
