"""Day of Atonement LONG (16:9 living-sketchbook, EW01 Two Goats narration) --
step 4: animate the paid-generative spreads. Follows bronze_serpent_long's
_s4_animate.py pattern EXACTLY: imports the shared driver from
poc_comic_page/_animate_piece1_v2.py, reuses its LOCK/NOGLITTER camera-locked,
INVENT-NOTHING, named-ambient-motion-only prompting, run_job_with_fallback,
and the cost note-override. Kling for multi-figure/crowd/gesture spreads,
Seedance for calm single-figure spreads (cost-tiered), and Seedance ALWAYS for
Christ/crucifixion iconography regardless of complexity (living-light-no-
fresh-blood: Kling has REGENERATED blood/wounds from crucifixion iconography
even on a retouched-clean still).

An earlier session wrongly assumed the standard /animate-long veo3_1_lite
recipe applied to this episode -- it does NOT. This living-sketchbook style's
only proven precedent is bronze_serpent_long's own Kling/Seedance pipeline;
this file mirrors it, not /animate-long.

ASPECT: "16:9" (this project's long-form format, NOT the shorts' 9:16).

COUNT (flagged, not silently fixed): the plan (_PLAN.md) has 76 spreads.
Of those, 4 are NOT in the JOBS list below, each for a distinct reason:

  - s54_guilt_laid_on_christ / s55 (no still of its own -- composites onto
    s54): ALREADY BUILT as a bespoke $0 compositing device (gold Thread +
    letterpressed verse + focal-tour spotlight camera) by
    _s3_thread_leaf_54_55.py in this same folder. Do not touch it, do not
    re-animate it here.
  - s76_already_inside (LAND type, the film's landing): EXCLUDED by the same
    rule bronze_serpent_long applied to its own s68_landing -- "tear_hole"
    is the landing's own $0 mandatory device (page tears open AS the veil,
    gold light from beneath, sacred stillness). Bronze Serpent's own
    _s4_animate.py docstring is explicit that its landing spread "gets NO
    pan of its own -- it's a static held frame revealed by the tear_hole
    transition at assembly time." Same logic applies here verbatim: s76
    needs a static held frame + a tear_hole compositing pass, not a paid
    Kling/Seedance clip. Not a JOBS entry on purpose.
  - s75_the_reach: EXCLUDED from this batch on purpose -- flagged for a
    SEPARATE human decision, see below. Real controlled motion (Christ's
    hand reaching toward the viewer) is intentional here, per the plan's own
    Device column: "designed acting spread (Kling tier, fail-closed Jesus
    QC)". This is the one spread in the whole episode where a generative
    animator must convincingly complete a specific Christ gesture and hold
    it -- both the wound-risk register (Christ) and the acting-spread risk
    register (a completed, non-frozen motion) stack here at once. It needs
    its own prompt, its own extra-scrutiny QC pass, and an explicit human
    go-ahead before it is batched with everything else -- not a silent
    default the way s29 (Aaron's much lower-stakes acting spread) got one.

  => 72 runnable jobs below: 62 Seedance + 10 Kling.

VERIFICATION METHOD (flagged): every prompt below is grounded in _PLAN.md's
own Shows/Assets/Device text for that spread, per this project's standing
no-lazy-prompting rule. Additionally, ~16 of the 72 stills were opened and
eye-checked at full res before writing their prompts (across every spread
"class" in the episode: verse cards, multi-vignette, object/hand close-ups,
Christ portraits, the acting spread, the crucifixion). That spot-check caught
THREE real drift-from-plan cases the table text alone would have gotten
wrong: s36's "two lots turned over in his hand" is actually rendered as
lots/bowls RESTING ON A TABLE with his hands clasped, not held; s34 and s65
are both close-up Aaron-face portraits with one or two SMALL background
insets, not equal-weight multi-vignette compositions, so both moved from the
MV-default Kling tier to Seedance + PAGE (talking-head risk). The other ~56
prompts are grounded in the plan text alone, following bronze_serpent_long's
own proven conservative discipline (freeze everything not explicitly named,
license only ambient elements the text or asset list actually implies) --
eye-check the actual stills against these prompts before running "all".

VC / LETTERING NOTE: unlike a still carrying pre-baked lettering, every VC
(verse-card) spread's still here was confirmed at full res to have a BLANK
paper margin reserved for text -- the live Scribed-Ink / Illuminated-Rubric /
composite-over-art reveal is a SEPARATE $0 compositing pass added later
(same pipeline position as bronze_serpent_long's own _s10_captions.py, run
after assembly), never something asked of the animator. TEXTLOCK below is
still applied to every VC job as insurance against the animator inventing
false lettering-like marks in that blank space -- exactly bronze_serpent_long's
own reasoning (its own VC stills are equally blank; TEXTLOCK there is also
preventative, not protecting real baked-in letters).

ACTING SPREADS: two spreads in this episode carry the plan's own "designed
acting spread" tag (a still capturing a motion in progress that the clip
must complete and hold, not the usual full-clip freeze): s29 (Aaron's hand
settling onto the goat's head) and s75 (excluded above, Christ's hand
reaching -- separate human decision). s29 is included below with a custom
prompt licensing exactly that one settling motion.

FROZEN-MID-STRIKE CLASS CHECK: this project's Bronze Serpent pilot excluded
2 spreads (a hammer mid-swing, a pole mid-shatter) because three independent
generative attempts all invented a completed strike. Every spread description
in this episode's _PLAN.md was checked against that failure class -- NONE
of the 76 spreads shows a raised/mid-swing implement or an object in flight.
The closest content is s25 (a knife at the altar, explicitly "staged,
wound-free," not mid-strike) -- included below on the Kling tier with an
ELEVATED RISK comment and a $0 fallback recommendation, not excluded outright.
s50 (THE SHADOW) is flagged for a different but related reason: Bronze
Serpent's own docstring documents a shadow-SHAPE doctrinal-inversion failure
(a cross-shaped shadow redrew itself as a serpent) when a meaningful,
unexplained shadow was left for the animator to reinterpret -- s50 is the
same content class (an unexplained shadow cast by something beyond the
frame) and carries the same elevated-risk flag + eye-check note, not an
exclusion.

MULTI-STAGE HARD-CUT PAIRS (flagged per this project's own resume notes):
spreads 10/11 (strange fire), 25/26/27 (slaying through the veil), and
61/62 (whole veil -> torn veil) each need their OWN individual animate job
below (they are NOT skipped or merged) -- but at the ASSEMBLY stage they
must be spliced together as a true hard cut, never a dissolve or morph.
Differing providers within a pair (e.g. s25 Kling, s26/s27 Seedance) are
fine -- it is a hard cut, not a continuity blend, so there is no requirement
that a pair share a provider.

CAMERA-PUSH DEVICES: several spreads' own Device column calls for a slow
push-in or slow drift (s04, s16, s51, s74, among others). Exactly as
bronze_serpent_long's own docstring notes: generated clips here are
camera-LOCKED (LOCK forbids all camera movement), so any push/drift the plan
wants must be added deterministically at assembly regardless of what runs
here.

DURATION GAPS (for the assembly stage): every clip is capped at 8s max
(seedance1_5 only accepts 4/8/12; Kling used at 5 throughout). Spreads whose
_PLAN.md on-screen hold exceeds 8s rely on assembly looping/hold-extension
per longform-motion-fill -- 27 of them: s04 (8.3s), s14 (9.7), s16 (18.3),
s18 (10.0), s19 (11.0), s31 (21.5), s32 (8.2), s34 (9.3), s36 (9.2), s37
(9.2), s40 (11.1), s41 (9.2), s42 (10.3), s44 (9.9), s47 (8.1), s48 (10.3),
s49 (10.5), s51 (13.8), s52 (10.4), s56 (10.7), s57 (10.5), s59 (9.5), s65
(11.5), s67 (9.0), s68 (9.5), s71 (8.5), s74 (12.7). Four of these are the
plan's own explicitly-named "four heaviest moments" (confession live-write
s31, the LORD's charge s16, the Jesus pivot s51, the final "will you come
in?" s74) -- those four get duration=8 below (all other Seedance jobs use
duration=4); the rest stay at the default 4s/5s and rely entirely on
assembly-stage looping.

STYLE-VARIANT NOTE (not a JOBS concern, flagged for completeness): the
plan's own s13 is a candidate for the sl13 charcoal-and-eraser style variant,
pending a user decision + an Aaron identity test (_PLAN.md section 6). The
rendered still (`s13_door_curtain_sl13.png`) already carries the sl13
filename suffix. This does not change s13's animate treatment below --
its content (Aaron gripping his robe at the door-curtain) is animated the
same way regardless of which ink style the still itself ended up in.

TEST GATE: exactly 3 jobs run unless "all" or an explicit list is passed --
one per risk tier: s17_squared_at_veil (calm single-figure Seedance, the
most common spread class), s07_nation_outside (crowd/gesture Kling),
s53_the_cross (crucifixion Seedance, wound-lock language).

  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s4_animate.py            # test gate (3 jobs)
  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s4_animate.py all         # full batch
  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s4_animate.py s01_cold_open,s53_the_cross  # explicit subset

NOTHING IN THIS FILE HAS BEEN RUN. No `hf generate create` call, no spend,
no test-gate execution -- planning/script-writing only, per the task that
produced it. Get an explicit cost go-ahead before running anything.
"""
import contextlib
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
HERE = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location(
    "_anim", ROOT / "poc_comic_page" / "_animate_piece1_v2.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
A.EPISODE = "LS_DayOfAtonementLong"
A.OUT = HERE / "clips"
A.OUT.mkdir(exist_ok=True)

STILLS = HERE / "stills"
ASPECT = "16:9"  # long-form -- NOT the short's 9:16

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, torn edges, and every sketch line hold perfectly still. ")
NOGLITTER = ("the light stays a steady, even glow -- it does not sparkle, "
             "flicker into particles, or scatter into glitter. ")
# Verse-card letter-freeze guard (never-animate-writing: letters garble).
# Every VC still here has a BLANK card margin (confirmed at full res), so
# this is preventative -- guarding against the animator inventing false
# lettering-like marks in that blank space -- not protecting real text.
TEXTLOCK = ("Every lettered word and every stroke of any handwritten text "
            "stays pixel-identical and perfectly legible -- no letter warps, "
            "redraws, shimmers, or changes in any way. ")
# Crucifixion/Christ wound-freeze guard (living-light-no-fresh-blood).
WOUND_LOCK = ("His hands and feet stay exactly as drawn, with no wound, no "
              "blood, no red mark, no nail, no puncture appearing or "
              "growing anywhere on them at any point in the clip. ")

# Self-contained-portrait reframe (bronze_serpent_long's proven fix for the
# talking-head/direct-address defect class: a close facial hold reads as an
# interview prior to Kling/Seedance, inventing lip movement or a push-zoom).
# Reframes the subject as "a finished drawing being filmed," never a live
# person -- full prompt replacement, no LOCK prepend, used only for names in
# SELF_CONTAINED below. Applied here PROPHYLACTICALLY (this episode has no
# redo-round history yet) to every close facial expression-hold / direct-
# address spread, since that is exactly the failure class Bronze Serpent had
# to discover the hard way across a dozen redo rounds.
PAGE = ("A finished ink-and-watercolor drawing on an aged sketchbook page, "
        "filmed as a perfectly still page under steady light. The framing "
        "stays fixed and locked for the entire clip. The drawing is "
        "finished and dry: every figure, face, hand, and object in it is "
        "ink on paper and stays exactly as drawn from the first frame to "
        "the last. ")
SELF_CONTAINED = {
    "s01_cold_open", "s08_curtain_shut", "s09_grief_close", "s30_confession",
    "s34_riddle_recap", "s39_honesty_close", "s51_jesus_pivot",
    "s56_the_answer", "s64_empty_hands", "s65_ritual_uninks",
    "s73_aaron_steps_aside", "s74_every_year_gone",
}

# Spreads showing Christ -- wound-risk-critical. A Seedance failure here
# must NEVER silently substitute Kling (main() below calls A.run_job
# directly, no fallback, for anything in this set) -- a real failure should
# stop and ask a human, not quietly reintroduce the exact risk the Seedance-
# always rule exists to avoid.
NO_KLING_FALLBACK = {
    "s51_jesus_pivot", "s52_jesus_entering_formal", "s53_the_cross",
    "s56_the_answer", "s57_without_the_gate", "s60_seated_glory",
    "s66_high_priests_face", "s75_the_reach",
}

# TEST GATE default: exactly these 3 run unless overridden on the command line.
TEST_GATE = ("s17_squared_at_veil", "s07_nation_outside", "s53_the_cross")

# (name, provider, duration, motion)
JOBS = [
    # --- Beat 1: I was there (spreads 1-8) ---
    ("s01_cold_open", "seedance", 4,
     PAGE +
     "Aaron's face and shoulders stay exactly as drawn, his gaze and "
     "expression fixed, mouth closed. The only movement in the whole clip: "
     "the light across the page breathes very gently. Nothing else "
     "changes."),
    # Note: the /blue-line ink-arrival reveal ("the page being made IS the
    # hook") is a separate $0 compositing pass over this base clip, added
    # later -- same pattern bronze_serpent_long used for its own blue-line
    # spread (s04_icon_pole), which also got a normal animate job here.

    ("s02_tabernacle_wide", "seedance", 4,
     LOCK +
     "The tabernacle, its linen courtyard, and the desert beyond hold their "
     "exact shapes and positions, perfectly still. Only: faint dust drifts "
     "low across the open ground, the linen hangings stir very slightly in "
     "the wind, and the desert light breathes very gently. Nothing else "
     "changes."),

    ("s03_golden_garments", "seedance", 4,
     LOCK +
     "Aaron's hands and the breastplate, robe, and mitre laid on the stone "
     "ledge all hold their exact positions, perfectly still -- his fingers "
     "do not lift, grip, or move, and none of the garments shifts, lifts, "
     "or is picked up. Only: the light across the gold and jewels breathes "
     "very gently. Nothing else changes."),

    ("s04_donning_linen", "seedance", 4,
     LOCK +
     "Aaron holds his exact posture, hands at the girdle knot, perfectly "
     "still -- his fingers do not tie, pull, or move further, and the "
     "bronze laver behind him holds its exact position. Only: the linen "
     "fabric stirs very slightly, faint light breathes across the scene. "
     "Nothing else changes."),
    # Plan's own slow push-in is added at assembly -- camera stays locked here.

    # EXCLUDED after 2 generative attempts (2026-08-04): the woven cherub
    # figures on the veil kept flapping/distorting their wings even with
    # the wings explicitly named and locked in round 2 -- same failure
    # class as s53's robe (fine embroidered/fabric detail Seedance won't
    # reliably hold still for). $0 dynamic_cam3d push instead, via
    # _s05_orbit.py in this folder. Both defective attempts kept for the
    # record: s05_walking_to_veil.v1_flying_wings_defect.mp4 (round 1) and
    # .v2_flying_wings_defect.mp4 (round 2, wings still moving).
    # ("s05_walking_to_veil", "seedance", 4, ...),

    ("s06_holy_of_holies_empty", "seedance", 4,
     LOCK +
     "The mercy seat, the cherubim, and the stone chamber hold their exact "
     "shapes and positions, perfectly still -- the room stays empty, no "
     "figure or form ever appears. Only: the golden cloud-glow above the "
     "mercy seat pulses very gently brighter and dimmer in a steady, even "
     "glow -- " + NOGLITTER + "Nothing else in the frame moves."),

    # === TEST GATE JOB (crowd/gesture Kling tier) ===
    # REDO round 1 (2026-08-04): first attempt invented a new figure walking
    # into the empty courtyard partway through the clip (confirmed by a
    # start-vs-mid frame crop comparison) -- a real NOINVENT violation, not a
    # style nitpick. Strengthened per this project's own fix pattern: reframe
    # as ink on paper being filmed (not a photograph of a live crowd, which
    # primes a documentary/newsreel prior), and explicitly name the exact
    # empty space that got violated rather than relying on a general
    # "nothing new" line alone.
    ("s07_nation_outside", "kling", 5,
     LOCK +
     "This is a finished ink-and-watercolor drawing on an aged page, filmed "
     "as a perfectly still page under steady light -- not a photograph of a "
     "real crowd. Every one of the hundreds of tiny figures is ink on paper "
     "and stays exactly as drawn, frozen, for the entire clip -- no one "
     "steps, turns, gestures, or walks. The empty courtyard between the "
     "gate and the tabernacle stays completely empty from the first frame "
     "to the last -- no figure enters it, nothing crosses it. INVENT "
     "NOTHING new anywhere in the frame. Only: faint dust drifts across the "
     "outer ground, the tabernacle's linen hangings stir very slightly in "
     "the wind. Nothing else changes."),

    ("s08_curtain_shut", "seedance", 4,
     PAGE +
     "Aaron's face stays exactly as drawn in the darkness, his expression "
     "and gaze fixed, mouth closed. The curtain behind him holds its exact "
     "folded shape. The only movement in the whole clip: the faint light "
     "across his face breathes very gently. Nothing else changes."),

    # --- Beat 2: the world / grief + the charge (spreads 9-21) ---
    ("s09_grief_close", "seedance", 4,
     PAGE +
     "Aaron's face stays exactly as drawn, his grieving expression fixed, "
     "mouth closed, eyes unmoving. The only movement in the whole clip: "
     "the light across his face breathes very gently. Nothing else "
     "changes."),

    ("s10_strange_fire", "kling", 5,
     LOCK +
     "This is a finished ink-and-watercolor drawing on an aged page, not a "
     "photograph of real men -- Nadab and Abihu hold their exact postures "
     "over their censers, perfectly frozen -- no gesture, no step, no "
     "change of expression. INVENT NOTHING new. Only: the strange fire in "
     "the censers glows and breathes very gently brighter and dimmer -- " + NOGLITTER +
     "faint smoke curls very slowly upward. Nothing else in the frame "
     "changes."),
    # Multi-stage hard cut with s11 -- assembly must splice as a true hard
    # cut, never a dissolve/morph (this project's own resume-note rule).

    ("s11_struck_down", "kling", 5,
     LOCK +
     "This is a finished ink-and-watercolor drawing on an aged page, not a "
     "photograph -- the ground and the fallen censers hold their exact "
     "positions, perfectly still. No figure, face, or form ever appears "
     "within the light, and none enters the frame from any edge. Only: the "
     "fire and light falling from above pulses very gently brighter and "
     "dimmer in a steady, even glow -- " + NOGLITTER +
     "Nothing else in the frame moves."),
    # Pair with s10, hard cut (see above).

    ("s12_bodies_carried_out", "kling", 5,
     LOCK +
     "This is a finished ink-and-watercolor drawing on an aged page, not a "
     "photograph of real men -- the two bearers carrying the wrapped "
     "bodies hold their exact posture and stride, perfectly frozen -- no "
     "further steps, no shift of grip. INVENT NOTHING new -- no new bearer "
     "or figure enters the frame. Only: faint dust drifts across the "
     "ground, cloth stirs very slightly. Nothing else in the frame "
     "changes."),

    ("s13_door_curtain_sl13", "seedance", 4,
     LOCK +
     "Aaron holds his exact posture, one hand gripping the robe firmly at "
     "his chest, perfectly still -- his grip never loosens, tightens, or "
     "moves, and he does not rend or move the fabric. The door-curtain "
     "behind him holds its exact folded shape. Only: the light across the "
     "scene breathes very gently. Nothing else changes."),

    ("s14_hand_at_veil", "seedance", 4,
     LOCK +
     "Aaron's hand at the veil's edge holds its EXACT position, perfectly "
     "still -- the fingers do not curl, lift, or move, and the veil's "
     "fabric under them does not shift or part. Only: the light across "
     "the scene breathes very gently. Nothing else changes."),

    # REDO round 1 (2026-08-04, user eye-check): "weird eye moments" --
    # Moses's eyebrows/eyes were doing a real squint-and-furrow cycle across
    # the clip despite "no change of expression." Named explicitly below
    # (eyes/eyelids/eyebrows), matching the fix pattern that worked for s07.
    ("s15_moses_charge", "kling", 5,
     LOCK +
     "This is a finished ink-and-watercolor drawing on an aged page, not a "
     "photograph of real men -- Moses and Aaron both hold their exact "
     "postures and expressions, perfectly frozen -- no gesture, no step, "
     "no change of expression. Both men's eyes stay open at their exact "
     "drawn width, eyebrows and eyelids never move -- no blink, no squint, "
     "no furrow. INVENT NOTHING new -- no third figure ever appears. Only: "
     "faint light breathes across the scene, cloth stirs very slightly. "
     "Nothing else in the frame changes."),

    ("s16_lords_charge_card", "seedance", 8,
     LOCK + TEXTLOCK +
     "The ark, the cherubim, and the stone chamber behind the card's "
     "blank margin hold their exact shapes and positions, perfectly "
     "still. Only: the golden cloud-glow above the mercy seat pulses very "
     "gently brighter and dimmer in a steady, even glow -- " + NOGLITTER +
     "Nothing else in the frame moves."),
    # duration=8: one of the plan's own 4 heaviest-hold spreads (18.3s on
    # screen -- the film's central charge). The Scribed Ink whole-arrival
    # lettering and the plan's slow push are both added later, not by this
    # clip; assembly still needs to loop/extend past 18.3s.

    # === TEST GATE JOB (calm single-figure Seedance tier) ===
    ("s17_squared_at_veil", "seedance", 4,
     LOCK +
     "Aaron holds his exact squared stance before the veil, perfectly "
     "still -- no gesture, no step. The veil holds its exact folded shape. "
     "Only: the light across the scene breathes very gently. Nothing else "
     "changes."),

    ("s18_own_sin_first", "seedance", 4,
     LOCK +
     "Aaron holds his exact posture, both hands steady on the basin, "
     "perfectly still -- his grip never shifts, and nothing is poured, "
     "lifted, or spilled. Only: the light across the scene breathes very "
     "gently. Nothing else changes."),

    ("s19_altar_ministry", "seedance", 4,
     LOCK +
     "Aaron and the altar hold their exact positions, perfectly still -- "
     "no gesture, no step. Only: the smoke from the altar rises and curls "
     "very slowly upward, faint light breathes across the scene. Nothing "
     "else changes."),

    ("s20_blood_atonement_card", "seedance", 4,
     LOCK + TEXTLOCK +
     "The altar and the smoke behind the card's blank margin hold their "
     "exact shapes, perfectly still. Only: the smoke curls very slowly "
     "upward, the light breathes very gently. Nothing else changes."),

    ("s21_goat_innocent", "seedance", 4,
     LOCK +
     "The goat holds its exact gaze and posture, perfectly still -- no "
     "blink, no head turn. Only: the light across its face breathes very "
     "gently, its coat catches the light. Nothing else changes."),

    # --- Beat 3: the act (spreads 22-33) ---
    ("s22_ritual_hands", "seedance", 4,
     LOCK +
     "Aaron's hands hold their EXACT position, perfectly frozen -- no "
     "finger moves, nothing is lifted or gathered. Only: the light across "
     "his hands breathes very gently. Nothing else changes."),

    ("s23_two_goats_brought", "kling", 5,
     LOCK +
     "This is a finished ink-and-watercolor drawing on an aged page, not a "
     "photograph of a real scene -- Aaron, the handlers, and both goats "
     "hold their exact positions, perfectly frozen -- no one steps, "
     "gestures, or changes posture, and neither goat moves. INVENT NOTHING "
     "new -- no new person or animal ever enters the frame. Only: faint "
     "dust drifts across the ground, cloth stirs very slightly. Nothing "
     "else in the frame changes."),

    ("s24_lots_card", "seedance", 4,
     LOCK + TEXTLOCK +
     "Aaron's hands and both goats behind the card's blank margin hold "
     "their exact positions, perfectly still -- neither goat moves. Only: "
     "the light breathes very gently. Nothing else changes."),

    ("s25_slaying_stage1", "kling", 5,
     LOCK +
     "This is a finished ink-and-watercolor drawing on an aged page, not a "
     "photograph of a real scene -- Aaron, the altar, and the goat hold "
     "their exact positions, perfectly frozen -- the goat does not move, "
     "no strike, no cut, no motion of the knife occurs at any point in the "
     "clip; nothing changes state. INVENT NOTHING new -- no wound, no "
     "blood, no red mark appears anywhere at any point, and no new figure "
     "ever enters the frame. Only: faint light breathes across the scene. "
     "Nothing else in the frame moves."),
    # ELEVATED RISK: a knife-adjacent staged tableau is the same general
    # content family as this project's documented mid-strike failures
    # (though nothing here is drawn mid-swing -- explicitly staged/at-rest
    # per the plan). Eye-check first/mid/last frames before accepting; a $0
    # push-in is the fallback if the knife or goat show any invented
    # motion. Multi-stage hard cut with s26/s27 -- splice as a true hard
    # cut at assembly, never a dissolve/morph.

    ("s26_through_veil_stage2", "seedance", 4,
     LOCK +
     "Aaron, half-swallowed by the curtain, and the basin in his hands "
     "hold their exact positions, perfectly still -- his grip on the "
     "basin never shifts, nothing spills. The veil holds its exact "
     "folded shape. Only: the light breathes very gently. Nothing else "
     "changes."),

    ("s27_sprinkling", "seedance", 4,
     LOCK +
     "Aaron and the mercy seat hold their exact positions, perfectly "
     "still -- his hand never moves, nothing is sprinkled or poured at "
     "any point in the clip. Only: the golden cloud-glow pulses very "
     "gently brighter and dimmer in a steady, even glow -- " + NOGLITTER +
     "Nothing else in the frame moves."),

    ("s28_bring_blood_card", "seedance", 4,
     LOCK + TEXTLOCK +
     "The dark chamber behind the card's blank margin holds its exact "
     "shape, perfectly still. Only: the light breathes very gently. "
     "Nothing else changes."),

    ("s29_hands_on_goat", "kling", 5,
     "The camera does not move, zoom, or change angle at all. Aaron's "
     "hand, already resting at the goat's head, presses gently down and "
     "settles fully onto the goat's head within the first two seconds of "
     "the clip, then holds that exact final position, perfectly still, "
     "for the rest of the clip -- the motion happens once and completes, "
     "it never repeats, reverses, or continues. The goat holds its exact "
     "posture throughout, its head steady under the hand, no other part "
     "of the goat or of Aaron moves. INVENT NOTHING new beyond this one "
     "settling motion. Only after the hand settles: the light across the "
     "scene breathes very gently. Nothing else in the frame ever moves."),
    # Designed acting spread (Kling tier, per the plan's own Device
    # column) -- the lower-stakes of the episode's 2 acting spreads (the
    # other, s75, is Christ and is excluded above for a separate human
    # decision). Eye-check that the motion completes once and holds,
    # rather than looping or drifting.

    ("s30_confession", "seedance", 4,
     PAGE +
     "Aaron stays exactly as drawn: head bowed, eyes shut, mouth closed, "
     "both hands resting still on the goat's head. The goat holds its "
     "exact posture. The only movement in the whole clip: the light "
     "across the scene slowly and very slightly brightens and dims. "
     "Nothing else changes."),
    # The plan's own text says his mouth is "moving" (the spoken
    # confession) -- licensing lip movement is this project's single most
    # common animator-defect class (see bronze_serpent_long's own repeated
    # "REDO ROUND" fixes on exactly this), so the confession is carried by
    # his bowed posture, mouth locked closed, from the first attempt.

    ("s31_confession_card", "seedance", 8,
     LOCK + TEXTLOCK +
     "Aaron and the goat in the background art behind the card's blank "
     "margin hold their exact positions, perfectly still. Only: the "
     "light breathes very gently. Nothing else changes."),
    # duration=8: one of the plan's own 4 heaviest-hold spreads (21.5s --
    # the film's longest single card, the confession live-write). The live
    # glyph-by-glyph Scribed Ink reveal is composited later, not by this
    # clip; assembly must loop/extend well past 21.5s.

    ("s32_goat_led_away", "seedance", 4,
     LOCK +
     "The fit man and the goat hold their exact positions on the path, "
     "perfectly frozen -- no further steps, no pulling on the tether. "
     "INVENT NOTHING new. Only: faint dust drifts low across the ground. "
     "Nothing else in the frame changes."),

    ("s33_empty_horizon_card", "seedance", 4,
     LOCK + TEXTLOCK +
     "The empty wilderness horizon behind the card's blank margin holds "
     "its exact shape, perfectly still. Only: the light breathes very "
     "gently, faint dust drifts low across the ground. Nothing else "
     "changes."),

    # --- Beat 4: the strange detail / the riddle (spreads 34-38) ---
    ("s34_riddle_recap", "seedance", 4,
     PAGE +
     "Aaron's face stays exactly as drawn, his expression fixed, mouth "
     "closed. The two memory vignettes behind him -- the goat at the "
     "altar and the goat receding on the path -- hold their exact shapes "
     "and positions, perfectly still; neither goat moves. The only "
     "movement in the whole clip: the light across the page slowly and "
     "very slightly brightens and dims. Nothing else changes."),
    # Eye-checked: a close Aaron-face portrait with 2 small background
    # insets, not an equal-weight multi-vignette -- moved from the MV
    # default (Kling) to Seedance + PAGE (talking-head risk dominates
    # here). Optional INK STAMP "WHY TWO?" overlay is a later $0
    # compositing pass, not part of this clip.

    ("s35_two_kids_card", "seedance", 4,
     LOCK + TEXTLOCK +
     "Both goats behind the card's blank margin hold their exact "
     "positions, perfectly still -- neither moves. Only: the light "
     "breathes very gently. Nothing else changes."),

    ("s36_two_shadows_one_flame", "seedance", 4,
     LOCK +
     "Aaron holds his exact seated posture, hands clasped together and "
     "still. The bowls resting on the table hold their EXACT positions "
     "-- they do not turn, tip, or move at any point in the clip. Only: "
     "the single lamp's flame sways and flickers very gently, and the "
     "shadows it casts breathe softly with it. Nothing else changes."),
    # Eye-checked: the still shows the lots/bowls RESTING ON THE TABLE with
    # Aaron's hands clasped, not lots turned over in his open hand as the
    # plan's prose alone implies -- prompt corrected to match the actual
    # render (an open-hand object is also an animation-safety risk per
    # this project's own RESUME.md lesson #7: a Kling/Seedance animator
    # reads "loose in an open hand" as an invitation to invent motion).

    ("s37_split_two_things", "seedance", 4,
     LOCK +
     "The altar and the empty horizon on each half of the frame hold "
     "their exact shapes, perfectly still. Only: faint smoke curls very "
     "slowly upward from the altar, faint dust drifts low across the "
     "wilderness ground. Nothing else changes."),

    ("s38_walking_home_dusk", "seedance", 4,
     LOCK +
     "Aaron holds his exact mid-stride pose, perfectly frozen -- no "
     "further steps, no leg or arm movement. The camp behind him holds "
     "its exact shape. Only: the dusk light breathes very gently, faint "
     "dust drifts low. Nothing else changes."),

    # --- Beat 5: the wrestling (spreads 39-45) ---
    ("s39_honesty_close", "seedance", 4,
     PAGE +
     "Aaron's face stays exactly as drawn, his direct, honest expression "
     "fixed, mouth closed, gaze steady toward the viewer. The only "
     "movement in the whole clip: the light across his face breathes "
     "very gently. Nothing else changes."),

    # ELEVATED RISK: same content class as s07 (a wide crowd scene) --
    # s07's first attempt invented a figure walking into empty ground.
    # Strengthened with the same "ink on paper, not a photograph" reframe
    # + an explicit named-empty-space line before this ever runs; eye-check
    # a full frame sequence (not just start/mid/end) before accepting.
    ("s40_people_home_clean", "kling", 5,
     LOCK +
     "This is a finished ink-and-watercolor drawing on an aged page, not a "
     "photograph of a real crowd -- every one of the figures in the "
     "evening camp is ink on paper and holds their exact relieved posture, "
     "perfectly frozen -- no one steps, turns, or gestures, and no one "
     "walks. Any open ground between figures stays completely empty from "
     "the first frame to the last -- no figure enters it, nothing crosses "
     "it. INVENT NOTHING new anywhere in the frame. Only: faint dust "
     "drifts across the ground, cloth stirs very slightly, the evening "
     "light breathes very gently. Nothing else in the frame changes."),

    ("s41_repetition_vignettes", "kling", 5,
     LOCK +
     "This is a finished ink-and-watercolor drawing on an aged page, not a "
     "photograph -- Aaron's face holds its exact expression, mouth closed, "
     "no blink, no head turn. All three memory vignettes -- dawn, dusk, "
     "and haze -- hold their exact shapes and positions, perfectly frozen; "
     "in each, the hand on the goat's head never moves and the goat never "
     "moves. INVENT NOTHING new -- no new figure or vignette ever appears. "
     "Only: the light across each vignette breathes very gently in its own "
     "register. Nothing else in the frame changes."),
    # Confirmed at full res as a genuine 3-vignette composition (unlike
    # s34/s65) -- kept on the MV-default Kling tier.

    ("s42_basin_linen_ready", "seedance", 4,
     LOCK +
     "The basin and the folded linen hold their exact positions, "
     "perfectly still -- nothing is lifted, unfolded, or moved. Only: "
     "the light across them breathes very gently. Nothing else changes."),

    ("s43_shadow_on_tent_wall", "seedance", 4,
     LOCK +
     "Aaron holds his exact seated posture, hands resting still. His "
     "shadow cast on the tent wall behind him holds its EXACT shape and "
     "position -- it never grows, shifts, or changes form. Only: the "
     "single lamp's flame sways and flickers very gently, its light "
     "breathing with it. Nothing else changes."),
    # This is candle-only's literal design case (per the plan's own Device
    # column) -- the $0 radial light-budget pass (light closing down with
    # the fear) is a later compositing step over this base clip.

    ("s44_pointing_smoke", "seedance", 4,
     LOCK +
     "Aaron's face and eyes hold their exact position and gaze, "
     "perfectly still -- no blink, no eye movement, no head turn. Only: "
     "the altar smoke rises and leans, drifting slowly past the frame's "
     "edge. Nothing else changes."),

    ("s45_sign_before_veil", "seedance", 4,
     LOCK +
     "Aaron's silhouette and the veil hold their exact shapes and "
     "positions, perfectly still -- no gesture, no step. Only: the faint "
     "light breathes very gently, barely perceptibly. Nothing else "
     "changes."),
    # Held-breath quiet point -- wants the LEAST motion of any spread in
    # the batch; keep ambient change minimal even relative to the other
    # calm holds.

    # --- Beat 6: the reveal (spreads 46-63) ---
    ("s46_aged_unchanged_veil", "seedance", 4,
     LOCK +
     "Aaron and the veil behind him hold their exact positions, "
     "perfectly still -- no gesture, no step. Only: the dim light "
     "breathes very gently. Nothing else changes."),

    ("s47_light_arrives", "seedance", 4,
     LOCK +
     "Aaron holds his exact posture, perfectly still. Only: the light "
     "entering from beyond the page's edge grows warmer and brighter in "
     "one slow, steady wash across the scene -- " + NOGLITTER +
     "Nothing else changes."),
    # The halftone-dissolve time-shift transition is a later compositing
    # pass, not part of this clip.

    ("s48_small_basin_towering_veil", "seedance", 4,
     LOCK +
     "The basin and the towering veil hold their exact positions and "
     "shapes, perfectly still. Only: the light across the veil breathes "
     "very gently. Nothing else changes."),

    ("s49_veil_detail_card", "seedance", 4,
     LOCK + TEXTLOCK +
     "The veil behind the card's blank margin holds its exact shape, "
     "perfectly still. Only: the light breathes very gently. Nothing "
     "else changes."),

    ("s50_the_shadow", "seedance", 4,
     LOCK +
     "The wilderness sand and the long shadow thrown across it hold "
     "their EXACT shapes and positions, perfectly still -- the shadow "
     "never grows, shrinks, shifts, or changes form in any way, and "
     "nothing enters the frame to cast it. Only: faint dust drifts low "
     "across the sand. Nothing else changes."),
    # ELEVATED RISK: a meaningful, unexplained shadow shape is the exact
    # content class that caused a doctrinal-inversion failure in
    # bronze_serpent_long (a cross-shaped shadow redrew itself as a
    # serpent silhouette once left for the animator to reinterpret).
    # Eye-check this one at full res before accepting; a $0 static hold is
    # the fallback if the shadow's shape drifts at all.

    # EXCLUDED from JOBS (2026-08-04, after s53): s53's prompt already had
    # explicit "robe holds its exact folds" language and STILL animated the
    # robe (billowing/swinging, user: "Jesus is dancing") across 3 tightened
    # attempts. Prompt-tightening alone is not trusted anymore for Christ/
    # robe content -- every NO_KLING_FALLBACK spread (the highest doctrinal
    # stakes in the episode) moves to the same $0 dynamic_cam3d treatment
    # that fixed s53, via _s_christ_spreads_orbit.py in this folder, not a
    # generative attempt. duration=8 below was for this spread's own
    # heaviest-hold status (13.8s, the Jesus pivot) -- now handled by the
    # deterministic script's own duration param instead.
    # ("s51_jesus_pivot", "seedance", 8, ...),

    # EXCLUDED (see s51's note above) -- deterministic dynamic_cam3d instead.
    # ("s52_jesus_entering_formal", "seedance", 4, ...),

    ("s53_the_cross", "seedance", 4,
     LOCK + WOUND_LOCK +
     "Christ's entire body and the cross hold their EXACT position and "
     "shape, perfectly still -- His head stays bowed, His arms stay "
     "stretched along the crossbeam, unchanged from the first frame to "
     "the last; His robe and its knotted belt hold their exact folds. "
     "INVENT NOTHING new. Only: the pale light along His robe breathes "
     "very gently. Nothing else in the frame moves."),
    # NO_KLING_FALLBACK. TEST GATE job (crucifixion Seedance tier).

    # EXCLUDED (see s51's note above) -- deterministic dynamic_cam3d instead.
    # ("s56_the_answer", "seedance", 4, ...),

    # EXCLUDED (see s51's note above) -- deterministic dynamic_cam3d instead.
    # Loses this spread's licensed smoke-rising ambient motion (no
    # generative model runs at all) -- acceptable trade for removing the
    # Christ/crowd invention risk; a $0 smoke-overlay device could be added
    # later if the still hold feels too static on eye-check.
    # ("s57_without_the_gate", "seedance", 4, ...),

    ("s58_gate_card", "seedance", 4,
     LOCK + TEXTLOCK +
     "The city gate behind the card's blank margin holds its exact "
     "shape, perfectly still. Only: the light breathes very gently. "
     "Nothing else changes."),

    ("s59_no_chair", "seedance", 4,
     LOCK +
     "Aaron and the ark hold their exact positions, perfectly still -- "
     "the room stays bare except the ark, no chair or seat ever appears. "
     "Only: the light breathes very gently. Nothing else changes."),

    # EXCLUDED (see s51's note above) -- deterministic dynamic_cam3d instead.
    # ("s60_seated_glory", "seedance", 4, ...),

    ("s61_veil_recall", "seedance", 4,
     LOCK +
     "The veil holds its exact whole, unbroken shape, perfectly still. "
     "Only: the light across its weave breathes very gently. Nothing "
     "else changes."),
    # Multi-stage hard cut with s62 (whole -> torn) -- splice as a true
    # hard cut at assembly, never a dissolve/morph.

    ("s62_veil_torn", "seedance", 4,
     LOCK +
     "The torn veil holds its EXACT torn shape, perfectly still -- the "
     "tear never widens, narrows, or changes. No hand or figure ever "
     "appears. Only: the gold light spilling through the rent pulses "
     "very gently brighter and dimmer -- " + NOGLITTER + "Nothing else "
     "in the frame moves."),
    # Pair with s61, hard cut (see above).

    ("s63_torn_veil_card", "seedance", 4,
     LOCK + TEXTLOCK +
     "The torn veil behind the card's blank margin holds its EXACT torn "
     "shape, perfectly still. Only: the gold light spilling through the "
     "rent pulses very gently -- " + NOGLITTER + "Nothing else changes."),

    # --- Beat 7: the invitation (spreads 64-74; 75/76 excluded, see top) ---
    ("s64_empty_hands", "seedance", 4,
     PAGE +
     "Aaron stays exactly as drawn: facing the viewer, mouth closed, "
     "hands still, gaze steady. The only movement in the whole clip: the "
     "light across the page slowly and very slightly brightens and dims. "
     "Nothing else changes."),

    ("s65_ritual_uninks", "seedance", 4,
     PAGE +
     "Aaron's face stays exactly as drawn, his expression fixed, mouth "
     "closed. The small memory sketch behind him -- the priest, the "
     "goat, and the altar -- holds its exact shapes and positions, "
     "perfectly still; nothing in it moves. The only movement in the "
     "whole clip: the light across the page slowly and very slightly "
     "brightens and dims. Nothing else changes."),
    # Eye-checked: a close Aaron-face portrait with ONE small background
    # inset (priest+goat+altar together), not 3 separate equal-weight
    # vignettes -- moved from MV/Kling to Seedance + PAGE. The inset's own
    # "uninks" desaturating fade (per the still's filename) is a later $0
    # grade pass -- no color change is licensed in this clip.

    # EXCLUDED (see s51's note above) -- deterministic dynamic_cam3d instead.
    # ("s66_high_priests_face", "seedance", 4, ...),

    ("s67_same_road_lit", "seedance", 4,
     LOCK +
     "The goat holds its exact receding position on the road, perfectly "
     "frozen -- no further steps. Only: the gold light along the road "
     "pulses very gently brighter and dimmer -- " + NOGLITTER +
     "faint dust drifts low. Nothing else changes."),

    ("s68_east_west_horizon", "seedance", 4,
     LOCK +
     "The east and west horizon hold their exact shapes, perfectly "
     "still. Only: the dawn light at one edge breathes very gently. "
     "Nothing else changes."),

    ("s69_east_west_card", "seedance", 4,
     LOCK + TEXTLOCK +
     "The horizon sky behind the card's blank margin holds its exact "
     "shape, perfectly still. Only: the light breathes very gently. "
     "Nothing else changes."),

    ("s70_veil_held_open", "seedance", 4,
     LOCK +
     "The torn veil holds its EXACT open, torn shape, perfectly still -- "
     "it never widens, narrows, or moves. Only: the gold light through "
     "the opening pulses very gently brighter and dimmer -- " + NOGLITTER +
     "Nothing else changes."),

    ("s71_the_way_open", "seedance", 4,
     LOCK +
     "The torn veil and the mercy seat visible beyond hold their exact "
     "shapes and positions, perfectly still. Only: the light pouring out "
     "through the rent pulses very gently brighter and dimmer, toward "
     "the viewer -- " + NOGLITTER + "Nothing else in the frame moves."),

    ("s72_boldness_card", "seedance", 4,
     LOCK + TEXTLOCK +
     "The torn veil behind the card's blank margin holds its exact "
     "shape, perfectly still. Only: the light breathes very gently. "
     "Nothing else changes."),

    ("s73_aaron_steps_aside", "seedance", 4,
     PAGE +
     "Aaron stays exactly as drawn: standing aside from the torn veil, "
     "one arm extended in a gesture toward the viewer, mouth closed. The "
     "torn veil beside him holds its exact shape. The only movement in "
     "the whole clip: the light across the page slowly and very slightly "
     "brightens and dims. Nothing else changes."),

    ("s74_every_year_gone", "seedance", 8,
     PAGE +
     "Aaron stays exactly as drawn: facing the viewer, mouth closed, "
     "every year's fear gone from his gaze. The only movement in the "
     "whole clip: the light across his face slowly and very slightly "
     "brightens and dims. Nothing else changes."),
    # duration=8: one of the plan's own 4 heaviest-hold spreads (12.7s --
    # the final "will you come in?"). The plan's own slow push-in is added
    # at assembly; camera stays locked here.

    # s75_the_reach: user go-ahead given 2026-08-04. The still already shows
    # the hand fully extended (the reach is visually complete) -- modeled
    # tightly on s29's proven "one completing motion, then holds" pattern
    # (the only acting-spread precedent that's worked cleanly), with an
    # explicit no-wound guard since this is Christ. Fail-closed QC: a full
    # dense-frame sweep of the hand/fingers specifically before accepting,
    # not just start/mid/end.
    ("s75_the_reach", "kling", 5,
     "The camera does not move, zoom, or change angle at all. Christ's "
     "extended hand, already reaching toward the viewer, opens very "
     "slightly further and settles into its final resting gesture within "
     "the first two seconds of the clip -- fingers relax open a little "
     "more, then the hand holds that exact final position, perfectly "
     "still, for the rest of the clip -- the motion happens once and "
     "completes, it never repeats, reverses, or continues. Christ's face, "
     "hair, robe, and the curtains on both sides hold their exact position "
     "and shape throughout -- no gesture beyond the one hand-settling "
     "motion, no step, no change of expression. His hand and arm stay "
     "exactly as drawn otherwise -- no wound, no mark, no blood ever "
     "appears on them at any point. INVENT NOTHING new beyond this one "
     "settling motion. Only after the hand settles: the golden light "
     "through the torn veil breathes very gently. Nothing else in the "
     "frame ever moves."),
    # NO_KLING_FALLBACK-equivalent: Christ present, so on failure this must
    # stop and be reported, never silently retried with a different prompt
    # strategy without a fresh human look.

    # s76_already_inside: EXCLUDED -- $0 static held frame + tear_hole
    # landing device, see module docstring.
]


@contextlib.contextmanager
def _note_override(note):
    """A.run_job's cost.record_hf call hardcodes note=f"[piece1-v2] {name}"
    (same reasoning as bronze_serpent_long/_s4_animate.py: rather than fork
    run_job's subprocess/curl/retry logic just to change one string, patch
    cost.record_hf for the duration of one call)."""
    orig = A.cost.record_hf
    def patched(*a, **kw):
        kw["note"] = note
        return orig(*a, **kw)
    A.cost.record_hf = patched
    try:
        yield
    finally:
        A.cost.record_hf = orig


def main(only=None):
    jobs = JOBS if only is None else [j for j in JOBS if j[0] in only]
    A.cost.record_stage(A.EPISODE, "animate_start", note=f"{len(jobs)} jobs")
    results = []
    for name, provider, dur, motion in jobs:
        still = STILLS / f"{name}.png"
        out = A.OUT / f"{name}.mp4"
        if out.exists():
            print(f"[skip] {name}")
            results.append((name, "cached"))
            continue
        if not still.exists():
            print(f"[HOLD] {name}: still missing")
            results.append((name, "NO-STILL"))
            continue
        # Unlike bronze_serpent_long (which prepends LOCK centrally here
        # based on SELF_CONTAINED membership), every JOBS motion string in
        # this file already has its own full framing baked in at
        # definition time (LOCK, or PAGE for names in SELF_CONTAINED,
        # plus TEXTLOCK/NOGLITTER/WOUND_LOCK inline where needed) -- so
        # each spread's exact framing choice is visible right next to its
        # prompt. SELF_CONTAINED is kept as documentation/cross-check, not
        # active branching.
        prompt = motion
        with _note_override(f"[dayofatonementlong] {name}"):
            if name in NO_KLING_FALLBACK:
                # No provider fallback for wound-risk spreads -- a Seedance
                # failure here must stop and be reported, never silently
                # reintroduce Kling's documented wound-regeneration risk.
                ok = A.run_job(name, provider, still, ASPECT, prompt, duration=dur)
                used = provider
            else:
                ok, used = A.run_job_with_fallback(name, provider, still, ASPECT, prompt, duration=dur)
        if not ok:
            status = "FAILED (no-fallback wound-risk spread)" if name in NO_KLING_FALLBACK else "FAILED"
        elif used == provider:
            status = "clean"
        else:
            status = f"clean (fallback:{used})"
        results.append((name, status))
    A.cost.record_stage(A.EPISODE, "animate_end", note=f"{len(results)} jobs processed")
    print("\n=== summary ===")
    for name, status in results:
        print(f"  {name}: {status}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        only = None if arg == "all" else arg.split(",")
    else:
        only = list(TEST_GATE)
        print(f"[test-gate] running {only} -- pass 'all' or an explicit list to override")
    main(only)
