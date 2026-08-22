"""swirls_page.py -- shared prompt-assembly module for Swirls of Life pages.

Replaces per-episode render_the_X.py boilerplate duplication (six scripts,
each re-typing the same ~120 words of fixed structure) with one parameterized
assembly function. Scene-specific content (motif clauses, character poses,
swirl placement) stays AUTHORED PROSE per page, passed in on a PageSpec --
see .claude/skills/swirls-of-life/PRODUCTION_PIPELINE.md for why: those
clauses carry too much scene-specific geometry to templatize without either
losing the specificity that passes QC, or reinventing a parameter language as
complex as prose itself. Only the genuinely-identical wrapping text is
mechanized here.

Usage: an episode script builds a PageSpec, calls assemble_still_prompt() /
assemble_animation_prompt(), then render_still() / render_animation() to
actually spend and fetch the render (same hf.exe subprocess pattern every
existing script already uses, so behavior is unchanged, only the prompt
construction is shared).
"""
from __future__ import annotations

import re
import subprocess
import urllib.request
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"

_IMG_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
_VID_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)

# ---- fixed boilerplate, verbatim from the validated scripts (Hem F04/F05,
# Thomas F01/F01v2/F02) -- see PRODUCTION_PIPELINE.md's derivation notes.
# Any change here must be re-diffed against known-good renders (module
# docstring's usage note / the migration path in PRODUCTION_PIPELINE.md).

STYLE_OPEN = (
    'One single storyboard page of hand-drawn animation development art, delicate ink linework and '
    'watercolor on aged cream paper, laid out like a real found piece of production art. Top-left '
    'title, handwrite: "SEQ: {seq_title}". Top-right frame number, handwrite: "{frame_label}". Across the top, a '
    'row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY '
    'label: '
)

TEXT_LOCK = (
    'No other text, letters, numbers, or words appear anywhere on the page beyond the exact '
    'handwrite strings given above — no invented captions, signs, inscriptions, or titulus.'
)

PALETTE_PREFIX = (
    'Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash on '
    'aged cream paper with visible grain. Not photorealistic, not anime, not Disney, no polished '
    'graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing '
    'spiritual VFX — every blue or gold element behaves like literal wet ink bleeding into paper, '
    'never a magic-particle glow, and '
)

NO_BUBBLE_CLAUSE = "with no border, box, or speech bubble ever appearing around any caption or note"


@dataclass
class Ref:
    """One chained reference image for a RECURRING subject (character, object,
    artifact, or location). Rule (locked 2026-08-22, Jacob's Ladder pilot): any
    subject that appears on more than one page gets its own ref, cropped from its
    first approved render, and is chained into every later page it appears on.
    Text alone drifted every one of them — beard, dress, stone, staff, ladder,
    terrain — across the 8 pilot stills."""
    subject: str    # what it is + what to match, e.g. "Jacob — his face, hair, sparse beard, build and dress"
    path: str       # local PNG, auto-uploaded by hf; must exist or render_still hard-stops


@dataclass
class Panel:
    label: str      # circled-number caption, e.g. "not with them"
    content: str    # authored prose, NO leading/trailing punctuation, e.g.
                     # 'a small sketch of a shut wooden door with its heavy bar in place'


@dataclass
class PageSpec:
    seq_title: str                 # e.g. "THOMAS" (goes after "SEQ: ")
    frame_label: str               # e.g. "F01"
    panels: tuple[Panel, Panel, Panel]
    still_shot_type: str           # e.g. "MEDIUM WIDE shot" -- exact capitalization for the still prompt
    anim_shot_desc: str            # e.g. "medium wide shot" -- exact wording for the animation camera line
    main_scene_still: str          # authored prose from "a plain lamplit room..." through the
                                     # motif/swirl clause's own final period. NOT decomposed further.
    material_closer: str           # authored prose: trailing palette-sentence clause naming how
                                     # THIS page's own dead ink (or absence of it) behaves, incl. trailing period
    panel_motions: tuple[str, str, str]   # authored prose, animation-side, one per panel, NO leading
                                            # "panel N" prefix and no trailing punctuation
    main_scene_animation: str      # authored prose: character motion content only, starting right
                                     # after "Large bottom panel: ", NOT including the closing fence
    fence_kind: Literal["fray", "stain", "none"]
    fence_callout: str = ""        # required unless fence_kind == "none", e.g.
                                     # "the broken, tremored linework of Thomas's figure"
    caption_lines: tuple[str, ...] = ()
    corner_note: str = ""
    refs: list[Ref] = field(default_factory=list)   # chained subject refs, in attach order
    model_tier: Literal["kling3_0", "veo3_1_lite"] = "kling3_0"
    aspect_ratio: Literal["9:16", "16:9"] = "9:16"
    include_no_bubble_clause: bool = True


