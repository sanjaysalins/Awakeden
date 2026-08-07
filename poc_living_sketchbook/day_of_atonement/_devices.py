"""Day of Atonement LONG -- device dispatch layer for the motion-design
rollout (2026-08-06), implementing RESUME.md's 2026-08-05 handover.

_s5b_spread_windows.py / _s6_assemble.py only solve the mechanical problem
of stretching a clip to fill its window (trim/hold/drift). This file adds
the separate, previously-missing axis: WHICH of the 27 kept devices (from
_KEEPER_PICKER.html) a given spread should use instead of the generic
push/arc camera move, keyed by spread name.

Two scopes:
  "full" -- the spread has no real generative clip worth keeping (or its
            device fully replaces the visual) -- render straight from the
            spread's own STILL for the whole window, bypassing fill-mode
            entirely.
  "tail" -- the spread keeps its real clip playing forward once, then the
            device replaces only the generic push/arc TAIL (over the clip's
            own last frame) that used to fill the remainder.

Scope-per-spread was derived from _s5b_spread_windows.py's own DETERMINISTIC
set (spreads with no real clip at all get "full"; everything else gets
"tail") -- NOT by re-reading RESUME.md's prose list, which mixes the two.

Covers RESUME.md handover section 2 (verse-card text-combo devices, 8 plain
cards) + section 3 (21 held/no-camera-move device swaps). Section 4 (the
~50 "plain" NS/MV rotation) and section 5 (the ~73-cut transition layer)
are a follow-up pass -- spreads not listed here just keep today's existing
fill-mode behavior unchanged.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "panel_animator"))
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import parallax_25d  # noqa: E402
import registration_snap  # noqa: E402
import palette_pivot  # noqa: E402
import crop_mark_approval  # noqa: E402
import letterpress_beat  # noqa: E402
import ink_up_build  # noqa: E402
import focal_tour  # noqa: E402
from held_breath import energy_envelope  # noqa: E402
from raking_light import (apply_raking_light, paper_tooth_highpass, scale_crop as rl_scale_crop,  # noqa: E402
                           isolate_gold_leaf, apply_gold_flare)
import line_boil  # noqa: E402
import candle_only  # noqa: E402
import _poc_motion_text_combo as combo  # noqa: E402  -- reuse the proven verse-arrival renders
import _s3_thread_leaf_54_55 as tl  # noqa: E402  -- reuse the proven letterpress-tile primitives
BODY_SIZE = combo.BODY_SIZE  # 40 -- shared alias so VERSE_CARDS' run-lists stay in sync with the module
import unseen_hand  # noqa: E402
import thread_device  # noqa: E402
import leaf_flick  # noqa: E402
import tipped_in_plate  # noqa: E402
import ink_transition  # noqa: E402
import verse_mask_reveal  # noqa: E402
import through_object_cut  # noqa: E402

W, H, FPS = 1920, 1080, 30

ALIGNMENT = json.loads((HERE / "_alignment.json").read_text(encoding="utf-8"))
LAST_WORD_END = max(w["end"] for w in ALIGNMENT)


def _run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


# ------------------------------------------------------------- no-bbox devices

def _plain_static(still: Path, dest: Path, duration: float):
    _run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(still), "-t", f"{duration:.3f}",
          "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])


def _raking_light(still: Path, dest: Path, duration: float, flare: bool = False,
                   energy_amp: bool = False, abs_start: float = 0.0, hush_decay: bool = False):
    """Plain lamp sweep, no wobble/no flare by default -- legibility-preserving,
    for cards/objects (panel_animator/raking_light.py's own render_demo() defaults
    to a 1080x1920 VERTICAL frame, wrong for this 1920x1080 film -- call the
    primitives directly at the right size instead, per _poc_holds_round2.py).

    Round 10 additions (only 3 raking survivors now, each paired per the
    Pairing Law): `flare` enables the one-flare-per-episode gold specular
    bump (s03, the subject IS gold); `energy_amp` multiplies the sweep
    strength `k` by this episode's own held-breath energy_envelope (s42, so
    the light visibly quiets with the narrator instead of a flat sweep);
    `hush_decay` forces k -> 0 over the final ~1.2s (s61, the page goes DEAD
    STILL just before the mandatory hard cut into the tear -- stillness that
    ARRIVES reads as intent, not a freeze)."""
    base = rl_scale_crop(Image.open(still).convert("RGB"), W, H)
    tooth = paper_tooth_highpass(base)
    gold_mask = isolate_gold_leaf(base) if flare else None
    energy = energy_envelope(ALIGNMENT, LAST_WORD_END, floor=0.25, ramp=0.15) if energy_amp else None
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        progress = i / max(1, n - 1)
        t_local = i / FPS
        k = 0.03
        if energy is not None:
            k *= 0.4 + 0.6 * energy(abs_start + t_local)
        if hush_decay:
            hush_start = max(0.0, duration - 1.2)
            if t_local >= hush_start:
                k *= max(0.0, 1.0 - (t_local - hush_start) / 1.2)
        frame = apply_raking_light(base, progress, tooth=tooth, k=k)
        if flare:
            frame = apply_gold_flare(frame, progress, gold_mask=gold_mask, intensity=1.0)
        frame.save(frames / f"f{i:04d}.png")
    _run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames / "f%04d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    shutil.rmtree(frames)


def _line_boil_still(still: Path, dest: Path, duration: float, amount: float = 0.6):
    """line_boil.py's own render() reads fps/w/h off an EXISTING clip (it
    probes, doesn't assume) -- build a plain static hold first, then apply
    the hand-inked wobble on top of it. Amplitude kept subtler (0.6, not the
    module's own 1.0 default) since this is a calm held moment, not an
    action panel."""
    pre = dest.parent / (dest.stem + "_preboil.mp4")
    _plain_static(still, pre, duration)
    line_boil.render(pre, dest, amount)
    pre.unlink(missing_ok=True)


def _candle_only_still(still: Path, dest: Path, duration: float, anchor_frac: tuple):
    """Promotes panel_animator/candle_only.py's radial light budget (Round 6)
    to a real device slot here -- replaces s43's dramatic_spotlight
    placeholder with the module the plan always called "the device's literal
    design case." R(t) closes down over the spread ("fear closes it down,"
    per the module's own governing rule) then flickers; anchor is the
    AUTHORED lamp position from the still-QC pass, never auto-detected."""
    src = Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS)
    ax, ay = anchor_frac[0] * W, anchor_frac[1] * H
    keyframes = [(0.0, H * 0.42), (duration * 0.65, H * 0.24), (duration, H * 0.20)]
    base_curve = lambda t: candle_only.radius_from_keyframes(keyframes, t)  # noqa: E731
    R_of_t = candle_only.flicker_R(base_curve, seed=51, amplitude=6.0)
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t_local = i / FPS
        frame = candle_only.apply_candle(src, t_local, (ax, ay), R_of_t)
        frame.save(frames / f"f{i:04d}.png")
    _run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames / "f%04d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    shutil.rmtree(frames)


# ------------------------------------------------------ post-process ramps
# Both operate on an ALREADY-RENDERED clip (parallax_25d's own render() writes
# straight to disk via rembg + ffmpeg, no per-frame hook) -- extract frames,
# apply a per-frame gain field, re-encode. Reuses the clip's own real motion,
# just adds a slow global colour/vignette arc on top.

def _apply_edge_darken_ramp(clip_path: Path, dest: Path, target_edge_gain: float = 0.72,
                             center_frac: float = 0.55):
    """Passion-Vigil register (s53, Fable Round 10): a slow radial vignette
    eases in from neutral to `target_edge_gain` at the frame edges across the
    clip's own duration, while the centre (the figure) stays lit -- "the
    world darkens around Him." Restrained, no pulse."""
    work = dest.parent / (dest.stem + "_vframes")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    _run(["ffmpeg", "-y", "-i", str(clip_path), str(work / "f%05d.png")])
    frames = sorted(work.glob("f*.png"))
    n = len(frames)
    y_grid, x_grid = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W / 2.0, H / 2.0
    max_r = float(np.sqrt(cx ** 2 + cy ** 2))
    dist = np.sqrt((x_grid - cx) ** 2 + (y_grid - cy) ** 2) / max_r
    vignette_shape = np.clip((dist - center_frac) / (1.0 - center_frac), 0, 1)
    for i, fp in enumerate(frames):
        t = i / max(1, n - 1)
        gain_at_edge = 1.0 - t * (1.0 - target_edge_gain)
        gain_field = 1.0 - vignette_shape * (1.0 - gain_at_edge)
        arr = np.asarray(Image.open(fp).convert("RGB"), dtype=np.float32) * gain_field[..., None]
        Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(fp)
    _run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    shutil.rmtree(work)


def _apply_warm_goldin_ramp(clip_path: Path, dest: Path, ramp_duration: float = 3.0, boost: float = 0.12):
    """s51_jesus_pivot (Fable Round 10): the gold register the still already
    carries in its rays arrives with Him -- a warm channel gain eases IN over
    the first `ramp_duration` seconds (smootherstep), then holds, rather than
    a flat unchanging tint for the whole spread."""
    work = dest.parent / (dest.stem + "_gframes")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    _run(["ffmpeg", "-y", "-i", str(clip_path), str(work / "f%05d.png")])
    frames = sorted(work.glob("f*.png"))
    warm = np.array([1.0 + boost, 1.0 + boost * 0.5, 1.0 - boost * 0.3], dtype=np.float32)
    for i, fp in enumerate(frames):
        t = i / FPS
        p = min(1.0, t / ramp_duration)
        ease = p * p * (3 - 2 * p)
        gain = 1.0 + ease * (warm - 1.0)
        arr = np.asarray(Image.open(fp).convert("RGB"), dtype=np.float32) * gain[None, None, :]
        Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(fp)
    _run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    shutil.rmtree(work)


# ---------------------------------------------------------------- bbox devices

def _spotlight_family(style: str, still: Path, dest: Path, duration: float, bbox: list):
    """dramatic_spotlight / caravaggio_pulse via the same duration-scaled
    hold/move tuning _poc_spotlight_holds.py proved (focal_tour.render_clip's
    own hardcoded 2.5/1.0/2.5s defaults need >=6s and would overrun a short
    spread)."""
    regions = [{"bbox": bbox}]
    init_hold = max(0.8, min(2.5, duration * 0.18))
    move = max(0.5, min(1.0, duration * 0.08))
    src = Image.open(still).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    focal_tour._RENDERERS[style](src, regions, duration, W, H, dest,
                                  initial_hold_sec=init_hold, move_sec=move, final_hold_sec=init_hold)


def _breath_synced_halo(still: Path, dest: Path, duration: float, bbox: list, abs_start: float):
    """The approved caravaggio_pulse halo, but its breathing damps toward
    stillness during this episode's OWN real narration silences instead of a
    fixed 3s cycle (per _poc_holds_round2.py's build_breath_synced_halo)."""
    energy = energy_envelope(ALIGNMENT, LAST_WORD_END, floor=0.25, ramp=0.15)
    src = Image.open(still).convert("RGB")
    src_arr = np.asarray(src.resize((W, H), Image.LANCZOS), dtype=np.float32) / 255.0
    y_grid, x_grid = np.mgrid[0:H, 0:W].astype(np.float32)
    regions = [{"bbox": bbox}]
    init_hold = max(0.8, min(2.5, duration * 0.18))
    move = max(0.5, min(1.0, duration * 0.08))
    schedule = focal_tour.build_tour_schedule(regions, duration, W, H, init_hold, move, init_hold)
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t_local = i / FPS
        e = energy(abs_start + t_local)
        cx, cy, r = focal_tour.center_at(schedule, t_local)
        r_pulsed = r * (1.0 + 0.20 * e * np.sin(2 * np.pi * (t_local % 3.0) / 3.0))
        dim_floor = 0.30 - 0.04 * (1.0 - e)
        bright = focal_tour.halo_brightness(x_grid, y_grid, cx, cy, r_pulsed, dim_floor)
        frame = np.clip(src_arr * bright[..., None] * 255.0, 0, 255).astype(np.uint8)
        Image.fromarray(frame).save(frames / f"f{i:04d}.png")
    _run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames / "f%04d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    shutil.rmtree(frames)


# ------------------------------------------------------- special-card renders
# Concept B (Fable Round 10): the four "specially-named" verse cards
# (s16/s52 Illuminated Rubric, s31 Scribed-Ink live-write, s49 stacked
# double-verse) shipped on raking_light placeholders through the whole
# rollout -- built for real here, un-deferrable now. None of these fit the
# combo A/B/C system (they're each a bespoke register per _PLAN.md), so they
# dispatch outside VERSE_CARDS/render_verse_card entirely.

RUBRIC = (150, 26, 22)      # matches panel_animator's own RUBRIC (annotators_circle.py etc.)
GOLD = (185, 146, 74)       # matches panel_animator's own GOLD
CAP_SIZE = 110
RUBRIC_BODY_SIZE = 36
ATTRIB_SIZE = 32


def _radial_gain(x_grid, y_grid, cx, cy, radius, peak_gain):
    dist = np.sqrt((x_grid - cx) ** 2 + (y_grid - cy) ** 2)
    return 1.0 + (peak_gain - 1.0) * np.clip(1.0 - dist / radius, 0.0, 1.0)


def _render_illuminated_rubric(still: Path, dest: Path, duration: float, glow_bbox: list,
                                cap_letter: str, first_line_rest: str, body_lines: list,
                                attribution: str, abs_start: float,
                                press_t: float = 1.5, raking_t: float = 9.0,
                                body_color: tuple = None, ref_text: str = None):
    """LAW 1 (red-letter arrives WHOLE, never word-by-word): a charge or
    thesis verse presses in as ONE block at `press_t` with a brief light
    swell on the dropped cap, a gold-leaf ground behind the cap only (gold =
    His glory). `body_color` defaults to RUBRIC (red-letter, for actual
    first-person LORD/Christ speech per this project's locked "red-letter
    speaker = the speaker" rule) -- pass tl.INK_FINAL for a verse that is
    NOT divine speech (e.g. Hebrews narrating about Christ's action), which
    reuses this card's visual grammar without misrepresenting who's talking.
    `attribution` may be "" to omit the narrator-frame line entirely (some
    verses have no natural "X said" clause); `ref_text` optionally stamps a
    small gold-stitched citation after the last body line for a card with no
    attribution, so it still reads as a grounded, cited verse.
    The art's own light source (glow_bbox) breathes throughout (before AND
    after the press) plus one slow k=0.02 raking pass crossing near
    `raking_t` so a long card is never inert -- built from already-proven
    primitives, no new visual grammar."""
    body_color = body_color or RUBRIC
    src = Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS)
    src_arr = np.asarray(src, dtype=np.float32) / 255.0
    tooth = paper_tooth_highpass(src)
    y_grid, x_grid = np.mgrid[0:H, 0:W].astype(np.float32)

    # Round 10 bugfix: the first cut of this reused focal_tour's spotlight-
    # SCHEDULE (built for a moving attention halo across a bare still) --
    # once the "tour" arrived at the glow it dimmed EVERYTHING outside that
    # region, including the text block sitting right next to it (confirmed
    # by eye: the whole card visibly darkened from ~t=2s to ~t=16s). This
    # card needs the opposite: the glow breathes IN PLACE, nothing else ever
    # dims. A plain localized radial gain (>1 inside the glow, =1 outside,
    # oscillating with the episode's own energy envelope) replaces the tour.
    glow_cx, glow_cy, glow_r = focal_tour.focal_to_px(tuple(glow_bbox), W, H)
    energy = energy_envelope(ALIGNMENT, LAST_WORD_END, floor=0.25, ramp=0.15)

    cap_font = ImageFont.truetype(tl.F_BODY, CAP_SIZE)
    body_font = ImageFont.truetype(tl.F_BODY, RUBRIC_BODY_SIZE)
    attrib_font = ImageFont.truetype(tl.F_BODY, ATTRIB_SIZE)
    fonts = {CAP_SIZE: cap_font, RUBRIC_BODY_SIZE: body_font, ATTRIB_SIZE: attrib_font}

    has_attrib = bool(attribution)
    attrib_mask = tl.make_line_mask([(attribution, ATTRIB_SIZE)], fonts) if has_attrib else None
    attrib_tile = tl.compose_pressed_tile(attrib_mask[0], tl.INK_FINAL) if has_attrib else None
    line1_mask = tl.make_line_mask([(cap_letter, CAP_SIZE), (first_line_rest, RUBRIC_BODY_SIZE)], fonts)
    line1_tile = tl.compose_pressed_tile(line1_mask[0], body_color)
    body_masks = [tl.make_line_mask([(line, RUBRIC_BODY_SIZE)], fonts) for line in body_lines]
    body_tiles = [tl.compose_pressed_tile(m[0], body_color) for m in body_masks]

    ref_tile = None
    if ref_text:
        ref_font = ImageFont.truetype(tl.F_BODY, 22)
        dummy = ImageDraw.Draw(Image.new("L", (1, 1)))
        ref_w = int(sum(dummy.textlength(ch, font=ref_font) for ch in ref_text) + 3 * (len(ref_text) - 1))
        rt_w, rt_h = max(tl.STITCH_LEN, ref_w) + 8, int(ref_font.size * 1.9) + 8
        ref_tile = Image.new("RGBA", (rt_w, rt_h), (0, 0, 0, 0))
        rd = ImageDraw.Draw(ref_tile)
        rd.line([(0, 4), (tl.STITCH_LEN, 4)], fill=(*tl.GOLD, 255), width=3)
        tl.draw_letterspaced(rd, (0, 14), ref_text, ref_font, (*tl.REF_GOLD, 255), spacing=3)

    all_masks = ([attrib_mask] if has_attrib else []) + [line1_mask] + body_masks
    line_heights = [max(int(RUBRIC_BODY_SIZE * 1.4), m[2] + 8) for m in all_masks]
    max_w = max([m[1] for m in all_masks] + ([ref_tile.width] if ref_tile else []))
    plate_h = sum(line_heights) + 24 + (ref_tile.height + 10 if ref_tile else 0)
    plate_w = max_w + 44
    block_x, block_y = int(0.055 * W), int(0.035 * H)

    # cap glyph's own screen position (for the gold ground + the swell) --
    # roughly one cap-width right of the block's left edge, vertically at
    # line1's own baseline (offset past the attribution row, if present).
    _, _, _, pad1, base1 = line1_mask
    line1_idx = 1 if has_attrib else 0
    y_before_line1 = block_y + (line_heights[0] if has_attrib else 0)
    cap_cx = block_x + CAP_SIZE * 0.55
    cap_cy = y_before_line1 + base1 - CAP_SIZE * 0.35

    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        e = energy(abs_start + t)
        breath = 1.0 + 0.10 * e * np.sin(2 * np.pi * (t % 4.0) / 4.0)
        bright = _radial_gain(x_grid, y_grid, glow_cx, glow_cy, glow_r * 1.15, breath)

        # one slow raking pass, confined to a window around raking_t --
        # progress sweeps 0->1 only inside that window, static outside it.
        pass_dur = 5.0
        p = np.clip((t - (raking_t - pass_dur / 2)) / pass_dur, 0.0, 1.0)
        frame = apply_raking_light(Image.fromarray(np.clip(src_arr * bright[..., None] * 255, 0, 255).astype(np.uint8)),
                                    p, tooth=tooth, k=0.02)
        img = frame.convert("RGBA")

        if t >= press_t:
            plate = Image.new("RGBA", (plate_w, plate_h), (222, 208, 178, 165))
            img.alpha_composite(plate, (block_x - 20, block_y - 12))

            # gold-leaf ground behind the cap ONLY, drawn before the glyph
            gold_r = CAP_SIZE * 0.62
            d = ImageDraw.Draw(img)
            d.ellipse([cap_cx - gold_r, cap_cy - gold_r * 0.9, cap_cx + gold_r, cap_cy + gold_r * 0.9],
                      fill=(*GOLD, 200))

            y = block_y
            if has_attrib:
                tl.paste_tile(img, attrib_tile, block_x, y + attrib_mask[4], attrib_mask[3], attrib_mask[4], 1.0, 1.0)
                y += line_heights[0]
            # swell: a brief radial brightening centered on the cap, 0.6s
            swell = max(0.0, 1.0 - (t - press_t) / 0.6) if t < press_t + 0.6 else 0.0
            if swell > 0:
                gain = _radial_gain(x_grid, y_grid, cap_cx, cap_cy, CAP_SIZE * 1.4, 1.0 + 0.5 * swell)
                arr = np.asarray(img.convert("RGB"), dtype=np.float32) * gain[..., None]
                img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
                d = ImageDraw.Draw(img)
            tl.paste_tile(img, line1_tile, block_x, y + line1_mask[4], line1_mask[3], line1_mask[4], 1.0, 1.0)
            y += line_heights[line1_idx]
            for bi, tile in enumerate(body_tiles):
                mask = body_masks[bi]
                tl.paste_tile(img, tile, block_x, y + mask[4], mask[3], mask[4], 1.0, 1.0)
                y += line_heights[line1_idx + 1 + bi]
            if ref_tile:
                img.alpha_composite(ref_tile, (block_x, y + 6))

        Image.fromarray(np.array(img.convert("RGB"))).save(frames / f"f{i:04d}.png")

    _run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames / "f%04d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    shutil.rmtree(frames)


