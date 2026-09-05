"""Episode spec for "Where Are the Nine" (Luke 17:11-19, ten lepers cleansed on
the road; one, a Samaritan, returns). Dead ink: STAIN (uncleanness) -- ONE
corporate stain under a company of TEN men, the series' first Stain carried by
a group, and the first whose clearing happens with Jesus OUT OF FRAME (the
series-plan v4 locked continuity fix, executed here). NO Fray anywhere -- the
ten cry out in need, not in doubt; the nine who walk on are OBEDIENT, not
wavering. NT episode, Jesus bodily present and speaking on the bookend pages,
absent on the two road pages -- Stage 3 begins on the hero (F09) and completes
on F10. panel_style woodcut_hybrid throughout. Voices: narrator + jesus
(voices.json -- the lepers' cry stays in the narrator's voice).

Design authored by Fable (full brief: `_DESIGN_BRIEF.md` in this folder),
implemented by Sonnet per the "Fable designs, Sonnet executes" rule. The user
confirmed two open calls: back-cover subtitle = EPHESIANS 2:8 ("For by grace
are ye saved through faith... not of works" -- the doctrine the narration held
through six panel-rounds); hero page = F09 (Christ's own word, "thy faith hath
made thee whole" -- the gospel pivot, not the emotional climax which is F06).

THE TWO HARD PROBLEMS (full reasoning in _DESIGN_BRIEF.md section 2):

1. Jesus is out of frame when the actual cleansing happens ("as they went,
   they were cleansed", v14). Fixed by making the Stage-1 swirl thread the
   WORD, not the man: it rises from Jesus's sending hand on F03 (he is still
   in frame, they have just turned to obey) with its tip already leaning
   toward the road; on F04 (Jesus beyond the left frame edge) the SAME single
   thread enters at the upper-left edge and runs high above the walking group
   -- his word traveling with them, never his figure, never touching anyone.
   The clearing itself is the page CUT (F03 wet D3 stain -> F04 dried D1 ring)
   -- no clip ever shows it happening (LAW 2: a stain never clears inside a
   clip).

2. The two-tier-ending risk -- making sure the pictures never say "the nine
   got less." Solved by splitting the two motifs' jobs: the STAIN's clearing
   is the GIFT and is identical for all ten (F04 shows the whole company
   cleansed as one group, before anyone responds; F05 puts nine and one on
   the same wholly clean D0 paper under the same single thread, differing
   only in direction -- the nine drawn upright, unhurried, obedient, never
   diminished). The SWIRL is the GIVER and is anchored to Jesus's own hand
   only, on every page he appears on -- it never touches, rises from, or is
   "for" the Samaritan. He receives no extra ink; he goes to where the ink
   is. F07's road is empty (absence, not punishment); F10's two footprint
   tracks are equal size, equal line, equal light.

Reverence guard (hard problem #3): the Samaritan is a man among ten -- no
ethnic costume, no darker skin, no head-dress marking him as "other"; distinct
only by his own face (refs) and a narrow clay-red band on an olive-grey
mantle, per the same non-caricature standard as every other named character
in this series.

Leprosy skin wording: Fable's brief flagged this as design intent pending a
check against ep4 Naaman's own validated string. Naaman's `NAAMAN_PATCHES`
constant ("a scatter of faint pale dry patches ... matte, dry, unbroken skin,
like frost settled on skin, never raw, never a wound, never over his face")
is the only prior leprosy render in the series -- reused here (adapted to a
group, three zones) in place of Fable's own draft wording.

COUNT is this episode's literalism trap (the Barrel's "barrel", the Bier's
"bier"): every group page states "exactly ten -- count them"; F05 states
"nine ... and this one make ten"; the eye-QC checklist counts before anything
else on every group page/panel.
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

# ---- character / object / location continuity builds -----------------------

# LOCKED series-wide, reused verbatim from episode 10 (itself from ep7/ep4/ep1/ep8).
# jesus_ref.png copied verbatim from episode 10's own refs/ directory -- no redesign,
# no new approval cycle.
JESUS_BUILD = (
    "Jesus, a Judean man in his early thirties, medium height and ordinary build, sun-browned "
    "skin, shoulder-length dark brown hair pushed back from his face, a short full dark beard, "
    "wearing a simple ankle-length robe of undyed cream-brown wool with a plain olive-toned "
    "mantle draped over one shoulder, a narrow rope belt, and flat worn leather sandals -- no "
    "halo, no glow, nothing in his dress distinguishing him from the men around him, standing "
    "square, still, and unhurried, his gaze steady and direct"
)

# New to the series -- a GROUP identity, no individual refs (the nine never individuate in
# the text, and individuating them would invite a "nine bad men" reading -- see brief section
# 3). Leprosy wording adapted from ep4 Naaman's own validated NAAMAN_PATCHES string (the
# series' only prior leprosy render), not Fable's own draft wording, per the brief's own
# instruction to prefer a validated string where one exists.
TEN_BUILD = (
    "exactly ten men -- count them -- no more, no fewer: gaunt, sun-worn men of the region in "
    "coarse rent tunics of undyed grey-cream and ochre wool torn open at the breast, their "
    "heads bare, each with a strip of cloth bound over his upper lip and mouth, a scatter of "
    "faint pale dry patches on the backs of their hands, their forearms, and their bare shins "
    "-- matte, dry, unbroken skin, like frost settled on skin, never raw, never a wound, never "
    "over any face -- their hands empty; nine of them unindividuated, faces half-hidden by "
    "their cloths, drawn as different men in the same steady, confident, single-struck line, "
    "no doubled or tremored contour on any of them; no bells, no rattles, no begging bowls, no "
    "bandages, no hoods"
)

# New to the series. Unnamed -- the narration calls him "one," "a Samaritan," and (in Jesus's
# mouth) "this stranger." Reverence guard: no ethnic costume, no darker skin than the nine, no
# turban or foreign head-dress -- a man among ten men, distinct only by his mantle's clay-red
# band and his own face.
SAMARITAN_BUILD = (
    "the Samaritan, a man of about forty, lean and weathered, olive-brown skin like the men "
    "around him, a long face with a broad brow, deep-set dark eyes with heavy brows, a strong "
    "straight nose, and a close-cropped black beard flecked with grey; dark hair cut short, his "
    "head bare -- no headband, no head-wrap, no turban, no cloth of any kind tied around his "
    "head; wearing THE EXACT SAME PLAIN coarse rent tunic as the other nine men (same cut, same "
    "length, same undyed grey-cream wool, torn open at the breast the same way) with a plain "
    "mantle of faded olive-grey wool worn over one shoulder in the SAME PLAIN DRAPE as any "
    "ordinary mantle; his ONLY distinguishing mark is a single thin line of clay-red color "
    "running along the OUTER HEM EDGE of his mantle only, like a plain sewn edge-trim on a "
    "garment border -- this red line lies FLAT along the mantle's existing hem, following the "
    "hem's own edge exactly, and must NEVER appear as a diagonal band, sash, or ribbon crossing "
    "his chest or torso, must NEVER cross his body diagonally from shoulder to waist, must NEVER "
    "be a decorative garment layered over or under the mantle, and is not repeated anywhere else "
    "on his clothing; bare dusty feet; he is the SAME height, SAME build, and SAME plainness as "
    "the nine men beside him, not more elaborate, not more voluminous, not wearing an extra "
    "layer, not more richly colored, blending into the group at first glance except for that one "
    "thin edge-line; drawn with the same care, the same line weight, and the same dignity as "
    "every other man on the page; when a reference image is attached, match its face and its "
    "plain edge-trim placement exactly, not any dramatic drape or pose the reference may show"
)

# The location of every Jesus page (F01-F03, F06-F10, back cover). LAW 3 for this episode:
# no water anywhere -- the threads live in the sky/air on every page.
VILLAGE_EDGE_BUILD = (
    "the edge of a small Galilean-border village: a few low flat-roofed houses of pale "
    "field-stone with a low dry-stone wall running out from them, a bare terebinth tree, and a "
    "dry dirt road beginning at the wall's end and running away over open stony hill country; "
    "no well, no spring, no stream, no water anywhere -- the ground dry ochre earth and stone"
)

# The location of the two Jesus-absent pages (F04, F05).
ROAD_BUILD = (
    "the same dry dirt road further along, running from left to right over a low rise of open "
    "stony hill country, dry ochre earth, scattered field-stones, thin dry grass, no wall, no "
    "building, no tree, and no water of any kind"
)

R_JESUS = Ref("Jesus -- his face, build, and dress", str(REFS_DIR / "jesus_ref.png"))
R_TEN = Ref(
    "the company of ten lepers -- match their rent garments, bare heads, and the cloth bound "
    "over each mouth",
    str(REFS_DIR / "ten_ref.png"),
)
R_SAMARITAN = Ref(
    "the Samaritan -- his face only, and the plain edge-trim placement on his mantle (ignore "
    "any dramatic drape or pose in the reference itself, use only the face and the thin-edge-"
    "trim detail)",
    str(REFS_DIR / "samaritan_ref.png"),
)
R_SAMARITAN_FACE = Ref(
    "the Samaritan -- his face and eyes only, for close crops",
    str(REFS_DIR / "samaritan_face_ref.png"),
)
R_VILLAGE = Ref(
    "the village edge -- its exact houses, dry-stone wall, and terebinth tree",
    str(REFS_DIR / "village_edge_ref.png"),
)
R_ROAD = Ref(
    "the road further along -- its exact rise and hill country, no figures",
    str(REFS_DIR / "road_ref.png"),
)

# ===========================================================================
# F02 -- "Jesus, Master, have mercy on us" (KJV 17:13) -- THE DEBUT PAGE,
# renders FIRST. The ten large enough to crop ten_ref + samaritan_ref +
# village_edge_ref. Three Levitical marks fill the panels so the main scene
# can be the cry itself.
# ===========================================================================
F02 = PageSpec(
    seq_title="WHERE ARE THE NINE",
    frame_label="F02",
    panels=(
        Panel("covered lip",
              "a strip of cloth bound over a man's upper lip and mouth, close, his eyes above it"),
        Panel("rent garment",
              "the torn-open breast of a coarse tunic, close, the tear's frayed edge"),
        Panel("have mercy",
              "one raised open hand against the sky, a faint pale mark on its back"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        f"{TEN_BUILD}, standing together at the right in a tight huddled company arranged in "
        "TWO staggered rows so all ten are individually countable -- a front row of six men "
        "fully visible head to foot, and a second row of four more men standing close behind "
        "and between them, each of the four back-row heads and raised hands clearly visible "
        "above and between the shoulders of the front row -- EXACTLY TEN HEADS TOTAL, EXACTLY "
        "TEN RAISED HANDS TOTAL, count every head and every hand before finishing this image; "
        "crying out -- heads lifted, arms raised, hands open and empty; WITHOUT ANY EXCEPTION, "
        "every one of the ten men, including the man with the clay-red mantle band, has his "
        "own strip of cloth bound fully over his upper lip and mouth -- no man's bare mouth, "
        "lips, or teeth are visible anywhere in the scene, no man is drawn shouting with an "
        "uncovered mouth, every mouth without exception stays hidden behind its bound cloth -- "
        "fully inside the frame; one of the ten the man in the olive-grey mantle with the "
        f"narrow clay-red band ({SAMARITAN_BUILD}, his mouth ALSO fully covered by his own "
        "bound lip-cloth like every other man here), fully inside the frame among the others, "
        "in no way set apart from them; far beyond them at the frame's left, small, the edge "
        f"of the village ({VILLAGE_EDGE_BUILD}) and {JESUS_BUILD} standing on foot at the "
        "wall's end, facing them across a long stretch of empty road, his hands empty, "
        "touching no one on this page; the whole ground dry, no water anywhere. The same cold "
        "grey-umber stain lies in the paper beneath the group where they stand, formless and "
        "matte, beneath the linework, crossing the drawn frame border into the right margin, "
        "unchanged, never over any face, bounded to less than a third of the page; a wide "
        "band of clean paper between it and the road, the village, and Jesus. Stage 0 "
        "dosage: no blue Swirls of Life ink motif anywhere on this page -- no blue ink "
        "appears anywhere in the scene, the panels, or the margins."
    ),
    material_closer=(
        "the cold stain in the paper beneath the ten men is the only unusual ink at work on "
        "this page, and no blue appears anywhere."
    ),
    panel_motions=(
        "the eyes above the cloth blink once fully -- close, then open again, ending wide open",
        "only the loose frayed threads at the very edge of the tear stir faintly in the wind; "
        "the tear's shape, size, and depth never change; the skin of the chest visible through "
        "the tear stays exactly as drawn -- no new mark, spot, shadow, hole, or darkening of any "
        "kind ever appears on that skin, at any point in the clip; nothing about the opening "
        "itself moves, widens, or deepens, only the frayed cloth threads at its rim",
        "the raised hand holds, the light across it warming very slightly",
    ),
    main_scene_animation=(
        "the ten men hold their raised arms up, their chests lifting once together with the "
        "breath of the cry and settling, their heads staying lifted, their cloths staying "
        "bound over their mouths, none stepping forward; the far figure of Jesus stays exactly "
        "as drawn, still; the loose ends of their garments stir in the wind; the cold stain in "
        "the paper stays exactly as drawn, never deepening, never spreading, never fading."
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain in the paper beneath the ten men",
    caption_lines=("Jesus, Master,", "have mercy on us"),
    corner_note="NOTE: as required",
    refs=[R_JESUS, R_SAMARITAN],
    model_tier="veo3_1_lite",
    clip_duration=6,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F01 -- "before a single one of them was healed" -- the establishing shot and
# the Stain's debut. Renders AFTER F02 (all refs already chained).
# ===========================================================================
F01 = PageSpec(
    seq_title="WHERE ARE THE NINE",
    frame_label="F01",
    panels=(
        Panel("leprosy",
              "a bare forearm and the back of a hand, close, with a few faint pale dry "
              "patches, no sore, no wound"),
        Panel("the road",
              "the dry dirt road leaving a village between a low stone wall and open ground, "
              "no one on it"),
        Panel("came back",
              "one small figure alone far down a road, facing the viewer, walking this way"),
    ),
    still_shot_type="WIDE shot",
    anim_shot_desc="wide shot",
    main_scene_still=(
        f"the edge of the village ({VILLAGE_EDGE_BUILD}) at the frame's left, fully inside the "
        f"frame; {JESUS_BUILD}, standing on foot on the dry road at the wall's end, facing "
        "right toward the road, still, his hands empty, touching no one on this page, fully "
        "inside the frame; the road running away to the right, EMPTY between him and them for "
        f"a long stretch; far along it at the frame's right, at a clear distance from him, "
        f"{TEN_BUILD} standing together in a huddle, stopped, looking toward him -- one of "
        f"them the man in the olive-grey mantle with the narrow clay-red band "
        f"({SAMARITAN_BUILD}, match the attached reference), among the others and in no way "
        "set apart from them; late-afternoon light, long shadows; the whole ground dry ochre "
        "earth and stone, no water anywhere. A cold grey-umber stain lies in the paper itself "
        "beneath and around the huddle of ten, formless and matte, lying beneath the linework "
        "so every drawn line passes over it unbroken, its feathered damp edge crossing the "
        "drawn frame border into the page's own right margin directly below them, never over "
        "any face, bounded to less than a third of the page; a wide band of clean paper "
        "between the stain and the empty road, the village, and Jesus; the stain nowhere near "
        "Jesus. Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page -- no "
        "blue ink appears anywhere in the scene, the panels, or the margins."
    ),
    material_closer=(
        "the cold stain lying in the paper beneath the ten men at the right is the only "
        "unusual ink at work on this page, and no blue appears anywhere."
    ),
    panel_motions=(
        "the light across the forearm warms very slightly and settles",
        "a thin banner of dust drifts across the empty road",
        "the far figure holds, still",
    ),
    main_scene_animation=(
        "Jesus stays exactly as drawn, one slow breath, his face toward the far men, his "
        "hands still and empty; the ten men stand still in their huddle, the loose ends of "
        "their rent garments and lip-cloths stirring faintly in the wind, none of them "
        "stepping forward; a low thin haze of dust drifts along the empty road between; the "
        "cold stain in the paper stays exactly as drawn, never deepening, never spreading, "
        "never fading."
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain in the paper beneath the ten men at the right",
    caption_lines=("Only one of them", "came back"),
    corner_note="NOTE: afar off",
    refs=[R_JESUS, R_SAMARITAN, R_VILLAGE],
    model_tier="veo3_1_lite",
    clip_duration=6,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F03 -- "Go shew yourselves unto the priests" -- his word, and their
# obedience before any difference. AT-CAP page (Stain D3 + Swirl 1 = 4).
# ===========================================================================
F03 = PageSpec(
    seq_title="WHERE ARE THE NINE",
    frame_label="F03",
    panels=(
        Panel("the priests",
              "a far walled town on a hill under evening light, small, no figures"),
        Panel("they obeyed",
              "the backs of two men walking away, their bare heads and the knots of their "
              "lip-cloths at the napes, close"),
        Panel("his word",
              "Jesus's right hand raised, open, palm forward, close"),
    ),
    still_shot_type="WIDE shot",
    anim_shot_desc="wide shot",
    main_scene_still=(
        f"the village edge ({VILLAGE_EDGE_BUILD}) at the left; {JESUS_BUILD}, standing on foot "
        "at the wall's end facing right, his right hand raised in sending -- already raised, "
        "open, palm toward the road, touching nothing -- fully inside the frame, his hands "
        f"otherwise empty, touching no one on this page; at the right, {TEN_BUILD}, all ten "
        "turned away from him and walking to the right along the road in the same direction, "
        "their backs to him, mid-stride, their cloths still bound over their mouths, the faint "
        "pale patches still on their hands and forearms, their heads bare, in no way changed "
        f"-- one of them the man in the olive-grey mantle with the clay-red band "
        f"({SAMARITAN_BUILD}), among the others; the stretch of empty road between him and "
        "them fully inside the frame; the ground dry, no water anywhere. The cold grey-umber "
        "stain lies in the paper beneath their walking feet, formless and matte, beneath the "
        "linework, EXACTLY as before -- its edge nearest Jesus as saturated as everywhere "
        "else, neither dried nor spread -- crossing the drawn frame border into the right "
        "margin, never over any face; their obedience is already in the picture and nothing "
        "about the stain has changed; a wide band of clean paper between the stain and the "
        "road behind them, the village, and Jesus; the stain nowhere near Jesus. Stage 1 "
        "dosage: exactly one restrained thread of blue ink rising from the back of Jesus's "
        "raised right hand into the air above it, its upper end leaning to the right toward "
        "the road the men are walking down, touching only his hand and the air, touching no "
        "man and nothing on the ground, the only blue on the whole page, behaving like one "
        "stroke of wet ink bled into the paper, smooth and open in its curl, never blot-shaped; "
        "the stain formless and matte, never swirl-shaped; a wide band of untouched clean "
        "paper between the thread and the stain at every point (they sit at opposite sides of "
        "the frame); the thread drawn ON the page's surface, the stain lying IN the paper "
        "beneath the linework."
    ),
    material_closer=(
        "the cold stain in the paper beneath the walking men and the single blue thread at "
        "his raised hand are the only two kinds of unusual ink at work on this page, kept "
        "apart by clean paper."
    ),
    panel_motions=(
        "a faint haze drifts over the far hill town",
        "the two backs hold their step, unmoving",
        "the raised hand holds, still",
    ),
    main_scene_animation=(
        "the ten men keep walking away from left to right along the road at an even pace, "
        "their backs to him, one continuous steady stride the whole clip, none turning; Jesus "
        "stays exactly as drawn, his raised hand held and not rising further, one slow breath, "
        "his lips staying closed and completely still -- he is not speaking and his mouth does "
        "not move at all; the single thin blue ink thread at his hand stays exactly as drawn, "
        "in place, for the whole clip; the cold stain in the paper beneath the walking men "
        "stays exactly as drawn, never deepening, never spreading, never fading."
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain in the paper beneath the ten walking men and the single blue thread at Jesus's raised hand",
    caption_lines=("Go shew yourselves", "unto the priests"),
    corner_note="NOTE: no difference yet",
    # SAMARITAN face ref dropped 2026-09-04: on masked-mouth pages the model kept copying
    # his ref's bare face over the required lip-cloth. His face isn't visually verifiable
    # while masked anyway -- text + the edge-trim detail carry him on this page.
    refs=[R_JESUS, R_VILLAGE],
    model_tier="veo3_1_lite",
    clip_duration=6,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F04 -- "as they went, they were cleansed" -- THE LOCKED-NOTE BEAT. The
# road, Jesus out of frame, the cut that IS the miracle.
# ===========================================================================
F04 = PageSpec(
    seq_title="WHERE ARE THE NINE",
    frame_label="F04",
    panels=(
        Panel("as they went",
              "bare walking feet on dry dust mid-stride, low, dust lifting"),
        Panel("before",
              "a bare forearm with the faint pale dry patches, close"),
        Panel("cleansed",
              "the same bare forearm, clean and unmarked, close, the same angle"),
    ),
    still_shot_type="MEDIUM WIDE PROFILE shot",
    anim_shot_desc="medium wide profile shot",
    main_scene_still=(
        f"the road ({ROAD_BUILD}) running from left to right over a low rise, no village "
        "anywhere in the frame; JESUS DOES NOT APPEAR ANYWHERE ON THIS PAGE -- not in the main "
        "scene, not in any panel -- there is NO robed teacher figure, NO leader, NO one guiding "
        "or walking ahead of or apart from the group, and no man in this scene has "
        "shoulder-length hair, a full dark beard, an ankle-length cream-brown robe, or flat "
        "leather sandals in the style of a rabbi -- the ONLY people visible anywhere on this "
        "page are exactly ten leprosy-marked lepers, no thirteenth or eleventh figure of any "
        "kind, no additional person; exactly ten men -- count them -- no more, no fewer: gaunt, "
        "sun-worn men of the region in coarse rent tunics of undyed grey-cream and ochre wool "
        "torn open at the breast, their heads bare, "
        "walking together along the road from left to right in profile, mid-stride, still one "
        "group -- exactly ten, count them -- and CLEANSED: every man's lip-cloth loosed and hanging "
        "at his throat, their mouths and faces bare, the skin of their hands, forearms, and "
        "shins clear and unmarked, standing taller, two of them looking down at their own "
        "bared forearms as they walk, one with an open hand lifted to his own uncovered mouth, "
        "their tunics still rent; one of them the man in the olive-grey mantle with the "
        f"clay-red band ({SAMARITAN_BUILD}, his lip-cloth now loosed, hanging at his throat), "
        "walking IN THE MIDDLE OF THE LINE shoulder-to-shoulder with the others, the EXACT "
        "same height and the EXACT same build as the nine men beside him, no taller, no more "
        "upright, no more finely dressed, wearing a short worn tunic to the same length as "
        "theirs under his mantle -- not a single figure in this scene is taller, more richly "
        "dressed, more youthful, or drawn with a fuller flowing robe than the rest; among the "
        "others; the ground dry ochre earth and stone, no water anywhere. Of the "
        "cold stain, nothing wet remains anywhere: only a thin, faint, pale dried watermark "
        "ring lies in the paper around the stretch of road the ten walk on -- the dried edge "
        "of the old stain, the stain itself gone -- and the paper inside that ring is the "
        "cleanest, brightest cream on the whole page; where the ring meets the drawn frame "
        "border at the right, only a pale dried trace remains on the margin; the ring contains "
        "no blue, no gold, and no red, and touches no figure's drawn line. Stage 1 dosage, "
        "held: exactly one restrained thread of blue ink high in the sky, entering the frame "
        "at its upper-left edge and running across the upper air above the walking men to a "
        "point a little ahead of them at the right, thin as a hair, tied to no figure, "
        "touching no man and nothing on the ground, the only blue on the whole page, behaving "
        "like one stroke of wet ink bled into the paper's sky wash, smooth and open, never "
        "blot-shaped; a wide band of clean paper between the thread in the sky and the dried "
        "ring on the ground at every point."
    ),
    material_closer=(
        "the dried pale ring in the paper around the road and the single blue thread high in "
        "the sky are the only two kinds of unusual mark on this page, and the paper inside the "
        "ring is the cleanest on it."
    ),
    panel_motions=(
        "dust lifts and drifts from the walking feet",
        "the marked forearm lies still, the light across it unchanged",
        "the clean forearm holds, the light across it warming very slightly",
    ),
    main_scene_animation=(
        "the ten men keep walking from left to right along the road at an even pace, one "
        "continuous steady stride the whole clip, the two looking at their forearms keeping "
        "their heads bowed to them, the one with his hand at his mouth holding it there, none "
        "turning; the loosed cloths at their throats stir with their steps; the single thin "
        "blue ink thread high in the sky stays exactly as drawn, in place, for the whole clip; "
        "the dried pale ring in the paper stays exactly as drawn, and no new stain, spot, or "
        "darkening appears anywhere on the page at any point."
    ),
    fence_kind="stain",
    fence_callout="the dried pale ring in the paper around the stretch of road the ten men walk on",
    caption_lines=("as they went,", "they were cleansed"),
    corner_note="NOTE: not in frame",
    # SAMARITAN ref re-added 2026-09-04 with a freshly regenerated, plainer samaritan_ref.png
    # (the old ref that caused the leader-figure defect here has been superseded). R_TEN
    # dropped project-wide -- a 10-person group reference doesn't chain reliably in this
    # model; the already-precise TEN_BUILD text carries costume consistency instead.
    refs=[R_SAMARITAN, R_ROAD],
    model_tier="veo3_1_lite",
    clip_duration=4,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F05 -- "One turned back" -- THE FORK. Two responses to one gift, on one
# page. Renders SECOND (after F02): crop source for samaritan_face_ref +
# road_ref.
# ===========================================================================
F05 = PageSpec(
    seq_title="WHERE ARE THE NINE",
    frame_label="F05",
    panels=(
        Panel("kept going",
              "a single pair of bare feet mid-stride on dry dust, toes pointing to the RIGHT, low"),
        Panel("loud voice",
              "two raised open hands against the sky, clean and unmarked, no face"),
        Panel("the village",
              "the far edge of the village small on its rise, the dry-stone wall and the bare "
              "tree, no figure"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        f"the road ({ROAD_BUILD}) running from left to right, the village "
        f"({VILLAGE_EDGE_BUILD}) tiny on the far-left horizon, no figure of Jesus anywhere in "
        "the frame; in the foreground at center-left, seen from the FRONT in a clear "
        "three-quarter view facing the viewer and facing the village on the left -- his back "
        "NEVER turned to the viewer, his whole body and face oriented the OPPOSITE way from "
        f"the walking men behind him -- {SAMARITAN_BUILD}, stopped and turned fully around to "
        "face this way, his lip-cloth loosed and hanging at his throat, his bare face clearly "
        "visible to the viewer and lifted a little toward the sky over the village, his open "
        "eyes and his whole face plainly visible, his mouth closed, both arms lifted from his "
        "sides with open, empty, clean hands turned palm up, his skin clear and unmarked, his "
        "rent tunic and olive-grey mantle with its clay-red band as before, fully inside the "
        "frame, drawn with the same care, the same line weight, and the same dignity as every "
        "other man on the page; beyond him "
        "to the right and smaller, NINE men -- nine, count them, nine and this one make ten -- "
        "walking on away from the viewer to the right along the road in the OPPOSITE direction "
        "from the way the foreground man now faces, their backs to the viewer, "
        "upright and unhurried, their cloths loosed, their skin clear, in the same clean "
        "confident line as the one, none shadowed, none hunched, none looking back; the ground "
        "dry, no water anywhere. No stain, ring, or grey blot anywhere in the paper -- the "
        "paper wholly clean beneath the nine and beneath the one alike. Stage 1 dosage, held: "
        "exactly one restrained thread of blue ink high in the sky, entering the frame at its "
        "upper-left edge and running across the upper air above ALL ten men -- over the nine "
        "walking away and over the one turned back alike -- thin as a hair, tied to no figure, "
        "touching no man and nothing on the ground, the only blue on the whole page, behaving "
        "like one stroke of wet ink bled into the sky wash, smooth and open, never blot-shaped."
    ),
    material_closer=(
        "the single blue thread high in the sky is the only unusual ink on the page, and the "
        "paper beneath every man is wholly clean."
    ),
    panel_motions=(
        "dust lifts from the striding feet and drifts",
        "the raised hands hold, the light across them warming very slightly",
        "a thin haze drifts over the far village",
    ),
    main_scene_animation=(
        "the Samaritan's raised open hands lift the last small distance higher and hold there, "
        "his face lifting with them and holding, his eyes open, his lips staying closed and "
        "completely still -- he is not speaking and his mouth does not move at all; the nine "
        "men beyond him keep walking away to the right at an even pace, one continuous stride, "
        "none turning; the loosed cloth at his throat stirs; the single thin blue ink thread "
        "high in the sky stays exactly as drawn, in place, for the whole clip; no new stain, "
        "spot, or darkening appears anywhere on the page at any point."
    ),
    fence_kind="none",
    caption_lines=("One turned back",),
    corner_note="NOTE: nine kept going",
    refs=[R_SAMARITAN],
    model_tier="kling3_0",
    clip_duration=4,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F06 -- "and fell down on his face at his feet" -- the emotional climax, NOT
# the hero. Jesus bodily in frame again; swirl rises to Stage 2.
# ===========================================================================
F06 = PageSpec(
    seq_title="WHERE ARE THE NINE",
    frame_label="F06",
    panels=(
        Panel("turned back",
              "a single pair of bare feet on dry dust, toes pointing to the LEFT, low"),
        Panel("on his face",
              "dry dust and a field-stone, close, the edge of a spread hand pressed into the dust"),
        Panel("a Samaritan",
              "the man's bowed profile, close, eyes closed, calm, drawn with care"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        f"the village edge ({VILLAGE_EDGE_BUILD}) at the left; {JESUS_BUILD}, standing on foot "
        "at the wall's end facing right, looking down, his right hand lowered and open, palm "
        "toward the man below him, not touching him, his hands otherwise empty, touching no "
        f"one on this page, fully inside the frame; on the dry road at his feet, "
        f"{SAMARITAN_BUILD}, fallen prostrate -- lying on his face, his forehead to the dust a "
        "hand's width before Jesus's sandals, not touching them, his arms stretched forward on "
        "the ground, his open empty hands spread on the dust, his lip-cloth loosed at his "
        "throat, his skin clear, his olive-grey mantle with its clay-red band fallen about his "
        "shoulders, fully clothed, fully inside the frame, drawn with the same care, the same "
        "line weight, and the same dignity as any figure on the page; the road beyond them to "
        "the right running away EMPTY over the rise, no other figure on it; the ground dry, no "
        "water anywhere. No stain, ring, or grey blot anywhere in the paper. Stage 2 dosage: "
        "the blue ink motif quietly present -- a few soft blue threads rising UPWARD ONLY from "
        "the back of Jesus's lowered hand into the air above it, every thread's root touching "
        "his hand directly and going up from there, none descending toward the man, the "
        "ground, or his feet, none dripping, none pooling; at the top of the threads, one "
        "soft, irregular, hazy patch of the same blue pigment, entirely amorphous, with soft "
        "feathered edges and no internal structure of any kind, exactly like a single drop of "
        "watercolor spreading into wet paper, touching only his hand and the air above it, "
        "touching no other person and nothing else on the page; the ground, the man, and his "
        "feet free of any ink of any kind; every thread behaving like wet ink bled into the "
        "paper, smooth and open, never blot-shaped."
    ),
    material_closer=(
        "the soft blue threads at Jesus's lowered hand are the only unusual ink on the page, "
        "and the paper beneath the man is wholly clean."
    ),
    panel_motions=(
        "dust drifts from the turned feet",
        "the pressed dust lies still, the light across it warming very slightly",
        "the bowed profile holds, tone-only",
    ),
    main_scene_animation=(
        "the Samaritan's shoulders heave once with the breath of his thanks and settle, his "
        "forehead staying to the dust, his spread fingers pressing into the dust and holding; "
        "Jesus stays exactly as drawn, his lowered open hand not moving further and not "
        "reaching down, his face on the man, one slow breath; the soft blue threads at his "
        "hand drift gently within their own small area, never lowering toward the man or the "
        "ground; a low thin haze of dust drifts along the empty road beyond; no new stain, "
        "spot, or darkening appears anywhere on the page at any point."
    ),
    fence_kind="none",
    caption_lines=("giving him thanks",),
    corner_note="NOTE: a Samaritan",
    refs=[R_JESUS, R_SAMARITAN, R_SAMARITAN_FACE, R_VILLAGE],
    model_tier="kling3_0",
    clip_duration=6,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F07 -- "but where are the nine?" -- the question aimed at the empty road.
# ===========================================================================
F07 = PageSpec(
    seq_title="WHERE ARE THE NINE",
    frame_label="F07",
    panels=(
        Panel("ten cleansed",
              "ten small clean figures standing in a line, cloths loosed, small, far -- TEN, "
              "count them"),
        Panel("the empty road",
              "a bend of the dry road over a rise with no one on it, a little dust hanging "
              "where men have gone"),
        Panel("out loud",
              "Jesus's face in profile, close, lips closed, brow lifted in the question"),
    ),
    still_shot_type="MEDIUM WIDE shot",
    anim_shot_desc="medium wide shot",
    main_scene_still=(
        f"the village edge ({VILLAGE_EDGE_BUILD}) at the left; {JESUS_BUILD}, standing on foot "
        "at the wall's end, his body and face turned to the RIGHT toward the road, his right "
        "hand lifted a little from his side toward it, open, palm up in the question -- "
        "already lifted, touching nothing -- his hands otherwise empty, touching no one on "
        f"this page, fully inside the frame; at his feet at lower center, {SAMARITAN_BUILD} "
        "still prostrate on the dust, his forehead to the ground a hand's width before the "
        "sandals, not touching them, his arms forward, his mantle with its clay-red band about "
        "him, fully inside the frame, drawn with the same dignity as any figure; the road "
        "running away to the right over the rise and out of sight, EMPTY -- no figure anywhere "
        "on it -- fully inside the frame, in the same clear late light as the village; the "
        "ground dry, no water anywhere. No stain, ring, or grey blot anywhere in the paper. "
        "Stage 2 dosage, held: a few soft blue threads rising UPWARD ONLY from the back of "
        "Jesus's lifted right hand into the air above it, their roots touching his hand and "
        "nowhere else, one soft amorphous watercolor patch at their top (as before), touching "
        "only his hand and the air, never descending toward the man, the ground, or the road, "
        "never reaching out along the road; the road and the man free of any ink of any kind."
    ),
    material_closer=(
        "the soft blue threads at his lifted hand are the only unusual ink on the page; the "
        "road beyond is empty and the paper wholly clean."
    ),
    panel_motions=(
        "the ten small figures hold, the light across them warming very slightly",
        "the hanging dust on the road bend drifts and thins",
        "the sketched profile holds, tone-only",
    ),
    main_scene_animation=(
        "Jesus's lifted hand rises the last small distance and opens a little wider toward the "
        "empty road, then holds, his face staying toward the road, his lips staying closed and "
        "completely still -- he is not speaking and his mouth does not move at all; the "
        "Samaritan holds exactly as drawn, his forehead to the dust, one slow breath through "
        "his back; the soft blue threads at Jesus's hand drift gently within their own small "
        "area, never lowering and never reaching out along the road; a low thin haze of dust "
        "drifts along the empty road; no new stain, spot, or darkening appears anywhere on the "
        "page at any point."
    ),
    fence_kind="none",
    caption_lines=("where are the nine?",),
    corner_note="NOTE: out loud",
    refs=[R_JESUS, R_SAMARITAN, R_SAMARITAN_FACE, R_VILLAGE],
    model_tier="kling3_0",
    clip_duration=8,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F08 -- "save this stranger" -- the word aimed at the man, presence after
# absence.
# ===========================================================================
F08 = PageSpec(
    seq_title="WHERE ARE THE NINE",
    frame_label="F08",
    panels=(
        Panel("not found",
              "a far dust cloud hanging over an empty road, no figures"),
        Panel("give glory",
              "a man's two raised open hands against the sky, clean, no face"),
        Panel("this stranger",
              "the man's hand spread open on the dust, weathered, clean, unmarked, close"),
    ),
    still_shot_type="CLOSE MEDIUM shot",
    anim_shot_desc="close medium shot",
    main_scene_still=(
        f"{JESUS_BUILD}, standing on foot on the dry road at the left, his face turned DOWN "
        "toward the man at his feet, calm, his right hand lowered and open, palm toward the "
        "man, not touching him -- already lowered -- his hands otherwise empty, touching no "
        "one on this page, his face and lowered hand and sandaled feet fully inside the frame; "
        f"at his feet, {SAMARITAN_BUILD} prostrate, his bowed head and shoulders and his "
        "spread hands on the dust large in the frame at the right, his forehead to the ground "
        "a hand's width before the sandals, not touching them, his loosed lip-cloth at his "
        "throat, his olive-grey mantle with its clay-red band across his back, fully inside "
        "the frame, drawn with the same care and dignity as any figure; the ground dry, no "
        "water anywhere; no road, no village, and no other figure needed in this tight frame. "
        "No stain, ring, or grey blot anywhere in the paper. Stage 2 dosage, held: a few soft "
        "blue threads rising UPWARD ONLY from the back of Jesus's lowered hand into the air "
        "above it, their roots touching his hand and nowhere else, one soft amorphous "
        "watercolor patch at their top (as before), touching only his hand and the air, never "
        "descending toward the man's back, head, or hands, never touching him; the man and the "
        "dust free of any ink of any kind."
    ),
    material_closer=(
        "the soft blue threads at his lowered hand are the only unusual ink on the page, and "
        "the paper beneath the man is wholly clean."
    ),
    panel_motions=(
        "the hanging dust drifts and thins",
        "the raised hands hold, the light warming very slightly",
        "the spread hand lies still on the dust",
    ),
    main_scene_animation=(
        "Jesus's eyes lower the last small distance to the man and hold there, his lowered "
        "open hand staying exactly as drawn and not reaching down, one slow breath, his lips "
        "staying closed and completely still -- he is not speaking and his mouth does not move "
        "at all; the man's back rises and falls with one slow breath, his forehead staying to "
        "the dust, his spread hands still; the soft blue threads at Jesus's hand drift gently "
        "within their own small area, never lowering toward the man; no new stain, spot, or "
        "darkening appears anywhere on the page at any point."
    ),
    fence_kind="none",
    caption_lines=("save this stranger",),
    corner_note="NOTE: he looked at him",
    refs=[R_JESUS, R_SAMARITAN, R_SAMARITAN_FACE, R_VILLAGE],
    model_tier="kling3_0",
    clip_duration=5,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F09 -- HERO -- "thy faith hath made thee whole" -- the gospel pivot.
# Faith and wholeness stay in ONE caption line -- never "made thee whole"
# alone.
# ===========================================================================
F09 = PageSpec(
    seq_title="WHERE ARE THE NINE",
    frame_label="F09",
    panels=(
        Panel("Arise",
              "Jesus's right hand extended low, open, palm UP, close, empty"),
        Panel("go thy way",
              "the dry road ahead, open and bright in morning light, no one on it"),
        Panel("thy faith",
              "a close study of the man's face, lifted, dust on his brow, eyes open on someone "
              "above him, contour steady"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        f"the village edge ({VILLAGE_EDGE_BUILD}) at the left; {JESUS_BUILD}, standing on foot "
        "at the wall's end, bent a little toward the man below him, his right hand extended "
        "low and open, palm UP, in the gesture of raising -- already extended, touching "
        "nothing -- his hands otherwise empty, touching no one on this page, his face on the "
        f"man, calm and kind, fully inside the frame; at his feet, {SAMARITAN_BUILD} rising "
        "from his face -- his forehead just lifted from the dust, his head coming up, his eyes "
        "open and meeting Jesus's for the first time, his hands still spread on the ground, "
        "his knees under him, his loosed lip-cloth at his throat, dust on his brow, his "
        "olive-grey mantle with its clay-red band about him, fully clothed, fully inside the "
        "frame, drawn with the same care, the same line weight, and the same dignity as any "
        "figure on the page; the road beyond to the right running away empty into morning "
        "light; the ground dry, no water anywhere. No stain, ring, or grey blot anywhere in "
        "the paper. Stage 3 beginning dosage: the blue ink motif begins to diffuse -- a few "
        "soft blue threads rising UPWARD from the back of Jesus's extended palm-up hand into "
        "the air above it, and for the first time one loose open band of blue ink threads with "
        "traces of muted gold drifting high in the air above BOTH figures, tied to no single "
        "figure, touching neither of them and nothing on the ground, no longer one single "
        "thread but not yet filling the scene, behaving like wet ink bled into the paper's sky "
        "wash, never a glow; the man, the dust, and the road free of any ink of any kind; the "
        "threads never descending toward the man and never rising from him."
    ),
    material_closer=(
        "the blue threads at his extended hand and the loose band beginning in the air above "
        "both figures are the only unusual ink on the page, and the paper beneath the man is "
        "wholly clean."
    ),
    panel_motions=(
        "the palm-up hand holds, the light across it warming very slightly",
        "a thin banner of dust drifts across the bright road",
        "the sketched face blinks once fully -- closes, then opens again fully, ending wide open",
    ),
    main_scene_animation=(
        "the Samaritan's head lifts the last small distance and holds, his eyes staying on "
        "Jesus's, his hands staying spread on the ground, his lips closed; Jesus's one small "
        "kind nod completes and holds, his extended palm-up hand staying exactly as drawn and "
        "not reaching further, his lips staying closed and completely still -- he is not "
        "speaking and his mouth does not move at all; the soft blue threads at his hand drift "
        "gently within their own small area, and the loose band high in the air above both "
        "figures drifts smoothly within its own fixed band, never lowering onto either of "
        "them; no new stain, spot, or darkening appears anywhere on the page at any point."
    ),
    fence_kind="none",
    caption_lines=("thy faith hath made thee whole",),
    corner_note="NOTE: Arise",
    refs=[R_JESUS, R_SAMARITAN, R_SAMARITAN_FACE, R_VILLAGE],
    model_tier="kling3_0",
    clip_duration=7,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F10 -- "Luke calls it thanks. Jesus calls it faith." -- the encounter
# complete, the man RISEN, face to face. The episode's Stage 3 page.
# ===========================================================================
F10 = PageSpec(
    seq_title="WHERE ARE THE NINE",
    frame_label="F10",
    panels=(
        Panel("kept walking",
              "a single track of bare footprints in dry dust running straight away from the "
              "viewer over a rise, no figure"),
        Panel("turned back",
              "a single track of bare footprints in dry dust that doubles back on itself, the "
              "returning prints laid over the departing ones, no figure"),
        Panel("faith",
              "Jesus's face, close, calm, his eyes on someone before him"),
    ),
    still_shot_type="MEDIUM TWO-SHOT",
    anim_shot_desc="medium two-shot",
    main_scene_still=(
        f"the village edge ({VILLAGE_EDGE_BUILD}) at the left, the dry road running away to "
        f"the right; {JESUS_BUILD}, standing on foot at the wall's end facing right, square "
        "and still, his right hand still open toward the man from the raising, low, not "
        "touching him, his hands otherwise empty, touching no one on this page, fully inside "
        f"the frame; before him, {SAMARITAN_BUILD}, RISEN -- standing upright on the road "
        "facing LEFT toward Jesus, close, whole, his face bare and level with Jesus's, his "
        "eyes on Jesus's eyes, his loosed lip-cloth hanging at his throat, his hands open and "
        "empty at his sides, his skin clear, his rent tunic and olive-grey mantle with its "
        "clay-red band as before, fully clothed, fully inside the frame, drawn with the same "
        "care, the same line weight, and the same dignity as any figure on the page; the road "
        "beyond him to the right empty in morning light; the ground dry, no water anywhere. No "
        "stain, ring, or grey blot anywhere in the paper -- the paper wholly clean. Stage 3 "
        "dosage: the blue ink motif, with traces of muted gold, is woven through the whole "
        "scene -- threads drifting in one loose open band through the air above the road and "
        "the village edge, over both heads, tied to no single figure, touching no person, "
        "touching nothing on the ground, behaving like wet ink bled through the page's own sky "
        "wash, never a glow."
    ),
    material_closer=(
        "the blue-and-gold band woven through the air above both men is the only unusual ink "
        "on the page, and the paper beneath them is wholly clean."
    ),
    panel_motions=(
        "a thin banner of dust drifts across the straight track",
        "the doubled-back track lies still, the light across it warming very slightly",
        "the sketched face holds, tone-only",
    ),
    main_scene_animation=(
        "the Samaritan's chest rises once in a slow breath and his open hands settle at his "
        "sides, his eyes staying on Jesus's, his lips closed; Jesus stays exactly as drawn, his "
        "open hand not moving, one slow breath, his lips closed and completely still -- not "
        "speaking; the loosed cloth at the man's throat stirs faintly; the blue-and-gold ink "
        "threads drift smoothly within their own fixed band across the air above both heads, "
        "never lowering onto either figure; a low thin haze of dust drifts along the empty "
        "road beyond; no new stain, spot, or darkening appears anywhere on the page at any "
        "point."
    ),
    fence_kind="none",
    caption_lines=("Luke calls it thanks.", "Jesus calls it faith."),
    corner_note="NOTE: face to face",
    refs=[R_JESUS, R_SAMARITAN, R_SAMARITAN_FACE, R_VILLAGE],
    model_tier="veo3_1_lite",
    clip_duration=8,
    panel_style="woodcut_hybrid",
)

PAGES = {
    "f01": F01, "f02": F02, "f03": F03, "f04": F04, "f05": F05,
    "f06": F06, "f07": F07, "f08": F08, "f09": F09, "f10": F10,
}

# ---- covers -------------------------------------------------------------
# The hook is ten men told to go before one was healed; the landing is "at his
# feet, not on the road." Covers are the two ends of that road: the TEN
# standing afar off (front, Jesus absent, the hook's own picture) and Jesus's
# feet at the village edge with the pressed place in the dust before them
# (back, the landing's own picture, no whole figure).

FRONT_COVER = CoverSpec(
    side="front",
    scene=(
        "ten men standing together in a ragged line across the lower third of the frame, "
        "small against the landscape, seen from the road in front of them at a distance -- "
        "gaunt, sun-worn, in coarse rent tunics torn open at the breast, heads bare, each with "
        "a strip of cloth bound over his upper lip and mouth, their hands empty at their "
        "sides, none stepping forward -- exactly ten, count them; behind and above them a dry "
        "dirt road climbing away over open stony hill country under carved structural cloud "
        "forms; at the far left edge, small, the low flat-roofed houses and dry-stone wall of "
        "a village, no one standing there."
    ),
    lighting=(
        "Warm low late-afternoon sun from behind the hills, rim-lighting the men's ragged "
        "shoulders and the dust in gold-ochre; cold blue-grey shadow filling the near "
        "foreground of the road between the viewer and the men, and the shadowed face of the "
        "village wall, cinematic atmospheric haze, dramatic volumetric light rays, "
        "photographic tonality."
    ),
    background_detail="",
    title="WHERE ARE THE NINE",
    subtitle="LUKE 17",
    title_position="top",
    animation=(
        "the loose ends of the men's rent garments and lip-cloths stir faintly in the road's "
        "wind; the low sun behind the hills stays exactly as warm and low as it already is, "
        "unchanged for the whole clip; the cold shadow across the foreground road stays "
        "exactly as cold and dim as it already is; the ten men stand exactly as drawn, none "
        "stepping forward, none raising a hand; the village houses stay exactly as drawn; no "
        "new figure, mark, or text appears"
    ),
    extra_avoid=(
        "bells, rattles, begging bowls, bandaged faces, medieval hoods, sores, blood, gore, "
        "grotesque deformity, any figure touching another, modern clothing, any single figure "
        "more prominent, more finely dressed, or differently posed than the rest of the line, "
        "any figure without a cloth bound over his mouth"
    ),
    refs=[R_TEN, R_VILLAGE],
    clip_duration=4,
)

BACK_COVER = CoverSpec(
    side="back",
    # REDESIGNED 2026-09-04 ("The One Who Came Back") -- the original close-up
    # feet-and-pressed-face-in-dust concept was rejected outright by the user
    # ("wrong concept entirely"), not just a defect in its execution. This is a
    # full replacement, designed by a separate Fable pass, matching the front
    # cover's own composition logic: small figures held in the lower third of
    # the frame against the landscape, not a macro close-up.
    scene=(
        "the village edge at dawn, small figures held in the lower third of the frame against "
        "the landscape, seen at a clear middle distance -- not a close-up; at the left, "
        f"{JESUS_BUILD}, standing on foot at the wall's end, still and square, his hands empty "
        "at his sides, touching no one, touching nothing; a hand's width before his sandals, "
        f"{SAMARITAN_BUILD}, already fallen and held in a single prostration -- his forehead "
        "and both open hands already down in the dust, not shown mid-fall or collapsing, his "
        "mantle with its thin clay-red hem-trim fallen across his back, fully clothed, drawn "
        "with the same dignity as every man in this episode; no face visible in the dust, no "
        "impression or pressed mark left in the ground -- only the man himself, whole and "
        "clothed, prostrate; behind Jesus at the left, the corner of the village's dry-stone "
        f"wall, the bare terebinth tree, and the low field-stone houses ({VILLAGE_EDGE_BUILD}); "
        "the dry road runs away to the right and up over a low rise into open stony hill "
        "country, EMPTY -- no other figure anywhere on it."
    ),
    lighting=(
        "Warm dawn gold from the village side at the left, low across both figures -- Jesus's "
        "robe, the fallen man's back, the dust between them; cold blue-grey night still "
        "holding the far empty road, the rise, and the hills behind, cinematic atmospheric "
        "haze, photographic tonality."
    ),
    background_detail="",
    title="AT HIS FEET, NOT ON THE ROAD",
    subtitle="EPHESIANS 2:8",
    title_position="bottom",
    animation=(
        "for the ENTIRE clip, from the very first frame to the very last frame, the fallen man "
        "stays exactly and completely as drawn in the still image: his forehead touching the "
        "ground, both his open hands flat on the ground, his knees bent beneath him, his whole "
        "body low and prostrate -- across the whole clip his body height, his pose, and the "
        "angle of his back and head never change by even a small amount; he does NOT lift his "
        "head, he does NOT rise onto his hands or knees, he does NOT sit up, he does NOT stand, "
        "he does NOT straighten his back even partially -- his silhouette in the very last frame "
        "of the clip must be pixel-for-pixel the same low prostrate silhouette as the first "
        "frame; only the loose frayed edge of his mantle may stir faintly in the road wind, "
        "nothing else about his body moves at all; Jesus likewise stays exactly as drawn, still "
        "and square on his feet, his hands empty at his sides -- he does NOT reach down, kneel, "
        "bend, or move toward the fallen man at any point; fine dust drifts slowly along the "
        "empty far road; the warm light across both figures stays exactly as warm and low as it "
        "already is, unchanged; the far road stays exactly as cold and dim as it already is; no "
        "new figure, mark, or text appears"
    ),
    extra_avoid=(
        "any figure on the road, Jesus's hand touching or reaching toward the fallen man, "
        "healing light, glow, or radiance of any kind, the man shown mid-fall or collapsing "
        "rather than already still and down, a face or any impression visible pressed into the "
        "dust, sores, blood, gore, jewelry, bright neon, water of any kind"
    ),
    refs=[R_JESUS, R_SAMARITAN, R_SAMARITAN_FACE, R_VILLAGE, R_ROAD],
    clip_duration=6,
)

COVERS = {"front": FRONT_COVER, "back": BACK_COVER}

# ---- assembly manifest ---------------------------------------------------
# Word weights are Fable's own count against the locked narration (sum 202,
# matching narration.md; 80.61s locked audio, natural speed, no time-stretch).
# Final modes are an assembly-QC call on the real renders, per the standing rule.

MANIFEST = EpisodeManifest(
    episode_dir=HERE,
    narration=HERE / "narration.mp3",
    units=[
        Unit("front", HERE / "front_cover.mp4", 8, "freeze"),
        Unit("f01", HERE / f"{HERE.name}_f01_9x16.mp4", 20, "freeze"),
        Unit("f02", HERE / f"{HERE.name}_f02_9x16.mp4", 18, "freeze"),
        Unit("f03", HERE / f"{HERE.name}_f03_9x16.mp4", 17, "freeze"),
        Unit("f04", HERE / f"{HERE.name}_f04_9x16.mp4", 12, "freeze"),
        Unit("f05", HERE / f"{HERE.name}_f05_9x16.mp4", 13, "freeze"),
        Unit("f06", HERE / f"{HERE.name}_f06_9x16.mp4", 17, "freeze"),
        Unit("f07", HERE / f"{HERE.name}_f07_9x16.mp4", 22, "freeze"),
        Unit("f08", HERE / f"{HERE.name}_f08_9x16.mp4", 14, "freeze"),
        Unit("f09", HERE / f"{HERE.name}_f09_9x16.mp4", 19, "freeze"),
        Unit("f10", HERE / f"{HERE.name}_f10_9x16.mp4", 23, "freeze"),
        Unit("back", HERE / "back_cover.mp4", 19, "freeze"),
    ],
    scores={
        "piano": ScoreVariant(
            score=HERE / "score_piano.mp3",
            duck=DuckProfile(gain_db=-6, threshold=0.12, ratio=2.5, release_ms=250),
            out=HERE / f"{HERE.name}_final_piano.mp4",
        ),
    },
    panel_style="woodcut_hybrid",
)
