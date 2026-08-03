"""living-sketchbook -- Bronze Serpent LONG pilot, step 2 (FULL BATCH).

Source: `poc_living_sketchbook/bronze_serpent_long/_PLAN.md` -- the 68-spread
plan for the first full-length living-sketchbook film. Follows the exact
code pattern of `poc_living_sketchbook/bronze_serpent/_s2_stills.py` (the
SHORT's own stills script): same STYLE constant (verbatim), same repo-level
cast-bible anchor chaining, same FULLBLEED framing note, same run()/
resolve_refs()/main() shape, same retry-once-on-failure.

TEST GATE (2026-08-01) rendered s23_lord_presence + s37_calf_flashback --
both APPROVED, do not re-render (main() skips any existing file). This round
(2026-08-01, FULL BATCH) adds the remaining 66 spreads from the plan's
68-row table. JESUS / PEOPLE / BRONZE_SERPENT constants are reused VERBATIM
from `poc_living_sketchbook/bronze_serpent/_s2_stills.py` (the short's own
proven cast text) per the batch instructions. HEZEKIAH is new (2 Kings
18:2 -- a YOUNG king in his mid-to-late twenties, NOT elderly).

Multi-pose identity lock (SKILL.md sec.2): every Moses spread chains BOTH
the repo anchor (moses_ref.png) AND the approved in-episode s23_lord_presence
render as a second reference; every Jesus spread chains BOTH the repo
anchor (jesus_ref.png) AND the short's approved s10_golgotha render as a
second reference.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s2_stills.py
"""
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "LS_BronzeSerpentLong"
HERE = Path(__file__).resolve().parent
WORLD_CAST = HERE.parent / "cast"          # repo-level cast-bible (shared across episodes)
SHORT_STILLS = HERE.parent / "bronze_serpent" / "stills"  # the short's own approved renders
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

MOSES_REF = WORLD_CAST / "moses_ref.png"                  # elder, ~120yo, used for EVERY spread incl. the golden-calf flashback (see cast/MOSES.md)
MOSES_REF2 = OUT / "s23_lord_presence.png"                 # approved in-episode Moses pose -- multi-pose identity lock (SKILL.md sec.2)
JESUS_REF = WORLD_CAST / "jesus_ref.png"
JESUS_REF2 = SHORT_STILLS / "s10_golgotha.png"             # the short's approved narrative-scale Jesus -- multi-pose identity lock

