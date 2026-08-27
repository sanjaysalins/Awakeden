"""Episode spec for The Ashes That Made Clean's REBUILD -- the first real
episode built through the fixed swirls-of-life pipeline (mirrors how Jacob's
Ladder was "the first episode through swirls_page.py"). Fixes all 3
user-caught defects from the original build:

1. Covers: front-cover lighting re-authored (Fable, 2026-08-23) to restore
   the warm/cool cinematic contrast the original lost ("no vivid color
   anywhere" -> a single shaft of amber ember-light against ash-grey/cold-
   blue shadow -- the warmth reads as the ashes' own color, not decoration).
   Back cover's content is unchanged (it was never defective in TEXT -- the
   border was a pure render hallucination the new V2 image audit now checks
   for automatically).
2. Interior pages: panel_style="woodcut_hybrid" on all 4 pages (the
   previously-disconnected validated template, now wired in for real).
3. Freeze-hold budget: F01 and F04 (the two freeze pages) get clip_duration
   raised per swirls_verify.sw_f1_freeze_budget's own computed fix
   suggestions (F01 -> 6s veo3_1_lite, F04 -> 7s kling3_0) -- verify with
   `swirls_episode.py <this dir> plan` before spending on the real
   animate step.

Content for pages is SLICED from render_ashes.py (imported, not retyped) --
only panel_style/clip_duration are overridden via dataclasses.replace(). New
cover content is authored fresh (the front cover's old prompt was the actual
defect; there is nothing valid to slice from render_ashes_covers.py for the
front cover's lighting).
"""
from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "test_the_cross"))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from swirls_page import Ref  # noqa: E402
from swirls_cover import CoverSpec  # noqa: E402
from swirls_assemble import DuckProfile, EpisodeManifest, ScoreVariant, Unit  # noqa: E402
import render_ashes  # noqa: E402 -- the real, already-validated page content

REFS_DIR = HERE / "refs"

# ---- swirl-dosage build-up, 2026-08-23 (Fable-designed) -- user watched the
# rebuilt episode and said "I just feel the swirls that make up this unique
# series was missing in the middle pages." Checked: F01-F03 were all Stage 0
# (zero blue ink anywhere), only F04 carried any swirl at all (Stage 1, one
# thread). User's chosen direction: F01-F03 each get a faint Stage 1 trace
# anchored to a different in-scene object (never touching either man's
# ash-marked skin -- the series' locked "Stain and Swirl never touch" rule);
# F04 upgrades to Stage 2 (this episode's own documented ceiling). F03's
# thread is deliberately anchored to the SAME water vessel that carries F04's
# fuller payoff, so the escalation visually rhymes across the two pages.
_DOSAGE_REPLACEMENTS = {
    "f01": (
        "Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page — "
        "no blue ink appears anywhere in the scene, the panels, or the margins.",
        "Stage 1 dosage: exactly one restrained thread of blue ink rising out of "
        "the cedar fire with the grey smoke, one thin line climbing inside the "
        "smoke column, touching only the smoke, touching neither the priest nor "
        "his ash-marked hands, the only blue on the whole page, behaving like a "
        "single line of wet ink bled into the paper — never a glow, never a spark.",
    ),
    "f02": (
        "Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page — "
        "no blue ink appears anywhere in the scene, the panels, or the margins.",
        "Stage 1 dosage: exactly one restrained thread of blue ink rising thin "
        "from among the low tents of the camp far off across the open ground, "
        "small with the distance, touching only the tents at the horizon, "
        "touching the man nowhere, the only blue on the whole page, behaving "
        "like a single line of wet ink bled into the paper.",
    ),
    "f03": (
        "Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page — "
        "no blue ink appears anywhere in the scene, the panels, or the margins.",
        # Reworded 2026-08-23 (Fable-designed, tested against 2 rejected alternates)
        # after the user flagged "sometimes the swirl looks like thread" -- the
        # original "thread... curling... winding down its side" rendered as a
        # literal wound cord/bracelet. "rising from the mouth" (variant A) let it
        # detach and float off the vessel; "spill/bleeds/feathering" (variant B)
        # read as the vessel literally leaking liquid onto the ground. This
        # version ("brushstroke... drawn once down the neck... against the
        # vessel's own drawn outline") rendered clean on the first real test: a
        # flat painted band on the pottery's own surface, contained, no drift,
        # no drip. See NORTH_STAR_PROMPT.md's Stage 1 template -- this episode's
        # own local proof that "thread" is the risky word before touching the
        # locked series-wide wording.
        "Stage 1 dosage: exactly one restrained brushstroke of blue ink drawn once down the neck of "
        "the plain clay water vessel sitting untouched on the ground some distance off, a single thin "
        "flat stroke lying flat in the surface of the paper against the vessel's own drawn outline, "
        "overlapping only the vessel, crossing the man nowhere, the only blue on the whole page, "
        "behaving like one stroke of wet ink bled flat into the paper — no thickness, no cast shadow, "
        "never dripping, never pooling on the ground.",
    ),
    "f04": (
        "Stage 1 dosage: exactly one restrained thread of blue ink, with the "
        "faintest trace of muted gold, winding once around the plain clay "
        "vessel of water the priest holds in his other hand, touching only the "
        "vessel, touching neither man, the only blue on the whole page, "
        "behaving like a single line of wet ink bled into the paper.",
        "Stage 2 dosage: the blue ink motif is quietly present — a few soft "
        "blue threads, with the faintest trace of muted gold, winding around "
        "the plain clay vessel of water the priest holds in his other hand and "
        "running along the upper stem of the dripping hyssop branch, clear of "
        "the priest's grip and clear of the falling water, and one small "
        "watercolor bloom spreading from the vessel's shoulder into the paper "
        "around it, touching only the vessel and the branch, touching neither "
        "man and never the grey ash, the only blue on the whole page, every "
        "thread behaving like wet ink bled into the paper.",
    ),
}

