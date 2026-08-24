"""swirls_cover.py -- shared prompt-assembly module for Swirls of Life covers.

Covers were 100% copy-pasted per episode (render_covers.py -> render_ashes_
covers.py) with zero shared module and zero canonical doc -- the direct
mechanism that let episode 2's cover lose its warm/cool color contrast and
grow an unrequested border, both caught only by the user watching the
finished video. This module + .claude/skills/swirls-of-life/NORTH_STAR_
COVER_PROMPT.md give covers the same single-source treatment interior pages
already have via swirls_page.py + NORTH_STAR_PROMPT.md.

Covers stay a genuinely separate dataclass from PageSpec -- no panels,
captions, dosage, or fence overlap; folding them into one type would be all
conditionals. See NORTH_STAR_COVER_PROMPT.md for the full template + the two
new laws (lighting-contrast, edge-to-edge) written directly against the two
observed defects.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "test_the_cross"))
from swirls_page import HF_CLI, Ref, _IMG_URL_RE, _VID_URL_RE, _refs_clause, _run_hf  # noqa: E402

# ---- fixed boilerplate, verbatim from the validated scripts (Jacob's Ladder
# render_covers.py / animate_covers.py) -- see NORTH_STAR_COVER_PROMPT.md's
# derivation notes. Any change here must be re-diffed against known-good
# renders (_validate_swirls_cover.py).

TITLE_STYLE = (
    "bold engraved wood-block title lettering, carved in the same dense woodcut style as the "
    "rest of the image — thick confident carved strokes, not a modern font, not a decorative "
    "flourish font, no drop shadow, no glow, no banner or box behind it, sitting naturally "
    "within the composition"
)

TEXT_LOCK_COVER = (
    "No other text, letters, numbers, or words appear anywhere on the image beyond these two "
    "lines — no watermark, no invented captions."
)

AVOID_BASE = (
    "modern clothing, busy foreground, bright neon colors, deformed anatomy, blurry rendering, "
    "smooth photorealism without linework"
)

# ---- NEW clauses, 2026-08-23 -- disclosed additions, not present in the
# original validated prompts (see NORTH_STAR_COVER_PROMPT.md's "SLOT" laws).

EDGE_TO_EDGE_CLAUSE = (
    "The artwork fills the entire image edge to edge — never a drawn border, picture frame, "
    "caption strip, or margin band around the scene."
)


def _opposite_edge_clause(title_position: str) -> str:
    """Targeted, POSITIVELY-worded fix for a defect the generic EDGE_TO_EDGE_CLAUSE above did
    NOT reliably prevent: a blank paper margin band at the edge opposite the title, seen on 3/3
    episode-8 front-cover renders (title_position='top') -- present even in the very first,
    otherwise-approved render, so this is not one-off variance. Named the edge positively
    (what the art DOES) rather than negatively (what must not appear) per the same lesson
    learned on F05's animation prompt the same session -- naming the banned thing tends to
    partially render it anyway on these models."""
    edge = "bottom" if title_position == "top" else "top"
    return (
        f"At the very {edge} of the frame, the scene's own artwork runs all the way to the "
        "canvas edge, fully painted with no blank paper showing."
    )

# Warm/cool token families for SW-L1 (swirls_verify.py) -- kept here so the
# lint and the doc's own law stay next to the constant they check.
WARM_TOKENS = ("ochre", "gold", "golden", "amber", "warm", "dawn", "dusk sun", "ember")
# "grey"/"gray" added 2026-08-23: episode 2's own non-defective back cover ("an open sky
# breaking from grey into warm gold") has no more specific cool word than plain grey --
# a standard cool/desaturated descriptor in art direction, not a loophole. Adding it does
# NOT weaken the check against the actual observed defect (episode 2's front cover had
# ZERO warm tokens at all -- "no vivid color anywhere" -- so it still correctly fails
# regardless of what counts as cool).
COOL_TOKENS = ("teal", "blue", "cool", "grey", "gray", "cold")

FRONT_ANIM_LOCK = (
    "Stationary camera, locked wide static shot, no pan, no zoom. The baked title lettering "
    "at the top of the frame — both the large title and the smaller line beneath it — stays "
    "pixel-for-pixel identical for every single frame of the clip: same exact opacity from "
    "first frame to last, never fading in or out, never dissolving, never duplicating or "
    "doubling, never drifting position."
)

BACK_ANIM_LOCK = (
    "Stationary camera, locked wide static shot, no pan, no zoom. The baked closing lettering "
    "at the bottom of the frame stays perfectly static and unchanged for the whole clip."
)

ANIM_CLOSER = "no new figure, mark, or text appears anywhere on the frame at any point."


@dataclass
class CoverSpec:
    side: Literal["front", "back"]
    scene: str                     # authored prose: figure(s) + landscape setting, ending
                                     # right before the lighting sentence, NOT decomposed further
    lighting: str                  # authored prose, the full lighting/atmosphere sentence --
                                     # MUST name >=1 warm + >=1 cool element (SW-L1, see
                                     # NORTH_STAR_COVER_PROMPT.md's lighting-contrast law)
    title: str                     # baked headline, grounded in the narration's own line
    subtitle: str                  # real scripture reference
    title_position: Literal["top", "bottom"]   # front=top, back=bottom, validated pattern
    animation: str                 # authored prose: the living-detail + lighting-invariance
                                     # body, between the camera/text lock and the closer --
                                     # NOT decomposed further, same discipline as PageSpec's
                                     # main_scene_animation
    background_detail: str = ""    # optional trailing still-prompt sentence, e.g. distant tents
    extra_avoid: str = ""          # appended to the base Avoid list, e.g. "visible wounds, blood, gore"
    refs: list[Ref] = field(default_factory=list)
    aspect_ratio: Literal["9:16", "16:9"] = "9:16"
    clip_duration: int = 4         # veo3_1_lite; legal values 4, 6, 8 only (hf CLI enforces)


# Present in the validated source (render_covers.py) and documented as a LOCKED constant in
# NORTH_STAR_COVER_PROMPT.md ("Vast wind-scoured wilderness... sweeping sky"), but was never
# actually wired into this module -- the gap that let episode 8's front cover render as a
# soft, intimate ink-wash illustration instead of the epic cinematic-woodcut cover style every
# episode's cover is supposed to share. Fixed 2026-08-24 (user: "can Front cover look more
# epic like we did with the first episode").
WILDERNESS_SKY_CLAUSE = (
    "Vast wind-scoured wilderness, rugged rocky hill country, sweeping stony valleys, carved "
    "structural cloud forms in an open sweeping sky."
)


def _style_block(aspect_ratio: str) -> str:
    ratio_desc = "vertical 9:16" if aspect_ratio == "9:16" else "16:9"
    return (
        "16th-century Albrecht Durer woodcut linework blended with contemporary cinematic "
        "landscape photography, dense parallel hatching, hard black contours, ink-on-block "
        f"texture, {ratio_desc} aspect ratio, figure isolated in the lower third, stationary "
        "camera, wide static shot, ultra-crisp."
    )


def _avoid_clause(extra: str) -> str:
    tail = f", {extra}" if extra else ""
    return f"Avoid: {AVOID_BASE}{tail}."


def assemble_cover_still_prompt(spec: CoverSpec) -> str:
    position_word = "top" if spec.title_position == "top" else "bottom"
    parts = [spec.scene.strip(), " ", WILDERNESS_SKY_CLAUSE, " ", spec.lighting.strip()]
    if spec.background_detail:
        parts += [" ", spec.background_detail.strip()]
    parts += [
        " ", _style_block(spec.aspect_ratio), " ",
        f'Near the {position_word} of the frame, {TITLE_STYLE}, reading: "{spec.title}", '
        f'with smaller matching lettering beneath it reading: "{spec.subtitle}". ',
        EDGE_TO_EDGE_CLAUSE, " ", _opposite_edge_clause(spec.title_position), " ",
        TEXT_LOCK_COVER, " ",
        _avoid_clause(spec.extra_avoid),
        _refs_clause(spec.refs),
    ]
    return "".join(parts)


def assemble_cover_animation_prompt(spec: CoverSpec) -> str:
    lock = FRONT_ANIM_LOCK if spec.side == "front" else BACK_ANIM_LOCK
    return f"{lock} {spec.animation.strip()}; {ANIM_CLOSER}"


def render_cover_still(spec: CoverSpec, out_png: Path) -> bool:
    if out_png.exists():
        print(f"  [skip] {out_png.name} already exists")
        return True
    missing = [r for r in spec.refs if not Path(r.path).exists()]
    if missing:
        for r in missing:
            print(f"  FAILED: ref missing for {r.subject!r}: {r.path}")
        print("  (ref-chaining rule: a recurring subject with no chained ref is a hard stop — "
              "crop it from its first approved render before spending.)")
        return False
    prompt = assemble_cover_still_prompt(spec)
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", prompt]
    for r in spec.refs:
        cmd += ["--image", r.path]
    cmd += ["--aspect_ratio", spec.aspect_ratio, "--resolution", "2k", "--wait"]
    print(f"  [nano_banana_pro] rendering {out_png.name} ({spec.side} cover)...")
    ok = _run_hf(cmd, out_png, _IMG_URL_RE, 600)
    if ok:
        print("  NOW: eyeball at 1:1 + referent check BEFORE animating.")
    return ok


def render_cover_animation(spec: CoverSpec, png: Path, out_mp4: Path) -> bool:
    if out_mp4.exists():
        print(f"  [skip] {out_mp4.name} already exists")
        return True
    if not png.exists():
        print(f"  FAILED: still {png.name} not rendered yet.")
        return False
    prompt = assemble_cover_animation_prompt(spec)
    cmd = [HF_CLI, "generate", "create", "veo3_1_lite", "--prompt", prompt,
           "--start-image", str(png), "--aspect_ratio", spec.aspect_ratio,
           "--duration", str(spec.clip_duration), "--wait"]
    print(f"  [veo3_1_lite] rendering {out_mp4.name} ({spec.side} cover)...")
    ok = _run_hf(cmd, out_mp4, _VID_URL_RE, 900)
    if ok:
        print("  NOW: 4-frame contact sheet + real playback (QC law).")
    return ok
