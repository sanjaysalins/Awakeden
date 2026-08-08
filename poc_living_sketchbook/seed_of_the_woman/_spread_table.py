"""Seed of the Woman LONG -- the one shared source of truth for the spread
table. FULL EPISODE: 71 spreads (spreads 1-5 promoted from the POC30
process-validation test, memory `day-of-atonement-retro-learnings`;
spreads 6-71 authored 2026-08-07 per SKILL.md sec.8b -- Fable pre-designed
the full plan in `_PLAN.md` + `_PREFLIGHT.md` BEFORE any further
rendering). Mirrors day_of_atonement/_spread_table.py's exact pattern/role.

Timing basis: CORRECTED 2026-08-07 night by `_s5b_reconcile_timing.py`.
`_turn_boundaries.json`'s claimed turn starts turned out to be a
proportional ESTIMATE, not real ffprobe'd/measured turn boundaries (unlike
Day of Atonement) -- confirmed by searching the real per-word
`_alignment.json` for turn 34's own first words ("That is the cross"): real
346.67s vs the claimed 353.66s, a ~7s drift that grows through the file
(cumulative tokenization mismatch, up to ~9s by turn 29). Every turn's real
start was re-derived by literal word-sequence search against
`_alignment.json` (ground truth: the actual forced alignment of
narration.mp3); each spread's ORIGINAL fractional position within its
claimed turn window (the plan's own sub-turn design intent) was then
re-applied to that turn's REAL window. Spreads 1-5 barely moved (turns 0-2
had near-zero drift); by spread 71 the correction is ~2s. Old
plan-estimate numbers are in git history (this file, pre-2026-08-07-night)
and in `_PLAN.md`'s own table (not yet re-synced -- treat this file as
authoritative for build). The chain is continuous: each spread's start ==
the previous spread's end.
"""

