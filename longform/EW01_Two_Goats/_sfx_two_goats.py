"""Lay a reverent, choir-free ambient/SFX bed UNDER the scored Two Goats film.

Cue sheet only — the engine is pipeline/sfx_bed.py (ONE shared copy, see its
docstring for the layer-stack / no-choir rules). Reuse-only from sound_library ($0).

Cues mapped to the scene_plan time windows (589.2s narration, 591.7s scored).
Output: EW01_Two_Goats_16x9_scored_sfx.mp4 (then caption it).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.sfx_bed import build  # noqa: E402

VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9"
SCORED = VIS / "EW01_Two_Goats_16x9_scored.mp4"
OUT = VIS / "EW01_Two_Goats_16x9_scored_sfx.mp4"
TOTAL = 591.7

# (slug, start_s, end_s, gain_db) — ambient only, low. NO choir, NO score_* clips.
CUES = [
    ("air_hollow_desolate",   0.0,   591.7, -40),  # faint sacred air base throughout
    ("crowd_murmur_distant",  0.0,    99.0, -36),  # M1 the hushed multitude outside the court
    ("rumble_deep_sub",      58.5,    99.0, -31),  # S4-S5 behind the veil / the cloud / holy weight
    ("rumble_deep_sub",      99.0,   122.0, -30),  # S6 the dead sons — strange fire judgment
    ("fire_crackling",       78.0,   195.0, -35),  # incense + the altar fire through the act
    ("wind_desert_bleak",   167.0,   213.0, -33),  # S9-S10 the scapegoat into "a land not inhabited"
    ("rumble_deep_sub",     313.0,   360.0, -32),  # S15 the ache — "pointing at a greater atonement"
    ("rumble_deep_sub",     360.0,   428.0, -29),  # M6 the reveal building (Christ, his own blood)
    ("wind_desert_bleak",   405.8,   428.0, -33),  # S19 "suffered without the gate"
    ("thunder_low_roll",    383.0,   428.0, -27),  # S18-S20 the cross / the iniquity laid on him
    ("veil_tearing",        428.4,   433.5, -25),  # S20 "the veil rent from the top to the bottom"
    ("crowd_murmur_distant",531.0,   558.0, -39),  # S24 boldness to enter — the quiet procession
    ("dawn_morning_warm",   451.0,   591.7, -29),  # M7 the invitation + close on Christ (warm resolve)
]


if __name__ == "__main__":
    build(SCORED, OUT, CUES, TOTAL)
