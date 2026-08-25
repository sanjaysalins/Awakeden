"""Episode spec for "The Queen Who Came to Test Him" (1 Kings 10:1-13 +
Matthew 12:42) -- the first episode to introduce the queen of Sheba and
Solomon in this style, and the first to REUSE an already-approved character
(Jesus, from episode 8) instead of designing him fresh.

Design authored by Fable (2026-08-25, full design brief kept in session
history): 7 interior pages (one more than episode 8's 6-page anchor -- the
queen's and Jesus' own long KJV quotes each needed a full page to breathe
rather than being crowded onto one), a rising Swirls-of-Life arc that
crosses into Stage 3 exactly on F06 ("a greater than Solomon is here"), and
a Fray arc on the queen that resolves early (F03, "mine eyes had seen it")
-- three pages and centuries before the swirl's own crossing point. That
gap between her doubt dying and the truth's own rise finishing is the
episode's whole argument, drawn as ink.

Ref-chain order (hard, enforced by render_still's missing-ref stop):
F01 (queen + camel + ridge first appearance, refs=[]) must render and be
approved before front/f02/f03/f04/f05/f07 can run; F02 (Solomon + throne
first appearance) must render and be approved before F03 can run. Jesus
needs no such cycle -- refs/jesus_ref.png is copied verbatim from episode
8's own approved crop.
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

# ---- character continuity builds (Fable-authored) -- inlined verbatim into
# each page's main_scene_still the first time that character is named on the
# page; refs (once cropped) carry the real likeness-matching work, this text
# is backup only, per swirls_page.py's own Ref docstring.

QUEEN_BUILD = (
    "the queen of Sheba, a South Arabian queen in her late thirties, tall and straight-backed with a "
    "poised, deliberate bearing, deep bronze-brown skin, strong high cheekbones and dark level "
    "appraising eyes, black hair in many fine braids gathered back beneath a sheer ochre head-veil "
    "edged with small matte gold discs, a narrow matte gold circlet across her brow, small heavy gold "
    "earrings, wearing layered ankle-length robes of ochre and deep clay-red with an olive-green "
    "fringed sash at the waist and flat leather traveling sandals, her hands bare and empty"
)
SOLOMON_BUILD = (
    "Solomon, the king of Israel in his early fifties, medium-tall and settled in build, olive-brown "
    "skin, a full dark beard streaked with grey, dark hair to the nape beneath a narrow matte gold "
    "diadem, no tall crown, wearing an ankle-length robe of fine cream linen with a deep clay-red "
    "mantle across both shoulders and a heavy matte gold signet ring on his right hand, his expression "
    "attentive and unsurprised"
)
# Reused verbatim from episode 8 -- no amendment. jesus_ref.png is copied from that
# episode's own approved crop; no first-appearance approval cycle needed here.
JESUS_BUILD = (
    "Jesus, a Judean man in his early thirties, medium height and ordinary build, sun-browned "
    "skin, shoulder-length dark brown hair pushed back from his face, a short full dark beard, "
    "wearing a simple ankle-length robe of undyed cream-brown wool with a plain olive-toned "
    "mantle draped over one shoulder, a narrow rope belt, and flat worn leather sandals -- no "
    "halo, no glow, nothing in his dress distinguishing him from the men around him, standing "
    "square, still, and unhurried, his gaze steady and direct"
)

R_QUEEN = Ref("the queen of Sheba -- her face, build, and dress", str(REFS_DIR / "queen_ref.png"))
R_QUEEN_FACE = Ref("the queen of Sheba -- her face and eyes, for close crops", str(REFS_DIR / "queen_face_ref.png"))
R_SOLOMON = Ref("Solomon -- his face, build, and dress", str(REFS_DIR / "solomon_ref.png"))
R_THRONE = Ref("Solomon's throne -- its exact form and gilding", str(REFS_DIR / "throne_ref.png"))
R_CAMEL = Ref("the lead camel -- its exact markings and saddle", str(REFS_DIR / "camel_ref.png"))
R_RIDGE = Ref("the desert ridge and horizon -- its exact silhouette and the far city notch", str(REFS_DIR / "ridge_ref.png"))
R_JESUS = Ref("Jesus -- his face, build, and dress", str(REFS_DIR / "jesus_ref.png"))

# ===========================================================================
# F01 -- "To See For Herself"  (narration: "She had heard about Solomon's
# wisdom and did not believe it... to see for herself.")
# First appearance of the queen, the camel, and the ridge. NO refs yet --
# crop after approval. Fray FR2: her doubt at its peak.
# ===========================================================================
F01 = PageSpec(
    seq_title="TO TEST HIM",
    frame_label="F01",
    panels=(
        Panel("her level gaze",
              "a tight close crop of the queen's eyes just above her veil edge, brow set, skeptical"),
        Panel("the cargo",
              "an open cedar chest packed with matte gold ingots, bound spice bundles, and uncut stones"),
        Panel("the far city",
              "a distant walled city rendered as a small pale silhouette alone on a heat-hazed horizon line"),
    ),
    still_shot_type="WIDE shot",
    anim_shot_desc="wide shot",
    main_scene_still=(
        f"a high desert ridge crest at early light. {QUEEN_BUILD}, fully inside the frame, stands at "
        "the crest beside her kneeling lead camel, also fully inside the frame, looking out over a "
        "vast sea of dunes toward a pale far horizon; a small pale notch of a distant walled city sits "
        "on that horizon, fully inside the frame. Fray FR2 -- her figure alone is drawn in a "
        "DIFFERENT, rougher medium than the rest of the page: loose, unfinished pencil-sketch "
        "crosshatching, the kind an artist uses for a rapid uncertain first study, not the clean "
        "inked linework everywhere else on the page. Visible construction lines and scribbly repeated "
        "pencil strokes build up her silhouette and every fold of her robe, graphite-grey and soft-edged, "
        "never fully committing to one clean outline -- in visible contrast to the confident solid "
        "black ink used for the camel, the caravan, and the rest of the page. Her face itself stays "
        "legible and finished; only her outer silhouette and robe are rendered this rough, sketchy way. "
        "Kept apart from the horizon by the whole width of the dune-sea. Behind and "
        "below her the halted caravan winds back down the slope -- three laden camels visible, the "
        "rest suggested in dust-haze, none of them walking. Stage 1 dosage: exactly one restrained "
        "thread of blue ink rising from the far horizon notch where the pale city sits, the only blue "
        "on the whole page, behaving like a single line of wet ink bled into the paper. All gold on "
        "this page is matte object-gold, part of the scene, separate from the blue ink motif; no gold "
        "wash traces in the air or on the ground."
    ),
    material_closer=(
        "the queen's broken, restless contour and the single blue thread on the far horizon are the "
        "only two kinds of unusual ink at work on this page, kept apart by the whole width of the "
        "dune-sea between them."
    ),
    panel_motions=(
        "her eyes hold their level, skeptical look, unblinking",
        "a thin haze drifts faintly over the gold and spice bundles",
        "a faint heat-shimmer plays over the distant city silhouette",
    ),
    main_scene_animation=(
        "the queen and her camel hold completely still at the ridge crest; her veil's trailing edge "
        "and the camel's saddle-fringe stir faintly in the wind; the caravan below sits motionless in "
        "the haze; the blue thread on the horizon stays exactly as drawn, never fading;"
    ),
    fence_kind="fray",
    fence_callout="the queen's own broken, tremored outer contour and restless robe hatching",
    caption_lines=("to see for herself",),   # narration verbatim contiguous
    corner_note="NOTE: she doubted",
    refs=[],
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F02 -- "A True Report"  (narration: "She said it plainly:" / KJV "It was a
# true report... of thy acts and of thy wisdom.")
# First appearance of Solomon + the throne. Queen's 2nd appearance -- needs
# R_QUEEN. Fray FR1: her doubt already loosening.
# ===========================================================================
F02 = PageSpec(
    seq_title="TO TEST HIM",
    frame_label="F02",
    panels=(
        Panel("hard questions",
              "the queen's raised hand alone, two fingers marking a point mid-question"),
        Panel("nothing hid",
              "a close study of Solomon's listening face, calm and unsurprised"),
        Panel("gold and spices",
              "the gifts laid out at the foot of the throne steps: gold, bound spice bundles, and uncut stones"),
    ),
    still_shot_type="MEDIUM WIDE shot",
    anim_shot_desc="medium wide shot",
    main_scene_still=(
        f"Solomon's throne hall. {SOLOMON_BUILD}, fully inside the frame, sits elevated at frame right "
        "on a broad flight of stone steps with small carved stone lions flanking them, his throne "
        f"overlaid with matte gold. At frame left, a stride back from the lowest step, {QUEEN_BUILD}, "
        "fully inside the frame, stands addressing him, chin lifted, one hand raised mid-speech with "
        "two fingers marking a point. Fray FR1: only her own hatching is loose and faintly overworked "
        "now, her outer contour whole and steady. Stage 1 dosage: exactly one restrained thread of "
        "blue ink curling up from the base of the lowest throne step, touching only the stone, the "
        "only blue on the page, with a clean band of floor between it and the queen's own figure. All "
        "gold on this page is matte object-gold, part of the throne and the gifts, separate from the "
        "blue ink motif; no gold wash traces in the air or on the ground."
    ),
    material_closer=(
        "the queen's loosened but still-whole hatching and the single thread at the throne's base are "
        "the only unusual ink on the page, held apart by a clean band of open floor."
    ),
    panel_motions=(
        "her raised fingers hold their count, not moving further",
        "Solomon's calm listening face holds its stillness",
        "a thin haze drifts faintly over the laid-out gold and spice",
    ),
    main_scene_animation=(
        "the queen and Solomon hold their poses, lips staying exactly as drawn, not speaking; a little "
        "dust drifts in the hall's low light; the thread at the throne's base stays exactly as drawn, "
        "never fading;"
    ),
    fence_kind="fray",
    fence_callout="the queen's own loosened, faintly overworked robe hatching, her outer contour otherwise whole",
    caption_lines=("a true report",),   # KJV 1 Kings 10:6 verbatim contiguous
    corner_note="NOTE: spoken plainly",
    refs=[R_QUEEN],
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F03 -- "The Half Was Not Told Me"  (KJV "Howbeit I believed not the
# words... the half was not told me.")
# Fray resolves HERE -- her line is the cleanest of the whole episode.
# ===========================================================================
F03 = PageSpec(
    seq_title="TO TEST HIM",
    frame_label="F03",
    panels=(
        Panel("the same eyes",
              "the identical tight crop and angle of the queen's eyes from the first page, but now "
              "wide and soft, brow lifted"),
        Panel("the ascent",
              "a glimpse of a broad stone stairway rising toward a temple facade, small distant figures on it"),
        Panel("the king's table",
              "one laden table corner: matte gold vessels, bread, and a cupbearer's hand"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        f"{QUEEN_BUILD}, fully inside the frame, stands at center, one open hand pressed flat over her "
        "own heart, the other open low at her side, chin lifted, eyes wide. Fray: none -- her line is "
        "confident and whole here, the cleanest she is drawn in the whole episode. Behind her, soft "
        f"and warm, the golden bulk of Solomon's throne with {SOLOMON_BUILD} seated on it, indistinct "
        "in the middle distance. Stage 2 dosage: a few soft threads of blue ink curl up from the "
        "polished stone floor around the hem-shadow at her feet, and one small blue watercolor bloom "
        "is soaked into the floor inside her own cast shadow, touching only the stone, never her body. "
        "All gold in the background is matte object-gold, part of the throne, separate from the blue "
        "ink motif; no gold wash traces in the air."
    ),
    material_closer=(
        "the queen's line is the steadiest and most confident of the whole episode here, so the soft "
        "threads and the small bloom at her feet are the only unusual ink at work on the page."
    ),
    panel_motions=(
        "her wide, soft eyes hold their look, unblinking",
        "the small distant figures on the stairway hold their places",
        "the cupbearer's hand holds still over the laden table",
    ),
    main_scene_animation=(
        "the queen holds her pose, one hand pressed to her heart, lips staying exactly as drawn, not "
        "speaking, her veil stirring faintly in a breeze; Solomon sits still on his throne behind her; "
        "a little dust drifts in the hall's low light; the soft threads and the bloom at her feet stay "
        "exactly as drawn, never fading;"
    ),
    fence_kind="none",
    caption_lines=("the half was not", "told me"),   # KJV 1 Kings 10:7 verbatim contiguous
    corner_note="NOTE: doubt falls",
    refs=[R_QUEEN, R_QUEEN_FACE, R_SOLOMON, R_THRONE],
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F04 -- "Homeward"  (narration: "She had doubted a report. Seeing it
# changed everything... to make a claim about Himself:")
# ===========================================================================
F04 = PageSpec(
    seq_title="TO TEST HIM",
    frame_label="F04",
    panels=(
        Panel("all her desire",
              "a small ivory-and-matte-gold casket, a royal gift, in close detail"),
        Panel("one look back",
              "a close crop of the queen's face turned back over her shoulder, calm and settled"),
        Panel("the fading track",
              "camel footprints in sand, the wind already half-smoothing them away"),
    ),
    still_shot_type="WIDE shot",
    anim_shot_desc="wide shot",
    main_scene_still=(
        "the same high ridge as before, now at golden evening light. The caravan is halted mid-descent "
        f"on the homeward slope, three laden camels standing. {QUEEN_BUILD}, fully inside the frame, "
        "stands at the rear of the line beside her camel, her head turned back over her shoulder for "
        "one last look toward the far pale city notch on the horizon, fully inside the frame. The "
        "caravan's own trodden track runs back up the slope behind her toward that horizon. Fray: "
        "none. Stage 2 dosage: a few soft threads of blue ink lie along the trodden track in the sand "
        "behind the caravan, and one small blue watercolor bloom is soaked into the trodden sand of "
        "the track itself, touching only the sand. All gold stays matte and object-bound to the gifts "
        "carried on the camels, separate from the blue ink motif."
    ),
    material_closer=(
        "the queen's line stays steady and whole here, so the soft threads and the small bloom lying "
        "along the trodden track are the only unusual ink on the page."
    ),
    panel_motions=(
        "the small casket sits undisturbed, catching the low light",
        "her calm, backward-turned gaze holds its look",
        "a thin skin of windblown sand drifts faintly over the footprints",
    ),
    main_scene_animation=(
        "the caravan and the queen hold completely still on the slope; a thin skin of wind-blown sand "
        "drifts across the track's surface; the threads and the bloom lying in the track stay exactly "
        "as drawn, never fading;"
    ),
    fence_kind="none",
    caption_lines=("changed everything",),   # narration verbatim contiguous
    corner_note="NOTE: homeward",
    refs=[R_QUEEN, R_CAMEL, R_RIDGE],
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F05 -- "The Queen of the South"  (KJV "The queen of the south shall rise
# up in the judgment with this generation...")
# Jesus' first appearance in this episode -- series ref, no approval cycle.
# Deliberate quick cut (~5s) at the pivot's setup.
# ===========================================================================
F05 = PageSpec(
    seq_title="TO TEST HIM",
    frame_label="F05",
    panels=(
        Panel("she came far",
              "the queen at the ridge crest from the very first page, redrawn small as a pinned-up "
              "storyboard thumbnail"),
        Panel("this generation",
              "two scribes' faces close together, brows down, mouths tight, unpersuaded"),
        Panel("he points back",
              "Jesus' extended hand alone, open palm, mid-gesture"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        f"a first-century Jerusalem courtyard, dusty open ground, plain stone walls. {JESUS_BUILD}, "
        "fully inside the frame, stands at left-center addressing a knot of two or three scribes in "
        "fringed robes at frame right, their faces half-turned and skeptical, fully inside the frame; "
        "his arm is extended, open palm gesturing back and away toward a low gap in the courtyard wall "
        "behind him, fully inside the frame, through which a far southern horizon line of open sky is "
        "visible, fully inside the frame. Fray: none. Stage 2 dosage: a few soft threads of blue ink "
        "curl in through the wall gap from the far southern horizon, and one small blue watercolor "
        "bloom is soaked into the stone sill of the gap, touching only the stone and the sky beyond."
    ),
    material_closer=(
        "every line on this page is confident and whole, so the threads curling through the wall gap "
        "and the small bloom on its sill are the only unusual ink at work here."
    ),
    panel_motions=(
        "the small pinned thumbnail of the queen stays static, a fixed piece of reference art",
        "the scribes' tight, unpersuaded expressions hold their look, their head coverings stirring faintly in a breeze",
        "Jesus' extended hand holds its open-palm gesture, dust motes drifting faintly through the light",
    ),
    main_scene_animation=(
        "Jesus stands still, arm extended, lips staying exactly as drawn, not speaking, his mantle "
        "stirring faintly in a breeze; the scribes hold their skeptical stillness, their robe hems "
        "stirring faintly in the same breeze; a thin haze drifts faintly through the wall gap behind "
        "them; the threads curling through the wall gap stay exactly as drawn, never fading;"
    ),
    fence_kind="none",
    caption_lines=("queen of the south",),   # KJV Matthew 12:42 verbatim contiguous
    corner_note="NOTE: he points back",
    refs=[R_JESUS, R_QUEEN],
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F06 -- "Greater Than Solomon"  (KJV "...for she came from the uttermost
# parts of the earth... a greater than Solomon is here.")
# THE GOSPEL PIVOT and the swirl's crossing point -- Stage 3 begins here.
# Real one-directional gesture (hand settles to chest) -- FREEZE, not
# boomerang, matching this series' established completing-gesture rule.
# ===========================================================================
F06 = PageSpec(
    seq_title="TO TEST HIM",
    frame_label="F06",
    panels=(
        Panel("no throne",
              "Jesus' worn leather sandals standing on bare dust"),
        Panel("no palace",
              "a rough plain stone doorway in the courtyard wall, empty"),
        Panel("his eyes",
              "a close crop of Jesus' eyes alone, calm and level"),
    ),
    still_shot_type="CLOSE MEDIUM shot",
    anim_shot_desc="close medium three-quarter shot",
    main_scene_still=(
        f"{JESUS_BUILD}, fully inside the frame from the waist up, stands at center in three-quarter "
        "view, his extended hand now drawn back and turned palm-inward toward his own chest, fully "
        "inside the frame -- the claim made with one plain gesture -- his gaze steady, standing on "
        "bare dust against the plain courtyard wall, nothing elevated, nothing gilded anywhere in "
        "frame. The scribes are reduced to soft, indistinct shoulders at the frame's edge. Stage 3 "
        "dosage: the blue ink motif, with traces of muted gold, is woven through the whole scene -- "
        "threads drifting through the air of the courtyard, curling along the ground shadows and the "
        "wall edges, muted gold traces running in the dust at his feet, never touching any figure's "
        "skin."
    ),
    material_closer=(
        "every line on this page is confident and whole, so the diffused blue-and-gold threads through "
        "the air, ground, and wall edges are the only unusual ink at work here."
    ),
    panel_motions=(
        "his sandalled feet hold still on the bare dust",
        "the empty stone doorway sits undisturbed",
        "his calm, level eyes hold their gaze, unblinking",
    ),
    main_scene_animation=(
        "Jesus' hand completes its settle against his own chest early in the clip, then holds still; "
        "his gaze stays level, lips staying exactly as drawn, not speaking; the woven blue-gold "
        "threads through the air and ground stay exactly as drawn, never fading;"
    ),
    fence_kind="none",
    caption_lines=("a greater than Solomon", "is here"),   # KJV Matthew 12:42 verbatim contiguous
    corner_note="NOTE: the claim",
    refs=[R_JESUS],
    clip_duration=9,
    model_tier="kling3_0",
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F07 -- "Ask Him"  (narration: "She crossed a continent to verify a king's
# wisdom. A greater than Solomon is already in front of you... Just ask Him
# your hardest question.")
# Deliberate fourth-wall break -- the only page in the episode. Heaviest
# slot -- freeze + tail_loop, matching episode 8's F05 recipe.
# ===========================================================================
F07 = PageSpec(
    seq_title="TO TEST HIM",
    frame_label="F07",
    panels=(
        Panel("no long road",
              "the same ridge from the very first page, redrawn empty -- no caravan, the track almost "
              "wind-smoothed away"),
        Panel("come near",
              "Jesus' open hand alone, palm up, relaxed"),
        Panel("ask him",
              "a single bare forearm and hand raised mid-question, fingers marking a point"),
    ),
    still_shot_type="HELD SINGLE shot",
    anim_shot_desc="held single frontal shot",
    main_scene_still=(
        f"{JESUS_BUILD}, fully inside the frame from the knees up, stands alone on plain open ground "
        "at dusk, facing the viewer squarely, his gaze meeting the viewer's straight on, both hands "
        "open low at his sides, palms turned slightly forward, fully inside the frame -- no other "
        "figure, no courtyard, no scribes anywhere in frame. Stage 3 dosage: the blue ink motif, with "
        "traces of muted gold, is woven through the whole scene -- threads drifting slow through the "
        "dusk air around him, curling along the ground shadows, one small blue-gold watercolor bloom "
        "soaked into the dust directly before his feet, at the viewer's own side of the frame, never "
        "touching his body."
    ),
    material_closer=(
        "Jesus' own line is completely confident and still here, so the slow-drifting threads and the "
        "small bloom at his feet are the only unusual ink at work on the page."
    ),
    panel_motions=(
        "the empty ridge sits undisturbed, its track almost gone",
        "his open, upturned palm holds its ease",
        "the raised hand and marking fingers hold their question, unmoving",
    ),
    main_scene_animation=(
        "Jesus stands in near-total stillness, gaze steady on the viewer, no blink language, lips "
        "staying exactly as drawn, not speaking; a faint dusk haze drifts around him; the threads and "
        "the bloom at his feet stay exactly as drawn, never fading;"
    ),
    fence_kind="none",
    caption_lines=("your hardest question",),   # narration verbatim contiguous
    corner_note="NOTE: just ask",
    refs=[R_JESUS, R_RIDGE],
    clip_duration=9,
    model_tier="kling3_0",
    panel_style="woodcut_hybrid",
)

PAGES = {"f01": F01, "f02": F02, "f03": F03, "f04": F04, "f05": F05, "f06": F06, "f07": F07}

# ---- covers ---------------------------------------------------------------

FRONT_COVER = CoverSpec(
    side="front",
    scene=(
        f"{QUEEN_BUILD}, sits prominent on her standing lead camel at right-foreground, both fully "
        "inside the frame, at the crest of a dune. Her figure alone is drawn in a DIFFERENT, rougher "
        "medium than the rest of the page: loose, unfinished pencil-sketch crosshatching, the kind an "
        "artist uses for a rapid uncertain first study, not the clean inked linework everywhere else on "
        "the page. Visible construction lines and scribbly repeated pencil strokes build up her "
        "silhouette and every fold of her robe, graphite-grey and soft-edged, never fully committing to "
        "one clean outline -- in visible contrast to the confident solid black ink used for the camel "
        "and the rest of the page. Her face itself stays legible and finished; only her outer silhouette "
        "and robe are rendered this rough, sketchy way. Past them, an empty dune-sea runs left and away "
        "toward a pale far horizon; a small pale notch of a distant walled city sits on that horizon."
    ),
    lighting=(
        "The dune-sea beneath them is held in cool pre-dawn blue-grey wash. Along the horizon's whole "
        "length, warm golden first light is breaking, catching the edges of the far city notch."
    ),
    background_detail=(
        "One single restrained thread of blue ink rises from the far city notch on the horizon, its "
        "whole visible length modest, touching only the horizon line -- a wide clean band of dune and "
        "paper separates it from the queen's own frayed figure."
    ),
    title="THE QUEEN WHO CAME TO TEST HIM",
    subtitle="1 KINGS 10:1-13",
    title_position="top",
    animation=(
        "the queen and her camel hold still at the dune crest; her veil and the camel's fringe stir "
        "faintly in the wind; the blue thread on the horizon and the warm light along its edge stay "
        "exactly as drawn, unchanged"
    ),
    refs=[R_QUEEN, R_CAMEL],
)

BACK_COVER = CoverSpec(
    side="back",
    scene=(
        "The same dune ridge at dusk -- the caravan gone, the track down the slope almost entirely "
        "wind-smoothed away. A far pale city notch still sits small on the horizon."
    ),
    lighting=(
        "The sky above the ridge is a deep cool evening blue with the first faint stars showing. One "
        "last low band of warm lamp-gold light lies along the horizon behind the distant city."
    ),
    background_detail=(
        "In the near foreground, at the very bottom edge of the frame, a few soft blue threads and one "
        "small blue-gold watercolor bloom are soaked into the sand, close enough that a viewer's own "
        "feet would stand right beside them."
    ),
    title="YOUR HARDEST QUESTION",
    subtitle="MATTHEW 12:42",
    title_position="bottom",
    animation=(
        "the empty ridge and the almost-vanished track hold still; a thin skin of sand drifts faintly "
        "in the evening air; the threads and the bloom at the frame's own edge stay exactly as drawn, "
        "unchanged"
    ),
    refs=[R_RIDGE],
)

COVERS = {"front": FRONT_COVER, "back": BACK_COVER}

# ---- assembly manifest -----------------------------------------------------
# Word weights are pacing shares from the Fable brief, tracking each unit's real
# narration-beat weight (F07's closing double-line is the heaviest page; F05's
# quick pivot-setup cut is the lightest) -- sum 180 matches narration.md's own
# count (SW-L5 word-count-parity gate, WARN-only).
MANIFEST = EpisodeManifest(
    episode_dir=HERE,
    narration=HERE / "narration.mp3",
    # RETUNED (user, 2026-08-25): "a couple of scenes where the camels are working
    # backwards" -- boomerang (play forward then reverse) only reads clean on a clip
    # that settles into stillness; these units have real continuous ambient motion
    # (wind on veil/fringe, drifting dust/haze -- added to fix the earlier "zero
    # motion" bug), so extending them via boomerang visibly played that motion in
    # reverse. Switched to freeze (hold the native clip's own last frame for the
    # rest of the slot, $0, no re-render) -- same fix class as f06/f07 below,
    # applied here for the same underlying reason (per project_swirls_boomerang_
    # continuous_motion_unsafe: a clip with no completing gesture reverses badly).
    # RETUNED again (user, 2026-08-25): "you are just doing a freeze, which [I]
    # hate ... figure out a better way to show motion." Fable picked one $0
    # devised fill per page (see _devise_fills.py, adapted from the John-4
    # piece's own build_fills.py precedent) instead of a plain held last-frame.
    # Round 2 (user watched the real cut, gave timestamped notes): f02's
    # parallax_25d read "shaky" and f04's Lamplight still read as a freeze --
    # f02/f03 have no camels (ambient-only motion), so simplified to a plain
    # boomerang of the native clip per the user's own call; f04 DOES have
    # camels (the original backward-motion bug), so boomerang was never safe
    # there -- swapped Lamplight for the same Halo Tour device that clearly
    # worked on F01 instead, targeting the small blue-gold bloom in the sand.
    # Final devices: f01 Halo Tour (horizon thread), f02/f03 boomerang,
    # f04 Halo Tour (sand bloom). f01/f04's Halo Tour clips land within ~0.1s
    # of their own slot (harmless under freeze). f02/f03's full-clip boomerang
    # (10.08s) genuinely exceeds its 8.31s slot by ~1.8s -- confirmed "freeze"
    # mode does NOT trim an over-long native clip (only pads a short one), so
    # those two need "boomerang" mode specifically, which does trim to slot
    # when native already exceeds it (no second reversal added on top, since
    # that path only triggers when native < slot).
    units=[
        Unit("front", HERE / "front_cover.mp4", 12, "freeze"),
        Unit("f01", HERE / f"{HERE.name}_f01_9x16_devised.mp4", 22, "freeze"),
        Unit("f02", HERE / f"{HERE.name}_f02_9x16_devised.mp4", 23, "boomerang"),
        Unit("f03", HERE / f"{HERE.name}_f03_9x16_devised.mp4", 23, "boomerang"),
        Unit("f04", HERE / f"{HERE.name}_f04_9x16_devised.mp4", 23, "freeze"),
        Unit("f05", HERE / f"{HERE.name}_f05_9x16.mp4", 14, "freeze"),
        # freeze: Jesus' hand-settle-to-chest is a real one-directional completing
        # gesture (per this series' established rule -- see episode 8's F05).
        Unit("f06", HERE / f"{HERE.name}_f06_9x16.mp4", 24, "freeze"),
        # freeze + tail_loop: heaviest slot: near-total stillness has no completing
        # gesture to hold on, so ping-pong the settled tail instead of a dead freeze
        # (user's own validated fix, see feedback_freeze_tail_loop_technique).
        Unit("f07", HERE / f"{HERE.name}_f07_9x16.mp4", 33, "freeze", tail_loop_seconds=2.0),
        Unit("back", HERE / "back_cover.mp4", 6, "boomerang"),
    ],
    scores={
        "original": ScoreVariant(
            score=HERE / "score_final.mp3",
            # RETUNED (user, 2026-08-25): "score is great, just make it a bit softer" --
            # measured mix was already reasonably ducked (mix mean during narration was
            # QUIETER than narration alone -- real duck engagement, not the ep8-style
            # zero-movement bug), so this is a plain baseline-level pull-down, not a
            # duck-shape fix. gain_db -6 -> -9.
            duck=DuckProfile(gain_db=-9, threshold=0.12, ratio=2.5, release_ms=250),
            out=HERE / "THE_QUEEN_WHO_CAME_TO_TEST_HIM_final.mp4",
        ),
    },
    # RETUNED (user, 2026-08-25): "at the end of narration linger a few seconds, it
    # feels too abrupt". 3.0 -> 5.0 -- still >= the INV-26 floor, just longer. The
    # score's own artificial fade-out (generate_score.py) shifts later to match --
    # re-trimmed from the SAME already-generated raw file (its own volume profile is
    # flat straight through 60-70.6s, no natural decay to protect), no new ElevenLabs
    # spend needed.
    outro_hold=5.0,
    panel_style="woodcut_hybrid",
)
