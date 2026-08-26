"""Ambient/SFX bed for the pilot, "The Ladder" (Jacob's Ladder, Gen 28:10-17 +
John 1:51) -- retrofit pass, reuses the shared sfxlib.py mix pattern first
built for episode 1, $0, reuse-only from sound_library.

Layer map keyed to the locked unit timeline (from THE_LADDER_BOOK_final.mp4's
own held durations, cross-checked against _assembly_v2/concat.txt + the
+3.0s INV-26 landing hold): front 0-4.0 (the flight, dusk), f02 4.0-16.9
(asleep on the stone, open night), f03 16.9-21.93 (the dream: the ladder,
angels ascending/descending), f04 21.93-33.93 ("I am with thee" -- the
theophany peak, a deliberate near-hold page), f05 33.93-38.97 (waking,
first light), f06 38.97-44.0 ("I knew it not" -- ordinary dawn ground), f07
44.0-50.8 (the wide field, dew, birds, "you are not alone"), back 50.8-62.0
(full dawn, the gospel pivot "He is that ladder" + CTA + the 3s landing hold).

Design: a desert-wind bookend opens on the flight and closes on the renewed
dawn walk (fled at dusk in wind / walks on at dawn in wind). The dream and
the theophany get NO added device at all beyond a bare thread of hollow
room-tone -- the page's own comment calls f04 "the world holds its breath
while the LORD speaks," so the sound design holds its breath too, rather
than illustrating the vision with an effect. Birdsong warmth joins for the
wide dawn field (the art itself draws two birds crossing the sky), and the
one heavenly-choir swell is reserved for the single gospel-pivot line "He is
that ladder" -- not the OT vision -- so the sound design itself performs the
whole thread's own claim: Jacob saw a ladder, but the swell belongs to Jesus.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "sfx_pilots"))
import sfxlib  # noqa: E402
from sfxlib import layer  # noqa: E402

CUT = HERE / "THE_LADDER_BOOK_final.mp4"
OUT = HERE / "THE_LADDER_BOOK_final_sfx.mp4"

LAYERS = [
    layer("flight_wind",   "wind_desert_bleak",   "loop",     0.0,  9.0, -36.0, fin=1.5, fout=3.0),
    layer("night_air",     "air_hollow_desolate", "loop",     5.0, 29.0, -44.0, fin=3.0, fout=4.0),
    layer("dawn_wind",     "wind_desert_bleak",   "loop",    33.0, 29.0, -34.0, fin=2.5, fout=3.5),
    layer("morning_birds", "dawn_morning_warm",   "loop",    43.5, 12.0, -33.0, fin=2.5, fout=3.0),
    layer("landing_choir", "heavenly_choir_soft", "oneshot", 52.5,  9.5, -31.0, fin=2.5, fout=4.0),
]

if __name__ == "__main__":
    sfxlib.show_plan("The Ladder (pilot)", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT, regions=[
        ("front flight", 0.0, 4.0), ("f02 asleep", 4.0, 16.9),
        ("f03/f04 dream+theophany", 16.9, 33.93), ("f05/f06 waking", 33.93, 44.0),
        ("f07 wide field", 44.0, 50.8), ("back landing+hold", 50.8, 62.035),
    ])
