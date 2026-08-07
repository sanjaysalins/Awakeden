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
}

SPECIAL_CARDS = {}

EXTERNAL_LETTERING = set()

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
    "s16_sentencing_tableau": {"device": "hunt_and_lock", "scope": "full",
                                "params": {"target_frac": [0.68, 0.85]}},
}

SPECIAL_CARDS_LANDING = {}  # s05 handled by its own bespoke render, not a table entry

TRANSITION_OVERRIDES = {}
NO_TRANSITION_SEAMS = set()
