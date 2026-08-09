"""Seed of the Woman LONG -- stills stage. Spreads 1-5 promoted from the
POC30 process-validation test (memory `day-of-atonement-retro-learnings`);
extend SPREAD_SHOTS as the full plan is authored. Follows the exact
code pattern of day_of_atonement/_s2_stills.py (same STYLE constant, same
repo-level cast-bible anchor chaining, same FULLBLEED framing note, same
run()/resolve_refs()/main() shape) -- fix #9 (check the sibling episode's
real script chain before assuming a generic skill applies).

Renders, in order: 3 anchors (Adam, Eve, Eden world -- new cast/world dir,
$0 cross-style reuse is not possible per the locked provider-split rule),
then the 5 spread stills chained to those anchors. Every prompt authored
per the fix #7 discipline (camera-angle/shot-type from _PREFLIGHT.md,
period-accurate detail -- fig-leaf aprons per Gen 3:7, not skin coats,
which come later at 3:21) BEFORE the first render, not learned via re-roll.

  .venv\\Scripts\\python.exe poc_living_sketchbook/seed_of_the_woman/_s2_stills.py
"""
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "SeedOfTheWoman"
HERE = Path(__file__).resolve().parent
CAST = HERE.parent / "cast"
WORLD = HERE.parent / "world"
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

ADAM_REF = CAST / "adam_ref.png"
EVE_REF = CAST / "eve_ref.png"
EDEN_REF = WORLD / "eden_ref.png"
SERPENT_REF = WORLD / "serpent_ref.png"
JESUS_REF = CAST / "jesus_ref.png"
DESK_REF = WORLD / "desk_ref.png"

JESUS_S51_REF = OUT / "s51_bearing_wages.png"

REF_MAP = {"adam": ADAM_REF, "eve": EVE_REF, "eden": EDEN_REF, "serpent": SERPENT_REF,
           "jesus": JESUS_REF, "desk": DESK_REF, "jesus51": JESUS_S51_REF}

# ---- canon text, matching cast/AARON.md's level of detail ----

ADAM = (
    "Adam: the first man, freshly made that same day (Genesis 2:7) -- a "
    "man in the full prime of life, never old, never a boy. Face geometry: "
    "a strong open brow, straight nose, firm jaw, unweathered skin -- a "
    "face with no lines of age yet, only the new shock of fear and shame. "
    "Hair: dark brown, short, natural, uncut (no barber has ever touched "
    "it). Beard: short, close, natural growth, never groomed or shaped by "
    "a blade. Skin: warm olive Near-Eastern complexion, entirely "
    "unweathered -- this is the FIRST day anyone has ever been afraid. "
    "Build: powerfully made, broad-shouldered, an unspoiled human frame in "
    "its prime. Eyes: wide, stricken, ashamed -- a man who has never once "
    "before felt fear. Garment: a crude covering of stitched fig leaves "
    "tied at the waist as an apron (Genesis 3:7) -- NOT a coat of animal "
    "skin (that comes later, Genesis 3:21, after this scene) -- otherwise "
    "bare-chested, no other clothing of any kind."
)

EVE = (
    "Eve: the first woman, freshly made that same day (Genesis 2:22) -- a "
    "woman in the full prime of life, never old, never a girl. Face "
    "geometry: soft even features, wide clear eyes, a face with no lines "
    "of age yet, only the new shock of fear and shame. Hair: long, dark, "
    "loose and natural, uncut and unbound by any ornament (no comb, no "
    "clasp, no ribbon has ever touched it). Skin: warm olive Near-Eastern "
    "complexion, entirely unweathered. Build: an unspoiled human frame in "
    "its prime. Eyes: wide, stricken, ashamed -- a woman who has never "
    "once before felt fear. Garment: a crude covering of stitched fig "
    "leaves (Genesis 3:7) wrapped and tied to cover the body -- NOT a coat "
    "of animal skin (that comes later, Genesis 3:21, after this scene) -- "
    "modestly but roughly covered, nothing woven, nothing dyed, nothing "
    "ornamental."
)

EDEN = (
    "The garden of Eden at the cool of the day (Genesis 3:8): dense, "
    "unspoiled, ancient trees with heavy dark-green canopy, dappled "
    "warm-gold late-afternoon light breaking through in shafts, thick "
    "underbrush and broad-leafed plants at ground level offering places to "
    "hide, no path, no cultivation lines, no structure of any kind visible "
    "-- a wild, lush, pre-agricultural paradise, now carrying the FIRST "
    "shadow it has ever had to carry: the light still golden but the mood "
    "gone wrong, a faint coolness/greyness creeping in at the forest's "
    "deep background edges as if the garden itself senses the fall."
)

STYLE = (
    "Editorial documentary sketch illustration: loose confident graphite-and-ink "
    "linework with muted watercolor wash, drawn on aged warm cream paper. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured stock, "
    "torn and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile hand-made "
    "feel, muted ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge. CRITICAL: absolutely NO lettering, numerals, words, newsprint, "
    "printed book-page text, handwriting, ruler markings, dates, or captions "
    "ANYWHERE on ANY layer -- every paper surface is BLANK textured stock."
)