# ------------------------------------------------------- bespoke text layouts
# Concept A1/A2/A3 (Fable Round 10): "the layout choreography enacts the
# verse's own claim" -- built on the same proven letterpress-tile primitives
# as everything else in this file, each with its own geometry per verse.

def _make_ref_stamp(ref_text: str) -> Image.Image:
    ref_font = ImageFont.truetype(tl.F_BODY, 22)
    dummy = ImageDraw.Draw(Image.new("L", (1, 1)))
    ref_w = int(sum(dummy.textlength(ch, font=ref_font) for ch in ref_text) + 3 * (len(ref_text) - 1))
    rt_w, rt_h = max(tl.STITCH_LEN, ref_w) + 8, int(ref_font.size * 1.9) + 8
    tile = Image.new("RGBA", (rt_w, rt_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    d.line([(0, 4), (tl.STITCH_LEN, 4)], fill=(*tl.GOLD, 255), width=3)
    tl.draw_letterspaced(d, (0, 14), ref_text, ref_font, (*tl.REF_GOLD, 255), spacing=3)
    return tile


def _render_torn_veil_descend(still: Path, dest: Path, duration: float, clauses: list,
                               press_times: list, rent_bbox: list, ref_text: str, abs_start: float):
    """A1 -- Matt 27:51's own clauses descend the page beside the torn
    veil's rent, each landing lower than the last, arriving LOWEST exactly
    as the voice says "to the bottom" -- the text performs the verse's own
    doctrinal detail (torn from the TOP, God's act, not man's). The rent's
    own light breathes throughout; one swell fires at the "rent in twain"
    clause. `clauses`: [(runs, y_frac), ...]; `press_times`: local seconds."""
    src = Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS)
    src_arr = np.asarray(src, dtype=np.float32) / 255.0
    y_grid, x_grid = np.mgrid[0:H, 0:W].astype(np.float32)
    rent_cx, rent_cy, rent_r = focal_tour.focal_to_px(tuple(rent_bbox), W, H)

    sizes = sorted({sz for runs, _ in clauses for _, sz in runs})
    fonts = {sz: ImageFont.truetype(tl.F_BODY, sz) for sz in sizes}
    tiles = []
    for runs, y_frac in clauses:
        mask = tl.make_line_mask(runs, fonts)
        tile = tl.compose_pressed_tile(mask[0], tl.INK_FINAL)
        tiles.append((mask, tile, y_frac))
    ref_tile = _make_ref_stamp(ref_text) if ref_text else None

    block_x = int(0.06 * W)
    swell_t = press_times[1] if len(press_times) > 1 else None  # "rent in twain" clause
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        breath = 1.0 + 0.06 * np.sin(2 * np.pi * (t % 3.0) / 3.0)
        bright = _radial_gain(x_grid, y_grid, rent_cx, rent_cy, rent_r * 1.3, breath)
        if swell_t is not None and swell_t <= t < swell_t + 0.4:
            swell = 1.0 - (t - swell_t) / 0.4
            bright = bright * (1.0 + 0.15 * swell)
        arr = np.clip(src_arr * bright[..., None] * 255, 0, 255).astype(np.uint8)
        img = Image.fromarray(arr).convert("RGBA")

        last_y = None
        for ci, (mask, tile, y_frac) in enumerate(tiles):
            if t < press_times[ci]:
                continue
            alpha = min(1.0, (t - press_times[ci]) / 0.35)
            y = int(y_frac * H)
            mw, mh = mask[1], mask[2]
            plate = Image.new("RGBA", (mw + 36, mh + 16), (222, 208, 178, int(150 * alpha)))
            img.alpha_composite(plate, (block_x - 16, y - 8))
            tl.paste_tile(img, tile, block_x, y + mask[4], mask[3], mask[4], 1.0, alpha)
            last_y = y + mh

        if ref_tile and last_y is not None and t >= press_times[-1] + 0.3:
            img.alpha_composite(ref_tile, (block_x, last_y + 14))

        Image.fromarray(np.array(img.convert("RGB"))).save(frames / f"f{i:04d}.png")

    _run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames / "f%04d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    shutil.rmtree(frames)


def _render_east_west_edges(still: Path, dest: Path, duration: float, west_press_t: float,
                             ref_text: str, abs_start: float):
    """A2 -- Ps 103:12 presses at OPPOSITE frame edges: "As far as the east"
    left, "is from the west..." right, timed to their own real spoken
    words. The whole horizon between them IS the statement; nothing else
    moves -- no halo, no raking, just the two presses on the already-still
    landscape."""
    src = Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS)
    font = ImageFont.truetype(tl.F_BODY, RUBRIC_BODY_SIZE)
    fonts = {RUBRIC_BODY_SIZE: font}
    east_mask = tl.make_line_mask([("As far as the east", RUBRIC_BODY_SIZE)], fonts)
    east_tile = tl.compose_pressed_tile(east_mask[0], tl.INK_FINAL)
    west_mask = tl.make_line_mask([("is from the west...", RUBRIC_BODY_SIZE)], fonts)
    west_tile = tl.compose_pressed_tile(west_mask[0], tl.INK_FINAL)
    ref_tile = _make_ref_stamp(ref_text) if ref_text else None

    east_x, east_y = int(0.04 * W), int(0.42 * H)
    west_x, west_y = int(W - 0.04 * W - west_mask[1]), int(0.42 * H)

    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        img = src.convert("RGBA").copy()

        if t >= 0.0:
            alpha = min(1.0, t / 0.35)
            plate = Image.new("RGBA", (east_mask[1] + 36, east_mask[2] + 16), (222, 208, 178, int(150 * alpha)))
            img.alpha_composite(plate, (east_x - 16, east_y - 8))
            tl.paste_tile(img, east_tile, east_x, east_y + east_mask[4], east_mask[3], east_mask[4], 1.0, alpha)
        if t >= west_press_t:
            alpha = min(1.0, (t - west_press_t) / 0.35)
            plate = Image.new("RGBA", (west_mask[1] + 36, west_mask[2] + 16), (222, 208, 178, int(150 * alpha)))
            img.alpha_composite(plate, (west_x - 16, west_y - 8))
            tl.paste_tile(img, west_tile, west_x, west_y + west_mask[4], west_mask[3], west_mask[4], 1.0, alpha)
            if ref_tile and t >= west_press_t + 0.3:
                img.alpha_composite(ref_tile, (west_x, west_y + west_mask[2] + 14))

        Image.fromarray(np.array(img.convert("RGB"))).save(frames / f"f{i:04d}.png")

    _run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames / "f%04d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    shutil.rmtree(frames)


