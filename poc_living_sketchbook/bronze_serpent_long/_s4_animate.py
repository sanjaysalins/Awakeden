"""Bronze Serpent LONG (16:9 living-sketchbook pilot) -- step 4: animate the
paid-generative spreads. Follows bronze_serpent/_s3_animate.py's exact pattern:
imports the shared driver from poc_comic_page/_animate_piece1_v2.py, reuses its
LOCK/NOGLITTER camera-locked, INVENT-NOTHING, named-ambient-motion-only
prompting, run_job_with_fallback, and the cost note-override. Kling for
multi-figure/crowd/gesture spreads, Seedance for calm single-figure spreads
(cost-tiered), and Seedance ALWAYS for crucifixion/Christ iconography
(living-light-no-fresh-blood: Kling has REGENERATED blood/wounds from
crucifixion iconography even on a retouched-clean still).

ASPECT: "16:9" (NOT the short's 9:16). Confirmed supported end-to-end: the
driver passes the string straight to `hf generate create ... --aspect_ratio`,
and this same driver has already run 16:9 on Seedance
(poc_castbible_look/_03_rain_clip.py) and kling3_0 at 16:9 has run via
poc_thief_e2e/_animate_zacchaeus.py.

COUNT (flagged, not silently fixed): the plan has 68 spreads. s43/s67/s68 are
$0 deterministic devices (insert-page camera pans + the torn-page landing) --
NOT in this list, per the plan's own Device column. Of the remaining 65:

  - s28_forge_acting is EXCLUDED -- the short's own equivalent beat
    (s06_forge) is a documented 3-STRIKES failure (2x Kling + 1x Seedance all
    invented a completed hammer swing despite three different prompt
    strategies; see bronze_serpent/_s3_animate.py lines ~124-187). The still
    here is the same content class (hammer + glowing serpent on the pole).
    Default: the same $0 deterministic InsertPageCamera push-in the short
    resolved to. Do NOT re-attempt Kling/Seedance unattended.
  - s55_hezekiah_breaks is EXCLUDED after a full-res eye-check (2026-08-01):
    the still shows the hammer RAISED mid-swing and the pole mid-SHATTER with
    debris drawn in flight -- the exact frozen-mid-strike class that failed
    3x on s06_forge. Proposing Kling/Seedance here would be silently retrying
    the same failure. Default: $0 deterministic push-in + the plan's own
    assigned impact-burst device (ink impact-star synced to a real SFX hit
    carries the strike energy deterministically). A generative attempt is a
    USER decision, not a batch job.

  => 63 runnable jobs below: 47 Seedance + 16 Kling.

VERSE-CARD CAVEAT (flagged): 7 spreads are verse cards carrying Scribed Ink
lettering (s10, s12, s15, s20, s24, s48, s58). The never-animate-writing rule
(letters garble under generative animation) makes these the riskiest Seedance
jobs in the list; every one carries an explicit letter-freeze guard (TEXTLOCK
below). If any test shows letter shimmer, the $0 deterministic camera pan is
the fallback -- eye-check lettering at full res on the first VC clip before
running the rest. Related: the plan's own Device column already suggests
insert_page_camera-style $0 pans for s12 (and slow push/drift for s32/s41) --
generated clips here are camera-LOCKED, so any push/drift the plan wants must
be added deterministically at assembly regardless.

DURATION GAPS (for the assembly stage): every clip is capped at 8s (the
short's own ceiling; no provider in the stack renders longer natively).
Spreads whose on-screen hold is >=10s rely on assembly looping/hold-extension
per longform-motion-fill: s08 (10.0s), s12 (10.9), s30 (18.6), s32 (25.6),
s33 (13.6), s34 (12.2), s36 (21.4), s38 (18.8), s40 (14.2), s41 (18.3),
s52 (10.8), s66 (11.0).

TEST GATE: exactly 3 jobs run unless "all" or an explicit list is passed --
one per risk tier: s03_eyes_haunted (calm single-figure Seedance, the most
common spread class), s11_crowd_angry (crowd/gesture Kling -- also probes the
moderation profile that NSFW-rejected the short's distressed-group s01_wide
on Seedance), s45_golgotha_wide (crucifixion Seedance with the wound-lock
language, mirroring the short's own proven s10_golgotha test job).

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s4_animate.py            # test gate (3 jobs)
  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s4_animate.py all         # full batch
  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s4_animate.py s01_wide,s04_icon_pole  # explicit subset
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
A.EPISODE = "LS_BronzeSerpentLong"
A.OUT = HERE / "clips"
A.OUT.mkdir(exist_ok=True)

STILLS = HERE / "stills"
ASPECT = "16:9"  # long-form pilot -- NOT the short's 9:16

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, torn edges, and every sketch line hold perfectly still. ")
NOGLITTER = ("the light stays a steady, even glow -- it does not sparkle, "
             "flicker into particles, or scatter into glitter. ")
# Verse-card letter-freeze guard (never-animate-writing: letters garble).
TEXTLOCK = ("Every lettered word and every stroke of the handwritten text "
            "stays pixel-identical and perfectly legible -- no letter warps, "
            "redraws, shimmers, or changes in any way. ")

# REDO ROUND 1 (2026-08-01, Fable diagnosis after the 63-clip QC pass found
# 16 real defects): root causes were (1) negation-priming -- naming a verb
# to forbid it (per this project's own seedream-no-negative-channel lesson,
# generalizing from stills to Seedance animation), (2) unlocked-region
# migration -- LOCK's body-part-list locks let anything NOT named drift,
# (3) a talking-head/interview prior on direct-address portraits causing
# invented lip-sync + push-zoom, (4) licensed ambient motion escalating
# into unwanted coupled content (a "breathing glow" on wound-adjacent skin
# read as monotonic intensification; "serpent on pole" primed a shadow to
# redraw AS a serpent). PAGE replaces LOCK for the self-contained-portrait
# redo class: reframes the subject as "a finished drawing being filmed"
# instead of a live person, with whole-figure POSITIVE state locks (never
# a forbidden-verb list) -- this is a full prompt replacement (no LOCK
# prepend), used only for names in SELF_CONTAINED below.
PAGE = ("A finished ink-and-watercolor drawing on an aged sketchbook page, "
        "filmed as a perfectly still page under steady light. The framing "
        "stays fixed and locked for the entire clip. The drawing is "
        "finished and dry: every figure, face, hand, and object in it is "
        "ink on paper and stays exactly as drawn from the first frame to "
        "the last. ")
SELF_CONTAINED = {
    "s64_moses_sit_with_that", "s59_moses_be_still", "s18_moses_empty_hands",
    "s53_moses_know_that_now", "s52_moses_reflecting", "s62_moses_neverasked",
    "s26_moses_resolve_serpent", "s14_serpent_hint", "s16_bite_closeup",
    "s45_golgotha_wide",  # REDO ROUND 2 (2026-08-02): confirmed dancing defect fix
}

# TEST GATE default: exactly these 3 run unless overridden on the command line.
TEST_GATE = ("s03_eyes_haunted", "s11_crowd_angry", "s45_golgotha_wide")

# BUG FOUND + FIXED 2026-08-01 (test-gate run on s45): 14 Seedance jobs had
# duration=5, which is INVALID for seedance1_5 (only 4/8/12 accepted) --
# every one of them was silently falling back to Kling via
# run_job_with_fallback's generic on-any-failure retry, INCLUDING most of
# the Christ/crucifixion tier below. That's exactly the wound-regeneration
# risk this whole tier is pinned to Seedance to avoid (see
# living-light-no-fresh-blood memory) -- a silent parameter-validation
# fallback was defeating the safeguard without anyone noticing. All 14
# durations corrected to 4 above. The real s45 test clip WAS actually
# animated by Kling (not Seedance) because of this bug -- its grown wound
# marks are the already-documented Kling failure mode, not new evidence
# against Seedance. A clean-duration Seedance retry is still needed to
# confirm Seedance itself is safe on this content before trusting the tier.
#
# NO_KLING_FALLBACK: every spread that shows Jesus on/near the cross is
# wound-risk-critical -- for these, a Seedance failure must NEVER silently
# substitute Kling (main() below calls A.run_job directly, no fallback, for
# anything in this set). A real failure here should stop and ask a human,
# not quietly reintroduce the exact risk the tier assignment exists to avoid.
NO_KLING_FALLBACK = {
    "s45_golgotha_wide", "s46_thesis_pair", "s47_golgotha_midshot",
    "s49_christ_radiant_begin", "s50_christ_close_words",
    "s51_christ_draw_all_men", "s57_bridge_moses_christ", "s58_vc_john316",
    "s63_vignette_least_last_child", "s65_christ_open_invite",
}

# (name, provider, duration, motion)
JOBS = [
    # --- Beat 1: the hook (spreads 1-6) ---
    ("s01_wide", "seedance", 4,
     "Aged Moses and the wilderness camp behind him hold their exact "
     "positions, perfectly still -- no steps, no gesture, no head turn. "
     "Only: faint dust drifts low across the open ground, distant tent "
     "fabric stirs very slightly in the wind. Nothing else changes."),

    # Multi-vignette triptych -- Kling tier. The rod-serpent vignette gets
    # the serpent-lock (documented Kling failure: "a coiled serpent uncoiled
    # and slithered"); the sea and rock-water vignettes get explicit
    # water-freeze (water invites invented flow).
    ("s02_triptych", "kling", 5,
     "All three memory vignettes hold perfectly still -- the rod-serpent "
     "keeps its EXACT frozen shape and position, it does not move, uncoil, "
     "or slither; the parted sea walls do not flow, fall, or churn; the "
     "water from the rock does not pour or splash. No figure moves or "
     "changes posture. Only: a faint light breathing across the paper. "
     "Nothing else in the frame changes."),

    # === TEST GATE JOB 1 of 3 (calm single-figure Seedance tier) ===
    ("s03_eyes_haunted", "seedance", 4,
     "Moses's eyes and face hold their exact haunted expression and gaze, "
     "perfectly still -- no blink, no head turn. Only: the light across his "
     "face breathes very gently. Nothing else changes."),

    ("s04_icon_pole", "seedance", 4,
     "The bronze serpent holds its EXACT coiled shape and position on the "
     "pole, perfectly frozen -- it does not move, uncoil, or slither. The "
     "pole and the sand hold perfectly still. Only: faint dust drifts low "
     "across the sand, the light on the bronze breathes very gently. "
     "Nothing else changes."),

    # Frozen mid-action (digging) -- named freeze so no dig-stroke completes.
    ("s05_graves", "kling", 5,
     "Every figure among the graves holds their exact posture and gesture, "
     "perfectly frozen -- no digging motion continues, no one steps, turns, "
     "or changes expression. INVENT NOTHING new. Only: faint dust drifts "
     "across the ground, the sky beyond breathes very slightly. Nothing "
     "else in the frame changes."),

    ("s06_dying_hand_eye", "seedance", 4,
     "The dying man's reaching hand and his eye hold their exact positions, "
     "perfectly still -- the hand does not close, lift, or reach further. "
     "Only: the warm light across the skin breathes very gently. Nothing "
     "else changes."),

    # --- Beat 2: discouragement -> serpents (spreads 7-18) ---
    ("s07_ungrateful_camp", "kling", 5,
     "Every figure in the camp holds their exact posture, perfectly frozen "
     "-- no one steps, turns, or gestures. INVENT NOTHING new. Only: faint "
     "dust drifts between the tents, tent fabric stirs very slightly in the "
     "wind. Nothing else in the frame changes."),

    ("s08_wandering_column", "kling", 5,
     "Every figure in the distant wandering column holds their exact place "
     "on the road, perfectly frozen -- no one walks, steps, or advances; "
     "the column does not move. Only: faint dust drifts low across the "
     "barren ground, heat-haze breathes very slightly above the horizon. "
     "Nothing else changes."),

    # REDO ROUND 1 (2026-08-01): the licensed "manna drifts down" motion
    # escalated into a white haze/fog over the figures + multiplied flecks
    # by 75% -- Kling's documented atmospheric-bloom family. Kling DOES
    # respond to naming the specific failure directly (feedback-kling-
    # lowmotion-fix), so kept on Kling with an explicit no-mist/fog/haze
    # clause added rather than switching provider.
    ("s09_manna_scorned", "kling", 5,
     "Every figure holds their exact turned-away posture, perfectly "
     "frozen -- no one steps, turns, or gestures. The manna flakes hang in "
     "the air exactly where they are drawn, motionless. The air stays "
     "perfectly clear from the first frame to the last -- no mist, no "
     "fog, no haze, no white vapor forms anywhere. Only: faint dust stirs "
     "at the ground, cloth stirs very slightly. Nothing else in the frame "
     "changes."),

    ("s10_vc_discouraged", "seedance", 4,
     TEXTLOCK +
     "The background crowd artwork holds perfectly still. Only: the light "
     "across the paper breathes very gently. Nothing else changes."),

    # === TEST GATE JOB 2 of 3 (crowd/gesture Kling tier) ===
    # Mirrors the short's proven s03_complaint prompt (same content class).
    ("s11_crowd_angry", "kling", 5,
     "Every figure in the angry crowd holds their exact raised-hand gesture "
     "and posture perfectly frozen -- no new gesture, no stepping, no "
     "change of expression. Moses holds his exact stance apart, unmoving. "
     "INVENT NOTHING new. Only: faint dust drifts across the ground, the "
     "sky beyond breathes very slightly. Nothing else in the frame "
     "changes."),

    # Plan's Device column wants an insert_page_camera-style push-in here;
    # the generated clip is camera-locked, so that push must be added
    # deterministically at assembly (see module docstring).
    # REDO ROUND 1 (2026-08-01): the first attempt invented a pointing-
    # finger rotation + a hand-shape shift (micro-acting on an argument
    # scene locked only at vague "artwork" level). The plan's own Device
    # column already wanted an insert_page_camera push-in here anyway (see
    # main script's docstring notes) -- EXCLUDED from generative animation,
    # $0 deterministic push-in fallback instead. Old reject archived.

    # RICHNESS PASS (2026-08-02, user feedback -- "felt plain"): enriched
    # from one thin ambient clause to layered, still-grounded elements (dark
    # cloud on the distant peak, mantle edge, light) -- every existing
    # figure/object freeze-lock kept verbatim; Moses now explicitly locked
    # by name since a cloth license now touches him.
    ("s13_vignette_calf", "kling", 5,
     "All three memory vignettes hold perfectly still -- the sea, the rock, "
     "and the tarnished calf under the cloud keep their EXACT shapes and "
     "positions; no water flows, no figure moves, and the calf never moves, "
     "gleams, or brightens. Moses holds his exact pose and expression, "
     "perfectly still. Only: the dark storm-cloud wrapped around the "
     "distant mountain peak, high above the calf, drifts and curls very "
     "slowly in place; the loose outer edge of Moses's mantle stirs very "
     "slightly; and a faint light breathes across the paper. Nothing else "
     "in the frame changes."),

    # REDO ROUND 1 (2026-08-01): the "does not move, uncoil, or slither"
    # negation-lock is the exact documented failure verb-for-verb (naming a
    # noun/verb to forbid it DRAWS it, generalizing this project's own
    # seedream-no-negative-channel lesson to Seedance animation) -- the
    # serpent grew from a thin line into a thick body sweeping the
    # foreground. PAGE reframe: serpent described as fixed ink, never named
    # as something that could move; ambient motion moved OFF the ground
    # (up onto the tent fabric) so it can't couple with the serpent's region.
    ("s14_serpent_hint", "seedance", 4,
     PAGE +
     "The serpent shape drawn in the dust between the tents is a fixed "
     "line of ink: it keeps the exact length, thickness, curve, and "
     "position it has in the drawing, from the first frame to the last. "
     "The only movement in the whole clip: the tent fabric stirs very "
     "slightly in the wind, high on the tents. Nothing else changes."),

    ("s15_vc_fiery_serpents", "seedance", 4,
     TEXTLOCK +
     "Every serpent in the artwork holds its EXACT shape and position, "
     "perfectly frozen -- none moves, uncoils, or slithers. Only: the light "
     "across the paper breathes very gently. Nothing else changes."),

    # REDO ROUND 1 (2026-08-01): the licensed "red heat-glow breathes
    # brighter and dimmer" motion, on wound-adjacent skin, ran monotonically
    # UP instead of oscillating -- a faint pink mark at 2% became a
    # saturated dark-red wound by 50-98%. Same failure FAMILY as the
    # crucifixion wound-regeneration bug (semantic coupling: licensed
    # color/intensity motion on skin content escalates), but this happened
    # on Seedance, not via a Kling fallback -- new lesson: NEVER license
    # color/intensity motion on skin or wound-adjacent content on ANY
    # provider. State-lock the mark instead; motion moved to ambient light.
    ("s16_bite_closeup", "seedance", 4,
     PAGE +
     "The clenched fist and forearm stay exactly as drawn. The small mark "
     "on the back of the hand keeps the exact size, shape, and faint shade "
     "it has in the first frame, all the way to the last frame. The only "
     "movement in the whole clip: the soft light across the paper slowly "
     "and very slightly brightens and dims. Nothing else changes."),

    # RICHNESS PASS (2026-08-02): layered, still-grounded elements (tent
    # fabric, tunic hems, sky wash) replacing the single thin dust/cloth
    # clause. Figure freeze-locks kept verbatim.
    ("s17_vignette_collapse", "kling", 5,
     "The collapsed man and the mother cradling her child hold their exact "
     "postures, perfectly frozen -- no one moves, rocks, or changes "
     "position. INVENT NOTHING new. Only: faint dust drifts low across the "
     "sand; the loose hems of their tunics stir very slightly; the faint "
     "sketched tent fabric in the far background stirs very slightly in "
     "the wind; and the pale blue-grey wash of sky behind the collapsed "
     "man breathes very slowly and evenly. Nothing else in the frame "
     "changes."),

    # REDO ROUND 1 (2026-08-01): direct-address-portrait talking-head prior
    # -- the mouth parted/opened (an invented speech gesture) between 25%
    # and 50%. PAGE reframe + explicit "mouth closed" as a positive state
    # (never a "no lip movement" negation, which is the exact verb that
    # keeps getting drawn). Kept the same passing-dust ambient motion.
    ("s18_moses_empty_hands", "seedance", 4,
     PAGE +
     "Moses stays exactly as drawn: arms spread wide, hands open and "
     "empty, mouth closed. The only movement in the whole clip: faint "
     "dust drifts low across the ground behind him. Nothing else "
     "changes."),

    # --- Beat 3: contrition -> the command -> the forge (spreads 19-30) ---
    ("s19_people_kneel", "kling", 5,
     "Every kneeling figure holds their exact contrite posture, perfectly "
     "frozen -- no one bows further, rises, or gestures. Moses holds his "
     "exact stance, unmoving. INVENT NOTHING new. Only: faint dust drifts "
     "across the ground, cloth stirs very slightly. Nothing else in the "
     "frame changes."),

    ("s20_vc_we_have_sinned", "seedance", 4,
     TEXTLOCK +
     "The background artwork holds perfectly still. Only: the light across "
     "the paper breathes very gently. Nothing else changes."),

    ("s21_moses_intercede", "seedance", 4,
     "Moses holds his exact kneeling posture, arms raised in prayer, "
     "perfectly still -- no gesture change, no head movement. Only: faint "
     "dust drifts across the open ground, the sky beyond breathes very "
     "slightly. Nothing else changes."),

    ("s22_moses_listening", "seedance", 4,
     "Moses's face holds its exact listening expression, perfectly still -- "
     "no blink, no head turn, no lip movement. Only: the light across his "
     "face breathes very gently. Nothing else changes."),

    # Pivotal glory beat -- 8s hold per the short's s13_lifted precedent.
    # LORD-presence is light only, never a figure (red-letter-speaker rule).
    ("s23_lord_presence", "seedance", 8,
     "Moses holds his exact kneeling posture, shielding his eyes, perfectly "
     "still -- no gesture change, no head movement. The radiant light keeps "
     "its exact shape and position -- no figure, face, or form ever appears "
     "within it. Only: the radiant golden light pulses very gently brighter "
     "and dimmer in a steady, even glow -- " + NOGLITTER + "Nothing else in "
     "the frame moves."),

    ("s24_vc_make_thee", "seedance", 4,
     TEXTLOCK +
     "The gold dropped-cap and every gold accent stay exactly where they "
     "are -- " + NOGLITTER + "Only: the warm glow behind the card breathes "
     "very gently. Nothing else changes."),

    ("s25_moses_empty_negation", "seedance", 4,
     "Moses holds his exact posture, open empty hands unmoving, perfectly "
     "still -- no gesture, no head movement. Only: the light across the "
     "scene breathes very gently. Nothing else changes."),

    # REDO ROUND 1 (2026-08-01): same negation-priming failure as s14 --
    # "does not move, uncoil, or slither" drew exactly that; the coil
    # re-formed with the head crossing to the stone's far edge by 98%.
    # PAGE reframe, serpent described as fixed ink; ground-dust motion
    # removed entirely (it overlapped the serpent's own region) -- only
    # ambient light motion remains.
    ("s26_moses_resolve_serpent", "seedance", 4,
     PAGE +
     "Moses stays exactly as drawn, kneeling with one hand pressed on the "
     "flat stone. The small serpent beside his hand is a fixed line of "
     "ink: it keeps the exact coiled shape, position, and head placement "
     "it has in the drawing, from the first frame to the last. The only "
     "movement in the whole clip: the light across the paper slowly and "
     "very slightly brightens and dims. Nothing else changes."),

    # Eye-checked 2026-08-01: hands gathering ore chunks at a sack, small
    # stone furnace at left -- NO hammer, no mid-strike; frozen grip only.
    ("s27_hands_gather_ore", "seedance", 4,
     "Both hands hold their exact grip on the ore and the sack, perfectly "
     "frozen -- no finger moves, nothing is lifted, gathered, or poured. "
     "The small furnace and stones hold perfectly still. Only: the light "
     "across the scene breathes very gently. Nothing else changes."),

    # s28_forge_acting: EXCLUDED -- 3-strikes failure class (see module
    # docstring). $0 deterministic push-in fallback, same as the short's own
    # resolution for s06_forge. Not a JOBS entry on purpose.

    ("s29_pole_first_healing", "kling", 5,
     "The bronze serpent on the pole holds its EXACT coiled shape and "
     "position, perfectly frozen -- it does not move, uncoil, or slither. "
     "Every figure holds their exact upturned-gaze posture, perfectly "
     "frozen -- no one steps, kneels, rises, or gestures. INVENT NOTHING "
     "new. Only: faint dust drifts across the ground, cloth stirs very "
     "slightly. Nothing else in the frame changes."),

    # RICHNESS PASS (2026-08-02): the old "warm light on his FACE breathes"
    # clause was color/intensity motion on skin -- the same class that grew
    # a wound on s16 -- doubly risky here since "fever breaks" + warmth on a
    # face invites a monotonic flush. Moved the light off his skin onto the
    # paper/wash, added 2 more grounded layers (tunic sleeve, shadow wash).
    ("s30_payoff_fever_breaks", "kling", 5,
     "The man holds his exact upward-looking posture, perfectly frozen -- "
     "his expression does not change, he does not rise or move, and his "
     "headwrap stays exactly as drawn on his head the whole time, never "
     "fading, shrinking, or disappearing at any point in the clip. The "
     "bronze serpent on the pole holds its EXACT coiled shape, perfectly "
     "frozen -- it does not move, uncoil, or slither. Every other figure "
     "holds perfectly still. Only: the light across the paper CLEARLY and "
     "visibly brightens and dims in a slow, steady breathing rhythm -- a "
     "real, noticeable swing from dim to bright and back, not a subtle "
     "flicker; the grey wash of shadow behind him swells and fades "
     "visibly in that same rhythm; the loose folds of his tunic sleeves "
     "sway gently with each breath of light; and faint dust drifts low "
     "and visibly across the ground, catching the light as it passes. "
     "Nothing else in the frame changes."),

    # REDO ROUND 4 (2026-08-02): user caught the man's headwrap vanishing
    # partway through the clip during assembly QC -- confirmed real in the
    # SOURCE clip itself (present for ~1s, gone for the rest), same
    # unlocked-region-migration mechanism as s45's sky/s65's robe: the old
    # lock never named the headwrap, so it was free to drift. Fix: explicit
    # lock added. The assembly's slow_pingpong bounce made the defect MORE
    # visible (it plays the vanish forward then the reverse un-vanish on
    # the bounce-back), but did not cause it -- the source clip itself is
    # the one that needs re-rendering.

    # REDO ROUND 3c (2026-08-02): user confirmed the first enrichment pass
    # was real (full-res compare showed motion) but too subtle to actually
    # read as richer. Reworded with explicit "clearly/visibly/noticeable"
    # language and a bigger swing on each already-licensed element -- same
    # elements, same locks on the man/serpent, just turned up.

    # --- Beat 4: why a serpent? (spreads 31-34) ---
    ("s31_moses_why_serpent", "seedance", 4,
     "Moses's face holds its exact questioning expression, perfectly still "
     "-- no blink, no head turn. Only: the light across his face breathes "
     "very gently. Nothing else changes."),

    # 25.6s on-screen hold -- longest of the film. 8s clip; assembly loops /
    # extends and adds the plan's slow drift deterministically.
    ("s32_pole_silhouette_dusk", "seedance", 8,
     "The bronze serpent and its pole hold their EXACT silhouetted shape "
     "and position against the dusk, perfectly frozen -- the serpent never "
     "moves, uncoils, or slithers. The camp below holds perfectly still. "
     "Only: the dusk sky behind breathes very slowly and evenly, faint "
     "smoke from distant campfires drifts very slightly. Nothing else "
     "changes."),

    # RICHNESS PASS (2026-08-02): dropped the old "dust drifting low" clause
    # -- this still has no drawn ground plane (the 3 vignettes float on
    # plain paper), so licensed dust wasn't grounded in anything visible.
    # Replaced with elements actually IN the still (tunic hems, the elder's
    # blanket + mat fringe, per-vignette wash halos). Blanket motion bounded
    # to its outermost hanging edge, away from the elder's body.
    ("s33_vignette_universal", "kling", 5,
     "All three figures -- the strong man, the child, and the dying elder "
     "-- hold their exact lifted-eyes postures, perfectly frozen; no one "
     "moves, steps, or changes expression. INVENT NOTHING new. Only: the "
     "loose hems of the standing man's and the child's tunics stir very "
     "slightly; the outermost hanging edge of the elder's blanket and the "
     "frayed fringe of the woven mat beneath it stir very slightly; the "
     "soft sepia wash behind each figure breathes very gently and evenly; "
     "and a faint light breathes across the paper. Nothing else in the "
     "frame changes."),

    # Frozen mid-stride -- panel_d precedent (proven Seedance freeze).
    ("s34_moses_walking_dusk", "seedance", 4,
     "Moses holds his exact mid-stride pose perfectly frozen -- no "
     "additional steps, no leg or arm movement, no walking continues. "
     "Only: the dusk light across the scene breathes very gently, faint "
     "dust drifts low. Nothing else changes."),

    # --- Beat 5: the wrestle (spreads 35-42) ---
    ("s35_moses_honest_close", "seedance", 4,
     "Moses's face holds its exact direct, honest expression, perfectly "
     "still -- no blink, no head movement, no lip movement. Only: the "
     "light across his face breathes very gently. Nothing else changes."),

    ("s36_proud_man_turns_away", "kling", 5,
     "The proud man holds his exact turned-away posture, perfectly frozen "
     "-- he does not keep turning, step, or gesture. Every background "
     "figure holds their exact pose, and the bronze serpent on its pole "
     "holds its EXACT shape, perfectly frozen -- it never moves, uncoils, "
     "or slithers. INVENT NOTHING new. Only: faint dust drifts, cloth "
     "stirs very slightly. Nothing else in the frame changes."),

    # Eye-checked 2026-08-01: grinding stone RESTS in contact on the calf's
    # back (no raised implement, no gap to close -- unlike the forge/s55
    # failure class, where all invented motion completed an in-flight
    # strike). Kling for the multi-element action frame; maximal freeze.
    # ELEVATED RISK: eye-check first/mid/last frames before accepting.
    ("s37_calf_flashback", "kling", 5,
     "Moses and the grinding stone in his hands hold their EXACT positions, "
     "perfectly frozen -- the stone stays exactly where it rests, no "
     "grinding motion begins or continues, his arms and hands never move. "
     "The tarnished calf holds its exact shape and position -- it never "
     "moves, gleams, or brightens. INVENT NOTHING new. Only: the shaft of "
     "pale light breathes very gently, faint dust drifts within it. "
     "Nothing else in the frame changes."),

    ("s38_dread_image", "seedance", 4,
     "Moses holds his exact pose, staring at the bronze serpent in his "
     "hands, perfectly still -- his grip never shifts, and the serpent "
     "holds its EXACT shape, never moving, uncoiling, or slithering. The "
     "tablets stay exactly where they are. Only: the light across the "
     "scene breathes very gently. Nothing else changes."),

    ("s39_moses_sleepless_candle", "seedance", 4,
     "Moses holds his exact sleepless posture, perfectly still -- no "
     "movement, no blink. Only: the candle flame sways and breathes very "
     "gently, and the warm light it casts flickers softly with it. Nothing "
     "else changes."),

    ("s40_moses_resolve_returning", "seedance", 4,
     "Moses holds his exact pose, hand resting on the bronze serpent, eyes "
     "lifted, perfectly still -- his hand never moves, and the serpent "
     "holds its EXACT shape, never moving, uncoiling, or slithering. Only: "
     "the light across his face breathes very gently. Nothing else "
     "changes."),

    # 18.3s hold; plan wants a slow push-out -- assembly adds it ($0).
    ("s41_moses_long_road", "seedance", 8,
     "Moses holds his exact stance at the camp's edge, perfectly still -- "
     "no steps, no turning. The long empty road and the darkness beyond "
     "hold perfectly still. Only: faint dust drifts low across the road, "
     "the far darkness breathes very slightly. Nothing else changes."),

    # Eye-checked 2026-08-01: a hammer IS in frame (gripped, head lowered AT
    # REST beside the pole -- not raised mid-swing) plus the serpent on the
    # pole. Same content family as the 3-strikes forge but without the
    # in-flight strike; ELEVATED RISK all the same. Seedance, hammer + hand
    # + serpent all explicitly frozen, motion on light only. Eye-check
    # first/mid/last frames before accepting; $0 push-in is the fallback.
    ("s42_hands_finish_forge", "seedance", 4,
     "Both hands hold their EXACT positions, perfectly frozen -- the hand "
     "gripping the hammer never lifts, lowers, or swings it, and the "
     "hammer head stays exactly where it rests; the other hand never "
     "shifts its grip on the pole. The bronze serpent on the pole holds "
     "its EXACT coiled shape and position, perfectly frozen -- it never "
     "moves, uncoils, or slithers. INVENT NOTHING new. Only: the light on "
     "the bronze breathes very gently. Nothing else in the frame changes."),

    # s43_insert_scholars_margin2: $0 insert-page device -- not in this list.

    # --- Beat 6: the fulfilment (spreads 44-58) ---
    # REDO ROUND 1 (2026-08-01): EXCLUDED from generative animation.
    # First attempt semantically coupled "serpent on pole" -> the
    # cross-shaped shadow (the spread's own doctrinal point -- Numbers 21's
    # serpent prefiguring the cross) redrew itself AS a giant serpent-
    # silhouette by 98%, crossbar gone -- an exact doctrinal inversion, not
    # just a technical glitch. The shadow's SHAPE is the meaning here, so
    # this is not a phrasing problem worth a second generative roll -- $0
    # deterministic InsertPageCamera push-in instead (same fallback pattern
    # as s28/s55), framed so the full shadow incl. crossbar stays in frame.

    # === TEST GATE JOB 3 of 3 (crucifixion Seedance tier) ===
    # REAL DEFECT CONFIRMED 2026-08-02 (user: "Jesus is dancing"): a dense
    # 12fps frame-diff analysis (not sparse sampling) showed body-region
    # motion, isolated from the sky background, stayed elevated and roughly
    # CONSTANT across the whole clip rather than spiking once and settling
    # -- the signature of continuous sway, not ambient breathing. Diagnosis:
    # licensed-motion coupling, spatial-drift variant. The old prompt's
    # "the sky... drifts" is a continuous SPATIAL motion; this still's dark
    # sky occupies the upper two-thirds and surrounds the thin figure on
    # all sides, so imperfect figure/sky segmentation let that spatial warp
    # field bleed across the body boundary for the whole clip. Every OTHER
    # crucifixion clip that passed licenses INTENSITY-only motion ("light
    # breathes/pulses evenly") -- s45 was the only one licensing spatial
    # drift, and the only one that swayed. Fix: kill all spatial drift,
    # license intensity-only whole-field motion instead (the pattern that
    # already fixed s58's glitter), PAGE reframe (drawing-being-filmed, not
    # a live man under weather), explicit positive pose statements (the fix
    # that held on s49's earlier head-lift). Wound-lock kept verbatim -- it
    # already held clean across two independent test rounds. Seedance
    # MANDATORY (living-light-no-fresh-blood: Kling regenerates wounds/blood
    # from crucifixion iconography) -- added to SELF_CONTAINED below so PAGE
    # replaces LOCK entirely (no spatial "camera does not move" negation
    # either, for the same reason).
    ("s45_golgotha_wide", "seedance", 4,
     PAGE +
     "Christ on the cross, the bare hill, and the darkened sky are all "
     "part of the same finished drawing. His entire body -- head, arms, "
     "hands, and feet -- stays exactly as drawn: His head stays bowed low "
     "in stillness and His arms stay stretched along the crossbeam, "
     "unchanged from the first frame to the last. His hands and feet stay "
     "exactly as drawn, with no wound, no blood, no red mark, no nail, no "
     "puncture appearing or growing anywhere on them at any point in the "
     "clip. Every cloud shape in the painted sky keeps its exact form and "
     "position. The only movement in the whole clip: the dark watercolor "
     "of the sky very gently darkens and lightens again in a slow, "
     "steady, even rhythm, the whole sky at once, and the pale band of "
     "light along the horizon breathes in the same slow, even rhythm. "
     "Nothing else changes."),

    # REDO ROUND 1 (2026-08-01): wound-lock held (Christ clean), but the
    # negation-primed serpent-lock failed AGAIN -- the bronze serpent's
    # mouth opened wide with an invented tongue by 60% (doctrinally wrong:
    # its deadness/rigidity as cast metal IS the point). Surgical fix: keep
    # LOCK + wound-lock verbatim, replace only the serpent sentence with a
    # positive "solid cast metal" description, never naming a mouth/motion
    # verb to forbid. Stays Seedance (crucifixion-adjacent, NO_KLING_FALLBACK).
    ("s46_thesis_pair", "seedance", 4,
     "Christ's entire body, the cross, and His hands and feet hold their "
     "EXACT position and shape, perfectly still -- no wound, no blood, no "
     "red mark, no nail, no puncture appearing or growing anywhere on them "
     "at any point in the clip. The bronze serpent on its pole is solid "
     "cast metal, part of the drawing: its mouth stays closed and its "
     "coiled shape stays exactly as drawn, rigid from the first frame to "
     "the last. INVENT NOTHING new. Only: the light across the paper "
     "breathes very gently. Nothing else in the frame moves."),

    ("s47_golgotha_midshot", "seedance", 4,
     "Christ's entire body, the cross, and His head, arms, hands, and feet "
     "hold their EXACT current position and shape, perfectly still -- His "
     "hands and feet stay exactly as drawn, with no wound, no blood, no "
     "red mark, no nail, no puncture appearing or growing anywhere on them "
     "at any point in the clip. INVENT NOTHING new. Only: the light across "
     "the scene breathes very gently. Nothing else in the frame moves."),

    ("s48_vc_curse_for_us", "seedance", 4,
     TEXTLOCK +
     "The artwork of Christ behind the card holds perfectly still, with no "
     "wound, no blood, no red mark appearing anywhere at any point. Only: "
     "the light across the paper breathes very gently. Nothing else "
     "changes."),

    # REDO ROUND 1 (2026-08-01): the wound-lock WORKED (hands/feet stayed
    # clean) -- the failure was the HEAD, which was never named/locked
    # (unlocked-region migration): bowed head + closed eyes fully lifted
    # and opened by 90%. Surgical fix -- keep LOCK + wound-lock verbatim,
    # add an explicit positive head/eye state. Stays Seedance (crucifixion-
    # tier, NO_KLING_FALLBACK) -- second failure goes to $0 push-in, not Kling.
    ("s49_christ_radiant_begin", "seedance", 4,
     "Christ's entire body and the cross hold their EXACT position and "
     "shape, perfectly still -- His head stays bowed and His eyes stay "
     "closed, exactly as drawn, from the first frame to the last; His "
     "hands and feet stay exactly as drawn, with no wound, no blood, no "
     "red mark, no nail, no puncture appearing or growing anywhere at any "
     "point. INVENT NOTHING new. Only: the warm light around Him pulses "
     "very gently brighter and dimmer in a steady, even glow -- " +
     NOGLITTER + "Nothing else in the frame moves."),

    ("s50_christ_close_words", "seedance", 4,
     "Christ's face and body hold their EXACT position and expression, "
     "perfectly still, exactly as drawn, from the first frame to the "
     "last -- His lips and mouth stay fully closed and never part, open, "
     "or move even slightly at any point in the clip; His eyes never "
     "blink or change; no wound, no blood, no red mark appearing anywhere "
     "at any point. The warm glow around His head and shoulders keeps its "
     "EXACT size, shape, and outer edge from the first frame to the last "
     "-- it never grows, spreads, or reaches further outward than where "
     "it already sits in the very first frame. INVENT NOTHING new. Only: "
     "within that fixed edge, the warm glow pulses very gently brighter "
     "and dimmer in a steady, even rhythm -- " + NOGLITTER +
     "Nothing else in the frame moves."),

    # REDO ROUND 3b (2026-08-02): user caught real lip/mouth movement in the
    # first fix's render (a close reverent face shot invites a talking-head
    # read even with the halo-lock fixed) -- confirmed on a 30-frame dense
    # sheet the earlier 16-frame check missed. The old lock said "no lip
    # movement" but never named the mouth staying CLOSED explicitly enough;
    # strengthened per the same unlocked-region-migration pattern as every
    # other fix this round.

    # REDO ROUND 3 (2026-08-02): the wet-in-wet restyle (STYLE_SL06) bakes a
    # bloomed halo into the STILL itself; the old vague "light breathes"
    # motion, unchanged since before the restyle, let the animator read
    # that bloom as CONTINUING to spread rather than a fixed glow pulsing --
    # confirmed via a 16-frame dense sheet showing the halo growing from a
    # faint wash to a full bullseye ring with zero recession across the
    # whole clip (licensed-motion-escalation, same mechanism as s16/s30).
    # Fix: explicit edge-lock on the glow + reworded to the proven
    # pulses-brighter-dimmer-within-a-fixed-shape pattern already used on
    # s49. Stays Seedance (crucifixion-tier, NO_KLING_FALLBACK).

    # REDO ROUND 1 (2026-08-01): Christ himself stayed clean; the failure
    # was tail-end (~90% of the original 8s clip) -- a small light patch
    # appeared near a FOREGROUND onlooker's head. Root cause: the lock only
    # named "every distant figure" (unlocked-region migration -- the near
    # foreground group was never locked), and 8s doubles the late-drift
    # window every other defect in this batch also bloomed into. Fix:
    # duration 8->4 (assembly loops/extends the hold, per longform-motion-
    # fill, already standard practice) + lock EVERY figure, near and far.
    # Stays Seedance (crucifixion-tier, NO_KLING_FALLBACK).
    ("s51_christ_draw_all_men", "seedance", 4,
     "Christ holds His EXACT radiant position and shape, perfectly still "
     "-- no wound, no blood, no red mark, no nail, no puncture appearing "
     "or growing anywhere at any point. Every figure below Him, near and "
     "far -- the onlookers in the foreground and the pilgrims in the "
     "distance -- stays exactly as drawn: every head, face, hand, and "
     "garment unchanged from the first frame to the last. INVENT NOTHING "
     "new. Only: the warm gold light around and behind Him pulses very "
     "gently brighter and dimmer in a steady, even "
     "glow -- " + NOGLITTER + "Nothing else in the frame moves."),

    # REDO ROUND 1 (2026-08-01): talking-head/interview prior -- a visible
    # push-zoom cropped the staff/hands and the torn-paper page-edge out of
    # frame entirely by 75% (seedance1_5 has no camera_fixed param, so the
    # lock is prompt-only -- "does not move, zoom" negation failed). PAGE
    # reframe + explicit "whole page stays in frame" anchor, since the zoom
    # can't happen without visibly cropping the page.
    ("s52_moses_reflecting", "seedance", 4,
     PAGE +
     "Moses stays exactly as drawn: seated facing the viewer, both hands "
     "resting on the staff across his lap, mouth closed. The whole page "
     "stays in frame the entire time, including the staff and both hands "
     "at the bottom. The only movement in the whole clip: the light across "
     "the paper slowly and very slightly brightens and dims. Nothing else "
     "changes."),

    # REDO ROUND 1 (2026-08-01): unlocked-region migration -- only the face
    # was locked, so the hand drifted from resting on his chest (2-30%) to
    # the staff (40%+). PAGE reframe, whole-figure positive-state lock.
    ("s53_moses_know_that_now", "seedance", 4,
     PAGE +
     "Moses stays exactly as drawn: one hand gripping the upright staff, "
     "the other hand resting flat on his chest, mouth closed, gaze "
     "steady. The only movement in the whole clip: the light across the "
     "paper slowly and very slightly brightens and dims. Nothing else "
     "changes."),

    ("s54_timeshift_enshrined", "kling", 5,
     "Every worshipping figure holds their exact posture, perfectly frozen "
     "-- no one bows, steps, or gestures. The enshrined bronze serpent "
     "holds its EXACT shape and position, perfectly frozen -- it never "
     "moves, uncoils, or slithers. INVENT NOTHING new. Only: the incense "
     "smoke already in the air drifts and curls very slowly upward, the "
     "lamp light breathes very gently. Nothing else in the frame changes."),

    # s55_hezekiah_breaks: EXCLUDED -- eye-checked frozen-mid-strike class
    # (see module docstring). $0 push-in + impact-burst is the default.

    ("s56_moses_affirms", "seedance", 4,
     "Moses's face holds its exact affirming expression, perfectly still "
     "-- no blink, no head movement, no lip movement. Only: the light "
     "across his face breathes very gently. Nothing else changes."),

    # Eye-checked 2026-08-01: diptych -- elder Moses with staff (left) and
    # Christ standing radiant in a halo glow (right), NOT on the cross.
    ("s57_bridge_moses_christ", "seedance", 4,
     "Moses and Christ both hold their EXACT poses and expressions, "
     "perfectly still -- no blink, no gesture, no movement of the staff or "
     "hands. Only: the soft halo glow around Christ breathes very gently "
     "brighter and dimmer in a steady, even glow -- " + NOGLITTER +
     "Nothing else in the frame changes."),

    # REDO ROUND 1 (2026-08-01): gold flakes/particles appeared and
    # increased in the background light by 98% -- of 7 NOGLITTER jobs in
    # this episode, only this one glittered, and it has the strongest
    # full-frame gold-ray context of any of them (radiant-gold priming).
    # The source still is confirmed letterless (Scribed Ink verse text is
    # composited later at assembly, not baked into the AI render) -- so
    # TEXTLOCK's text-nouns are dead weight that may be inviting glyph-like
    # marks; dropped. NOGLITTER's own particle nouns ("sparkle... particles
    # ...glitter") may be priming exactly what they forbid (this project's
    # own seedream-no-negative-channel lesson) -- replaced with positive-
    # only "one smooth continuous wash" language. Second failure -> the
    # script's own pre-approved VC fallback: $0 camera pan. Stays Seedance
    # (crucifixion-tier, NO_KLING_FALLBACK).
    ("s58_vc_john316", "seedance", 4,
     "The radiant artwork of Christ stays exactly as drawn, perfectly "
     "still from the first frame to the last. The golden light behind Him "
     "stays one smooth, continuous, unbroken wash of watercolor, and its "
     "glow rises and settles very gently and evenly across the whole "
     "background at once. Nothing else changes."),

    # --- Beat 7: the CTA (spreads 59-66) ---
    # REDO ROUND 1 (2026-08-01): talking-head prior -- mouth visibly opened
    # (50-75%) then closed again (98%), an invented speech gesture despite
    # "no lip movement" (the exact negated verb). PAGE reframe, "mouth
    # closed" as a positive state.
    ("s59_moses_be_still", "seedance", 4,
     PAGE +
     "Moses stays exactly as drawn: one palm raised toward the viewer, "
     "the staff in his other hand, mouth closed, gaze steady. The only "
     "movement in the whole clip: the light across the paper slowly and "
     "very slightly brightens and dims. Nothing else changes."),

    ("s60_vignette_selfeffort", "kling", 5,
     "Every struggling figure holds their exact straining posture, "
     "perfectly frozen -- no one walks, staggers, or moves; each failed "
     "effort stays exactly as drawn. INVENT NOTHING new. Only: faint dust "
     "drifts low across the ground. Nothing else in the frame changes."),

    ("s61_moses_thatisyou", "seedance", 4,
     "Moses's face holds its exact intimate expression and gaze, perfectly "
     "still -- no blink, no head movement, no lip movement. Only: the "
     "light across his face breathes very gently. Nothing else changes."),

    # REDO ROUND 1 (2026-08-01): same push-zoom failure as s52 -- progressive
    # zoom-in cropped a hand out of frame and enlarged the face by 60-98%.
    # PAGE reframe + "whole page stays in frame, torn edge to torn edge."
    ("s62_moses_neverasked", "seedance", 4,
     PAGE +
     "Moses stays exactly as drawn: facing the viewer, mouth closed, "
     "steady gaze. The whole page stays in frame the entire time, from "
     "torn edge to torn edge. The only movement in the whole clip: the "
     "light across the paper slowly and very slightly brightens and "
     "dims. Nothing else changes."),

    # Eye-checked 2026-08-01: Christ lifted radiant in rays of light, three
    # small figures below (man / child / elder) looking up -- no cross, but
    # lifted-Christ iconography stays on the Seedance tier (wound risk
    # dominates, per the short's own s13_lifted reasoning). 8s glory hold.
    ("s63_vignette_least_last_child", "seedance", 8,
     "Christ holds His EXACT lifted radiant position and shape, perfectly "
     "still -- His hands and feet stay exactly as drawn, with no wound, no "
     "blood, no red mark appearing anywhere at any point. The three "
     "figures below -- the man, the child, and the elder -- hold their "
     "exact upturned postures, perfectly frozen. INVENT NOTHING new. Only: "
     "the rays of warm light around Him pulse very gently brighter and "
     "dimmer in a steady, even glow -- " + NOGLITTER + "Nothing else in "
     "the frame moves."),

    # Near-silence pause beat -- minimum possible named motion.
    # REDO ROUND 1 (2026-08-01): the vaguest lock in the whole batch ("no
    # movement of any kind" with no positive pose description at all) --
    # by 80% Moses's entire posture had changed (hunched/clasped/gaze-down
    # became upright/hands-on-lap/gaze-lifted, staff repositioned). PAGE
    # reframe with an explicit whole-figure positive-state description.
    ("s64_moses_sit_with_that", "seedance", 4,
     PAGE +
     "Moses stays exactly as drawn: seated on the rock, head bowed, gaze "
     "down, hands clasped together over the staff. The only movement in "
     "the whole clip: the warm light across the paper slowly and very "
     "slightly brightens and dims, like a cloud passing far away. Nothing "
     "else changes."),

    # Eye-checked 2026-08-01: Christ standing plain on open paper, open
    # hands -- not on the cross; simple freeze + gentle light.
    ("s65_christ_open_invite", "seedance", 4,
     "Christ holds His exact open-handed stance and expression, exactly as "
     "drawn, from the first frame to the last -- no blink, no gesture, no "
     "step, no sway, no shift of weight; His open hands, arms, and feet "
     "never move. His robe -- its hem, its sleeves, its folds, and the "
     "knotted belt with its hanging tassels -- keeps its EXACT shape and "
     "position throughout, unmoving, never swinging or billowing. INVENT "
     "NOTHING new. Only: the light across the paper breathes very gently. "
     "Nothing else changes."),

    # REDO ROUND 3b (2026-08-02): user reported "he seems to be a dance" --
    # confirmed real via a tight figure-crop 16-frame sheet: the robe hem
    # and belt tassels were swinging/billowing between frames, and the body
    # showed a faint side-to-side shift -- unlocked-region migration, same
    # mechanism as s45's original dancing defect. The old lock only named
    # hands/gesture/blink; the robe and belt were never named so they drifted
    # freely. Fix: explicit lock on the robe, hem, and belt/tassels, matching
    # the same pattern already proven on s45.

    ("s66_moses_direct_question", "seedance", 4,
     "Moses holds his exact direct gaze toward the viewer, perfectly still "
     "-- no blink, no head movement, no lip movement. Only: the light "
     "across his face breathes very gently. Nothing else changes."),

    # s67_insert_gilded_proclamation2 / s68_landing: $0 deterministic
    # devices (insert-page pan / tear_hole landing) -- not in this list.
]


@contextlib.contextmanager
def _note_override(note):
    """A.run_job's cost.record_hf call hardcodes note=f"[piece1-v2] {name}"
    (same reasoning as bronze_serpent/_s3_animate.py: rather than fork
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
        # PAGE already includes its own full framing -- SELF_CONTAINED
        # motion strings are NOT prepended with LOCK (see PAGE's own
        # docstring above, redo round 1).
        prompt = motion if name in SELF_CONTAINED else LOCK + motion
        with _note_override(f"[bronzeserpentlong] {name}"):
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