SERPENT = (
    "A real serpent, plainly drawn in loose graphite-and-ink linework "
    "matching this style's own hand -- no dragon fantasy, no wings, no "
    "expressive or anthropomorphic face, no upright posture, no charm. "
    "Ink-blue-toned scales, cool judgment coloring, never gold, never "
    "warm. Before the curse: coiled low among tree branches or roots, "
    "still and watching."
)

JESUS = (
    "Jesus: a Judean man in his early thirties. Face geometry: a strong "
    "straight nose, defined cheekbones, a broad calm forehead, an angular "
    "jaw beneath the beard. Hair: long dark wavy hair falling past the "
    "shoulders, parted center. Beard: short, close-cropped, dark, "
    "well-kept. Skin: sun-weathered olive Mediterranean complexion. "
    "Build: lean and wiry-strong, a carpenter's and traveler's frame. "
    "Eyes: warm deep brown, level and calm. Hands: strong, calloused, a "
    "craftsman's hands -- the SAME man as the reference image, identical "
    "face, beard, and hair."
)

LORD_PRESENCE = (
    "the presence of the LORD: no figure, no face, no human or angelic "
    "form of any kind -- only a low warm golden light moving gently among "
    "the trees, felt as an overwhelming approaching presence rather than "
    "seen as a person."
)

FULLBLEED = (
    "CRITICAL FRAMING: zoom in close enough that the illustrated subject "
    "and its immediate surroundings occupy the ENTIRE frame, corner to "
    "corner, no wide empty margins of bare paper around the main subject."
)

DESK = (
    "a worn wooden writing desk in the Keeper's own study nook: aged dark "
    "timber grain, close and cluttered, a small clay oil lamp burning warm "
    "at one side, a cut reed pen resting still, a small stoppered ink pot, "
    "a folded cloth -- ordinary desk-top objects filling the corners of "
    "the frame, nothing floating in bare space. No hands, no figure "
    "present unless the scene says otherwise."
)

MARY = (
    "a young Judean woman, bowed low, veiled head to shoulder in plain "
    "undyed cloth, face turned fully down and away from camera so no "
    "facial features are legible -- identity deliberately withheld, only "
    "her bowed silhouette and gathered hands read. Hands drawn together "
    "at her heart, fingers loosely folded, anatomically correct, no "
    "elongated or extra digits. Garment: plain, rough, unornamented, "
    "modestly covering."
)

# ---- sl20 (Sketchbook Spread) style-variant block -- the episode's FIRST
# committed style-variant use, per _PLAN.md sec.5b + the user's standing
# note to actually ship the full style library, not just baseline. v2
# recipe only (STYLE_LAB.md #20) -- the v1 prompt is REJECTED (baked
# garbled captions); this version renders clean on both bake-off
# characters and is production_approved on the condition it's used as-is.
SL20_STYLE = (
    "Editorial documentary sketch illustration on an aged warm cream "
    "sketchbook spread: one main resolved drawing surrounded by six or "
    "seven small loose sketch fragments of the SAME subject's own nearby "
    "details from other angles, arranged loosely around it as quick "
    "graphite marks, no notation of any kind. Coffee ring, thumbprint, "
    "faint binding shadow down the centre. Loose graphite-and-ink "
    "linework, muted watercolor wash, halftone grain, narrow torn-paper "
    "margin, a thin strip of gold leaf at one edge. Fills the spread "
    "corner to corner. CRITICAL: absolutely NO lettering, numerals, "
    "words, newsprint, printed book-page text, handwriting, ruler "
    "markings, dates, notes, annotations, or captions ANYWHERE on ANY "
    "layer -- every paper surface is BLANK textured stock."
)

# ---- anchors (eden_ref FIRST -- adam/eve chain to it for a consistent
# background; order matters, resolve_refs() only finds refs already on disk) ----
ANCHOR_SHOTS = [
    ("eden_ref", STYLE, "",
     f"{EDEN} Wide establishing view, eye-level, no figures present. "
     f"{FULLBLEED}"),
    ("adam_ref", STYLE, "eden",
     f"Portrait, medium shot, eye-level: {ADAM}, standing among the trees "
     f"of the same garden, caught mid-motion trying to hide, looking "
     f"back over his shoulder toward the camera with dawning fear. "
     f"{FULLBLEED}"),
    ("eve_ref", STYLE, "eden",
     f"Portrait, medium shot, eye-level: {EVE}, standing among the trees "
     f"of the same garden, caught mid-motion trying to hide, looking "
     f"back over her shoulder toward the camera with dawning fear. "
     f"{FULLBLEED}"),
    ("serpent_ref", STYLE, "eden",
     f"{SERPENT} Resting low among the roots and branches of the same "
     f"garden's trees, no other figure present, the camera looking DOWN "
     f"on it (per world/SERPENT.md's locked camera rule -- the lens never "
     f"kneels to the enemy). {FULLBLEED}"),
    # NEW (batch 4): the study desk -- a recurring SETTING reused across
    # s26/32/38/39/40/46/60/66 per _PREFLIGHT.md's asset table, built once
    # here and re-dressed per spread. Rendered in BASELINE style (not the
    # sl20 variant s26 itself uses) so it stays a stable, plain identity/
    # geometry reference every later baseline re-dress can chain to.
    ("desk_ref", STYLE, "",
     f"MEDIUM shot, eye-level establishing view: {DESK} A single blank "
     f"page of aged parchment lies flat and empty at the desk's center, "
     f"entirely blank, no writing of any kind. {FULLBLEED}"),
]