def _render_seated_settle(still: Path, dest: Path, duration: float, lead_lines: list,
                           settle_words: str, tail_line: str, glow_bbox: list,
                           settle_press_t: float, tail_press_t: float,
                           ref_text: str, abs_start: float):
    """A3 -- Heb 10:12: the opening clause presses in at t=0, then "sat
    down" (display scale) arrives with a SETTLE at its own real spoken
    moment -- not a pop, the tile descends ~12px into its baseline over
    0.35s ease-out with a paper-thump darken, text that physically sits
    down -- then the closing clause presses. A gentle breathing halo (same
    localized radial-gain primitive as the Illuminated Rubrics) sits behind
    the seated figure throughout."""
    src = Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS)
    src_arr = np.asarray(src, dtype=np.float32) / 255.0
    y_grid, x_grid = np.mgrid[0:H, 0:W].astype(np.float32)
    glow_cx, glow_cy, glow_r = focal_tour.focal_to_px(tuple(glow_bbox), W, H)
    energy = energy_envelope(ALIGNMENT, LAST_WORD_END, floor=0.25, ramp=0.15)

    body_font = ImageFont.truetype(tl.F_BODY, RUBRIC_BODY_SIZE)
    settle_font = ImageFont.truetype(tl.F_BODY, 76)
    fonts = {RUBRIC_BODY_SIZE: body_font, 76: settle_font}

    lead_masks = [tl.make_line_mask([(line, RUBRIC_BODY_SIZE)], fonts) for line in lead_lines]
    lead_tiles = [tl.compose_pressed_tile(m[0], tl.INK_FINAL) for m in lead_masks]
    settle_mask = tl.make_line_mask([(settle_words, 76)], fonts)
    settle_tile_final = tl.compose_pressed_tile(settle_mask[0], tl.INK_FINAL)
    settle_tile_dark = tl.compose_pressed_tile(settle_mask[0], tl.INK_DARK)
    tail_mask = tl.make_line_mask([(tail_line, RUBRIC_BODY_SIZE)], fonts)
    tail_tile = tl.compose_pressed_tile(tail_mask[0], tl.INK_FINAL)
    ref_tile = _make_ref_stamp(ref_text) if ref_text else None

    block_x, block_y = int(0.055 * W), int(0.035 * H)
    lead_heights = [max(int(RUBRIC_BODY_SIZE * 1.4), m[2] + 8) for m in lead_masks]
    settle_h = max(int(RUBRIC_BODY_SIZE * 1.4) + 20, settle_mask[2] + 8)

    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        e = energy(abs_start + t)
        breath = 1.0 + 0.08 * e * np.sin(2 * np.pi * (t % 4.0) / 4.0)
        bright = _radial_gain(x_grid, y_grid, glow_cx, glow_cy, glow_r * 1.2, breath)
        arr = np.clip(src_arr * bright[..., None] * 255, 0, 255).astype(np.uint8)
        img = Image.fromarray(arr).convert("RGBA")

        y = block_y
        any_shown = t >= 0.0
        if any_shown:
            max_w = max([m[1] for m in lead_masks] + [settle_mask[1], tail_mask[1]])
            plate_h = sum(lead_heights) + settle_h + int(RUBRIC_BODY_SIZE * 1.4) + 24
            plate = Image.new("RGBA", (max_w + 44, plate_h), (222, 208, 178, 165))
            img.alpha_composite(plate, (block_x - 20, block_y - 12))
            for li, tile in enumerate(lead_tiles):
                mask = lead_masks[li]
                tl.paste_tile(img, tile, block_x, y + mask[4], mask[3], mask[4], 1.0, 1.0)
                y += lead_heights[li]

        if t >= settle_press_t:
            local = t - settle_press_t
            settle_p = min(1.0, local / 0.35)
            drop = 12 * (1.0 - (1.0 - settle_p) ** 2)  # ease-out descent into baseline
            tile = settle_tile_dark if settle_p < 1.0 else settle_tile_final
            tl.paste_tile(img, tile, block_x, y + settle_mask[4] + int(drop), settle_mask[3], settle_mask[4], 1.0, 1.0)
            if local < 0.15:  # paper-thump: a brief darken flash right at landing
                thump = 1.0 - local / 0.15
                d = ImageDraw.Draw(img)
                d.rectangle([block_x - 4, y - 4, block_x + settle_mask[1] + 4, y + settle_h],
                            fill=(0, 0, 0, int(40 * thump)))
        y += settle_h

        if t >= tail_press_t:
            alpha = min(1.0, (t - tail_press_t) / 0.35)
            tl.paste_tile(img, tail_tile, block_x, y + tail_mask[4], tail_mask[3], tail_mask[4], 1.0, alpha)
            if ref_tile and t >= tail_press_t + 0.4:
                img.alpha_composite(ref_tile, (block_x, y + tail_mask[2] + 14))

        Image.fromarray(np.array(img.convert("RGB"))).save(frames / f"f{i:04d}.png")

    _run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames / "f%04d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    shutil.rmtree(frames)


