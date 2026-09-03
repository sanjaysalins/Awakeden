"""Episode spec for "She Loved Much" (Luke 7:36-50, the woman who washed Jesus's
feet with her tears in Simon the Pharisee's house). Dead ink: STAIN (moral
sin/guilt) ONLY -- locked in SWIRLS_OF_LIFE_SERIES_PLAN_V4.md -- and it is the
series' first Stain attached to a living, named-in-text person ("a woman... which
was a sinner", v37/v39), not an object. NT episode -- the OT Stage 1-2 swirl cap
does NOT apply; Stage 3 is reached once, on F09, per the fulfilment-on-page
carve-out (Jesus bodily present, declaring forgiveness in his own voice).

Design authored by Fable (full brief: `_DESIGN_BRIEF.md` in this folder),
implemented by Sonnet per the "Fable designs, Sonnet executes" rule. Four open
questions were put to the user and answered: (1) the opening three pages (F01-F03)
stay at Stage 0 -- zero blue -- as Fable designed, pending a look at the real F01
render before deciding whether to pull a thread in earlier (user: "let's see the
still first and then decide, the stain could be under the jar on the floor" --
this is a real open item, see the note at the bottom of this docstring, NOT
silently folded into the design below); (2) back-cover subtitle is 1 JOHN 4:19
("we love him, because he first loved us" -- the episode's own thesis verse);
(3) hero page is F08, the declaration ("her sins... are forgiven"), not F07 (the
seeing) -- matches the locked rule that the hero is the gospel-pivot, not the
emotional climax; (4) stills-phase spend (~$2-3 for 9 interior pages + 2 covers,
scaled off episode 7's real $1.30/8-unit cost) was approved.

THE HARD PROBLEM (full reasoning in _DESIGN_BRIEF.md section 2): the stain
belongs to the woman herself, but her tears/kiss/ointment must NOT be drawn as
what clears it -- that would repeat the exact backwards-causality error the
narration itself was revised four times to avoid ("Not thy tears. Not thy
ointment. Thy faith."). Solution: the stain lies IN THE PAPER beneath her
position (never her skin/face/garments), unmoved and fully saturated through
both tear-and-ointment pages (F02, F03) where her love is most visibly poured
out -- her tears and the ointment are real liquid, in the scene, on HIS feet, a
different substrate in a different zone, always separated from the stain by a
stated band of clean paper. The stain only begins drying on the page-turn into
F05, the first time forgiveness is SPOKEN ("he frankly forgave them both"),
dries to a ring at the declaration (F08), and is gone entirely by the sending
(F09). The cut is the miracle -- no clip ever shows the clearing itself. The
swirl rises against it (0 on F01-F03, 1 on F04-F06, 2 on F07-F08, 3 on F09),
anchored throughout to the hand Jesus speaks/gestures with (the ep7 precedent),
crossing the stain at F07 ("Seest thou this woman?" -- equality, 2+2 at cap) and
running ahead of it at F08 (the declaration, 2 > 1).

OPEN ITEM, not yet resolved -- flagged here so it is not lost: the user's own
note when approving the paper design was "let's see the still first and then
decide[,] the stain could be under the jar on the floor" for the opening pages.
That is a genuinely different placement than this file currently implements
(stain beneath HER, not beneath the alabaster flask) -- Fable's brief explicitly
rejected anchoring any dead-ink motif to the flask (doctrine risk: it would read
as blaming the gift/ointment, the same "Not thy ointment" trap in reverse). The
plan agreed with the user is to render F01 first, look at the real pixels, and
revisit the user's placement idea then -- this file implements Fable's original
(stain-on-her) design as the one to render first; do not silently change the
geometry without going back to the user once F01 is in hand.

F03 ANIMATION -- SUPERSEDED, switched to $0 Ken Burns (2026-09-03, user: "F03 --
and kissed his feet is coming off as nsfw, can we perhaps just ken burn zoom in").
The still itself was approved as reverent at GATE 2 (hair hides her face, lips at
his instep, fully clothed) -- the generative Kling clip read as NSFW once
animated, the exact risk this page's own design brief flagged it as "the most
render-fragile composition in the episode (hair on feet; reverence)." Same fix
ep7 used on its own equivalent page: drop the generative animation, replace with
a slow ffmpeg zoompan push (6% zoom over the clip's full 7.04s, matching
swirls_assemble.py's own make_freeze zoom formula) directly over the approved
still -- zero hallucination risk by construction, since no new motion is ever
generated, only a camera move over already-approved pixels. The original
generative clip is kept alongside as
`..._f03_9x16.SUPERSEDED_generative_nsfw_reading_replaced_with_kenburns.mp4` for
the record, never used in assembly. Same output dimensions (1072x1928) and exact
duration (7.041667s) as the clip it replaces, so no MANIFEST change is needed.
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

# LOCKED series-wide, reused verbatim from episode 7 (itself from ep4/ep1/ep8) --
# no amendment, no new approval cycle. jesus_ref.png copied from episode 7's own
# refs/ directory.
JESUS_BUILD = (
    "Jesus, a Judean man in his early thirties, medium height and ordinary build, sun-browned "
    "skin, shoulder-length dark brown hair pushed back from his face, a short full dark beard, "
    "wearing a simple ankle-length robe of undyed cream-brown wool with a plain olive-toned "
    "mantle draped over one shoulder, a narrow rope belt, and flat worn leather sandals -- no "
    "halo, no glow, nothing in his dress distinguishing him from the men around him, standing "
    "square, still, and unhurried, his gaze steady and direct"
)

# New to the series. Unnamed in the text -- "a woman in the city, which was a sinner".
# Chromatic reservation: no blue on her; the madder-red mantle is her likeness pin and the
# one saturated color in a room of undyed/ochre men, with Isaiah 1:18's "scarlet" sitting
# quietly underneath. Reverence guards (full modest dress, no jewelry, never a sensual pose)
# and the steady-line no-Fray override are stated on every page she appears on.
WOMAN_BUILD = (
    "the woman of the city, about thirty, olive-skinned, a narrow oval face with high "
    "cheekbones, large dark heavy-lidded eyes, strong dark brows, a straight nose and a full "
    "mouth, thick black hair bound back beneath a plain cream head-cloth, wearing an "
    "ankle-length tunic of faded ochre-cream linen under a deep madder-red woolen mantle drawn "
    "close about her shoulders and body, full and modest, no jewelry of any kind, no sandals "
    "or footwear of any kind on either foot, her bare dusty feet and toes fully visible"
)

# New to the series. A different Simon from any disciple elsewhere in this project -- the
# skeptical host, courteous and closed, not a villain: "Simon had seen the sin. Never the
# woman." His fringe is stated undyed cream (never blue) -- the tekhelet thread a real
# Pharisee's fringe would carry (Num 15:38) is sacrificed to the motif's chromatic reservation.
SIMON_BUILD = (
    "Simon the Pharisee, a man of about fifty-five, thickset and well-fed, an olive-skinned "
    "broad face with heavy lids, a long straight nose, and a full square-trimmed beard streaked "
    "iron-grey, dark hair beneath a fine cream linen head-cloth, wearing a long wide-sleeved "
    "robe of fine undyed white-cream linen, a broad cream-and-umber striped woolen mantle with "
    "long knotted fringes at its corners -- the fringes undyed cream, never blue -- and a wide "
    "embroidered sash, composed, upright even while reclining, his hands folded, his face "
    "courteous and closed"
)

# The title object. The "box" literalism trap (the Barrel's "barrel", the Bier's "bier" --
# same family): KJV "alabaster box" = an alabastron, a stone perfume flask; an image model's
# prior for "box" is a hinged jewelry casket. Every prompt states the corrected form first and
# carries the never-box/never-casket/never-chest triple. Two states between pages: sealed in
# her hands (F01, F02, front cover); open, stopper beside it, on the floor (F03 onward, back
# cover).
ALABASTER_BUILD = (
    "the alabaster box: a small palm-sized flask of pale translucent white-veined alabaster "
    "stone, a rounded body narrowing to a short neck closed with a small stone stopper -- never "
    "a square box, never a hinged casket, never a wooden chest, never any lid"
)

# The location of every interior page. First-century reclining-dinner architecture. The DRY
# BASIN is the hook's first sentence made into furniture -- it stands unused by the door on
# F01, F09, and the back cover (Simon never did give the water).
ROOM_BUILD = (
    "the dining room of Simon the Pharisee's house: a lamplit room of plastered walls washed "
    "warm by oil-lamp light, low wooden dining couches with cushions set around a low table on "
    "three sides, the fourth side open, a tall bronze lamp-stand carrying several small burning "
    "clay lamps, a doorway open to a dim courtyard; a plain clay foot-basin with a folded towel "
    "standing DRY beside the doorway, unused"
)

R_JESUS = Ref("Jesus -- his face, build, and dress", str(REFS_DIR / "jesus_ref.png"))
R_WOMAN = Ref("the woman -- her face, build, and dress", str(REFS_DIR / "woman_ref.png"))
R_WOMAN_FACE = Ref("the woman -- her face and eyes, for close crops", str(REFS_DIR / "woman_face_ref.png"))
R_SIMON = Ref("Simon the Pharisee -- his face, build, and dress", str(REFS_DIR / "simon_ref.png"))
R_SIMON_FACE = Ref("Simon the Pharisee -- his face, for close crops", str(REFS_DIR / "simon_face_ref.png"))
R_ALABASTER = Ref(
    "the alabaster box -- its exact stone flask form, sealed or open per the page",
    str(REFS_DIR / "alabaster_ref.png"),
)
R_ROOM = Ref(
    "Simon's dining room -- its exact couches, table, lamp-stand, and doorway",
    str(REFS_DIR / "room_ref.png"),
)

# Refs common to every page from F02 onward (once F01 has established them all).
_REFS_FULL = [R_JESUS, R_SIMON, R_SIMON_FACE, R_WOMAN, R_WOMAN_FACE, R_ALABASTER, R_ROOM]

# ===========================================================================
# F01 -- "at his own table"  (narration: "That's what Simon the Pharisee never
# gave Jesus at his own table. A woman he hadn't invited walked in anyway, and
# gave him all three.")
# The room's establishing shot and the Stain's debut -- the three absences as
# furniture, and the uninvited woman just inside the door. QUADRUPLE debut:
# woman, Simon, flask, and room all crop from this one approval.
# ===========================================================================
F01 = PageSpec(
    seq_title="SHE LOVED MUCH",
    frame_label="F01",
    panels=(
        Panel("no water",
              "the plain clay foot-basin and folded towel standing dry beside a doorway, unused"),
        Panel("no kiss",
              "the open doorway of a house from inside, its threshold stones empty, no host "
              "standing in it to greet anyone"),
        Panel("no oil",
              "a small stoppered oil flask on a high wall-shelf, out of reach, dusty"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        f"the lamplit dining room ({ROOM_BUILD}), the low table at the frame's left, fully "
        f"inside the frame. {JESUS_BUILD}, reclining on the near couch on his left side, "
        "propped on his left elbow, facing the low table, his empty sandals lying together on "
        "the floor beside the couch, well clear of his feet, his feet themselves completely "
        "bare and unshod -- no strap, no sole, no footwear of any kind touching either foot, "
        "his ten bare toes and the skin of both feet fully visible, dusty and unwashed -- "
        "extended away from the table past the couch's foot-end "
        "toward the lower right -- never seated upright on a chair, never at a high table -- "
        f"fully inside the frame; {SIMON_BUILD}, reclining on the far couch across the table, "
        "propped on his elbow, his head turned toward the doorway, composed; two or three "
        "other guests on the far couches as unindividuated hatched figures in undyed and ochre "
        "wool, faces turned toward the door, none finished. At the right, just inside the "
        f"doorway, stopped: {WOMAN_BUILD}, her hair bound under the cloth, the sealed alabaster "
        f"flask ({ALABASTER_BUILD}) held in both hands against her breast, fully inside the "
        "frame, her eyes on Jesus's feet, her dress full and modest, never a sensual pose; her "
        "contour drawn steady and single-struck, no doubled or tremored line anywhere in her "
        "figure; the dry foot-basin and folded towel by the door-jamb between her and the "
        "couch-foot, fully inside the frame. A cold grey-umber stain lies in the paper itself "
        "beneath and around where she stands, formless and matte, lying beneath the linework so "
        "every drawn line passes over it unbroken, its feathered damp edge crossing the drawn "
        "frame border into the page's own lower-right margin directly below her, never over any "
        "face, bounded to less than a third of the page; a band of clean paper between the "
        "stain and the basin, the couch-foot, Jesus's feet, and every other figure; the stain "
        "nowhere near Jesus and never beneath his couch. Stage 0 dosage: no blue Swirls of Life "
        "ink motif anywhere on this page -- no blue ink appears anywhere in the scene, the "
        "panels, or the margins."
    ),
    material_closer=(
        "the cold stain lying in the paper beneath the woman at the door is the only unusual "
        "ink at work on this page, and no blue appears anywhere."
    ),
    panel_motions=(
        "the light across the dry basin warms very slightly and settles",
        "a thin haze of lamp-smoke drifts across the empty doorway",
        "the shelf flask sits undisturbed, exactly as drawn",
    ),
    main_scene_animation=(
        "the woman stands still just inside the door, one slow breath, her mantle settling from "
        "her walk and stilling; Simon's turned head stays turned, still; Jesus stays exactly as "
        "drawn, one slow breath, his face toward the table, his feet completely still; the "
        "guests hold; the lamp flames on the stand waver softly; the cold stain in the paper "
        "stays exactly as drawn, never deepening, never spreading, never fading;"
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain in the paper beneath the woman at the door",
    caption_lines=("at his own table",),
    corner_note="NOTE: not invited",
    refs=[R_JESUS],
    model_tier="veo3_1_lite",
    clip_duration=8,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F02 -- "stood at his feet behind him weeping"  (narration KJV, Luke 7:38)
# She has crossed the room and stands where no guest stands. The tears begin;
# the stain does not move.
# ===========================================================================
F02 = PageSpec(
    seq_title="SHE LOVED MUCH",
    frame_label="F02",
    panels=(
        Panel("in the city", "a narrow dusk street between close house walls, empty"),
        Panel("alabaster", "a close object study of the sealed flask, pale veined stone, its "
              "small stopper"),
        Panel("behind him",
              "the back of Jesus's head and one shoulder as he reclines, seen from behind, "
              "close"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        f"{WOMAN_BUILD}, standing at the foot-end of Jesus's couch, behind him, fully inside "
        "the frame, her head bowed, wet tear-tracks on her cheeks, the sealed alabaster flask "
        "held low in both hands, her hair still bound under the cloth, her dress full and "
        "modest; her contour drawn steady and single-struck, no doubled or tremored line "
        f"anywhere in her figure. {JESUS_BUILD}, reclining on the near couch on his left side, "
        "propped on his left elbow, his head and torso toward the table, his face NOT turned "
        "toward her; his bare feet -- no sandal, strap, or footwear of any kind on either foot -- "
        "extended toward her on the couch-end, fully inside the "
        f"frame, a few fallen tear-drops on them. Beyond, the low table, {SIMON_BUILD} watching "
        "from the far couch, the guests as hatched masses. The same cold grey-umber stain lies "
        "in the paper beneath her standing feet, still crossing the drawn frame border into the "
        "lower-right margin, unchanged in every way from before; the tears are in the scene, on "
        "his feet; the stain is in the paper, beneath her; a band of clean paper between them "
        "at every point; the stain nowhere near his feet or his couch, never over any face. "
        "Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page -- the only "
        "water on this page is her tears, drawn plainly in the scene, and no blue ink appears "
        "anywhere in the scene, the panels, or the margins."
    ),
    material_closer=(
        "the cold stain in the paper beneath her is the only unusual ink at work on this page; "
        "her tears are plain drawn water, and no blue appears anywhere."
    ),
    panel_motions=(
        "a thin haze drifts along the empty dusk street",
        "the flask study holds, the light across it warming very slightly",
        "the sketched shoulder holds, still",
    ),
    main_scene_animation=(
        "the woman's shoulders tremble with weeping and settle, her head staying bowed, her "
        "lips closed; the wet tracks on her cheeks stay as they are; Jesus stays exactly as "
        "drawn, his face toward the table, one slow breath, his feet completely still; Simon "
        "and the guests hold; the lamp flames waver; the cold stain in the paper stays exactly "
        "as drawn, never deepening, never spreading, never fading;"
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain in the paper beneath the woman's feet",
    caption_lines=("stood at his feet", "behind him weeping"),
    corner_note="NOTE: behind him",
    refs=[R_JESUS, R_WOMAN, R_WOMAN_FACE, R_ALABASTER, R_ROOM],
    model_tier="veo3_1_lite",
    clip_duration=8,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F03 -- "and kissed his feet"  (narration KJV, Luke 7:38)
# The climax of her love -- and the page that proves the doctrine by NOT
# changing the stain. Smallest animation ask (fragile composition).
# ===========================================================================
F03 = PageSpec(
    seq_title="SHE LOVED MUCH",
    frame_label="F03",
    panels=(
        Panel("with tears", "close on a bare foot's instep with a few fallen drops on it"),
        Panel("her hair loosed",
              "her plain head-cloth lying discarded on the floor stones"),
        Panel("the ointment",
              "the flask now open on the floor stones, its stopper lying beside it"),
    ),
    still_shot_type="CLOSE MEDIUM shot",
    anim_shot_desc="close medium shot",
    main_scene_still=(
        f"{WOMAN_BUILD}, kneeling on the floor at his feet, fully inside the frame, her hair "
        "now unbound and fallen forward, its ends drawn across his wet feet, her head bowed low "
        "over them so that her face is turned down and mostly hidden by her hair, her lips at "
        "his instep -- the kiss already made, reverent; her red mantle covering her shoulders "
        "and back, her dress full and modest, never a sensual pose; her contour drawn steady "
        "and single-struck, no doubled or tremored line anywhere in her figure; the open "
        "alabaster flask in one hand, tilted, its stopper lying on the floor stones, a matte "
        "sheen of ointment on his feet. His bare feet -- no sandal, strap, or footwear of any "
        "kind on either foot -- fully inside the frame on the couch-end, "
        "the lower hem of his plain cream robe and the wooden foot of the couch visible, his "
        "face out of frame. The cold grey-umber stain lies in the paper beneath her knees and "
        "the floor around them, crossing the drawn frame border into the lower-right margin, "
        "EXACTLY as before -- its edge nearest his feet as saturated as everywhere else, "
        "neither dried nor spread; the tears and the ointment are in the scene, on his feet; "
        "the stain is in the paper, beneath her; a band of clean paper between them at every "
        "point; the open flask and its stopper standing on clean paper outside the stain's "
        "edge; never over any face. Stage 0 dosage: no blue Swirls of Life ink motif anywhere "
        "on this page -- no blue ink appears anywhere in the scene, the panels, or the margins."
    ),
    material_closer=(
        "the unchanged cold stain in the paper beneath her knees is the only unusual ink at "
        "work on this page; the tears and ointment are plain drawn liquid on his feet, and no "
        "blue appears anywhere."
    ),
    panel_motions=(
        "the drops on the instep hold, the light across them warming very slightly",
        "the fallen head-cloth lies undisturbed",
        "the open flask sits still, exactly as drawn",
    ),
    main_scene_animation=(
        "her shoulders shake once with a sob and still; her hands hold the tilted flask exactly "
        "as drawn, not moving; her hair lies still across his feet; his feet stay completely "
        "still; her lips stay closed against his instep, her mouth not moving; the cold stain "
        "in the paper stays exactly as drawn, never deepening, never spreading, never fading;"
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain in the paper beneath the woman's knees",
    caption_lines=("and kissed his feet",),
    corner_note="NOTE: stain unchanged",
    refs=[R_JESUS, R_WOMAN, R_WOMAN_FACE, R_ALABASTER, R_ROOM],
    model_tier="kling3_0",
    clip_duration=7,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F04 -- "she is a sinner"  (narration: Simon's unspoken thought, Luke 7:39)
# Simon's page -- the thought he never spoke -- and the first blue of the
# episode, entering with "Jesus answered anyway". First of two at-cap pages
# (Stain D3 + Swirl 1 = 4). Crop source for simon_face_ref.
# ===========================================================================
F04 = PageSpec(
    seq_title="SHE LOVED MUCH",
    frame_label="F04",
    panels=(
        Panel("a prophet", "a small robed figure far off on a bare hill, staff in hand"),
        Panel("the guests",
              "two or three guests' faces on a far couch turned toward the lower corner, hard, "
              "unfinished"),
        Panel("answered anyway",
              "Jesus's right hand lifted a little from a cushion, palm open, close"),
    ),
    still_shot_type="MEDIUM TWO-SHOT",
    anim_shot_desc="medium two-shot",
    main_scene_still=(
        f"{SIMON_BUILD}, reclining on the far couch propped on his elbow, largest in the frame, "
        "fully inside the frame, his face turned toward the lower right, his brow drawn down, "
        "his mouth SHUT, composed and cold, courteous and closed, never a sneer; "
        f"{JESUS_BUILD} in the near foreground, reclining on the near couch on his left side, "
        "his shoulder and the side of his face visible, his gaze on Simon, calm, his right hand "
        "lifted a little from the cushion, palm open toward Simon, already raised, not touching "
        f"anything, fully inside the frame; at the lower-right corner of the frame, the bowed "
        f"figure of {WOMAN_BUILD} -- her hair unbound and fallen forward, her red mantle, "
        "the open alabaster flask on the floor beside her on clean paper -- her contour drawn "
        "steady and single-struck, no doubled or tremored line anywhere in her figure. The cold "
        "grey-umber stain lies in the paper beneath her at the lower-right corner, crossing the "
        "drawn frame border into the lower-right margin, unchanged, never over any face, "
        "nowhere near Jesus or Simon and never beneath either couch. Stage 1 dosage: exactly "
        "one restrained thread of blue ink curling up from the back of Jesus's lifted right "
        "hand, touching only his hand and the air just above it, the only blue on the whole "
        "page, behaving like one stroke of wet ink bled into the paper, smooth and open in its "
        "curl, never blot-shaped; the stain formless and matte, never swirl-shaped; a wide band "
        "of untouched clean paper between the thread and the stain at every point (they sit at "
        "opposite corners of the frame); the thread drawn ON the page's surface, the stain "
        "lying IN the paper beneath the linework."
    ),
    material_closer=(
        "the cold stain in the paper beneath the woman and the single blue thread at his hand "
        "are the only two kinds of unusual ink at work on this page, kept apart by clean paper."
    ),
    panel_motions=(
        "a faint heat-shimmer plays over the far hill",
        "the sketched faces hold, the light across them warming very slightly",
        "the lifted hand holds, still",
    ),
    main_scene_animation=(
        "Simon's jaw sets and his eyes narrow a fraction and hold, his lips staying closed and "
        "completely still -- he is not speaking and his mouth does not move at all; Jesus stays "
        "exactly as drawn, his lifted hand not rising further and not reaching toward anything, "
        "one slow breath; the woman's bowed head stays bowed; the single thin blue ink thread "
        "at his hand stays exactly as drawn, in place, for the whole clip; the cold stain in "
        "the paper stays exactly as drawn, never deepening, never spreading, never fading;"
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain in the paper beneath the woman and the single blue thread at his lifted hand",
    caption_lines=("she is a sinner",),
    corner_note="NOTE: not out loud",
    # NOT _REFS_FULL: this page is the crop SOURCE for simon_face_ref (it doesn't exist yet).
    refs=[R_JESUS, R_SIMON, R_WOMAN, R_WOMAN_FACE, R_ALABASTER, R_ROOM],
    model_tier="veo3_1_lite",
    clip_duration=8,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F05 -- "he frankly forgave them both"  (narration: the debtor parable)
# The parable page. The stain turns HERE -- the first spoken forgiveness.
# ===========================================================================
F05 = PageSpec(
    seq_title="SHE LOVED MUCH",
    frame_label="F05",
    panels=(
        Panel("five hundred pence",
              "a ringed, well-kept hand holding a large empty purse upside-down over a table, "
              "nothing falling from it"),
        Panel("fifty",
              "a rough, work-worn hand holding a small empty purse likewise turned out, nothing "
              "falling"),
        Panel("forgave them both",
              "a creditor's two open hands, palms up and empty, over the same table -- "
              "releasing"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        f"{JESUS_BUILD}, reclining on the near couch on his left side, propped on his left "
        "elbow, his face toward Simon, calm, his right hand now open in a teller's gesture -- "
        f"already lifted, not touching anything -- fully inside the frame; {SIMON_BUILD}, "
        "reclining on the far couch across the table, listening, composed and guarded, his "
        f"hands folded, fully inside the frame; at the lower right, {WOMAN_BUILD}, her hair "
        "unbound and fallen forward, kneeling at his feet, her head bowed but lifted a little -- "
        "listening -- her dress full and modest, her contour drawn steady and single-struck, "
        "no doubled or tremored line anywhere in her figure; the open alabaster flask on the "
        "floor beside her on clean paper; his bare feet -- no sandal, strap, or footwear of any "
        "kind on either foot -- on the couch-end with the matte "
        "ointment sheen, fully inside the frame. The cold grey-umber stain in the paper beneath "
        "her knees still crosses the drawn frame border into the lower-right margin on the door "
        "side, never over any face -- but its whole edge nearest Jesus's couch and feet has "
        "dried to a pale ring, the wet remainder lying only toward the door and the margin, "
        "away from him; no stain anywhere near Jesus, his couch, or his feet. Stage 1 dosage, "
        "held: the same single restrained thread of blue ink rising from the back of his open "
        "right hand, touching only his hand and the air above it, the only blue on the whole "
        "page, behaving like one stroke of wet ink bled into the paper, smooth and open, never "
        "blot-shaped; the stain formless and matte, never swirl-shaped; a wide band of "
        "untouched clean paper between the thread and the stain's wet remainder at every "
        "point; the thread drawn ON the page, the stain lying IN the paper beneath the "
        "linework."
    ),
    material_closer=(
        "the stain drying back from his side and the single blue thread at his hand are the "
        "only two kinds of unusual ink at work on this page, kept apart by clean paper."
    ),
    panel_motions=(
        "the upturned purse holds, nothing falling",
        "the small purse holds, nothing falling",
        "the open hands hold, the light across them warming very slightly",
    ),
    main_scene_animation=(
        "the woman's bowed head lifts a fraction as she listens and holds, her eyes staying "
        "down; Jesus stays exactly as drawn, his open hand not moving further, one slow breath, "
        "his lips staying closed and completely still -- he is not speaking and his mouth does "
        "not move at all; Simon holds, one breath; the lamp flames waver; the single thin blue "
        "ink thread at his hand stays exactly as drawn, in place, for the whole clip; the stain "
        "and its dried pale edge stay exactly as drawn, never deepening, never spreading, never "
        "fading;"
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain beneath the woman, its dried pale edge, and the single blue thread at his hand",
    caption_lines=("forgave them both",),
    corner_note="NOTE: that's freely",
    refs=_REFS_FULL,
    model_tier="kling3_0",
    clip_duration=10,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F06 -- "which of them will love him most"  (narration: Simon's hedge)
# Deliberately the stillest middle page -- nothing advances on either motif;
# the one human thing is a grudging half-nod.
# ===========================================================================
F06 = PageSpec(
    seq_title="SHE LOVED MUCH",
    frame_label="F06",
    panels=(
        Panel("two debtors",
              "two small figures walking away from a counting-house door side by side, one in "
              "fine dress, one in rags, seen from behind"),
        Panel("I suppose", "Simon's hand, palm half-turned outward in a reluctant concession, "
              "close"),
        Panel("the most",
              "the woman's hand laid flat on Jesus's bare foot, close, the matte sheen on it"),
    ),
    still_shot_type="MEDIUM TWO-SHOT",
    anim_shot_desc="medium two-shot",
    main_scene_still=(
        f"{SIMON_BUILD}, reclining on the far couch propped on his elbow, his face half-turned "
        f"away, eyes down, his chin just beginning to dip, fully inside the frame; {JESUS_BUILD}, "
        "reclining on the near couch on his left side, his face on Simon, patient, his open "
        "right hand exactly as before, already lifted, fully inside the frame; at the lower "
        f"right, {WOMAN_BUILD}, her hair unbound, bowed at his feet, her dress full and modest, "
        "her contour drawn steady and single-struck, no doubled or tremored line anywhere in "
        "her figure; the open flask on clean paper beside her; his bare feet -- no sandal, "
        "strap, or footwear of any kind on either foot -- on the couch-end, fully "
        "inside the frame. The cold grey-umber stain in the paper beneath her knees exactly as "
        "before -- its edge nearest Jesus's couch dried to a pale ring, the wet remainder lying "
        "only toward the door and still crossing the lower-right margin, never over any face, "
        "nowhere near either couch. Stage 1 dosage, held: the same single thread of blue ink "
        "from the back of his open hand, touching only his hand and the air above it, the only "
        "blue on the page; a wide band of clean paper between thread and stain at every point."
    ),
    material_closer=(
        "the stain drying back from his side and the single blue thread at his hand are the "
        "only two kinds of unusual ink at work on this page, kept apart by clean paper."
    ),
    panel_motions=(
        "the two far figures hold their walk, unmoving",
        "the half-turned hand holds",
        "the hand on the foot holds, the light across it warming very slightly",
    ),
    main_scene_animation=(
        "Simon's grudging half-nod completes -- his chin dips once and holds, his eyes never "
        "meeting Jesus's, his lips staying closed and completely still, not speaking; Jesus "
        "stays exactly as drawn, one slow breath, his lips also closed and completely still -- "
        "not speaking; the woman holds exactly as drawn; the single thin blue ink thread stays "
        "exactly as drawn, in place; the stain and its dried edge stay exactly as drawn, never "
        "deepening, never spreading, never fading;"
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain beneath the woman, its dried pale edge, and the single blue thread at his hand",
    caption_lines=("will love him most",),
    corner_note="NOTE: he hedged",
    refs=_REFS_FULL,
    model_tier="kling3_0",
    clip_duration=7,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F07 -- "Seest thou this woman?"  (narration KJV, Luke 7:44)
# The crossing point. Jesus has TURNED and looks at her; she is seen for the
# first time in the episode. Second at-cap page (Stain D2 + Swirl 2 = 4).
# ===========================================================================
F07 = PageSpec(
    seq_title="SHE LOVED MUCH",
    frame_label="F07",
    panels=(
        Panel("the water", "tear-drops on a bare instep, close"),
        Panel("the kiss",
              "her bowed profile at his instep, her face hidden by her fallen hair, close"),
        Panel("the oil", "the open flask on the floor stones, stopper beside it"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        f"{JESUS_BUILD}, reclining on the near couch on his left side but turned back toward "
        "the couch-foot, his torso and face toward the woman, his right hand extended low and "
        "open toward her over the couch's side at couch height -- a hand's width clear of his "
        f"own feet and clear of her, touching nothing -- fully inside the frame; {WOMAN_BUILD}, "
        "kneeling at his feet, her hair unbound and fallen forward, her face lifted to his, "
        "wet, her eyes meeting his, her dress full and modest, her contour drawn steady and "
        f"single-struck, no doubled or tremored line anywhere in her figure, fully inside the "
        f"frame; Jesus's own bare feet -- no sandal, strap, or footwear of any kind on either "
        "foot -- on the couch-end with the matte ointment sheen, fully inside the frame; "
        f"{SIMON_BUILD} beyond on the far couch, his gaze on JESUS, not on her; the open "
        "flask on clean paper beside her. The cold grey-umber stain in the paper beneath her "
        "knees exactly as before -- its edge nearest Jesus dried to a pale ring, the wet "
        "remainder toward the door and the lower-right margin, never over any face, nowhere "
        "near Jesus. Stage 2 dosage: the blue ink motif quietly present -- a few soft blue "
        "threads rising UPWARD ONLY from the back of his extended hand into the air above it, "
        "every thread's root touching his hand directly and going up from there, none "
        "descending toward his feet, the floor, or her, none dripping, none pooling; at the top "
        "of the threads, one soft, irregular, hazy patch of the same blue pigment, entirely "
        "amorphous, with soft feathered edges and no internal structure of any kind, exactly "
        "like a single drop of watercolor spreading into wet paper, completely without symmetry "
        "or distinct segments, touching only his hand and the air above it, touching no other "
        "person and nothing else on the page; the floor and his feet free of any ink of any "
        "kind; every thread behaving like wet ink bled into the paper, smooth and open, never "
        "blot-shaped; the stain formless and matte, never swirl-shaped; a wide band of "
        "untouched clean paper between the threads and the stain at every point; the threads "
        "drawn ON the page, the stain lying IN the paper beneath the linework."
    ),
    material_closer=(
        "the stain drying back from his side and the soft blue threads at his extended hand are "
        "the only two kinds of unusual ink at work on this page, kept apart by clean paper."
    ),
    panel_motions=(
        "the drops hold, the light warming very slightly",
        "the sketched profile holds, tone-only",
        "the flask sits still",
    ),
    main_scene_animation=(
        "the woman's eyes lift the last small distance to his and one full blink -- closes, "
        "then opens again fully, ending wide open on him; Jesus stays exactly as drawn, his "
        "extended hand not moving further, one slow breath, his lips closed and completely "
        "still -- he is not speaking and his mouth does not move at all; Simon's gaze stays on "
        "Jesus, never turning to her; the soft blue threads at his hand drift gently within "
        "their own small area, never lowering toward the floor or his feet; the stain and its "
        "dried edge stay exactly as drawn, never deepening, never spreading, never fading;"
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain beneath the woman, its dried pale edge, and the blue threads at his extended hand",
    caption_lines=("Seest thou this woman?",),
    corner_note="NOTE: he saw her",
    refs=_REFS_FULL,
    model_tier="kling3_0",
    clip_duration=7,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F08 -- HERO -- "her sins, which are many, are forgiven"  (Luke 7:47)
# The declaration and the episode's gospel pivot. The stain is gone between
# F07 and F08 -- at his word -- leaving only the ring. Longest interior slot.
# ===========================================================================
F08 = PageSpec(
    seq_title="SHE LOVED MUCH",
    frame_label="F08",
    panels=(
        Panel("the receipt",
              "a small wax tablet, its surface scraped smooth and blank, lying on a table"),
        Panel("her face",
              "a close study of her tear-streaked face, lifted, at rest, eyes open, contour "
              "steady"),
        Panel("loveth little",
              "a stiff figure reclining alone at a table's far end, small, an untouched cup "
              "before him"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        f"{JESUS_BUILD}, reclining on the near couch, turned fully toward her, his face on her, "
        "calm and kind, his right hand open toward her as before, fully inside the frame; "
        f"{WOMAN_BUILD}, risen tall on her knees at his feet, her face lifted to his, her hands "
        "open at her sides, her hair unbound, her dress full and modest, her contour drawn "
        "steady and single-struck, no doubled or tremored line anywhere in her figure, fully "
        "inside the frame; the open alabaster flask on the floor beside her, outside the ring; "
        f"{SIMON_BUILD} beyond on the far couch, his face at last turned toward HER, unreadable; "
        "the guests as hatched masses; his bare feet -- no sandal, strap, or footwear of any "
        "kind on either foot -- on the couch-end, fully inside the frame. "
        "Of the cold stain, nothing wet remains anywhere: only a thin, faint, pale dried "
        "watermark ring lies in the paper around where she kneels -- the dried edge of the old "
        "stain, the stain itself gone -- and the paper inside that ring is the cleanest, "
        "brightest cream on the whole page; no border crossing remains but a pale dried trace; "
        "the ring contains no blue, no gold, and no red, and touches no figure's drawn line. "
        "Stage 2 dosage, held: a few soft blue threads rising UPWARD ONLY from the back of his "
        "open hand into the air above it, their roots touching his hand and nowhere else, one "
        "soft amorphous watercolor patch at their top, touching only his hand and the air; a "
        "band of clean paper between the threads and the dried ring."
    ),
    material_closer=(
        "the dried pale ring in the paper and the soft blue threads at his hand are the only "
        "two kinds of unusual mark on this page, and the paper inside the ring is the cleanest "
        "on it."
    ),
    panel_motions=(
        "the blank tablet lies undisturbed",
        "the sketched face blinks once fully -- closes, then opens again, ending wide open",
        "the stiff figure holds",
    ),
    main_scene_animation=(
        "Jesus's one small kind nod completes and holds, his lips staying closed and completely "
        "still -- he is not speaking and his mouth does not move at all; the woman takes one "
        "slow deep breath and her shoulders drop and release as the weight visibly leaves her, "
        "then hold; Simon's turned face stays turned toward her, still; the lamp flames waver; "
        "the soft blue threads at his hand drift gently within their own small area, never "
        "lowering; the dried pale ring stays exactly as drawn, and no new stain, spot, or "
        "darkening appears anywhere on the page at any point;"
    ),
    fence_kind="stain",
    fence_callout="the dried pale ring in the paper around where the woman kneels",
    caption_lines=("which are many, are forgiven",),
    corner_note="NOTE: forgiven first",
    refs=_REFS_FULL,
    model_tier="kling3_0",
    clip_duration=10,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F09 -- "thy faith hath saved thee"  (narration KJV, Luke 7:50)
# The sending. She has risen; the flask is left on the floor; the peace is in
# the room's air. The episode's one Stage 3 page.
# ===========================================================================
F09 = PageSpec(
    seq_title="SHE LOVED MUCH",
    frame_label="F09",
    panels=(
        Panel("not thy tears", "a close study of her face, tears dried, at peace"),
        Panel("not thy ointment", "the open flask standing alone on the floor stones"),
        Panel("go in peace",
              "the open doorway from inside, its threshold clear, a dawn-grey courtyard beyond"),
    ),
    still_shot_type="WIDE shot",
    anim_shot_desc="wide shot",
    main_scene_still=(
        f"the lamplit dining room ({ROOM_BUILD}) fully inside the frame. {WOMAN_BUILD}, "
        "standing risen at the couch-foot, facing the doorway at the right, at rest, her hair "
        "bound back beneath her re-settled head-cloth, her mantle drawn about her, her hands "
        "empty and open at her sides, her dress full and modest, her contour drawn steady and "
        f"single-struck, no doubled or tremored line anywhere in her figure, fully inside the "
        f"frame; {JESUS_BUILD}, half-risen on his left elbow on the near couch, his right hand "
        f"open toward her in sending, his face on her, fully inside the frame; {SIMON_BUILD} on "
        "the far couch, the guests as hatched masses; the open alabaster flask left on the "
        "floor at the couch-foot behind her, fully inside the frame; the dry foot-basin and "
        "folded towel still standing unused by the door. No stain, ring, or grey blot anywhere "
        "in the paper -- the paper wholly clean. Stage 3 dosage: the blue ink motif, with "
        "traces of muted gold, is woven through the whole scene -- threads drifting in one "
        "loose open band through the lamplit air of the room above every head, tied to no "
        "single figure, touching no person, touching neither the flask on the floor nor his "
        "feet, behaving like wet ink bled through the page's own wash, never a glow."
    ),
    material_closer=(
        "the blue-and-gold band woven through the air of the room is the only unusual ink on "
        "the page, and the paper beneath it is wholly clean."
    ),
    panel_motions=(
        "the sketched face holds, the light warming very slightly",
        "the flask sits still",
        "a thin haze drifts across the courtyard beyond the door",
    ),
    main_scene_animation=(
        "the woman's empty hands open a little further at her sides and settle; her chest rises "
        "once in a slow breath, her face toward the door; Jesus stays exactly as drawn, his "
        "open hand not moving, one slow breath, his lips closed and completely still -- not "
        "speaking; Simon and the guests hold; the flask sits still on the floor; the "
        "blue-and-gold ink threads drift smoothly within their own fixed band across the air "
        "above every head, never lowering onto any figure; the lamp flames waver; no new "
        "stain, spot, or darkening appears anywhere on the page at any point;"
    ),
    fence_kind="none",
    caption_lines=("Thy faith hath", "saved thee"),
    corner_note="NOTE: she left it",
    refs=_REFS_FULL,
    model_tier="veo3_1_lite",
    clip_duration=8,
    panel_style="woodcut_hybrid",
)

PAGES = {
    "f01": F01, "f02": F02, "f03": F03, "f04": F04, "f05": F05,
    "f06": F06, "f07": F07, "f08": F08, "f09": F09,
}

# ---- covers -------------------------------------------------------------
# The hook's three absences are Simon's table; the landing is the box she left
# behind. So the covers are the alabaster box in its two states, at the two ends
# of the same room. Jesus appears on neither cover.

FRONT_COVER = CoverSpec(
    side="front",
    scene=(
        "the woman, small and isolated in the lower third, standing on the threshold stones of "
        "Simon's open doorway seen from behind and a little to one side, the sealed alabaster "
        "flask held in both hands against her breast, her madder-red mantle drawn about her, "
        "her head covered, no sandals or footwear of any kind, her bare feet on the stone; "
        "beyond and above her through the doorway, "
        "the lamplit dining room -- the low table, the reclining figures on their couches small "
        "and unindividuated, the near couch's foot-end nearest the door with a pair of bare "
        "feet extended toward it, the tall lamp-stand; the plain clay foot-basin and folded "
        "towel standing dry beside the door-jamb; behind her, the dim courtyard and a narrow "
        "dusk street between close walls."
    ),
    lighting=(
        "Warm amber lamplight pouring OUT through the doorway across the threshold stones and "
        "her shoulders; cold blue-grey dusk holding the street, the courtyard, and the stone "
        "jambs of the door, cinematic atmospheric haze, dramatic volumetric light rays, "
        "photographic tonality."
    ),
    background_detail="",
    title="SHE LOVED MUCH",
    subtitle="LUKE 7",
    title_position="top",
    animation=(
        "the hem of her mantle stirs faintly in the doorway's air; the lamplight inside stays "
        "exactly as warm and steady as it already is, unchanged; the dusk outside stays exactly "
        "as cold and dim as it already is; the reclining figures, the basin, and the lamp-stand "
        "stay exactly as drawn; no new figure, mark, or text appears"
    ),
    extra_avoid="jewelry, bared shoulders, revealing dress, sensual pose, hinged box, jewelry casket, wooden chest, modern clothing",
    refs=[R_WOMAN, R_WOMAN_FACE, R_ALABASTER, R_ROOM],
    clip_duration=4,
)

BACK_COVER = CoverSpec(
    side="back",
    scene=(
        "the same dining room at dawn, empty of every person: the couches bare, their cushions "
        "pressed, the low table cleared; on the worn floor stones at the foot-end of the near "
        "couch, the alabaster flask standing open, its small stopper lying beside it, a matte "
        "trace of spent ointment at its lip, alone; the dry foot-basin and folded towel still "
        "standing unused beside the doorway; the lamps on the stand burned low; the doorway "
        "open to a courtyard just catching light. The floor where she knelt is bare clean "
        "stone. One small hard-capped hooked curl of blue ink with a trace of muted gold rises "
        "from the floor stones beside the flask -- from the place where she knelt, not from the "
        "flask -- its whole visible length no longer than a hand's width, curling back toward "
        "its own root like a comma or a fishhook WITHOUT fully closing into a ring, flat and "
        "two-dimensional, drawn ON the paper's surface, a single continuous brushstroke, never "
        "a ring, never a bracelet, never a bangle, never jewelry, never metallic, never "
        "reflective, never straightening, never trailing, behaving like a small dab of living "
        "ink, never a glow."
    ),
    lighting=(
        "Warm dawn gold low through the doorway across the floor stones, the flask, and the "
        "couch-foot; cold blue-grey holding the room's far corners, the bare far couches, and "
        "the burned-low lamp-stand, cinematic atmospheric haze, photographic tonality."
    ),
    background_detail="",
    title="SHE LEFT CARRYING HIS PEACE",
    subtitle="1 JOHN 4:19",
    title_position="bottom",
    animation=(
        "fine dust motes drift slowly through the dawn shaft in the doorway; the last low lamp "
        "flame on the stand wavers softly and settles; the blue-gold curl stays exactly as "
        "drawn, in place, for the whole clip; the dawn light stays exactly as warm and low as "
        "it already is, unchanged; no new figure, mark, or text appears"
    ),
    extra_avoid="any human figure, hinged box, jewelry casket, wooden chest, jewelry, bright neon",
    refs=[R_ALABASTER, R_ROOM],
    clip_duration=8,
)

COVERS = {"front": FRONT_COVER, "back": BACK_COVER}

# ---- assembly manifest ---------------------------------------------------
# Word weights are Fable's own count against the locked narration (sum 240,
# matching narration.md's real word count; 103.29s locked audio, natural speed,
# no time-stretch). Boomerang nowhere in this episode -- every unit either
# settles a completing gesture, drifts a band/motes, or wavers lamp flames, all
# of which read backwards under reversal. Final modes are an assembly-QC call
# on the real renders, per the standing rule.

MANIFEST = EpisodeManifest(
    episode_dir=HERE,
    narration=HERE / "narration.mp3",
    units=[
        Unit("front", HERE / "front_cover.mp4", 9, "freeze"),
        Unit("f01", HERE / f"{HERE.name}_f01_9x16.mp4", 25, "freeze"),
        Unit("f02", HERE / f"{HERE.name}_f02_9x16.mp4", 23, "freeze"),
        Unit("f03", HERE / f"{HERE.name}_f03_9x16.mp4", 18, "freeze", tail_loop_seconds=1.0),
        Unit("f04", HERE / f"{HERE.name}_f04_9x16.mp4", 24, "freeze"),
        Unit("f05", HERE / f"{HERE.name}_f05_9x16.mp4", 26, "freeze", tail_loop_seconds=1.0),
        Unit("f06", HERE / f"{HERE.name}_f06_9x16.mp4", 18, "freeze", tail_loop_seconds=1.0),
        Unit("f07", HERE / f"{HERE.name}_f07_9x16.mp4", 19, "freeze", tail_loop_seconds=1.0),
        Unit("f08", HERE / f"{HERE.name}_f08_9x16.mp4", 30, "freeze", tail_loop_seconds=1.0),
        Unit("f09", HERE / f"{HERE.name}_f09_9x16.mp4", 23, "freeze"),
        Unit("back", HERE / "back_cover.mp4", 25, "freeze"),
    ],
    scores={
        # Felt-piano identity reused near-verbatim from episode 5/7/8/Naaman (the series
        # default). Duck profile starts from the Bier's own working values -- re-measure
        # against the real mixed output before calling this final, per this project's own
        # "a duck does not transfer between score generations" rule.
        "piano": ScoreVariant(
            score=HERE / "score_piano.mp3",
            duck=DuckProfile(gain_db=-6, threshold=0.12, ratio=2.5, release_ms=250),
            out=HERE / f"{HERE.name}_final_piano.mp4",
        ),
    },
    panel_style="woodcut_hybrid",
)