# MOSES text, AGE CORRECTED 2026-08-01 (was "in his eighties" -- wrong; KJV
# gives explicit numbers: Exodus 7:7 = 80 at the Exodus, Deuteronomy 34:7 =
# 120 at death, Numbers 33:38 pins the Bronze Serpent to the fortieth year
# after the Exodus -- so ~120, not "eighties". Matches cast/MOSES.md verbatim.
MOSES = (
    "Moses: an elderly Hebrew man of about 120 years, at the very end of "
    "his life -- the aged lawgiver of Numbers, NOT the young Moses of the "
    "Exodus/burning-bush years -- his eye not dim, his natural force not "
    "abated (Deuteronomy 34:7), so drawn upright and vital despite his "
    "extreme age, never frail or feeble -- a broad weathered forehead, "
    "deep-set eyes beneath heavy grey brows, hollowed cheeks, a strong jaw "
    "beneath the beard, long white and grey hair swept back off the "
    "forehead and thinning at the crown, a long full white beard streaked "
    "with iron-grey reaching mid-chest, deeply sun-weathered leathery "
    "skin, an old man's spare sinewed frame -- still upright and "
    "strong-shouldered, never frail or youthful -- dark steady eyes "
    "weighted with authority and grief, large veined elder's hands, a "
    "plain undyed woolen robe with a coarse mantle draped over one "
    "shoulder, a woven cord girdle, plain leather sandals, always holding "
    "or beside a tall wooden staff worn smooth by decades of use. the SAME "
    "man as the reference image(s) -- identical face, beard, hair, and "
    "clothing."
)
# JESUS text -- reused VERBATIM from poc_living_sketchbook/bronze_serpent/_s2_stills.py
JESUS = (
    "Jesus: a Judean man in his early thirties, long dark wavy hair past "
    "the shoulders parted center, short close-cropped dark beard, a "
    "strong straight nose and defined cheekbones, warm deep brown eyes "
    "level and calm, sun-weathered olive skin, lean wiry-strong build, "
    "simple undyed homespun ankle-length tunic with a woven cord sash, "
    "leather sandals. the SAME man as the reference image(s) -- identical "
    "face, beard, hair, and clothing."
)
# PEOPLE text -- reused VERBATIM from the short's own script (at-most-three-
# sharp-faces crowd discipline).
PEOPLE = (
    "the stricken Israelites: ordinary wilderness-worn Hebrew men, women, "
    "and children in plain undyed tunics and mantles, unnamed and never "
    "repeated as named characters -- AT MOST three faces rendered with "
    "any individual detail anywhere in the frame, count them: no more "
    "than three -- every other figure present is turned away, downcast, "
    "or held in soft shadow so no further face reads as distinct, and "
    "there is no fourth or fifth clearly-detailed face anywhere, even "
    "partially hidden or turned away. Distress is shown ONLY through "
    "posture and gesture -- slumped shoulders, a hand pressed to an arm "
    "or leg, huddled closeness, faces turned down or away -- NEVER a "
    "visible wound, bite mark, snake attached to skin, or blood anywhere "
    "on any figure."
)
# Spread-specific EXACT-headcount crowds, ported from the short's proven
# PEOPLE_S04 pattern (an enumerated headcount + hard "no one else present"
# close closes the loophole the soft "at most three" wording left open).
PEOPLE_S17 = (
    "EXACTLY two figures and no more, in two soft-edged vignettes side by "
    "side within the one frame -- count them: (1) a strong grown man "
    "collapsed onto the sand, one arm outflung, eyes closed, his face "
    "turned to the side; (2) a mother kneeling apart from him, cradling a "
    "small child close against her chest, her head bowed low over the "
    "child -- both ordinary wilderness-worn Hebrews in plain undyed "
    "tunics, unnamed. There is NO third person, no fourth person, no "
    "partial figure, no extra head or body visible anywhere in the "
    "frame, even partially hidden or in the far background -- only these "
    "two vignettes and no one else. Distress is shown ONLY through "
    "posture -- a collapsed body, a protective embrace -- NEVER a "
    "visible wound, bite mark, snake attached to skin, or blood on "
    "either figure."
)
PEOPLE_S33 = (
    "EXACTLY three figures and no more, in three soft-edged vignettes "
    "arranged within the one frame -- count them: (1) a strong grown "
    "man, upright, lifting his face upward; (2) a young child, small, "
    "lifting their face upward in the same direction; (3) a dying elder, "
    "frail and reclined on a mat, lifting only their eyes upward in the "
    "same direction -- all three ordinary wilderness-worn Hebrews in "
    "plain undyed tunics, unnamed, each looking the same way as though "
    "at the same unseen point beyond the frame's edge. There is NO "
    "fourth person, no fifth person, no partial figure, no extra head or "
    "body visible anywhere in the frame -- only these three figures and "
    "no one else. Weakness is shown ONLY through posture, NEVER a "
    "visible wound, bite mark, snake attached to skin, or blood."
)
PEOPLE_S60 = (
    "EXACTLY three figures and no more, in three soft-edged vignettes "
    "within the one frame -- count them: (1) a strong man pacing and "
    "stamping his foot hard against the ground, jaw clenched, trying to "
    "walk the burning off; (2) a man pressing both his own hands hard "
    "against his own chest and arm, trying to press the fire out; (3) a "
    "man rubbing sand vigorously onto his own forearm, trying to scrub "
    "the burning away -- all three ordinary wilderness-worn Hebrew men "
    "in plain undyed tunics, unnamed, each visibly failing at his own "
    "remedy, each alone, not looking at each other or at anything beyond "
    "his own effort. There is NO fourth person, no fifth person, no "
    "partial figure, no extra head or body visible anywhere in the "
    "frame -- only these three figures and no one else. NEVER a visible "
    "wound, bite mark, snake attached to skin, or blood on any figure."
)
PEOPLE_S63 = (
    "EXACTLY three small figures and no more, tiny and distant in the "
    "lower portion of the frame, looking up toward the radiant figure "
    "above -- count them: (1) the least among them, a humble "
    "poorly-dressed figure; (2) the last, an elderly frail figure near "
    "the back; (3) a small child, mid-turn, just now turning their head "
    "upward to look -- all three ordinary wilderness-worn Hebrews, "
    "rendered small and mostly silhouetted at this distance, no "
    "individual facial detail needed. There is NO fourth figure, no "
    "fifth figure, no additional person visible anywhere in the frame "
    "-- only these three and no one else."
)
# BRONZE_SERPENT -- reused VERBATIM from the short's own script.
BRONZE_SERPENT = (
    "a serpent cast in plain dull bronze and copper, coiled around a "
    "tall wooden pole, catching only dull worked-metal highlights -- "
    "never gold; gold is reserved for Christ's glory alone in this "
    "episode, never for the serpent or its pole"
)
# HEZEKIAH -- NEW, single appearance (spread 55). AGE per §4 item 2 of the
# plan (2 Kings 18:2: "twenty and five years old when he began to reign";
# the Nehushtan-breaking sits in the same undated opening-reform block,
# before the chapter's first dated regnal year -- so a young, vigorous
# king, NOT an elderly "wise king" stereotype). No reference image needed
# (single appearance) -- canon text only, written in cast/MOSES.md's format.
HEZEKIAH = (
    "Hezekiah: a YOUNG king of Judah, in his mid-to-late twenties, "
    "vigorous and strong -- NOT an elderly or grey-bearded 'wise king' "
    "(2 Kings 18:2: twenty and five years old when he began to reign) -- "
    "a lean, energetic build, dark hair and a short dark beard with no "
    "grey, a youthful unlined face set with resolve and decisive "
    "purpose, dark steady eyes, a fine but not gaudy royal tunic in a "
    "deep dyed color, a woven belt, a simple plain gold circlet or no "
    "crown at all -- no elaborate crown, no jewels, no royal regalia "
    "beyond the plain circlet -- a young man's strong bared forearms, "
    "sandaled feet planted firmly, captured mid-motion breaking an idol "
    "-- deliberate and corrective, not violent or shameful."
)
# THE LORD's unseen presence -- translated into the living-sketchbook's own
# graphite/wash/gold-leaf register from ref_library/characters/THE_LORD.json's
# canonical oil/inked-style description ("the unseen presence of the LORD
# shown only as overwhelming radiant golden light ... a towering pillar of
# glory and shadow ... never a human face or body").
LORD_PRESENCE = (
    "the unseen presence of the LORD: NEVER a human face, NEVER a human "
    "body or silhouette of a body anywhere in the frame -- shown only as "
    "an overwhelming column of radiant light and billowing luminous cloud, "
    "rays breaking outward from within it, rendered in the same loose "
    "graphite-and-wash sketch linework as the rest of the page but with "
    "every scrap of gold-leaf accent in the composition concentrated into "
    "this one pillar of glory -- light and shadow given towering form, no "
    "figure, no face, no limbs, no eyes"
)
# The golden calf -- doctrine-load-bearing: dull/tarnished, NEVER the sacred
# gold-leaf register (that is reserved for Christ/the LORD's glory alone),
# ported from the short's own bronze-serpent rendering discipline.
# SCALE ADDED 2026-08-01 (user catch): Scripture states no exact size, but
# the metal came from a whole nation's jewelry (Exodus 32:2-3) and the whole
# camp gathered to worship it (Exodus 32:6) -- a substantial public cult
# object, not a hand-sized figurine.
GOLDEN_CALF = (
    "a LARGE cast idol, easily as big as a real young bull calf or bigger, "
    "a substantial public cult statue meant for a whole encampment to "
    "gather around and worship -- NOT a small hand-sized figurine or "
    "trinket -- its metal dull, tarnished, and base, a flat greenish-brown "
    "oxidized patina and dark corroded shadow, catching no bright polished "
    "highlight anywhere on its surface -- explicitly NOT gold leaf, NOT "
    "bright, NOT glowing; gold in this episode is reserved for Christ and "
    "the LORD's glory alone, never for this idol"
)
FULLBLEED = (
    "CRITICAL FRAMING: zoom in close enough that the illustrated subject "
    "and its immediate surroundings occupy the ENTIRE frame, corner to "
    "corner. There must be NO large empty cream-paper or kraft-paper "
    "region anywhere inside the frame, and no blank kraft-paper rectangle "
    "or sticky-note patch used as filler -- the torn-edge collage texture "
    "is only a narrow border treatment along the outermost margin, never a "
    "wide blank zone."
)

