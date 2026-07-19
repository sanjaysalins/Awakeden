"""Lay a reverent, choir-free ambient/SFX bed UNDER the scored Day of Atonement film.

Cue sheet only — the engine is pipeline/sfx_bed.py (ONE shared copy, see its
docstring for the layer-stack / no-choir rules). Reuse-only from sound_library ($0).

Cues mapped to the scene_plan time windows (532.6s, 25 scenes).
Output: Day_Of_Atonement_16x9_scored_sfx.mp4 (then caption it).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.sfx_bed import build  # noqa: E402

VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9"
SCORED = VIS / "Day_Of_Atonement_16x9_scored.mp4"
OUT = VIS / "Day_Of_Atonement_16x9_scored_sfx.mp4"
TOTAL = 532.6

# (slug, start_s, end_s, gain_db) — ambient only, low. NO choir, NO score_* clips.
CUES = [
    ("air_hollow_desolate",    0.0,   532.6, -40),  # faint sacred air base throughout
    ("shofar_blast",           0.5,     6.5, -26),  # M1 hook — the Day of Atonement ram's-horn call (Lev 25:9)
    ("fire_crackling",         0.0,    61.0, -33),  # M1 the lamp/incense warmth, the priest robing
    ("crowd_murmur_distant",  61.0,   102.0, -34),  # M2 "a guilty people" — the congregation's weight
    ("rumble_deep_sub",       61.0,   102.0, -30),  # M2 a year of sin piled up
    ("fire_crackling",       102.0,   166.0, -31),  # M3 goats at the altar, lots cast
    ("rumble_deep_sub",      166.0,   208.0, -30),  # M4 blood behind the veil / hands on the goat
    ("wind_desert_bleak",    208.0,   293.1, -32),  # M4 the scapegoat into the wilderness, outside the gate
    ("footsteps_dirt_approach", 208.0, 212.0, -27), # S11 the scapegoat driven out
    ("thunder_low_roll",     229.3,   250.5, -26),  # S12 "by his own blood entered in" — the cross
    ("rumble_deep_sub",      250.5,   293.1, -28),  # S13-14 Isaiah 53 / outside the camp — holy weight
    ("fire_crackling",       316.1,   362.2, -28),  # M5 "the same blood, never finished" — endless altar smoke
    ("rumble_deep_sub",      362.2,   409.4, -27),  # M6 the priest stands / once for all — building weight
    ("veil_tearing",         411.5,   416.5, -22),  # S20 "the veil rent in twain from the top"
    ("dawn_morning_warm",    432.9,   532.6, -28),  # M6 close + M7 invitation + risen-Christ hero (grace resolve)
    ("crowd_murmur_distant", 494.6,   513.6, -37),  # S24 "boldness to enter" — the quiet approach
]


if __name__ == "__main__":
    build(SCORED, OUT, CUES, TOTAL)