_MATERIAL_CLOSER_REPLACEMENTS = {
    "f04": (
        "the single blue thread on the vessel is the only ink that behaves "
        "like living ink on this page.",
        "the blue threads and small bloom on the vessel and hyssop branch are "
        "the only ink that behaves like living ink on this page.",
    ),
}

# FIXED 2026-08-23: the still-prompt dosage upgrade above was NOT enough on its own --
# the animation prompts never told the model the new thread should stay put, and a
# real render confirmed the exact documented risk (memory
# feedback_ink_motif_animation_unsafe): F01's smoke-thread, clearly visible in the
# still, had vanished by 1.2s into the clip. Every page with a new/changed swirl
# element needs its own explicit "stays exactly as drawn... never fading" clause in
# main_scene_animation, matching the pattern F04 already had for its original
# single-thread version (now updated for the upgraded multi-thread version).
_ANIMATION_REPLACEMENTS = {
    "f01": (
        "never spreading, never changing shape; his robe stirs faintly in the wind;",
        "never spreading, never changing shape; the thin blue ink thread rising in "
        "the smoke stays exactly as drawn, in place, for the whole clip, never "
        "spreading, never changing shape, never fading; his robe stirs faintly in "
        "the wind;",
    ),
    "f02": (
        "never spreading, never changing shape; the dry grass around him sways "
        "very gently;",
        "never spreading, never changing shape; the thin blue ink thread rising "
        "from the distant tents stays exactly as drawn, in place, for the whole "
        "clip, never spreading, never changing shape, never fading; the dry grass "
        "around him sways very gently;",
    ),
    "f03": (
        "the untouched water vessel sits still, exactly as drawn, well apart from "
        "him;",
        "the untouched water vessel sits still, exactly as drawn, well apart from "
        "him, the flat blue brushstroke on its neck staying exactly as drawn, in "
        "place, for the whole clip, never spreading, never changing shape, never "
        "fading, never dripping;",
    ),
    "f04": (
        "the single thin blue ink thread on the vessel stays exactly as drawn, "
        "in place, for the whole clip;",
        "the blue ink threads and small bloom on the vessel and hyssop branch "
        "stay exactly as drawn, in place, for the whole clip, never spreading, "
        "never changing shape, never fading;",
    ),
}


