"""Episode spec for "The Bier He Touched" (Luke 7:11-17, the widow of Nain).
Dead ink: STAIN (ceremonial uncleanness / corpse-defilement) ONLY -- the
series-plan retag is binding (v3 wrongly called this Fray; the text has zero
fear/doubt vocabulary, her arc is grief met with compassion, and Fray is
fear/doubt only). NT episode -- the OT Stage 1-2 swirl cap does NOT apply;
the swirl reaches Stage 3 once, on F06, per the fulfilment-on-page carve-out.

Design authored by Fable (full brief: `_DESIGN_BRIEF.md` in this folder),
implemented by Sonnet per the "Fable designs, Sonnet executes" rule. Four
open questions Fable deliberately left unresolved were put to the user and
answered (all recommended options taken, matching episode 5's own pattern):
(1) back-cover subtitle is NUMBERS 19:11, completing the season's #2->#7
rhyme (episode 2's front cover already reads "NUMBERS 19"); (2) the swirl
reaches Stage 3 on F06 -- the NT fulfilment-on-page carve-out, not the OT
habit-cap; (3) the proposed panel-crop `empty_bier_ref.png` (from F03's own PANEL 2)
was attempted but abandoned during implementation: that panel's own prompt
text never carried the bier's literalism-trap guard (no coffin/box/lid),
and it rendered with raised side walls, a tray/box shape -- exactly the
defect the guard exists to prevent. Cropping it would have propagated a
boxy bier into F06 and the back cover, so both fall back to the brief's own
alternative: chain the regular with-body `bier_ref` plus an explicit
"now empty, no raised walls, never a box" text override, per open question
#6's stated fallback; (4) F04 stays at the
high-tide cap (Stain D2 + Swirl Stage 2 = 4) with the full QUAD lock,
matching episode 12's own proven at-cap shape, so the swirl's bloom still
visibly answers the word "Arise".

Two small corrections made during this implementation pass (brief vs. code
mapping, not creative changes): (a) F06's own refs list in the brief named
`bier_ref` (the with-body ref) even though its own scene text and its own
open-question #6 both call for the EMPTY bier -- F06 uses
`empty_bier_ref` here, consistent with the brief's chosen resolution of
that open question. (b) F06's caption was drafted from Luke 7:16 ("God
hath visited his people") -- a real verse, but not a word of this
episode's own LOCKED narration, breaking the series' own caption rule
(every caption is a verbatim fragment of what is actually spoken on that
page, same rule every precedent episode follows). Replaced with a fragment
of F06's own beat text ("Life spread from Jesus... to the boy"). (c) F06's
refs list originally named `empty_bier_ref` per the brief's own chosen
resolution of open question #6 -- but implementation found that panel's own
render defective (see below), so F06 and the back cover both fall back to
`bier_ref` + a text override instead, superseding (a).

A post-render user note (2026-08-31, after seeing F03/F04's first renders):
the bearers holding the bier aloft at shoulder height through the touch
(F03) and the extended "Arise" pause (F04) read as physically awkward --
four men frozen mid-carry through a whole static conversation. Fixed by
having the bearers set the bier down to rest directly on the bare ground
for those two pages only (F01/F02 stay in motion or just-halted; F05/F06
stay shoulder-borne, brief holds/a resuming procession, not an extended
static pause). Explicit "never on built-in legs, a table, a bench, or a
stand" guards carried over from the F04 box-legs fix below, since a
grounded bier is a new failure surface for the same defect.

The Stain decision (the hard problem this episode poses): the uncleanness
is corpse-contact, not a diagnosis on a living person, so it is attached to
the BIER-AND-ITS-BURDEN as one object -- never to the widow (grief is not
Stain; giving her one would repeat the v3 Fray mistake one motif over) and
never merely "cured" on contact (state changes happen only between pages,
never within a clip). Instead the narration's reversal ("Death didn't
spread from the boy to Jesus. Life spread from Jesus to the boy") is told
as GEOMETRY: from the moment of contact (F03) the stain dries from the
edge nearest Jesus's touching hand outward, page by page, until only the
dried pale ring remains under the boy who sits up inside the cleanest
paper on the page (F05) -- it dies of the touch instead of spreading by
it. The stain never touches Jesus, his hand, or the paper beneath him at
any dose, on any page. The swirl (rising: 0 -> 1 -> 1(held) -> 2 -> 2(held)
-> 3) is anchored to Jesus's own touching hand throughout, crossing the
falling stain at F04 -- "Arise" -- the gospel turn, per the system's own
law (swirl >= stain).

Covers: neither carries Jesus (deliberate -- the narration's hook doesn't
name him yet, and the empty bier says what he did more loudly than his
figure would). Front = the procession carrying the full bier OUT through
the gate of Nain toward the tombs (warm living world / cold procession).
Back = the same bier EMPTY at dawn, graveclothes folded on its boards, a
quiet John 20:7 folded-napkin echo, titled "IT BECOME A HOMECOMING" --
closing the season's #2->#7 rhyme with NUMBERS 19:11.
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

# New to the series. She carries NO motif at all -- no Stain (the diagnosis belongs to
# the bier, not to her grief) and no Fray (the retag is binding). Her contour is stated
# steady on every page she appears on (the standing no-Fray guard, since a weeping
# figure is exactly what a render will spontaneously loosen into fray-like hatching).
WIDOW_BUILD = (
    "the widow of Nain, a Galilean village woman in her late forties, worn thin by loss, a "
    "lined olive-skinned face with deep-set dark eyes red-rimmed from weeping, strands of grey "
    "in the dark hair bound back beneath a plain mourning veil of coarse dark charcoal-grey wool "
    "drawn low over her brow, wearing an ankle-length tunic of faded umber-brown beneath a loose "
    "mourning mantle of the same dark grey wool, its edge visibly rent in one torn place at the "
    "breast, bare dusty feet"
)

# The dead son, State A (F01-F04) -- no ref possible, no face exists to pin. Period
# basis: John 11:44, bound in graveclothes, face bound with a napkin.
SON_SHROUDED = (
    "the dead son: a still human form lying full-length on the open bier, wrapped from chest to "
    "feet in plain linen grave-bands, a folded linen napkin bound over the face so that no "
    "feature of the face is visible, the wrapped form slight and young in build"
)

# The son, State B (F05 onward) -- alive. Ref crops from F05's approved render.
SON_BUILD = (
    "the widow's son, a young man of about eighteen, lean and slight, an olive-skinned unlined "
    "face with large dark eyes and tousled black hair, bare-shouldered above the loosened linen "
    "grave-bands still wrapped about his waist and legs, the unbound napkin fallen in his lap"
)

# The title object. The "bier" literalism trap (the Barrel's "barrel" lesson, same
# family): an image model's prior for "bier"/"funeral procession" is a Western coffin
# or draped casket -- wrong by geography and centuries, and it would hide the shrouded
# form the whole episode turns on. Every prompt states the corrected form first and
# carries the never-coffin/never-box/never-lid triple.
BIER_BUILD = (
    "the bier: an open flat wooden hand-bier -- a plain rectangular pallet of weathered "
    "olive-brown wood boards with two long carrying poles running its full length, borne "
    "shoulder-high on the shoulders of four bearers, its top entirely open to the sky -- never a "
    "coffin, never a casket, never a box, never any lid"
)

GATE_BUILD = (
    "the gate of Nain: a low squared opening in a rough drystone-and-mud-brick village wall, a "
    "heavy timber lintel, the lane through it climbing between small flat-roofed houses stacked "
    "on the green-brown slope of the hill behind; outside the gate, a dusty road running down the "
    "open slope, and scattered dark rock-cut tomb openings in the hillside further down"
)

R_JESUS = Ref("Jesus -- his face, build, and dress", str(REFS_DIR / "jesus_ref.png"))
R_WIDOW = Ref("the widow of Nain -- her face, build, and dress", str(REFS_DIR / "widow_ref.png"))
R_WIDOW_FACE = Ref("the widow of Nain -- her face and eyes, for close crops", str(REFS_DIR / "widow_face_ref.png"))
R_BIER = Ref(
    "the open hand-bier with the shrouded form on it -- its exact wooden form and the wrapped body",
    str(REFS_DIR / "bier_ref.png"),
)
R_BIER_GROUNDED = Ref(
    "the open hand-bier, set down and resting on its own low X-braced trestle-leg frame at each "
    "end -- its exact grounded construction, cropped from F03's own approved render",
    str(REFS_DIR / "bier_grounded_ref.png"),
)
R_GATE = Ref("the gate of Nain -- its exact drystone posts and timber lintel", str(REFS_DIR / "gate_ref.png"))
R_SON = Ref("the widow's son, alive -- his face, build, and dress", str(REFS_DIR / "son_ref.png"))

# ===========================================================================
# F01 -- "Everyone kept their distance"  (narration: "The law was simple:
# touch a dead man, and you were unclean. Everyone kept their distance.
# That was survival, not cruelty.")
# The Stain's own establishing shot. Triple debut (widow, bier, gate) --
# renders unpinned, sources five ref crops. Camera is a MEDIUM shot
# deliberately, not wide, so the widow's face crops clean for widow_face_ref.
# ===========================================================================
F01 = PageSpec(
    seq_title="THE BIER HE TOUCHED",
    frame_label="F01",
    panels=(
        Panel("kept their distance",
              "a doorway in a village wall, a householder drawn back deep into its shadow, "
              "watching the road pass"),
        Panel("water of separation",
              "a plain clay vessel of water with a sprig of hyssop laid across its mouth"),
        Panel("outside the walls",
              "dark rock-cut tomb openings in a bare hillside, small and unadorned"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        "the dusty road just outside the gate of Nain -- the low drystone-and-mud-brick wall and "
        f"timber-lintel gate rising at the frame's edge, fully inside the frame. {BIER_BUILD}, "
        "borne shoulder-high past the viewer by four bearers in plain undyed and ochre wool, "
        "their heads bowed, their faces turned down toward the poles, none of them individuated "
        f"or finished; lying full-length on the bier's open top, {SON_SHROUDED}, fully inside the "
        f"frame. Close behind the bier, {WIDOW_BUILD}, fully inside the frame, walking with her "
        "eyes down, one hand holding her rent mantle closed at the breast, her face lined with "
        "weeping; her contour drawn steady and single-struck, no doubled or tremored line "
        "anywhere in her figure. At the road's edges, villagers drawn back off the road -- "
        "figures pressed to the walls and standing in halted clusters, a wide band of bare empty "
        "ground between every one of them and the bier, no one within arm's reach of it but the "
        "bearers and the widow. A cold grey-umber stain lies in the paper itself beneath the bier "
        "and the bare ground around it, formless and matte, its feathered damp edge crossing the "
        "drawn frame border into the page's own lower margin directly below the bier, never over "
        "any face, bounded to less than a third of the page; its edge stops short of every living "
        "figure, a band of clean paper between the stain and the widow, the bearers' feet, and "
        "every villager. Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page "
        "-- no blue ink appears anywhere in the scene, the panels, or the margins."
    ),
    material_closer=(
        "the cold stain lying in the paper beneath the bier is the only unusual ink at work on "
        "this page, and no blue appears anywhere."
    ),
    panel_motions=(
        "the shadow inside the doorway deepens very slightly, nothing else changes",
        "the light across the clay vessel warms softly and settles",
        "a thin haze drifts across the hillside before the tomb openings",
    ),
    main_scene_animation=(
        "the bearers and the bier continue their slow, even funeral pace along the road, one "
        "continuous unhurried walk; the widow walks with them at the same pace, her eyes staying "
        "down, her mantle stirring faintly; the shrouded form lies completely still on the bier, "
        "exactly as drawn, no rise or fall of breath, for the whole clip; every villager at the "
        "road's edges stays exactly as drawn, held in their drawn-back stillness; the cold stain "
        "in the paper stays exactly as drawn, never deepening, never spreading, never fading;"
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain in the paper beneath the bier",
    caption_lines=("and you were unclean",),
    corner_note="NOTE: survival, not cruelty",
    refs=[],
    model_tier="veo3_1_lite",
    clip_duration=6,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F02 -- "Weep not"  (narration: "Jesus walked toward her instead of away.
# And when the Lord saw her, he had compassion on her, and said unto her,
# 'Weep not.'")
# Jesus enters; the first blue enters with him, from the hand that will do
# the touching. AT-CAP page (Stain D3 + Swirl Stage 1 = 4) -- full QUAD lock.
# ===========================================================================
F02 = PageSpec(
    seq_title="THE BIER HE TOUCHED",
    frame_label="F02",
    panels=(
        Panel("he saw her", "a close study of the widow's tear-lined eyes beneath the dark veil"),
        Panel("toward, not away",
              "worn sandaled feet mid-stride on a dusty road, the hem of a plain cream-brown robe "
              "above them"),
        Panel("two crowds met",
              "two streams of small figures converging on one road outside a gate, seen far off"),
    ),
    still_shot_type="MEDIUM TWO-SHOT",
    anim_shot_desc="medium two-shot",
    main_scene_still=(
        f"the road before the gate of Nain. {JESUS_BUILD}, fully inside the frame, standing in "
        "the procession's path facing the widow, his gaze on her, his right hand half-lifted "
        f"toward her, palm gently open, already raised, not touching anything; {WIDOW_BUILD}, "
        "fully inside the frame, stopped before him, her tear-lined face lifting toward his, one "
        "hand still holding her rent mantle closed; her contour drawn steady and single-struck, "
        "no doubled or tremored line anywhere in her figure. Behind and beside them, the open "
        "wooden hand-bier held steady on the four bearers' shoulders, the shrouded form with its "
        "napkin-bound face lying on its open top, never a coffin, never any lid, fully inside the "
        "frame; the halted crowds drawn as unindividuated hatched masses beyond. The cold "
        "grey-umber stain lies in the paper beneath the bier, unchanged from before, still "
        "crossing the drawn frame border into the lower margin, never over any face, a band of "
        "clean paper between the stain and every living figure, the stain nowhere near Jesus and "
        "never beneath his figure or his feet. Stage 1 dosage: exactly one restrained thread of "
        "blue ink curling up from the back of Jesus's half-lifted right hand, touching only his "
        "hand and the air just above it, the only blue on the whole page, behaving like one "
        "stroke of wet ink bled into the paper, smooth and open in its curl, never blot-shaped; "
        "the stain formless and matte, never swirl-shaped; a wide band of untouched clean paper "
        "between the thread and the stain at every point, the thread drawn ON the page's surface, "
        "the stain lying IN the paper beneath the linework."
    ),
    material_closer=(
        "the cold stain in the paper and the single blue thread at his hand are the only two "
        "kinds of unusual ink at work on this page, kept apart by clean paper."
    ),
    panel_motions=(
        "the sketched eyes hold, the light across the study warming very slightly",
        "a thin banner of dust drifts low across the road behind the sandaled feet",
        "the two far crowd-streams hold, a faint heat-shimmer over the road between them",
    ),
    main_scene_animation=(
        "the widow's tear-lined face completes its lift and her eyes settle on Jesus, finishing "
        "early and holding still; Jesus stays exactly as drawn, his half-lifted hand not rising "
        "further and not reaching toward anything, one slow steady breath, his lips staying "
        "closed and completely still -- he is not speaking and his mouth does not move at all; "
        "the bearers hold the bier perfectly steady; the shrouded form lies completely still, "
        "exactly as drawn, no rise or fall of breath; the single thin blue ink thread at his hand "
        "stays exactly as drawn, in place, for the whole clip; the cold stain in the paper stays "
        "exactly as drawn, never deepening, never spreading, never fading;"
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain in the paper beneath the bier and the single blue thread at his lifted hand",
    caption_lines=("Weep not",),
    corner_note="NOTE: toward, not away",
    refs=[R_JESUS, R_WIDOW, R_WIDOW_FACE, R_BIER, R_GATE],
    model_tier="kling3_0",
    clip_duration=7,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F03 -- "And touched the bier"  (narration: "Then he touched what no one
# else would touch: and he came and touched the bier, and they that bare
# him stood still.")
# The title act. Contact is drawn as already made -- no clip ever shows the
# hand arriving. Panel 2 is the deliberate seed of empty_bier_ref (§8).
# ===========================================================================
F03 = PageSpec(
    seq_title="THE BIER HE TOUCHED",
    frame_label="F03",
    panels=(
        Panel("stood still",
              "four pairs of sandaled feet halted mid-stride on the dusty road, close, low dust "
              "settling around them"),
        Panel("the open bier",
              "a small object study of the hand-bier empty: bare boards, two poles, no lid, drawn "
              "plain"),
        Panel("unclean until even",
              "a lone small figure seated apart from a village wall under a low sun"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        "the road before the gate -- the bearers having set the bier down to rest directly on the "
        "bare ground, BOTH of its two long poles lying flat and level along the ground running the "
        "bier's own full length, resting on the earth their entire visible length, from end to "
        "end, with no gap or lift anywhere -- no pole, rail, or part of the bier is held up, "
        "gripped, or carried at hand height, chest height, or shoulder height by anyone, no wooden "
        "part of the bier floats or hovers apart from the rest of it, all its wooden parts touching "
        "the ground together, connected and continuous. The bier is still completely FLAT and "
        "OPEN, exactly as before -- a bare plain plank with no raised edge, wall, lip, or rim of "
        "any kind along any of its four sides, front, back, left, or right -- never a coffin, never "
        "a casket, never a crate, never a box, never a tray, never a cradle with sides, the wrapped "
        "body lying fully exposed and visible from directly above with absolutely nothing enclosing "
        "or bordering it on any side -- setting the bier down on the ground changes ONLY its "
        "height, never its flat open shape -- its plank resting low and level just above "
        "the dust -- never on built-in legs, a table, a bench, or any raised stand, the "
        f"bier's own bare wood the only thing touching the ground. {JESUS_BUILD}, fully inside the "
        "frame, standing at the side of the grounded bier, bending slightly toward it, his right "
        "hand laid flat and full on the bier's wooden side rail, palm down, in complete unbroken "
        "contact with the wood, fully inside the frame -- the hand and the rail touching with no "
        "gap between them; the four bearers standing upright beside the grounded bier, their own "
        "hands empty and open at their sides, not touching the bier anywhere, no longer bearing "
        "its weight, their heads turned toward him, watching, none of their faces "
        f"individuated or finished; {SON_SHROUDED}, lying "
        "full-length on the bier's open top, fully inside the frame; "
        f"{WIDOW_BUILD} a step behind, her hands risen toward her mouth, her contour drawn steady "
        "and single-struck, no doubled or tremored line anywhere in her figure. The cold "
        "grey-umber stain lies in the paper beneath the bier, still crossing the drawn frame "
        "border into the lower margin on the side away from Jesus, never over any face -- but its "
        "whole edge nearest his touching hand has dried to a pale ring, the wet remainder lying "
        "only toward the bier's far end, away from him; no stain of any kind on Jesus's figure, "
        "hand, sleeve, or the paper beneath him -- his side of the page the cleanest paper on it. "
        "Stage 1 dosage, held: the same single restrained thread of blue ink, now rising thin "
        "from the back of his right hand where it rests on the rail, straight up, touching only "
        "his hand and the air above it, the only blue on the whole page, behaving like one stroke "
        "of wet ink bled into the paper, a wide band of untouched clean paper between the thread "
        "and the stain's wet remainder at every point."
    ),
    material_closer=(
        "the stain dying back from his hand and the single blue thread rising from it are the "
        "only two kinds of unusual ink at work on this page, kept apart by clean paper."
    ),
    panel_motions=(
        "the settling dust around the halted feet thins and stills",
        "the empty bier study holds, the light across its boards warming very slightly",
        "the lone figure holds, seated apart, unmoving",
    ),
    main_scene_animation=(
        "Jesus's head bows slightly toward the shrouded form and stills, finishing early and "
        "holding -- his hand staying laid flat on the rail exactly as drawn, pressing without "
        "moving, never lifting, never sliding; the bearers stand upright and still beside the "
        "grounded bier, exactly as drawn, each one slow breath; the bier itself stays resting on "
        "the ground exactly as drawn, its poles never lifting; the shrouded form lies completely "
        "still, exactly as drawn, no rise or fall of breath; the widow's raised hands tremble "
        "faintly and still; the single thin blue ink thread at his hand stays exactly as drawn, "
        "in place, for the whole clip; the stain and its dried pale edge stay exactly as drawn, "
        "never deepening, never spreading, never fading;"
    ),
    fence_kind="stain",
    fence_callout="the cold grey-umber stain in the paper beneath the bier, its dried pale edge, and the single blue thread at his hand",
    caption_lines=("and touched the bier",),
    corner_note="NOTE: the flow reverses",
    refs=[R_JESUS, R_BIER, R_WIDOW, R_WIDOW_FACE, R_GATE],
    model_tier="kling3_0",
    clip_duration=7,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F04 -- "Arise"  (narration: "Under that same law, the touch should have
# made him unclean. It didn't work that way with him. And he said, 'Young
# man, I say unto thee, Arise.'")
# The doctrinal pivot and the crossing point (swirl == stain, first equality).
# AT-CAP page (Stain D2 + Swirl Stage 2 = 4) -- full QUAD lock, kept per the
# user's confirmed choice (matches episode 12's own proven at-cap shape).
# ===========================================================================
F04 = PageSpec(
    seq_title="THE BIER HE TOUCHED",
    frame_label="F04",
    panels=(
        Panel("the old remedy",
              "the same plain clay vessel of water with its hyssop sprig, unused, exactly as F01's "
              "panel drew it"),
        Panel("the bound napkin",
              "a close study of the folded linen napkin bound over the face, its knot and folds"),
        Panel("her clasped hands", "the widow's hands clasped tight at her lips, close"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        "close along the side of the bier, resting exactly as it was set down in the previous "
        "scene -- the SAME simple low wooden trestle-leg frame at each end (crossed X-braced legs, "
        "tied at the crossing, holding the plank a short distance clear of the dust), the plank "
        "itself flat, open, and bare, no raised side walls, no coffin, no box, matching that "
        f"construction exactly. {JESUS_BUILD}, fully inside the "
        "frame, standing at the bier's head end, bending slightly toward it, his right hand "
        "resting on the wooden rail, his face turned down toward the shrouded form, calm, "
        "unhurried, his gaze steady on the "
        f"napkin-bound face; {SON_SHROUDED}, lying full-length on the open boards, fully inside "
        "the frame; two of the bearers standing upright beside the grounded bier, no longer "
        "bearing its weight, heads turned, unfinished faces; "
        f"{WIDOW_BUILD} beyond the bier, gripping the rent edge of her mantle, watching, her "
        "contour drawn steady and single-struck, no doubled or tremored line anywhere in her "
        "figure. Of the cold grey-umber stain in the paper, only a narrow wet remainder is left, "
        "lying directly beneath the bier's head end; all the rest of its former reach -- "
        "including where it once crossed the drawn frame border into the margin -- has dried to "
        "a pale ring; never over any face, no stain anywhere on Jesus or the paper beneath him. "
        "Stage 2 dosage: the blue ink motif quietly present -- a few soft blue threads and one "
        "small rounded watercolor bloom rising from the back of his hand on the rail into the air "
        "above it, the bloom a soft blurred stain of pigment with no stem, no petals, no wings, and "
        "no leaf shape, never a literal flower, insect, or butterfly, and no sparkle, glint, or "
        "star-point of any kind anywhere on the page, touching only his hand and the air, touching "
        "no other person and nothing else on the page, every thread behaving like wet ink bled "
        "into the paper, smooth and open, never blot-shaped; the stain remainder formless and "
        "matte, never swirl-shaped; a wide band of untouched clean paper between the threads and "
        "the stain remainder at every point, the threads drawn ON the page, the stain lying IN the "
        "paper beneath the linework."
    ),
    material_closer=(
        "the last narrow remainder of the stain and the soft blue threads at his hand are the "
        "only two kinds of unusual ink at work on this page, kept apart by clean paper."
    ),
    panel_motions=(
        "the light across the clay vessel warms softly and settles",
        "the napkin study holds, its folds exactly as drawn, nothing stirring",
        "her clasped hands press once slightly tighter and still",
    ),
    main_scene_animation=(
        "Jesus stays exactly as drawn, his hand resting on the rail without moving, one slow "
        "steady breath, his lips staying closed and completely still -- he is not speaking and "
        "his mouth does not move at all; the shrouded form lies completely still, exactly as "
        "drawn, no rise or fall of breath, no stir anywhere in the linen, for the whole clip; the "
        "widow's grip on her mantle's edge tightens once and stills; the bearers stand upright and "
        "still beside the grounded bier, exactly as drawn; the bier itself stays resting on the "
        "ground exactly as drawn, its poles never lifting; the soft blue threads at his hand drift "
        "gently within their own small area, never "
        "spreading beyond his hand and the air above it; the stain remainder and its dried ring "
        "stay exactly as drawn, never deepening, never spreading, never fading;"
    ),
    fence_kind="stain",
    fence_callout="the narrow wet remainder of the stain beneath the bier's head, its dried pale ring, and the blue threads at his hand",
    caption_lines=("I say unto thee,", "Arise"),
    corner_note="NOTE: no stain on him",
    refs=[R_JESUS, R_BIER_GROUNDED, R_WIDOW, R_WIDOW_FACE],
    model_tier="kling3_0",
    clip_duration=9,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F05 -- "He that was dead sat up"  (narration: "And he that was dead sat
# up, and began to speak. And he delivered him to his mother.")
# The miracle page -- the change happens entirely between F04 and F05, never
# on camera. Ref-crop page for son_ref.
# ===========================================================================
F05 = PageSpec(
    seq_title="THE BIER HE TOUCHED",
    frame_label="F05",
    panels=(
        Panel("the bands loosed",
              "the linen grave-bands lying slack and unwound across the bier's boards"),
        Panel("his eyes open", "a close study of the boy's living eyes, open, unlined, light in them"),
        Panel("to his mother",
              "two pairs of hands meeting: an older woman's hands clasping a young man's hand "
              "between them"),
    ),
    still_shot_type="MEDIUM WIDE shot",
    anim_shot_desc="medium wide shot",
    main_scene_still=(
        "the road before the gate, the bier still borne on the four bearers' shoulders. "
        f"{SON_BUILD}, alive, his eyes open -- SITTING FULLY UPRIGHT on the open bier's boards, "
        "already risen to a seated position, his face turned toward his mother, his lips closed; "
        f"fully inside the frame. {JESUS_BUILD}, fully inside the frame, standing at the bier's "
        "side, his right hand now lifted open toward the widow in a small presenting gesture -- "
        f"giving him back; {WIDOW_BUILD}, fully inside the frame, her arms opening toward her "
        "son, not yet reaching him, her tear-lined face breaking from grief into astonishment; "
        "her contour drawn steady and single-struck, no doubled or tremored line anywhere in her "
        "figure. The bearers still under the poles, faces turned up toward the risen boy, awe in "
        "their unfinished faces; the halted crowds beyond, drawn as hatched masses. Of the stain, "
        "nothing wet remains anywhere: only the dried pale ring lies in the paper where the stain "
        "once sat beneath the bier, and the paper inside that ring is the cleanest cream on the "
        "whole page; no border crossing remains but a pale dried trace. Stage 2 dosage, held: a "
        "few soft blue threads and one small rounded watercolor bloom rising from the back of "
        "Jesus's lifted hand into the air above it, the bloom a soft blurred stain of pigment with "
        "no stem, no petals, no wings, and no leaf shape, never a literal flower, insect, or "
        "butterfly, and no sparkle, glint, or star-point of any kind anywhere on the page, "
        "touching only his hand and the air, touching no other person, every thread behaving like "
        "wet ink bled into the paper, a band of clean paper between the threads and the dried ring."
    ),
    material_closer=(
        "the dried pale ring in the paper and the soft blue threads at his lifted hand are the "
        "only two kinds of unusual mark on this page, and the paper inside the ring is the "
        "cleanest on it."
    ),
    panel_motions=(
        "the slack grave-bands lie undisturbed, exactly as drawn",
        "the sketched living eyes blink once fully -- closing, then opening again fully, ending "
        "wide open",
        "the clasped hands hold, the light across them warming very slightly",
    ),
    main_scene_animation=(
        "the boy's chest rises and falls in slow visible breathing -- the first breath on any "
        "bier page -- his head turning the last small distance toward his mother and settling, "
        "his lips staying closed and completely still, not speaking, his mouth never moving; the "
        "widow's opening arms complete the last small part of their opening and hold, not yet "
        "reaching him; Jesus stays exactly as drawn, his lifted hand not moving further, one slow "
        "steady breath, lips closed and completely still; the bearers hold the bier perfectly "
        "steady; the soft blue threads at his hand drift gently within their own small area; the "
        "dried pale ring stays exactly as drawn, and no new stain, spot, or darkening appears "
        "anywhere on the page at any point;"
    ),
    fence_kind="stain",
    fence_callout="the dried pale ring in the paper beneath the bier",
    caption_lines=("he that was dead", "sat up"),
    corner_note="NOTE: given back",
    refs=[R_JESUS, R_BIER, R_WIDOW, R_WIDOW_FACE],
    model_tier="kling3_0",
    clip_duration=6,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F06 -- "Life spread from Jesus to the boy"  (narration: "Death didn't
# spread from the boy to Jesus. Life spread from Jesus to the boy.")
# The thesis page, drawn as homecoming through the same gate death was
# carried out of. The episode's one Stage 3 page. Uses R_BIER (with-body ref)
# plus a text override for the empty state (see module docstring's fix note --
# the panel-crop empty_bier_ref attempt was abandoned, defective render).
# ===========================================================================
F06 = PageSpec(
    seq_title="THE BIER HE TOUCHED",
    frame_label="F06",
    panels=(
        Panel("a great prophet",
              "a cluster of small figures with arms lifted in praise, seen from behind"),
        Panel("the tombs behind",
              "the rock-cut tomb openings on the hillside, the road past them empty and untraveled"),
        Panel("home again",
              "a warm-lit open doorway inside the village, a low table laid, no figures"),
    ),
    still_shot_type="WIDE shot",
    anim_shot_desc="wide shot",
    main_scene_still=(
        "the gate of Nain from outside, the low drystone-and-mud-brick wall and timber lintel "
        "fully inside the frame, the lane through it climbing between the small flat-roofed "
        "houses on the slope. The crowd streaming IN through the gate toward home, drawn as one "
        "glad unindividuated hatched mass; at its heart, fully inside the frame, the widow and "
        "her son walking side by side, her arm wrapped through his, his loosened grave-bands "
        "traded for a plain borrowed mantle about his shoulders, both their contours drawn steady "
        f"and single-struck; {JESUS_BUILD}, fully inside the frame, walking among them at the "
        "same unhurried pace, unremarkable in the crowd; leaning upright against the wall's outer "
        "face beside the gate, small in the midground, the open hand-bier now empty, no body on "
        "it, its bare boards and two poles plain and flat, the linen lying folded on its boards, "
        "never a coffin, never a casket, never a box, never any raised side walls, never any lid, "
        "fully inside the frame. No stain, ring, or grey blot anywhere in "
        "the paper -- the paper wholly clean. Stage 3 dosage: the blue ink motif, with traces of "
        "muted gold, is woven through the whole scene -- threads drifting in one loose open band "
        "through the air of the road and the gate's opening, above every head, touching no "
        "person, tied to no single figure, behaving like wet ink bled through the page's own sky "
        "wash, never a glow."
    ),
    material_closer=(
        "the blue-and-gold band woven through the air is the only unusual ink on the page, and "
        "the paper beneath it is wholly clean."
    ),
    panel_motions=(
        "the lifted arms hold their praise, unmoving, the light across them warming",
        "a thin haze drifts across the hillside before the tombs",
        "the doorway's warm light stays exactly as warm and steady as it already is, unchanged",
    ),
    main_scene_animation=(
        "the crowd continues its slow glad walk in through the gate at an even pace; the widow "
        "and her son walk with them, her arm keeping its hold through his, neither turning; Jesus "
        "walks among them at the same even pace; the blue-and-gold ink threads drift smoothly "
        "within their own fixed band across the air above the road, never lowering onto any "
        "figure; the empty bier leans motionless against the wall, exactly as drawn;"
    ),
    fence_kind="none",
    caption_lines=("Life spread from Jesus", "to the boy"),
    corner_note="NOTE: the other direction",
    refs=[R_JESUS, R_WIDOW, R_WIDOW_FACE, R_SON, R_GATE, R_BIER],
    model_tier="veo3_1_lite",
    clip_duration=6,
    panel_style="woodcut_hybrid",
)

PAGES = {"f01": F01, "f02": F02, "f03": F03, "f04": F04, "f05": F05, "f06": F06}

# ---- covers -------------------------------------------------------------
# Neither cover carries Jesus (deliberate -- the narration's hook doesn't name him
# yet, and the empty bier on the back says what he did more loudly than his figure
# would). Both belong to the title object in its two states.

FRONT_COVER = CoverSpec(
    side="front",
    scene=(
        "the funeral procession emerging through the gate of Nain, small and isolated in the "
        "lower third: four bearers carrying the open hand-bier shoulder-high -- a bare flat plank "
        "with no raised edge, wall, rail, or rim of any kind along any of its four sides, front, "
        "back, left, or right, never a coffin, never a casket, never a box, never a crate, never a "
        "cradle with sides, never a lid -- the shrouded form lying fully exposed on its open top "
        "with absolutely nothing enclosing or bordering it on any side, the form openly "
        "visible; the widow walking close behind it, veiled, her rent mourning mantle drawn about "
        "her; behind her, the village crowd following out of the gate; the low "
        "drystone-and-mud-brick wall and timber-lintel gate rising behind them, the small "
        "flat-roofed houses of Nain stacked on the hill's slope above; the dusty road running "
        "down the open slope ahead of the procession toward scattered dark rock-cut tomb openings "
        "in the hillside -- the destination visible, the walk already begun."
    ),
    lighting=(
        "Low hard morning light breaking warm ochre-gold across the hillside, the village "
        "rooftops, and the dusty road, against cold slate blue-grey shadow holding the gate's "
        "opening, the wall, and the dark-clothed procession itself, cinematic atmospheric haze, "
        "dramatic volumetric light rays, photographic tonality."
    ),
    background_detail="",
    title="THE BIER HE TOUCHED",
    subtitle="LUKE 7",
    title_position="top",
    animation=(
        "the procession continues its slow, even funeral pace forward along the road -- one "
        "continuous unhurried walk, no figure turning or stopping; the widow's veil and mantle "
        "stir faintly as she walks; the morning light stays exactly as warm and low as it already "
        "is, unchanged; the gate, wall, and tombs stay exactly as drawn"
    ),
    extra_avoid="coffin, casket, closed box, crate, cradle with side rails, raised side walls or railing on the bier, lid, visible dead face, gore, skeletal figures, modern funeral clothing",
    refs=[R_WIDOW, R_BIER, R_GATE],
    clip_duration=8,
)

BACK_COVER = CoverSpec(
    side="back",
    scene=(
        "dawn, outside the gate of Nain; the open hand-bier EMPTY, its plank flat and shallow with "
        "no raised side walls of any kind, never a box, never a crate, never a coffin, leaning "
        "upright at a slight angle against the drystone wall beside the gate opening, its two "
        "carrying poles bare; lying folded in a neat small pile on its bare boards, the linen "
        "grave-bands and, set on "
        "top of them, the linen napkin folded together by itself; the road down toward the "
        "rock-cut tombs empty and untraveled; through the gate's opening, the lane into the "
        "village just catching light."
    ),
    lighting=(
        "Warm dawn gold pouring OUT through the gate's opening from the village side, falling "
        "across the bier's boards and the folded linen; cold blue-grey night shadow still holding "
        "the downhill road and the tomb-pocked slope, cinematic atmospheric haze, photographic "
        "tonality."
    ),
    background_detail=(
        "One small hard-capped closed curl of blue ink with a trace of muted gold rises from the "
        "folded napkin on the boards, its whole visible length no longer than a hand's width, "
        "curled into one small closed loop, never straightening, never trailing, behaving like a "
        "small dab of living ink, never a glow."
    ),
    title="IT BECAME A HOMECOMING",
    subtitle="NUMBERS 19:11",
    title_position="bottom",
    animation=(
        "fine dust motes drift slowly through the shaft of dawn light in the gate's opening; one "
        "loose edge of the folded linen stirs faintly and settles; the blue-gold curl stays "
        "exactly as drawn, in place, for the whole clip; the dawn light stays exactly as warm and "
        "low as it already is, unchanged"
    ),
    extra_avoid="coffin, casket, closed box, crate, raised side walls or tray shape, lid, skeleton, bones, any human figure",
    refs=[R_BIER, R_GATE],
    clip_duration=8,
)

COVERS = {"front": FRONT_COVER, "back": BACK_COVER}

# ---- assembly manifest ---------------------------------------------------
# Word weights are Fable's own count against the locked narration (sum 186, matching
# narration.md's real word count; 69.0s locked audio). Boomerang nowhere in this
# episode -- every unit either walks (directional locomotion), settles a completing
# gesture, or drifts motes (back cover) -- all of which read backwards under reversal.
# Final modes are an assembly-QC call on the real renders, per the standing rule.

MANIFEST = EpisodeManifest(
    episode_dir=HERE,
    narration=HERE / "narration.mp3",
    units=[
        Unit("front", HERE / "front_cover.mp4", 23, "freeze"),
        Unit("f01", HERE / f"{HERE.name}_f01_9x16.mp4", 21, "freeze"),
        Unit("f02", HERE / f"{HERE.name}_f02_9x16.mp4", 24, "freeze", tail_loop_seconds=1.0),
        Unit("f03", HERE / f"{HERE.name}_f03_9x16.mp4", 23, "freeze", tail_loop_seconds=1.0),
        Unit("f04", HERE / f"{HERE.name}_f04_9x16.mp4", 28, "freeze", tail_loop_seconds=1.0),
        Unit("f05", HERE / f"{HERE.name}_f05_9x16.mp4", 18, "freeze", tail_loop_seconds=1.0),
        Unit("f06", HERE / f"{HERE.name}_f06_9x16.mp4", 15, "freeze"),
        Unit("back", HERE / "back_cover.mp4", 34, "freeze"),
    ],
    scores={
        # Felt-piano identity reused near-verbatim from episode 5/8/Naaman (the series
        # default), re-timed to this episode's own arc. Duck profile starts from the
        # Barrel's own working values -- re-measure against the real mixed output
        # before calling this final, per this project's own "a duck does not transfer
        # between score generations" rule.
        "piano": ScoreVariant(
            score=HERE / "score_piano.mp3",
            duck=DuckProfile(gain_db=-6, threshold=0.12, ratio=2.5, release_ms=250),
            out=HERE / f"{HERE.name}_final_piano.mp4",
        ),
    },
    panel_style="woodcut_hybrid",
)
