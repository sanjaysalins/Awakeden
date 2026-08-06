"""POC (2026-08-05, round 4): combine the 3 motion-design treatments the user
picked (Registration Snap, Ink-Up Build, Letterpress Beat) with the REAL
verse lettering a verse-card spread actually needs -- per the user's own
correction: "we use motion design along with the narrative text... not just
for the animation part... combine text and other cool creative things."
Round 3 animated the ART; this round makes the TEXT arrival itself part of
each device's own beat, using this project's own proven letterpress-verse
rendering (reused, not reinvented, from _s3_thread_leaf_54_55.py's
make_line_mask/compose_pressed_tile/paste_tile -- the same pressed-ink verse
technique already approved on spreads 54-55).

Test verse: Lev 16:8 KJV, spread #24's own real citation --
"And Aaron shall cast lots upon the two goats; one lot for the LORD, and the
other lot for the scapegoat."

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_poc_motion_text_combo.py
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "panel_animator"))
sys.path.insert(0, str(HERE))
from registration_snap import _shift_channel, _ease  # noqa: E402
from print_grade import make_halftone_screen  # noqa: E402
from focal_tour import build_tour_schedule, center_at, halo_brightness, focal_to_px  # noqa: E402
import letterpress_beat  # noqa: E402
import _s3_thread_leaf_54_55 as tl  # noqa: E402  -- reuse the proven letterpress-verse primitives

STILLS = HERE / "stills"
OUT = HERE / "_poc_motion_text_combo"
OUT.mkdir(exist_ok=True)
WINDOWS = {r["name"]: r for r in json.loads((HERE / "_spread_windows.json").read_text(encoding="utf-8"))}
ALIGNMENT = json.loads((HERE / "_alignment.json").read_text(encoding="utf-8"))

FPS = 30
W, H = 1920, 1080
PAPER_TONE = np.array([222, 208, 178], dtype=np.float32)

LINES = ["And Aaron shall cast lots", "upon the two goats;",
         "one lot for the LORD,", "and the other lot for the scapegoat."]
BLOCK_X, BLOCK_Y = int(0.055 * W), int(0.035 * H)
BODY_SIZE = 40
LINE_H = int(BODY_SIZE * 1.4)


def _scale_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def _norm_line(line):
    """LINES entries may be a plain string (legacy, single run at BODY_SIZE)
    or a list of (text, size) run tuples (LAW-2 display-scale key words,
    same format _s3_thread_leaf_54_55.py already uses on spreads 54-55) --
    normalize to the run-list form everywhere below."""
    return [(line, BODY_SIZE)] if isinstance(line, str) else line


def _line_plain_text(line) -> str:
    return "".join(text for text, _ in _norm_line(line))


def _build_line_tiles():
    norm_lines = [_norm_line(ln) for ln in LINES]
    sizes = sorted({sz for runs in norm_lines for _, sz in runs})
    fonts = {sz: ImageFont.truetype(tl.F_BODY, sz) for sz in sizes}
    masks = [tl.make_line_mask(runs, fonts) for runs in norm_lines]
    tiles_dark = [tl.compose_pressed_tile(m[0], tl.INK_DARK) for m in masks]
    tiles_final = [tl.compose_pressed_tile(m[0], tl.INK_FINAL) for m in masks]
    return masks, tiles_dark, tiles_final


def _norm_word(s: str) -> str:
    return "".join(c.lower() for c in s if c.isalnum())


def match_line_press_times(lines, alignment, abs_start: float, duration: float) -> list:
    """Round 10 A0.1 (Fable): for each line, find its OWN leading word's
    real spoken start time inside the card's alignment window, matching in
    order (each match consumes words so repeated words like "the" still
    press lines in sequence, not all on the first hit). Returns LOCAL press
    times (seconds from abs_start) -- None per line with no match, printing
    a WARN once; the caller falls back to its own proportional-spacing
    default on None rather than breaking."""
    win_words = [w for w in alignment if abs_start - 0.5 <= w["start"] <= abs_start + duration + 1.0]
    cursor = 0
    times = []
    for line in lines:
        plain = _line_plain_text(line)
        toks = [_norm_word(t) for t in plain.split() if _norm_word(t)]
        found_t = None
        if toks:
            first_tok = toks[0]
            for i in range(cursor, len(win_words)):
                if _norm_word(win_words[i]["w"]) == first_tok:
                    found_t = win_words[i]["start"] - abs_start
                    cursor = i + 1
                    break
        if found_t is None:
            print(f"[WARN] motion_text_combo: no alignment match for line {plain!r} "
                  f"in window [{abs_start:.2f},{abs_start + duration:.2f}]")
        times.append(found_t)
    return times


def _line_heights(masks: list) -> list:
    """Round 10 bugfix: a fixed LINE_H (sized off BODY_SIZE alone) let a
    LAW-2 display-scale run's real glyph height overflow into the next
    line -- "blood" at 2x scale visibly collided with the line below it.
    Each line now advances by its own REALIZED mask height (already
    reflects the tallest run in that line, from make_line_mask), never
    less than the LINE_H floor, plus a little breathing room."""
    return [max(LINE_H, m[2] + 6) for m in masks]


def _draw_backing(img: Image.Image, masks: list, alpha: int = 165):
    """Semi-opaque parchment plate behind the verse block. Some cards' own
    art is dark/busy right where the text lands (e.g. s28's brick wall +
    gold frame border) and the dark-brown pressed ink nearly disappears
    against it -- this keeps every card legible regardless of its own
    background, not just the plain-paper ones the devices were first tried
    on. Sized from the REALIZED line tiles (Round 10 fix), not a fixed
    line-count guess -- LAW-2 display-scale key words widen a line well
    beyond the old flat estimate."""
    max_w = max((m[1] for m in masks), default=int(0.40 * W))
    w = max_w + 40
    h = sum(_line_heights(masks)) + 20
    x0, y0 = BLOCK_X - 18, BLOCK_Y - 14
    plate = Image.new("RGBA", (w, h), (*[int(v) for v in PAPER_TONE], alpha))
    img.alpha_composite(plate, (x0, y0))


def _encode(work: Path, dest: Path):
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%04d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {dest}")


# ---------------------------------------------------------- A: Registration Snap + Verse

def render_combo_a(still: Path, dest: Path, duration: float, abs_start: float = 0.0, snap_frac: float = 0.5):
    base = _scale_crop(Image.open(still).convert("RGB"), W, H)
    arr = np.asarray(base, dtype=np.float32)
    screen = make_halftone_screen(W, H)
    dot_alpha = np.asarray(screen.split()[-1], dtype=np.float32) / 255.0

    masks, tiles_dark, tiles_final = _build_line_tiles()
    press_times = match_line_press_times(LINES, ALIGNMENT, abs_start, duration)
    matched = [t for t in press_times if t is not None]
    # Registration Snap's own print-resolves beat -- ties to the FIRST
    # matched line's real word (the print settles right as the text starts
    # arriving), falling back to the old fixed fraction if nothing matched.
    snap_t = min(matched) if matched else duration * snap_frac
    ease_dur = 0.6
    line_press = [pt if pt is not None else snap_t for pt in press_times]

    work = dest.parent / (dest.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n = max(1, int(round(duration * FPS)))
    for i in range(n):
        t = i / FPS
        if t < snap_t - ease_dur:
            dx, screen_op = 2.4, 0.11
        elif t < snap_t:
            p = _ease((t - (snap_t - ease_dur)) / ease_dur)
            dx, screen_op = 2.4 * (1 - p), 0.11 + (0.02 - 0.11) * p
        else:
            p2 = min(1.0, (t - snap_t) / 0.35)
            dx, screen_op = -0.7 * np.sin(np.pi * p2) * np.exp(-3.5 * p2), 0.02

        frame = arr.copy()
        frame[..., 0] = _shift_channel(arr[..., 0], dx)
        frame[..., 2] = _shift_channel(arr[..., 2], -dx)
        frame *= (1.0 - screen_op * dot_alpha * 0.9)[..., None]
        img = Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).convert("RGBA")
        _draw_backing(img, masks)

        # each line: faint + blurred before ITS OWN matched word, presses in
        # sharp exactly when that word is actually spoken (Round 10 A0.1) --
        # was one global snap for the whole block, now per-line.
        y = BLOCK_Y
        line_heights = _line_heights(masks)
        for li, line in enumerate(LINES):
            mask, mw, mh, pad, base_local = masks[li]
            pre_snap = t < line_press[li]
            tile = tiles_dark[li] if pre_snap else tiles_final[li]
            if pre_snap:
                tile = tile.copy()
                tile = tile.filter(ImageFilter.GaussianBlur(3.5))
                r, g, b, a = tile.split()
                tile.putalpha(a.point(lambda v: int(v * 0.22)))
            tl.paste_tile(img, tile, BLOCK_X, y + base_local, pad, base_local, 1.0, 1.0)
            y += line_heights[li]

        Image.fromarray(np.array(img.convert("RGB"))).save(work / f"f{i:04d}.png")

    _encode(work, dest)


# ---------------------------------------------------------------- B: Ink-Up Build + Verse

def render_combo_b(still: Path, dest: Path, duration: float, abs_start: float = 0.0):
    base = _scale_crop(Image.open(still).convert("RGB"), W, H)
    src = np.asarray(base, dtype=np.float32)
    y_grid, x_grid = np.mgrid[0:H, 0:W].astype(np.float32)

    # 2 focal "elements" in narration order: the hand+lots (already-drawn
    # art), then the verse block itself (not yet on the page at all).
    image_region = {"bbox": [55, 35, 40, 55]}
    verse_region = {"bbox": [4, 2, 45, 30]}
    regions = [image_region, verse_region]
    schedule = build_tour_schedule(regions, duration, W, H,
                                    initial_hold_sec=max(0.6, duration * 0.12),
                                    move_sec=max(0.5, duration * 0.08),
                                    final_hold_sec=max(0.6, duration * 0.12))
    img_cx, img_cy, img_r = focal_to_px(tuple(image_region["bbox"]), W, H)
    img_field = halo_brightness(x_grid, y_grid, img_cx, img_cy, img_r, dim_floor=0.0)

    masks, tiles_dark, tiles_final = _build_line_tiles()
    press_times = match_line_press_times(LINES, ALIGNMENT, abs_start, duration)

    work = dest.parent / (dest.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n = max(1, int(round(duration * FPS)))
    verse_reveal_start = None
    for i in range(n):
        t = i / FPS
        cx, cy, _ = center_at(schedule, t)
        d_img = (cx - img_cx) ** 2 + (cy - img_cy) ** 2
        vx, vy, _ = focal_to_px(tuple(verse_region["bbox"]), W, H)
        d_verse = (cx - vx) ** 2 + (cy - vy) ** 2
        verse_active = d_verse < d_img

        k = 0.40 + (1.0 - 0.40) * img_field if not verse_active else np.full((H, W), 0.55, dtype=np.float32)
        frame = PAPER_TONE[None, None, :] + (src - PAPER_TONE[None, None, :]) * k[..., None]
        img = Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).convert("RGBA")

        if verse_active and verse_reveal_start is None:
            verse_reveal_start = t
        if verse_reveal_start is not None:
            _draw_backing(img, masks)
            y = BLOCK_Y
            line_heights = _line_heights(masks)
            for li, line in enumerate(LINES):
                mask, mw, mh, pad, base_local = masks[li]
                # Round 10 A0.1: each line presses at ITS OWN matched
                # narration word, clamped to not fire before the tour's
                # attention has even reached the verse block; falls back to
                # the old li*0.15 stagger only when no match was found.
                matched = press_times[li]
                line_press_t = max(matched, verse_reveal_start) if matched is not None \
                    else verse_reveal_start + li * 0.15
                line_local = t - line_press_t
                if line_local < 0:
                    y += line_heights[li]
                    continue
                lp = min(1.0, max(0.0, line_local / 0.4))
                color_t = min(1.0, max(0.0, (line_local - 0.1) / 0.5))
                color = tl.lerp_color(tl.INK_DARK, tl.INK_FINAL, color_t)
                tile = tl.compose_pressed_tile(mask, color)
                tl.paste_tile(img, tile, BLOCK_X, y + base_local, pad, base_local,
                              1.05 - 0.05 * lp, lp)
                y += line_heights[li]

        Image.fromarray(np.array(img.convert("RGB"))).save(work / f"f{i:04d}.png")

    _encode(work, dest)


# --------------------------------------------------------------- C: Letterpress Beat + Verse

def render_combo_c(still: Path, dest: Path, duration: float, beats_local: list):
    base = _scale_crop(Image.open(still).convert("RGB"), W, H)
    src = np.asarray(base, dtype=np.float32)
    gray = np.asarray(base.convert("L"), dtype=np.float32) / 255.0
    ink_mask = np.clip(1.0 - gray, 0.0, 1.0) ** 1.3

    masks, tiles_dark, tiles_final = _build_line_tiles()
    line_beats = beats_local[1::2][:len(LINES)] if len(beats_local) >= 8 else beats_local[:len(LINES)]

    work = dest.parent / (dest.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n = max(1, int(round(duration * FPS)))
    for i in range(n):
        t = i / FPS
        pulse = 0.0
        for b in beats_local:
            dt = t - b
            if 0 <= dt < letterpress_beat.PULSE_DUR:
                pulse = max(pulse, 1.0 - dt / letterpress_beat.PULSE_DUR)
        darken = letterpress_beat.DARKEN_K * 1.5 * pulse  # Round 10: C-card pulse barely
        # registered on screen at the module's own default amplitude
        frame = src * (1.0 - darken * ink_mask[..., None])
        img = Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).convert("RGBA")
        if line_beats and t >= line_beats[0]:
            _draw_backing(img, masks)

        y = BLOCK_Y
        line_heights = _line_heights(masks)
        for li, line in enumerate(LINES):
            beat_t = line_beats[li] if li < len(line_beats) else None
            if beat_t is None or t < beat_t:
                y += line_heights[li]
                continue
            mask, mw, mh, pad, base_local = masks[li]
            lt = t - beat_t
            if lt < 0.10:
                pop = lt / 0.10
                scale, alpha, color = 1.05 - 0.05 * pop, pop, tl.INK_DARK
            else:
                ease = min(1.0, (lt - 0.10) / 0.5)
                scale, alpha, color = 1.0, 1.0, tl.lerp_color(tl.INK_DARK, tl.INK_FINAL, ease)
            tile = tl.compose_pressed_tile(mask, color)
            tl.paste_tile(img, tile, BLOCK_X, y + base_local, pad, base_local, scale, alpha)
            y += line_heights[li]

        Image.fromarray(np.array(img.convert("RGB"))).save(work / f"f{i:04d}.png")

    _encode(work, dest)


if __name__ == "__main__":
    name = "s24_lots_card"
    still = STILLS / f"{name}.png"
    dur = WINDOWS[name]["dur"]
    start = WINDOWS[name]["start"]

    render_combo_a(still, OUT / f"{name}_A_registration_snap_verse.mp4", dur)
    render_combo_b(still, OUT / f"{name}_B_ink_up_build_verse.mp4", dur)
    beats = letterpress_beat.beats_in_window(ALIGNMENT, start, start + dur, letterpress_beat.MIN_SPACING)
    render_combo_c(still, OUT / f"{name}_C_letterpress_beat_verse.mp4", dur, beats)
