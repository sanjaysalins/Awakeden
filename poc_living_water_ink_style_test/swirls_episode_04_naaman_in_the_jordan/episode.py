"""Episode spec for "Naaman in the Jordan" (2 Kings 5 + Luke 4:27) -- episode 4
in the locked series slate. Stain (ceremonial uncleanness) motif only, no Fray;
swirl capped Stage 1-2 throughout per the OT-episode rule.

Design authored by Fable across 3 rounds this session (full brief kept in
session history + `_DESIGN_BRIEF_REVIEW.html`): the narration's own cold-open
hook (Jesus citing this story to his hometown, Luke 4:28-29) is answered by
putting the FRONT COVER in Nazareth (not Naaman's world) so picture matches
the hook's own audio -- the first cover in this series to lead with the NT
scene. The back cover swings to Naaman at the river, mirroring episode 1's
GENESIS 28 / JOHN 1:51 old-then-new cover split, just with the poles reversed
(front=NT image+OT subtitle, back=OT image+NT subtitle) because THIS episode's
narration opens on the NT scene instead of closing on it.

Ref-chain order (hard, enforced by render_still's missing-ref stop): F01
(Naaman's first appearance, refs=[]) must render and be approved before
F02-F05 can run; F02 (chariot + door's first appearance) must be approved
before F03/F04 need them; F05 (the Jordan's first appearance) must be
approved before the back cover can run. Jesus needs no such cycle --
refs/jesus_ref.png is copied verbatim from episode 1's own approved crop
(itself copied from episode 8) -- no new design, no new approval.

Two-layer uncleanness (Fable's flag, kept deliberate, not silently folded
into one): literal pale dry skin patches on Naaman's forearm (the fact the
text names) PLUS the paper-Stain proper (the ceremonial-barrier motif, with
its own dose rules). The patches vanish entirely at F05 ("new skin, like a
child's"); the paper-Stain clears in the hard cut between F04 and F05, never
within a clip -- the cut is the miracle.
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
from swirls_assemble import EpisodeManifest, Unit  # noqa: E402

REFS_DIR = HERE / "refs"

# ---- character continuity builds -------------------------------------------

# LOCKED series-wide, reused verbatim from episode 1 (itself reused from
# episode 8) -- no amendment, no new approval cycle. jesus_ref.png is copied
# from episode 1's own approved crop.
JESUS_BUILD = (
    "Jesus, a Judean man in his early thirties, medium height and ordinary build, sun-browned "
    "skin, shoulder-length dark brown hair pushed back from his face, a short full dark beard, "
    "wearing a simple ankle-length robe of undyed cream-brown wool with a plain olive-toned "
    "mantle draped over one shoulder, a narrow rope belt, and flat worn leather sandals -- no "
    "halo, no glow, nothing in his dress distinguishing him from the men around him, standing "
    "square, still, and unhurried, his gaze steady and direct"
)

# Naaman's SKIN STATE is deliberately NOT in this build -- it changes mid-episode
# (leprous F01-F04, healed F05 onward), so it is authored per-page in main_scene_still.
NAAMAN_BUILD = (
    "Naaman, a Syrian commander in his late forties, tall and heavily built with a soldier's "
    "squared, commanding bearing, weathered olive-bronze skin, a broad face with a strong jaw "
    "and a short dark beard streaked with iron grey, dark deep-set appraising eyes under a "
    "heavy brow, black hair cropped close beneath a plain dark head-cloth bound with a narrow "
    "matte bronze band, wearing an ankle-length tunic of deep clay-red under a scaled "
    "bronze-and-leather cuirass, a heavy olive-green mantle pinned at the right shoulder with a "
    "large round matte bronze clasp, plain leather wrist-guards, and hard-worn soldier's sandals"
)

# Leprosy prose, reused verbatim on F01-F04 (never over his face, never a wound):
NAAMAN_PATCHES = (
    "a scatter of faint pale dry patches on his bared right forearm and the back of that hand "
    "-- matte, dry, unbroken skin, like frost settled on skin, never raw, never a wound, never "
    "over his face"
)
# The explicit override, required on F05 onward (his full-figure ref carries the patches):
NAAMAN_HEALED = (
    "his skin wholly clean and unmarked, the pale dry patches gone entirely, no trace anywhere"
)

R_JESUS = Ref("Jesus -- his face, build, and dress", str(REFS_DIR / "jesus_ref.png"))
R_NAAMAN = Ref("Naaman -- his face, build, and dress", str(REFS_DIR / "naaman_ref.png"))
R_NAAMAN_FACE = Ref("Naaman -- his face and eyes, for close crops", str(REFS_DIR / "naaman_face_ref.png"))
R_CHARIOT = Ref("Naaman's gilded war chariot and its two horses -- their exact form and markings",
                str(REFS_DIR / "chariot_ref.png"))
R_DOOR = Ref("Elisha's shut wooden door -- its exact form", str(REFS_DIR / "door_ref.png"))
R_JORDAN = Ref("the Jordan gorge -- its exact bank, reeds, and gorge silhouette",
               str(REFS_DIR / "jordan_ref.png"))

# ===========================================================================
# F01 -- "A great general -- and a leper"  (narration: "Naaman: a great
# general -- and a leper. A servant girl pointed him to a prophet.")
# First appearance of Naaman. NO refs yet -- crop after approval.
# ===========================================================================
F01 = PageSpec(
    seq_title="ONE OLD STORY",
    frame_label="F01",
    panels=(
        Panel("his rank",
              "Naaman's plumed bronze helmet and folded scarlet cloak set on a wooden stand, trophies of a commander"),
        Panel("a little maid",
              "a young Israelite servant girl, ten or eleven, small and neat in a plain undyed servant's tunic and "
              "a simple head-scarf, bare feet, her face open and certain, one small hand lifted mid-word, pointing away"),
        Panel("the prophet's land",
              "far hill country of Samaria, small on a heat-hazed horizon"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        f"a quiet corner of a Damascus courtyard at early light. {NAAMAN_BUILD}, fully inside the frame, "
        f"stands alone, his right sleeve drawn back, regarding {NAAMAN_PATCHES}, fully inside the frame; his "
        "commander's dress immaculate around the one thing his rank cannot fix; his face set, private, unbowed. "
        "A cold grey-umber stain lies in the paper itself beneath the linework, its feathered damp edge crossing "
        "the drawn frame border into the page's own lower margin on the side nearest his bared forearm, never "
        "over any face, a band of clean paper between it and everything else unusual on the page. Stage 0 "
        "dosage: no blue Swirls of Life ink motif anywhere on this page -- no blue ink appears anywhere in the "
        "scene, the panels, or the margins."
    ),
    material_closer=(
        "the cold stain lying in the paper is the only unusual ink at work on this page."
    ),
    panel_motions=(
        "the plumed helmet and folded cloak sit undisturbed, catching the early light",
        "her lifted hand holds its point, unmoving",
        "a faint heat-shimmer plays over the distant hill country",
    ),
    main_scene_animation=(
        "Naaman stands still, his thumb pressing once slowly against the patched forearm and stopping, not "
        "moving further; his sleeve stirs faintly; the cold stain in the paper stays exactly as drawn, never "
        "deepening, never spreading, never fading;"
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain in the paper and the pale dry patches on his forearm",
    caption_lines=("a great general", "and a leper"),
    corner_note="NOTE: rank cannot cure",
    refs=[],
    model_tier="kling3_0",
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F02 -- "The shut door"  (narration: "Elisha didn't even come out. He sent
# one line: wash in the Jordan, seven times.")
# First appearance of the chariot + door. Needs R_NAAMAN/R_NAAMAN_FACE.
# ===========================================================================
F02 = PageSpec(
    seq_title="ONE OLD STORY",
    frame_label="F02",
    panels=(
        Panel("the shut door", "a plain wooden door, closed, its heavy latch dropped"),
        Panel("the river country",
              "a low far valley, the Jordan a thin reed-lined thread winding through it, small and unimpressive"),
        Panel("seven times", "seven small smooth river stones laid in a row on bare dirt"),
    ),
    still_shot_type="WIDE shot",
    anim_shot_desc="wide shot",
    main_scene_still=(
        "Naaman's gilded war chariot and its two horses halted, grand and out of scale, before a small plain "
        "mud-brick house with its door shut, fully inside the frame. Elisha's messenger, a plain middle-aged "
        "Israelite servant in a simple undyed tunic and worn sandals, bare-headed, calm and entirely unafraid "
        "before the great commander, fully inside the frame, standing on the doorstep, one arm extended level "
        "and steady, pointing away toward the river country beyond the frame's edge. "
        f"{NAAMAN_BUILD}, fully inside the frame, standing down from the chariot facing him, towering, "
        f"affronted stillness, {NAAMAN_PATCHES}. No one else on the page -- Elisha never appears. A cold "
        "grey-umber stain lies in the paper itself between Naaman and the shut door's own threshold, its "
        "feathered damp edge crossing the drawn frame border into the page's own margin, never over any face. "
        "Stage 1 dosage: exactly one restrained brushstroke of blue ink lying flat against the shut door's own "
        "drawn seam, along the gap where door meets frame, no thickness, no drift, the only blue on the whole "
        "page, behaving like one stroke of wet ink bled flat into the paper, a clean band of paper between it "
        "and the stain."
    ),
    material_closer=(
        "the paper-stain between them and the single flat brushstroke on the door's own seam are the only two "
        "kinds of unusual ink at work on this page, kept apart by a clean band of paper."
    ),
    panel_motions=(
        "the shut door's latch sits undisturbed, casting a fixed shadow",
        "a thin haze drifts faintly over the winding river thread",
        "the seven stones sit undisturbed in their row",
    ),
    main_scene_animation=(
        "one horse shifts its weight and stills, its tail swishing once, not moving further; the messenger's "
        "pointing arm stays exactly as drawn, already extended, not moving further, his lips staying exactly as "
        "drawn, not speaking; Naaman stands motionless, one slow breath; the paper-stain and the blue "
        "brushstroke on the door's seam both stay exactly as drawn, never deepening, never spreading, never "
        "fading;"
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain in the paper between Naaman and the door, and the pale dry patches on his forearm",
    caption_lines=("wash in the Jordan", "seven times"),
    corner_note="NOTE: he never came out",
    refs=[R_NAAMAN, R_NAAMAN_FACE],
    model_tier="veo3_1_lite",
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F03 -- "The fury"  (KJV 2 Kings 5:12: "Are not Abana and Pharpar, rivers of
# Damascus, better than all the waters of Israel? may I not wash in them,
# and be clean?")
# Stain PEAK. Needs R_CHARIOT/R_DOOR.
# ===========================================================================
F03 = PageSpec(
    seq_title="ONE OLD STORY",
    frame_label="F03",
    panels=(
        Panel("Abana", "a broad royal river sweeping beneath great city walls"),
        Panel("Pharpar", "a second strong clear river through green orchards"),
        Panel("turned away", "a chariot wheel and churned dust, close"),
    ),
    still_shot_type="WIDE PROFILE shot",
    anim_shot_desc="wide profile shot",
    main_scene_still=(
        f"{NAAMAN_BUILD}, fully inside the frame, storming in full profile from left to right, "
        f"mid-stride, his cloak flaring behind him, his face legible and set in rage, {NAAMAN_PATCHES}; the "
        "small plain house with its shut door behind him at the lower left, fully inside the frame; his "
        "waiting chariot ahead of him at the right edge, fully inside the frame; nothing on the line between; "
        "dry ochre ground, no water drawn anywhere in the main scene. The cold grey-umber stain, saturated and "
        "spread, bounded to no more than a third of the page and never over any face, crosses the drawn frame "
        "border into the page's own margin along the direction he is storming. Stage 1 dosage, held: the same "
        "single flat blue brushstroke on the shut door's own seam, now small with distance, behind him, the "
        "only blue on the whole page, a clean band of paper between it and the stain."
    ),
    material_closer=(
        "the saturated stain crossing the margin and the single small brushstroke fading behind him are the "
        "only two kinds of unusual ink at work on this page."
    ),
    panel_motions=(
        "the royal river sweeps on, undisturbed",
        "the second river runs on through the still orchards",
        "the churned dust drifts low and settles",
    ),
    main_scene_animation=(
        "Naaman strides the remaining distance and arrives beside the chariot, gripping its rail, completing "
        "his stride and holding still, his lips staying exactly as drawn, not speaking; dust drifts low behind "
        "him, not rising further; the saturated stain and the small brushstroke on the distant door both stay "
        "exactly as drawn, never deepening, never spreading, never fading;"
    ),
    fence_kind="stain",
    fence_callout="the saturated grey-umber stain crossing the margin and the pale dry patches on his forearm",
    caption_lines=("Abana and Pharpar,", "rivers of Damascus"),
    corner_note="NOTE: too plain for him",
    refs=[R_NAAMAN, R_NAAMAN_FACE, R_CHARIOT, R_DOOR],
    model_tier="kling3_0",
    clip_duration=9,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F04 -- "The servants"  (KJV 2 Kings 5:13: "My father, if the prophet had
# bid thee do some great thing, wouldest thou not have done it? how much
# rather then, when he saith to thee, Wash, and be clean?")
# The pivot. Stain begins turning.
# ===========================================================================
F04 = PageSpec(
    seq_title="ONE OLD STORY",
    frame_label="F04",
    panels=(
        Panel("some great thing", "a tiny armored figure ascending a jagged storm-lit peak"),
        Panel("wash", "plain shallow water moving over ordinary stones, near-abstract, humble"),
        Panel("the way down", "the road descending ahead toward the river valley"),
    ),
    still_shot_type="MEDIUM TWO-SHOT",
    anim_shot_desc="medium two-shot",
    main_scene_still=(
        "the road south, Naaman's chariot halted at the frame edge. Naaman's eldest servant, a grey-bearded "
        "weathered man in a simple undyed wool tunic with a rope belt, fully inside the frame, standing close "
        "before Naaman, his open empty hands lifted palms-up in appeal; two younger servants in plain olive "
        "and muted-brown dress, bare-headed, hands empty, standing behind him, their bearing respectful but "
        f"unafraid, fully inside the frame. {NAAMAN_BUILD} -- his hair, beard, and head-cloth matching "
        "reference image 1 and image 2 EXACTLY: the same grey-streaked dark hair fully covered by the dark "
        "head-cloth bound with its narrow matte bronze band, never bare brown hair, never a plain circlet "
        "alone, and the same short dark beard streaked with iron grey, never a solid dark-brown beard -- "
        f"fully inside the frame, half-turned away "
        f"from them, his head just beginning to bow, {NAAMAN_PATCHES}. A cold grey-umber stain lies in the "
        "paper, still crossing the drawn frame border into the margin, but its edge on the side toward the "
        "descending road has already dried to a pale ring -- turning, not yet cleared. Stage 1 dosage: exactly "
        "one restrained thread of blue ink rising thin from the road's far bend where it drops toward the "
        "river valley, small with the distance, touching only the road's own horizon line, the only blue on "
        "the whole page, a clean band of paper between it and the stain."
    ),
    material_closer=(
        "the turning stain and the single distant thread at the road's bend are the only two kinds of unusual "
        "ink at work on this page."
    ),
    panel_motions=(
        "the small armored figure holds its climb, unmoving on the storm-lit peak",
        "the shallow water moves steadily over the stones",
        "the road holds still, descending toward the valley",
    ),
    main_scene_animation=(
        "Naaman's shoulders drop and his head completes its bow, finishing early and holding still; the eldest "
        "servant's open hands stay exactly as drawn, already lifted, not moving further, his lips staying "
        "exactly as drawn, not speaking; the servants' robes stir faintly; the turning stain and the distant "
        "blue thread both stay exactly as drawn, never deepening, never spreading, never fading;"
    ),
    fence_kind="stain",
    fence_callout="the turning grey-umber stain in the paper and the pale dry patches on Naaman's forearm",
    caption_lines=("Wash, and be clean",),
    corner_note="NOTE: a servant again",
    refs=[R_NAAMAN, R_NAAMAN_FACE, R_CHARIOT],
    model_tier="kling3_0",
    clip_duration=9,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F05 -- "The seventh wash"  (narration: "He went down. He washed, seven
# times. New skin, like a child's.")
# THE GOSPEL TURN. Stain hard-cuts to D1; Swirl crosses to Stage 2 -- the
# crossing point lands exactly on the healing. First appearance of the
# Jordan. LAW 3: zero blue in the water, verbatim requirement.
# ===========================================================================
F05 = PageSpec(
    seq_title="ONE OLD STORY",
    frame_label="F05",
    panels=(
        Panel("the seventh", "seven small ripple-rings sketched in a row, the last drawn largest"),
        Panel("what he left", "the heaped bronze cuirass, plumed helmet, and folded scarlet cloak on the bank stones"),
        Panel("downstream", "the river winding on toward a soft bright horizon"),
    ),
    still_shot_type="MEDIUM WIDE shot",
    anim_shot_desc="medium wide shot",
    main_scene_still=(
        f"{NAAMAN_BUILD}, fully inside the frame, standing waist-deep in the Jordan between low "
        "reed-lined banks, risen from the seventh plunge, water streaming off him, wearing a plain undyed "
        "linen under-tunic, soaked and clinging; both his bared forearms held up before his own eyes, fully "
        f"inside the frame, {NAAMAN_HEALED}; his face open in wonder. On the bank, small, the heap of his "
        "bronze cuirass, plumed helmet, and folded scarlet cloak, fully inside the frame. The river is "
        "painted only in grey-green and umber ink wash -- no blue anywhere in the water. Only a dried pale "
        "ring remains of the stain, sitting in the paper's own lower margin where the stain used to cross the "
        "border, the paper inside that ring the cleanest cream on the whole page. Stage 2 dosage: a few soft "
        "blue threads and one small watercolor bloom drift high in the sky above the gorge, in one loose open "
        "band, tied to no figure, touching nothing below the skyline, the ground and the river entirely free "
        "of blue."
    ),
    material_closer=(
        "the dried pale ring in the margin and the soft blue-and-gold band drifting high above the gorge are "
        "the only two kinds of unusual mark on this page, the river itself carrying neither."
    ),
    panel_motions=(
        "the seven ripple-rings hold their spread, unmoving",
        "the heaped armor sits undisturbed, catching the light",
        "the river winds on toward the bright horizon, unmoving",
    ),
    main_scene_animation=(
        "water drips from Naaman's raised forearms; gentle ripple-rings spread around his waist and fade, not "
        "repeating; the reeds sway faintly; the sky band drifts smoothly within its own fixed band, never "
        "lowering toward the water; the armor heap sits still; the dried pale ring and the clean margin stay "
        "exactly as drawn, no new stain, spot, or darkening appearing anywhere on the page at any point;"
    ),
    fence_kind="stain",
    fence_callout="the dried pale ring in the paper's margin",
    caption_lines=("new skin", "like a child's"),
    corner_note="NOTE: the seventh time",
    refs=[R_NAAMAN, R_NAAMAN_FACE],
    model_tier="veo3_1_lite",
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F06 -- "Nazareth, the telling"  (KJV Luke 4:27: "Many lepers were in
# Israel in the time of Eliseus the prophet; and none of them was cleansed,
# saving Naaman the Syrian.")
# Jesus's first appearance in this episode -- series ref, no approval cycle.
# Swirl peak (Stage 2, the slate's own cap). No Stain -- this is not an
# uncleanness page.
# ===========================================================================
F06 = PageSpec(
    seq_title="ONE OLD STORY",
    frame_label="F06",
    panels=(
        Panel("his hometown", "Nazareth's low flat rooftops stacked on the hillside"),
        Panel("the brow", "the empty cliff edge outside town, wind-scoured, no one on it"),
        Panel("many lepers",
              "a scattering of far small figures standing apart from a walled town across open ground, dignified, distant"),
    ),
    still_shot_type="MEDIUM WIDE shot",
    anim_shot_desc="medium wide shot",
    main_scene_still=(
        f"the plain stone synagogue interior. {JESUS_BUILD}, fully inside the frame, standing at the "
        "reading desk, one hand resting beside the closed scroll on the desk, fully inside the frame, square, "
        "still, unhurried, his gaze steady and level. Around and before him, the men of Nazareth risen to "
        "their feet, drawn as one pressing collective mass -- townsmen in plain undyed and ochre wool, drawn "
        "with repeated dense hatching as a single surging shape, faces turned toward Jesus or half-lost in "
        "shadow, no single face individuated or finished anywhere in the mass, their anger carried entirely "
        "in posture, press, and tightened fists, never in any one legible face, fully inside the frame. Stage "
        "2 dosage, held at this episode's own cap: the blue ink motif quietly present -- a few soft blue "
        "threads with the faintest trace of muted gold, and one small watercolor bloom, rising from the "
        "closed scroll on the reading desk beside his hand, touching only the scroll and the air above the "
        "desk, touching no person on the page."
    ),
    material_closer=(
        "the blue-and-gold threads on the scroll are the only living ink on the page."
    ),
    panel_motions=(
        "the rooftops of the hillside town sit undisturbed",
        "the empty cliff edge holds still, wind-scoured",
        "the far distant figures stand undisturbed, dignified",
    ),
    main_scene_animation=(
        "the crowd mass leans slowly in as one body without advancing, not rising further; every man in the "
        "crowd keeps his lips exactly as drawn, not speaking, not shouting, never opening; no speech bubble, "
        "dialogue balloon, or any bubble-shaped mark of any kind ever appears near any figure at any point; "
        "Jesus stays exactly as drawn, one slow steady breath, his lips staying exactly as drawn, not "
        "speaking; the threads and bloom on the scroll drift gently within their own small area, never "
        "spreading beyond the scroll and the air above it, never fading; no new figure, bubble, or mark "
        "appears anywhere on the page at any point;"
    ),
    fence_kind="none",
    caption_lines=("saving Naaman the Syrian",),
    corner_note="NOTE: his own hometown",
    refs=[R_JESUS],
    model_tier="veo3_1_lite",
    clip_duration=8,
    panel_style="woodcut_hybrid",
)

PAGES = {"f01": F01, "f02": F02, "f03": F03, "f04": F04, "f05": F05, "f06": F06}

# ---- covers -------------------------------------------------------------

FRONT_COVER = CoverSpec(
    side="front",
    scene=(
        f"{JESUS_BUILD}, standing isolated in the lower third at the very brow of a high rocky cliff "
        "outside a hillside town, square, still, and unhurried, facing out; behind and above him on the "
        "slope, the men of Nazareth as one dark surging mass -- townsmen in plain undyed and ochre wool, "
        "no single face individuated, but every single man in the mass, all the way back to the ones nearest "
        "the town, drawn as a solid whole figure with a clear head, shoulders, and body, never thinning into "
        "bare parallel hatch lines or a texture pattern, the same solid density of drawn men from the nearest "
        "rank to the farthest -- pressing downhill toward him but drawn frozen mid-press; the low flat "
        "rooftops of Nazareth small on the hill's shoulder; a long drop of wind-scoured crags falling away "
        "below the brow."
    ),
    lighting=(
        "Late golden-afternoon light breaking low and warm across the cliff brow and the standing figure, "
        "against a heavy cold slate-blue storm shelf massing above the town, deep teal shadow holding the "
        "pressing crowd, cinematic atmospheric haze, dramatic volumetric light rays, photographic tonality."
    ),
    background_detail=(
        "One small hard-capped curl of blue ink floats in the open air beside Jesus's shoulder, its whole "
        "visible length no longer than a hand's width, curled into one small closed loop, never straightening, "
        "never trailing, behaving like a small dab of living ink, never a glow."
    ),
    title="ONE OLD STORY",
    subtitle="2 KINGS 5",
    title_position="top",
    animation=(
        "the crowd mass sways and leans very slightly as one body without advancing; Jesus stays exactly as "
        "drawn, his mantle's hem stirring faintly in the wind; the blue curl stays exactly as drawn, never "
        "spreading; the afternoon light stays exactly as warm and low as it already is, unchanged"
    ),
    extra_avoid="visible wounds, blood, gore, falling figures",
    refs=[R_JESUS],
    clip_duration=4,
)

BACK_COVER = CoverSpec(
    side="back",
    scene=(
        f"the Jordan gorge wide at dawn; {NAAMAN_BUILD}, {NAAMAN_HEALED}, small and isolated in the "
        "lower third, standing mid-river in his plain soaked undyed linen under-tunic, facing the breaking "
        "light, arms loose at his sides; in the near foreground on the bank stones, the abandoned heap of his "
        "splendor -- bronze cuirass, plumed helmet, folded scarlet cloak -- larger in frame than the man "
        "himself."
    ),
    lighting=(
        "Dawn gold breaking low along the gorge rim and catching the water's far edge warm, against cold "
        "grey-green river shadow and blue-grey rock holding the near bank, cinematic atmospheric haze, "
        "photographic tonality. The lowest strip of the frame is a wide flat sunlit sandbank, bare warm-lit "
        "stone catching the same dawn gold as the gorge rim above -- open, uncluttered ground with nothing "
        "drawn on it, wide enough across the full frame to carve the title straight into that lit stone "
        "itself, the letters made of the same rock and light as the bank around them."
    ),
    title="STILL WORTH LOSING",
    subtitle="LUKE 4:27",
    title_position="bottom",
    animation=(
        "the water glimmers and drifts steadily past him; his wet tunic clings and stirs faintly; the armor "
        "heap stays exactly as drawn; the dawn light stays exactly as warm and low as it already is, unchanged"
    ),
    extra_avoid="visible wounds, blood, gore",
    refs=[R_NAAMAN, R_JORDAN],
    clip_duration=8,
)

COVERS = {"front": FRONT_COVER, "back": BACK_COVER}

# ---- assembly manifest ---------------------------------------------------
# Word weights are approximate narration-share per unit (word-proportional
# slot timing, not exact sync) -- Fable's own estimates against the locked
# narration, sum ~194 vs the narration's real 188 words.
# Modes: freeze+tail_loop for pages with a real completing gesture (F01's
# thumb-press, F03's arrival-at-chariot, F04's head-bow, F06's crowd lean);
# boomerang for pages that are genuinely all-holds/ambient (front, F02, F05,
# back) -- matches this series' own established distinction.

MANIFEST = EpisodeManifest(
    episode_dir=HERE,
    narration=HERE / "narration.mp3",
    units=[
        Unit("front", HERE / "front_cover.mp4", 21, "boomerang"),
        Unit("f01", HERE / f"{HERE.name}_f01_9x16.mp4", 16, "freeze", tail_loop_seconds=1.0),
        Unit("f02", HERE / f"{HERE.name}_f02_9x16.mp4", 15, "boomerang"),
        Unit("f03", HERE / f"{HERE.name}_f03_9x16.mp4", 28, "freeze", tail_loop_seconds=1.5),
        Unit("f04", HERE / f"{HERE.name}_f04_9x16.mp4", 37, "freeze", tail_loop_seconds=1.8),
        Unit("f05", HERE / f"{HERE.name}_f05_9x16.mp4", 12, "boomerang"),
        Unit("f06", HERE / f"{HERE.name}_f06_9x16.mp4", 35, "boomerang"),
        Unit("back", HERE / "back_cover.mp4", 30, "boomerang"),
    ],
    scores={},  # added once a score is generated, before running `assemble`
    panel_style="woodcut_hybrid",
)