# --------------------------------------------------------- redemption reprise

def _render_answer_thread_reprise(still: Path, dest: Path, duration: float, regions: list,
                                   christ_anchor: tuple, swell_time: float):
    """Concept C (Fable Round 10) -- s56_the_answer, the film's thesis image.
    Reimplements focal_tour's own chiaroscuro-reveal math (regions ignite in
    order, each staying lit -- see panel_animator/focal_tour.py's
    _render_chiaroscuro_reveal, same formula) but with `regions` REORDERED
    so Christ ignites LAST (the climax lands on Him, matching this project's
    own locked hero-bookend pattern) -- was [Christ, goat1, goat2] igniting
    Christ FIRST, silently backwards from that rule. As each goat-memory
    region ignites, its own gold thread (promoted panel_animator/
    thread_device.py, the same primitive proven on spreads 54-55) fades in
    to Christ; both threads swell once together at `swell_time` (the real
    spoken moment of "one Priest") -- two deaths of meaning, one Person,
    resolved in the film's own established redemption grammar."""
    src = Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS)
    src_arr = np.asarray(src, dtype=np.float32) / 255.0
    y_grid, x_grid = np.mgrid[0:H, 0:W].astype(np.float32)

    focal_centers = [focal_tour.focal_to_px(tuple(r["bbox"]), W, H) for r in regions]
    total_frames = max(1, int(round(duration * FPS)))
    n = len(focal_centers)
    ignition_frames = [int(total_frames * (0.10 + 0.75 * i / max(n - 1, 1))) for i in range(n)]
    ramp_frames = max(1, int(total_frames * 0.12))
    masks = []
    for cx, cy, r in focal_centers:
        sigma = max(r * 0.55, 1.0)
        masks.append(np.exp(-((x_grid - cx) ** 2 + (y_grid - cy) ** 2) / (2.0 * sigma ** 2)))

    thread1 = thread_device.make_thread_layer(W, H, focal_centers_frac(regions[0]["bbox"]), christ_anchor,
                                                thread_device.GOLD)
    thread1_bright = thread_device.make_thread_layer(W, H, focal_centers_frac(regions[0]["bbox"]), christ_anchor,
                                                       thread_device.GOLD_BRIGHT)
    thread2 = thread_device.make_thread_layer(W, H, focal_centers_frac(regions[1]["bbox"]), christ_anchor,
                                                thread_device.GOLD)
    thread2_bright = thread_device.make_thread_layer(W, H, focal_centers_frac(regions[1]["bbox"]), christ_anchor,
                                                       thread_device.GOLD_BRIGHT)
    thread1_start = ignition_frames[0] / FPS
    thread2_start = ignition_frames[1] / FPS
    thread_fade = 1.0

    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for f in range(total_frames):
        t = f / FPS
        lit = np.zeros((H, W), dtype=np.float32)
        for i in range(n):
            if f < ignition_frames[i]:
                continue
            amt = focal_tour.smoothstep((f - ignition_frames[i]) / ramp_frames)
            lit = np.maximum(lit, masks[i] * amt)
        bright = focal_tour._CHIARO_BASE_DIM + (1.0 - focal_tour._CHIARO_BASE_DIM) * lit
        frame_arr = np.clip(src_arr * bright[..., None] * 255, 0, 255).astype(np.uint8)
        img = Image.fromarray(frame_arr).convert("RGBA")

        swell = thread_device.thread_swell(t, swell_time)
        for th_start, layer, layer_bright in ((thread1_start, thread1, thread1_bright),
                                                (thread2_start, thread2, thread2_bright)):
            op = thread_device.thread_opacity(t, th_start, thread_fade)
            if op > 0:
                l = layer if op >= 1.0 else Image.blend(Image.new("RGBA", layer.size, (0, 0, 0, 0)), layer, op)
                if swell > 0:
                    l = Image.blend(l, layer_bright, swell * 0.6)
                img.alpha_composite(l)

        Image.fromarray(np.array(img.convert("RGB"))).save(frames / f"f{f:04d}.png")

    _run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames / "f%04d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    shutil.rmtree(frames)


