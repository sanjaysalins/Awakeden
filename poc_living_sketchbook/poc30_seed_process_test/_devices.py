"""POC30 Seed -- device table (process-validation test). Mirrors
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
    "s01_something_wrong": {"device": "dramatic_spotlight", "scope": "full", "params": {}},
    "s04_god_walking": {"device": "breath_synced_halo", "scope": "full", "params": {}},
}

SPECIAL_CARDS_LANDING = {}  # s05 handled by its own bespoke render, not a table entry

TRANSITION_OVERRIDES = {}
NO_TRANSITION_SEAMS = set()
