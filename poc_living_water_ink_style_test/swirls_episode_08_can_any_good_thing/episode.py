"""Episode spec for "Can Any Good Thing" (John 1:45-51) -- the first episode
built through this series' Fray (fear/doubt) dead-ink motif and the first to
put Jesus himself on-page in this style. Both are genuinely new: NORTH_STAR_
PROMPT.md's own DEAD INK section says "The Fray motif is still undemonstrated
(no still or clip test yet)" as of the last update, and no jesus_ref.png
exists anywhere in this series (Jacob's Ladder / Episode 1 is an OT dream
scene that never puts Jesus on-page).

Design authored by Fable (2026-08-23, full design brief + response kept in
session history): 6 interior pages, a hard Fray dissolve at the F03->F04
page-turn (Nathanael's doubt is FR2 on F03, gone -- FR0 -- on F04, matching
the series' own text: "Dissolves the instant Jesus names something He
couldn't have seen"), and a Jacob's Ladder callback on F06 that visually
rhymes with Episode 1's own ladder page.

Content here is authored fresh, not sliced from an existing render_*.py --
there is no prior script for this episode. Refs are chained progressively,
matching the established Jacob's Ladder / Ashes workflow: a character's ref
is cropped from their OWN FIRST APPROVED render, then chained into every
later page -- so refs/nathanael_ref.png, refs/philip_ref.png, and
refs/jesus_ref.png do NOT exist yet at the time this file is written. F01
(no refs needed, first appearance of Nathanael + Philip) must render and be
approved before F02 can run; F03 (first appearance of Jesus) must render and
be approved before F04/F05/F06 can run. render_still()'s own hard-stop on a
missing ref path enforces this ordering -- it is not a bug if `still f02`
fails before `still f01` has been approved and cropped.
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

JESUS_BUILD = (
    "Jesus, a Judean man in his early thirties, medium height and ordinary build, sun-browned "
    "skin, shoulder-length dark brown hair pushed back from his face, a short full dark beard, "
    "wearing a simple ankle-length robe of undyed cream-brown wool with a plain olive-toned "
    "mantle draped over one shoulder, a narrow rope belt, and flat worn leather sandals -- no "
    "halo, no glow, nothing in his dress distinguishing him from the men around him, standing "
    "square, still, and unhurried, his gaze steady and direct"
)
NATHANAEL_BUILD = (
    "Nathanael, a broad-shouldered Judean man around thirty, sturdy build, big workman's hands, "
    "square jaw, heavy expressive brow, thick black hair cropped short, a short dense dark "
    "beard, wearing an ochre-yellow wool robe with a clay-red sash at the waist and plain "
    "leather sandals"
)
PHILIP_BUILD = (
    "Philip, a lean, eager Judean man in his late twenties, narrow face, thin dark beard, dark "
    "hair shorter than Jesus', wearing a muted brown robe with an olive-green mantle and "
    "carrying a plain wooden walking staff, its wood pale and hand-smoothed"
)

R_NATHANAEL = Ref("Nathanael -- his face, build, and dress", str(REFS_DIR / "nathanael_ref.png"))
R_PHILIP = Ref("Philip -- his face, build, and dress", str(REFS_DIR / "philip_ref.png"))
R_JESUS = Ref("Jesus -- his face, build, and dress", str(REFS_DIR / "jesus_ref.png"))

# ===========================================================================
# F01 -- "The News"  (narration: "A man insulted Jesus... Nathanael's answer:")
# First appearance of Nathanael + Philip. NO refs yet -- crop after approval.
# Fray FR1: the first stirring, Nathanael's contour still whole.
# ===========================================================================
F01 = PageSpec(
    seq_title="CAN ANY GOOD THING",
    frame_label="F01",
    panels=(
        Panel("Philip's news",
              "a tight close-up of Philip's face mid-sentence, eyes wide with urgent joy, teeth just visible"),
        Panel("Nazareth itself",
              "the village of Nazareth seen from a distance, a small huddle of flat-roofed mud-brick houses "
              "on an unremarkable brown hillside, deliberately drawn ordinary and forgettable"),
        Panel("ripening figs",
              "a close study of ripening figs on a leafy branch, one fig split open"),
    ),
    still_shot_type="WIDE shot",
    anim_shot_desc="wide shot",
    main_scene_still=(
        "the dusty edge of a small Galilean village in early morning light, long shadows raking across the "
        "ground. A broad old fig tree with a thick gnarled trunk and heavy canopy fills the right third of "
        f"the frame, fully inside the frame; {NATHANAEL_BUILD} sits cross-legged in its deep shade, fully "
        "inside the frame, one hand resting on his knee, his head just turning toward the road. Fray dose "
        "FR1: Nathanael's own drawn outer contour and robe hatching are kept loose and faintly overworked, "
        "a first restless stirring in the line — his outer edge is otherwise still whole and continuous, "
        "not yet broken or gapped anywhere. Along a pale "
        f"dirt road entering from the left, {PHILIP_BUILD} arrives at a half-run, fully inside the frame, his "
        "robe hem lifted, his free arm flung back toward the road behind him. Stage 1 dosage: exactly one "
        "restrained thread of blue ink wound loosely along the length of Philip's wooden staff, from "
        "mid-shaft to tip, touching only the wood, never his hand or skin, the only blue on the whole page, "
        "behaving like a single line of wet ink bled into the paper."
    ),
    material_closer=(
        "the loose, scratchy hatching of Nathanael's own robe and outer line and the single blue thread "
        "wound along Philip's staff are the only two kinds of ink at work on this page, kept apart by a "
        "clean band of untouched paper between the fig tree's shade and the road."
    ),
    panel_motions=(
        "Philip's eyes hold their wide, urgent look, lips still",
        "a thin haze drifts faintly over the distant rooftops",
        "the fig leaves stir faintly in a breeze",
    ),
    main_scene_animation=(
        "Philip completes his last stride and comes to a stop at the tree's edge, robe hem settling, early "
        "in the clip, then holds; Nathanael sits still in the shade, head turned toward him; fig leaves sway "
        "gently overhead; the blue thread on Philip's staff stays exactly as drawn, never fading;"
    ),
    fence_kind="fray",
    fence_callout="the loose, faintly overworked hatching of Nathanael's robe and outer contour",
    caption_lines=("the Messiah — Jesus, of Nazareth",),   # narration.md verbatim contiguous
    corner_note="NOTE: news arrives",
    refs=[],
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F02 -- "The Sneer"  (narration: quote + "Philip did not argue -- he invited.
# Jesus spoke first:")
# Fray PEAK: FR3, real gaps in Nathanael's own contour.
# ===========================================================================
F02 = PageSpec(
    seq_title="CAN ANY GOOD THING",
    frame_label="F02",
    panels=(
        Panel("the sneer",
              "an extreme close-up of Nathanael's mouth and brow mid-sneer, upper lip lifted, brow crushed down"),
        Panel("the open hand",
              "Philip's open hand alone, palm up, fingers relaxed, drawn large"),
        Panel("the road ahead",
              "the empty dirt road curving away between low stone walls toward a hazy horizon"),
    ),
    still_shot_type="MEDIUM TWO-SHOT",
    anim_shot_desc="medium two-shot",
    main_scene_still=(
        "a medium two-shot, camera slightly low, the fig tree's lower branches framing the top of the frame "
        f"like a proscenium. {NATHANAEL_BUILD} has risen to one knee, fully inside the frame, torso twisted "
        "toward Philip, one arm thrown out in a flat dismissive backhand gesture, brow knotted, lip curled "
        "mid-scorn. Fray dose FR3, the peak dose of the whole page: Nathanael's own drawn outer contour is "
        "broken, with real visible gaps along his shoulder and his outflung arm where the ink line simply "
        "stops and restarts, doubled and tremored strokes stacked two and three deep along his back, his "
        "robe's own hatching scratchy and violently overworked — the least settled, most broken linework "
        "anywhere in the whole episode. "
        f"Facing him, {PHILIP_BUILD}, fully inside the frame, stands relaxed, weight back, one open "
        "hand extended palm-up toward the road running out of frame behind him, no tension anywhere in his "
        "body. Stage 1 dosage: exactly one restrained thread of blue ink lying along the near edge of the "
        "dirt road at lower frame-right, running off-frame in the direction of Philip's open palm, touching "
        "only the road-earth, the only blue on the whole page, behaving like a single line of wet ink bled "
        "into the paper."
    ),
    material_closer=(
        "Nathanael's broken, doubled, and tremored linework and the single blue thread lying along the "
        "road's edge are the only two kinds of ink at work on this page, separated by a wide clean band of "
        "untouched paper between his figure and the road."
    ),
    panel_motions=(
        "Nathanael's sneer holds, no further change",
        "Philip's open hand holds its palm-up position",
        "a light haze drifts faintly along the road",
    ),
    main_scene_animation=(
        "Nathanael and Philip hold their poses, robes stirring faintly in a passing breeze; fig branches "
        "sway gently overhead; the blue thread along the road's edge stays exactly as drawn, never fading;"
    ),
    fence_kind="fray",
    fence_callout=(
        "Nathanael's own outer contour, visibly incomplete with real gaps along his shoulder and outflung "
        "arm, doubled and tremored strokes stacked along his back"
    ),
    caption_lines=("any good thing",),   # KJV John 1:46 verbatim contiguous
    corner_note="NOTE: the sneer",
    refs=[R_NATHANAEL, R_PHILIP],
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F03 -- "Seen Before Spoken"  (narration: "Behold an Israelite indeed..." /
# "Whence knowest thou me?")
# First appearance of Jesus -- NO jesus_ref yet, crop after approval.
# LAST PAGE WITH VISIBLE FRAY: FR2, rattled but not yet gone.
# ===========================================================================
F03 = PageSpec(
    seq_title="CAN ANY GOOD THING",
    frame_label="F03",
    panels=(
        Panel("already knowing",
              "a close crop of Jesus' eyes only, calm, level, no glow"),
        Panel("still he came",
              "Nathanael's sandaled feet mid-step in the road dust, dense shadow under the arch, dust kicked up"),
        Panel("not yet named",
              "the fig tree seen small and far behind on the road they walked, its canopy a dark mass with a lit crown"),
    ),
    still_shot_type="WIDE-MEDIUM shot",
    anim_shot_desc="wide-medium shot",
    main_scene_still=(
        "open trampled ground just outside the village, afternoon light. At frame right, "
        f"{JESUS_BUILD}, fully inside the frame, facing left, one hand slightly lifted in calm greeting, "
        "two or three indistinct disciple figures loose behind him, their faces unclear. At frame left, "
        f"{NATHANAEL_BUILD}, fully inside the frame, enters mid-stride, caught off-balance, his head pulled "
        "back in astonishment, one foot still lifted. Fray dose FR2: Nathanael's own drawn outer contour is "
        "no longer gapped but still doubled and tremored along his arms and shoulders, his robe hatching "
        "restless and unsettled, rattled but not yet steadied. The ground between the two men is mostly bare and "
        "empty, one low stone visible. Stage 2 dosage: a few soft threads of blue ink curling up from the "
        "trampled ground at Jesus' feet, and one small blue-gold watercolor bloom soaked into the earth "
        "beside his sandal, touching only the ground, never his body, the only blue on the whole page, every "
        "thread behaving like wet ink bled into the paper."
    ),
    material_closer=(
        "Nathanael's broken, tremored linework on the left half of the page and the blue threads and bloom "
        "rising from the ground at Jesus' feet on the right half are the only two kinds of ink at work here, "
        "kept apart by an unbroken vertical band of clean paper between the two halves."
    ),
    panel_motions=(
        "Jesus' gaze holds steady, no blink",
        "the dust around Nathanael's feet settles",
        "the distant fig tree sits still",
    ),
    main_scene_animation=(
        "Jesus holds his greeting completely still, no motion anywhere in his robe or mantle; Nathanael holds "
        "his off-balance step, robe hem swaying; the disciples behind Jesus stay still; the blue threads and "
        "small bloom at his feet stay exactly as drawn, never fading;"
    ),
    fence_kind="fray",
    fence_callout=(
        "the broken, tremored contour along Nathanael's arms and shoulders, no longer gapped but still "
        "doubled and unsettled"
    ),
    caption_lines=("in whom is no guile",),   # KJV John 1:47 verbatim contiguous
    corner_note="NOTE: seen already",
    refs=[R_NATHANAEL],
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F04 -- "A Moment Only Heaven Had Seen"  (narration: the fig-tree line +
# "A moment only heaven had seen -- named. The doubt did not fade. It fell.")
# FIRST PAGE WITHOUT FRAY -- the hinge turns here, hard jump from F03's FR2.
# ===========================================================================
F04 = PageSpec(
    seq_title="CAN ANY GOOD THING",
    frame_label="F04",
    panels=(
        Panel("unseen prayer",
              "Nathanael's clasped hands alone, knuckles pressed together in prayer"),
        Panel("from beneath",
              "fig leaves overhead against the sky, sun coming through them in small coins of light"),
        Panel("present time",
              "a close-up of Jesus' calm face mid-sentence, unhurried, no glow"),
    ),
    still_shot_type="HIGH OVERHEAD shot",
    anim_shot_desc="high overhead shot",
    main_scene_still=(
        "heaven's own memory of an earlier moment: a high overhead view, looking nearly straight down "
        "through a parted gap in a fig tree's canopy. Far below, small in the frame, "
        f"{NATHANAEL_BUILD} sits alone at the base of the trunk, fully inside the frame, head bowed over his "
        "own clasped hands in private prayer, the tree's shadow a soft dark ring around him, the land beyond "
        "the shadow empty in every direction -- no road, no other figure, no witness anywhere. Stage 2 "
        "dosage: soft threads of blue ink tracing along the outer edge of the fig canopy's shadow-ring, and "
        "one small blue-gold watercolor bloom at the very top of the frame, at the point in the sky the view "
        "descends from, touching only the ground at the shadow's edge and the open sky above, never "
        "Nathanael's body, the only blue on the whole page, every thread behaving like wet ink bled into the "
        "paper."
    ),
    material_closer=(
        "Nathanael's own line is completely confident and settled here -- the cleanest he has been drawn in "
        "the whole episode -- so the blue threads at the canopy's edge and the bloom at the top of the frame "
        "are the only ink of any kind doing anything unusual on this page."
    ),
    panel_motions=(
        "Nathanael's clasped hands stay still",
        "sunlight coins through the leaves shift slowly",
        "Jesus' lips hold mid-sentence stillness",
    ),
    main_scene_animation=(
        "Nathanael sits still at the tree's base, head bowed, only his breath moving his shoulders; the "
        "shadow-ring holds its shape; the blue threads at the canopy's edge and the small bloom above stay "
        "exactly as drawn, never fading;"
    ),
    fence_kind="none",
    caption_lines=("under the fig tree",),   # KJV John 1:48 verbatim contiguous
    corner_note="NOTE: it fell",
    refs=[R_NATHANAEL, R_JESUS],
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F05 -- "The Confession"  (narration: "Rabbi, thou art the Son of God..." /
# "Thou shalt see greater things than these...")
# A real one-directional gesture (Jesus' hand beginning to rise) -- FREEZE,
# not boomerang, matching this series' established completing-gesture rule.
# ===========================================================================
F05 = PageSpec(
    seq_title="CAN ANY GOOD THING",
    frame_label="F05",
    panels=(
        Panel("the same face, changed",
              "Nathanael's face in the same tight crop as F02's sneer panel, same angle, but the brow lifted "
              "and the mouth open in wonder"),
        Panel("Philip watching",
              "Philip half-turned in the middle distance, caught mid-breaking-smile"),
        Panel("greater things",
              "Jesus' hand alone, rising, palm opening toward the upper frame edge"),
    ),
    still_shot_type="MEDIUM OVER-SHOULDER shot",
    anim_shot_desc="medium over-the-shoulder shot",
    main_scene_still=(
        f"a medium shot framed over {PHILIP_BUILD}'s near shoulder, soft-focus in the lower-left foreground, "
        f"fully inside the frame. At center, {NATHANAEL_BUILD}, fully inside the frame, drops to one knee "
        f"before Jesus, both hands pressed flat against his own chest, face lifted, brow open, every line of "
        f"him settled and whole. {JESUS_BUILD}, fully inside the frame, receives it simply, standing as "
        "plainly as ever, his free hand just beginning to rise, palm turning upward toward the sky. Late "
        "golden light, long warm shadows toward the viewer. Stage 3 dosage: the blue ink motif, with traces "
        "of muted gold, is woven through the whole scene -- threads drifting loose through the air of the "
        "composition, curling along the ground shadows and the hem-lines of the robes, with muted gold "
        "traces running in the dust and along the stone edges, staying in the air, the ground, and the "
        "cloth's own hem, never touching any figure's skin."
    ),
    material_closer=(
        "every line on this page -- Nathanael's, Philip's, and Jesus' -- is confident and whole, so the "
        "diffused blue-and-gold threads through the air, ground, and hems are the only unusual ink at work "
        "here."
    ),
    panel_motions=(
        "Nathanael's lifted face holds its wonder",
        "Philip's breaking smile holds its shape",
        "Jesus' hand rises a little further, then settles palm-up, holding",
    ),
    main_scene_animation=(
        "Jesus' free hand completes its rise early in the clip, palm turning fully upward, then holds still "
        "for the rest of the clip; Nathanael holds his kneeling pose, hands at his chest; Philip holds his "
        "half-turned stance in the foreground; the diffused blue-gold threads through the air and ground "
        "stay exactly as drawn, never fading;"
    ),
    fence_kind="none",
    caption_lines=("the Son of God",),   # KJV John 1:49 verbatim contiguous
    corner_note="NOTE: confession",
    refs=[R_NATHANAEL, R_JESUS, R_PHILIP],
    model_tier="kling3_0",
    clip_duration=9,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F06 -- "The Ladder, Standing Open"  (narration: "...heaven open, and the
# angels of God ascending and descending..." / "That is Jacob's ladder...")
# The Jacob's-Ladder echo. Angels CONTINUE a cyclical climb -- no completing
# gesture -- so this stays boomerang-safe, matching Episode 1's own F03.
# ===========================================================================
F06 = PageSpec(
    seq_title="CAN ANY GOOD THING",
    frame_label="F06",
    panels=(
        Panel("the first ladder",
              "Episode 1's own ladder redrawn small as a pinned-up storyboard thumbnail: a tall ladder of "
              "plain weathered wood, two straight rails and flat rungs, rising into a night sky, tiny robed "
              "angels on it"),
        Panel("descending",
              "a single descending angel in close detail, a small robed figure caught mid-step downward, "
              "face indistinct"),
        Panel("your fig tree",
              "a fig tree on a quiet hillside seen from slightly above, its shade empty except for one flat "
              "unoccupied sitting-stone at the trunk"),
    ),
    still_shot_type="LOW WIDE VERTICAL shot",
    anim_shot_desc="low wide vertical shot",
    main_scene_still=(
        "a low, wide, monumental vertical composition, deliberately echoing Episode 1's own ladder page. "
        f"{JESUS_BUILD}, fully inside the frame, stands small at the bottom center of the frame on dark open "
        "ground, arms slightly open at his sides, face lifted. Above him the deep night-blue sky is parted: "
        "two long straight rifts of paler sky run parallel from high in the frame down toward him, reading "
        "unmistakably as the two rails of a ladder, and between them, at even rung-like intervals, angels of "
        "God -- small robed figures, faces indistinct, six or seven of them -- are ascending and descending, "
        "some rising, some coming down, fully inside the frame, no glow VFX, the open heaven rendered only "
        "as lighter night-blue wash between the rifts with soft gold watercolor traces along their edges, "
        "the foot of the parted column resting directly upon Jesus. Stage 3 dosage: blue ink threads and "
        "muted gold traces woven all through the parted column of sky, running the length of both rifts and "
        "threading between the angels, pooling in one small blue-gold bloom where the column's foot meets "
        "the ground at Jesus' feet, touching skin only at the point of ground contact beneath his feet, "
        "never elsewhere on his body."
    ),
    material_closer=(
        "the blue-gold threads woven through the parted sky and pooling at Jesus' feet are the only ink of "
        "any kind on this page -- the steadiest, most confident linework of the whole episode, no Fray "
        "anywhere."
    ),
    panel_motions=(
        "the pinned ladder thumbnail stays static, a fixed piece of reference art",
        "the descending angel continues its slow step downward",
        "the fig tree and stone sit still, leaves stirring faintly",
    ),
    main_scene_animation=(
        "Jesus stands completely still, arms slightly open, no motion anywhere in his robe or mantle; the "
        "angels continue their drawn "
        "climb along the parted sky, at most half a rung over the whole clip, none ever leaving the column "
        "or reaching the ground; the blue-gold threads through the sky and the bloom at his feet stay "
        "exactly as drawn, never fading;"
    ),
    fence_kind="none",
    caption_lines=("ascending and descending",),   # KJV John 1:51 verbatim contiguous
    corner_note="NOTE: standing open",
    refs=[R_JESUS],
    panel_style="woodcut_hybrid",
)

PAGES = {"f01": F01, "f02": F02, "f03": F03, "f04": F04, "f05": F05, "f06": F06}

# ---- covers ---------------------------------------------------------------

FRONT_COVER = CoverSpec(
    side="front",
    scene=(
        f"{NATHANAEL_BUILD} sits alone beneath a great fig tree, which anchors the right half of the frame, "
        "his figure drawn with a broken, tremored contour and restless, overworked hatching -- the episode's "
        "question made visible before a word is spoken. Past the tree, an empty dirt road runs left and away "
        "toward the horizon."
    ),
    lighting=(
        "The fig tree's shade is held in cool pre-dawn blue-grey wash. Along the road's whole length, warm "
        "golden first light is breaking over the horizon -- the news arriving before anyone is on the road "
        "to carry it."
    ),
    background_detail=(
        "One single restrained thread of blue ink lies along the sunlit road's edge in the far distance, "
        "pointing toward the horizon, its whole visible length no longer than the width of the road itself, "
        "touching only the road-earth -- a wide clean band of shade and paper separates it from Nathanael's "
        "frayed figure under the tree."
    ),
    title="CAN ANY GOOD THING",
    subtitle="JOHN 1 -- EPISODE 8",
    title_position="top",
    animation=(
        "Nathanael sits still beneath the tree; the leaves sway gently in a breeze; the blue thread on the "
        "road's edge and the warm light along the horizon stay exactly as drawn, unchanged"
    ),
    refs=[R_NATHANAEL],
)

BACK_COVER = CoverSpec(
    side="back",
    scene=(
        "The same fig tree at dusk -- the shade beneath it now stands empty, Nathanael having gone to "
        "follow. A flat, unoccupied sitting-stone rests at the trunk's base."
    ),
    lighting=(
        "The sky above the tree is a deep cool evening blue with the first faint stars showing. One last "
        "low band of warm lamp-gold sunlight lies across the trunk and across the top of the empty "
        "sitting-stone."
    ),
    background_detail=(
        "High in the blue, thin and quiet, a narrow vertical seam of paler sky stands open above the "
        "horizon -- not closing, rendered purely as lighter wash, no glow. A few soft blue threads curl "
        "around the base of the empty sitting-stone with one small blue-gold watercolor bloom soaked into "
        "the stone's warm-lit top surface, touching only the stone."
    ),
    title="COME AND SEE",
    subtitle="JOHN 1:46",
    title_position="bottom",
    animation=(
        "The empty stone and tree stay still; leaves stir faintly in the evening air; the blue threads on "
        "the stone and the open seam of sky stay exactly as drawn, unchanged"
    ),
    refs=[],
)

COVERS = {"front": FRONT_COVER, "back": BACK_COVER}

# ---- assembly manifest -----------------------------------------------------
# Word weights are pacing shares (slot = narration_len * words / total_words),
# not a literal re-count of each unit's own on-screen text -- see swirls_
# verify.sw_l5_word_count_parity's own docstring ("WARN-only... a naive split
# does NOT match this project's own hand-counted totals exactly"). Chosen so
# the 6 interior pages' relative shares track their real narration-beat
# weight (F05's long double-quote is the heaviest page; F02/F03's quick
# back-and-forth are the lightest) while the grand total across all 8 units
# lands close to narration.md's own ~164-word count, mirroring how Episode
# 2's front(21)+back(23)+interior(113)=157 landed within SW-L5's tolerance
# of its own narration.md count (163).
MANIFEST = EpisodeManifest(
    episode_dir=HERE,
    narration=HERE / "narration.mp3",
    units=[
        Unit("front", HERE / "front_cover.mp4", 20, "boomerang"),
        Unit("f01", HERE / f"{HERE.name}_f01_9x16.mp4", 19, "boomerang"),
        Unit("f02", HERE / f"{HERE.name}_f02_9x16.mp4", 13, "boomerang"),
        Unit("f03", HERE / f"{HERE.name}_f03_9x16.mp4", 11, "boomerang"),
        Unit("f04", HERE / f"{HERE.name}_f04_9x16.mp4", 25, "boomerang"),
        # freeze: Jesus' hand-rise is a real one-directional completing gesture (per this
        # series' established rule -- see episode 2's F04). clip_duration=9 keeps SW-F1's
        # static_ratio under the 35% FAIL line at this page's word-weighted slot; tail_loop
        # pings-pongs the settled hand-raised tail for the remainder instead of a dead freeze
        # (user's own validated fix, see feedback_freeze_tail_loop_technique).
        Unit("f05", HERE / f"{HERE.name}_f05_9x16.mp4", 33, "freeze", tail_loop_seconds=2.0),
        Unit("f06", HERE / f"{HERE.name}_f06_9x16.mp4", 23, "boomerang"),
        Unit("back", HERE / "back_cover.mp4", 20, "boomerang"),
    ],
    scores={
        "original": ScoreVariant(
            score=HERE / "score_final.mp3",
            # Starting duck matched to Ashes' own FINAL (already-softened-twice) values, not
            # its original -- no reason to re-discover the same "too loud" feedback from
            # scratch on a new episode; re-tune from here if this episode's own score needs it.
            duck=DuckProfile(gain_db=-1, threshold=0.7, ratio=1.15, release_ms=500),
            out=HERE / "CAN_ANY_GOOD_THING_final.mp4",
        ),
    },
    panel_style="woodcut_hybrid",
)
