"""Seed of the Woman LONG -- device table. Spreads 1-5 promoted from the
POC30 process-validation test (memory `day-of-atonement-retro-learnings`);
remaining spreads to be added as the full plan is authored. Mirrors
day_of_atonement/_devices.py's dict shapes so panel_animator/motion_lint.py
and poc_living_sketchbook/_layer_check.py both work unmodified against this
episode too.
"""

BODY_SIZE = 40

# filled in AFTER first proving _layer_check.py FAILs on an empty dict here
# (fix #4's acceptance test -- red before, green after). KJV Gen 3:8
# verbatim, verified against data/kjv_cache.json wording.
VERSE_CARDS = {
    "s03_verse_card": {
        "combo": "A",
        "lines": [
            [("And they heard the voice of the LORD God", BODY_SIZE)],
            [("walking in the garden in the cool of the day:", BODY_SIZE)],
            [("and Adam and his wife ", BODY_SIZE), ("hid themselves", 70)],
            [("...from the presence of the LORD God.", BODY_SIZE)],
        ],
    },
    # Gen 3:13b KJV verbatim, verified against data/kjv_cache.json wording.
    "s07_beguiled_card": {
        "combo": "A",
        "lines": [
            [("The serpent beguiled me,", BODY_SIZE)],
            [("and I did eat.", BODY_SIZE)],
        ],
    },
    # Gen 3:14 (narration's own quoted excerpt, narration.md line 29) KJV
    # verbatim, verified against data/kjv_cache.json wording.
    "s19_curse_card": {
        "combo": "A",
        "lines": [
            [("And the LORD God said unto the serpent,", BODY_SIZE)],
            [("Because thou hast done this,", BODY_SIZE)],
            [("thou art cursed above all cattle,", BODY_SIZE)],
            [("and above every beast of the field.", BODY_SIZE)],
        ],
    },
}

# s22_promise_card (Illuminated Rubric, Gen 3:15 full verse, red-letter --
# narration.md: "Multi-voice: the_LORD voices Gen 3:14-15") -- doesn't fit
# the combo A/B/C system (LAW 1 whole-block arrival + gold dropped cap),
# dispatches via build_s22() directly, same as day_of_atonement's own
# s16/s52 cards.
SPECIAL_CARDS = {
    "s22_promise_card": {"kind": "illuminated_rubric"},
}

# batch 4 (2026-08-08) -- real lettering built by standalone functions in
# _s6_assemble.py outside the VERSE_CARDS/SPECIAL_CARDS dict dispatch:
# s26 (hand-lettered study copy via render_line_png), s29 (Illuminated
# Rubric, Gal 4:4), s31 (Luke 1:35b letters over s30's art), s34/s35 (the
# Naming Docket plate, real Constantia typography via render_dom_clip.py).
# batch 5 adds s36 (the same Naming Docket plate, entry 3/3).
EXTERNAL_LETTERING = {
    "s26_her_seed_study",
    "s29_fulness_card",
    "s31_holy_thing_card",
    "s34_naming_serpent",
    "s35_naming_mission",
    "s36_naming_crushing",
}

