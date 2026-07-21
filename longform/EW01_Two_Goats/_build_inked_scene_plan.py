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
        "Aaron in white linen standing perfectly still in thick darkness before the "
        "faint golden glow of the mercy seat, the sprinkling already finished: his arm "
        "lowered at his side, the shallow bronze basin held level and steady, its blood "
        "dark, settled and motionless; a few small already-fallen droplets resting dry "
        "and static on the stone floor; seen from behind and side, the quiet after the "
        "act, nothing falling, nothing flowing."
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
SCAR = (" Each of his palms bears a single small quiet healed nail scar, a simple "
        "dark oval mark on otherwise smooth unmarked skin, hands and wrists clean.")
GRAY = ("the aged high priest with long gray hair and a full gray beard")
FIXES_APPEND = {   # appended to the subject_block
    17: SCAR, 18: SCAR, 20: SCAR, 22: SCAR, 25: SCAR,
    9: " The priest is " + GRAY + ", the same aged man throughout the film.",
    3: " The walking priest is " + GRAY + ", seen from behind.",
    14: " Aaron and every ghosted echo of him are " + GRAY + ".",
    8: " The stone of the altar pedestal is clean and dry.",
    12: " The setting sun hangs small and distant in the sky, well away from his face, his eyes calm and human.",
}
FIXES_REPLACE = {  # whole-block rewrites where the composition itself failed
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
         "watchtowers behind the rampart wall, warm evening haze." + SCAR),
}

for s in plan["scenes"]:
    if s["id"] in REDESIGN:
        s["subject_block"] = REDESIGN[s["id"]]
        s["_redesign_note"] = ("blood-rite still redesigned to a settled/completed "
                               "state before the ink rebuild (2026-07-21) — i2v models "
                               "complete mid-action blood into growing streams")
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