def _apply_swirl_upgrade(pid: str, page):
    old_dose, new_dose = _DOSAGE_REPLACEMENTS[pid]
    assert old_dose in page.main_scene_still, f"{pid}: expected dosage text not found -- render_ashes.py changed?"
    new_scene = page.main_scene_still.replace(old_dose, new_dose)
    new_closer = page.material_closer
    if pid in _MATERIAL_CLOSER_REPLACEMENTS:
        old_c, new_c = _MATERIAL_CLOSER_REPLACEMENTS[pid]
        assert old_c in new_closer, f"{pid}: expected material_closer text not found"
        new_closer = new_closer.replace(old_c, new_c)
    old_a, new_a = _ANIMATION_REPLACEMENTS[pid]
    assert old_a in page.main_scene_animation, f"{pid}: expected animation text not found"
    new_anim = page.main_scene_animation.replace(old_a, new_a)
    return dataclasses.replace(page, main_scene_still=new_scene, material_closer=new_closer,
                                main_scene_animation=new_anim)


# ---- interior pages: panel_style="woodcut_hybrid" for all 4; clip_duration
# raised only on the 2 freeze pages, per SW-F1's own computed fix suggestion
# (confirmed via `swirls_episode.py <dir> plan` before any spend); swirl dosage
# upgraded per the design above.
PAGES = {
    pid: _apply_swirl_upgrade(pid, dataclasses.replace(
        page,
        panel_style="woodcut_hybrid",
        clip_duration={"f01": 6, "f04": 7}.get(pid),  # None (unchanged) for f02/f03 (boomerang)
    ))
    for pid, page in render_ashes.PAGES.items()
}

# ---- covers -------------------------------------------------------------

_R_HAND = Ref(
    "the reaching/marked hand's build and skin tone, matching the unclean man's own hand",
    str(REFS_DIR / "unclean_man_ref.png"),
)

FRONT_COVER = CoverSpec(
    side="front",
    scene=(
        "A man's hand reaching down toward a still, fallen human form half-lost in dry grass "
        "at the edge of a bare field — the body itself left indistinct, unglamorized, no "
        "visible wound or gore, just a still shape and a reaching hand meeting it."
    ),
    # Fable-authored, 2026-08-23 -- replaces the original's all-cold lighting ("no vivid
    # color anywhere") that killed the cover's warm/cool contrast. The warmth is the ashes'
    # own color (amber ember-light), not decoration; the grey still dominates the frame.
    lighting=(
        "Vast, wind-scoured wilderness under a heavy ash-grey overcast, the cloud bank split "
        "by a single narrow seam where one low shaft of deep amber ember-light breaks through "
        "behind the reaching hand. Cinematic atmospheric haze, cold blue-grey and ash-toned "
        "shadow holding everything the shaft does not touch, dramatic volumetric light kept "
        "narrow and low against the grey, photographic tonality."
    ),
    title="THE ASHES THAT MADE CLEAN",
    subtitle="NUMBERS 19",
    title_position="top",
    animation=(
        "The reaching hand and the still form beneath it stay exactly as drawn, in place, "
        "for the whole clip — no new motion in the hand or the body; the dry grass around "
        "them sways very gently in a passing wind; the narrow shaft of amber light stays "
        "exactly as steady as it already is, unchanged for the whole clip"
    ),
    extra_avoid="visible wounds, blood, gore",
    refs=[_R_HAND],
)

BACK_COVER = CoverSpec(
    side="back",
    scene=(
        "A serene, dignified hand — its wrist and sleeve the only part of the figure "
        "visible, unhurried and warm-lit — reaching to rest gently on another hand marked "
        "with a faint grey ash smudge, held open at the edge of the frame; where the two "
        "hands meet, the grey mark begins to lift and lighten, without any wound or graphic "
        "detail."
    ),
    lighting=(
        "Vast wind-scoured wilderness under an open sky breaking from grey into warm gold, "
        "cinematic atmospheric haze, dramatic volumetric light rays widening behind the two "
        "hands, photographic tonality."
    ),
    background_detail=(
        # Strengthened 2026-08-23 after a first render let the thread trail down past the
        # hands toward the frame edge -- this style's ink motif has a documented tendency to
        # over-escalate past a soft cap (NORTH_STAR_PROMPT.md's animation-lessons section);
        # this uses the harder, explicit-size-limit phrasing that has actually worked before.
        "A single short thread of luminous blue-gold ink lies directly against the serene "
        "hand's own wrist and knuckles ONLY, its whole visible length no longer than that "
        "hand's own width, curled into one small closed loop that stays touching the skin at "
        "every point — it never straightens, never trails down the arm or sleeve, never "
        "extends toward the ground, the other hand, or any edge of the frame, behaving like a "
        "small dab of living ink on paper, never a glow or halo."
    ),
    title="READY TO BE MADE CLEAN?",
    subtitle="HEBREWS 9:14",
    title_position="bottom",
    animation=(
        "The two hands stay exactly as drawn, in the same position, for the whole clip — no "
        "new motion, no further closing of the gap between them; the single restrained "
        "blue-gold thread on the wrist stays exactly as drawn, in place, for the whole clip, "
        "never spreading, never changing shape; the sleeve stirs very faintly in a passing "
        "wind; the volumetric light rays behind them stay exactly as steady as they already "
        "are, unchanged for the whole clip"
    ),
    extra_avoid="visible wounds, blood, gore",
    refs=[_R_HAND],
)

