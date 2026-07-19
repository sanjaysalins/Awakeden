"""Lay the SAME reverent, choir-free ambient/SFX bed as _sfx_bronze.py UNDER the
graphic-novel rebuild's scored film (2026-07-16 test). Cues/timings are IDENTICAL
(sound design doesn't change with art style; the scene ids/timings are unchanged
from the archived Baroque plan) -- only the visual_16x9 path -> visual_16x9_inked
and the film name change.

Cue sheet only — the engine is pipeline/sfx_bed.py (ONE shared copy, see its
docstring for the layer-stack / no-choir rules). Reuse-only from sound_library ($0).
Output: BronzeSerpent_16x9_scored_sfx.mp4
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.sfx_bed import build  # noqa: E402

VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked"
SCORED = VIS / "BronzeSerpent_16x9_scored.mp4"
OUT = VIS / "BronzeSerpent_16x9_scored_sfx.mp4"
TOTAL = 477.77  # matches BronzeSerpent_16x9_scored.mp4 (dense rebuild, 2026-07-16)

# Cue timings are tied to NARRATIVE time (what's being said), not to specific beat
# boundaries -- the underlying narration.mp3 is byte-identical to the original cut,
# so these word-timeline anchors still land on the same moments after the dense
# beat-authoring rebuild. Only the tail (dawn_morning_warm/wind_desert_bleak) end
# points are nudged to the new total.
CUES = [
    ("wind_desert_bleak",      0.0,   477.7, -37),
    ("air_hollow_desolate",    0.0,    76.9, -34),
    ("crowd_murmur_distant",  16.4,    43.3, -38),
    ("rumble_deep_sub",       43.3,    76.9, -29),
    ("thunder_low_roll",      45.0,    53.5, -27),
    ("crowd_murmur_distant",  63.5,   109.6, -36),
    ("fire_crackling",       118.4,   150.4, -29),
    ("air_hollow_desolate",  150.4,   178.0, -35),
    ("fire_crackling",       178.0,   220.9, -33),
    ("rumble_deep_sub",      220.9,   262.5, -31),
    ("thunder_low_roll",     234.2,   262.5, -26),
    ("air_hollow_desolate",  262.5,   330.5, -34),
    ("impact_low_boom",      275.5,   278.5, -15),
    ("rumble_deep_sub",      330.5,   361.0, -30),
    ("dawn_morning_warm",    418.9,   477.7, -30),
]


if __name__ == "__main__":
    build(SCORED, OUT, CUES, TOTAL)