DEVICE_ASSIGNMENTS = {
    # FIXED 2026-08-07 -- the independent-review panel caught s04 listed
    # here as "breath_synced_halo" while _s6_assemble.py actually builds it
    # via build_clip_hold() on the real Seedance clip -- a real
    # plan/code/motion_lint/layer_check mismatch, not just documentation
    # drift. This dict now only lists spreads that ACTUALLY dispatch
    # through render_device()/hunt_and_lock -- real-clip spreads (s02, s04,
    # s06) have no entry here, matching how s02 was already correctly
    # absent.
    "s01_something_wrong": {"device": "dramatic_spotlight", "scope": "full", "params": {}},
    # key matches _spread_table.py's canonical spread-16 name ("Now watch
    # closely" -- the underlying still file keeps its original descriptive
    # filename, s16_sentencing_tableau.png, only the dict key changed
    # (real key/spread-table mismatch found reconciling timing 2026-08-07 night).
    # RETUNED (2026-08-09, hero-stills cinematic pass): the still was
    # redesigned (serpent now large in the near-foreground lower-left,
    # not small at the bottom edge) -- re-measured via panel_animator/
    # bbox_sheet.py's grid overlay against the ACTUAL new render, not
    # eyeballed. Old value [0.68, 0.85] targeted the OLD composition's
    # small bottom-right serpent and no longer applies.
    "s16_watch_closely": {"device": "hunt_and_lock", "scope": "full",
                           "params": {"target_frac": [0.44, 0.565]}},
    # batch 2 (2026-08-08) -- bbox/anchor picked via panel_animator/
    # bbox_sheet.py against the real rendered still, per SKILL.md sec.8b
    # gate #2, not eyeballed.
    "s09_unexpected_place": {"device": "candle_only", "scope": "full",
                              "params": {"anchor_frac": [0.52, 0.79]}},
    "s13_the_fruit": {"device": "dramatic_spotlight", "scope": "full",
                       "params": {"bbox": [27, 20, 36, 65]}},
    "s14_death_enters": {"device": "wash_creep_advance", "scope": "full", "params": {}},
    # amp raised 2026-08-08: motion_lint FROZEN-SPREAD at fg=12/bg=4
    # (p95=0.117, just under the 0.15 threshold) -- not a scale artifact,
    # a real too-subtle render.
    "s15_the_breach": {"device": "parallax_25d", "scope": "full",
                        "params": {"fg_amp": 24.0, "bg_amp": 9.0}},
    # s21: gold thread's FIRST appearance in the episode, drawn over s20's
    # own already-approved extreme-close-up art (per _PLAN.md's own device
    # column, "Thread draw-on ($0)" -- never a new render, see the note in
    # _s2_stills.py). Endpoints picked to cross diagonally through the
    # curse-dark scale texture.
    # width/fade_dur tightened 2026-08-08: motion_lint FROZEN-SPREAD at the
    # original 4px-wide thread + 2.2s fade (p95=0.036) -- a thin gold line
    # on a 1920x1080 frame barely moves the whole-frame luminance-diff
    # metric no matter how real the animation is. Thicker stroke + a
    # punchier arrival window, not a cosmetic change.
    "s21_gold_woven_in": {"device": "thread_device", "scope": "full",
                           "params": {"p0_frac": [0.12, 0.85], "p1_frac": [0.85, 0.15],
                                      "fade_start": 0.5, "fade_dur": 0.9, "swell_time": 3.0,
                                      "width": 12}},
    # s23: s22's own card held -- sacred stillness, nothing moves but the
    # grain (line_boil) and the thread's faint gleam underneath.
    "s23_let_that_land": {"device": "line_boil_hold", "scope": "full",
                           "params": {"amount": 0.6}},
    # s25: the thread ALREADY drawn across s25's own art (per _PREFLIGHT.md:
    # "the thread rises past the TOP edge") -- gleam-pass only, no fade-in
    # (it's meant to already be visible, per _PLAN.md's device column).
    # width widened same reason as s21 (FROZEN-SPREAD, p95=0.035).
    # width widened again 2026-08-08 (12->20px): first widen only got
    # p95=0.104, still under the 0.15 threshold -- a long diagonal thread
    # is real motion but still a small fraction of a 1920x1080 frame.
    "s25_promise_in_curse": {"device": "thread_device_gleam", "scope": "full",
                              "params": {"p0_frac": [0.20, 0.92], "p1_frac": [0.55, -0.05],
                                         "swell_time": 3.2, "width": 20}},
}

SPECIAL_CARDS_LANDING = {}  # s05 handled by its own bespoke render, not a table entry

TRANSITION_OVERRIDES = {}
NO_TRANSITION_SEAMS = set()
