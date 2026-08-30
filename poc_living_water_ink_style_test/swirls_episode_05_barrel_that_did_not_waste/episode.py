"""Episode spec for "The Barrel That Did Not Waste" (1 Kings 17:8-16 + Luke
4:25-26) -- episode 5 in the locked series slate. Fray motif (fear/doubt --
1 Kings 17:13 has the verbatim "Fear not") only, no Stain; swirl capped
Stage 1-2 throughout per the OT-episode rule, held at Stage 2 (not 3) on the
Jesus page, matching Naaman's own precedent and the series-plan row.

Design authored by Fable (full brief: `_DESIGN_BRIEF.md` in this folder),
implemented by Sonnet per the "Fable designs, Sonnet executes" rule. Three
open questions Fable deliberately left unresolved were put to the user and
answered (all recommended options taken): (1) F05 crops a cross-episode
`synagogue_ref.png` from episode 4's own approved F06 still -- the series'
first cross-episode location ref, since Luke 4:25-26 (this episode) and
4:27 (Naaman) are two verses of the SAME sermon; (2) F05's third panel is a
deliberate Naaman-in-the-Jordan cameo, not a plain Nazareth-rooftops panel;
(3) the swirl on F05 holds at Stage 2 (the episode cap), not Stage 3.

Shape: the narration opens on the widow (not on Jesus, the opposite of
Naaman), so the covers belong to HER world -- front = the widow gathering
sticks in the famine (the hook's own image), back = the open meal barrel in
dawn light (the landing's own image, "He needs it open"). The Nazareth/
Jesus beat goes to an INTERIOR page (F05) instead of a cover, deliberately
NOT repeating Naaman's own Nazareth-cliff front cover one episode later --
see _DESIGN_BRIEF.md section 4 for the full reasoning. F05 is designed as
the sibling of Naaman's own F06: the SAME synagogue room, one minute
EARLIER in the sermon (the crowd still seated and hardening, not yet risen
-- that belongs to Naaman's page, verse 4:27-28).

Fray arc (the widow's fear, descending): F01 FR1 (subtle -- her ref crops
from this page, so a heavy fray here would bake tremor into the reference
itself, the same trap Naaman's own leprosy patches taught) -> F02 FR3 PEAK
(her death-sentence line, "we may eat it, and die") -> HARD CUT clear to F03
FR1 (lands exactly on "Fear not") -> HARD CUT to F04-F06 FR0 (she obeys;
every steady page carries an explicit steady-line override, since her
full-figure ref itself was cropped mid-fray at F01). The clearing is always
the cut between pages, never a within-clip dissolve -- same law as Naaman's
Stain and the Hem's own Fray precedent.

Swirl arc (living ink, rising against the falling Fray): 0 (front/F01) -> 0
(F02, her lowest page stays stark) -> 1 (F03, first trace rises from the two
dry sticks lying between her and Elijah -- the funeral wood becomes the
first thing the life touches, arriving exactly WITH "Fear not") -> 2 (F04,
the meal jar's own mouth) -> 2 held (F05, the reading-desk-and-scroll
anchor, Naaman F06's own anchor reused as a deliberate series constant) ->
2 held (F06) -> a small closed curl on the back cover (the barrel's own
open mouth, echoing the front cover's curl-in-air language family).

The "barrel" literalism trap: KJV "barrel" is a storage JAR (earthenware),
not a wooden stave-and-hoop cask -- every prompt showing it says
"earthenware storage jar" first and carries an explicit never-wooden/
never-hoops pair; captions still say "barrel" (the KJV's own word), only
the drawing is corrected.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "test_the_cross"))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from swirls_page import PageSpec, Panel, Ref  # noqa: E402
from swirls_cover import CoverSpec  # noqa: E402
from swirls_assemble import DuckProfile, EpisodeManifest, ScoreVariant, Unit  # noqa: E402

REFS_DIR = HERE / "refs"

# ---- character continuity builds -------------------------------------------

# LOCKED series-wide, reused verbatim from episode 4 (itself from ep1/ep8) --
# no amendment, no new approval cycle. jesus_ref.png copied from episode 4's
# own refs/ directory.
JESUS_BUILD = (
    "Jesus, a Judean man in his early thirties, medium height and ordinary build, sun-browned "
    "skin, shoulder-length dark brown hair pushed back from his face, a short full dark beard, "
    "wearing a simple ankle-length robe of undyed cream-brown wool with a plain olive-toned "
    "mantle draped over one shoulder, a narrow rope belt, and flat worn leather sandals -- no "
    "halo, no glow, nothing in his dress distinguishing him from the men around him, standing "
    "square, still, and unhurried, his gaze steady and direct"
)

# New to the series. Her FRAY STATE is deliberately NOT in this build -- it changes
# page to page (peaking at F02, clearing F03, gone F04 onward), authored per-page
# in main_scene_still. The clay-red scarf band is her likeness pin (Naaman's bronze
# band pattern); no blue anywhere in her dress -- blue belongs to the motif alone.
WIDOW_BUILD = (
    "the widow of Zarephath, a Phoenician woman in her middle thirties made older by famine, "
    "thin and small-framed with a worn upright dignity, hollowed cheeks and large deep-set dark "
    "eyes, sun-lined olive skin, dark hair bound back under a plain widow's head-scarf of undyed "
    "grey-brown wool with a narrow band of faded clay-red woven at its edge, wearing a patched "
    "ankle-length tunic of faded ochre-brown under a loose olive-grey shawl knotted at one "
    "shoulder, bare dusty feet"
)

# New to the series. Grounded in 2 Kings 1:8 ("an hairy man, girt with a girdle of
# leather") and the mantle of 1 Kings 19:19. Maximally distinct silhouette from
# every existing series man (Jesus, Naaman, Jacob, Nathanael).
ELIJAH_BUILD = (
    "Elijah the Tishbite, a wilderness prophet in his fifties, lean and rawboned, weathered hard "
    "by sun and travel, a deep-lined dark-bronzed face with fierce steady eyes, a great unkempt "
    "mane of thick grey-streaked black hair and a full wild beard, wearing a rough shaggy mantle "
    "of dark camel-hair thrown over a coarse knee-length tunic of undyed wool, a wide plain "
    "leather girdle bound about his loins, worn leather sandals, a tall rough-cut walking staff "
    "in one hand"
)

R_JESUS = Ref("Jesus -- his face, build, and dress", str(REFS_DIR / "jesus_ref.png"))
R_WIDOW = Ref("the widow of Zarephath -- her face, build, and dress", str(REFS_DIR / "widow_ref.png"))
R_WIDOW_FACE = Ref("the widow of Zarephath -- her face and eyes, for close crops", str(REFS_DIR / "widow_face_ref.png"))
R_ELIJAH = Ref("Elijah -- his face, build, and dress", str(REFS_DIR / "elijah_ref.png"))
R_ELIJAH_FACE = Ref("Elijah -- his face and eyes, for close crops", str(REFS_DIR / "elijah_face_ref.png"))
R_GATE = Ref("the gate of Zarephath -- its exact drystone posts and timber lintel", str(REFS_DIR / "gate_ref.png"))
R_BARREL = Ref("the meal barrel and oil cruse -- their exact earthenware form", str(REFS_DIR / "barrel_cruse_ref.png"))
R_SYNAGOGUE = Ref(
    "the Nazareth synagogue interior -- the same room as episode 4's own F06, its exact stone "
    "walls, reading desk, and low benches",
    str(REFS_DIR / "synagogue_ref.png"),
)

# ===========================================================================
# F01 -- "A stranger asks"  (narration: "A stranger passing through, Elijah,
# asked her for water. Then bread. She had nothing to spare -- nothing,
# period:")
# Debut page for the widow, Elijah, AND the gate -- renders unpinned, sources
# five ref crops. Highest approval bar in the episode: FR1 only (see docstring
# -- a heavy fray here would bake tremor into her own reference).
# ===========================================================================
F01 = PageSpec(
    seq_title="AN HANDFUL OF MEAL",
    frame_label="F01",
    panels=(
        Panel("the dry brook",
              "the cracked, stone-littered bed of a dried-up brook, no water anywhere"),
        Panel("two sticks",
              "two dry sticks lying crossed on bare cracked earth"),
        Panel("by the sea",
              "Zarephath's low flat rooftops stepping down to a flat grey sea"),
    ),
    still_shot_type="MEDIUM TWO-SHOT",
    anim_shot_desc="medium two-shot",
    main_scene_still=(
        "the dusty open ground before the gate of Zarephath -- two squared weathered drystone "
        "posts carrying a rough timber lintel in a low sun-dried mud-brick town wall, "
        f"drought-bleached, fully inside the frame. {WIDOW_BUILD}, fully inside the frame, "
        "paused half-bent over the bare ground, a thin bundle of dry sticks gathered in the "
        "crook of one arm, her face lifted toward the stranger, guarded and hollow-eyed; the "
        "hatching of her figure drawn slightly loose and overworked, though her contour stays "
        f"whole and single. {ELIJAH_BUILD}, fully inside the frame, standing travel-worn before "
        "her, his staff in one hand, his other hand half-raised in a quiet ask, his own linework "
        "steady, single-struck, confident; cracked dry earth, wisps of drought-killed grass, no "
        "water drawn anywhere. Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this "
        "page -- no blue ink appears anywhere in the scene, the panels, or the margins."
    ),
    material_closer=(
        "the loosened hatching in the widow's own figure is the only unusual ink at work on this "
        "page, and no blue appears anywhere."
    ),
    panel_motions=(
        "a faint heat-shimmer plays over the dry brook stones",
        "the two sticks sit undisturbed, casting fixed shadows",
        "a thin haze drifts over the far rooftops and sea",
    ),
    main_scene_animation=(
        "the widow's head completes its lift and her eyes settle on Elijah, finishing early and "
        "holding still; Elijah does not move at all for the entire clip -- no breath, no shift of "
        "weight, no change of expression, his whole body and every part of him staying at "
        "exactly its original drawn size and exactly its original drawn position in the frame, "
        "never growing, never shrinking, never shifting up, down, or sideways, his head and face "
        "staying fully visible inside the frame the entire time, never rising toward the top edge "
        "or leaving the frame; the space above and beside him stays completely empty for the "
        "whole clip -- no round, oval, or cloud-shaped white or pale mark of any kind, no "
        "balloon, no bubble, no tail or pointer shape, and no lettering or text of any kind ever "
        "appears anywhere near him or anywhere else on the page, at any point, in any frame; the "
        "dry grass wisps at their feet stir faintly;"
    ),
    fence_kind="fray",
    fence_callout="the loosened, overworked hatching of the widow's figure",
    caption_lines=("nothing to spare",),
    corner_note="NOTE: a stranger asks",
    refs=[],
    model_tier="kling3_0",
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F02 -- "We may eat it, and die"  (KJV 1 Kings 17:12, her own voiced line)
# Fray PEAK. Needs R_WIDOW/R_WIDOW_FACE/R_GATE.
# ===========================================================================
F02 = PageSpec(
    seq_title="AN HANDFUL OF MEAL",
    frame_label="F02",
    panels=(
        Panel("the last handful",
              "looking straight down into the open mouth of an earthenware meal jar, a thin "
              "handful's worth of pale meal dusting its bottom"),
        Panel("a little oil",
              "a palm-sized clay cruse lying tilted, near empty, one soft gleam of oil at its lip"),
        Panel("two empty bowls",
              "a bare low table with two empty clay bowls set out"),
    ),
    still_shot_type="CLOSE-UP",
    anim_shot_desc="close-up",
    main_scene_still=(
        f"tight on the widow before the gate's shadowed stones. {WIDOW_BUILD}, her head and "
        "shoulders filling the frame, the bundle of dry sticks clutched against her chest with "
        "both arms, fully inside the frame; her eyes down, her face emptied of hope, resigned; "
        "her figure's linework destabilized to its furthest point -- her contour visibly broken "
        "and doubled, a faint tremored second line running beside the true line of her shoulder, "
        "cheek, and arms, the hatching scratchy, overworked, almost flying -- while every stone "
        "and stick around her is drawn steady and single-struck. Stage 0 dosage: no blue Swirls "
        "of Life ink motif anywhere on this page -- no blue ink appears anywhere in the scene, "
        "the panels, or the margins."
    ),
    material_closer=(
        "the broken, tremored linework of the widow's own figure is the only unusual ink at work "
        "on this page, and no blue appears anywhere."
    ),
    panel_motions=(
        "the light inside the jar's mouth deepens very slightly, nothing else changes",
        "the gleam of oil at the cruse's lip catches the light softly and settles",
        "the two empty bowls sit undisturbed on the bare table",
    ),
    main_scene_animation=(
        "the widow takes one slow shallow breath; her eyes lower the last small distance and "
        "settle, finishing early and holding still; her grip on the stick bundle tightens once "
        "and stills; her lips stay closed and completely still -- she is not speaking and her "
        "mouth does not move at all;"
    ),
    fence_kind="fray",
    fence_callout="the broken, doubled, tremored linework of the widow's figure and its scratchy flying hatching",
    caption_lines=("we may eat it,", "and die"),
    corner_note="NOTE: the funeral fire",
    refs=[R_WIDOW, R_WIDOW_FACE, R_GATE],
    model_tier="kling3_0",
    clip_duration=9,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F03 -- "Fear not"  (KJV 1 Kings 17:13)
# The gospel turn's first half. Page turn FROM F02 IS the Fray clearing --
# the widow's linework arrives already steadied; the swirl's first trace
# arrives WITH the word. Needs R_WIDOW/R_WIDOW_FACE/R_ELIJAH/R_ELIJAH_FACE/R_GATE.
# ===========================================================================
F03 = PageSpec(
    seq_title="AN HANDFUL OF MEAL",
    frame_label="F03",
    panels=(
        Panel("steady eyes", "a close study of Elijah's weathered face, his eyes level and unafraid"),
        Panel("a cake first", "one small round flat cake resting on an open upturned palm"),
        Panel("go and do", "the narrow lane from the gate running toward low flat-roofed houses"),
    ),
    still_shot_type="WIDE TWO-SHOT",
    anim_shot_desc="wide two-shot, pulled back further than any earlier page in this sequence",
    main_scene_still=(
        f"a wide pulled-back view before the gate of Zarephath, small figures against open "
        "ground -- the gate itself now only a third of the frame's width, not filling it, with "
        "the narrow lane beyond the gate visible curving away toward the low flat-roofed houses "
        "in the distance, and a wide open sky above taking up the whole upper half of the frame. "
        f"{ELIJAH_BUILD}, his hair and beard matching reference image 3 and image 4 EXACTLY: the "
        "same thick grey-STREAKED black mane and full grey-streaked beard, never solid white "
        "hair or a solid white beard -- fully inside the frame, small in the wide ground, facing "
        "the widow, his staff grounded, his free hand lifted gently palm-out toward her, already "
        f"extended, his linework steady, single-struck, confident. {WIDOW_BUILD}, fully inside "
        "the frame, small in the wide ground, facing him, her arms loosened at her sides, her "
        "chin just beginning to lift, her contour whole and single again though her hatching "
        "stays loose and worked; the small bundle of dry sticks now lying on the bare ground "
        "between the two figures, fully inside the frame, with clean open ground around it -- "
        "the sticks themselves lying cold, dry, and completely unlit: no flame, no ember, no "
        "glow, no smoke, and no orange or red color of any kind anywhere on or around the "
        "sticks; cracked dry earth, no water drawn anywhere. Stage 1 dosage: exactly one "
        "restrained thread of blue ink rising thin from the two dry sticks lying on the ground "
        "between them, cool blue in color only, never orange, never red, never flame-colored, "
        "touching only the sticks and the air just above them, the only blue on the whole page, "
        "behaving like one stroke of wet ink bled into the paper, a clean band of untouched "
        "paper between the thread and both figures."
    ),
    material_closer=(
        "the widow's loosened hatching and the single blue thread above the sticks are the only "
        "two kinds of unusual ink at work on this page, kept apart by clean paper."
    ),
    panel_motions=(
        "Elijah's sketched face holds, the light across it warming very slightly",
        "the small cake sits undisturbed on the open palm",
        "a thin banner of dust drifts low along the empty lane",
    ),
    main_scene_animation=(
        "the widow's chin completes its lift and her shoulders drop and settle, finishing early "
        "and holding still; Elijah stays exactly as drawn, his lifted palm not moving further, "
        "one slow steady breath, his lips staying closed and completely still -- he is not "
        "speaking and his mouth does not move at all; the single thin blue ink thread stays "
        "exactly as drawn, in place, for the whole clip;"
    ),
    fence_kind="fray",
    fence_callout="the loosened hatching of the widow's figure and the single blue thread above the sticks",
    caption_lines=("Fear not",),
    corner_note="NOTE: before the miracle",
    refs=[R_WIDOW, R_WIDOW_FACE, R_ELIJAH, R_ELIJAH_FACE, R_GATE],
    model_tier="kling3_0",
    clip_duration=9,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F04 -- "The barrel of meal wasted not"  (narration: giving + miracle,
# compressed into one scene exactly as the narration compresses them)
# Fray gone (FR0). Interior debut of the house + the barrel/cruse (ref-crop
# page for R_BARREL). Needs R_WIDOW/R_WIDOW_FACE/R_ELIJAH/R_ELIJAH_FACE.
# ===========================================================================
F04 = PageSpec(
    seq_title="AN HANDFUL OF MEAL",
    frame_label="F04",
    panels=(
        Panel("a stranger fed", "Elijah's weathered hands breaking a small flat cake over a plain bowl"),
        Panel("the cruse", "the small clay cruse standing upright, stopper set beside it, one soft gleam of oil at its lip"),
        Panel("wasted not",
              "looking straight down into the jar's open mouth, a thin handful's worth of pale meal dusting its bottom"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        "the single dim room of the widow's small mud-brick house, morning light through the low "
        "doorway. In the foreground, the meal barrel -- a waist-high rounded earthenware storage "
        "jar of fired ochre-umber clay, one smooth ceramic body with a wide open mouth and two "
        "small clay lug handles, its flat round lid set aside, never wooden planks, never metal "
        f"hoops -- fully inside the frame, the small stoppered clay cruse standing beside it. "
        f"{WIDOW_BUILD}, fully inside the frame, her face, age, and headscarf matching reference "
        "image 1 and image 2 EXACTLY: the same gaunt, hollow-cheeked, famine-worn face with large "
        "deep-set dark eyes, never a smooth young face; the same undyed grey-brown headscarf with "
        "its narrow band of faded clay-red woven at the edge, never a plain white or cream scarf "
        "with no band -- kneeling at the jar, her hand just drawn back from its mouth a "
        "hand's-width clear of the rim, a fresh handful of pale dry meal -- warm ochre-cream, "
        "never blue -- lifted in her open fingers, her face turning toward it in the first break "
        "of wonder; her contour drawn steady, confident, and single-struck, no doubled or "
        f"tremored line anywhere in her figure. Behind her at a low table, {ELIJAH_BUILD}, his "
        "hair, beard, and mantle matching reference image 3 and image 4 EXACTLY: the same thick "
        "grey-STREAKED black mane and full grey-streaked beard, never solid white hair or a solid "
        "white beard; the same rough shaggy camel-hair mantle with its long matted fur texture, "
        "never a plain smooth cloak -- seated, a small flat cake before him, and beside him the "
        "widow's son, a thin boy of seven or eight, large dark eyes in a small famine-thinned "
        "face, a plain patched undyed tunic, watching the jar wide-eyed, both fully inside the "
        "frame. No liquid drawn pouring anywhere on the page. Stage 2 dosage: the blue ink motif "
        "is quietly present -- a few soft blue threads and one small rounded watercolor bloom "
        "rising from the open mouth of the meal jar, the bloom a soft blurred stain of pigment "
        "with no stem, no petals, and no leaf shape, never a literal flower, touching only the "
        "jar's rim and the air above it, touching no person and nothing else on the page, "
        "behaving like wet ink bled into the paper."
    ),
    material_closer=(
        "the soft blue threads at the jar's mouth are the only unusual ink at work on this page; "
        "every figure's linework is steady and single-struck."
    ),
    panel_motions=(
        "Elijah's hands complete the breaking of the cake and hold",
        "the gleam at the cruse's lip warms softly and settles",
        "the light inside the jar's mouth deepens very slightly, nothing else changes",
    ),
    main_scene_animation=(
        "the widow's hand completes its small lift and a few grains of pale meal sift down from "
        "her fingers and fall, then her hand holds still; her face stays turned toward her open "
        "hand; Elijah and the boy stay exactly as drawn, each one slow breath; the soft blue "
        "threads near the jar's mouth drift gently within their own small area; the cruse sits "
        "still beside the jar;"
    ),
    fence_kind="none",
    caption_lines=("the barrel of meal", "wasted not"),
    corner_note="NOTE: she gave first",
    refs=[R_WIDOW, R_WIDOW_FACE, R_ELIJAH, R_ELIJAH_FACE],
    model_tier="kling3_0",
    clip_duration=9,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F05 -- "Sarepta, a city of Sidon"  (KJV Luke 4:25-26, Jesus's own citation)
# THE GOSPEL TURN, fulfilment-on-page. Same synagogue as Naaman ep4's F06,
# one minute EARLIER in the sermon (crowd seated, hardening -- not yet risen).
# Swirl held at Stage 2 (episode cap, not 3 -- matches Naaman's own
# precedent). No Fray -- this is not the widow's own page.
# ===========================================================================
F05 = PageSpec(
    seq_title="AN HANDFUL OF MEAL",
    frame_label="F05",
    panels=(
        Panel("her city", "Zarephath's low rooftops by the flat grey sea, small"),
        Panel("many widows", "several distant veiled figures standing apart across open ground, dignified"),
        Panel("the syrian", "a far small figure standing waist-deep in a river gorge"),
    ),
    still_shot_type="MEDIUM WIDE shot",
    anim_shot_desc="medium wide shot",
    main_scene_still=(
        f"the plain stone synagogue interior. {JESUS_BUILD}, fully inside the frame, seated on "
        "the low stone bench at the front, his hands at rest, his gaze steady and level; beside "
        "him the simple wooden reading desk with the closed scroll lying on it, fully inside the "
        "frame. Around him on low benches, the men of Nazareth still seated, drawn as one "
        "dense-hatched mass -- townsmen in plain undyed and ochre wool, faces turned toward "
        "Jesus, hardening, brows drawn down, a few heads inclined toward one another, no single "
        "face individuated or finished anywhere in the mass, their gathering anger carried "
        "entirely in posture and stillness, not one man risen, fully inside the frame. Stage 2 "
        "dosage, held at this episode's own cap: the blue ink motif quietly present -- a few "
        "soft blue threads with the faintest trace of muted gold, and one small watercolor "
        "bloom, rising from the closed scroll on the reading desk beside him, touching only the "
        "scroll and the air above the desk, touching no person on the page."
    ),
    material_closer=(
        "the blue-and-gold threads on the scroll are the only living ink on the page."
    ),
    panel_motions=(
        "a thin haze drifts over the sea beyond the rooftops",
        "the far veiled figures stand undisturbed, dignified",
        "the river's surface glimmers faintly around the far figure, who holds still",
    ),
    main_scene_animation=(
        "the seated crowd mass does not move at all for the entire clip -- no man shifts, leans, "
        "inclines his head, or changes posture in any way, no man rising at any point, every man "
        "keeps his lips exactly as drawn, not speaking; Jesus does not move at all for "
        "the entire clip -- no breath, no shift of weight, no change of expression, his lips "
        "staying closed and completely still, not speaking, his whole body and every part of him "
        "staying at exactly its original drawn size and exactly its original drawn position, "
        "never growing, never shrinking, never shifting, his head and face staying fully visible "
        "inside the frame the entire time; every single figure on the page, Jesus and every man "
        "in the crowd alike, stays at exactly its original drawn size and position for the whole "
        "clip; the space above and beside every figure on the page stays completely empty for "
        "the whole clip -- no round, oval, or cloud-shaped white or pale mark of any kind, no "
        "balloon, no bubble, no tail or pointer shape, and no lettering or text of any kind ever "
        "appears anywhere on the page beyond the two caption lines already given, at any point, "
        "in any frame, near any figure, foreground or background alike; the threads and bloom on "
        "the scroll drift gently within their own small area, never spreading beyond the scroll "
        "and the air above it; no new figure or mark appears anywhere on the page at any point;"
    ),
    fence_kind="none",
    caption_lines=("save unto Sarepta,", "a city of Sidon"),
    corner_note="NOTE: named centuries later",
    refs=[R_JESUS, R_SYNAGOGUE],
    model_tier="veo3_1_lite",
    clip_duration=8,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F06 -- "The one with nothing left"  (narration: "Of every hungry house in
# Israel, God went to the one with nothing left to give -- and asked her
# anyway.")
# The reflection beat, made literal: God went OUTSIDE Israel -- the one lit
# house stands apart, at the coast, not among the dark hills.
# ===========================================================================
F06 = PageSpec(
    seq_title="AN HANDFUL OF MEAL",
    frame_label="F06",
    panels=(
        Panel("no rain", "cracked bare earth under an empty rainless sky"),
        Panel("three full bowls", "the same low table, three plain clay bowls set out, filled"),
        Panel("her face, after",
              "a close study of the widow's face at rest, her linework steady and single, no tremor anywhere"),
    ),
    still_shot_type="WIDE shot",
    anim_shot_desc="wide shot",
    main_scene_still=(
        "dusk over a wide drought-stricken land: dark hills rolling away under a deepening sky, "
        "small flat-roofed houses scattered across them, every one of them dark and unlit; far "
        "beyond the hills at the coastline, small with distance and set apart across open "
        "ground, one single low house by the flat grey evening sea with a warm lit doorway, a "
        "thin line of pale hearth-smoke rising from its roof, fully inside the frame; the ground "
        "everywhere dry, no water drawn anywhere but the far sea. Her contour and the whole "
        "scene drawn steady, confident, and single-struck. Stage 2 dosage, held: a few soft blue "
        "threads with traces of muted gold and one small rounded watercolor bloom, floating "
        "freely in the open sky directly above the one lit house, small with distance, touching "
        "nothing below the sky and not attached to the frame's own top edge -- the bloom a soft "
        "blurred stain of pigment with no stem, no petals, no leaf, and no hanging vine shape, "
        "never a literal flower or plant of any kind."
    ),
    material_closer=(
        "the blue-and-gold threads above the one lit house are the only unusual ink at work on "
        "this page."
    ),
    panel_motions=(
        "a low banner of dust drifts across the cracked earth",
        "a faint curl of steam rises from the bowls and thins",
        "the sketched face holds, the light across it warming very slightly",
    ),
    main_scene_animation=(
        "the thin line of hearth-smoke rises steadily from the one lit roof and drifts, staying "
        "its own thin line; the far grey sea glimmers faintly along the coast; the blue-and-gold "
        "threads above the house drift gently within their own small area; every dark house on "
        "the hills stays exactly as drawn, none of them ever lighting;"
    ),
    fence_kind="none",
    caption_lines=("nothing left to give",),
    corner_note="NOTE: asked her anyway",
    refs=[R_WIDOW_FACE],
    model_tier="veo3_1_lite",
    clip_duration=5,
    panel_style="woodcut_hybrid",
)

PAGES = {"f01": F01, "f02": F02, "f03": F03, "f04": F04, "f05": F05, "f06": F06}

# ---- covers -------------------------------------------------------------
# The narration opens on the widow, not on Jesus (the opposite of Naaman) --
# so the covers belong to HER world; the Nazareth beat stays interior (F05).
# See docstring + _DESIGN_BRIEF.md section 4 for the full reasoning.

FRONT_COVER = CoverSpec(
    side="front",
    scene=(
        f"{WIDOW_BUILD}, small and isolated in the lower third, standing bent forward at the "
        "waist before the gate of Zarephath, a full bundle of dry sticks held close against her "
        "chest and stomach with both arms wrapped fully around it, both hands closed and resting "
        "still on the bundle, not reaching or open toward anything, no loose sticks anywhere on "
        "the ground near her -- the drystone posts and timber lintel rising behind her in the low "
        "mud-brick wall; beyond the wall, the town's low flat rooftops stepping down toward a "
        "flat grey sea on the far horizon; drought-bleached scrub, dust, a bare dead tree, the "
        "bare ground around her otherwise empty."
    ),
    lighting=(
        "A low smoldering ember-orange sun breaking under a heavy slate-grey famine sky, its "
        "warm light raking the ground and the sticks in her arm; cold blue-teal shadow holding "
        "the gate, the wall, and the sea, cinematic atmospheric haze, dramatic volumetric light "
        "rays, photographic tonality."
    ),
    background_detail="",
    title="AN HANDFUL OF MEAL",
    subtitle="1 KINGS 17",
    title_position="top",
    animation=(
        "a low dry wind moves across the whole scene, stirring loose fabric and the dead scrub; "
        "the ember light stays exactly as warm and low as it already is, unchanged"
    ),
    extra_avoid="emaciated horror, skeletal figures, corpses",
    refs=[R_WIDOW],
    clip_duration=4,
)

BACK_COVER = CoverSpec(
    side="back",
    scene=(
        "the dim interior of the widow's small mud-brick house at dawn; the meal barrel -- the "
        "earthenware storage jar, never wooden staves, never metal hoops -- standing open in the "
        "lower third, its flat lid leaning against its side, mouth toward the door; a shaft of "
        "dawn light through the low open doorway falls across the jar's open mouth and the pale "
        "meal inside it; the little clay cruse standing beside the jar, stoppered; in the "
        f"doorway beyond, {WIDOW_BUILD}, standing small, half-silhouetted against the light, at "
        "rest."
    ),
    lighting=(
        "Warm dawn gold pouring through the doorway and pooling in the jar's mouth; cold "
        "blue-grey night shadow still holding the room's corners and the floor's edges, "
        "cinematic atmospheric haze, photographic tonality."
    ),
    background_detail=(
        "One small hard-capped closed curl of blue ink with a trace of muted gold rises from the "
        "jar's open mouth into the light shaft, its whole visible length no longer than a hand's "
        "width, curled into one small closed loop, never straightening, never trailing, behaving "
        "like a small dab of living ink, never a glow."
    ),
    title="HE NEEDS IT OPEN",
    subtitle="LUKE 4:26",
    title_position="bottom",
    animation=(
        "fine dust motes drift slowly through the dawn shaft; the widow's scarf stirs faintly in "
        "the doorway air; the blue curl stays exactly as drawn; the dawn light stays exactly as "
        "warm and low as it already is, unchanged"
    ),
    extra_avoid=(
        "wooden staves, metal hoops, wine cask, drawn border, picture frame, outline rectangle "
        "around the image, separate caption strip or bar below the scene, divider line between "
        "the picture and the title lettering"
    ),
    refs=[R_BARREL, R_WIDOW],
    clip_duration=8,
)

COVERS = {"front": FRONT_COVER, "back": BACK_COVER}

# ---- assembly manifest ---------------------------------------------------
# Word weights are Fable's own estimates against the locked narration (sum 212,
# matching narration.md's real word count). Modes follow the Naaman lesson:
# boomerang ONLY for genuinely non-directional ambience; anything with real
# directional motion (a lift, a rising smoke line, a settling gesture) gets
# freeze (+tail_loop where a completing gesture settles near the clip's end).
# Final modes are an assembly-QC call on the real renders, per the standing
# rule -- these are starting choices, not locked.

MANIFEST = EpisodeManifest(
    episode_dir=HERE,
    narration=HERE / "narration.mp3",
    units=[
        Unit("front", HERE / "front_cover.mp4", 10, "freeze"),
        Unit("f01", HERE / f"{HERE.name}_f01_9x16.mp4", 22, "freeze", tail_loop_seconds=1.0),
        Unit("f02", HERE / f"{HERE.name}_f02_9x16.mp4", 27, "freeze", tail_loop_seconds=1.0),
        Unit("f03", HERE / f"{HERE.name}_f03_9x16.mp4", 33, "freeze", tail_loop_seconds=1.5),
        Unit("f04", HERE / f"{HERE.name}_f04_9x16.mp4", 26, "freeze"),
        Unit("f05", HERE / f"{HERE.name}_f05_9x16.mp4", 38, "freeze"),
        Unit("f06", HERE / f"{HERE.name}_f06_9x16.mp4", 22, "freeze"),
        Unit("back", HERE / "back_cover.mp4", 34, "freeze"),
    ],
    scores={
        # Felt-piano identity reused near-verbatim from episode 8/Naaman (two-episode
        # validated series default), re-timed to this episode's own arc -- see
        # generate_score_piano.py's own docstring. Duck profile STARTS from Naaman's
        # own working values (same trap measured: raw score -19.9dB vs narration's
        # -18.5dB, nearly equal) -- re-measure against the real mixed output before
        # calling this final, per this project's own "a duck does not transfer
        # between score generations" rule.
        "piano": ScoreVariant(
            score=HERE / "score_piano.mp3",
            duck=DuckProfile(gain_db=-6, threshold=0.12, ratio=2.5, release_ms=250),
            out=HERE / f"{HERE.name}_final_piano.mp4",
        ),
    },
    panel_style="woodcut_hybrid",
)
