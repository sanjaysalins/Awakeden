"""Day of Atonement LONG -- the one shared source of truth for the 76-spread
table (number, name, beat, plan-estimated start/end). Mirrors
`bronze_serpent_long/_spread_table.py`'s exact pattern and role: imported by
the assembly stage only (this episode has no separate review-gallery script
that also needs these rows -- `_BATCH_PROGRESS.html`'s own SPREADS list is
the gallery's independent copy, same names, same order).

Start/end here are `_PLAN.md` section 2's ESTIMATED windows (turn-boundary
splits are ffprobe-hard per _PLAN.md sec 1c; sub-turn seams inside a turn are
estimates). `_s5_align.py` + `_s5b_spread_windows.py` correct the sub-turn
seams against real forced-alignment word timings; this file is the
un-corrected baseline they start from.

DEVICES intentionally NOT included here for the v1 "simple cut" pass
(blue-line, candle-only, halftone dissolve, Thread Device/Elder Leaf,
tear_hole, ribbon-marker) -- those are a deliberate polish-pass-2 layer,
same discipline bronze_serpent_long's own table used, added on TOP of this
base timeline once it exists and has been seen, not baked in now. Spreads 54
and 55 (Thread Device + Elder Leaf) are the one exception already built as
their own $0 compositing pass by `_s3_thread_leaf_54_55.py` -- their CLIPS
already exist and are used here like any other spread's clip.
"""