# (spread_num, name, beat, start_s, end_s) -- from _PLAN.md, corrected per
# the docstring above (see _corrected_spreads.json for the raw output)
# beat == movement number (1-7 per longform/05_The_Seed_Of_The_Woman/v1/narration.md)
SPREADS = [
    (1, "s01_something_wrong", 1, 0.00, 5.44),
    (2, "s02_the_hiding", 1, 5.44, 11.15),
    (3, "s03_verse_card", 1, 11.15, 23.57),
    (4, "s04_god_walking", 1, 23.57, 30.07),
    (5, "s05_where_art_thou", 1, 30.07, 33.18),
    # ---- Movement 1 remainder (turns 4-6) ----
    (6, "s06_blame_circle", 1, 33.18, 39.30),
    (7, "s07_beguiled_card", 1, 39.30, 42.86),
    (8, "s08_coming_apart", 1, 42.86, 48.00),
    (9, "s09_unexpected_place", 1, 48.00, 52.60),
    # ---- Movement 2 (turns 7-8) ----
    (10, "s10_judgment_falls", 2, 52.60, 60.07),
    (11, "s11_afraid_of_presence", 2, 60.07, 67.56),
    (12, "s12_creatures_word", 2, 67.56, 75.15),
    (13, "s13_the_fruit", 2, 75.15, 82.06),
    (14, "s14_death_enters", 2, 82.06, 87.98),
    (15, "s15_the_breach", 2, 87.98, 94.49),
    # ---- Movement 3 (turns 9-14) ----
    (16, "s16_watch_closely", 3, 94.49, 99.16),
    (17, "s17_not_adam_not_eve", 3, 99.16, 103.83),
    (18, "s18_turns_to_serpent", 3, 103.83, 108.70),
    (19, "s19_curse_card", 3, 108.70, 119.19),
    (20, "s20_pure_curse", 3, 119.19, 124.66),
    (21, "s21_gold_woven_in", 3, 124.66, 130.67),
    (22, "s22_promise_card", 3, 130.67, 139.42),
    (23, "s23_let_that_land", 3, 139.42, 145.88),
    (24, "s24_before_their_sentences", 3, 145.88, 152.49),
    (25, "s25_promise_in_curse", 3, 152.49, 158.53),
    # ---- Movement 4 (turns 15-25) ----
    (26, "s26_her_seed_study", 4, 158.53, 165.00),
    (27, "s27_line_of_fathers", 4, 165.00, 172.98),
    (28, "s28_clue_lights_up", 4, 172.98, 183.26),
    (29, "s29_fulness_card", 4, 183.26, 191.53),
    (30, "s30_annunciation", 4, 191.53, 198.41),
    (31, "s31_holy_thing_card", 4, 198.41, 204.19),
    (32, "s32_honest_match", 4, 204.19, 211.71),
    (33, "s33_trajectory", 4, 211.71, 220.30),
    (34, "s34_naming_serpent", 4, 220.30, 232.00),
    (35, "s35_naming_mission", 4, 232.00, 239.68),
    (36, "s36_naming_crushing", 4, 239.68, 248.50),
    (37, "s37_promise_planted", 4, 248.50, 254.11),
    # ---- Movement 5 (turns 26-30) ----
    (38, "s38_skeptic_quiet", 5, 254.11, 261.29),
    (39, "s39_snake_story", 5, 261.29, 268.96),
    (40, "s40_partly_fair", 5, 268.96, 276.94),
    (41, "s41_shape_of_canon", 5, 276.94, 286.42),
    (42, "s42_from_within", 5, 286.42, 298.11),
    (43, "s43_under_your_feet", 5, 298.11, 302.75),
    (44, "s44_stands_on_one", 5, 302.75, 311.32),
    (45, "s45_eden_to_cross", 5, 311.32, 321.28),
    # ---- Movement 6 (turns 31-36) ----
    (46, "s46_look_again", 6, 321.28, 328.14),
    (47, "s47_two_wounds_card", 6, 328.14, 333.53),
    (48, "s48_heel_strike", 6, 333.53, 340.35),
    (49, "s49_head_crush", 6, 340.35, 346.68),
    (50, "s50_that_is_the_cross", 6, 346.68, 352.47),
    (51, "s51_bearing_wages", 6, 352.47, 358.43),
    (52, "s52_judgment_on_him", 6, 358.43, 364.10),
    (53, "s53_through_death_card", 6, 364.10, 370.80),
    (54, "s54_seeming_win", 6, 370.80, 377.76),
    (55, "s55_the_inversion", 6, 377.76, 384.92),
    (56, "s56_triumph_card", 6, 384.92, 393.11),
    (57, "s57_empty_tomb", 6, 393.11, 401.29),
    (58, "s58_beaten_enemy", 6, 401.29, 406.92),
    (59, "s59_end_certain", 6, 406.92, 412.34),
    # ---- Movement 7 (turns 37-40) ----
    (60, "s60_still_open", 7, 412.34, 416.84),
    (61, "s61_not_altar_not_mountain", 7, 416.84, 423.23),
    (62, "s62_into_a_curse", 7, 423.23, 430.22),
    (63, "s63_before_temple", 7, 430.22, 436.70),
    (64, "s64_named_future", 7, 436.70, 442.60),
    (65, "s65_oldest_lie", 7, 442.60, 450.36),
    (66, "s66_promise_kept", 7, 450.36, 457.04),
    (67, "s67_matter_of_time", 7, 457.04, 463.69),
    (68, "s68_no_climbing_back", 7, 463.69, 469.14),
    (69, "s69_empty_hands", 7, 469.14, 480.04),
    (70, "s70_step_out", 7, 480.04, 488.42),
    (71, "s71_found_by_him", 7, 488.42, 500.45),  # LANDING (+ >=3.0s hold at assembly)
]

# Full episode: last word "Him." ends at 500.451 per _alignment.json (real
# forced alignment -- confirmed ground truth, unlike _turn_boundaries.json).
LAST_WORD_END_ESTIMATE = 500.451
# Real INV-26 landing hold for the full episode (was 0.6 for the short test
# excerpt, which was explicitly not a real landing).
LANDING_HOLD_S = 3.0

ALWAYS_STATIC_HOLD = set()

by_name = {name: (num, beat, start, end) for num, name, beat, start, end in SPREADS}
by_num = {num: (name, beat, start, end) for num, name, beat, start, end in SPREADS}