STYLE = (
    "Editorial documentary sketch illustration: loose confident graphite-and-ink "
    "linework with muted watercolor wash, drawn on aged warm cream paper. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured stock, "
    "torn and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile hand-made "
    "feel, muted ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge. CRITICAL: absolutely NO lettering, numerals, words, newsprint, "
    "printed book-page text, handwriting, ruler markings, dates, or captions "
    "ANYWHERE on ANY layer -- every paper surface is BLANK textured stock."
)

# (name, refs-tag, scene) -- all 68 spreads from _PLAN.md's table, in spread-
# number order. tag: "moses" chains MOSES_REF+MOSES_REF2, "jesus" chains
# JESUS_REF+JESUS_REF2, "moses,jesus" chains all four, "" chains nothing.
SHOTS_ALL = [
    # spread 1 | Beat 1 | 0.40-7.50s | Wide establishing: aged Moses, camp behind
    ("s01_wide", "moses",
     f"Wide establishing shot at the edge of a vast wilderness encampment "
     f"at the end of forty years' wandering: rows of weathered goat-hair "
     f"tents recede into the distance beneath a pale desert sky, {MOSES} "
     f"stands alone in the foreground, staff in hand, surveying the camp "
     f"-- no other person nearby, the scale of the wilderness dwarfing "
     f"the tents behind him. {FULLBLEED}"),

    # spread 2 | Beat 1 | 7.50-17.00s | Triptych memory-vignette: rod-to-
    # serpent / Red Sea split / water from the rock
    ("s02_triptych", "moses",
     f"A multi-vignette memory composition: {MOSES} stands centered in "
     f"the foreground, staff in hand, eyes distant -- around him, three "
     f"soft-edged memory-vignettes drift like faded watercolor "
     f"recollections woven into the paper's own texture (never in "
     f"panels, frames, arches, or windows): to one side, his rod "
     f"transforming into a serpent before Pharaoh; above, the Red Sea "
     f"walled up and parting; to the other side, water bursting from a "
     f"struck desert rock -- each vignette hazy, translucent, and "
     f"desaturated compared to Moses's own sharp present-tense "
     f"rendering, clearly memory rather than present action. {FULLBLEED}"),

    # spread 3 | Beat 1 | 17.00-21.50s | Close on Moses's eyes, haunted
    ("s03_eyes_haunted", "moses",
     f"Extreme close-up on {MOSES}'s face and eyes only, cropped tight "
     f"from brow to upper beard filling the frame corner to corner -- "
     f"his eyes haunted, distant, weighted with a memory that will not "
     f"leave him, deep creases at their corners, staff/hands/shoulders "
     f"not visible in this crop. {FULLBLEED}"),

    # spread 4 | Beat 1 | 21.50-27.50s | THE ICON: pole in sand, bronze
    # serpent revealed. Device: blue-line (assembly-stage reveal, not
    # requested here).
    ("s04_icon_pole", "moses",
     f"THE ICON, a hero composition: the {BRONZE_SERPENT} stands upright "
     f"on its pole, driven into the sand in the immediate foreground, "
     f"filling much of the frame, {MOSES} beside it with one hand "
     f"resting near its base, wilderness camp faint in the far "
     f"background -- the serpent on its pole is the clear visual center "
     f"of the composition. {FULLBLEED}"),

    # spread 5 | Beat 1 | 27.50-32.50s | Graves being dug, the dying, grief
    ("s05_graves", "",
     f"A wide, grief-heavy composition: {PEOPLE}, some digging graves in "
     f"the sunbaked earth with crude tools, others kneeling beside the "
     f"dying, the wide desert stretching behind them under a heavy sky "
     f"-- sorrow and mourning shown through posture and distance, never "
     f"a visible wound or blood. {FULLBLEED}"),

    # spread 6 | Beat 1 | 32.50-37.10s | Close: dying man's reaching hand,
    # then an eye -- "look not climb"
    ("s06_dying_hand_eye", "",
     f"Extreme close-up, a single ordinary wilderness-worn Hebrew man's "
     f"open, empty, reaching hand in the foreground, and beyond it, his "
     f"own eye -- weary, searching, lifted upward and outward rather "
     f"than reaching or grasping -- no other body part, no wound, no "
     f"blood, no second person anywhere in the frame, the composition "
     f"built entirely around the theme of a look rather than a climb or "
     f"a grasp. {FULLBLEED}"),

    # spread 7 | Beat 2 | 37.10-43.00s | Wide: the freed-but-ungrateful camp
    ("s07_ungrateful_camp", "",
     f"A wide shot of the wilderness encampment, ordinary tents and "
     f"cookfires, {PEOPLE} scattered in small ungrateful, restless "
     f"clusters -- turned from each other, arguing gestures, no one "
     f"looking toward the sky or toward Moses, an atmosphere of drift "
     f"and discontent. {FULLBLEED}"),

    # spread 8 | Beat 2 | 43.00-53.00s | Wide: wandering column round Edom
    ("s08_wandering_column", "",
     f"A vast wide shot: a long column of {PEOPLE} trudging along a "
     f"barren rocky road that curves away around a distant range of "
     f"reddish hills, no end to the road visible, the column small "
     f"against the huge empty landscape, dust rising faintly under their "
     f"feet. {FULLBLEED}"),

    # spread 9 | Beat 2 | 53.00-61.52s | Manna falling, being scorned
    ("s09_manna_scorned", "",
     f"Fine white manna flakes drifting down at dawn over the camp like "
     f"frost, settling on the ground -- in the foreground, {PEOPLE}, "
     f"some gathering it with cupped hands, others turned away in "
     f"visible scorn, arms crossed or backs turned to the falling manna, "
     f"contrast between quiet provision and open contempt. {FULLBLEED}"),

    # spread 10 | Beat 2 | 62.22-67.50s | VC: "the soul of the people was
    # much discouraged" -- background art hosts a Scribed Ink overlay at
    # assembly, no text baked into the render (STYLE already forbids it)
    ("s10_vc_discouraged", "",
     f"A quiet wide composition: {PEOPLE}, slumped and discouraged, "
     f"sitting and lying in exhausted heaps along a barren stretch of "
     f"road at dusk, heads down, postures utterly weary and "
     f"discouraged. {FULLBLEED}"),

    # spread 11 | Beat 2 | 68.20-76.04s | Crowd turns angry, toward Moses
    # and toward heaven
    ("s11_crowd_angry", "moses",
     f"{PEOPLE}, several with raised fists and open hands thrust upward "
     f"toward the sky, faces turned in anger toward both heaven and "
     f"{MOSES}, who stands at the frame's edge, staff in hand, absorbing "
     f"their fury with a heavy, sorrowful expression. {FULLBLEED}"),

    # spread 12 | Beat 2 | 76.74-87.62s | VC: "Wherefore have ye brought us
    # up..." -- background art only
    ("s12_vc_wherefore", "",
     f"A wide composition of angry accusation: {PEOPLE}, several with "
     f"arms flung outward accusingly, mouths open mid-complaint, faces "
     f"twisted in bitter reproach, the barren wilderness road stretching "
     f"behind them. {FULLBLEED}"),

    # spread 13 | Beat 2 | 88.32-98.00s | Memory-vignette: sea / rock /
    # golden calf under the cloud at Sinai
    ("s13_vignette_calf", "moses",
     f"A multi-vignette memory composition, matching spread 2's device: "
     f"{MOSES} stands in the foreground, troubled, staff in hand -- "
     f"around him, soft-edged desaturated memory-vignettes woven into "
     f"the paper's own texture (never panels, frames, arches, or "
     f"windows): the Red Sea parted and walled, water gushing from the "
     f"struck rock, and -- rendered smaller and set apart, its metal "
     f"dull and unlit, never sacred-gold -- {GOLDEN_CALF} standing "
     f"beneath a dark cloud-wrapped mountain, each vignette clearly "
     f"memory, not present action. {FULLBLEED}"),

    # spread 14 | Beat 2 | 98.00-104.16s | Something slides in the dust --
    # first hint of the serpents
    ("s14_serpent_hint", "",
     f"A quiet, tense atmosphere shot at dusk: the narrow gap between two "
     f"weathered goat-hair tents, a single dim serpent-shape just "
     f"visible sliding low through the dust and shadow at the base of "
     f"the frame, no person present, the empty tent-lines heightening "
     f"the sense of an unseen threat entering the camp. {FULLBLEED}"),

    # spread 15 | Beat 2 | 104.86-112.06s | VC: "the LORD sent fiery
    # serpents among the people..." + serpents among the camp
    ("s15_vc_fiery_serpents", "",
     f"Small venomous desert serpents darting among the rocks and "
     f"tent-stakes of the camp at dusk, {PEOPLE} recoiling and "
     f"scattering in alarm, arms raised protectively, bodies twisted "
     f"away -- tension shown through composition and posture, never a "
     f"visible bite or wound. {FULLBLEED}"),

    # spread 16 | Beat 2 | 112.76-117.00s | Close: the bite, "burned like
    # a coal" -- heat/glow, not a graphic wound
    ("s16_bite_closeup", "",
     f"Extreme close-up on a single ordinary Hebrew figure's forearm and "
     f"hand, gripped tight in visible pain, a faint reddish heat-glow "
     f"suggested at the skin's surface where the venom burns -- no "
     f"visible puncture, no blood, no snake attached to the skin, the "
     f"pain conveyed entirely through gripping tension and a subtle warm "
     f"glow, never graphic. {FULLBLEED}"),

    # spread 17 | Beat 2 | 117.00-125.00s | Vignette: strong man collapsed
    # + mother cradling child -- restrained, 2 figures max
    ("s17_vignette_collapse", "",
     f"{PEOPLE_S17} The desert ground and tent-lines around them are "
     f"empty environment only, restrained and quiet, no gore. {FULLBLEED}"),

    # spread 18 | Beat 2 | 125.00-131.61s | Moses alone, hands empty, no
    # remedy -- atmosphere beat
    ("s18_moses_empty_hands", "moses",
     f"{MOSES} stands alone amid the suffering camp, his hands empty and "
     f"open at his sides, no staff gripped, his weathered face heavy "
     f"with helplessness, no remedy in hand -- an atmosphere beat, the "
     f"empty hands the visual center of the composition. {FULLBLEED}"),

    # spread 19 | Beat 3 | 131.61-137.56s | People kneel before Moses,
    # posture shifts from anger to contrition
    ("s19_people_kneel", "moses",
     f"{PEOPLE}, several kneeling low on the sand before {MOSES}, heads "
     f"bowed, hands open in a posture of contrition rather than the "
     f"earlier anger -- Moses standing before them, staff in hand, "
     f"looking down at them gently. {FULLBLEED}"),

    # spread 20 | Beat 3 | 138.26-147.38s | VC: "We have sinned, for we
    # have spoken against the LORD..."
    ("s20_vc_we_have_sinned", "",
     f"{PEOPLE}, several kneeling with heads bowed and hands clasped or "
     f"pressed to their chests in open confession, faces turned down in "
     f"genuine sorrow rather than anger. {FULLBLEED}"),

    # spread 21 | Beat 3 | 148.08-154.00s | Moses interceding, kneeling,
    # arms raised in prayer
    ("s21_moses_intercede", "moses",
     f"{MOSES} kneels alone on open ground, staff laid beside him, both "
     f"arms raised high overhead in earnest intercession, face lifted "
     f"toward the sky, utterly alone. {FULLBLEED}"),

    # spread 22 | Beat 3 | 154.00-163.84s | Moses's face -- surprise the
    # LORD did not simply remove the serpents; listening
    ("s22_moses_listening", "moses",
     f"A mid close-up on {MOSES}'s face, head tilted slightly as though "
     f"listening intently to an unseen voice, brows drawn in surprise "
     f"and searching thought, staff loosely in one hand at his side. "
     f"{FULLBLEED}"),

    # spread 23 | Beat 3 | 164.54-169.00s | THE LORD's presence appears --
    # ALREADY RENDERED AND APPROVED (test gate). Do NOT re-render.
    ("s23_lord_presence", "moses",
     f"A moment of overwhelming divine encounter: {MOSES} kneels low in "
     f"the foreground, one arm raised to shield his eyes from an "
     f"unbearable brightness, head bowed and turned away from "
     f"{LORD_PRESENCE} -- the light and cloud dominate the composition, "
     f"filling easily two-thirds of the frame, Moses small and dwarfed "
     f"before it, no other person present anywhere. {FULLBLEED}"),

    # spread 24 | Beat 3 | 169.00-177.18s | VC (Illuminated Rubric): [the
    # LORD] "Make thee a fiery serpent, and set it upon a pole..."
    ("s24_vc_make_thee", "",
     f"A quiet composition dominated by soft radiant golden glow filling "
     f"the upper portion of the frame -- {LORD_PRESENCE}, its brightness "
     f"now settled to a steady warm background presence rather than the "
     f"overwhelming burst of the theophany moment, the wilderness ground "
     f"and a suggestion of tents faint and small below it, no figure "
     f"present in the frame. {FULLBLEED}"),

    # spread 25 | Beat 3 | 177.88-184.00s | Moses processing -- no
    # medicine offered, negation imagery (empty hands, no jar)
    ("s25_moses_empty_negation", "moses",
     f"{MOSES} stands with both hands turned palm-up and empty before "
     f"him, studying them, no jar, no herb, no medicine of any kind in "
     f"his hands or nearby -- his face processing, working through the "
     f"strangeness of the command he has just received. {FULLBLEED}"),

    # spread 26 | Beat 3 | 184.00-192.00s | Moses looking at a live
    # serpent on the ground -- resolve forming
    ("s26_moses_resolve_serpent", "moses",
     f"{MOSES} crouches low, staff set aside, studying a single small "
     f"live desert serpent coiled on a flat stone a short distance in "
     f"front of him, his weathered face hardening into resolve rather "
     f"than fear. {FULLBLEED}"),

    # spread 27 | Beat 3 | 192.00-196.28s | Close-up hands, beginning the
    # forge (shot-variety floor: close hands)
    ("s27_hands_gather_ore", "moses",
     f"Extreme close-up on {MOSES}'s hands alone, gathering rough lumps "
     f"of raw bronze and copper ore into a leather-wrapped hand, "
     f"beginning to lay them by a small unlit forge -- only hands and "
     f"forearms in frame, no face, no shoulders. {FULLBLEED}"),

    # spread 28 | Beat 3 | 196.98-204.00s | ACTING spread: Moses hammering
    # the bronze serpent into shape, extreme close, motion completes then
    # holds. Device: optional raking-light (assembly-stage).
    ("s28_forge_acting", "moses",
     f"An acting spread, extreme close on {MOSES}'s hands and forearms "
     f"at a small desert forge, hammer raised then striking down onto a "
     f"glowing half-formed bronze serpent shape on an anvil stone, "
     f"sparks scattering, an ochre firelight glow catching his knuckles "
     f"-- the completed motion of a single hammer-strike, no other "
     f"person present. {FULLBLEED}"),

    # spread 29 | Beat 3 | 204.00-208.98s | The pole now stands; first
    # bitten look up, first healing
    ("s29_pole_first_healing", "",
     f"The {BRONZE_SERPENT} stands newly raised on its pole in the camp, "
     f"and in the foreground a single stricken Hebrew figure lifts his "
     f"face up toward it, one hand still pressed to his own arm, an "
     f"expression shifting from pain toward relief -- no other person "
     f"present, no visible wound or blood. {FULLBLEED}"),

    # spread 30 | Beat 3 | 209.68-228.25s | Payoff: a man's fever breaks
    # as he looks up -- "no payment, no climbing"
    ("s30_payoff_fever_breaks", "",
     f"A single ordinary Hebrew man kneels in the foreground before the "
     f"{BRONZE_SERPENT} raised on its pole nearby, his face tilted "
     f"straight up toward it, eyes open, a visible easing in his posture "
     f"-- shoulders relaxing, a hand that was clutched now open and "
     f"loose -- no climbing, no reaching toward the pole, no offering "
     f"laid before it, only the act of looking. {FULLBLEED}"),

    # spread 31 | Beat 4 | 228.25-233.41s | Close on Moses's face turning
    # the question over: "Why a serpent?"
    ("s31_moses_why_serpent", "moses",
     f"A close-up on {MOSES} in three-quarter profile, NOT facing the "
     f"viewer -- his gaze lowered and inward, brow furrowed in genuine "
     f"puzzlement, staff held loosely, the faint wilderness road visible "
     f"behind him, turning an unspoken question over in his mind alone. "
     f"{FULLBLEED}"),

    # spread 32 | Beat 4 | 233.41-259.03s | Wide/mid: the serpent on its
    # pole, silhouetted against the camp at dusk. Device: slow drift/push
    # camera (assembly-stage).
    ("s32_pole_silhouette_dusk", "",
     f"A wide dusk composition: the {BRONZE_SERPENT} on its pole stands "
     f"in silhouette in the foreground against a darkening sky, the "
     f"camp's tents small and distant behind it, its coiled shape stark "
     f"and deliberate against the fading light -- no person present, the "
     f"serpent's own form the entire visual point. {FULLBLEED}"),

    # spread 33 | Beat 4 | 259.03-272.61s | Vignette: strong man / child /
    # dying elder, all lifting their eyes the same way -- universality
    ("s33_vignette_universal", "",
     f"{PEOPLE_S33} The composition emphasizes that all three, despite "
     f"their differences, share the exact same upward gaze. {FULLBLEED}"),

    # spread 34 | Beat 4 | 272.61-284.83s | Moses walking alone at dusk,
    # the riddle "walking home with him every evening"
    ("s34_moses_walking_dusk", "moses",
     f"A wide, quiet composition: {MOSES} walks alone along a bare "
     f"wilderness path at dusk, staff in hand, small against the vast "
     f"fading landscape, no tent or person nearby, an unhurried solitary "
     f"figure heading home. {FULLBLEED}"),

    # spread 35 | Beat 5 | 284.83-293.25s | Close on elderly Moses's face,
    # direct-address register begins: "I will be honest with you"
    ("s35_moses_honest_close", "moses",
     f"A close, intimate mid-shot: {MOSES}'s face turned directly toward "
     f"the viewer, his expression open and searching, about to speak "
     f"plainly, staff loosely at his side. {FULLBLEED}"),

    # spread 36 | Beat 5 | 293.25-314.62s | Mid: a proud man turning away
    # from the pole while others look -- "a cure so simple is its own
    # stumbling-block"
    ("s36_proud_man_turns_away", "",
     f"A mid-distance composition: in the foreground, one proud-postured "
     f"Hebrew man turns his back deliberately on the {BRONZE_SERPENT} "
     f"visible on its pole in the middle distance, arms crossed, chin "
     f"lifted in refusal; behind him, {PEOPLE} looking toward the pole "
     f"in contrast -- the refusal in the foreground against the looking "
     f"behind him is the composition's whole point. {FULLBLEED}"),

    # spread 37 | Beat 5 | 314.62-325.48s | FLASHBACK: Moses grinding the
    # golden calf -- ALREADY RENDERED AND APPROVED (test gate). Do NOT
    # re-render.
    ("s37_calf_flashback", "moses",
     f"A MEMORY, not a present-moment scene -- render this drastically "
     f"differently from every other spread in the episode: a hazy, "
     f"desaturated, soft-focus recollection, rendered in loose, "
     f"unfinished, sketchy pencil linework with the ink and watercolor "
     f"almost entirely withheld (barely a wash of muted grey-brown, no "
     f"crisp linework anywhere), heavy soft-edged vignetting swallowing "
     f"the entire outer two-thirds of the frame into indistinct fog and "
     f"blank paper, as though the memory itself is fading at the edges: "
     f"within that hazy vignette, {MOSES}, seen only in silhouette or "
     f"deep half-shadow (no clear facial detail, deliberately obscured, "
     f"unlike his sharp/lit appearance everywhere else in the episode), "
     f"a dim indistinct shape kneeling and grinding {GOLDEN_CALF} to "
     f"powder between two stones on the desert floor, one single weak "
     f"shaft of light the only illumination, no other person present "
     f"anywhere. {FULLBLEED}"),

    # spread 38 | Beat 5 | 325.48-344.31s | THE DREAD IMAGE: Moses holding
    # the bronze serpent, staring at it -- the tablets of the law
    # referenced small in-frame
    ("s38_dread_image", "moses",
     f"{MOSES} sits alone, holding the {BRONZE_SERPENT} up before his "
     f"own face at arm's length, staring at it with dread and searching "
     f"intensity -- small and distant in the background, barely "
     f"legible, two stone tablets rest against a rock, a quiet visual "
     f"echo of the second commandment, no other person present. "
     f"{FULLBLEED}"),

    # spread 39 | Beat 5 | 344.31-350.29s | Close, night: Moses sleepless.
    # Device: candle-only (single lamp, dread register).
    ("s39_moses_sleepless_candle", "moses",
     f"A close night composition: {MOSES} sits sleepless beside a single "
     f"small oil lamp, its flame the only light source in the frame, his "
     f"weathered face drawn with dread and turmoil in the lamp's warm "
     f"glow, deep shadow pressing in around him. {FULLBLEED}"),

    # spread 40 | Beat 5 | 350.29-364.51s | Moses's resolve returning,
    # hand on the bronze but eyes lifted
    ("s40_moses_resolve_returning", "moses",
     f"{MOSES}, one hand resting on the {BRONZE_SERPENT} beside him, but "
     f"his eyes lifted up and away from it toward the open sky, his "
     f"expression shifting from dread to settled resolve and trust. "
     f"{FULLBLEED}"),

    # spread 41 | Beat 5 | 364.51-382.80s | Wide: Moses at the camp's
    # edge, looking down a long empty road into darkness. Device: slow
    # push-out (assembly-stage).
    ("s41_moses_long_road", "moses",
     f"A wide composition: {MOSES} stands small at the very edge of the "
     f"camp, staff in hand, looking down a long empty road that "
     f"stretches away into gathering darkness, the vast landscape "
     f"dwarfing him, a sense of a path leading somewhere beyond what is "
     f"visible. {FULLBLEED}"),

    # spread 42 | Beat 5 | 382.80-387.84s | Close on hands finishing the
    # forge, quiet -- bookends spread 28
    ("s42_hands_finish_forge", "moses",
     f"Extreme close-up on {MOSES}'s hands alone, setting down the "
     f"hammer beside the now-finished {BRONZE_SERPENT}, the motion "
     f"complete and quiet, no sparks now, only stillness -- only hands "
     f"and forearms in frame, no face. {FULLBLEED}"),

    # spread 43 | Beat 6 | 388.54-402.14s | INSERT PAGE 1: Scholar's-Margin
    # two-panel typology diagram (Numbers 21 / John 3), red-letter John
    # 3:14-15 lettered whole at ASSEMBLY (not baked in -- STYLE forbids
    # lettering). Right panel = teaching-by-night register (Jesus +
    # Nicodemus), NOT a repeat of the crucifixion (spreads 45-51 already
    # carry that content) -- matches the SHORT's s08 device/register, new
    # content per the batch instructions.
    ("s43_insert_scholars_margin2", "moses,jesus",
     f"A Scholar's-Margin insert page, a formal two-panel typology "
     f"diagram laid out on a single aged parchment sheet (same device "
     f"and register as the episode's other insert page): on the left "
     f"panel, {MOSES} stands beside the {BRONZE_SERPENT} raised on its "
     f"pole, a wilderness camp of tents faint behind him; on the right "
     f"panel, {JESUS}, seated with a single small oil lamp for its only "
     f"light, teaching an anonymous seeker Nicodemus by night -- an "
     f"ordinary older Judean man in a plain robe, seated attentively -- "
     f"both panels in fine sepia pen-and-ink diagram linework, a thin "
     f"hairline rule dividing the panels, a small hand-drawn directional "
     f"arrow pointing from the left panel to the right, open cream "
     f"parchment margin below each panel. CRITICAL: absolutely NO "
     f"printed words, numerals, or labels anywhere on the page. "
     f"{FULLBLEED}"),

    # spread 44 | Beat 6 | 402.84-410.00s | Moses's realization: the
    # bronze serpent's shadow, symbolically cross-shaped on the ground
    ("s44_shadow_cross", "moses",
     f"{MOSES} stands beside the {BRONZE_SERPENT} on its pole at a low "
     f"sun angle, his gaze fixed downward on the ground where the pole "
     f"and its crossbar of shadow fall in a shape that faintly, "
     f"unmistakably suggests a cross -- restrained and natural, not "
     f"garish or glowing, an ordinary long shadow that happens to fall "
     f"this way. {FULLBLEED}"),

    # spread 45 | Beat 6 | 410.00-420.00s | Golgotha: Christ lifted, wide,
    # reverent, restrained, no gore -- echoes the short's s10
    ("s45_golgotha_wide", "jesus",
     f"A reverent Golgotha spread, respectful mid-distance wide framing: "
     f"{JESUS} lifted up on a plain wooden cross atop a bare hill, arms "
     f"stretched along the crossbeam, head bowed low in stillness and "
     f"peace, a plain white loincloth His only garment, no visible "
     f"wound, no blood, no nail shown in close-up -- sacred and "
     f"restrained, never graphic. A darkened sky presses low over the "
     f"hill -- supernatural darkness, NOT a storm, no lightning, no "
     f"rain, no wind-blown debris -- no crowd, no soldiers, no other "
     f"figure anywhere in the frame. {FULLBLEED}"),

    # spread 46 | Beat 6 | 420.00-425.00s | Paired composition: bronze
    # serpent + the cross together -- the film's thesis image
    ("s46_thesis_pair", "jesus",
     f"A symbolic paired composition, the film's thesis image: the "
     f"{BRONZE_SERPENT} stands upright on its pole in the near "
     f"foreground, and beyond it, smaller in the distance yet clearly "
     f"visible, {JESUS} lifted up on a plain wooden cross against an "
     f"open sky -- both hang in plain sight within the same single "
     f"unbroken view, nothing hidden, no gore, no wound, no blood "
     f"visible on either. {FULLBLEED}"),

    # spread 47 | Beat 6 | 425.00-433.48s | Christ on the cross, reverent,
    # leading into the Gal 3:13 quote
    ("s47_golgotha_midshot", "jesus",
     f"A reverent mid-shot of {JESUS} lifted up on the plain wooden "
     f"cross, head bowed, stillness and quiet dignity, no visible wound, "
     f"no blood, the darkened sky pressing low behind Him -- restrained, "
     f"sacred, leading toward the quote about bearing a curse. "
     f"{FULLBLEED}"),

    # spread 48 | Beat 6 | 434.18-441.54s | VC: "being made a curse for
    # us: for it is written, Cursed is every one that hangeth on a tree"
    ("s48_vc_curse_for_us", "jesus",
     f"{JESUS} lifted on the plain wooden cross, distant and slightly "
     f"softened in the background of the frame, head bowed, the "
     f"darkened sky filling most of the composition around Him, "
     f"restrained and reverent, no visible wound or blood. {FULLBLEED}"),

    # spread 49 | Beat 6 | 442.24-451.00s | Christ lifted, radiant
    # register beginning -- "bore the judgment... taken in our place"
    ("s49_christ_radiant_begin", "jesus",
     f"{JESUS} lifted up on the plain wooden cross, a soft warm glow "
     f"beginning to gather around His form -- the register shifting from "
     f"the darkened-sky suffering of the earlier spreads toward glory -- "
     f"head still bowed but the light growing, gold reserved only for "
     f"this glow, never elsewhere in the frame. {FULLBLEED}"),

    # spread 50 | Beat 6 | 451.00-456.48s | Close, leading into Jesus's
    # own words
    ("s50_christ_close_words", "jesus",
     f"A close reverent shot on {JESUS}'s face and upper form, lifted on "
     f"the cross, the gathering warm glow now clearly visible around His "
     f"head and shoulders, His expression calm and resolved, about to "
     f"speak. {FULLBLEED}"),

    # spread 51 | Beat 6 | 457.18-464.06s | Red-letter, arrives whole:
    # "And I, if I be lifted up from the earth, will draw all men unto
    # me" -- Christ radiant, light drawing figures toward Him
    ("s51_christ_draw_all_men", "jesus",
     f"{JESUS} lifted up on the plain wooden cross, now fully radiant, "
     f"warm gold light streaming outward from Him in wide symbolic rays "
     f"-- in the far distance below, small and drawn toward the light, "
     f"{PEOPLE}, tiny silhouetted figures walking toward the glow, no "
     f"individual detail needed at that distance, restrained and "
     f"symbolic rather than literal. {FULLBLEED}"),

    # spread 52 | Beat 6 | 464.76-475.54s | Moses reflecting, resolved:
    # "it was never the bronze; it was the looking that God honoured"
    ("s52_moses_reflecting", "moses",
     f"{MOSES}, seated, staff across his knees, face settled and "
     f"reflective rather than troubled, a quiet resolved expression, no "
     f"bronze serpent in frame at all -- the moment is about his "
     f"understanding, not the object. {FULLBLEED}"),

    # spread 53 | Beat 6 | 475.54-478.92s | Brief, close on Moses: "I
    # know that now better than I once wished to"
    ("s53_moses_know_that_now", "moses",
     f"A brief close-up on {MOSES}, three-quarter angle with his gaze "
     f"lowered inward rather than toward the viewer, one weathered hand "
     f"raised to rest against his own chest, a small rueful, honest "
     f"half-smile of hard-won understanding, eyes steady. {FULLBLEED}"),

    # spread 54 | Beat 6 | 478.92-486.11s | TIME SHIFT (generations
    # later): people burning incense before the enshrined serpent --
    # idolatry creeping in. Device: soft dissolve transition IN
    # (assembly-stage).
    ("s54_timeshift_enshrined", "",
     f"TIME SHIFT, generations later: the {BRONZE_SERPENT}, now set "
     f"within a small shrine-like niche of piled stones with a woven "
     f"canopy overhead -- a visibly different, more elaborate staging "
     f"than its plain forge/pole appearance earlier in the episode -- "
     f"{PEOPLE}, kneeling before it, some with small trails of incense "
     f"smoke rising from clay dishes at its base, an atmosphere of "
     f"misplaced reverence and creeping idolatry. {FULLBLEED}"),

    # spread 55 | Beat 6 | 486.11-493.51s | Hezekiah, a YOUNG king (2
    # Kings 18:2), breaks the bronze serpent to pieces -- decisive,
    # corrective, NOT shameful. Device: impact-burst (assembly-stage).
    ("s55_hezekiah_breaks", "",
     f"{HEZEKIAH}, mid-motion, one arm swinging a stone hammer down "
     f"decisively onto the {BRONZE_SERPENT} where it stands in its "
     f"shrine niche, the serpent's form just beginning to crack and "
     f"fracture under the blow -- his expression resolute and "
     f"corrective, not cruel or triumphant, a righteous king's decisive "
     f"act, no crowd present, no shame in the framing. {FULLBLEED}"),

    # spread 56 | Beat 6 | 493.51-498.18s | Moses's voice affirms: "he
    # was right to break it. The power was never in my handiwork"
    ("s56_moses_affirms", "moses",
     f"{MOSES} stands, not seated, looking off toward the shattered "
     f"fragments of the {BRONZE_SERPENT} faintly visible in the middle "
     f"distance where Hezekiah broke it, nodding slightly with quiet "
     f"approval, an expression of settled affirmation rather than any "
     f"grief over the loss of the object he once forged. {FULLBLEED}"),

    # spread 57 | Beat 6 | 498.18-507.64s | Transition back to
    # Christ/gold register: "the power was in the God who said look and
    # live"
    ("s57_bridge_moses_christ", "moses,jesus",
     f"A composition bridging both figures: {MOSES}, small and in the "
     f"near foreground, and beyond him, larger and radiant with a warm "
     f"gold glow, {JESUS} standing in light -- the visual weight "
     f"shifting from Moses toward the glowing figure of Christ, gold "
     f"reserved only for that glow. {FULLBLEED}"),

    # spread 58 | Beat 6 | 508.34-517.38s | VC (Illuminated Rubric, most
    # famous verse -- full ceremony): John 3:16
    ("s58_vc_john316", "jesus",
     f"{JESUS} standing fully radiant, warm gold light streaming outward "
     f"and filling most of the frame around Him, arms open, an "
     f"atmosphere of pure gift and grace, the composition's most "
     f"luminous and glorious moment in the film so far. {FULLBLEED}"),

    # spread 59 | Beat 7 | 518.08-524.00s | Moses direct-address: "So
    # hear me -- be still. Do not rush past this as my people rushed
    # past the manna"
    ("s59_moses_be_still", "moses",
     f"{MOSES}, facing the viewer directly, one open hand raised gently "
     f"as though asking for stillness and attention, his expression "
     f"earnest and urgent but gentle. {FULLBLEED}"),

    # spread 60 | Beat 7 | 524.00-532.00s | Vignette: strong men trying to
    # walk the fire off, each failing in his own way
    ("s60_vignette_selfeffort", "",
     f"{PEOPLE_S60} The composition emphasizes each man's isolated, "
     f"futile self-effort. {FULLBLEED}"),

    # spread 61 | Beat 7 | 532.00-539.00s | Intimate close on Moses:
    # "That is you. That is me"
    ("s61_moses_thatisyou", "moses",
     f"An intimate close-up on {MOSES}'s face, direct and searching, "
     f"addressing the viewer as though speaking to them personally, a "
     f"shared vulnerability in his expression. {FULLBLEED}"),

    # spread 62 | Beat 7 | 539.00-544.50s | Close, resolute: "you were
    # never asked to"
    ("s62_moses_neverasked", "moses",
     f"A mid-close shot pulled back enough to show {MOSES}'s shoulders "
     f"and one open hand held out, palm up, in a simple releasing "
     f"gesture, a settled certainty replacing the searching look of the "
     f"prior spread, steady eyes, a small reassuring nod-like tilt of "
     f"the head. {FULLBLEED}"),

    # spread 63 | Beat 7 | 544.50-553.00s | Christ radiant lifted; three
    # small figures below -- the least, the last, a child turning his
    # head -- looking up
    ("s63_vignette_least_last_child", "jesus",
     f"{JESUS}, lifted up and fully radiant, warm gold light streaming "
     f"from Him and filling the upper two-thirds of the frame -- below, "
     f"small in the distance, {PEOPLE_S63} A composition distinct in "
     f"staging from any earlier vignette of this episode -- Christ "
     f"towering in glory above, the three small figures below Him. "
     f"{FULLBLEED}"),

    # spread 64 | Beat 7 | 553.00-559.00s | Pause beat, near-silence:
    # "Sit with that". Optional held-breath energy-envelope pass
    # (assembly-stage only, no change to the still).
    ("s64_moses_sit_with_that", "moses",
     f"A quiet held pause: {MOSES}, seated on a low rock with the "
     f"wilderness stretching empty behind him, his staff planted "
     f"upright in the sand beside him with both hands resting atop it, "
     f"eyes lowered in contemplation, no motion, no gesture, a spread "
     f"built entirely for stillness. {FULLBLEED}"),

    # spread 65 | Beat 7 | 559.00-565.00s | Christ, plain and open:
    # "costs you nothing but a look"
    ("s65_christ_open_invite", "jesus",
     f"{JESUS} standing plainly, arms open in a simple, unadorned "
     f"gesture of invitation, a gentle warm glow but not overwhelming, "
     f"an approachable and open composition rather than a distant "
     f"glorified one. {FULLBLEED}"),

    # spread 66 | Beat 7 | 565.00-576.00s | Moses turning the question
    # directly to the viewer -- most intimate direct-address of the film
    ("s66_moses_direct_question", "moses",
     f"The most intimate direct-address spread of the film: an extreme "
     f"close-up on {MOSES}'s face alone, filling the frame corner to "
     f"corner, his eyes locked directly on the viewer, a final "
     f"searching, personal question in his expression. {FULLBLEED}"),

    # spread 67 | Beat 7 | 576.00-585.00s | INSERT PAGE 2 (Gilded
    # Proclamation echo, reuses the short's s12 device): "Not to the
    # bronze, nor to me -- but to Jesus" -- ONE unified gold-ground
    # composition, no labels
    ("s67_insert_gilded_proclamation2", "jesus",
     f"A Gilded Proclamation insert page, the same device and register "
     f"as the episode's other insert page: ONE unified gold-leaf-ground "
     f"composition, no panels, no dividing line -- the {BRONZE_SERPENT} "
     f"stands low and small in the earthbound foreground, plain dull "
     f"bronze catching no gold shine, while {JESUS} rises radiant above "
     f"and behind it against a burnished gold-leaf ground, arms "
     f"outstretched, filling the upper two-thirds of the frame in full "
     f"glory -- gold touches only Christ and the ground behind Him, the "
     f"serpent stays plain and dull throughout, no visible wound or "
     f"blood on either figure. CRITICAL: absolutely NO printed words, "
     f"numerals, or labels anywhere on the page. {FULLBLEED}"),

    # spread 68 | Beat 7 | 585.00-590.08s (+ >=3.0s hold) | THE LANDING:
    # "Look to Him, and live." Torn-page device (mandatory), gold light
    # from beneath the tear, Christ's silhouette distant
    ("s68_landing", "jesus",
     f"THE LANDING spread: the page itself is torn open in a ragged hole "
     f"near center, radiant warm gold light streaming up from beneath "
     f"the torn page, a small still silhouette of {JESUS} standing "
     f"within the golden light beyond the tear, arms open, sacred "
     f"stillness -- nothing else in frame, no serpent, no Moses, no "
     f"camp, only the torn page and the light. {FULLBLEED}"),
]


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "16:9", "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def resolve_refs(tag):
    refs = []
    if not tag:
        return refs
    if "moses" in tag:
        refs.append(MOSES_REF)
        if MOSES_REF2.exists():
            refs.append(MOSES_REF2)
    if "jesus" in tag:
        refs.append(JESUS_REF)
        if JESUS_REF2.exists():
            refs.append(JESUS_REF2)
    return refs


def main(only=None):
    shots = SHOTS_ALL if only is None else [s for s in SHOTS_ALL if s[0] in only]
    for name, tag, scene in shots:
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        refs = resolve_refs(tag)
        for r in refs:
            if not r.exists():
                print(f"   FAILED -- missing ref {r}, run its anchor script first")
                scene = None
                break
        if scene is None:
            continue
        prompt = STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(refs)}) ...", flush=True)
        ok = run(prompt, out, refs)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, refs)
        if ok:
            try:
                cost.record_hf(EPISODE, "long", "stills", MODEL, note=f"[bronzeserpentlong] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    only = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    main(only)