def focal_centers_frac(bbox: list) -> tuple:
    """bbox is [x%,y%,w%,h%] -- the thread anchors on the region's own
    CENTER point, as a (0..1, 0..1) fraction pair (make_thread_layer's own
    p0_frac/p1_frac convention)."""
    x, y, w, h = bbox
    return ((x + w / 2) / 100.0, (y + h / 2) / 100.0)


# --------------------------------------------------------------------- dispatch

def render_device(device: str, still: Path, dest: Path, duration: float, **params):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if device == "locked_plate_parallax":
        # Round 10 bugfix: parallax_25d.render() outputs at the STILL's own
        # native resolution (e.g. 2752x1536), never scaled to this film's
        # 1920x1080 -- every other device wrapper in this file scale-crops
        # internally, this was the one silent passthrough. Only surfaced now
        # because the new edge-darken ramp builds a fixed (H,W) grid and
        # crashed on the mismatch; the gold-in ramp's per-CHANNEL multiply
        # broadcasts fine at any resolution so it silently "worked" at the
        # wrong size. Always normalize now, for every parallax call, not
        # just the ramped ones -- this affects all locked_plate_parallax
        # spreads, not only s51/s53.
        raw = dest.parent / (dest.stem + "_prawnorm.mp4")
        parallax_25d.render(still, raw, duration,
                             fg_amp=params.get("fg_amp", 6.0), bg_amp=params.get("bg_amp", 0.0))
        normed = dest.parent / (dest.stem + "_preramp.mp4") if (params.get("edge_darken")
                                                                 or params.get("gold_in")) else dest
        _run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-vf",
              f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
              "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(normed)])
        raw.unlink(missing_ok=True)
        if params.get("edge_darken"):
            _apply_edge_darken_ramp(normed, dest, target_edge_gain=params.get("target_edge_gain", 0.72))
            normed.unlink(missing_ok=True)
        elif params.get("gold_in"):
            _apply_warm_goldin_ramp(normed, dest, ramp_duration=params.get("ramp_duration", 3.0),
                                     boost=params.get("boost", 0.12))
            normed.unlink(missing_ok=True)
    elif device == "registration_snap":
        registration_snap.render(still, dest, duration)
    elif device == "palette_pivot":
        palette_pivot.render(still, dest, duration)
    elif device == "crop_mark_approval":
        crop_mark_approval.render(still, dest, duration)
    elif device == "letterpress_beat":
        beats = letterpress_beat.beats_in_window(ALIGNMENT, params["abs_start"],
                                                  params["abs_start"] + duration, letterpress_beat.MIN_SPACING)
        letterpress_beat.render(still, dest, duration, beats)
    elif device == "ink_up_build":
        regions = params.get("regions") or [{"bbox": [38, 8, 24, 30]}, {"bbox": [8, 60, 20, 28]},
                                             {"bbox": [72, 60, 20, 28]}]
        ink_up_build.render(still, regions, dest, duration,
                             initial_hold_frac=params.get("initial_hold_frac", 0.10),
                             final_hold_frac=params.get("final_hold_frac", 0.10))
    elif device == "raking_light":
        _raking_light(still, dest, duration, flare=params.get("flare", False),
                      energy_amp=params.get("energy_amp", False), abs_start=params.get("abs_start", 0.0),
                      hush_decay=params.get("hush_decay", False))
    elif device == "plain_static":
        _plain_static(still, dest, duration)
    elif device == "breath_synced_halo":
        _breath_synced_halo(still, dest, duration, params["bbox"], params["abs_start"])
    elif device in ("chiaroscuro_reveal", "desat_focus"):
        regions = params["regions"] if "regions" in params else [{"bbox": params["bbox"]}]
        focal_tour.render_clip(still, regions, device, duration, W, H, dest)
    elif device in ("dramatic_spotlight", "caravaggio_pulse"):
        _spotlight_family(device, still, dest, duration, params["bbox"])
    elif device == "line_boil":
        _line_boil_still(still, dest, duration, amount=params.get("amount", 0.6))
    elif device == "candle_only":
        _candle_only_still(still, dest, duration, params["anchor_frac"])
    elif device == "answer_thread_reprise":
        _render_answer_thread_reprise(still, dest, duration, params["regions"],
                                       params["christ_anchor"], params["swell_time"])
    else:
        raise ValueError(f"unknown device {device!r}")


def render_verse_card(name: str, still: Path, dest: Path, duration: float, abs_start: float):
    dest.parent.mkdir(parents=True, exist_ok=True)
    card = VERSE_CARDS[name]
    combo.LINES = card["lines"]  # module-global override -- combo module's own
    # _build_line_tiles()/render_combo_* all resolve LINES by name at call
    # time, so reassigning it here before calling is sufficient (no need to
    # edit _poc_motion_text_combo.py itself; calls are sequential, not
    # concurrent, in this pipeline).
    if card["combo"] == "A":
        combo.render_combo_a(still, dest, duration, abs_start=abs_start)
    elif card["combo"] == "B":
        combo.render_combo_b(still, dest, duration, abs_start=abs_start)
    else:
        beats = letterpress_beat.beats_in_window(ALIGNMENT, abs_start, abs_start + duration,
                                                  letterpress_beat.MIN_SPACING)
        combo.render_combo_c(still, dest, duration, beats)


# ============================================================ ASSIGNMENT TABLES