COVERS = {"front": FRONT_COVER, "back": BACK_COVER}

# ---- assembly manifest ---------------------------------------------------
# Word counts/modes unchanged from the shipped assemble_ashes.py -- only the
# interior template and cover lighting change, not the timing/edit structure.

MANIFEST = EpisodeManifest(
    episode_dir=HERE,
    narration=HERE / "narration.mp3",
    # Paths corrected 2026-08-23 to match what swirls_episode.py's cmd_still/cmd_animate
    # ACTUALLY write ({episode_dir.name}_{id}_9x16.* for pages, {side}_cover.* for covers)
    # -- the original values here copied assemble_ashes.py's OLD filenames
    # (the_ashes_fNN_9x16.mp4 / front_cover_woodcut.mp4), which pointed at the
    # already-existing DEFECTIVE clips instead of the newly-rendered ones, so SW-F1 was
    # silently reading stale native durations from the wrong files.
    units=[
        Unit("front", HERE / "front_cover.mp4", 21, "boomerang"),
        # tail_loop_seconds: user's own fix idea, 2026-08-23 ("do the boomerang play
        # immediately at the end of a clip") -- ping-pong each clip's own settled tail
        # to fill its slot instead of a dead static freeze, $0, no longer render needed.
        # F04's tail is the SAFEST (its animation prompt explicitly completes the
        # gesture early and holds); F01's tail uses a shorter window since its motion
        # is more continuous -- both verified by eye before trusting (see session notes).
        Unit("f01", HERE / f"{HERE.name}_f01_9x16.mp4", 24, "freeze", tail_loop_seconds=1.0),
        Unit("f02", HERE / f"{HERE.name}_f02_9x16.mp4", 35, "boomerang"),
        Unit("f03", HERE / f"{HERE.name}_f03_9x16.mp4", 27, "boomerang"),
        Unit("f04", HERE / f"{HERE.name}_f04_9x16.mp4", 27, "freeze", tail_loop_seconds=1.8),
        Unit("back", HERE / "back_cover.mp4", 23, "boomerang"),
    ],
    scores={
        "original": ScoreVariant(
            score=HERE / "score_final.mp3",
            # gain_db lowered 3 -> 1 -> -1, 2026-08-23: user asked to soften the
            # score twice in a row -- pure local remix each time, no new HF spend.
            duck=DuckProfile(gain_db=-1, threshold=0.7, ratio=1.15, release_ms=500),
            out=HERE / "THE_ASHES_BOOK_final.mp4",
        ),
        "somber": ScoreVariant(
            score=HERE / "score_somber.mp3",
            duck=DuckProfile(gain_db=2, threshold=0.55, ratio=1.25, release_ms=400),
            out=HERE / "THE_ASHES_BOOK_final_somber.mp4",
        ),
        # NEW (2026-08-27, Fable "epic-soft" north-star pass): felt piano + strings +
        # choir, not the old trance -- ambient-pad duck (score_mix.py default), not the
        # rhythmic-tuned "original" duck above. Solo mean -17.8dB vs narration -20.3dB
        # (louder by 2.5dB, same magnitude ep8's Fig Tree needed gain_db=-6 for).
        "epic": ScoreVariant(
            score=HERE / "score_epic.mp3",
            duck=DuckProfile(gain_db=-6, threshold=0.12, ratio=2.5, release_ms=250),
            out=HERE / "THE_ASHES_BOOK_final_epic.mp4",
        ),
    },
    panel_style="woodcut_hybrid",
)