# ---- the 5 real spreads ----
SPREAD_SHOTS = [
    ("s01_something_wrong", STYLE, "adam,eve,eden",
     f"HIGH-ANGLE wide view looking down into the garden: {ADAM} and "
     f"{EVE}, small and distant in the frame against the vast unspoiled "
     f"canopy of {EDEN.split(':')[0]}, both crouched low near a dense "
     f"thicket, backs turned to the camera, isolated and small against "
     f"the scale of the garden -- the first faint wrongness showing only "
     f"as a cool greyness bleeding in at the frame's far edges. "
     f"{FULLBLEED}"),
    ("s02_the_hiding", STYLE, "adam,eve,eden",
     f"MEDIUM shot, eye-level, camera positioned low among broad-leafed "
     f"undergrowth as if hiding alongside them: {ADAM} and {EVE} pressed "
     f"close together behind a thick tree trunk and heavy foliage, "
     f"genuinely concealed (not merely standing near cover), both facing "
     f"AWAY from camera toward unseen approaching light, tense stillness. "
     f"{FULLBLEED}"),
    ("s04_god_walking", STYLE, "eden",
     f"WIDE-ANGLE, LOW angle looking UP through the tree canopy: "
     f"{LORD_PRESENCE} moving gently through {EDEN.split(':')[0]}, "
     f"golden light catching the undersides of leaves and drifting motes "
     f"of pollen/dust in the beams, no figure of any kind, the whole "
     f"canopy responding to the light's slow movement. {FULLBLEED}"),
    ("s05_where_art_thou", STYLE, "eden",
     f"Close, held, eye-level: {LORD_PRESENCE} now still, resting low "
     f"and warm in a gap between two tree trunks, framed by dark "
     f"foliage on both sides so the light itself is the entire subject "
     f"of the frame, quiet and waiting. {FULLBLEED}"),
    # test-tier spreads (2026-08-07, independent-review staged build order):
    # serpent's first on-screen appearance + the hardest identity+motion
    # still in the episode -- full QC here before the serpent's other ~17
    # appearances build on top of it.
    ("s06_blame_circle", STYLE, "adam,eve,serpent,eden",
     f"MEDIUM shot, eye-level: {ADAM} and {EVE} together among the trees, "
     f"Adam's arm extended toward Eve in a blaming gesture, Eve turning "
     f"her head down and away toward {SERPENT.split('.')[0]} coiled low "
     f"in the leaves at the bottom edge of the frame -- exactly three "
     f"figures present (Adam, Eve, the serpent), count them, no others. "
     f"{FULLBLEED}"),
    # s16: the full sentencing tableau in ONE wide frame -- hunt_and_lock
    # (a real device, panel_animator/hunt_and_lock.py) animates the camera
    # hunting toward the serpent's own position within this still; the
    # still itself must show the whole scene, not a pre-cropped close-up.
    ("s16_sentencing_tableau", STYLE, "adam,eve,serpent,eden",
     f"WIDE shot, eye-level, the full scene in one frame: {ADAM} and "
     f"{EVE} standing together braced for judgment on one side, "
     f"{LORD_PRESENCE} present but not facing them, and "
     f"{SERPENT.split('.')[0]} low in the dust at the LOWER portion of "
     f"the frame, clearly visible and separated from the two human "
     f"figures -- exactly three figures present (Adam, Eve, the "
     f"serpent) plus the light-presence, count them, no others. "
     f"{FULLBLEED}"),
    # s51: the Jesus multi-pose identity-lock anchor (_PREFLIGHT.md) --
    # every later Jesus spread (s42/s43/s50/s53-56/s64/s66/s71) chains off
    # THIS approved render as a 2nd reference. LOW angle, closer framing
    # per _PREFLIGHT.md's camera table; reverent wound-free treatment,
    # thin gold-leaf edge present -- reusing this project's own proven
    # crucifixion wording (day_of_atonement/_s2_stills.py s53/s54).
    # REDESIGNED (2026-08-08, 3rd attempt): open/gripping hand poses kept
    # failing anatomy (extra/fused/elongated digits) across 2 tries. Rather
    # than re-roll the same exposed-hand composition a 3rd time, changed
    # the STAGING itself, following the proven precedent already shipped
    # in this exact sibling episode (day_of_atonement/stills/
    # s54_guilt_laid_on_christ.png): a plain cord/rope wrapped around each
    # wrist against the beam, low-detail loosely-curled fingers mostly
    # tucked against the wood rather than fully exposed/splayed -- far
    # less hand geometry for the model to get wrong, and it already
    # rendered clean once in this repo's own style.
    ("s51_bearing_wages", STYLE, "jesus",
     f"Close, reverent view, LOW angle looking slightly up: {JESUS} upon "
     f"the cross, head bowed, upper body and bowed face the sharp focus "
     f"of the frame, arms stretched along the crossbeam. At each wrist, a "
     f"plain undyed cord is wrapped twice around the wrist and the wood, "
     f"holding the arm steady against the beam -- the hand itself mostly "
     f"TUCKED AND CURLED IN toward the wood behind the cord wrap, only a "
     f"simple soft curled shape of knuckles visible, fingers loosely "
     f"folded together and NOT individually splayed or spread apart, low "
     f"anatomical detail, natural proportions, no elongated or extra "
     f"digits. Wound-free and restrained -- no visible wound, no blood, "
     f"no graphic detail of any kind. A thin strip of gold leaf remains "
     f"visible along one edge of the page (glory never fully absent, "
     f"even here). The sky behind Him unnaturally dark at midday, a flat "
     f"heavy stillness, NOT storm clouds, no wind, no rain, no roiling "
     f"shapes. {FULLBLEED}"),
    # ---- batch 2 (2026-08-07 later night, spreads 7-15) ----
    # s07 and s14 are $0 composites over EXISTING art (s06's own render /
    # eden_ref.png) per _PLAN.md's own device column -- no new still here.
    ("s08_coming_apart", STYLE, "adam,eve,eden",
     f"WIDE shot, slightly HIGH angle: {ADAM} and {EVE}, separated by "
     f"empty dead-center negative space between them, both small within "
     f"the frame, a few autumn-like leaves drifting down through the "
     f"space between them, the garden's color visibly draining toward "
     f"grey at the far edges of the frame -- isolation and unraveling. "
     f"{FULLBLEED}"),
    ("s09_unexpected_place", STYLE, "eden",
     f"EXTREME LOW, close crop of bare GROUND and dust, camera HIGH "
     f"looking straight down: the page gone almost entirely dark, one "
     f"single small warm gold fleck of light glowing faintly in the dust "
     f"at the very lowest margin of the frame -- nothing else visible, no "
     f"figures, no plants, just dark dust and the one gold fleck. "
     f"{FULLBLEED}"),
    ("s10_judgment_falls", STYLE, "eden",
     f"VERY WIDE, HIGH OVERHEAD angle looking straight down: the whole "
     f"garden of Eden laid out as one unified shape far below, one long "
     f"dark shadow stretching and lengthening across the canopy, no "
     f"figures visible, the scale vast and impersonal. {FULLBLEED}"),
    ("s11_afraid_of_presence", STYLE, "adam,eve,eden",
     f"MEDIUM two-shot, eye-level, camera positioned low among the tree "
     f"trunks as if peering between them (occlusion): {ADAM} and {EVE} "
     f"crouched close together, both bracketed by dark tree trunks in the "
     f"foreground, a warm light presence glowing beyond them out of "
     f"frame, both faces turned away and averted from the light. Any "
     f"visible hand is anatomically correct, exactly five fingers "
     f"including a clearly separate thumb, natural proportions, no "
     f"elongated or extra digits. {FULLBLEED}"),
    ("s12_creatures_word", STYLE, "eve,serpent,eden",
     f"CLOSE profile shot, eye-level. CRITICAL COLOR TREATMENT: this "
     f"entire image is rendered almost MONOCHROME, near-grayscale sepia "
     f"-- every color drained down to faint dusty grey-brown tones only, "
     f"NO green, NO warm gold light anywhere, as flat and washed-out as a "
     f"faded old photograph -- this is a flashback memory, not the "
     f"present moment, and must look visibly, obviously different in "
     f"color from every other spread in this style. Within that "
     f"near-grayscale treatment: {EVE} her ear and turned profile "
     f"inclined toward {SERPENT.split('.')[0]} coiled still and unmoving "
     f"in the branches just behind her, listening. The tree bark and "
     f"branches are smooth, plain woodgrain texture ONLY -- absolutely no "
     f"scratches, scribbles, marks, or squiggles anywhere on the bark "
     f"that could be mistaken for handwriting or lettering of any kind. "
     f"{FULLBLEED}"),
    ("s13_the_fruit", STYLE, "eden",
     f"MACRO object insert, camera near-ground: a single piece of ripe "
     f"fruit fallen in the garden dust, one clear bite missing from it, "
     f"sharp and large in the frame, the garden softly out of focus "
     f"behind it in shallow depth of field, no figures, no hands. "
     f"{FULLBLEED}"),
    # s14: a DEDICATED still, not a raw eden_ref.png reuse -- motion_lint
    # caught the wash-creep device producing zero real motion (p95=0.000)
    # because eden_ref.png has no actual blue-grey wash region for
    # panel_animator/wash_creep.py's isolate_storm_wash() (HSV hue 95-140)
    # to isolate and grow; a still with the wash already visibly present
    # at the edges is required, same as Storm's own s01/s04 stills.
    ("s14_death_enters", STYLE, "eden",
     f"Wide establishing view, eye-level, no figures present: "
     f"{EDEN.split(':')[0]}, but a dark ink-blue-grey watercolour wash is "
     f"visibly bleeding and creeping inward from all four edges of the "
     f"frame like spreading stain on damp paper -- a clear, fibrous, "
     f"feathered blue-grey front encroaching from the borders, cool and "
     f"desaturated (matching this style's own muted ink-blue accent "
     f"tone), while the center of the frame still shows the garden's "
     f"natural warm green/gold color untouched. No figures. {FULLBLEED}"),
    ("s15_the_breach", STYLE, "adam,eve,eden",
     f"WIDE shot, slightly LOW angle from the near rim: a single DRAWN "
     f"chasm (an inked line splitting the page itself, never a "
     f"torn-paper edge) runs diagonally across the frame -- on the far "
     f"side, the garden sits HIGH and brightly lit; on the near side, "
     f"{ADAM} and {EVE} stand small and dim at the chasm's edge, no "
     f"bridge of any kind between the two sides. {FULLBLEED}"),
    # ---- batch 3 (2026-08-08, spreads 17-25, movement 3 close) ----
    # s19/s22/s23 are $0 composites over s18's / s21's own already-rendered
    # art (same reuse pattern as s07 over s06) -- no new stills for those.
    # The gold thread itself is NEVER painted into any still -- it's a
    # procedural device overlay (panel_animator/thread_device.py, drawn
    # from a bbox at build time), so none of these prompts depict it.
    ("s17_not_adam_not_eve", STYLE, "adam,eve,eden",
     f"MEDIUM two-shot, eye-level: {ADAM} and {EVE} standing close "
     f"together, braced and tense as if awaiting judgment, a warm light "
     f"entering the frame from one edge but NOT falling directly on "
     f"either of their faces -- both remain in soft shadow, unlit. "
     f"{FULLBLEED}"),
    ("s18_turns_to_serpent", STYLE, "serpent,eden",
     f"WIDE shot, HIGH angle looking DOWN (per world/SERPENT.md's locked "
     f"camera rule -- the lens never kneels to the enemy): "
     f"{SERPENT.split('.')[0]} alone, low in the dust, no human figures "
     f"present, a warm light beginning to fall directly onto it from "
     f"above, accused and exposed. {FULLBLEED}"),
    # REDESIGNED (2026-08-08): first render of s20 came back as a
    # near-duplicate of s18's own wide coiled-in-roots composition -- a
    # real repetition defect, not a minor nit. _PREFLIGHT.md is explicit
    # s20 must differ from s18 by real compositional grammar (SCALE), so
    # this prompt forces a genuinely different crop, not just a re-roll of
    # the same framing.
    ("s20_pure_curse", STYLE, "serpent",
     f"EXTREME CLOSE-UP macro crop, HIGH angle looking straight down -- "
     f"fill the ENTIRE frame with {SERPENT.split('.')[0]}'s own scaled "
     f"body and belly pressed flat to the bare ground; NO wide tree-root "
     f"environment, no cave-like root archway, no surrounding forest "
     f"visible anywhere in this frame at all, only scales and bare dust "
     f"filling every edge. Rendered in a cool ink-blue-grey judgment "
     f"color register, desaturated, no warm garden tones. {FULLBLEED}"),
    # s21 has NO entry here -- re-scoped 2026-08-08 after 3 wasted re-rolls
    # (near-duplicate of s18, then a real hidden-lettering defect in the
    # crack texture, then a regression back to the near-duplicate). Re-read
    # _PLAN.md's own device column: "Thread draw-on ($0)" -- this spread
    # was NEVER supposed to be a new paid render, it's a $0 composite
    # reusing s20's own already-approved extreme-close-up art (same reuse
    # pattern as s07 over s06), with the gold thread drawn on top
    # procedurally at build time. See build_s21() in _s6_assemble.py.
    ("s24_before_their_sentences", STYLE, "adam,eve,eden",
     f"MEDIUM two-shot, eye-level: {ADAM} and {EVE} standing close "
     f"together in heavy shadow, waiting, sentences not yet spoken, a "
     f"soft warm presence-light glowing gently in one corner of the "
     f"frame only, no thread or lettering visible. {FULLBLEED}"),
    ("s25_promise_in_curse", STYLE, "serpent",
     f"WIDE shot, LOW horizon: {SERPENT.split('.')[0]} low within a dark "
     f"ink-blue judgment-toned band across the lower portion of the "
     f"frame, the space above open and empty, no figures, no thread or "
     f"lettering visible. {FULLBLEED}"),
    # ---- batch 4 (2026-08-08+, spreads 26-35, movement 4) ----
    # Applying the standing device/style-variety note for real: s26 is the
    # episode's FIRST committed style-variant (sl20 Sketchbook Spread,
    # _PLAN.md sec.5b) instead of another baseline render, and every new
    # prompt below carries explicit fill-frame/cinematic composition
    # language, not just the generic FULLBLEED tail -- per the user's
    # 2026-08-08 note (memory feedback-full-style-device-library-cinematic-
    # fill): no dead paper margins unless the emptiness IS the device
    # (s32's gap is the one deliberate exception, called out inline).
    ("s26_her_seed_study", SL20_STYLE, "desk",
     f"Overhead view looking straight down onto the desk (the Keeper's "
     f"own view): a single blank page of aged parchment lying flat and "
     f"empty at the center of the frame -- no writing, no marks -- the "
     f"oil lamp glowing warm just beyond the page's upper-right corner, "
     f"casting a pool of light across it, the reed pen and ink pot "
     f"resting at the page's near edge. No figure, no hands. Small "
     f"sketch fragments scattered in the margins around this main view: "
     f"a quick graphite study of the ink pot's curve, the pen's cut nib, "
     f"the lamp's small flame, a fold of the desk cloth. {FULLBLEED}"),
    ("s27_line_of_fathers", STYLE, "",
     f"Page-scale LATERAL composition on plain aged paper, no background "
     f"setting: a chain of small anonymous robed male figures in "
     f"profile, one behind the next, each a half-generation older toward "
     f"the LEFT edge and younger toward the RIGHT, linked by ONE "
     f"continuous hand-drawn descent-line running through them at chest "
     f"height -- most faces turned away, lowered, or simplified to a "
     f"plain dark silhouette (at most one distant figure carries any "
     f"individual facial detail), no ornament, no lettering of any kind. "
     f"The figures and their drawn line fill the frame's full width, "
     f"corner to corner -- no bare empty paper at either end. {FULLBLEED}"),
    # REDESIGNED (2026-08-08, re-roll 1): first render read Eve as a
    # normal-scale medium figure, not the small/dwarfed hope-against-vast-
    # world contrast _PLAN.md calls for -- explicit extreme-scale-contrast
    # language this time (feedback-camera-angle-dynamism's own device).
    ("s28_clue_lights_up", STYLE, "eve,eden",
     f"WIDE, page-scale composition on a hard diagonal, EXTREME SCALE "
     f"CONTRAST: {EVE} shown TINY and distant, occupying less than "
     f"one-sixth of the frame's height, seated small in the LOWER-LEFT "
     f"corner within the shadowed garden setting, dwarfed by the vast "
     f"dense forest around her; her face turned toward the UPPER-RIGHT "
     f"where a single small warm point of gold light glows in the far "
     f"distance -- the wide space between them filled with soft "
     f"indistinct garden forms, tree trunks, and layered shadow at "
     f"multiple depths (not bare blank paper), no thread, no lettering "
     f"visible. {FULLBLEED}"),
    # s30: designed ACTING spread (Kling) -- Mary deliberately carries NO
    # character anchor (_PREFLIGHT.md, a reverence choice, not an
    # omission); the angel is light-presence only, written fresh here
    # rather than reusing the LORD_PRESENCE constant (angel is not the
    # LORD -- a doctrine distinction worth keeping textually separate).
    ("s30_annunciation", STYLE, "",
     f"MEDIUM shot, camera angled slightly LOW toward the upper field: a "
     f"single warm searching light -- no figure, no face, no form of any "
     f"kind, only light -- fills the UPPER portion of the frame; beneath "
     f"it, {MARY}, her whole bowed figure filling the LOWER portion of "
     f"the frame, small and still beneath the light, within a plain dim "
     f"interior room, rough stone and plaster wall texture visible "
     f"around her (not bare empty space). {FULLBLEED}"),
    ("s32_honest_match", STYLE, "desk",
     f"Overhead view looking straight down onto the desk, high angle, "
     f"perfectly symmetric: TWO separate blank pages of aged parchment "
     f"lie side by side, one left and one right, entirely blank -- no "
     f"writing of any kind on either. A deliberate GAP of bare desk wood "
     f"sits exactly at the center of the frame between them, the desk's "
     f"own grain and the lamp's warm light filling that gap so it reads "
     f"as an intentional empty space -- the composition's own subject, "
     f"not a rendering accident. The two pages and the desk's edges fill "
     f"the rest of the frame corner to corner. {FULLBLEED}"),
    # REDESIGNED (2026-08-08, re-roll 1): first render left the TOP HALF
    # of the frame as bare blank paper (a real FULLBLEED violation) --
    # "very wide lateral" read as license to leave headroom. This version
    # forces the fanned books to occupy the frame's full HEIGHT, not just
    # a diagonal sliver across the bottom.
    ("s33_trajectory", STYLE, "",
     f"WIDE composition: dozens of aged book and scroll pages fanned "
     f"open and overlapping, densely stacked and layered so they fill "
     f"the ENTIRE HEIGHT of the frame from the very top edge to the very "
     f"bottom edge -- no bare empty paper sky or background visible "
     f"above or below the books anywhere. The mass of pages rises on a "
     f"slight diagonal from the LOWER-LEFT toward the UPPER-RIGHT, page "
     f"after page densely layered with real texture and shadow between "
     f"them, the pages themselves are the entire visual content of the "
     f"frame corner to corner. The whole fanned shape bends like one "
     f"long drawn curve toward a single small brilliant point of warm "
     f"gold light glowing at the extreme far-right edge of the frame -- "
     f"vast in scope, the eye pulled the full width AND height of the "
     f"frame toward that one distant point. {FULLBLEED}"),
    # s34: the shared naming-page paper prop (s35/s36 reuse this SAME art,
    # $0 composites with accumulating Scribed Ink lettering -- no new
    # render for either, same reuse pattern as s07-over-s06 / s21-over-s20).
    # REDESIGNED (2026-08-08, re-roll 1): first render was near-identical
    # to s26/s32/desk_ref (same lamp+pen+inkpot+cloth arrangement in the
    # same corners) -- a real repetition risk this project's own contact-
    # sheet lesson exists to catch. Dropped the "desk" chain entirely and
    # gave the page its OWN distinguishing physical marks instead of
    # reusing the desk's furniture as the visual identity.
    ("s34_naming_serpent", STYLE, "",
     f"Overhead view looking straight down, no desk or furniture visible "
     f"at all: ONE large open page of aged, heavily worn parchment fills "
     f"the ENTIRE frame corner to corner -- no lamp, no pen, no inkpot, "
     f"no cloth, no surrounding objects of any kind. The page is "
     f"entirely blank of any text, but carries real physical age "
     f"distinct from any other page in this story: heavy foxing spots "
     f"clustered in one corner, a faint ring-shaped water stain, a "
     f"short frayed loose cord looped once across one corner as if it "
     f"once bound the page shut, soft deep creases. A single dim shaft "
     f"of light falls across the page's upper third only, leaving the "
     f"lower two-thirds in cooler shadow. No figure, no hands. "
     f"{FULLBLEED}"),
    # ---- batch 5 (2026-08-08+, spreads 36-45, movement 4 close + 5) ----
    # s35/s36 need no new entry -- s36 reuses s34's own shared naming-page
    # art (build_s36 trims naming_plate.mp4's 3rd entry, same pattern as
    # build_s34/build_s35). s39 needs no new entry either -- $0 reuse of
    # s38's own wide-desk art, cropped tight to the margin for the
    # keeper-hand device, same reuse pattern as s07-over-s06.
    ("s37_promise_planted", STYLE, "",
     f"EXTREME MACRO, LOW angle looking up along a book's own fore-edge: "
     f"the stacked, layered page-edges of an old book rise like a cliff "
     f"face toward the top of the frame, dense packed paper strata "
     f"filling most of the height; at the very bottom edge, a small "
     f"patch of loose dark drawn soil sits in the narrow gap where the "
     f"pages meet the surface beneath them, one small pale seed resting "
     f"on it -- no sprout, no shoot, no green growth, no thread of any "
     f"kind yet visible, this still shows the seed alone, untouched. No "
     f"figure, no hands, no lettering. {FULLBLEED}"),
    ("s38_skeptic_quiet", STYLE, "desk",
     f"WIDE eye-level view of the SAME writing desk, pulled back much "
     f"further than before so the whole desk sits small within a "
     f"larger, cooler room -- the little clay oil lamp's flame burns "
     f"small and deliberately dimmed, its warm glow reduced to a faint "
     f"glow rather than a bright pool of light; the room's overall "
     f"temperature reads cool and quiet, muted blue-grey tones "
     f"dominating over the desk's usual warm wood and gold accents. The "
     f"reed pen, ink pot, and folded cloth remain in their places but "
     f"small and distant within the wider view. No figure, no hands, no "
     f"lettering. {FULLBLEED}"),
    ("s40_partly_fair", STYLE, "desk",
     f"Overhead view straight down onto the SAME writing desk, close, "
     f"two balanced elements side by side: on the LEFT half, one blank "
     f"page of aged parchment lying flat and empty, no writing of any "
     f"kind; on the RIGHT half, a loose scatter of small quick graphite "
     f"pencil studies on their own separate scraps of paper -- ordinary "
     f"human figures at different ages in a simple descending family "
     f"line: a small child, a young parent, an older grandparent, "
     f"sketched lightly and loosely, faces mostly turned away or "
     f"simplified, no individual detail, nothing formal or finished, "
     f"just quick honest graphite marks. Equal visual weight given to "
     f"both halves. No hands, no figure, no lettering. {FULLBLEED}"),
    ("s41_shape_of_canon", STYLE, "",
     f"HIGH overhead view looking straight down: an entire old book "
     f"lies open with ALL of its pages fanned out from the spine in "
     f"one long continuous arc, page after page splayed and "
     f"overlapping like a deck of cards spread wide, filling the "
     f"ENTIRE frame edge to edge -- dozens of pages, dense and "
     f"layered, curving in one long sweeping arc from one side of the "
     f"frame to the other. No thread, no lettering, no figure, no "
     f"hands visible on any page. {FULLBLEED}"),
    # REDESIGNED (2026-08-08, re-roll 1): first render came back as three
    # equal-sized side-by-side panels with visible torn-paper borders
    # between them -- a real SP-G6 violation (locked rule: vignettes
    # never in panels/arches/windows), caused by writing "on the LEFT...
    # in the CENTER... on the RIGHT" as if briefing three separate boxes.
    # Rewritten to follow this project's own PROVEN multi-vignette recipe
    # from day_of_atonement/_s2_stills.py (s34/s41/s56 etc.): ONE
    # dominant near-foreground figure, gold and vivid, with the other
    # vignettes staggered at DIFFERENT depths behind/around Him, smaller
    # and duller, blending into shared paper texture -- never equal
    # panels.
    ("s42_from_within", STYLE, "jesus,serpent",
     f"Eye-level medium shot: {JESUS}, standing centrally in the near "
     f"foreground, one hand extended in an act of quiet authority, warm "
     f"gold light gathering richly around His whole figure and "
     f"dominating the frame -- behind and around Him, two soft hazy "
     f"memory-vignettes at DIFFERENT depths (true layered staggering, "
     f"never a flat side-by-side split, no hard edges, no panel "
     f"borders, no frames of any kind), both rendered smaller and "
     f"visibly duller/less vivid than He is, without any gold light of "
     f"their own: nearer at one side, {SERPENT.split('.')[0]} coiled "
     f"low, named and cool ink-blue toned; farther at the other side, a "
     f"small dim silhouette of a mother bowed low over a swaddled "
     f"infant. All vignette elements blend softly into the same page's "
     f"own paper texture, no separate paper pieces or collage cutouts "
     f"visible anywhere. No thread yet drawn, no lettering. "
     f"{FULLBLEED}"),
    # s43: Kling spread (multi-figure crowd, locked comic-grid cost-
    # tiering) -- per memory living-light-no-fresh-blood, the still stays
    # entirely wound-free/unmarked (Kling regenerates blood even from a
    # healed-mark still); "same figure as reference" carries the
    # identity, not a visible wound.
    ("s43_under_your_feet", STYLE, "jesus",
     f"EXTREME ground-level crop, camera at floor height looking "
     f"nearly flat across worn stone paving: a crowd of many anonymous "
     f"bare human feet stand together on the stone, ordinary and "
     f"undifferentiated, no faces or bodies visible above the ankle, "
     f"filling most of the frame's width; among them, set slightly "
     f"apart, ONE pair of feet (the same figure as the reference "
     f"image, feet entirely healed and unmarked) stands in identical "
     f"scale and stance to the crowd's feet, not elevated or "
     f"spotlighted, simply present among them. No hands, no upper "
     f"bodies, no lettering. {FULLBLEED}"),
    ("s44_stands_on_one", STYLE, "serpent",
     f"WIDE shot, LOW angle looking UP toward high ground silhouetted "
     f"against bright gold sky-light: a cluster of small distant "
     f"anonymous human figures stand together atop the high ground, "
     f"lit warm gold from behind and above, too small and distant for "
     f"any facial detail; far below at the base of the rise, in cooler "
     f"shadow, {SERPENT.split('.')[0]}'s coiled shape lies flattened "
     f"and subdued beneath the ground-line's own long shadow, still "
     f"and defeated, scaled small relative to the height above it. No "
     f"lettering. {FULLBLEED}"),
    # s45: reuse-checked FIRST against day_of_atonement/stills/
    # s53_the_cross.png per _PREFLIGHT.md's own instruction -- rejected,
    # that candidate is a close frontal devotional portrait on solid
    # black, not isolatable into a distant landscape silhouette. New
    # render needed; this is the cross's FIRST appearance in the story.
    ("s45_eden_to_cross", STYLE, "eden",
     f"VERY WIDE lateral composition, flat low horizon line running "
     f"the full width of the frame: at the LEFT edge, the dense dark "
     f"trees of a garden (the same garden as the reference image); at "
     f"the FAR RIGHT edge, small and distant, the plain silhouette of "
     f"a bare wooden cross standing alone against the sky, rendered as "
     f"a flat dark shape with no figure upon it and no visible detail "
     f"-- pure silhouette only, reading as a distant landmark, not a "
     f"close devotional image. Between the two, a long stretch of open "
     f"horizon and sky fills the middle of the frame. No thread yet "
     f"drawn, no lettering, no other figures. {FULLBLEED}"),
]


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "16:9", "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def resolve_refs(tag):
    refs = []
    for t in tag.split(","):
        t = t.strip()
        if t and REF_MAP.get(t) and REF_MAP[t].exists():
            refs.append(REF_MAP[t])
    return refs


ANCHOR_DEST = {"adam_ref": CAST, "eve_ref": CAST, "eden_ref": WORLD, "serpent_ref": WORLD,
               "desk_ref": WORLD}


def render_set(shots, dest_of, label):
    for name, style, tag, scene in shots:
        out_dir = dest_of(name)
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        refs = resolve_refs(tag)
        prompt = style + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(refs)}) ...", flush=True)
        ok = run(prompt, out, refs)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, refs)
        if ok:
            try:
                cost.record_hf(EPISODE, "long", label, MODEL, note=f"[seed_of_the_woman] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")


def main():
    print("=== anchors ===")
    render_set(ANCHOR_SHOTS, lambda name: ANCHOR_DEST[name], "anchors")
    print("=== spreads ===")
    render_set(SPREAD_SHOTS, lambda name: OUT, "spreads")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
