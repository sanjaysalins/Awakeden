"""Port the LOCKED EW01 Two Goats scene plan (25 scenes) from the archived oil
production to the inked graphic-novel rebuild, per the Bronze Serpent precedent
(longform/04_The_Bronze_Serpent/_build_inked_scene_plan.py) and the 2026-07-20
user call: "archive every work we have done with oil painting... we will
reanimate them all in the new comic style". $0, no render.

Scene CONTENT (subject/camera/atmos/timing/movement) is unchanged, with ONE
deliberate exception, user-approved 2026-07-21 with the migration budget:
scenes 8 and 14 (the blood-rite pair) are redesigned from mid-action blood
(arm raised to sprinkle / active basin) to SETTLED, completed states — the
clip-QC repair batch proved every i2v model completes mid-action blood into
growing streams (memory living-light-no-fresh-blood; _qcfix_state history).

EW01's plan carries no baked style wrapper (style_base is null; subject_blocks
are pure content) — the inked look comes from config.STYLE_REGISTRY at render
time, exactly like the Bronze rebuild's renderer.

Writes v1/visual_16x9_inked/scene_plan.json.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE / "v1"
SRC = V1 / "_archived_oil_baroque" / "visual_16x9" / "scene_plan.json"
OUT_DIR = V1 / "visual_16x9_inked"
OUT_DIR.mkdir(exist_ok=True)

plan = json.loads(SRC.read_text(encoding="utf-8"))

# Blood-rite redesigns: same scene, same beat, the action already COMPLETE so
# no animator can "finish" it. Everything liquid is settled and still.
REDESIGN = {
    8: (
        # Blood removed ENTIRELY (2026-07-21, clip-QC): the earlier "settled "
        # droplets/dark blood" still had red on the floor that Seedance grew into a "
        # flowing drip (living-light-no-fresh-blood). No red anywhere now -> nothing "
        # to animate. Beat carried by the mercy-seat glow + reverent posture.
        "Aaron in white linen standing perfectly still in thick darkness before the "
        "faint golden glow of the mercy seat, the rite already finished and quiet: his "
        "arm lowered gently at his side, an empty shallow bronze basin resting level "
        "and still in his hand; seen from behind and side, the hush after the act; the "
        "pale stone floor entirely clean, smooth, dry and unmarked; only the soft "
        "golden glow and a thin thread of rising incense in the still air."
    ),
    14: (
        "A unified tableau of weary repetition: Aaron, in plain white linen, at the "
        "altar, repeated as the SAME one man in soft ghosted echoes receding into the "
        "dark — the same act year upon year, not different priests; the same two goats "
        "faintly doubled; turning seasons hinted in the sky; the same bronze basin "
        "resting closed and still on the altar stone, its contents dark, settled and "
        "motionless; the worn altar stone; soft vignettes melting into one dim "
        "recurring canvas; nothing dripping, nothing poured, no liquid in motion; no "
        "breastplate, no other priests or bearded men."
    ),
}

# Eye-audit fixes (2026-07-21, first ink render pass). All positive-only
# phrasing — seedream has no negative channel (memory seedream-no-negative-channel).
# ROUND 2 (2026-07-21, re-audit of the first re-roll): the round-1 SCAR text
# still rendered a stitched/starburst wound-icon on all 6 Christ-hand stills
# (17,18,19,20,22,25) — including scene 19, which never carried the older
# "visible nail-wounds in his hands" boilerplate, only this SCAR sentence.
# So the words "nail scar"/"wound" themselves are drawing the icon, not just
# the boilerplate. Round 2 drops "scar"/"wound"/"nail" entirely and the
# boilerplate phrase is stripped from the ported base text before SCAR is
# appended.
# CLEAN HANDS decision (user, 2026-07-21, after 4 failed scar-render rounds):
# the seedream ink style cannot reliably render a subtle nail scar — every
# wording produced either a barbed star, multiple orange sunbursts (scene 17
# had 4 on the knuckles, scene 25 had 3 on the palm), or a band-aid patch
# (scenes 19/20). User chose CLEAN, unmarked hands on all 6 Christ close-ups;
# the wound theology is carried by the narration, not the stills. So: strip the
# old oil-era "with visible nail-wounds" boilerplate from EVERY scene and append
# NO scar text. (SCAR/SCAR_MATTE retired — kept only in git history.)
STRIP_PHRASES = (" with visible nail-wounds in his hands",)
GRAY = ("the aged high priest with long gray hair and a full gray beard")

# ROUND 3 (2026-07-21, user's own eye-check of the gallery via the notes box):
# (a) scene 2's two hands releasing the breastplate read with wrong hand
#     position/anatomy — add an explicit natural-anatomy line rather than
#     leaving "two weathered hands" to the model's own composition.
# (b) scene 12 was NEVER given the GRAY identity fix that 3/9/14 got, even
#     though it's the same recurring witness — root cause of "he looks
#     different here" (missed in round 1's identity sweep).
# (c) scene 19's two raised hands read anatomically backwards (thumb/finger
#     placement) — add the same natural-anatomy line as (a).
HANDS = (" Both hands are ordinary human hands, thumb and four fingers each in "
         "their own natural anatomical place, wrists straight, nothing bent, "
         "fused or reversed.")
FIXES_APPEND = {   # appended to the subject_block (scar entries removed — clean hands)
    9: " The priest is " + GRAY + ", the same aged man throughout the film.",
    3: " The walking priest is " + GRAY + ", seen from behind.",
    14: " Aaron and every ghosted echo of him are " + GRAY + ".",
    8: " The stone of the altar pedestal is clean and dry.",
    12: (" The setting sun hangs small and distant in the sky, well away from "
         "his face, his eyes calm and human. Aaron is " + GRAY + ", the same "
         "aged man throughout the film."),
    2: HANDS,
}
FIXES_REPLACE = {  # whole-block rewrites where the composition itself failed
    # Scene 18: the archived block's "absolutely NO blood, no gore, no red"
    # DREW a blood smear on the goat (seedream has no negative channel — naming
    # blood/red draws it). Rewrite positively: goat at rest, clean coat, asleep.
    18: ("A unified fulfillment canvas: the figure of Christ central, reverent, "
         "arms open; soft-edged to the left, a single goat lying still and "
         "peacefully at rest upon the low stone altar as if asleep, its pale "
         "coat clean and whole (the price paid); soft-edged to the right, the "
         "scapegoat walking away into the pale wilderness (the guilt carried "
         "off); the two resolving into the one Priest at the centre; a faint "
         "cross of soft light above Christ. Ancient biblical-period Near-Eastern "
         "setting, calm and reverent. Christ wears a simple luminous undyed "
         "white robe; he is the risen Lord, in a plain robe, not any "
         "high-priestly breastplate, ephod or jewelled vestments."),
    # Scene 11: the "slain goat in blood-red light" rendered a pool of gore
    # (user flagged nsfw). Same call the user made on the oil EW01 (2026-06-26):
    # the goat lies at rest, no blood/gore, the red is FIRELIGHT not blood.
    11: ("One frame holding the riddle: on the left, the first goat lying "
         "still and peacefully at rest on the low altar step, as if asleep, "
         "its pale coat clean and whole, bathed in the warm red glow of the "
         "altar fire and rising smoke (the price); on the right, the live "
         "goat facing an open pale road into the waste (the guilt carried "
         "off); the altar standing dark between them. A single unified "
         "canvas, soft transition, no hard divider, calm and reverent, the "
         "stone clean and dry."),
    5: ("The Ark of the Covenant alone in the deep darkness of the Holy of Holies: "
        "a gold-covered chest with two golden cherubim wrought upon its lid, their "
        "wings stretched toward each other over the mercy seat, a radiant cloud of "
        "glory glowing above it; tabernacle curtain walls receding into shadow; the "
        "aged high priest prostrate on the stone floor before it, tiny beneath the "
        "light; the room bare and holy, only the Ark, the cloud, and the man."),
    6: ("The aged high priest, long gray hair and full gray beard, head bowed in "
        "grief; behind him in ghosted memory panels his two grown sons in white "
        "priestly linen lie still on scorched stone, their bodies whole and "
        "unmarked, thin gray smoke drifting up from the blackened ground around "
        "them, censers fallen beside their open hands; shrouded biers carried away "
        "into darkness; the ground charred, the air full of ash and silence."),
    19: ("The glowing risen Christ seen from behind, standing on a dusty road "
         "outside the city wall, looking up the bare hill toward the closed gate. "
         "Jerusalem's skyline is low flat-roofed stone houses and simple square "
         "watchtowers behind the rampart wall, warm evening haze." + HANDS),
}

for s in plan["scenes"]:
    if s["id"] in REDESIGN:
        s["subject_block"] = REDESIGN[s["id"]]
        s["_redesign_note"] = ("blood-rite still redesigned to a settled/completed "
                               "state before the ink rebuild (2026-07-21) — i2v models "
                               "complete mid-action blood into growing streams")
    # CLEAN HANDS: strip the old oil-era nail-wound boilerplate from EVERY scene
    # (not just ones with a fix entry) so the Christ close-ups render clean hands.
    for phrase in STRIP_PHRASES:
        if phrase in s["subject_block"]:
            s["subject_block"] = s["subject_block"].replace(phrase, "")
            s["_fix_note"] = "clean-hands strip (2026-07-21): see _build_inked_scene_plan.py"
    if s["id"] in FIXES_REPLACE:
        s["subject_block"] = FIXES_REPLACE[s["id"]]
        s["_fix_note"] = "eye-audit rewrite (2026-07-21): see _build_inked_scene_plan.py"
    elif s["id"] in FIXES_APPEND:
        s["subject_block"] = s["subject_block"].rstrip(". ") + "." + FIXES_APPEND[s["id"]]
        s["_fix_note"] = "eye-audit append (2026-07-21): see _build_inked_scene_plan.py"

plan["style_base"] = None    # style from config.STYLE_REGISTRY[VISUAL_STYLE] at render time
plan["style_tail"] = None
plan["image_provider"] = "hf"
plan["animation"] = {"model": "tiered", "aspect": "16:9",
                     "note": "Seedance 1.5 Pro for calm single-figure panels, "
                             "Kling 3.0 for action/crowd/complexity (comic-grid-cost-tiered-animation)"}
plan["film_name"] = "EW01_Two_Goats_16x9_inked.mp4"
plan["_migration_note"] = (
    "inked graphic-novel rebuild, 2026-07-21 — ported from the archived oil "
    "production (v1/_archived_oil_baroque/visual_16x9/scene_plan.json); scene "
    "content/camera/timing unchanged except the user-approved blood-rite "
    "redesigns of scenes 8 and 14; per memory graphic-novel-style-migration "
    "and the Bronze Serpent precedent.")

out = OUT_DIR / "scene_plan.json"
out.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
n = len(plan["scenes"])
print(f"ported {n} scenes ({len(REDESIGN)} blood-rite redesigns) -> {out}")
