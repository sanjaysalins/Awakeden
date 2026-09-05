"""Ambient/SFX bed for episode 11, "Where Are the Nine" (Luke 17:11-19, the
ten lepers) -- reuses the shared sfxlib.py mix pattern, $0, reuse-only from
sound_library.

CORRECTED 2026-09-05: retimed to `unit_timing.json`'s REAL per-word alignment
boundaries (the score-design-early rebuild), replacing the old word-count-
proportional guesses. Layer map keyed to the real unit timeline: front
0-3.139 (sent before healed), f01 3.139-10.979 (only one came back), f02
10.979-19.18 (the cry for mercy), f03 19.18-25.42 (obeyed, and they went),
f04 25.42-29.939 (cleansed on the road, off-page), f05 29.939-35.719 (the
fork -- nine keep going, one turns back), f06 35.719-41.899 (he falls at his
feet), f07 41.899-50.799 ("where are the nine?" -- the empty road), f08
50.799-55.319 ("this stranger"), f09 55.319-62.199 (HERO -- "made thee
whole"), f10 62.199-74.58 (face to face, "Luke calls it thanks..."), back
74.58-83.609 (dawn, the empty road, including the +3.0s INV-26 hold). The
real boundaries moved the f09/f10 split 1.65s earlier and the back cover
0.85s later than the old proportional estimate -- both layer starts below
are updated to match exactly.

Design: unlike ep10 (one continuous interior room, stayed genuinely dry) this
whole episode happens outdoors on open, wind-scoured hill country -- every
still explicitly describes "vast wind-scoured wilderness" -- so a single
bleak desert wind carries the entire front half of the piece (front through
f09, the moment of personal encounter), the same asset and register ep7 used
for its own outdoor funeral throughline. Footsteps mark the one stretch where
the text itself puts the company actually moving (f03's obedience through
f05's fork -- "they obeyed," "as they went," "nine kept going"); no footstep
layer anywhere else, since the rest of the piece is people standing still,
falling, or speaking. The wind recedes and falls silent for f10 (the
resolved face-to-face beat), same "the words carry it" call ep8/ep10 already
made at their own emotional peaks -- score + narration alone. Dawn ambience
returns only under the back cover, which is explicitly set at dawn in its
own art direction, matching the ep7 back-cover precedent exactly. No crowd
layer anywhere (no crowd in this story -- Jesus and ten men only) and no
water asset of any kind (locked design constraint on every still in this
episode: "no water anywhere").

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_11_where_are_the_nine\\build_sfx.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "sfx_pilots"))
import sfxlib  # noqa: E402
from sfxlib import layer  # noqa: E402

CUT = HERE / "swirls_episode_11_where_are_the_nine_final_piano.mp4"
OUT = HERE / "swirls_episode_11_where_are_the_nine_final_piano_sfx.mp4"

LAYERS = [
    layer("wilderness_wind", "wind_desert_bleak",      "loop", 0.0,   62.2, -46.0, fin=2.0, fout=4.0),
    layer("walking_steps",   "footsteps_dirt_approach", "loop", 19.18, 16.54, -48.0, fin=2.0, fout=2.0),
    layer("dawn_landing",    "dawn_morning_warm",       "loop", 74.58, 9.03, -44.0, fin=2.5, fout=3.0),
]

if __name__ == "__main__":
    sfxlib.show_plan("Episode 11 -- Where Are the Nine", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT, regions=[
        ("front sent before healed", 0.0, 4.033), ("f01 only one came back", 4.033, 11.999),
        ("f02 have mercy", 11.999, 19.165), ("f03 obeyed", 19.165, 25.965),
        ("f04 cleansed off-page", 25.965, 30.732), ("f05 the fork", 30.732, 35.899),
        ("f06 at his feet", 35.899, 42.666), ("f07 where are the nine", 42.666, 51.433),
        ("f08 this stranger", 51.433, 56.999), ("f09 made whole (hero)", 56.999, 64.565),
        ("f10 face to face", 64.565, 73.731), ("back dawn+hold", 73.731, 83.609),
    ])