# RESUME.md handover section 3 -- 21 held/no-camera-move spreads. "scope" is
# derived from _s5b_spread_windows.py's own DETERMINISTIC set (no real clip
# -> "full"; everything else -> "tail", replacing only the generic push/arc
# fwd_drift tail). bbox/regions for face- or element-anchored devices were
# picked by eye against the actual rendered still (2026-08-06).
DEVICE_ASSIGNMENTS = {
    # -- Locked-Plate Parallax (fg drifts, bg locked -- reads as camera-free) --
    "s51_jesus_pivot": {"device": "locked_plate_parallax", "scope": "full",
                         "params": {"fg_amp": 9.0, "bg_amp": 0.0, "gold_in": True, "ramp_duration": 3.0,
                                    "boost": 0.12}},
    # Round 10: fg_amp 6->9 + the gold register the still already carries
    # arrives WITH Him over the first 3s (the plan's own "gold-leaf arrival"
    # device column note, never built until now)
    "s05_walking_to_veil": {"device": "locked_plate_parallax", "scope": "full",
                             "params": {"fg_amp": 6.0, "bg_amp": 0.0}},
    "s53_the_cross": {"device": "locked_plate_parallax", "scope": "full",
                       "params": {"fg_amp": 6.0, "bg_amp": 0.0, "edge_darken": True, "target_edge_gain": 0.72}},
    # Round 10: Passion-Vigil register -- the world darkens around Him while
    # He stays lit; restrained, no pulse, reverence cap
    "s26_through_veil_stage2": {"device": "locked_plate_parallax", "scope": "full",
                                 "params": {"fg_amp": 6.0, "bg_amp": 0.0}},

    # -- Raking Light (cards/objects, no wobble/no flare, fully legible) --
    # s60/s63/s52 REBUILD deferred to Concept B/A verse-card registers (Fable
    # Round 10) -- their entries live further down once rebuilt.
    # Round 10 fixes (2026-08-06): motion_lint FROZEN-SPREAD FAILs, Raking
    # Light demoted from lazy zero-bbox default to its 3 legitimate spots.
    "s25_slaying_stage1": {"device": "dramatic_spotlight", "scope": "full",
                            "params": {"bbox": [40, 3, 35, 40]}},  # raised knife + Aaron's hands
    "s27_sprinkling": {"device": "breath_synced_halo", "scope": "full",
                        "params": {"bbox": [40, 15, 25, 32]}},  # the cloud-glow above the mercy seat
    "s50_the_shadow": {"device": "breath_synced_halo", "scope": "full",
                        "params": {"bbox": [17, 78, 20, 20]}},  # wash_creep re-anchor tested NOT viable
    # (isolate_storm_wash's blue-grey HSV band caught 0.5% of this warm-toned
    # ink shadow -- not a storm wash, the mask is essentially empty). The
    # shadow's own broad/origin end breathes instead: "a shadow waits for
    # the body that casts it."
    # specially-named VC cards (RESUME §2): s16 now built for real (see
    # SPECIAL_CARDS below) -- entry removed here so it doesn't poison the
    # lint's device-quota stats. s31/s49 bespoke builds still deferred,
    # raking light is the safe interim placeholder that just removes the
    # camera push until they're built too.
    "s31_confession_card": {"device": "raking_light", "scope": "tail", "params": {}},
    "s49_veil_detail_card": {"device": "raking_light", "scope": "tail", "params": {}},

    # -- Landing: plain static hold, sacred stillness, not a placeholder --
    "s76_already_inside": {"device": "plain_static", "scope": "full", "params": {},
                            "stillness_authored": True},  # sacred-stillness landing, exempt from motion_lint

    # -- Registration Snap (thematically apt for s47's own "halftone/print" idea) --
    "s47_light_arrives": {"device": "registration_snap", "scope": "tail", "params": {}},

    # -- Ink-Up Build (MV multi-vignette spreads) --
    "s34_riddle_recap": {"device": "ink_up_build", "scope": "full",
                          "params": {"initial_hold_frac": 0.05, "final_hold_frac": 0.20}},
    "s57_without_the_gate": {"device": "ink_up_build", "scope": "full",
                              "params": {"initial_hold_frac": 0.05, "final_hold_frac": 0.20}},
    # Round 10: re-weighted so the last vignette's arrival+settle stretches
    # later into the window (final_hold_frac 0.10->0.20, initial_hold_frac
    # 0.10->0.05) rather than resting on the "full" composition early.

    # -- Chiaroscuro Reveal (already tested on this exact multi-figure spread) --
    "s56_the_answer": {"device": "answer_thread_reprise", "scope": "full",
                        "params": {
                            # Round 10 Concept C: regions REORDERED so Christ
                            # ignites LAST (was [Christ, goat1, goat2] --
                            # Christ igniting FIRST silently broke this
                            # project's own locked hero-bookend/climax-lands-
                            # on-Christ pattern).
                            "regions": [{"bbox": [8, 60, 20, 28]}, {"bbox": [72, 60, 20, 28]},
                                        {"bbox": [38, 8, 24, 30]}],
                            "christ_anchor": (0.50, 0.55),
                            # real word-matched local swell time (abs_start=
                            # 415.691, alignment-verified: "one" at
                            # 425.20->local 9.51, "Priest." at 425.49)
                            "swell_time": 9.51,
                        }},

    # -- spotlight family (portrait/close-face) --
    "s66_high_priests_face": {"device": "caravaggio_pulse", "scope": "full", "params": {"bbox": [30, 15, 40, 45]}},
    "s43_shadow_on_tent_wall": {"device": "candle_only", "scope": "tail",
                                 "params": {"anchor_frac": (0.50, 0.87)}},
    # Round 10: upgraded from the dramatic_spotlight PLACEHOLDER to the real
    # device -- the plan's own "literal design case" for this beat, now that
    # candle_only exists as a real device slot here. Anchor derived from the
    # original placeholder bbox's center [42,78,16,18].

    # -- Breath-Synced Halo (held-breath quiet points + the 2 explicit picks) --
    "s74_every_year_gone": {"device": "breath_synced_halo", "scope": "tail", "params": {"bbox": [35, 8, 30, 42]}},
    "s04_donning_linen": {"device": "breath_synced_halo", "scope": "tail", "params": {"bbox": [36, 3, 24, 35]}},
    "s45_sign_before_veil": {"device": "breath_synced_halo", "scope": "full", "params": {"bbox": [44, 78, 12, 20]}},
    "s64_empty_hands": {"device": "breath_synced_halo", "scope": "tail", "params": {"bbox": [38, 25, 24, 45]}},

    # -- RESUME.md handover section 4 -- the remaining ~50 "plain" NS/MV
    # spreads (39 in practice; 5 are the acting/already-built exceptions
    # left untouched, 32 already covered above by section 2/3). Rotated by
    # content type read off the spread's own name (all scope="tail" -- none
    # of these are in the no-clip DETERMINISTIC set, so the device only
    # replaces the generic push/arc tail after the real clip plays; 3 of the
    # 39 -- s09/s10/s11 -- already resolve to once_trim/once_hold with no
    # tail at all, so their entry here is a documented no-op, not a bug).
    #
    # Portrait/close-face, direct address or contemplative -- spotlight
    # family rotated 3 ways + one Plain Static, bboxes eye-checked per still.
    "s09_grief_close": {"device": "dramatic_spotlight", "scope": "tail", "params": {"bbox": [35, 25, 32, 40]}},
    "s18_own_sin_first": {"device": "caravaggio_pulse", "scope": "tail", "params": {"bbox": [48, 5, 22, 42]}},
    "s30_confession": {"device": "breath_synced_halo", "scope": "tail", "params": {"bbox": [35, 3, 32, 38]}},
    "s39_honesty_close": {"device": "plain_static", "scope": "tail", "params": {}},
    # Object/prop/veil close-ups -- Raking Light (legible lamp sweep) or
    # Locked-Plate Parallax where there's a clean fg/bg depth split; Ink-Up
    # Build where 2+ named sub-elements share the frame.
    "s03_golden_garments": {"device": "raking_light", "scope": "tail", "params": {"flare": True}},
    # the subject IS gold -- spends the episode's ONE flare budget here (see
    # DEV.render_device's raking_light flare support, Round 10)
    "s08_curtain_shut": {"device": "caravaggio_pulse", "scope": "tail", "params": {"bbox": [30, 10, 30, 55]}},
    "s13_door_curtain_sl13": {"device": "dramatic_spotlight", "scope": "tail",
                               "params": {"bbox": [55, 48, 15, 22]}},  # the gripping hand at the curtain
    "s19_altar_ministry": {"device": "chiaroscuro_reveal", "scope": "tail",
                            "params": {"regions": [{"bbox": [35, 55, 25, 35]}, {"bbox": [15, 15, 20, 55]},
                                                    {"bbox": [62, 5, 20, 20]}]}},
    # order: altar base -> Aaron -> smoke tip LAST, handing the eye to the
    # existing through_object_cut into s20 which opens at the SAME point
    # (0.72,0.12) -- corrected from an earlier session's (0.30,0.10), which
    # was blank sky in the real still, not the smoke at all (see
    # TRANSITION_OVERRIDES fix below)
    "s21_goat_innocent": {"device": "line_boil", "scope": "tail", "params": {}},  # hand-inked life, not a lamp
    "s42_basin_linen_ready": {"device": "raking_light", "scope": "tail",
                               "params": {"energy_amp": True}},  # proven exact test spread;
    # Round 10 pairing: sweep strength now tracks this episode's own
    # held-breath energy envelope, so the light visibly quiets with the
    # narrator instead of a flat mechanical sweep (Pairing Law, sec 3b)
    "s44_pointing_smoke": {"device": "raking_light", "scope": "tail", "params": {}},
    "s46_aged_unchanged_veil": {"device": "desat_focus", "scope": "tail", "params": {"bbox": [66, 30, 20, 35]}},
    # "I did not see the answer in my own day" -- colour drains from his day
    # while his aged face holds it
    "s59_no_chair": {"device": "chiaroscuro_reveal", "scope": "full",
                      "params": {"regions": [{"bbox": [43, 50, 20, 35]}, {"bbox": [65, 67, 15, 27]},
                                              {"bbox": [30, 25, 15, 72]}]}},
    # ark -> the EMPTY floor beside it -> Aaron -- lighting an empty patch of
    # floor is the beat; there was no chair
    "s61_veil_recall": {"device": "raking_light", "scope": "tail", "params": {"hush_decay": True}},
    # Round 10 pairing: the page goes DEAD STILL over the final ~1.2s, right
    # before the mandatory hard cut into s62 (the tear) -- stillness that
    # ARRIVES reads as intent, not a freeze; the film's held breath before
    # the tear.
    "s36_two_shadows_one_flame": {"device": "caravaggio_pulse", "scope": "tail", "params": {"bbox": [66, 55, 12, 15]}},
    # the LIT LAMP on the table (Aaron's hands are clasped/empty in the real
    # still -- not "in Aaron's hand" as first assumed)
    # s11_struck_down entry DELETED (Round 10): raking_light was assigned but
    # never fires -- the real clip already fills this spread's window, no
    # tail exists to carry a device. Dead entry was poisoning the device-
    # share quota stats the lint counts against.
    "s14_hand_at_veil": {"device": "ink_up_build", "scope": "tail", "params": {}},
    "s22_ritual_hands": {"device": "ink_up_build", "scope": "tail", "params": {}},
    "s37_split_two_things": {"device": "ink_up_build", "scope": "tail", "params": {}},
    "s23_two_goats_brought": {"device": "ink_up_build", "scope": "tail",
                               "params": {"regions": [{"bbox": [10, 40, 35, 50]}, {"bbox": [55, 40, 35, 50]}]}},
    "s48_small_basin_towering_veil": {"device": "locked_plate_parallax", "scope": "tail",
                                       "params": {"fg_amp": 6.0, "bg_amp": 0.0}},
    "s70_veil_held_open": {"device": "locked_plate_parallax", "scope": "tail",
                            "params": {"fg_amp": 6.0, "bg_amp": 0.0}},
    # Action/movement moments -- Locked-Plate Parallax (fg drifts, camera-free)
    # s10/s12/s15 moved OFF parallax (Round 10 quota trim: parallax sat at
    # 13/76=17.1%, over the 15% FAIL threshold) to better content fits:
    "s10_strange_fire": {"device": "caravaggio_pulse", "scope": "tail", "params": {"bbox": [25, 45, 35, 20]}},
    # both censers together -- fire that pulses
    "s12_bodies_carried_out": {"device": "desat_focus", "scope": "tail", "params": {"bbox": [42, 15, 38, 75]}},
    # the two bearers -- the colour of the day drains as the dead leave camp
    "s15_moses_charge": {"device": "line_boil", "scope": "tail", "params": {}},
    # two old brothers holding still; hand-inked life, no lamp
    "s17_squared_at_veil": {"device": "locked_plate_parallax", "scope": "tail",
                             "params": {"fg_amp": 6.0, "bg_amp": 0.0}},
    "s32_goat_led_away": {"device": "locked_plate_parallax", "scope": "tail", "params": {"fg_amp": 6.0, "bg_amp": 0.0}},
    "s62_veil_torn": {"device": "locked_plate_parallax", "scope": "tail", "params": {"fg_amp": 6.0, "bg_amp": 0.0}},
    "s73_aaron_steps_aside": {"device": "locked_plate_parallax", "scope": "tail",
                               "params": {"fg_amp": 6.0, "bg_amp": 0.0}},
    # Landscape/wide -- East/West Palette Pivot, rotate
    "s02_tabernacle_wide": {"device": "palette_pivot", "scope": "tail", "params": {}},
    "s06_holy_of_holies_empty": {"device": "palette_pivot", "scope": "tail", "params": {}},
    "s07_nation_outside": {"device": "palette_pivot", "scope": "tail", "params": {}},
    "s38_walking_home_dusk": {"device": "palette_pivot", "scope": "tail", "params": {}},
    "s40_people_home_clean": {"device": "palette_pivot", "scope": "tail", "params": {}},
    "s67_same_road_lit": {"device": "palette_pivot", "scope": "tail", "params": {}},
    "s68_east_west_horizon": {"device": "palette_pivot", "scope": "tail", "params": {}},  # proven exact test spread
    "s71_the_way_open": {"device": "palette_pivot", "scope": "tail", "params": {}},
    # MV multi-vignette -- custom regions picked against the actual composition
    "s41_repetition_vignettes": {"device": "ink_up_build", "scope": "tail",
                                  "params": {"regions": [{"bbox": [15, 10, 25, 32]}, {"bbox": [5, 48, 28, 48]},
                                                          {"bbox": [30, 28, 32, 58]}, {"bbox": [63, 3, 33, 52]}]}},
    "s65_ritual_uninks": {"device": "chiaroscuro_reveal", "scope": "tail",
                           "params": {"regions": [{"bbox": [8, 45, 25, 42]}, {"bbox": [28, 25, 20, 45]},
                                                   {"bbox": [55, 3, 42, 90]}]}},
}

