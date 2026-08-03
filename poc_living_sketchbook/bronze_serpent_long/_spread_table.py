"""Bronze Serpent LONG -- the one shared source of truth for the 68-spread
table (number, name, beat, plan-estimated start/end, duration). Mirrors
`_build_review.py`'s own ROWS exactly (same numbers, same names) so the
galleries and the assembly stage never drift apart -- imported by both.

Start/end here are the _PLAN.md ESTIMATED windows (turn-boundary-exact,
sub-turn seams are estimates -- see _PLAN.md sec 1c/2). `_s6_align.py` +
`_s6b_spread_windows.py` correct the sub-turn seams against the real
forced-alignment word timings; this file is the un-corrected baseline they
start from.

DEVICES intentionally NOT included here for the v1 "simple cut" pass
(candle-only, blue-line, impact-burst, camera drift, lift_away, tear_hole,
dissolve) -- those are a deliberate polish-pass-2 layer per the user's own
2026-08-02 call ("simple first cut, polish after"), added on TOP of this
base timeline once it exists and has been seen, not baked in now.
"""

# (spread_num, name, beat, start_s, end_s)
SPREADS = [
    (1, "s01_wide", 1, 0.40, 7.50),
    (2, "s02_triptych", 1, 7.50, 17.00),
    (3, "s03_eyes_haunted", 1, 17.00, 21.50),
    (4, "s04_icon_pole", 1, 21.50, 27.50),
    (5, "s05_graves", 1, 27.50, 32.50),
    (6, "s06_dying_hand_eye", 1, 32.50, 37.10),
    (7, "s07_ungrateful_camp", 2, 37.10, 43.00),
    (8, "s08_wandering_column", 2, 43.00, 53.00),
    (9, "s09_manna_scorned", 2, 53.00, 61.52),
    (10, "s10_vc_discouraged", 2, 62.22, 67.50),
    (11, "s11_crowd_angry", 2, 68.20, 76.04),
    (12, "s12_vc_wherefore", 2, 76.74, 87.62),
    (13, "s13_vignette_calf", 2, 88.32, 98.00),
    (14, "s14_serpent_hint", 2, 98.00, 104.16),
    (15, "s15_vc_fiery_serpents", 2, 104.86, 112.06),
    (16, "s16_bite_closeup", 2, 112.76, 117.00),
    (17, "s17_vignette_collapse", 2, 117.00, 125.00),
    (18, "s18_moses_empty_hands", 2, 125.00, 131.61),
    (19, "s19_people_kneel", 3, 131.61, 137.56),
    (20, "s20_vc_we_have_sinned", 3, 138.26, 147.38),
    (21, "s21_moses_intercede", 3, 148.08, 154.00),
    (22, "s22_moses_listening", 3, 154.00, 163.84),
    (23, "s23_lord_presence", 3, 164.54, 169.00),
    (24, "s24_vc_make_thee", 3, 169.00, 177.18),
    (25, "s25_moses_empty_negation", 3, 177.88, 184.00),
    (26, "s26_moses_resolve_serpent", 3, 184.00, 192.00),
    (27, "s27_hands_gather_ore", 3, 192.00, 196.28),
    (28, "s28_forge_acting", 3, 196.98, 204.00),
    (29, "s29_pole_first_healing", 3, 204.00, 208.98),
    (30, "s30_payoff_fever_breaks", 3, 209.68, 228.25),
    (31, "s31_moses_why_serpent", 4, 228.25, 233.41),
    (32, "s32_pole_silhouette_dusk", 4, 233.41, 259.03),
    (33, "s33_vignette_universal", 4, 259.03, 272.61),
    (34, "s34_moses_walking_dusk", 4, 272.61, 284.83),
    (35, "s35_moses_honest_close", 5, 284.83, 293.25),
    (36, "s36_proud_man_turns_away", 5, 293.25, 314.62),
    (37, "s37_calf_flashback", 5, 314.62, 325.48),
    (38, "s38_dread_image", 5, 325.48, 344.31),
    (39, "s39_moses_sleepless_candle", 5, 344.31, 350.29),
    (40, "s40_moses_resolve_returning", 5, 350.29, 364.51),
    (41, "s41_moses_long_road", 5, 364.51, 382.80),
    (42, "s42_hands_finish_forge", 5, 382.80, 387.84),
    (43, "s43_insert_scholars_margin2", 6, 388.54, 402.14),
    (44, "s44_shadow_cross", 6, 402.84, 410.00),
    (45, "s45_golgotha_wide", 6, 410.00, 420.00),
    (46, "s46_thesis_pair", 6, 420.00, 425.00),
    (47, "s47_golgotha_midshot", 6, 425.00, 433.48),
    (48, "s48_vc_curse_for_us", 6, 434.18, 441.54),
    (49, "s49_christ_radiant_begin", 6, 442.24, 451.00),
    (50, "s50_christ_close_words", 6, 451.00, 456.48),
    (51, "s51_christ_draw_all_men", 6, 457.18, 464.06),
    (52, "s52_moses_reflecting", 6, 464.76, 475.54),
    (53, "s53_moses_know_that_now", 6, 475.54, 478.92),
    (54, "s54_timeshift_enshrined", 6, 478.92, 486.11),
    (55, "s55_hezekiah_breaks", 6, 486.11, 493.51),
    (56, "s56_moses_affirms", 6, 493.51, 498.18),
    (57, "s57_bridge_moses_christ", 6, 498.18, 507.64),
    (58, "s58_vc_john316", 6, 508.34, 517.38),
    (59, "s59_moses_be_still", 7, 518.08, 524.00),
    (60, "s60_vignette_selfeffort", 7, 524.00, 532.00),
    (61, "s61_moses_thatisyou", 7, 532.00, 539.00),
    (62, "s62_moses_neverasked", 7, 539.00, 544.50),
    (63, "s63_vignette_least_last_child", 7, 544.50, 553.00),
    (64, "s64_moses_sit_with_that", 7, 553.00, 559.00),
    (65, "s65_christ_open_invite", 7, 559.00, 565.00),
    (66, "s66_moses_direct_question", 7, 565.00, 576.00),
    (67, "s67_insert_gilded_proclamation2", 7, 576.00, 585.00),
    (68, "s68_landing", 7, 585.00, 590.08),
]

# Last spoken word ends here (spread 68's plan-estimated end); the real
# value is corrected against the alignment in _s6b. INV-26 landing hold
# (>=3.0s, audio=video) is added ON TOP of whichever value is final.
LAST_WORD_END_ESTIMATE = 590.08
LANDING_HOLD_S = 3.22   # -> TOTAL 593.30, matches the design's own accounting

# Spreads with no generative clip -- built by other means (deterministic
# push-ins already at full window duration, or a plain static hold).
ALWAYS_STATIC_HOLD = {"s68_landing"}  # no clip at all; hold the still

by_name = {name: (num, beat, start, end) for num, name, beat, start, end in SPREADS}
by_num = {num: (name, beat, start, end) for num, name, beat, start, end in SPREADS}
