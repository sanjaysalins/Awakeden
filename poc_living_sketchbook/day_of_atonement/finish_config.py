"""Day of Atonement LONG's finish_config.py -- for `_finish_long.py`
(poc_living_sketchbook/_finish_long.py). Content transcribed VERBATIM from
the shipped, hand-written `_s8_score.py`/`_s9_sfx.py`/`_s10_captions.py`
(2026-08-07), used as the regression fixture proving the shared runner
reproduces this episode's own real output before any new episode trusts it.
"""

STEM = "DAYOFATONEMENT_LONG_living_sketchbook"

SCORE = {
    "segments": ["lonely_searching_a", "glory_holy_stillness_a", "sacred_grace_rise_b"],
    "xfade_s": 6.0,
    "gain_db": -11.0,
    "outro_s": 2.5,
}

SFX_CUES = [
    ("wind_desert_bleak", "ALL", -22),
    ("footsteps_dirt_approach", "s05_walking_to_veil", -16),
    ("air_hollow_desolate", "s06_holy_of_holies_empty", -18),
    ("crowd_murmur_distant", "s07_nation_outside", -15),
    ("door_gate_creak", "s08_curtain_shut", -14),
    ("fire_crackling", "s10_strange_fire", -14),
    ("impact_low_boom", "s11_struck_down", -11),
    ("impact_low_boom", "s25_slaying_stage1", -12),
    ("waterpot_drop_run", "s42_basin_linen_ready", -15),
    ("veil_tearing", "s62_veil_torn", -8),
    ("door_gate_creak", "s70_veil_held_open", -18),
    ("footsteps_dirt_approach", "s73_aaron_steps_aside", -16),
]

CAPTIONS = {
    "skip_spreads": [
        "s16_lords_charge_card", "s20_blood_atonement_card", "s24_lots_card",
        "s28_bring_blood_card", "s33_empty_horizon_card", "s35_two_kids_card",
        "s52_jesus_entering_formal", "s58_gate_card", "s60_seated_glory",
        "s63_torn_veil_card", "s69_east_west_card", "s72_boldness_card",
    ],
    "segment_seconds": 60.0,
}

WATERMARK = True
