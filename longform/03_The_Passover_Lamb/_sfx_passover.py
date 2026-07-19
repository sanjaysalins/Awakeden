"""Lay a reverent, choir-free ambient/SFX bed UNDER the scored Passover film.

Cue sheet only — the engine is pipeline/sfx_bed.py (ONE shared copy, see its
docstring for the layer-stack / no-choir rules). Reuse-only from sound_library ($0).

Cues are mapped to the scene_plan time windows.
Output: Passover_Lamb_16x9_scored_sfx.mp4 (then caption it).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.sfx_bed import build  # noqa: E402

VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9"
SCORED = VIS / "Passover_Lamb_16x9_scored.mp4"
OUT = VIS / "Passover_Lamb_16x9_scored_sfx.mp4"
TOTAL = 509.5

# (slug, start_s, end_s, gain_db) — ambient only, low. NO choir, NO score_* clips.
CUES = [
    ("wind_desert_bleak",     0.0,   509.5, -37),  # faint ancient air throughout
    ("fire_crackling",        0.0,    13.4, -30),  # S1 lamp
    ("flock_sheep_field",    33.9,    53.2, -32),  # S3 the lamb
    ("rumble_deep_sub",      53.2,   102.9, -28),  # M2 death passes over Egypt
    ("thunder_low_roll",     55.0,    63.0, -26),  # the smiting (subtle)
    ("flock_sheep_field",   102.9,   121.6, -32),  # S6 flock at dawn
    ("dawn_morning_warm",   102.9,   121.6, -35),  # S6 dawn
    ("fire_crackling",      121.6,   146.4, -30),  # S7 hearth, four days
    ("crowd_murmur_distant",146.4,   167.6, -37),  # S8 the whole nation
    ("fire_crackling",      167.6,   213.9, -32),  # S9/S10 lamp + embers
    ("rumble_deep_sub",     213.9,   256.7, -31),  # M4 Golgotha weight
    ("crowd_murmur_distant",213.9,   240.7, -38),  # S11 Jerusalem below
    ("soldiers_march_armor",240.7,   256.7, -38),  # S12 soldiers (faint)
    ("air_hollow_desolate", 304.2,   365.3, -35),  # M5 the honest doubt, hollow
    ("fire_crackling",      414.3,   440.6, -31),  # S21 lamp, blood applied
    ("fire_crackling",      456.6,   477.7, -34),  # S23 inside the house
]


if __name__ == "__main__":
    build(SCORED, OUT, CUES, TOTAL)