# RESUME.md handover section 2 -- the 8 "plain" verse-card spreads. Text is
# the exact _PLAN.md on-screen excerpt (KJV-verbatim, not the full verse).
# Combo device rotated A/B/C across the 8 for variety. s24 was already built
# in the round-4 POC (Lev 16:8) -- kept, not re-authored, just wired in here.
# Round 10 A0: lines are now run-lists [(text, size), ...] wherever a LAW-2
# display-scale key word (~2x BODY_SIZE=40 -> 80) applies -- a plain string
# still works (single run at BODY_SIZE), kept where no single word carries
# the beat. Every key word/phrase below was verified against the real
# narration transcript in this card's own window before picking it (not
# guessed) -- see _FABLE_ROUND10...md sec 2 Concept A0.2. s24/s72's display
# words echo the SAME words the s20->s21/s72->s73 verse_mask_reveal
# transitions open through, tying card and cut together.
VERSE_CARDS = {
    "s20_blood_atonement_card": {"combo": "A",
                                  "lines": [[("for it is the ", BODY_SIZE), ("blood", 80)],
                                            [("that maketh an atonement", BODY_SIZE)],
                                            [("for the soul.", BODY_SIZE)]]},
    "s24_lots_card": {"combo": "B",
                       "lines": [[("And Aaron shall cast lots", BODY_SIZE)],
                                 [("upon the two goats;", BODY_SIZE)],
                                 [("one lot for the ", BODY_SIZE), ("LORD", 70), (",", BODY_SIZE)],
                                 [("and the other lot for the ", BODY_SIZE), ("scapegoat", 60), (".", BODY_SIZE)]]},
    "s28_bring_blood_card": {"combo": "C",
                              "lines": [[("...bring his blood", BODY_SIZE)],
                                        [("within the ", BODY_SIZE), ("vail.", 80)]]},
    "s33_empty_horizon_card": {"combo": "A",
                                "lines": [[("...unto a land", BODY_SIZE)],
                                          [("not inhabited.", 80)]]},
    "s35_two_kids_card": {"combo": "B",
                           "lines": [[("...", BODY_SIZE), ("two kids", 80), (" of the goats", BODY_SIZE)],
                                     [("for a sin offering.", BODY_SIZE)]]},
    "s58_gate_card": {"combo": "C",
                       "lines": [[("...suffered without", BODY_SIZE)],
                                 [("the gate.", 80)]]},
    # s69 entry removed -- replaced by the bespoke A2 layout (opposite-
    # frame-edge presses) in SPECIAL_CARDS below.
    "s72_boldness_card": {"combo": "B",
                           "lines": [[("...", BODY_SIZE), ("boldness", 80), (" to enter", BODY_SIZE)],
                                     [("into the holiest by", BODY_SIZE)],
                                     [("the blood of Jesus.", BODY_SIZE)]]},
    # explicitly deferred (RESUME.md 2026-08-06/07): still on the raking_light
    # placeholder from the original rollout, not yet given a real bespoke
    # register (Scribed-Ink live-write for s31, stacked double-verse for s49
    # -- both specced in Fable's Round 10 doc, Concept B). Registered here
    # (not just left unlisted) so poc_living_sketchbook/_layer_check.py
    # reports an explicit WARN instead of silently missing the gap.
    "s31_confession_card": {"deferred": True},
    "s49_veil_detail_card": {"deferred": True},
}

# spreads whose real lettering is built by a standalone script outside the
# normal VERSE_CARDS/SPECIAL_CARDS dispatch -- e.g. spread55_isaiah536, built
# by _s3_thread_leaf_54_55.py's Elder Leaf compositing pass. Checked by
# poc_living_sketchbook/_layer_check.py so these don't false-FAIL.
EXTERNAL_LETTERING = {"spread55_isaiah536"}


# Concept B special cards -- don't fit combo A/B/C, dispatch separately.
# KJV text verified verbatim against data/kjv_cache.json. glow_bbox is the
# still's own drawn cloud-glow (eye-checked per card before picking).
SPECIAL_CARDS = {
    "s16_lords_charge_card": {
        "kind": "illuminated_rubric",
        "glow_bbox": [39, 18, 34, 38],
        "attribution": "And the LORD said unto Moses,",
        "cap_letter": "S", "first_line_rest": "peak unto Aaron thy brother,",
        "body_lines": ["that he come not at all times",
                        "into the holy place within the vail",
                        "before the mercy seat, which is upon the ark;",
                        "that he die not: for I will appear",
                        "in the cloud upon the mercy seat."],
    },
    "s52_jesus_entering_formal": {
        "kind": "illuminated_rubric",
        # the light-ray burst at Christ's feet (a real drawn light source in
        # this still, unlike s16's cloud -- there's no separate glow blob
        # here, the whole doorway is gold-lit, but the rays at his feet are
        # the one element that reads as an actual light SOURCE to breathe)
        "glow_bbox": [38, 74, 20, 20],
        "attribution": "",  # no natural "X said" frame -- Heb 9:12 opens mid-clause
        "cap_letter": "N", "first_line_rest": "either by the blood of goats and calves,",
        "body_lines": ["but by his own blood he entered in once",
                        "into the holy place,",
                        "having obtained eternal redemption for us."],
        "body_color": tl.INK_FINAL,  # NOT red-letter -- Hebrews narrating
        # about Christ's action, not Christ's own first-person speech (this
        # project's locked red-letter rule)
        "ref_text": "HEBREWS 9:12",
        "press_t": 1.2, "raking_t": 6.0,
    },
    "s63_torn_veil_card": {
        "kind": "torn_veil_descend",
        "rent_bbox": [42, 15, 20, 75],  # the vertical light-rent running through frame center
        "clauses": [
            ([("...the veil of the temple", RUBRIC_BODY_SIZE)], 0.10),
            ([("was ", RUBRIC_BODY_SIZE), ("rent in twain", 64)], 0.35),
            ([("from the top", RUBRIC_BODY_SIZE)], 0.58),
            ([("to the bottom.", RUBRIC_BODY_SIZE)], 0.80),  # lands LOWEST -- the verse's own claim
        ],
        # real word-matched local press times (abs_start=475.77, alignment-
        # verified against the actual narration transcript, not guessed)
        "press_times": [1.49, 2.96, 4.74, 5.64],
        "ref_text": "MATTHEW 27:51",
    },
    "s69_east_west_card": {
        "kind": "east_west_edges",
        # real word-matched local press time for "is" (abs_start=526.206,
        # alignment-verified: "As" at 526.21->local 0.00, "is" at
        # 527.47->local 1.26)
        "west_press_t": 1.26,
        # deliberate stillness (Fable Round 10 A2 spec): "no halo, no
        # raking, just the two presses on the already-still landscape --
        # the whole horizon IS the statement; nothing else moves." Motion
        # lint scored this p95=0.099, a hair under T_frozen(card)=0.1 --
        # that's the two presses' own quiet amplitude, not a defect; adding
        # unwanted motion here would contradict the card's own design.
        "stillness_authored": True,
        "ref_text": "PSALM 103:12",
    },
    "s60_seated_glory": {
        "kind": "seated_settle",
        "glow_bbox": [30, 4, 40, 45],  # the light rays behind His head/shoulders
        "lead_lines": ["But this man, after he had offered", "one sacrifice for sins for ever,"],
        "settle_words": "sat down",
        "tail_line": "on the right hand of God.",
        # real word-matched local press times (abs_start=454.033, alignment-
        # verified: "sat" at 459.18->local 5.15, "on" at 460.02->local 5.99)
        "settle_press_t": 5.15, "tail_press_t": 5.99,
        "ref_text": "HEBREWS 10:12",
    },
}


