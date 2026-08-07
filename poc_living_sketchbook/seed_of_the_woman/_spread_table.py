"""POC30 Seed -- the one shared source of truth for the 5-spread table,
mirroring day_of_atonement/_spread_table.py's exact pattern/role. Real
forced-aligned timing (`_alignment.json`), not estimated -- this test
excerpt is short enough that no plan-vs-alignment correction pass is
needed the way the full 76-spread episodes require.
"""

# (spread_num, name, beat, start_s, end_s) -- from _PLAN.md
SPREADS = [
    (1, "s01_something_wrong", 1, 0.0, 5.8),
    (2, "s02_the_hiding", 1, 5.8, 11.9),
    (3, "s03_verse_card", 1, 11.9, 24.0),
    (4, "s04_god_walking", 1, 24.0, 30.7),
    (5, "s05_where_art_thou", 1, 30.7, 33.03),
]

LAST_WORD_END_ESTIMATE = 32.424  # real alignment, "thou?" ends here
LANDING_HOLD_S = 0.6  # short test excerpt -- not a real INV-26 landing, just enough tail to not cut abruptly

ALWAYS_STATIC_HOLD = set()

by_name = {name: (num, beat, start, end) for num, name, beat, start, end in SPREADS}
by_num = {num: (name, beat, start, end) for num, name, beat, start, end in SPREADS}
