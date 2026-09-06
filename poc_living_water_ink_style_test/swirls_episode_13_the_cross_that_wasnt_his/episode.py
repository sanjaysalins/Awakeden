"""Episode spec for "The Cross That Wasn't His" (Mark 15:20-21 + Luke 23:26,
Simon of Cyrene compelled to carry Jesus's cross; read through Hebrews
13:11-13's sin-offering typology -- "without the camp" -> Jesus "suffered
without the gate" -> "let us go forth therefore unto him"). Dead ink: NONE --
no Stain, no Fray, on any page (nobody in this text is marked unclean,
guilty, or wavering; a stain on Simon would say "guilty," exactly the
doctrine error the narration's own fence exists to prevent). NT episode,
Jesus bodily in frame on the gate pages (F01-F03, F06) and present only as a
small led figure ahead on the road pages (F07, F09), absent from F04-F05 and
F08 -- this episode's human protagonist is Simon, and Jesus is present
mostly by direction (he went out first). Stage 3 begins on the camera-turn
cut (F06->F07) and completes on F09. panel_style woodcut_hybrid throughout.
Voices: narrator only (voices.json -- every KJV line is narrator-read; lips
stay closed on every figure on every clip).

Design authored by Fable (full brief: `_DESIGN_BRIEF.md` in this folder),
implemented by Sonnet per the "Fable designs, Sonnet executes" rule. The
user confirmed two open calls (brief section 8): Simon of Cyrene = the
plain/generic build (sun-browned countryman, no ethnic marker -- the ep11
Samaritan reverence-guard pattern, §8 Q18); hero page = F06 (Hebrews 13:12,
"suffered without the gate," Christ's own atoning act named, Jesus a pace
ahead of the man who follows him out -- the gospel pivot, not the emotional
climax which is F02/F03; §8 Q14). Every OTHER open question in the brief's
section 8 is resolved here using Fable's own stated recommendation:
front title = the episode title (Q1, mandatory 2x-zoom check on the
apostrophe -- fallback WALKING THE OTHER WAY if it renders as a pasted
glyph); seq_title = WITHOUT THE GATE (Q2); back title/subtitle = THROUGH
THAT GATE FIRST / HEBREWS 13:13 (Q3); a plain BEAM, never a crucifix shape
(Q4, SUPERSEDED 2026-09-06 v3 -- see CROSS_BUILD's own comment: reversed to
the traditional full cross by explicit user decision, for legibility); no
crown of thorns, restraint (Q5); Jesus carries the beam on F01
(Q6); debut page = F04 (Q7); seedream-4-5 scoped to F08 only (Q8); NOTE:
Hebrews 13 corner note kept, fallback NOTE: the sin offering (Q9); F08's
5-word caption kept (Q10).

THE THREE HARD PROBLEMS (full reasoning in _DESIGN_BRIEF.md section 2):

1. Three citations from three books (Mark, Luke, Hebrews) stacked in under
   forty seconds -- the independent-review panel flagged a cold ear loses
   the thread between the Levitical sin-offering explanation and its
   Hebrews attribution. Fixed by a REGISTER rule: the Old-Testament type
   lives ONLY in the carved woodcut panels (F05's row, F06 panel 1), the
   road/event lives ONLY in the washed main scene, and the address to the
   viewer is carried by the camera itself turning to look out along the
   road (F07-F09) -- plus a `NOTE: Hebrews 13` corner note on F05 doing by
   eye the attribution the ear lost.

2. "Outside is 'without'" is a lesson about a WORD, not stageable as
   action. Fixed on F04: three panels are one doorway seen from inside, at
   the threshold, and from outside, labeled inside/the gate/without, under
   the caption "outside is without" -- the equation done by adjacency.

3. Simon's carrying must picture REPROACH and never re-enact the atonement
   (two reviewers heard the risk in the words alone). Fixed by seven locked
   drawing rules on every page the cross appears: a plain rough cross (see
   CROSS_BUILD's v3 note -- SUPERSEDED 2026-09-06 from a crucifix-avoiding
   crossbeam-only design; the risk this rule guards against is ornamentation
   and the atonement's OWN iconography -- a corpus, a plaque, a halo, gilding
   -- not the cross shape itself, which the user confirmed should be drawn
   plainly); nothing ever on the wood (no nails/rope/inscription/corpus/
   blood); the SOLDIERS lay it on him, never Jesus; no execution place ever
   in frame; no mark of any kind on Simon; the living ink never on the cross
   or the man who carries it; Jesus under the cross (F01 only) keeps the
   series' restraint (own clothes, bare head, no crown, no wounds).

The swirl's anchor is the gate's THRESHOLD STONE (not a hand, as in
ep7/ep10/ep11 -- Jesus's hands are on the beam on F01 and he is a led,
ahead figure from F02 on; the beam and Simon are both fence-forbidden
anchors). One thread rises from the stone under Simon's lifting heel on
F03 (the gospel turn -- swirl > 0 for the first time as Simon faces the
way Christ went, not when he is loaded and not when he understands), a
contained doorway bloom holds through F04-F06 while Hebrews explains what
crossing the stone meant, and the ink leaves the gate on the camera-turn
cut (F06->F07) to fill the open air above the road for the final three
pages -- "Hebrews turns to you" and the life opening outward read as one
event on that one cut.

DIRECTION is this episode's literalism trap (the Barrel's "barrel", ep11's
"ten"): Jesus faces/moves RIGHT (out) on every page he is on; Simon faces
LEFT (in) on the front cover, F01, and F02, and RIGHT (out) from F03 on --
the page cut F02->F03 IS Simon's turn, never drawn inside a clip (LAW 1).
The eye-QC checklist reads direction FIRST on every page, before anything
else.

Provider note: this episode renders entirely through the OpenArt bridge.
There is no veo model under OpenArt -- `model_tier` below is advisory only
(stated per page as the ideal lane, exactly as the brief reasons it); every
clip actually renders on Kling 3 Omni via `render_animation()`'s openart
branch unless the user explicitly sets SWIRLS_GEN_PROVIDER=hf for a single
clip. `still_model` is a real per-page choice (locked 2026-09-05 tiering):
nano-banana-pro is used everywhere except F08, the one calm single-figure
close-up where every ref is already chained and no other figure is in
frame to leak a mark onto -- the validated seedream-4-5 case.
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

# LOCKED series-wide, reused verbatim from episode 10/11. jesus_ref.png copied
# verbatim into this episode's refs/ -- no redesign, no new approval cycle.
JESUS_BUILD = (
    "Jesus, a Judean man in his early thirties, medium height and ordinary build, sun-browned "
    "skin, shoulder-length dark brown hair pushed back from his face, a short full dark beard, "
    "wearing a simple ankle-length robe of undyed cream-brown wool with a plain olive-toned "
    "mantle draped over one shoulder, a narrow rope belt, and flat worn leather sandals -- no "
    "halo, no glow, nothing in his dress distinguishing him from the men around him, standing "
    "square, still, and unhurried, his gaze steady and direct"
)

# Per-page guard for every Jesus page in THIS episode (the Passion-prior trap): the
# model's prior for "Jesus + soldiers + cross + road" is the Via Dolorosa (crown of
# thorns, blood, a fall, a dragged cross, a wailing crowd). None of that is in these
# two verses. State this clause verbatim on every Jesus page.
JESUS_PASSION_GUARD = (
    "his head bare, no crown of thorns, no wounds or blood anywhere, no rope on his wrists, "
    "walking upright at an even pace, his face calm and set toward the road ahead, in his own "
    "clothes; a soldier's hand on his upper arm is the only hand on him; he touches no one on "
    "this page and never looks back"
)

# New to the series -- the human protagonist. User-confirmed: the plain/generic build (no
# ethnic marker), Fable's recommended default, per the ep11 Samaritan reverence-guard pattern
# (brief section 8, Q18). The one-figure-only-mark rule (2026-09-05) is applied twice in this
# build text -- the head-cloth and the rust-red stripe are HIS alone.
SIMON_BUILD = (
    "Simon of Cyrene, a broad-shouldered countryman of about forty, thick-armed and "
    "strong-backed from field work, deep sun-browned skin, a wide square face with a heavy "
    "jaw, a broad straight nose, calm dark eyes under level brows, a short dense black beard, "
    "close-cut black hair under a plain undyed head-cloth tied at the nape; wearing a "
    "knee-length coarse tunic of undyed oatmeal wool with a rope belt and a short mantle of "
    "undyed wool with one narrow rust-red stripe along its edge worn over his left shoulder, "
    "bare dusty legs, flat worn leather sandals; his ONLY distinguishing marks are the plain "
    "head-cloth and the single rust-red stripe, and no other figure on this page, including "
    "Jesus and the soldiers, ever wears a head-cloth or that rust-red stripe; drawn in the "
    "same steady, confident, single-struck line, with the same care, the same line weight, "
    "and the same dignity as every other figure on the page"
)

# The unburdened override for the two pages before the beam is laid on him (front cover,
# F01) -- the ep11 "lip-cloth now loosed" pattern: a text-line state change against a ref
# that carries the beam.
SIMON_UNBURDENED = (
    "his shoulders bare of any beam or burden, nothing carried, his hands empty and swinging "
    "at his sides as he walks"
)

# A shared GROUP identity, one LOOK ref, no individual faces (the ep11 ten_ref pattern).
SOLDIERS_BUILD = (
    "two Roman soldiers -- exactly two, count them, no more -- in short rust-brown tunics "
    "under plain leather-and-iron cuirasses, bare-legged, in hobnailed sandals; both helmets "
    "are a bare smooth dome of plain iron ending in a plain curved neck-guard at the back, "
    "the metal itself the only thing visible on top -- NO horsehair, NO feathers, NO brush, "
    "NO ridge, NO fin, NO decoration of any kind rising from or crossing the top of either "
    "helmet, not in red, not in any color, no cloak, no shield; one carries a short spear "
    "held upright, the other is empty-handed; drawn as ordinary working men doing an ordinary "
    "duty, their faces neither cruel nor kind, never caricatured, never sneering, in the same "
    "steady single-struck line as every figure on the page"
)

# The episode's title object, recurring F01-F09 (neither cover shows it: the front is
# before it, the back is after it).
#
# LOCKED 2026-09-06 v2 (user catch #1 -- "log not cross"): the FIRST version of this build
# described the object only by negation ("single plank... no cross shape") and never said
# what it actually WAS -- so every render that passed the no-cross-shape test did it by
# becoming a smooth, pale, generic carpentry plank ("a log"). Fixed with a POSITIVE identity
# (rough-hewn, weathered execution-equipment timber) -- but that fix, a historically-precise
# crossbeam-only (patibulum) reconstruction, created a SECOND legibility problem: a lone
# beam with no upright and no execution-ground context still just reads as carried lumber to
# an ordinary viewer, because nothing in frame signals "this is for crucifixion."
#
# LOCKED 2026-09-06 v3 (user catch #2 -- "but people always associate the whole cross"):
# reversed by explicit user decision. Mark 15:21/Luke 23:26 say Simon bore "his cross" (Gk
# stauros) without specifying beam-vs-whole-structure, so depicting the traditional full
# cross is textually safe, not just artistically convenient -- and it is what nearly every
# viewer already associates with "Simon carried the cross." Rather than keep fighting the
# model's own strong prior for a full Latin-cross shape (the entire earlier effort was
# suppressing that prior as a hallucination), this version leans into it: the object is now
# the WHOLE cross (crossbeam pegged to an upright), built with the same weathered,
# rough-hewn, institutional-execution-equipment material established in v2 -- only the
# shape changed, not the material research. Era/location/artifact check (standing
# validation item, not just this episode): does the object read as 1st-century Roman
# execution equipment -- rough, weathered, plainly joined -- NOT smooth modern lumber, NOT
# ornamented, NOT a crucifix icon (no corpus, no INRI plaque, no halo)?
CROSS_BUILD = (
    "the cross: a plain Roman execution cross and nothing else -- a full Latin-cross shape, "
    "one long upright timber taller than the man who carries it, reaching from the ground to "
    "well above his own head, with one shorter crossbeam fixed transversely across it near "
    "its top third, the two timbers joined at a plain right angle so the cross shape is "
    "immediately unmistakable; the two timbers are CLEARLY DIFFERENT LENGTHS, never equal -- "
    "the upright is visibly the LONGER of the two, extending well past the crossbeam at both "
    "ends (a long tail reaching down toward the ground, a shorter length rising above the "
    "crossbeam), while the crossbeam is the SHORTER timber, crossing the upright close to one "
    "end, not at the middle of either timber -- this is a Latin cross with a long-and-short "
    "pairing, explicitly NOT a symmetrical X or saltire shape where both arms are equal length "
    "and cross at their midpoints; concretely, shaped like a lowercase letter t, not like an X, "
    "a plus sign, or a St. Andrew's cross: the length of upright visible ABOVE the crossbeam is "
    "SHORT -- no longer than the crossbeam itself is wide -- while the length of upright BELOW "
    "the crossbeam is LONG -- at least three times that short upper length, reaching a long way "
    "down toward the ground; check this specific ratio before finishing the drawing: if the "
    "wood above and below the crossbeam looks anywhere close to equal, it is drawn wrong and "
    "must be redrawn with a much shorter top and a much longer bottom; both timbers roughly hewn by hand with an adze and axe, NOT "
    "finish-planed, NOT smooth, NOT clean modern dimensional lumber; the surface of both "
    "timbers visibly rough, scarred with adze and axe marks, weathered dark grey-brown and "
    "umber with age and long outdoor use, like government execution equipment reused many "
    "times over -- never fresh pale carpentry-shop lumber; the upright's lower end raw, "
    "deeply split, and worn dark from handling; the crossbeam's squared end passes through a "
    "plain rectangular mortise cut through the upright and is held with exactly ONE single "
    "small wooden peg, the same dark weathered wood-tone as the timbers themselves, flush "
    "with the surface, round or square, easy to miss at a glance -- there is NEVER a metal "
    "nail, NEVER a rivet, NEVER a bolt, NEVER a row or pair or cluster of multiple round "
    "fastener-heads anywhere on the joint or anywhere else on the wood; if you can count more "
    "than one single fastening point at the joint, or if any fastener reads as dark metal "
    "rather than the same wood-tone as the timber, it is drawn wrong -- a real, visible, "
    "working carpentry joint, nothing decorative, nothing ornamental; the "
    "crossbeam resting across the back of the shoulders behind the neck with both arms raised "
    "and the hands gripping it at either side, the long upright trailing back and down behind "
    "him along his spine, its lower end lifted just clear of the ground, never dragged, "
    "exactly like image reference 'the cross' shows, including its dark weathered color, "
    "rough adzed surface, and plain pegged joint, never lightened or smoothed toward clean "
    "pale wood, never ornamented, never gilded; no nails, no rope, no inscription, no corpus, "
    "no plaque, no blood, no fresh cut marks of any kind on the wood; dark aged umber-grey "
    "wood with no blue and no gold on it anywhere"
)

# The location of every profile page (F01-F06) and both covers -- deliberately NOT ep7's
# Nain gate (a different town, a different scale). LAW 3: no water anywhere -- the doorway
# holds the dose on four pages and a trough or pool is exactly the water feature that turns
# a thread into a pour.
GATE_BUILD = (
    "the gate of the city: a tall squared opening in a high wall of great dressed pale-gold "
    "limestone blocks, the doorway framed by a heavy stone lintel and two stone jambs, its "
    "timber doors standing open inward, one broad worn threshold stone lying across the "
    "doorway's foot; through the opening, a narrow shadowed lane climbing between tall "
    "flat-roofed stone houses; outside the gate, a dry dirt road running along the foot of "
    "the wall to the right and then away over a low stony rise into open country; the ground "
    "dry ochre earth and stone, no water, no pool, no cistern, no trough anywhere; no hill, "
    "no crosses, no crowd, and no place of execution visible anywhere"
)

# The location of the three camera-turned pages (F07-F09) -- no gate in frame, it is
# behind the viewer.
ROAD_BUILD = (
    "the same dry dirt road seen from behind, running straight away from the viewer's own "
    "feet over open stony country and up a long gentle rise to a far crest where it goes out "
    "of sight against the sky; dry ochre earth and scattered field-stones, thin dry grass, no "
    "wall, no building, no tree, no water of any kind; nothing visible beyond the crest -- no "
    "hill, no crosses, no crowd"
)

R_JESUS = Ref("Jesus -- his face, build, and dress", str(REFS_DIR / "jesus_ref.png"))
R_SIMON = Ref(
    "Simon of Cyrene -- his full figure, build, dress, head-cloth, and rust-red mantle "
    "stripe (his only marks; no other figure ever wears them)",
    str(REFS_DIR / "simon_ref.png"),
)
R_SIMON_FACE = Ref(
    "Simon of Cyrene -- his face and eyes only, for close crops",
    str(REFS_DIR / "simon_face_ref.png"),
)
R_SOLDIERS = Ref(
    "the two Roman soldiers -- match their plain helmets, cuirasses, and kit exactly (no "
    "plume, no crest, no cloak, no shield)",
    str(REFS_DIR / "soldiers_ref.png"),
)
R_CROSS = Ref(
    "the cross -- match its full Latin-cross shape, its rough weathered timber, and its "
    "plain pegged crossbeam joint; nothing on the wood",
    str(REFS_DIR / "cross_ref.png"),
)
R_GATE = Ref(
    "the gate of the city -- its exact wall, doorway, jambs, lintel, and threshold stone",
    str(REFS_DIR / "gate_ref.png"),
)
R_ROAD = Ref(
    "the road from behind -- its exact rise and crest, no figures",
    str(REFS_DIR / "road_ref.png"),
)

SEQ_TITLE = "WITHOUT THE GATE"

# ===========================================================================
# F04 -- "Now he is through the gate... outside is 'without.'" -- THE DEBUT
# PAGE. Renders FIRST, refs=[]: Simon large, calm, alone, three-quarter to
# the viewer so one approval yields simon_ref, simon_face_ref, beam_ref, and
# gate_ref all at once. Hard problem #2 -- a page about a WORD.
# ===========================================================================
F04 = PageSpec(
    seq_title=SEQ_TITLE,
    frame_label="F04",
    panels=(
        Panel("inside",
              "the gate seen from INSIDE the lane -- shadowed stone jambs and lintel framing "
              "a bright opening onto the road beyond, no figure"),
        Panel("the gate",
              "the broad worn threshold stone across the doorway's foot, close and low, no "
              "figure"),
        Panel("without",
              "the gate's outer face seen from OUTSIDE on the road, the doorway dark, the "
              "road beginning at its foot, no figure"),
    ),
    still_shot_type="MEDIUM CLOSE shot",
    anim_shot_desc="medium close shot",
    main_scene_still=(
        f"{SIMON_BUILD} a few paces outside the gate, walking RIGHT along the dry road, seen "
        "three-quarter from the front-right so that his whole face is fully visible inside "
        "the frame -- his eyes open, his mouth closed, his brow set, dust on his cheek -- the "
        f"beam ({CROSS_BUILD}) across the back of his shoulders with both hands gripping it -- "
        "framed specifically so the asymmetry reads clearly in THIS shot: the crossbeam "
        "crosses the upright in the UPPER THIRD of the frame, close above his own shoulders, "
        "NOT at the frame's vertical center; above that crossing point only a short length of "
        "upright is visible, rising to about head height or a little above; below the "
        "crossing point the upright continues as one long unbroken timber all the way down "
        "past his hip and knee, exiting the BOTTOM edge of the frame -- the crossbeam itself "
        "is a distinctly shorter length of timber than the long downward run of the upright, "
        "and it visibly stops well short of the frame's own left and right edges, unlike the "
        "upright which runs the full height of the frame top-to-bottom; if the crossing point "
        "were moved to the exact center of the frame with equal timber-length on all four "
        "sides, the drawing would be wrong -- the crossing point belongs in the upper third "
        "only -- "
        "his head-cloth tied at the nape, his rust-striped mantle over his left shoulder, "
        "fully inside the frame from the knees up, drawn in the same steady, confident, "
        "single-struck line, no doubled or tremored contour; Simon positioned right-of-center "
        "in the frame, the gate positioned at the FRAME'S OWN LEFT EDGE, never at the frame's "
        "right and never at its center -- behind him and to his left, the "
        f"gate of the city ({GATE_BUILD}) -- its open doorway, its threshold stone, and the "
        "shadowed lane beyond, fully inside the frame at the frame's left edge only; no other "
        "figure anywhere in the frame; "
        "the ground dry, no water anywhere; no hill, no crosses, no crowd. Stage 2 dosage: "
        "the blue ink motif is quietly present -- a few soft blue threads rising from the "
        "threshold stone up into the gate's open doorway behind him, and at their top one "
        "soft, irregular, hazy patch of the same blue pigment, entirely amorphous, with soft "
        "feathered edges and no internal structure of any kind, exactly like a single drop "
        "of watercolor spreading into wet paper -- STRICTLY confined inside the dark opening "
        "of the doorway itself and nowhere else: it never rises above the top of the doorway "
        "or the lintel, never crosses onto the pale stone wall surrounding the doorway, never "
        "appears against the open sky, never floats free of the doorway as a cloud shape, and "
        "stays entirely inside the dark rectangle of the open doorway, small relative to that "
        "opening -- touching only the stone and the air within that opening, touching no "
        "figure, never on the road, never on the beam, never on the man; every thread "
        "behaving like wet ink bled into the paper, smooth and open, never blot-shaped, "
        "never a glow."
    ),
    material_closer=(
        "the soft blue threads and the one small bloom held inside the gate's doorway behind "
        "him are the only unusual ink on the page, and the beam, the man, and the paper "
        "beneath him are free of any ink."
    ),
    panel_motions=(
        "the light in the bright opening warms very slightly",
        "the threshold stone lies still, a little dust drifting over it",
        "a thin banner of dust drifts across the road at the gate's foot",
    ),
    main_scene_animation=(
        "Simon keeps walking right at a steady pace, the beam steady on his shoulders, his "
        "eyes on the road ahead, one slow breath, his lips closed and completely still; the "
        "soft blue threads and the small bloom in the doorway behind him drift gently within "
        "their own small area inside the doorway, never leaving it, never lowering toward "
        "the road; a low thin haze of dust drifts along the road; no new stain, spot, or "
        "darkening appears anywhere on the page at any point."
    ),
    fence_kind="none",
    caption_lines=("outside is without",),
    corner_note="NOTE: through the gate",
    refs=[],
    model_tier="veo3_1_lite",
    clip_duration=5,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F02 -- "Same road. They put the cross on Simon's back. Nobody asked him."
# The seizure at the gate's mouth. Renders second (after F04's refs); the
# soldiers debut here -> approve -> crop soldiers_ref.
# ===========================================================================
F02 = PageSpec(
    seq_title=SEQ_TITLE,
    frame_label="F02",
    panels=(
        Panel("same road",
              "the dust of the road close and low, two lines of sandal-prints crossing each "
              "other in opposite directions, no figure"),
        Panel("on his back",
              "the rough underside of a squared beam pressing down across the back of a "
              "man's neck and shoulders, seen from behind, the knot of a plain head-cloth at "
              "the nape, close, no face"),
        Panel("nobody asked",
              "a soldier's two hands gripping a beam and pressing it down, close, no face"),
    ),
    still_shot_type="MEDIUM shot",
    anim_shot_desc="medium shot",
    main_scene_still=(
        f"the gate of the city ({GATE_BUILD}) at the left, its doorway open and its "
        "threshold stone plain and unmarked, fully inside the frame; just outside the "
        f"threshold at center, {SIMON_BUILD} stopped mid-stride and facing LEFT toward the "
        "doorway -- the way he was walking -- with the beam "
        f"({CROSS_BUILD}) just laid across the back of his shoulders, his back bent under the "
        "sudden weight, his own hands coming up to grip it, his face turned toward the "
        "doorway, his eyes open, his mouth closed, fully inside the frame, drawn in the same "
        "steady, confident, single-struck line as every figure on the page, no doubled or "
        f"tremored contour; beside him one of {SOLDIERS_BUILD} with BOTH hands on the beam "
        "pressing it down onto Simon's shoulders; a few steps to the RIGHT beyond them, "
        f"outside, {JESUS_BUILD} standing unburdened, facing RIGHT toward the road, the "
        "other soldier's hand on his upper arm, his hands empty, touching no one, not "
        f"looking back, {JESUS_PASSION_GUARD}, fully inside the frame -- the beam passes "
        "from him to Simon only by the soldier's hands, never by his; exactly two soldiers; "
        "the road running out to the right; the ground dry, no water anywhere; no hill, no "
        "crosses, no crowd. Stage 0 dosage: no blue Swirls of Life ink motif anywhere on "
        "this page -- no blue ink appears anywhere in the scene, the panels, or the margins."
    ),
    material_closer=(
        "no unusual ink of any kind is at work on this page -- no blue, no gold, no stain -- "
        "and the paper beneath every figure is wholly clean."
    ),
    panel_motions=(
        "a thin haze of dust drifts across the crossing prints",
        "the beam's underside holds, the light across the wood warming very slightly",
        "the gripping hands hold, still",
    ),
    main_scene_animation=(
        "EVERY figure stays standing exactly where they are drawn for the whole clip -- "
        "this is a held moment, nobody walks anywhere, nobody moves toward the doorway or "
        "through it, and nobody enters the gate; Simon's feet stay planted in the exact same "
        "spot on the ground outside the threshold the entire clip, and the soldier pressing "
        "the beam onto him also stays standing in his own exact spot outside the gate the "
        "entire clip -- if either of them appears to have moved even one step toward the "
        "doorway, or if either of them is inside the doorway or the shadowed lane beyond it "
        "at any point, that is wrong: the interior of the gate stays visible and EMPTY of any "
        "figure for the whole clip, exactly as in the first frame; only this small, local "
        "motion happens: the soldier's hands press the beam down the last small distance onto "
        "Simon's shoulders and hold there; Simon's knees bend a little as they take the weight "
        "and his hands close around the beam and hold it, his face staying turned toward the "
        "doorway, his feet not moving, his lips closed and completely still; Jesus likewise "
        "stays standing in his own exact spot outside the gate, facing the road, the "
        "soldier's hand on his arm, one slow breath, never looking back, never stepping, his "
        "lips closed; a low thin haze of dust drifts along the road beyond; no new stain, "
        "spot, or darkening appears anywhere on the page at any point."
    ),
    fence_kind="none",
    caption_lines=("Nobody asked him",),
    corner_note="NOTE: same road",
    refs=[R_JESUS, R_SIMON, R_SIMON_FACE, R_CROSS, R_GATE],
    model_tier="kling3_0",
    clip_duration=8,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F01 -- "led him out to crucify him... coming out of the country." The
# establishing shot, the whole two-direction geometry in one frame. Renders
# after F04 and F02 (every ref already chained).
# ===========================================================================
F01 = PageSpec(
    seq_title=SEQ_TITLE,
    frame_label="F01",
    panels=(
        Panel("the soldiers", "a plain iron helmet and the head of a short spear against "
              "the sky, close, no face"),
        Panel("led him out", "a soldier's hand gripping a man's upper arm through the sleeve "
              "of an undyed cream-brown robe, close, no face"),
        Panel("the country", "open stony fields under morning light, a dry road coming in "
              "over a rise, no one on it"),
    ),
    still_shot_type="WIDE shot",
    anim_shot_desc="wide shot",
    main_scene_still=(
        f"the gate of the city ({GATE_BUILD}) at the frame's left-center, the high pale-gold "
        f"wall running across the background, the doorway open; IN the doorway, {JESUS_BUILD} "
        "stepping OUT through it from left to right, his right foot planted ON the broad worn "
        "threshold stone, walking upright at an even pace, already carrying the cross himself "
        f"({CROSS_BUILD}), its crossbeam resting across the back of his own shoulders and neck "
        "with both his hands raised and gripping it at either side, its long upright trailing "
        f"back and down behind him -- {JESUS_PASSION_GUARD}, fully "
        f"inside the frame; {SOLDIERS_BUILD} -- one just outside the doorway ahead of Jesus, "
        "his one hand resting only on Jesus's upper arm, leading him, his other hand empty; "
        "the other soldier a step behind Jesus, empty-handed, touching no one, an ordinary "
        "escort; only Jesus's own hands touch the cross, and only the leading soldier's "
        "one hand touches Jesus's upper arm -- no other contact of any kind between any two "
        "figures on this page; the shadowed lane visible through the doorway behind them is "
        "EMPTY -- no other figure, face, head, or silhouette of any kind visible anywhere in "
        "the lane or the doorway's shadow, empty bare stone only; at the frame's RIGHT, nearer "
        f"the viewer and larger, {SIMON_BUILD} walking from right to LEFT along the road "
        f"toward the gate, mid-stride, {SIMON_UNBURDENED}, his eyes on the road, not on the "
        "gate, fully inside the frame; a long stretch of EMPTY dry road between him and the "
        "gate; the road running along the foot of the wall and then away over the rise at the "
        "right; morning light, long shadows; the ground dry, no water anywhere; no hill, no "
        "crosses, no crowd anywhere, no figure anywhere except Jesus, the two soldiers, and "
        "Simon -- four figures total on this page, no more. Stage 0 dosage: no blue Swirls of "
        "Life ink motif anywhere on this page -- no blue ink appears anywhere in the scene, "
        "the panels, or the margins; the threshold stone plain worn stone, unmarked. The open "
        "sky above the wall is empty bare paper wash only -- no numeral, no digit, no letter, "
        "no stray mark of any kind floating in the sky or in any corner of the main scene."
    ),
    material_closer=(
        "no unusual ink of any kind is at work on this page -- no blue, no gold, no stain -- "
        "and the paper beneath every figure is wholly clean."
    ),
    panel_motions=(
        "the light on the helmet warms very slightly and settles",
        "the gripping hand holds, still",
        "a thin banner of dust drifts across the far road",
    ),
    main_scene_animation=(
        "EVERY figure on this page stays close to their starting position for the WHOLE "
        "clip -- this is a held moment, not a long journey, and no one should travel far "
        "enough to leave the frame or approach anyone else; ALL FIVE figures (Jesus, both "
        "soldiers, and Simon) must still be clearly visible, in their same relative places, "
        "in the very last frame exactly as they are in the very first frame -- if any figure "
        "is missing from the last frame, that is wrong; Jesus takes only one or two small, "
        "unhurried steps forward, staying well inside the doorway threshold area the whole "
        "clip, never walking far enough to approach the frame's right edge; the cross stays "
        "steady across his shoulders, its upright never shifting, his hands staying closed "
        "around it, the leading soldier's hand staying on his arm, his face toward the road, "
        "his lips closed and completely still; the second soldier takes the same one or two "
        "small steps beside him, empty-handed; Simon likewise takes only one or two small "
        "steps in place, staying clearly and obviously far from the gate the whole clip, the "
        "wide empty gap of road between him and the doorway looking essentially UNCHANGED "
        "from the first frame to the last -- he never approaches the doorway, never reaches "
        "the threshold, and never comes near Jesus's group; the two groups must never meet "
        "or close their distance in this clip; a low thin haze of dust drifts along the "
        "empty road between them; no blue or gold ink motif appears anywhere on this page, "
        "and none appears at any point in the clip; no new stain, spot, or darkening appears "
        "anywhere on the page at any point."
    ),
    fence_kind="none",
    caption_lines=("led him out",),
    corner_note="NOTE: passed by",
    refs=[R_JESUS, R_SIMON, R_SIMON_FACE, R_CROSS, R_GATE, R_SOLDIERS],
    model_tier="veo3_1_lite",
    clip_duration=8,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F03 -- "that he might bear it after Jesus. Simon turns, and walks out too."
# THE GOSPEL TURN. Same gate, same beam, same man -- now facing RIGHT (the
# page cut IS the turn, LAW 1). The episode's first blue.
# ===========================================================================
F03 = PageSpec(
    seq_title=SEQ_TITLE,
    frame_label="F03",
    panels=(
        Panel("they laid", "a beam lying across a man's shoulders seen from behind, its two "
              "raw ends jutting out either side, close, no face"),
        Panel("after Jesus", "Jesus's back, small, walking away to the right along a road, his "
              "head bare -- no crown of thorns, no crown of any kind, nothing encircling his "
              "head, plain hair only -- a soldier beside him"),
        Panel("turns", "a single pair of sandaled feet on a broad worn threshold stone, toes "
              "pointing RIGHT, the rear heel lifting, low and close"),
    ),
    still_shot_type="MEDIUM WIDE shot",
    anim_shot_desc="medium wide shot",
    main_scene_still=(
        f"the gate of the city ({GATE_BUILD}) at the left, its doorway open behind him, its "
        f"broad worn threshold stone fully inside the frame; AT the threshold, {SIMON_BUILD} "
        "TURNED -- now facing RIGHT toward the open road -- the beam "
        f"({CROSS_BUILD}) across the back of his shoulders, both hands gripping it, "
        "mid-first-step outward: his front foot on the dry road outside, his rear heel just "
        "lifting from the threshold stone, his face toward the road ahead, his eyes open, "
        "his mouth closed, fully inside the frame, drawn in the same steady, confident, "
        "single-struck line as every figure on the page; the broad worn threshold stone is a "
        "clearly visible pale slab lying flat across the doorway's foot, directly beneath and "
        "a little behind Simon's lifting rear heel, distinct from the wooden door and its "
        "frame, plainly readable as a separate stone object in the paving; TWO SEPARATE "
        f"soldier figures, count them, with visible open space between them, not touching "
        f"each other: one of {SOLDIERS_BUILD}, empty-handed now, walking immediately beside "
        "and a little behind Simon, close to him; and, several full strides further along the "
        f"road, a SECOND, separate soldier walking beside {JESUS_BUILD} -- a few paces ahead "
        "outside to the right, Jesus walking RIGHT at an even pace, this second soldier's "
        "hand on his upper arm, unburdened, not looking back, touching no one, "
        f"{JESUS_PASSION_GUARD}, fully inside the frame; a visible gap of open road lies "
        "between the Simon pair and the Jesus pair -- exactly two soldiers total on this "
        "page, one in each pair, never both soldiers standing together in one place; the "
        "road running out to the right over the rise; the ground dry, no water anywhere; no "
        "hill, no crosses, no crowd. Stage 1 dosage: exactly one SMALL, MODEST, RESTRAINED "
        "thread of blue ink rising from the top surface of the worn threshold stone itself -- "
        "from the stone just behind Simon's lifting heel -- its whole visible length no "
        "taller than the height of Simon's own knee, a short simple gentle curve with NO "
        "loop, NO coil, NO spiral, NO S-curve, NO more than one single gentle bend along its "
        "entire length, leaning a little to the right at its top and nowhere else; this is "
        "explicitly NOT a long ribbon, NOT a large sweeping line, NOT a dramatic swirl or "
        "flourish, and does NOT extend upward into the sky or across any significant part of "
        "the frame -- it stays small and low, close beside the stone it rises from; its "
        "lowest point is at the stone and it never hangs down, never droops, never trails "
        "toward the ground, never appears in the shadow of the door, and never resembles a "
        "drip, a trickle, or running water; it touches only the stone and the small patch of "
        "air directly above it, touching no figure, no clothing, and no part of Simon's body, "
        "never touching the beam, the man, or his foot, the only blue on the whole page, "
        "behaving like one small stroke of wet ink bled into the paper, never blot-shaped, "
        "never a glow."
    ),
    material_closer=(
        "the single blue thread rising from the threshold stone behind him is the only "
        "unusual ink at work on this page, and the beam, the man, and the paper beneath "
        "every figure are free of any ink."
    ),
    panel_motions=(
        "the beam on the shoulders holds, the light across the wood warming very slightly",
        "the small far figures hold, tone-only",
        "a little dust lifts from under the lifting heel and drifts",
    ),
    main_scene_animation=(
        "ALL FOUR figures (Simon, his soldier, Jesus, his soldier) must still be clearly "
        "visible in the frame at every single point in the clip, including the true final "
        "frame -- if any one of them is missing, cropped out, or has exited the frame at any "
        "point, that is wrong; only small, contained motion happens, not a long journey: "
        "Simon takes a few small unhurried steps out from left to right along the road away "
        "from the gate, staying well within the frame the whole time, the beam steady across "
        "his shoulders, his hands gripping it, his face toward the road ahead, his lips "
        "closed and completely still; the soldier beside him takes the exact same small "
        "steps at Simon's exact pace, staying right beside him shoulder-to-shoulder the "
        "whole clip -- he never falls behind, never stops early, and never drifts back "
        "toward the gate; Jesus and his soldier, further along the road, are the most "
        "important figures to keep drawn and visible for the ENTIRE clip -- if there is any "
        "doubt about how to animate them, the correct choice is to keep them PERFECTLY "
        "MOTIONLESS, like a frozen photograph, exactly as drawn in the first frame, rather "
        "than move them, fade them, or let them leave the frame; Jesus and his soldier are "
        "drawn, present, and fully visible in every single frame from the very first to the "
        "very last, never once disappearing, never fading out, never becoming transparent, "
        "never exiting past the frame's edge -- at most Jesus takes a few small unhurried "
        "steps of his own while staying well within the frame, the soldier's hand on his "
        "arm, never looking back, his lips closed, but if that motion risks losing either "
        "figure from view, they simply hold still instead; the single thin blue ink thread "
        "at the threshold stone stays exactly as "
        "drawn, in place, for the whole clip; a low thin haze of dust drifts along the road; "
        "no new stain, spot, or darkening appears anywhere on the page at any point."
    ),
    fence_kind="none",
    caption_lines=("after Jesus",),
    corner_note="NOTE: Simon turns",
    refs=[R_JESUS, R_SIMON, R_SIMON_FACE, R_CROSS, R_GATE, R_SOLDIERS],
    model_tier="veo3_1_lite",
    clip_duration=8,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F05 -- "The sin offering... burned 'without the camp.'" THE TYPE PAGE. The
# Old Testament enters the episode in the carved panels ONLY (the register
# rule) -- the main scene never leaves the road.
# ===========================================================================
F05 = PageSpec(
    seq_title=SEQ_TITLE,
    frame_label="F05",
    panels=(
        Panel("blood carried in",
              "a priest's two hands carrying a shallow clay bowl held level, its contents "
              "dark, LEFTWARD in through the hanging woven curtain of a tent's doorway, "
              "close, no face"),
        Panel("body went out",
              "two men carrying the carcass of a slaughtered animal slung on a pole between "
              "them, RIGHTWARD past the last goat-hair tents of a camp toward open ground, "
              "small, seen from the side, plainly and reverently drawn, no wound visible, no "
              "gore"),
        Panel("burned",
              "a low fire on open ground outside a camp's edge, thin smoke rising, the tents "
              "small and far at the left, no figure"),
    ),
    still_shot_type="WIDE shot",
    anim_shot_desc="wide shot",
    main_scene_still=(
        "the road outside the city: the high wall receding at the left with the gate of the "
        f"city ({GATE_BUILD}) small at the far left, its doorway and threshold stone fully "
        f"inside the frame; {SIMON_BUILD} seen from behind, his back three-quarters turned "
        "toward the viewer (NOT a flat side profile -- angle him so the viewer sees mostly "
        "his back and shoulders, only a hint of his face's far cheek), walking AWAY along "
        f"the road toward the right at mid-frame, the "
        f"cross ({CROSS_BUILD}) across the back of his shoulders, both hands gripping it, "
        "its long upright hanging down and trailing visibly below his waist toward the "
        "ground, its short crossbeam plainly higher up near his neck -- "
        "match reference image 'the cross' exactly: the same full Latin-cross shape, the "
        "same weathered rough-hewn timber, and the same plain pegged joint where the "
        "crossbeam meets the upright -- fully inside "
        "the frame, drawn in the same steady, confident, single-struck line; no other figure "
        "anywhere in the frame; the road "
        "running away to the right over the low stony rise into open country; the ground "
        "dry, no water anywhere; no hill, no crosses, no crowd, nothing at the road's end. "
        "Stage 2 dosage, held: a few soft blue threads rising from the small far threshold "
        "stone up into the small doorway at the far left, and one small amorphous "
        "watercolor bloom hanging in the doorway's air, small with the distance, STRICTLY "
        "contained within the dark opening of the doorway itself and nowhere else -- it "
        "never rises above the top of the doorway, never crosses onto the pale stone wall "
        "surrounding the doorway, never appears against the sky or the exterior stonework, "
        "and stays entirely inside the dark rectangle of the open doorway, touching only the "
        "stone and the air within that opening, the only blue on the whole page; no blue of "
        "any kind in any of the three top panels; the road, the man, and the beam free of "
        "any ink of any kind."
    ),
    material_closer=(
        "the small blue threads and bloom held inside the far doorway are the only unusual "
        "ink on the page; the three top panels carry no blue at all, and the paper beneath "
        "the man is wholly clean."
    ),
    panel_motions=(
        "the bowl and the hands hold, the light across them warming very slightly",
        "the two carriers hold, tone-only",
        "the flames of the fire flicker in place and the thin smoke drifts upward within "
        "its own column",
    ),
    main_scene_animation=(
        "Simon keeps walking away along the road toward the right at a steady pace, his back "
        "to the viewer, one continuous stride the whole clip, the cross steady on his "
        "shoulders; the small blue "
        "threads and bloom inside the far doorway drift gently within their own small area, "
        "never leaving the doorway; a low thin haze of dust drifts along the road; no new "
        "stain, spot, or darkening appears anywhere on the page at any point."
    ),
    fence_kind="none",
    caption_lines=("without the camp",),
    corner_note="NOTE: Hebrews 13",
    refs=[R_SIMON, R_SIMON_FACE, R_CROSS, R_GATE],
    model_tier="veo3_1_lite",
    clip_duration=10,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F06 -- HERO -- "Wherefore Jesus also... suffered without the gate. Out
# there, where Simon is walking." The gospel pivot: Christ's own atoning act
# named, Jesus bodily back in frame a single pace ahead of Simon.
# ===========================================================================
F06 = PageSpec(
    seq_title=SEQ_TITLE,
    frame_label="F06",
    panels=(
        Panel("without the camp",
              "the edge of a camp: the last goat-hair tents small at the LEFT, open ground "
              "and a low fire's thin smoke at the RIGHT, no figure"),
        Panel("without the gate",
              "the gate of the city small at the LEFT, the dry road running out to the "
              "RIGHT, empty, no figure"),
        Panel("Jesus also", "Jesus's face in profile, close, calm, facing right, lips "
              "closed, head bare"),
    ),
    still_shot_type="MEDIUM WIDE shot",
    anim_shot_desc="medium wide shot, from beside the road, low",
    main_scene_still=(
        f"the gate of the city ({GATE_BUILD}) small at the far-left edge of the frame, its "
        "doorway and threshold stone fully inside the frame; nearer the gate, at the LEFT "
        f"side of the frame, ALONE with no other figure anywhere near him, {SIMON_BUILD} "
        "walking RIGHT, one full stride BEHIND the group ahead of him, closer to the gate "
        f"than they are, the beam ({CROSS_BUILD}) across the back of his shoulders, both "
        "hands gripping it, his head LIFTED and his eyes on the man ahead of him further to "
        "the right, his mouth closed, fully inside the frame, drawn in the same steady, "
        "confident, single-struck line as every figure on the page -- a visible gap of open "
        "road between Simon and the group ahead of him, no soldier and no other figure "
        "walking anywhere near Simon, nothing behind him or beside him but empty road; then, "
        "positioned CLEARLY FURTHER RIGHT than Simon and further from the gate than Simon "
        f"is, nearer the frame's right edge, {JESUS_BUILD} walking RIGHT along the road, one "
        f"full stride AHEAD of Simon and further along the road than Simon -- "
        f"{JESUS_PASSION_GUARD}, BOTH of {SOLDIERS_BUILD} together with him, one on each "
        "side, one with a hand on his upper arm, fully inside the frame; the left-to-right "
        "order of figures across the frame, from nearest the gate to farthest from it, is: "
        "the gate, Simon ALONE, then a gap of open road, then Jesus with BOTH soldiers -- "
        "Jesus is never positioned to the left of Simon and never nearer the gate than Simon "
        "is; exactly two soldiers TOTAL on this page, both of them in Jesus's group and "
        "none anywhere near Simon; Simon and Jesus never touching; the road running away to "
        "right over the rise, nothing at its end; the ground dry, no water anywhere; no "
        "hill, no crosses, no crowd. Stage 2 dosage, held: a few soft blue threads and one "
        "small amorphous watercolor bloom held inside the small far doorway at the left "
        "edge, touching only the threshold stone and the air of the doorway; the road, "
        "Jesus, Simon, the soldiers, and the beam free of any ink of any kind."
    ),
    material_closer=(
        "the small blue threads and bloom held inside the far doorway are the only unusual "
        "ink on the page, and the beam and every figure on the road are free of any ink."
    ),
    panel_motions=(
        "the thin smoke drifts upward within its own column",
        "a thin banner of dust drifts across the empty road at the gate's foot",
        "the sketched profile holds, tone-only",
    ),
    main_scene_animation=(
        "the gap of open road between Simon and Jesus's group is the single most important "
        "thing to preserve in this clip -- it must look essentially UNCHANGED from the first "
        "frame to the very last frame; Simon takes only one or two small unhurried steps in "
        "place, staying clearly and obviously far behind Jesus's group the whole time -- he "
        "never closes the distance, never catches up, never comes near the soldiers or "
        "Jesus, and is never standing at the edge of their cluster; if Simon appears any "
        "closer to Jesus's group in the last frame than in the first frame, that is wrong; "
        "only this small motion happens: Simon's head lifts the last small distance and "
        "holds, his eyes staying on the man ahead of him, the beam steady on his shoulders, "
        "his lips closed and completely still; Jesus and the two soldiers likewise take only "
        "one or two small unhurried steps of their own, staying well within the frame, the "
        "soldier's hand on Jesus's arm, never looking back, lips closed and completely "
        "still; the small blue threads and bloom inside the far doorway drift gently within "
        "their own small area, never leaving it; a low thin haze of dust drifts along the "
        "road; no new stain, spot, or darkening appears anywhere on the page at any point; "
        "no text, letters, numbers, or words of any kind appear anywhere on the page beyond "
        "the two baked captions already drawn in the first frame -- no ghost text, no faint "
        "or duplicated lettering, no ground-level text of any kind ever appears."
    ),
    fence_kind="none",
    caption_lines=("suffered without the gate",),
    corner_note="NOTE: out there",
    refs=[R_JESUS, R_SIMON, R_SIMON_FACE, R_CROSS, R_GATE, R_SOLDIERS],
    model_tier="kling3_0",
    clip_duration=10,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F07 -- "Hebrews turns to you: 'Let us go forth therefore unto him...'"
# THE CAMERA TURN. "Turns to you" drawn as the camera turning: the viewer
# now stands on the road, the gate behind the camera and never in frame.
# The road-from-behind debuts here -> approve -> crop road_ref.
# ===========================================================================
F07 = PageSpec(
    seq_title=SEQ_TITLE,
    frame_label="F07",
    panels=(
        Panel("turns to you",
              "the dust of a road close at the viewer's own feet, one line of sandal-prints "
              "leading away from the panel's bottom edge into the distance, no figure"),
        Panel("unto him", "Jesus's back, small and far, walking away up a road, a soldier "
              "beside him"),
        Panel("his reproach",
              "the back of a man's neck and shoulders under a beam, from behind, close, the "
              "knot of a plain head-cloth at the nape, no face"),
    ),
    still_shot_type="WIDE shot",
    anim_shot_desc="wide shot, from behind, low",
    main_scene_still=(
        f"the road ({ROAD_BUILD}) running straight away from the viewer's own feet over open "
        "stony country and up the long gentle rise to the far crest, fully inside the frame; "
        f"no gate, no wall, and no building anywhere in the frame; at mid-distance, {SIMON_BUILD} "
        "walking AWAY from the viewer along the road, his back to the viewer, the beam "
        f"({CROSS_BUILD}) across the back of his shoulders with its two raw ends jutting out "
        "either side, both hands gripping it, the knot of his head-cloth at his nape and his "
        "rust-striped mantle over his left shoulder, fully inside the frame, drawn in the "
        f"same steady, confident, single-struck line; further along and smaller, {JESUS_BUILD} "
        f"walking away up the road, his back to the viewer, upright, one of {SOLDIERS_BUILD} "
        "with a hand on his upper arm and the other soldier beside him, exactly two soldiers, "
        "none of them turning; nothing visible beyond the crest -- no hill, no crosses, no "
        "crowd; the ground dry, no water anywhere. Stage 3 beginning dosage: the blue ink "
        "motif begins to diffuse -- one loose open band of blue ink threads with traces of "
        "muted gold drifting high in the air above the road, stretching from above the near "
        "road toward the far crest where the road goes out of sight, tied to no single "
        "figure, touching nothing on the ground, never on the beam, never on any figure, no "
        "longer held in any doorway but not yet filling the scene, behaving like wet ink bled "
        "into the paper's sky wash, never a glow."
    ),
    material_closer=(
        "the loose blue-and-gold band beginning high in the air above the road is the only "
        "unusual ink on the page, and the beam and every figure on the road are free of any "
        "ink."
    ),
    panel_motions=(
        "a thin haze of dust drifts across the near prints",
        "the small far figures hold, tone-only",
        "the beam on the shoulders holds, the light across the wood warming very slightly",
    ),
    main_scene_animation=(
        "Simon keeps walking away from the viewer along the road toward the far crest, one "
        "continuous steady stride the whole clip, his back to the viewer, the beam steady "
        "across his shoulders, never turning; Jesus and the two soldiers further along keep "
        "walking away at the same pace, never turning; the blue-and-gold ink threads high in "
        "the air drift smoothly within their own fixed band across the sky above the road; a "
        "low thin haze of dust drifts along the road; no new stain, spot, or darkening "
        "appears anywhere on the page at any point."
    ),
    fence_kind="none",
    caption_lines=("Let us go forth",),
    corner_note="NOTE: unto him",
    refs=[R_SIMON, R_CROSS, R_JESUS, R_SOLDIERS],
    model_tier="veo3_1_lite",
    clip_duration=6,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F08 -- "Reproach is shame. Bearing it is carrying it, as Simon carried the
# wood." THE FENCE PAGE -- the close on the carrying, the one page that can
# insist at close range that the thing on his shoulders is a plain beam
# with nothing on it. The one validated seedream-4-5 case in this episode.
# ===========================================================================
F08 = PageSpec(
    seq_title=SEQ_TITLE,
    frame_label="F08",
    panels=(
        Panel("the wood", "the rough adzed grain and split raw end of a timber beam, close, "
              "no hands, nothing on the wood"),
        Panel("bearing it", "two hands gripping the underside of a beam from below, knuckles "
              "tight, close, no face"),
        Panel("carrying it", "two sandaled feet in dust under a load, the prints pressed "
              "deep, low and close"),
    ),
    still_shot_type="CLOSE-UP profile shot",
    anim_shot_desc="close-up profile shot",
    main_scene_still=(
        f"{SIMON_BUILD} in profile facing RIGHT, from the waist up, "
        f"the beam ({CROSS_BUILD}) across the back of his shoulders behind his neck, both "
        "hands gripping it, his head bowed a little under the weight, his neck and shoulders "
        "taut, sweat at his temple, dust on his cheek and on the wood, his whole face fully "
        "visible in profile inside the frame -- his eyes open on the road ahead, his mouth "
        "closed -- drawn in the same steady, confident, single-struck line, no doubled or "
        "tremored contour; nothing on the wood -- no nails, no rope, no inscription, no "
        "blood, no marks of any kind, plain raw timber; the horizon LOW, so that open sky "
        "fills the upper third of the frame above his head and the beam; the road "
        f"({ROAD_BUILD}) small and soft in the far background; no other figure anywhere in "
        "the frame; the ground dry, no water anywhere; no hill, no crosses, no crowd. Stage "
        "3 dosage, held: a few threads of the loose blue-and-gold band cross the very top of "
        "the frame high in the sky, well above the beam and his head, tied to nothing, "
        "touching nothing, never lowering toward the beam or the man; the beam and the man "
        "free of any ink of any kind."
    ),
    material_closer=(
        "the few blue-and-gold threads crossing the top of the sky are the only unusual ink "
        "on the page, and the beam and the man are free of any ink of any kind."
    ),
    panel_motions=(
        "the light across the grain warms very slightly",
        "the gripping hands tighten a little and hold",
        "dust drifts from around the pressed feet",
    ),
    main_scene_animation=(
        "Simon's grip tightens on the beam and holds, his shoulders settling a little lower "
        "under the weight and holding there, one slow heavy breath, his head staying bowed, "
        "his eyes open on the road ahead, his lips closed and completely still; the few "
        "blue-and-gold threads high in the sky drift smoothly within their own fixed band at "
        "the top of the frame, never lowering; no new stain, spot, or darkening appears "
        "anywhere on the page at any point."
    ),
    fence_kind="none",
    caption_lines=("as Simon carried the wood",),
    corner_note="NOTE: reproach is shame",
    refs=[R_SIMON, R_SIMON_FACE, R_CROSS, R_ROAD],
    # Fallback to nano-banana-pro per the brief's own explicit rule (§8 Q8): a seedream
    # render that draws a cross shape triggers a ONE-TIME fallback, never a 2nd seedream
    # attempt. Triggered 2026-09-06 during the beam-v2 (patibulum) re-render pass -- the
    # seedream render put a clear X-shaped cross on Simon's shoulders.
    still_model="nano-banana-pro",
    model_tier="kling3_0",
    clip_duration=5,
    panel_style="woodcut_hybrid",
)

# ===========================================================================
# F09 -- "Simon was forced out. You are asked. Turn on your own road..."
# THE CALL, drawn as the viewer's own road. Jesus and the soldiers tiny at
# the crest, about to go over but not yet gone. Stage 3, the whole sky.
# ===========================================================================
F09 = PageSpec(
    seq_title=SEQ_TITLE,
    frame_label="F09",
    panels=(
        Panel("forced out",
              "a soldier's hand gripping a man's upper arm through an oatmeal wool sleeve, "
              "close, no face"),
        Panel("asked",
              "a single open hand, palm up, empty, offered toward the viewer against plain "
              "paper, no figure, no ink on or near it"),
        Panel("after him",
              "two lines of sandal-prints in dust running away from the viewer, one line a "
              "pace behind the other, no figure"),
    ),
    still_shot_type="WIDE shot",
    anim_shot_desc="wide shot, from behind, very low",
    main_scene_still=(
        f"the road ({ROAD_BUILD}) seen from the viewer's own standing place: the near dust of "
        "the road large in the foreground at the bottom edge of the frame, the road running "
        "straight away up the long gentle rise to the far crest, fully inside the frame; no "
        "gate, no wall, no building anywhere in the frame; at mid-distance, further along "
        f"than before and smaller, {SIMON_BUILD} walking AWAY from the viewer along the road, "
        f"his back to the viewer, the beam ({CROSS_BUILD}) across the back of his shoulders, "
        "both hands gripping it, the knot of his head-cloth at his nape, his rust-striped "
        "mantle over his left shoulder, fully inside the frame, drawn in the same steady, "
        f"confident, single-struck line; at the far crest, tiny, {JESUS_BUILD} and "
        f"{SOLDIERS_BUILD} -- exactly two soldiers -- walking away, their backs to the "
        "viewer, about to go over the crest but not yet gone; nothing visible beyond the "
        "crest -- no hill, no crosses, no crowd; the ground dry, no water anywhere. Stage 3 "
        "dosage: the blue ink motif, with traces of muted gold, is woven through the whole "
        "upper air above the road from the near foreground to the far crest -- threads "
        "drifting in one loose open band across the sky, tied to no single figure, touching "
        "no person, never on the beam, never on the ground, behaving like wet ink bled "
        "through the page's own sky wash, never a glow."
    ),
    material_closer=(
        "the blue-and-gold band woven through the whole sky above the road is the only "
        "unusual ink on the page, and the beam, the road, and every figure are free of any "
        "ink."
    ),
    panel_motions=(
        "the gripping hand holds, still",
        "the open hand holds, the light across it warming very slightly",
        "a thin haze of dust drifts across the prints",
    ),
    main_scene_animation=(
        "Simon keeps walking away from the viewer along the road toward the crest, one "
        "continuous steady stride the whole clip, his back to the viewer, the beam steady "
        "across his shoulders, never turning; the tiny figures at the crest keep walking away "
        "at the same pace, never turning, not yet going over the crest; the blue-and-gold ink "
        "threads drift smoothly within their own fixed band across the whole sky above the "
        "road; a low thin haze of dust drifts along the road; no new stain, spot, or "
        "darkening appears anywhere on the page at any point."
    ),
    fence_kind="none",
    caption_lines=("You are asked",),
    corner_note="NOTE: freely this time",
    refs=[R_SIMON, R_CROSS, R_JESUS, R_SOLDIERS, R_ROAD],
    model_tier="veo3_1_lite",
    clip_duration=8,
    panel_style="woodcut_hybrid",
)

PAGES = {
    "f01": F01, "f02": F02, "f03": F03, "f04": F04, "f05": F05,
    "f06": F06, "f07": F07, "f08": F08, "f09": F09,
}

# ---- covers -------------------------------------------------------------
# The hook is a man walking the other way; the landing is "He went out
# through that gate first." Covers are the two ends of one doorway: SIMON
# walking toward it, empty-shouldered, while the tiny procession comes out
# of it the other way (front); the same GATE at dusk, empty, with two lines
# of footprints running out from its threshold (back). Neither cover shows
# the beam -- the front is before it, the back is after it.

FRONT_COVER = CoverSpec(
    side="front",
    scene=(
        f"{SIMON_BUILD} in full figure, large in the lower third at the frame's "
        f"center-right, walking from right to LEFT along a dry dirt road in profile, "
        f"mid-stride, {SIMON_UNBURDENED}, his head-cloth tied at the nape, his rust-striped "
        "mantle over his left shoulder, an ordinary countryman on an ordinary morning; the "
        "road runs along the foot of a high wall of great dressed pale-gold limestone "
        f"blocks toward the tall squared gate of the city at the far left ({GATE_BUILD}); IN "
        "the gate's opening, small and far, the procession coming OUT the other way -- "
        f"{JESUS_BUILD}, walking right, completely UNBURDENED -- his shoulders bare of any "
        "beam or burden, nothing resting on them, both his hands empty at his sides -- a "
        f"soldier's hand on his upper arm, leading him; both of {SOLDIERS_BUILD} walking "
        "with him, one on each side -- NO wood, beam, timber, or object of any kind is "
        "carried by anyone in this small distant group; at this small, far-away size a "
        "carried timber cannot be drawn reliably as a single plank and keeps misreading as a "
        "cross shape, so this beat is told WITHOUT the beam at all: three small figures "
        "walking out through the doorway together, empty-handed, tiny against the doorway, "
        "none of them looking at Simon and Simon not looking at them; behind Simon at the "
        "right the road comes in over a low stony rise "
        "from open country. The artwork fills the frame completely edge to edge -- no "
        "picture-frame border, no black outline, no drawn frame of any kind around the image."
    ),
    lighting=(
        "Warm early-morning gold from the open country at the right, low behind Simon, "
        "rim-lighting his shoulders and the dust of the road he has walked; cold blue-grey "
        "shadow filling the gate's opening and the shadowed face of the wall at the left, "
        "the procession inside it in that cold."
    ),
    title="THE CROSS THAT WASN'T HIS",
    subtitle="MARK 15",
    title_position="top",
    animation=(
        "Simon takes only a few small, unhurried steps in place along the road, his empty "
        "hands swinging gently, his mantle's loose edge stirring, his body staying in "
        "exactly the same large center-right position and exactly the same size he is "
        "drawn in -- he must stay prominently and fully in frame for the ENTIRE clip, his "
        "full figure always clearly visible, NEVER walking toward either edge of the frame, "
        "NEVER approaching the frame's right edge, NEVER becoming cropped or partly cut off "
        "by the frame at any point, not even in the final moment of the clip; this is a small "
        "shift of weight and stride, not a journey -- he ends the clip exactly as prominent "
        "and fully visible as he began it; the small figures in the gate's opening hold "
        "exactly as drawn, still; the warm morning light behind him stays exactly as warm "
        "and low as it already is, unchanged for the whole clip; the cold shadow in the "
        "gate's opening stays exactly as cold and dim as it already is; the wall and the "
        "gate stay exactly as drawn; no new figure, mark, or text appears."
    ),
    extra_avoid=(
        "a full cross shape, a crucifix, a dragged cross, a crown of thorns, blood, wounds, "
        "gore, a crowd, a hill with crosses, any bundle or staff or pack carried, any figure "
        "touching another except a soldier's hand on an arm, modern clothing, Simon exiting "
        "or approaching the frame's edge, Simon becoming cropped or partly cut off"
    ),
    refs=[R_SIMON, R_SIMON_FACE, R_GATE, R_JESUS, R_SOLDIERS, R_CROSS],
    clip_duration=5,
)

BACK_COVER = CoverSpec(
    side="back",
    scene=(
        f"the gate of the city ({GATE_BUILD}) seen from outside at dusk, filling the left "
        "half of the frame and rising past its top -- the tall squared opening in the high "
        "pale-gold wall, its timber doors standing open, the doorway EMPTY, the shadowed "
        "lane beyond it empty, no figure anywhere on the image; the broad worn threshold "
        "stone across the doorway's foot, large and low in the frame; from that threshold, "
        "TWO SEPARATE, CLEARLY DISTINCT trails of bare footprints in the dust, side by side, "
        "running away to the RIGHT and out over the low stony rise -- this is explicitly NOT "
        "one person's own natural alternating left-right walking gait (which would show a "
        "single zigzag line of prints); it is TWO DIFFERENT people's tracks, each its own "
        "straight single-file line of prints, running parallel and close together the whole "
        "way, the second trail's prints consistently one full pace further back than the "
        "first trail's prints at every point along the road, both trails equally visible and "
        "equally clear from the threshold all the way to the rise -- plain marks in dust, no "
        "figure; from the threshold "
        "stone itself, not from the footprints and not from the road, the blue ink motif, "
        "with a trace of muted gold, rises and drifts out in the SAME long, loose, open "
        "thread used throughout this episode's own sky (see F07/F09's Stage 3 band) -- one "
        "continuous flowing line, longer than it is tall, running out over the road above "
        "the two lines of footprints and following their own path toward the rise, tied to "
        "no figure, touching no footprint, touching no ground; flat and two-dimensional, "
        "drawn ON the paper's surface, a single continuous brushstroke, never a hook, never "
        "a comma shape, never a closed curl, never a spiral, never a ring, never a bracelet, "
        "never a bangle, never jewelry, never metallic, never reflective, behaving like a "
        "long thread of wet ink bled into the paper's own sky wash, never a glow, never a "
        "blot; the road beyond the rise EMPTY under carved cloud forms in an open dusk sky."
    ),
    lighting=(
        "Warm last dusk gold lying low across the road OUTSIDE and along the two lines of "
        "footprints running out to the right; cold blue dusk holding the wall, the doorway, "
        "and the empty lane inside it at the left."
    ),
    title="THROUGH THAT GATE FIRST",
    subtitle="HEBREWS 13:13",
    title_position="bottom",
    animation=(
        "the two lines of title lettering at the bottom of the frame are baked into the paper "
        "itself, like carved wood -- they cannot fade, dissolve, thin, or disappear at any "
        "point in the clip, remaining fully opaque, fully legible, and pixel-identical from the "
        "very first frame to the very last frame with zero exceptions; if the lettering is even "
        "slightly fainter or partly covered in a later frame than in the first frame, that is "
        "wrong; a thin, sparse veil of fine dust drifts slowly and low along the empty road "
        "outside the gate in the dusk wind, staying well above and clear of the lettering the "
        "entire time and never thickening into a haze, mist, or fog that dims, blurs, or "
        "covers any part of the lettering or the ground beneath it; the long blue-gold thread "
        "above the footprints drifts smoothly within its own fixed line, exactly as drawn, for "
        "the whole clip; the two lines of footprints lie still, exactly as drawn and fully "
        "visible the whole clip; the warm light across the road stays exactly as warm and low "
        "as it already is, unchanged; the cold dusk in the doorway stays exactly as cold and "
        "dim as it already is; the gate and wall stay exactly as drawn; no new figure, mark, "
        "or text appears."
    ),
    extra_avoid=(
        "any human figure, a face, a hand, a cross of any shape, a beam or timber, a hill, "
        "jewelry, bright neon, a drawn border or caption strip, the title lettering fading, "
        "dimming, thinning, or disappearing at any point, dust or haze or fog thickening over "
        "or obscuring the lettering or the footprints"
    ),
    refs=[R_GATE],
    clip_duration=10,
)

COVERS = {"front": FRONT_COVER, "back": BACK_COVER}

# ---- assembly manifest ---------------------------------------------------
# Word weights are Fable's own count against the locked narration (sum 227,
# matching narration.md; 103.44s locked audio, natural speed, no
# time-stretch, one narrator turn). Final modes are an assembly-QC call on
# the real renders, per the standing rule -- real slots come from
# narration.alignment.json (forced-align first), not this word-proportional
# estimate.

MANIFEST = EpisodeManifest(
    episode_dir=HERE,
    narration=HERE / "narration.mp3",
    units=[
        Unit("front", HERE / "front_cover.mp4", 14, "freeze"),
        Unit("f01", HERE / f"{HERE.name}_f01_9x16.mp4", 25, "freeze"),
        Unit("f02", HERE / f"{HERE.name}_f02_9x16.mp4", 21, "freeze"),
        Unit("f03", HERE / f"{HERE.name}_f03_9x16.mp4", 22, "freeze"),
        Unit("f04", HERE / f"{HERE.name}_f04_9x16.mp4", 14, "freeze"),
        Unit("f05", HERE / f"{HERE.name}_f05_9x16.mp4", 28, "freeze"),
        Unit("f06", HERE / f"{HERE.name}_f06_9x16.mp4", 28, "freeze"),
        Unit("f07", HERE / f"{HERE.name}_f07_9x16.mp4", 17, "freeze"),
        Unit("f08", HERE / f"{HERE.name}_f08_9x16.mp4", 13, "freeze"),
        Unit("f09", HERE / f"{HERE.name}_f09_9x16.mp4", 21, "freeze"),
        Unit("back", HERE / "back_cover.mp4", 24, "freeze"),
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