def render_special_card(name: str, still: Path, dest: Path, duration: float, abs_start: float):
    card = SPECIAL_CARDS[name]
    dest.parent.mkdir(parents=True, exist_ok=True)
    if card["kind"] == "illuminated_rubric":
        _render_illuminated_rubric(still, dest, duration, card["glow_bbox"], card["cap_letter"],
                                    card["first_line_rest"], card["body_lines"], card["attribution"],
                                    abs_start, press_t=card.get("press_t", 1.5), raking_t=card.get("raking_t", 9.0),
                                    body_color=card.get("body_color"), ref_text=card.get("ref_text"))
    elif card["kind"] == "torn_veil_descend":
        _render_torn_veil_descend(still, dest, duration, card["clauses"], card["press_times"],
                                   card["rent_bbox"], card.get("ref_text"), abs_start)
    elif card["kind"] == "east_west_edges":
        _render_east_west_edges(still, dest, duration, card["west_press_t"], card.get("ref_text"), abs_start)
    elif card["kind"] == "seated_settle":
        _render_seated_settle(still, dest, duration, card["lead_lines"], card["settle_words"],
                               card["tail_line"], card["glow_bbox"], card["settle_press_t"],
                               card["tail_press_t"], card.get("ref_text"), abs_start)
    else:
        raise ValueError(f"unknown special-card kind {card['kind']!r}")


# ================================================================ TRANSITIONS

# RESUME.md handover section 5 -- ~75 cuts total. Unseen Hand is the default
# workhorse (nearly invisible, per the design panel's own recommendation) for
# every ordinary cut; only 3 kinds of seam get something else:
#   1. NO_TRANSITION_SEAMS -- the 3 mandatory multi-stage hard-cut PAIRS
#      (_PLAN.md's own "the cut tells the event, never a morph" rule) --
#      stay a pure hard cut, no device of any kind.
#   2. TRANSITION_OVERRIDES -- a handful of genuinely apt word/scene or
#      object/scene pairs (Verse-Mask Reveal, Through-the-Object Cut) plus
#      the 6 beat-change boundaries, which get a slightly more noticeable
#      device for pacing variety (Leaf-Flick / Tipped-In Plate / ink-bleed
#      blot), rotated, not evenly distributed by formula.
#   3. everything else -> DEFAULT_TRANSITION ("unseen_hand"), applied by
#      _s6_assemble.py's concat step for any seam not listed in either set
#      above.
#
# All 2-clip devices (unseen_hand/leaf_flick/tipped_in_plate/ink_transition)
# read the real tail of clip A and real head of clip B out of the FULL
# segment files themselves -- the caller (concat step) trims `duration/2` off
# the end of A's segment and `duration/2` off the start of B's segment so the
# transition clip exactly fills that gap and total film duration (and every
# later seam's absolute timing / narration sync) is UNCHANGED. The 2-still
# devices (verse_mask_reveal/through_object_cut) build a wholly new clip from
# the two stills instead of sampling the real clips -- same trim convention
# applies around them.

DEFAULT_TRANSITION = {"device": "unseen_hand", "duration": 0.7, "params": {}}

NO_TRANSITION_SEAMS = {
    ("s10_strange_fire", "s11_struck_down"),
    ("s25_slaying_stage1", "s26_through_veil_stage2"),
    ("s26_through_veil_stage2", "s27_sprinkling"),
    ("s61_veil_recall", "s62_veil_torn"),
}

TRANSITION_OVERRIDES = {
    # -- already-tested exact pairs (RESUME.md section 5) --
    ("s20_blood_atonement_card", "s21_goat_innocent"):
        {"device": "verse_mask_reveal", "duration": 3.2,
         "params": {"word": "BLOOD", "word_x": 0.30, "word_y": 0.04}},
    ("s44_pointing_smoke", "s45_sign_before_veil"):
        {"device": "through_object_cut", "duration": 1.6, "params": {"center": (0.55, 0.15)}},
    # -- second candidates RESUME suggested checking, both genuinely apt --
    ("s19_altar_ministry", "s20_blood_atonement_card"):
        {"device": "through_object_cut", "duration": 1.6, "params": {"center": (0.72, 0.12)}},
    # Round 10 fix: was (0.30,0.10), which is blank sky in the real still --
    # the smoke actually billows upper-RIGHT, not upper-left (verified
    # against the rendered still, not re-derived from the earlier guess).
    # s19's own chiaroscuro_reveal now tours to this SAME point last, so the
    # halo hands the eye to the cut.
    ("s72_boldness_card", "s73_aaron_steps_aside"):
        {"device": "verse_mask_reveal", "duration": 3.2,
         "params": {"word": "BOLDNESS", "word_x": 0.30, "word_y": 0.04}},
    # -- the 6 beat-change boundaries, rotated for pacing variety --
    ("s08_curtain_shut", "s09_grief_close"): {"device": "leaf_flick", "duration": 0.32, "params": {}},
    ("s21_goat_innocent", "s22_ritual_hands"): {"device": "tipped_in_plate", "duration": 0.6, "params": {}},
    ("s33_empty_horizon_card", "s34_riddle_recap"):
        {"device": "ink_transition", "duration": 0.9, "params": {"mode": "blot", "origin": (0.5, 0.5)}},
    ("s38_walking_home_dusk", "s39_honesty_close"): {"device": "leaf_flick", "duration": 0.32, "params": {}},
    ("s45_sign_before_veil", "s46_aged_unchanged_veil"): {"device": "tipped_in_plate", "duration": 0.6, "params": {}},
    ("s63_torn_veil_card", "s64_empty_hands"): {"device": "tipped_in_plate", "duration": 0.6, "params": {}},

    # -- Round 10 motion-cliff audit: s04 is a real Kling clip (p95~80),
    # cutting into s05's genuinely subtle parallax drift (deliberately left
    # unamplified per Fable's disposition table -- "above the frozen band,
    # leave"). No arrival event exists on the s05 side to bridge the gap
    # (parallax has no press/settle moment), so the transition itself
    # carries the motion instead, per the cliff rule's option 2. The other
    # two cliffs the lint flagged (s49->s50, s68->s69) are resolved without
    # a transition change: s50 now has real breathing motion after its
    # Task-9 device fix was actually rebuilt (was stale before), and s69
    # has its own arrival event (the "As far as the east" press) inside the
    # first 1.5s, satisfying option 1.
    ("s04_donning_linen", "s05_walking_to_veil"): {"device": "leaf_flick", "duration": 0.32, "params": {}},
}


def render_transition(device: str, a_path: Path, b_path: Path, dest: Path, duration: float, **params):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if device == "unseen_hand":
        unseen_hand.render(a_path, b_path, dest, duration=duration)
    elif device == "leaf_flick":
        leaf_flick.render(a_path, b_path, dest, duration=duration)
    elif device == "tipped_in_plate":
        tipped_in_plate.render(a_path, b_path, dest, duration=duration)
    elif device == "ink_transition":
        ink_transition.render(a_path, b_path, dest, duration, mode=params.get("mode", "blot"),
                               origin=params.get("origin", (0.5, 0.5)), fps=FPS)
    elif device == "verse_mask_reveal":
        verse_mask_reveal.render(a_path, b_path, dest, params["word"], params["word_x"], params["word_y"])
    elif device == "through_object_cut":
        through_object_cut.render(a_path, b_path, dest, params["center"], duration=duration)
    else:
        raise ValueError(f"unknown transition device {device!r}")
