"""Seed of the Woman LONG -- the one shared source of truth for the spread
table. FULL EPISODE: 71 spreads (spreads 1-5 promoted from the POC30
process-validation test, memory `day-of-atonement-retro-learnings`;
spreads 6-71 authored 2026-08-07 per SKILL.md sec.8b -- Fable pre-designed
the full plan in `_PLAN.md` + `_PREFLIGHT.md` BEFORE any further
rendering). Mirrors day_of_atonement/_spread_table.py's exact pattern/role.

Timing basis: spreads 1-5 = the excerpt's real forced alignment
(`_alignment.json`); spreads 6-71 = `_turn_boundaries.json` (real
forced-alignment-derived turn windows, +/-1-2s) with sub-turn seams as
word-proportional ESTIMATES -- the standard alignment-correction pass
re-cuts those seams before build (see _PREFLIGHT.md E8). The chain is
continuous: each spread's start == the previous spread's end; inter-turn
pauses are absorbed into the preceding spread's hold (e.g. s19, s59).
"""

# (spread_num, name, beat, start_s, end_s) -- from _PLAN.md
# beat == movement number (1-7 per longform/05_The_Seed_Of_The_Woman/v1/narration.md)
SPREADS = [
    (1, "s01_something_wrong", 1, 0.0, 5.8),
    (2, "s02_the_hiding", 1, 5.8, 11.9),
    (3, "s03_verse_card", 1, 11.9, 24.0),
    (4, "s04_god_walking", 1, 24.0, 30.7),
    # s05 end extended 33.03 -> 33.80 (full-file _turn_boundaries.json puts
    # turn 3's end at 33.76 vs the excerpt alignment's 33.03; the designed
    # hold just breathes ~0.8s longer -- see _PLAN.md timing seam note).
    (5, "s05_where_art_thou", 1, 30.7, 33.80),
    # ---- Movement 1 remainder (turns 4-6) ----
    (6, "s06_blame_circle", 1, 33.80, 40.67),
    (7, "s07_beguiled_card", 1, 40.67, 43.75),
    (8, "s08_coming_apart", 1, 43.75, 49.30),
    (9, "s09_unexpected_place", 1, 49.30, 54.33),
    # ---- Movement 2 (turns 7-8) ----
    (10, "s10_judgment_falls", 2, 54.33, 61.50),
    (11, "s11_afraid_of_presence", 2, 61.50, 68.81),
    (12, "s12_creatures_word", 2, 68.81, 76.50),
    (13, "s13_the_fruit", 2, 76.50, 83.50),
    (14, "s14_death_enters", 2, 83.50, 89.50),
    (15, "s15_the_breach", 2, 89.50, 96.16),
    # ---- Movement 3 (turns 9-14) ----
    (16, "s16_watch_closely", 3, 96.16, 100.64),
    (17, "s17_not_adam_not_eve", 3, 100.64, 105.30),
    (18, "s18_turns_to_serpent", 3, 105.30, 110.31),
    (19, "s19_curse_card", 3, 110.31, 121.36),
    (20, "s20_pure_curse", 3, 121.36, 126.50),
    (21, "s21_gold_woven_in", 3, 126.50, 132.20),
    (22, "s22_promise_card", 3, 132.20, 143.15),
    (23, "s23_let_that_land", 3, 143.15, 149.50),
    (24, "s24_before_their_sentences", 3, 149.50, 156.00),
    (25, "s25_promise_in_curse", 3, 156.00, 162.01),
    # ---- Movement 4 (turns 15-25) ----
    (26, "s26_her_seed_study", 4, 162.01, 168.50),
    (27, "s27_line_of_fathers", 4, 168.50, 176.50),
    (28, "s28_clue_lights_up", 4, 176.50, 186.90),
    (29, "s29_fulness_card", 4, 186.90, 194.76),
    (30, "s30_annunciation", 4, 194.76, 201.98),
    (31, "s31_holy_thing_card", 4, 201.98, 208.63),
    (32, "s32_honest_match", 4, 208.63, 216.50),
    (33, "s33_trajectory", 4, 216.50, 225.50),
    (34, "s34_naming_serpent", 4, 225.50, 236.91),
    (35, "s35_naming_mission", 4, 236.91, 244.96),
    (36, "s36_naming_crushing", 4, 244.96, 253.59),
    (37, "s37_promise_planted", 4, 253.59, 259.55),
    # ---- Movement 5 (turns 26-30) ----
    (38, "s38_skeptic_quiet", 5, 259.55, 267.82),
    (39, "s39_snake_story", 5, 267.82, 275.50),
    (40, "s40_partly_fair", 5, 275.50, 283.50),
    (41, "s41_shape_of_canon", 5, 283.50, 293.00),
    (42, "s42_from_within", 5, 293.00, 304.77),
    (43, "s43_under_your_feet", 5, 304.77, 311.19),
    (44, "s44_stands_on_one", 5, 311.19, 318.50),
    (45, "s45_eden_to_cross", 5, 318.50, 327.03),
    # ---- Movement 6 (turns 31-36) ----
    (46, "s46_look_again", 6, 327.03, 337.03),
    (47, "s47_two_wounds_card", 6, 337.03, 341.96),
    (48, "s48_heel_strike", 6, 341.96, 348.00),
    (49, "s49_head_crush", 6, 348.00, 353.66),
    (50, "s50_that_is_the_cross", 6, 353.66, 359.50),
    (51, "s51_bearing_wages", 6, 359.50, 365.50),
    (52, "s52_judgment_on_him", 6, 365.50, 371.21),
    (53, "s53_through_death_card", 6, 371.21, 377.70),
    (54, "s54_seeming_win", 6, 377.70, 384.50),
    (55, "s55_the_inversion", 6, 384.50, 391.50),
    (56, "s56_triumph_card", 6, 391.50, 399.50),
    (57, "s57_empty_tomb", 6, 399.50, 407.50),
    (58, "s58_beaten_enemy", 6, 407.50, 413.00),
    (59, "s59_end_certain", 6, 413.00, 419.44),
    # ---- Movement 7 (turns 37-40) ----
    (60, "s60_still_open", 7, 419.44, 424.59),
    (61, "s61_not_altar_not_mountain", 7, 424.59, 431.00),
    (62, "s62_into_a_curse", 7, 431.00, 438.00),
    (63, "s63_before_temple", 7, 438.00, 444.50),
    (64, "s64_named_future", 7, 444.50, 450.54),
    (65, "s65_oldest_lie", 7, 450.54, 457.50),
    (66, "s66_promise_kept", 7, 457.50, 463.50),
    (67, "s67_matter_of_time", 7, 463.50, 469.75),
    (68, "s68_no_climbing_back", 7, 469.75, 474.30),
    (69, "s69_empty_hands", 7, 474.30, 483.40),
    (70, "s70_step_out", 7, 483.40, 490.40),
    (71, "s71_found_by_him", 7, 490.40, 500.45),  # LANDING (+ >=3.0s hold at assembly)
]

# Full episode: last word "Him." ends at 500.451 per _turn_boundaries.json
# (turn 40 end). Was 32.424 for the 33s POC30 excerpt.
LAST_WORD_END_ESTIMATE = 500.451
# Real INV-26 landing hold for the full episode (was 0.6 for the short test
# excerpt, which was explicitly not a real landing).
LANDING_HOLD_S = 3.0

ALWAYS_STATIC_HOLD = set()

by_name = {name: (num, beat, start, end) for num, name, beat, start, end in SPREADS}
by_num = {num: (name, beat, start, end) for num, name, beat, start, end in SPREADS}
