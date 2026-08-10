"""Seed of the Woman LONG's finish_config.py -- the only per-episode
content _finish_long.py needs. Written for the real 71-spread film
(2026-08-10), replacing the POC30 5-spread validation stub (archived to
_poc30_finish_test_archive/, its own job -- proving _finish_long.py --
already done and no longer needed).

SCORE reuses Day of Atonement's proven 3-mood arc (same tracks' _b takes
where they're shorter) -- this episode's own arc is thematically close
(Eden/loneliness open -> a promise breaking into judgment -> grace rising
to the CTA landing mirrors DoA's wilderness -> Holy-of-Holies stillness ->
grace-rise shape) and it's the only real precedent this project has for
scoring a film at this length. Chose the SHORTER _b take of the first two
moods (lonely_searching_b 194.5s, glory_holy_stillness_b 168.0s) rather
than DoA's own _a takes (213.6s/223.2s): run_score() chains full tracks
then truncates at the film's own total duration, so this episode's
shorter 500.5s runtime (vs DoA's 591.0s) would otherwise cut sacred_grace_
rise_b off at only ~34% in -- likely before its own "climax near the end"
per the catalogue's own description, undermining exactly the landing
moment that matters most. The _b-take swap gets sacred_grace_rise_b to
~66% through (503.5 - (194.5-6) - (168.0-6) = 141.0s of its own 229.9s),
close to DoA's own validated ~74%. Real math, not guessed -- but still
worth an EAR check before calling it locked (dyslexic-user standing
preference: review audio by listening, not by spec). outro_s=3.0 (not
DoA's 2.5) per the now-current INV-26 landing-hold standard -- DoA shipped
under the OLDER 2.5s rule and per that standard's own note is not being
retrofitted; this is a NEW piece so it gets the current 3.0s bar.

SFX_CUES: one quiet dawn/garden bed under the whole film (matches this
world's own visual dawn-lit palette throughout, incl. the closing
eden_to_cross image) plus specific event accents tied to real spread
content -- verified against sound_library/clips's actual inventory, not
guessed names. No heavenly_choir_soft anywhere (locked rule
feedback-no-choir-pad-under-score -- the score alone carries the landing's
holy lift).

CAPTIONS.skip_spreads: every spread with real baked-in lettering, taken
directly from _devices.py's VERSE_CARDS + SPECIAL_CARDS + EXTERNAL_LETTERING
dicts (not guessed) so word-captions never double up on drawn text."""

STEM = "SEEDOFTHEWOMAN_LONG_living_sketchbook"

SCORE = {
    "segments": ["lonely_searching_b", "glory_holy_stillness_b", "sacred_grace_rise_b"],
    "xfade_s": 6.0,
    "gain_db": -11.0,
    "outro_s": 3.0,
}

SFX_CUES = [
    ("dawn_morning_warm", "ALL", -24),
    ("footsteps_dirt_approach", "s04_god_walking", -16),
    ("rumble_deep_sub", "s10_judgment_falls", -18),
    ("thunder_low_roll", ("s19_curse_card", "s20_pure_curse"), -18),
    ("impact_low_boom", "s48_heel_strike", -14),
    ("impact_low_boom", "s49_head_crush", -11),
    ("nail_strike_single", "s50_that_is_the_cross", -13),
    ("stone_roll_tomb", "s57_empty_tomb", -12),
]

CAPTIONS = {
    "skip_spreads": [
        "s03_verse_card", "s07_beguiled_card", "s19_curse_card", "s22_promise_card",
        "s26_her_seed_study", "s29_fulness_card", "s31_holy_thing_card",
        "s34_naming_serpent", "s35_naming_mission", "s36_naming_crushing",
        "s47_two_wounds_card", "s53_through_death_card", "s56_triumph_card",
    ],
    "segment_seconds": 60.0,
}

WATERMARK = True