def _panel_prose_still(panels: tuple[Panel, Panel, Panel]) -> str:
    p1, p2, p3 = panels
    return (
        f'panel 1 (handwrite: "{p1.label}") {p1.content}, '
        f'panel 2 (handwrite: "{p2.label}") {p2.content}, '
        f'panel 3 (handwrite: "{p3.label}") {p3.content}. '
    )


def _caption_prose(caption_lines: tuple[str, ...], corner_note: str) -> str:
    if len(caption_lines) == 1:
        cap_intro = "a caption beneath the main scene"
        cap_lines = f'handwrite: "{caption_lines[0]}"'
    else:
        cap_intro = "a caption beneath the main scene on two stacked lines"
        cap_lines = ", ".join(f'handwrite: "{line}"' for line in caption_lines)
    return (
        f"Small handwritten production notes integrated naturally on the page: {cap_intro}, "
        f'{cap_lines}, and a corner note, handwrite: "{corner_note}". '
    )


def _fence(kind: Literal["fray", "stain", "none"], callout: str) -> str:
    if kind == "none":
        return ""
    if kind == "fray":
        return (
            "every ink line and mark on the page is long set and stays exactly as drawn — including "
            f"{callout}, which keeps its exact drawn character, stroke for stroke, for the whole clip; "
            "no line anywhere redraws or changes, and no new stain, spot, or mark appears anywhere on "
            "the page at any point."
        )
    if kind == "stain":
        return (
            f"every stain and mark in the paper — including {callout} — is old, dry, and long set, "
            "staying exactly as drawn; no new stain, spot, or darkening appears anywhere on the page "
            "at any point."
        )
    raise ValueError(f"unknown fence_kind {kind!r}")


def _refs_clause(refs: list[Ref]) -> str:
    if not refs:
        return ""
    listing = "; ".join(f"image {i} is {r.subject}" for i, r in enumerate(refs, 1))
    return (
        f" Attached reference images, in order: {listing}. Every appearance of each referenced "
        "subject anywhere on this page — in any of the three top panels or in the main scene, at "
        "any size, angle, or distance — matches its reference exactly, the same drawing of the "
        "same thing."
    )


def assemble_still_prompt(spec: PageSpec) -> str:
    parts = [
        STYLE_OPEN.format(seq_title=spec.seq_title, frame_label=spec.frame_label),
        _panel_prose_still(spec.panels),
        "Below them, ONE large full-scene illustration filling the lower half of the page — a "
        + spec.still_shot_type + ": " + spec.main_scene_still.strip() + " ",
        _caption_prose(spec.caption_lines, spec.corner_note),
        TEXT_LOCK + " ",
        PALETTE_PREFIX + spec.material_closer.strip(),
        _refs_clause(spec.refs),
    ]
    return "".join(parts)


