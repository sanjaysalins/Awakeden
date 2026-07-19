"""Ambient/SFX bed for Psalm 22 ('Song From The Cross'), same reverent
choir-free-under-the-score approach as Bronze Serpent's _sfx_bronze_inked.py
(feedback-no-choir-pad-under-score) -- ambience/accents only, layered UNDER
the Suno score, never a musical/choir pad.

Cue sheet only — the engine is pipeline/sfx_bed.py (ONE shared copy).

No prior sfx script was found for this piece (the shipped LivingPage_Psalm22_
16x9_scored_sfx.mp4 predates a saved, reusable script) -- this is a fresh
cue sheet, authored from the piece's own beat captions
(v1/visual_16x9_inked/livingpage_full.spec.json), not a byte-exact recovery
of whatever ran before. Re-run after any score rebuild (2026-07-19: landing
hold extended to 3.0s, INV-26).

Arc: the forsaken cry (desolate) -> stripped/mocked (crowd) -> pierced hands
and feet / gambled garments (tension, then the exact detail) -> the honest
objection / scholarly weighing (quiet, contemplative) -> back to the cross,
the storm (weight) -> the turn to life, the congregation (warmth rising) ->
the ends of the earth streaming home, through the extended landing hold.

Output: LivingPage_Psalm22_16x9_scored_sfx.mp4
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.sfx_bed import build  # noqa: E402

VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9"
SCORED = VIS / "LivingPage_Psalm22_16x9_scored.mp4"
OUT = VIS / "LivingPage_Psalm22_16x9_scored_sfx.mp4"
TOTAL = 421.2  # 418.2s narration + 3.0s landing hold (INV-26, 2026-07-19)

CUES = [
    ("wind_desert_bleak",     0.0,   418.2, -37),   # continuous base
    ("air_hollow_desolate",   0.0,    45.0, -34),   # the forsaken cry
    ("crowd_murmur_distant", 59.4,    95.0, -36),   # stripped, mocked, the witness statement
    ("rumble_deep_sub",     101.8,   143.0, -30),   # bones out of joint, the tension before "pierced"
    ("nail_strike_single",  121.3,   122.3, -22),   # "they pierced my hands and my feet"
    ("coins_clinking",      143.0,   166.0, -32),   # "they part my garments... cast lots"
    ("air_hollow_desolate", 166.0,   230.0, -38),   # the honest objection, quiet and contemplative
    ("thunder_low_roll",    233.6,   279.0, -28),   # back to the cross, the storm
    ("rumble_deep_sub",     233.6,   289.0, -32),   # weight under the storm
    ("heavenly_choir_soft", 289.2,   340.0, -35),   # the turn to life, the congregation
    ("impact_low_boom",     370.5,   372.0, -18),   # "It is finished."
    ("dawn_morning_warm",   339.9,   TOTAL, -30),   # the ends of the earth stream home, through the landing hold
]


if __name__ == "__main__":
    build(SCORED, OUT, CUES, TOTAL)
