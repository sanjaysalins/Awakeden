"""Lay a reverent, choir-free ambient/SFX bed UNDER the scored Seed of the Woman film.

Cue sheet only — the engine is pipeline/sfx_bed.py (ONE shared copy, see its
docstring for the layer-stack / no-choir rules). Reuse-only from sound_library ($0).

Cues mapped to the scene_plan time windows (503.25s).
Output: Seed_Of_The_Woman_16x9_scored_sfx.mp4 (then caption it).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.sfx_bed import build  # noqa: E402

VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9"
SCORED = VIS / "Seed_Of_The_Woman_16x9_scored.mp4"
OUT = VIS / "Seed_Of_The_Woman_16x9_scored_sfx.mp4"
TOTAL = 500.53  # retimed 2026-07-03 to the panel-fix re-synth (-2.7s)

# (slug, start_s, end_s, gain_db) — ambient only, low. NO choir, NO score_* clips.
CUES = [
    ("air_hollow_desolate",    0.0,   500.53, -39),  # faint ambient air base throughout
    ("river_well_water",       0.0,    53.0,  -34),  # M1 the Eden garden (the still river)
    ("rumble_deep_sub",       53.0,    94.5,  -31),  # M2 the weight of judgment entering
    ("thunder_low_roll",      53.0,    67.5,  -28),  # S4 death enters the world (subtle)
    ("river_well_water",      94.5,   158.5,  -37),  # M3 still in the garden (faint presence)
    ("rumble_deep_sub",      130.2,   140.2,  -29),  # S9 the promise / holy weight
    ("fire_crackling",       183.4,   202.7,  -31),  # S12 the manger lamp
    ("rumble_deep_sub",      319.9,   345.1,  -30),  # S18 head/heel — the exchange weight
    ("wind_desert_bleak",    345.1,   415.1,  -34),  # M6 Golgotha desolate air
    ("thunder_low_roll",     345.1,   392.0,  -26),  # S19/S20 the cross / the turn (storm)
    ("dawn_morning_warm",    392.0,   415.1,  -29),  # S21 the empty tomb (dawn resolve)
    ("river_well_water",     415.1,   466.5,  -37),  # M7 back in the garden (where it was spoken)
    ("dawn_morning_warm",    464.0,   500.53, -28),  # S24/S25 step out + risen-Christ hero (resolve)
]


if __name__ == "__main__":
    build(SCORED, OUT, CUES, TOTAL)