def assemble_animation_prompt(spec: PageSpec) -> str:
    if spec.model_tier == "kling3_0" and len(spec.caption_lines) > 1:
        warnings.warn(
            "kling3_0 + a 2-line stacked caption: the no-bubble clause has FAILED 3/3 consecutive "
            "attempts on this exact combination (Thomas F02, 2026-08-21). Consider veo3_1_lite, or "
            "eyeball the contact sheet before trusting this one.",
            stacklevel=2,
        )
    bubble = (", " + NO_BUBBLE_CLAUSE) if spec.include_no_bubble_clause else ""
    m1, m2, m3 = spec.panel_motions
    parts = [
        f"Stationary camera, locked {spec.anim_shot_desc} of the 2D storyboard layout, frame borders "
        f"and all baked text stay static{bubble}. ",
        f"Animate isolated motion inside each panel: panel 1 {m1}; panel 2 {m2}; panel 3 {m3}. ",
        "Large bottom panel: " + spec.main_scene_animation.strip() + " ",
        _fence(spec.fence_kind, spec.fence_callout),
    ]
    return "".join(parts)


# ---- character build registry -------------------------------------------------
# Face/dress builds ONLY -- dead-ink motifs are applied per-page in
# main_scene_still, never baked in here (a character must be able to appear
# steady on one page and afflicted on another).

CHARACTER_REGISTRY: dict[str, str] = {
    "thomas": (
        "a sturdy middle-aged Galilean man with a squarish weathered face, heavy dark brows, deep-set "
        "questioning eyes, dark hair and a short thick dark beard flecked with grey, a plain robe of "
        "muted clay-red wash over an undyed cream tunic, a rough olive-brown mantle across one "
        "shoulder, drawn in dense workmanlike cross-hatching; he wears no blue and no gold anywhere"
    ),
    "hem_woman": (
        "a gaunt weary woman with a drawn, hollowed face and large hopeful dark eyes, dark hair "
        "fully under a plain undyed head covering, layered garments of faded olive-green and muted "
        "grey-brown wash over an undyed cream tunic, drawn in dense fine cross-hatching; she wears "
        "no blue and no red anywhere"
    ),
}


# ---- render (unchanged subprocess pattern from every existing script) --------

def _run_hf(cmd: list[str], out_path: Path, url_re: re.Pattern, timeout: int) -> bool:
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout)
    if proc.returncode != 0:
        print(f"        FAILED: hf CLI exit {proc.returncode}: {(proc.stderr or proc.stdout).strip()[-800:]}")
        return False
    match = url_re.search(proc.stdout)
    if not match:
        print(f"        FAILED: no output URL in stdout: {proc.stdout.strip()[-800:]}")
        return False
    req = urllib.request.Request(match.group(0), headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        out_path.write_bytes(resp.read())
    print(f"        -> {out_path.name} ({out_path.stat().st_size:,} bytes)")
    return True


def render_still(spec: PageSpec, out_png: Path) -> bool:
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
    prompt = assemble_still_prompt(spec)
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", prompt]
    for r in spec.refs:
        cmd += ["--image", r.path]
    cmd += ["--aspect_ratio", spec.aspect_ratio, "--resolution", "2k", "--wait"]
    print(f"  [nano_banana_pro] rendering {out_png.name}...")
    ok = _run_hf(cmd, out_png, _IMG_URL_RE, 600)
    if ok:
        print("  NOW: eyeball at 1:1 + referent check BEFORE animating.")
    return ok


def render_animation(spec: PageSpec, png: Path, out_mp4: Path) -> bool:
    if out_mp4.exists():
        print(f"  [skip] {out_mp4.name} already exists")
        return True
    if not png.exists():
        print(f"  FAILED: still {png.name} not rendered yet.")
        return False
    prompt = assemble_animation_prompt(spec)
    cmd = [HF_CLI, "generate", "create", spec.model_tier, "--prompt", prompt,
           "--start-image", str(png), "--aspect_ratio", spec.aspect_ratio]
    if spec.model_tier == "kling3_0":
        cmd += ["--mode", "pro", "--duration", "5", "--sound", "off"]
    else:
        cmd += ["--duration", "4"]
    cmd += ["--wait"]
    print(f"  [{spec.model_tier}] rendering {out_mp4.name}...")
    ok = _run_hf(cmd, out_mp4, _VID_URL_RE, 900)
    if ok:
        print("  NOW: 4-frame contact sheet + real playback (QC law).")
    return ok