# (spread_num, name, beat, start_s, end_s) -- from _PLAN.md section 2
SPREADS = [
    (1, "s01_cold_open", 1, 0.00, 3.20),
    (2, "s02_tabernacle_wide", 1, 3.20, 9.30),
    (3, "s03_golden_garments", 1, 9.30, 13.90),
    (4, "s04_donning_linen", 1, 13.90, 22.20),
    (5, "s05_walking_to_veil", 1, 22.20, 26.80),
    (6, "s06_holy_of_holies_empty", 1, 26.80, 34.50),
    (7, "s07_nation_outside", 1, 34.50, 39.40),
    (8, "s08_curtain_shut", 1, 39.40, 46.40),
    (9, "s09_grief_close", 2, 46.40, 49.60),
    (10, "s10_strange_fire", 2, 49.60, 54.30),
    (11, "s11_struck_down", 2, 54.30, 58.90),
    (12, "s12_bodies_carried_out", 2, 58.90, 65.60),
    (13, "s13_door_curtain_sl13", 2, 65.60, 72.30),
    (14, "s14_hand_at_veil", 2, 72.30, 82.00),
    (15, "s15_moses_charge", 2, 82.00, 87.92),
    (16, "s16_lords_charge_card", 2, 87.92, 106.24),
    (17, "s17_squared_at_veil", 2, 106.24, 112.30),
    (18, "s18_own_sin_first", 2, 112.30, 122.30),
    (19, "s19_altar_ministry", 2, 122.30, 133.28),
    (20, "s20_blood_atonement_card", 2, 133.28, 137.20),
    (21, "s21_goat_innocent", 2, 137.20, 141.20),
    (22, "s22_ritual_hands", 3, 141.20, 148.50),
    (23, "s23_two_goats_brought", 3, 148.50, 156.08),
    (24, "s24_lots_card", 3, 156.08, 163.36),
    (25, "s25_slaying_stage1", 3, 163.36, 167.40),
    (26, "s26_through_veil_stage2", 3, 167.40, 171.40),
    (27, "s27_sprinkling", 3, 171.40, 175.44),
    (28, "s28_bring_blood_card", 3, 175.44, 182.16),
    (29, "s29_hands_on_goat", 3, 182.16, 188.10),
    (30, "s30_confession", 3, 188.10, 193.92),
    (31, "s31_confession_card", 3, 193.92, 215.44),
    (32, "s32_goat_led_away", 3, 215.44, 223.68),
    (33, "s33_empty_horizon_card", 3, 223.68, 229.92),
    (34, "s34_riddle_recap", 4, 229.92, 239.20),
    (35, "s35_two_kids_card", 4, 239.20, 246.24),
    (36, "s36_two_shadows_one_flame", 4, 246.24, 255.40),
    (37, "s37_split_two_things", 4, 255.40, 264.60),
    (38, "s38_walking_home_dusk", 4, 264.60, 269.40),
    (39, "s39_honesty_close", 5, 269.40, 276.90),
    (40, "s40_people_home_clean", 5, 276.90, 288.00),
    (41, "s41_repetition_vignettes", 5, 288.00, 297.20),
    (42, "s42_basin_linen_ready", 5, 297.20, 307.50),
    (43, "s43_shadow_on_tent_wall", 5, 307.50, 314.00),
    (44, "s44_pointing_smoke", 5, 314.00, 323.90),
    (45, "s45_sign_before_veil", 5, 323.90, 327.00),
    (46, "s46_aged_unchanged_veil", 6, 327.00, 334.50),
    (47, "s47_light_arrives", 6, 334.50, 342.60),
    (48, "s48_small_basin_towering_veil", 6, 342.60, 352.88),
    (49, "s49_veil_detail_card", 6, 352.88, 363.36),
    (50, "s50_the_shadow", 6, 363.36, 368.30),
    (51, "s51_jesus_pivot", 6, 368.30, 382.08),
    (52, "s52_jesus_entering_formal", 6, 382.08, 392.48),
    (53, "s53_the_cross", 6, 392.48, 399.00),
    (54, "spread54_thread_leaf", 6, 399.00, 411.68),
    (55, "spread55_isaiah536", 6, 411.68, 415.60),
    (56, "s56_the_answer", 6, 415.60, 426.30),
    (57, "s57_without_the_gate", 6, 426.30, 436.80),
    (58, "s58_gate_card", 6, 436.80, 444.48),
    (59, "s59_no_chair", 6, 444.48, 454.00),
    (60, "s60_seated_glory", 6, 454.00, 461.28),
    (61, "s61_veil_recall", 6, 461.28, 468.90),
    (62, "s62_veil_torn", 6, 468.90, 475.84),
    (63, "s63_torn_veil_card", 6, 475.84, 482.08),
    (64, "s64_empty_hands", 7, 482.08, 489.50),
    (65, "s65_ritual_uninks", 7, 489.50, 501.00),
    (66, "s66_high_priests_face", 7, 501.00, 507.60),
    (67, "s67_same_road_lit", 7, 507.60, 516.60),
    (68, "s68_east_west_horizon", 7, 516.60, 526.08),
    (69, "s69_east_west_card", 7, 526.08, 532.32),
    (70, "s70_veil_held_open", 7, 532.32, 538.70),
    (71, "s71_the_way_open", 7, 538.70, 547.20),
    (72, "s72_boldness_card", 7, 547.20, 553.20),
    (73, "s73_aaron_steps_aside", 7, 553.20, 558.30),
    (74, "s74_every_year_gone", 7, 558.30, 571.00),
    (75, "s75_the_reach", 7, 571.00, 583.30),
    (76, "s76_already_inside", 7, 583.30, 588.64),
]

# Last spoken word ends here (spread 76's plan-estimated end); the real
# value is corrected against the alignment in _s5b. INV-26 landing hold
# (>=3.0s, audio=video) is added ON TOP of whichever value is final.
LAST_WORD_END_ESTIMATE = 588.64
LANDING_HOLD_S = 3.0  # -> TOTAL ~591.64, the plan's own stated minimum

# Every one of the 76 spreads has a real rendered clip (unlike bronze_serpent
# _long's one static-hold landing) -- see RESUME.md 2026-08-04: s76 got its
# own dynamic_cam3d push rather than a bare static hold. Nothing here.
ALWAYS_STATIC_HOLD = set()

by_name = {name: (num, beat, start, end) for num, name, beat, start, end in SPREADS}
by_num = {num: (name, beat, start, end) for num, name, beat, start, end in SPREADS}
