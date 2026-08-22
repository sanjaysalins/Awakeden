"""SEQ "THE LADDER" — Swirls of Life pilot ep 01, Jacob's dream (Genesis 28:10-17).

FIRST new-content episode through the shared production module (swirls_page.py).
8 pages, 9:16, swirl-only (NO Stain, NO Fray — forcing a diagnosis onto a story
that doesn't need one is worse than none, per SWIRLS_OF_LIFE_SERIES_PLAN.md).
OT episode: swirl CAPPED at Stage 1-2 (Stage 3 is reserved for fulfilment-in-
Christ-on-page; Jesus is never depicted or named visually here — the John 1:51
connection lands in the F08 caption's words only). Narration is LOCKED and
already recorded (narration.md / narration.mp3 in this folder) — every page
traces to it; the words never change.

Swirl arc across the episode (each dose only changes BETWEEN pages, never
within a clip — NORTH_STAR_ANIMATION_PROMPT.md LAW 2):
  F01 flight (Stage 0) -> F02 lying down (Stage 0) -> F03 the ladder (Stage 1,
  one thread woven up the ladder's right rail) -> F04 the presence (Stage 2
  peak, threads + bloom around the light at the top) -> F05 waking (Stage 2
  settling toward 1, pale threads high in the sky) -> F06 dreadful place
  (Stage 1 lingering, one thread above the stone) -> F07 empty field (Stage 1
  residue, one faint thread in the paler band where the ladder stood) ->
  F08 landing (Stage 2 HELD, threads + bloom along the dawn horizon — the
  life now spans the whole sky he must walk toward: "He is that ladder").
Every placement anchors to the thing the narration names in that beat — no
indirect placement that needs prose to explain (the Thomas F01 lesson).

THE THEOPHANY RESTRAINT (F04): Genesis never describes the LORD's form, only
that He "stood above it." The presence is drawn as a broad soft brightness of
pale gold wash the ladder's top dissolves into — explicitly NO figure, NO
face, NO form, stated in the still AND fenced in the clip. The in-world corner
note "NOTE: no face drawn" makes the restraint diegetic. This is a
PRE-INCARNATION theophany, not Jesus: no halo, no Christological iconography.

JACOB — brand-new character, never rendered anywhere in this project.
_JACOB_BUILD below is his locked face/dress build (grounded in Gen 25:27 "a
plain man, dwelling in tents", Gen 27:11 "I am a smooth man", Gen 32:10 "with
my staff I passed over this Jordan"): face/dress ONLY, no motif baked in.
REF-CHAINING (the 2026-08-20 locked rule): F01 renders with NO ref (his
first-ever render establishes him); after F01 passes eyeball QC, a human crops
his full figure -> jacob_ref.png in this folder; F02-F08 all chain it (the
script hard-stops without it). Angels deliberately get NO ref and NO build:
drawn "small and simplified, faces indistinct" on both pages — anonymous
figures like the Hem's crowd, so there is no likeness to drift and no invented
angel iconography to defend.

COST GATE: do NOT run without the user's OK (per /cost). Clean-run estimate:
  8 stills (nano_banana_pro 2k)      8 x ~$0.50 = ~$4.00
  5 veo3_1_lite clips (4s)           5 x ~$0.60 = ~$3.00
  3 kling3_0 pro clips (5s, no snd)  3 x ~$1.31 = ~$3.93
  total ~ $10.93 clean; budget ~$15-20 with a realistic regen buffer.

Run order (one page at a time, eyeball between every step — pilot discipline):
  .venv\\Scripts\\python.exe <this file> --print            # review ALL prompts, $0
  .venv\\Scripts\\python.exe <this file> f01                # still F01 (no ref)
  ... eyeball at 1:1 + F01 referent check ...
  ... CROP Jacob's full figure from the approved F01 -> jacob_ref.png HERE ...
  .venv\\Scripts\\python.exe <this file> f02                # etc., f02..f08
  ... each still passes its referent check BEFORE ...
  .venv\\Scripts\\python.exe <this file> f01 --animate      # etc.

Referent checks (LAW 4 — regen the still, never adapt the clause, on any fail):
  F01: Jacob full figure mid-stride L->R-ish, staff in hand, stone on bare
       ground at lower right fully in frame, dusk washes; ZERO blue anywhere.
       THEN crop jacob_ref.png before touching F02.
  F02: head on the STONE (not the ground), staff beside him, eyes closed;
       night sky grey-black only, ZERO blue anywhere.
  F03: ladder foot ON the earth fully in frame; angels ON the rungs (none
       flying), small, faces indistinct, both directions present; Jacob asleep
       at the foot matching ref; EXACTLY ONE blue thread, woven up the RIGHT
       rail only, even thickness, touching only the rail — never an angel,
       never Jacob; no blue in the sky wash itself.
  F04: NO figure, face, or form in or above the brightness (hard FAIL);
       brightness = pale gold wash the top rungs dissolve into; Stage 2
       threads + one bloom DISTINCT from the brightness, never merged (the
       Gold Exemplar halo/dose-merge lesson); angels few, still, heads bowed;
       Jacob small at the foot.
  F05: Jacob genuinely MID-RISE — propped on one arm, torso lifted, NOT flat
       and NOT fully sitting (the clip completes the rise; a wrong drawn
       endpoint is a LAW 1 blocking contradiction -> regen); eyes wide at the
       sky; 2-3 pale threads high in the sky with clear air around them.
  F06: head caught MID-TURN between sky and ground (same LAW 1 logic as F05);
       one hand flat on the earth; ONE thread in the air above the stone,
       touching nothing; ground reads utterly ordinary.
  F07: field genuinely empty — no invented figures, roads, animals (wide
       canvases invite extra detail: the Hem 16:9 crowd lesson); Jacob small,
       from behind, beside the stone; tall faint paler band high in the sky
       with ONE faint thread inside it.
  F08: sky EMPTY of any ladder or figure (hard FAIL if the model literalizes
       the baked caption "He is that ladder" into a drawn ladder — the
       Golgotha-skull literalism lesson); dose = threads + one bloom along the
       horizon band only; Jacob from behind, staff upright, stance straight.

Clip QC (every clip, no exceptions): 4-frame contact sheet AND real playback.
FAIL if any thread grows, travels, or changes; if any new stain/darkening
appears; if anything materializes inside F04's brightness; if F03's angels
leave the ladder or fly; if a speech bubble appears around any caption; if
Kling pages' completing gestures (F05 rise, F06 head-turn, F08 head-lift) do
NOT visibly complete — an all-static clip is a FAIL too (the Hem F05 lesson).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "test_the_cross"))
from swirls_page import (  # noqa: E402
    PageSpec, Panel, assemble_animation_prompt, assemble_still_prompt,
    render_animation, render_still,
)

JACOB_REF = HERE / "jacob_ref.png"  # human-cropped from the approved F01 render

# Locked build — face/dress only, no motif, reused verbatim on every page
# (F01 bare, F02+ prefixed with "match the attached reference").
_JACOB_BUILD = (
    "a young man with a smooth, unweathered face, quick watchful dark eyes, dark curling hair "
    "falling to his jaw and the first sparse shadow of a young beard, lean and light of build, a "
    "plain traveler's robe of muted olive-green wash over an undyed cream tunic, a rough "
    "ochre-brown mantle across one shoulder, worn leather sandals, drawn in fine, quick "
    "cross-hatching; he wears no blue and no gold anywhere"
)

# NOTE on fences: this is a swirl-only episode, so fence_kind is "none" on
# every page (swirls_page._fence only knows fray/stain). The page-global
# "no new stain, spot, or darkening appears" fence — validated on the Hem —
# is therefore authored into each main_scene_animation's own tail where the
# page's material risk warrants it (night/dawn pages are darkening-prior bait).

PAGES: dict[str, PageSpec] = {

    # ---------------------------------------------------------------- F01
    # The Flight. Swirl absent. veo: continuation walk, no completing gesture.
    "f01": PageSpec(
        seq_title="THE LADDER",
        frame_label="F01",
        panels=(
            Panel("the threat",
                  "a small sketch of a hunter's bow and full quiver hanging from a tent post, "
                  "drawn as quiet still objects"),
            Panel("tents behind",
                  "a small sketch of the low goat-hair tents of home, far off on a bare rise, "
                  "left behind"),
            Panel("the long road",
                  "a small sketch of an empty dirt track winding away over stony hills toward "
                  "Haran"),
        ),
        still_shot_type="WIDE shot",
        anim_shot_desc="wide shot",
        main_scene_still=(
            "open rocky hill country at dusk, the sun already gone and the sky banded in fading "
            "ochre and deep grey-umber washes; Jacob walks alone into the scene from the left, "
            "mid-stride and fully inside the frame, his body heavy with exhaustion, his head low, "
            "one hand gripping a plain wooden traveler's staff, the other holding his mantle "
            "closed at his chest; ahead of him, on the bare ground at the lower right and fully "
            "inside the frame, lies a single rough uncut field stone among sparse dry grass — "
            "the place where he will sleep; no tent, no wall, no shelter of any kind stands "
            "anywhere in the scene, and no other person appears anywhere on the page; the land "
            "around him is wide, stony, and empty to the horizon. Jacob: " + _JACOB_BUILD + ", "
            "his shoulders bowed and his stride worn down to a trudge. Stage 0 dosage: no blue "
            "Swirls of Life ink motif anywhere on this page — no blue ink appears anywhere in "
            "the scene, the panels, or the margins; the page carries only its own black ink and "
            "earth-toned washes."
        ),
        material_closer=(
            "the dusk behaves like layered washes of grey-umber and fading ochre drying into the "
            "paper, never photographic darkness."
        ),
        caption_lines=("the sun was set",),   # Gen 28:11, verbatim contiguous
        corner_note="NOTE: alone at dusk",
        panel_motions=(
            "the light across the sketched bow and quiver shifts gently, nothing else changes",
            "the sketched tent cloths ripple faintly once in an evening wind",
            "a thin drift of dust crosses the sketched track",
        ),
        main_scene_animation=(
            "Jacob continues his slow, weary walk forward along the drawn ground toward the stone "
            "at the lower right, one heavy step after another at the same tired, even pace for "
            "the whole clip, his head staying low, his staff swinging gently with his stride; his "
            "lips stay closed and completely still; the dry grass at the frame's edges stirs "
            "faintly in the evening wind; the dusk light stays exactly as warm and dim as it "
            "already is, unchanged for the whole clip; the stone lies still on the ground; no "
            "blue or gold ink motif appears anywhere on this page, and none appears at any point "
            "in the clip; no new stain, spot, or darkening appears anywhere on the page at any "
            "point."
        ),
        fence_kind="none",
        ref_images=[],          # FIRST-EVER Jacob render — establishes jacob_ref.png
        model_tier="veo3_1_lite",  # continuation of a drawn walk + atmospheric dusk hold;
                                   # nothing has to COMPLETE mid-clip
    ),

    # ---------------------------------------------------------------- F02
    # No Holy Place Required. Swirl absent. veo: sleeping atmospheric hold.
    "f02": PageSpec(
        seq_title="THE LADDER",
        frame_label="F02",
        panels=(
            Panel("no roof",
                  "a small sketch of bare open night sky over a low dark horizon, empty of any "
                  "roof or shelter"),
            Panel("the stone",
                  "a small plain study of the rough uncut field stone alone, drawn as a quiet "
                  "dry object"),
            Panel("his staff",
                  "a small sketch of a plain wooden traveler's staff lying on bare ground, the "
                  "one possession he carries"),
        ),
        still_shot_type="MEDIUM WIDE shot",
        anim_shot_desc="medium wide shot",
        main_scene_still=(
            "night has fallen over the open hill country, the sky laid in deep warm grey-black "
            "ink washes with a scatter of faint pale stars, and no blue anywhere in the sky "
            "itself; Jacob lies on his side on the bare ground in the center of the frame, fully "
            "inside the frame, his body curled under his ochre-brown mantle drawn over him like a "
            "blanket, his head resting on the rough uncut field stone, his eyes closed, his face "
            "slack with exhaustion; his wooden staff lies on the ground alongside him within "
            "reach; sparse dry grass and small stones around him, the land empty to the dark "
            "horizon, no shelter and no other person anywhere on the page. Jacob (match the "
            "attached reference): " + _JACOB_BUILD + ". Stage 0 dosage: no blue Swirls of Life "
            "ink motif anywhere on this page — no blue ink appears anywhere in the scene, the "
            "panels, or the margins; the night sky is grey-black ink only."
        ),
        material_closer=(
            "the night behaves like layered grey-black ink wash settled into the paper's grain, "
            "never solid printed black."
        ),
        caption_lines=("tarried there all night",),   # Gen 28:11, verbatim contiguous
        corner_note="NOTE: stone for pillow",
        panel_motions=(
            "a thin veil of cloud drifts slowly across the sketched night sky",
            "the light across the sketched stone shifts gently, nothing else changes",
            "the light along the sketched staff shifts gently, nothing else changes",
        ),
        main_scene_animation=(
            "Jacob lies completely still in sleep, only his chest rising and falling in a slow, "
            "exhausted rhythm under the mantle; the edge of his mantle stirs faintly once in the "
            "night air and settles; his lips stay closed and completely still; the dry grass "
            "around him sways very gently; the stone stays exactly as drawn beneath his head; the "
            "staff lies still on the ground beside him; the night stays exactly as deep and still "
            "as it already is, unchanged for the whole clip; no blue or gold ink motif appears "
            "anywhere on this page, and none appears at any point in the clip; no new stain, "
            "spot, or darkening appears anywhere on the page at any point."
        ),
        fence_kind="none",
        ref_images=[str(JACOB_REF)],
        model_tier="veo3_1_lite",  # pure atmospheric sleeping hold — veo's validated lane
    ),

    # ---------------------------------------------------------------- F03
    # The Ladder — the hero dream image. Stage 1 woven into the ladder.
    # veo: angels CONTINUE their drawn climb (no completing gesture) — but this
    # is the pilot's highest-risk clip; if it fights veo, switch to kling3_0
    # per the standing switch-models rule before rerolling veo.
    "f03": PageSpec(
        seq_title="THE LADDER",
        frame_label="F03",
        panels=(
            Panel("the dreamer",
                  "a close study of Jacob's sleeping face at rest against the stone, eyes "
                  "closed, drawn calm and still"),
            Panel("first rung",
                  "a small study of the ladder's lowest rung standing on bare dirt, drawn as "
                  "plain weathered wood"),
            Panel("under stars",
                  "a small sketch of deep night sky thick with faint stars over bare hills"),
        ),
        still_shot_type="WIDE shot",
        anim_shot_desc="wide shot",
        main_scene_still=(
            "the dream: the same night country transfigured — from the bare ground beside the "
            "sleeping Jacob, a great ladder of plain weathered wood rises through the whole "
            "height of the scene, its foot set on the earth among the dry grass and fully inside "
            "the frame, its two rails and every rung drawn in confident dark ink, climbing "
            "straight up into the deep night sky until its top passes out of the upper edge of "
            "the page; upon the ladder, angels of God are ascending and descending — six or "
            "seven robed figures in pale cream and ochre wash, drawn small and simplified with "
            "their faces indistinct, some stepping calmly upward and some stepping calmly "
            "downward, each one standing on the ladder itself and none of them flying; Jacob lies "
            "asleep at the ladder's foot at the lower left, small and fully inside the frame, "
            "curled under his mantle with his head on the stone, exactly as he lay; the night sky "
            "is laid in deep warm grey-black ink washes with faint pale stars, and no blue "
            "anywhere in the sky itself. Jacob (match the attached reference): " + _JACOB_BUILD +
            ". Stage 1 dosage: exactly one restrained thread of blue ink, with the faintest "
            "trace of muted gold, rising from the ground at the ladder's foot and winding slowly "
            "up alongside the ladder's right rail, woven with the rail's own line the whole way "
            "to the top of the page, drawn as one smooth unbroken calligraphic line of even "
            "thickness, touching only the wooden rail, touching no angel and never touching "
            "Jacob, the only blue on the whole page, behaving like a single line of wet ink bled "
            "upward into the paper."
        ),
        material_closer=(
            "the night sky behaves like deep grey-black ink wash with no blue in it, so the "
            "ladder's single blue thread reads as the only living ink on the page."
        ),
        caption_lines=("reached to heaven",),   # Gen 28:12, verbatim contiguous
        corner_note="NOTE: first thread",
        panel_motions=(
            # face panel -> tone-only (small sketched faces morph under content asks)
            "the light across the sleeping face softens very slightly, nothing else changes",
            "the light across the sketched rung shifts gently, nothing else changes",
            "a thin veil of cloud drifts slowly across the sketched stars",
        ),
        main_scene_animation=(
            "the angels continue the motion they are drawn in, the ascending figures climbing "
            "slowly and calmly upward and the descending figures stepping slowly and calmly "
            "downward, each one staying on the ladder itself for the whole clip, their robes "
            "swaying gently with their steps; the ladder stays exactly as drawn, every rail and "
            "rung in place; Jacob lies completely still at the ladder's foot, only his chest "
            "rising and falling slowly in sleep; the single thin blue ink thread woven up the "
            "ladder's right rail stays exactly as drawn, in place, for the whole clip; the night "
            "sky and stars stay exactly as they are; no new figure or mark appears anywhere on "
            "the page at any point."
        ),
        fence_kind="none",
        ref_images=[str(JACOB_REF)],
        model_tier="veo3_1_lite",  # continues a drawn, already-in-progress climb; no gesture
                                   # must complete — veo's exact lane (and half Kling's cost)
    ),

    # ---------------------------------------------------------------- F04
    # "I Am With Thee" — the peak. Stage 2 around the presence-light.
    # DELIBERATE near-hold page: the world holds its breath while the LORD
    # speaks. The living motion budget = dose drift + Jacob's breath + angel
    # robes. If it reads lifeless on watch, add angel micro-motion — NEVER
    # light motion (theophany integrity + veo glitter risk).
    "f04": PageSpec(
        seq_title="THE LADDER",
        frame_label="F04",
        panels=(
            Panel("this land",
                  "a small sketch of the wide sweep of bare hills and open land under the "
                  "night, the land itself the promise"),
            Panel("as the dust",
                  "a close study of a handful of fine dust spread wide across bare ground, "
                  "countless grains"),
            Panel("whither thou goest",
                  "a small study of a pair of worn leather sandals set side by side on bare "
                  "ground"),
        ),
        still_shot_type="WIDE shot",
        anim_shot_desc="wide shot",
        main_scene_still=(
            "the dream at its height: the great wooden ladder still rises through the whole "
            "height of the scene from the dry ground to the top of the page, and at its top, "
            "filling the upper reach of the sky and fully inside the frame, a broad soft "
            "brightness of pale gold watercolor wash opens in the night — the ladder's highest "
            "rungs entering it and dissolving from sight within it; the brightness has no edge "
            "line, only wash fading into wash; no figure, no face, and no human form appears "
            "within the brightness or anywhere above it — the LORD's presence is shown only as "
            "light held in the paper, never as a person; two or three angels remain on the lower "
            "half of the ladder, drawn small and simplified with faces indistinct, standing "
            "still upon the rungs with heads bowed toward the light; Jacob lies asleep far below "
            "at the ladder's foot, small at the bottom of the frame and fully inside it, curled "
            "under his mantle with his head on the stone; the night sky around the brightness "
            "stays deep warm grey-black ink wash with faint stars, no blue anywhere in the sky "
            "itself. Jacob (match the attached reference): " + _JACOB_BUILD + ". Stage 2 "
            "dosage: the blue ink motif is quietly present — a few soft threads of blue ink and "
            "one small watercolor bloom, with traces of muted gold, curling in the dark air "
            "close around the brightness at the top of the ladder, tied to no figure and "
            "touching nothing solid, distinct from the pale gold brightness itself and never "
            "merging with it, behaving like wet ink bled into the paper's night sky, quiet and "
            "restrained; the brightness is the scene's own light and is separate from the Swirls "
            "of Life dose."
        ),
        material_closer=(
            "the brightness at the ladder's top behaves like clean paper showing through thinned "
            "pale gold wash — light left in the page, never light added over it."
        ),
        caption_lines=("I am with thee",),   # Gen 28:15, verbatim contiguous — God's line,
                                             # spoken by the "god" voice in the narration
        corner_note="NOTE: no face drawn",   # the restraint, made diegetic
        panel_motions=(
            "the sketched grass on the far hills bows faintly in a passing wind",
            "the light across the sketched dust shifts gently, nothing else changes",
            "the light across the sketched sandals shifts gently, nothing else changes",
        ),
        main_scene_animation=(
            "the broad pale brightness at the top of the ladder stays exactly as warm and steady "
            "as it already is, unchanged for the whole clip, and nothing appears within it at "
            "any point; the angels on the lower rungs hold completely still, heads bowed, only "
            "their robes stirring faintly; the ladder stays exactly as drawn, every rail and "
            "rung in place; Jacob lies completely still far below, only his chest rising and "
            "falling slowly in sleep, his lips closed and completely still; the few soft blue "
            "threads and the small bloom around the brightness drift gently within their own "
            "small area, their traces of muted gold slowly warming and settling; the stars hold "
            "steady; no new figure, face, or mark appears anywhere on the page at any point."
        ),
        fence_kind="none",
        ref_images=[str(JACOB_REF)],
        model_tier="veo3_1_lite",  # atmospheric peak hold, validated drift clause only; the
                                   # light language is veo-safe positive-only ("stays exactly
                                   # as warm and steady"), no glint/sparkle words
    ),

    # ---------------------------------------------------------------- F05
    # Waking Afraid. Stage 2 settling toward 1. KLING: the rise must COMPLETE.
    # LAW 0 pairing: the still draws him MID-rise so the clip only continues
    # the drawing to its endpoint (sitting upright) — never a cold start.
    "f05": PageSpec(
        seq_title="THE LADDER",
        frame_label="F05",
        panels=(
            Panel("only sky",
                  "a small sketch of the bare pre-dawn sky over dark hills, first thin light at "
                  "the rim, nothing in it"),
            Panel("wide awake",
                  "a close study of Jacob's face, eyes wide open and startled, drawn with "
                  "quick urgent strokes"),
            Panel("same stone",
                  "a small plain study of the rough field stone in first light, exactly as it "
                  "was"),
        ),
        still_shot_type="MEDIUM shot",
        anim_shot_desc="medium shot",
        main_scene_still=(
            "first grey light before dawn over the open field, the sky paling from deep "
            "grey-black to cold grey-ochre at the horizon; Jacob is caught mid-startle, his "
            "body still mostly low to the ground and fully inside the frame — his legs still "
            "flat and trailing on the earth behind him exactly as he slept, only his upper body "
            "has begun to rise, his weight braced on one straight, locked arm with his open palm "
            "flat on the bare ground beside him taking his full weight, his torso lifted at a "
            "steep diagonal angle low over the ground, nowhere near upright yet, his shoulders "
            "still well below head-height off the ground; his other hand clutches the mantle "
            "sliding from his shoulder, his eyes wide open and staring upward at the empty sky, "
            "his mouth closed, his hair disordered from sleep; beneath him, fully inside the "
            "frame beside his supporting arm, the rough field stone where his head lay a moment "
            "ago; his staff lies on the ground nearby; the sky above him is empty and ordinary, "
            "pale wash and fading stars, with plenty of open air above his head inside the "
            "frame. Jacob (match the attached reference): " + _JACOB_BUILD + ". Fading dosage, "
            "Stage 2 settling toward Stage 1: only two or three small, closed, curled flourishes "
            "of blue ink remain, thinner and paler than in the dream, with the last trace of "
            "muted gold, each one short and self-contained like a single calligraphic curl, "
            "floating with open clear sky on every side of each one, well clear of the frame's "
            "top edge and not touching it, tied to no figure and touching nothing solid, the "
            "quiet remainder of the dream's ink; they do not fall, drip, run, or trail downward "
            "in any direction — each curl is closed and complete in itself, static and "
            "suspended, behaving like dry ink already set into the paper, never a wet streak."
        ),
        material_closer=(
            "the first light behaves like thin cold ochre wash creeping into the night's grey "
            "ink, never a sunbeam."
        ),
        caption_lines=("Jacob awaked",),   # Gen 28:16, verbatim contiguous
        corner_note="NOTE: dawn begins",
        panel_motions=(
            "the thin light at the rim of the sketched hills warms very slightly, nothing else "
            "changes",
            # full-arc blink, Kling's validated completing-gesture lane
            "his sketched eyes close once, then open again fully, ending wide open",
            "the light across the sketched stone shifts gently, nothing else changes",
        ),
        main_scene_animation=(
            "Jacob pushes the rest of the way up from his low, braced arm to sitting fully "
            "upright, his legs drawing in beneath him as his torso rises, one continuous motion "
            "that completes early in the clip and then holds, his wide eyes staying fixed on the "
            "sky above, his chest heaving with quick breaths that slowly steady; his mantle "
            "slips further from his shoulder and settles; his lips stay closed and completely "
            "still — he is not speaking and his mouth does not move at all; the two or three "
            "small closed curls of pale blue ink high in the sky stay exactly as drawn, in "
            "place, for the whole clip, never lengthening, spreading, or trailing downward; the "
            "stone lies still on the ground; the staff lies still; no new stain, spot, or "
            "darkening appears anywhere on the page at any point."
        ),
        fence_kind="none",
        ref_images=[str(JACOB_REF)],
        model_tier="kling3_0",  # the startle-rise (propped arm -> sitting) must visibly
                                # COMPLETE mid-clip — Kling's lane; caption is 1 line so the
                                # bubble bug's known 2-line trigger is avoided
    ),

    # ---------------------------------------------------------------- F06
    # "How Dreadful Is This Place". Stage 1 lingering. KLING: the head-turn
    # must COMPLETE. Still drawn mid-turn (LAW 0/LAW 1 pairing, as F05).
    # NO_MOUTH on Jacob — the baked caption is his own spoken line.
    "f06": PageSpec(
        seq_title="THE LADDER",
        frame_label="F06",
        panels=(
            Panel("he was afraid",
                  "a close study of Jacob's two hands pressed flat against the bare ground, "
                  "fingers spread"),
            Panel("house of God",
                  "a small sketch of the open empty field itself under early light, bare and "
                  "ordinary"),
            Panel("gate of heaven",
                  "a small sketch of the thin bright band of dawn where the dark hills meet "
                  "the sky"),
        ),
        still_shot_type="MEDIUM WIDE shot",
        anim_shot_desc="medium wide shot",
        main_scene_still=(
            "early dawn light, cold and clear, across the open field; Jacob sits upright on the "
            "ground in the center of the frame, fully inside it, his mantle pooled around his "
            "waist, his head caught partway through a downward turn — his chin still clearly "
            "raised above where it will finally come to rest, his face angled roughly midway "
            "between the empty sky above and the bare ground ahead, neither one nor the other, "
            "his wide eyes only beginning to find the ordinary earth, not yet settled on it, "
            "awe and fear together in his face, his mouth closed; "
            "one hand is pressed flat against the earth beside him, fully inside the frame; "
            "around him the ground is only dirt, sparse dry grass, and small stones, utterly "
            "ordinary, stretching away to the hills; the rough field stone sits beside him, "
            "fully inside the frame; his staff lies on the ground nearby; the sky holds thin "
            "early light, its stars nearly gone. Jacob (match the attached reference): "
            + _JACOB_BUILD + ". Stage 1 dosage, lingering: exactly one restrained thread of "
            "blue ink, with the faintest trace of muted gold, short and small, curling in the "
            "still air well above the field stone, its lowest point clearly separated from the "
            "stone's own surface by a wide, plainly visible gap of open sky at least as tall as "
            "the stone itself, its highest point rising no higher than Jacob's own head-height, "
            "tied to no figure and touching nothing at any point along its length — not the "
            "stone, not Jacob, not the ground — one smooth calligraphic line floating alone in "
            "open air, the last of the dream still present in the waking scene, behaving like a "
            "line of wet ink bled into the paper's morning air."
        ),
        material_closer=(
            "the morning light across the ordinary ground behaves like plain warm washes drying "
            "unevenly in the paper's grain."
        ),
        caption_lines=("I knew it not",),   # Gen 28:16, verbatim contiguous — Jacob's line,
                                            # chosen over splitting "How dreadful is this
                                            # place" across 2 lines (Kling bubble-bug lesson)
        corner_note="NOTE: ordinary ground",
        panel_motions=(
            "the sketched fingers press a fraction flatter against the ground, then hold",
            "the sketched grass across the little field bows faintly in a passing breath of "
            "wind",
            "the thin bright band at the sketched horizon warms very slightly, nothing else "
            "changes",
        ),
        main_scene_animation=(
            "Jacob continues the turn of his head downward until his gaze rests on the bare "
            "ground just in front of him, the turn completing and then holding, his eyes wide "
            "with awe, his shoulders rising and falling with his breath; his hand presses a "
            "fraction flatter against the earth and stays there; his lips stay closed and "
            "completely still — he is not speaking and his mouth does not move at all; the "
            "single thin blue ink thread in the air above the stone stays exactly as drawn, in "
            "place, for the whole clip; the stone sits still beside him; the staff lies still; "
            "the dawn light stays exactly as it already is; no new stain, spot, or darkening "
            "appears anywhere on the page at any point."
        ),
        fence_kind="none",
        ref_images=[str(JACOB_REF)],
        model_tier="kling3_0",  # the sky-to-ground head-turn must visibly COMPLETE mid-clip,
                                # plus the palm-press micro-gesture — Kling's lane
    ),

    # ---------------------------------------------------------------- F07
    # Still Alone? No. — the direct-address beat. Stage 1 residue.
    # veo: wide atmospheric hold. Deliberately near-empty: the field IS the
    # viewer's field. Caption "You are not" completes against the narration
    # ("certain you are alone. You are not.") and the corner note answers it
    # on the page itself.
    "f07": PageSpec(
        seq_title="THE LADDER",
        frame_label="F07",
        panels=(
            Panel("first light",
                  "a close study of bent grass blades heavy with dew in the early light"),
            Panel("the last star",
                  "a small sketch of one faint star alone in the paling sky"),
            Panel("morning birds",
                  "a small sketch of two small birds crossing the dawn sky together"),
        ),
        still_shot_type="WIDE shot",
        anim_shot_desc="wide shot",
        main_scene_still=(
            "a wide, quiet dawn over the whole field, seen from a distance: the open country "
            "stretching away to low hills, laid in broad half-dry washes of ochre and olive with "
            "wide bare paper showing between them; Jacob sits small in the middle distance "
            "beside the field stone, seen from behind, fully inside the frame, his back to us, "
            "still and unmoving, facing the paling horizon; around him the field is empty in "
            "every direction — no tent, no road, no wall, no other person and no animal "
            "anywhere in the scene; well below the sky's upper edge, at roughly the same height "
            "as the distant hilltops, where the ladder stood in the dream, a modest oval patch "
            "of paler air remains, barely lighter than the sky around it, plain thinned wash "
            "with no blue and no gold of its own, its edges well clear of the frame's top border "
            "on every side, fully inside the frame. Jacob (match the attached reference): "
            + _JACOB_BUILD + ", small at this distance, his figure simple and quiet. Stage 1 "
            "residue dosage: one small, closed, self-contained curl of blue ink, paler than on "
            "any other page, with the barest trace of muted gold, short and compact like a "
            "single calligraphic flourish no larger than a hand's width, floating inside that "
            "paler patch with open clear air around every side of it, tied to no figure and "
            "touching nothing; it does not fall, drip, run, or trail in any direction — it is a "
            "closed loop complete in itself, static and dry, the last visible remainder of the "
            "dream's ink, behaving like ink already set into the paper, never a wet streak."
        ),
        material_closer=(
            "the wide field behaves like broad, quiet, half-dry washes of ochre and olive, wide "
            "stretches of bare paper left open between them."
        ),
        caption_lines=("You are not",),   # narration verbatim contiguous ("certain you are
                                          # alone. You are not.") — the direct-address landing
        corner_note="NOTE: not alone",
        panel_motions=(
            "one drop of dew slips slowly down a sketched grass blade",
            "the light in the sketched sky shifts gently, nothing else changes",
            "the two sketched birds glide slowly onward across the panel",
        ),
        main_scene_animation=(
            "the wide field lies quiet; the grass across the field bows and rises faintly in a "
            "slow dawn wind; Jacob, small in the middle distance, sits completely still beside "
            "the stone, his back to us, unmoving for the whole clip; the modest paler patch in "
            "the sky stays exactly as drawn; the single closed curl of blue ink inside it stays "
            "exactly as drawn, in place, for the whole clip, never lengthening or trailing "
            "downward; the dawn light stays exactly "
            "as soft and even as it already is, unchanged; no new figure or mark appears "
            "anywhere on the page at any point."
        ),
        fence_kind="none",
        ref_images=[str(JACOB_REF)],
        model_tier="veo3_1_lite",  # pure wide atmospheric hold, nothing completes — veo lane
    ),

    # ---------------------------------------------------------------- F08
    # The True Ladder — the landing. Stage 2 HELD along the dawn horizon:
    # the life now spans the whole sky ahead of him ("He is that ladder,
    # standing open"). Jesus carried in the caption's words only — the page
    # stays inside its own OT moment. KLING: the head-lift must COMPLETE.
    "f08": PageSpec(
        seq_title="THE LADDER",
        frame_label="F08",
        panels=(
            Panel("on the earth",
                  "a small study of a wooden ladder's lowest rung standing on bare dirt, drawn "
                  "plain and solid"),
            Panel("heaven open",
                  "a small sketch of the dawn sky parting above the hills, pale light widening "
                  "between soft clouds"),
            Panel("on his journey",
                  "a small sketch of the open track leading away over the hills into the "
                  "morning light"),
        ),
        still_shot_type="WIDE shot",
        anim_shot_desc="wide shot",
        main_scene_still=(
            "full dawn: the whole horizon alight, soft gold wash bled evenly along the meeting "
            "of sky and hills and diffusing high into the paling sky, the field warm with "
            "morning; Jacob stands in the lower third of the frame, seen from behind and fully "
            "inside the frame, facing the dawn horizon, his mantle settled across both "
            "shoulders, his staff upright in his hand with its foot on the ground, his stance "
            "no longer bowed but straight, ready; beside him on the ground, fully inside the "
            "frame, the rough field stone; the sky is open and empty of any ladder, any figure, "
            "and any form — only light; the land ahead of him runs open toward the horizon. "
            "Jacob (match the attached reference): " + _JACOB_BUILD + ", his cross-hatching "
            "laid calmer and more even now than on any earlier page. Stage 2 dosage, held: a "
            "few soft threads of blue ink and one small watercolor bloom, with traces of muted "
            "gold, woven loosely along the band of dawn light where the sky meets the hills, "
            "stretched easy and unhurried across the horizon ahead of him, tied to no figure, "
            "touching neither Jacob nor the ground nor the stone, behaving like wet ink bled "
            "into the paper's morning light, quiet, present, and staying."
        ),
        material_closer=(
            "the full dawn behaves like soft gold wash bled evenly into the paper along the "
            "horizon — warm ink in paper, never radiance in air."
        ),
        caption_lines=("He is that ladder",),   # narration verbatim contiguous ("Jesus said He
                                                # is that ladder") — the landing line; John
                                                # 1:51 carried in words, never as a scene
        corner_note="NOTE: standing open",
        panel_motions=(
            "the light across the sketched rung shifts gently, nothing else changes",
            "the pale light between the sketched clouds slowly warms and settles",
            "a thin drift of dust crosses the sketched track",   # deliberate F01 bookend echo
        ),
        main_scene_animation=(
            "Jacob slowly lifts his head toward the dawn light, the small motion completing and "
            "then holding, his shoulders easing down and settling as one long breath leaves "
            "him; his mantle and the hem of his robe stir gently in the morning wind; his staff "
            "stays upright and still in his hand; the soft blue threads and the small bloom "
            "along the horizon's band of light drift gently within their own fixed band, their "
            "traces of muted gold glinting softly and settling; the stone sits still beside "
            "him; the dawn sky stays exactly as drawn, with nothing new appearing in it at any "
            "point; no new figure or mark appears anywhere on the page at any point."
        ),
        fence_kind="none",
        ref_images=[str(JACOB_REF)],
        model_tier="kling3_0",  # the head-lift + shoulder-release must visibly COMPLETE (the
                                # landing's one human turn, the Hem F05-v2 fix family); "glint
                                # softly and settle" is Kling-legal wording
    ),
}


def _out_paths(page_id: str) -> tuple[Path, Path]:
    return (HERE / f"the_ladder_{page_id}_9x16.png",
            HERE / f"the_ladder_{page_id}_9x16.mp4")


def main() -> int:
    args = [a for a in sys.argv[1:]]
    if "--print" in args:
        wanted = [a for a in args if a in PAGES] or list(PAGES)
        for pid in wanted:
            spec = PAGES[pid]
            print(f"\n{'=' * 78}\n{spec.frame_label}  [{spec.model_tier}]  "
                  f"caption: {spec.caption_lines}\n{'-' * 78}")
            print("STILL:\n" + assemble_still_prompt(spec))
            print("\nANIMATION:\n" + assemble_animation_prompt(spec))
        return 0

    page_ids = [a for a in args if a in PAGES]
    if len(page_ids) != 1:
        print("usage: render_jacobs_ladder.py <f01..f08> [--animate] | --print [fNN]")
        print("       one page per invocation, eyeball QC between every step (pilot law).")
        return 2
    pid = page_ids[0]
    spec = PAGES[pid]
    png, mp4 = _out_paths(pid)

    if pid != "f01" and not JACOB_REF.exists():
        print(f"  FAILED: {JACOB_REF.name} missing — crop Jacob's full figure from the "
              f"approved F01 render and save it there first (ref-chaining rule: a recurring "
              f"subject with no chained ref is a hard stop).")
        return 1

    if "--animate" in args:
        if not png.exists():
            print(f"  FAILED: still {png.name} not rendered/approved yet.")
            return 1
        return 0 if render_animation(spec, png, mp4) else 1
    return 0 if render_still(spec, png) else 1


if __name__ == "__main__":
    sys.exit(main())
