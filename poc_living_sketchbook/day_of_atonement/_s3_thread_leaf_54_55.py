#!/usr/bin/env python
"""Animate spreads 54-55 (Day of Atonement, longform/06_Day_Of_Atonement):
Thread Device (gold thread, goat-laying-on vignette -> Christ) + the verse
(Isaiah 53:6) letterpressed directly into the blank paper margin -- no card,
no cursive. $0 deterministic compositing over the existing s54 still -- no
new still needed. Per _PLAN.md lines 196-197.

DESIGN HISTORY (two rounds of user eye-check before this one):
  R1: hand-cursive Kunstler Script on a foxed/taped "leaf" card. Rejected --
      unreadable (user is dyslexic), looked cheap, card idea itself rejected.
  R2: flat ArkAIology-style caption card, bold sans, word-by-word pop-in.
      Functional and legible, but user wanted a stronger creative pass and
      asked for a Fable design round (their standing practice: Fable designs,
      Sonnet builds).
  R3 (this file): Fable proposed 3 concepts (letterpress-into-paper /
      tipped-in Bible leaf / cascading clause titles); user picked
      "Pressed into the page" -- no container object at all, the verse
      prints straight into the sketchbook's own blank paper, clause by
      clause, each arrival a physical press (halo + embossed highlight rim
      + crisp ink, landing dark and drying to the final ink tone over 0.5s).
      The cut at 12.7s is visually seamless, so the verse presses in during
      beat 1's tail; beat 2 (3.92s) is then pure hold/read time plus the
      reference stamping in with a matching gold stitch, and one luminance
      swell on the main thread at that instant.
  R4 (this file): user flagged the camera as "very very basic" (a flat
      uniform push-in ignores that the still has 3 real elements -- the
      goat/hand vignette, Christ, the verse) and pointed at a technique
      already proven in a sibling project (edenradios' motion_styles.py
      "dramatic_spotlight" family: a soft halo TOURS named elements in
      sequence, dimming the rest, rather than cropping/zooming the frame).
      Ported as the new reusable `panel_animator/focal_tour.py` skill (see
      its own docstring) and used here in place of the flat push-in: the
      halo settles on the goat+hand, moves to Christ as the thread reads,
      then arrives on the verse block just as it starts pressing in --
      light finds the page, then the words come.

Two separate clips (assembly stitches spreads by time-window, the boundary
sits at 411.68s): all timing below is GLOBAL (t_global = t within 54, or
D54+t within 55) so nothing jumps at the cut.

Run (sequential, single ffmpeg encode per clip -- gentle on CPU/RAM):
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s3_thread_leaf_54_55.py
"""
from __future__ import annotations
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO / "panel_animator"))
sys.path.insert(0, str(ROOT))
from elder_leaf import smootherstep  # noqa: E402
from focal_tour import build_tour_schedule, center_at, apply_halo  # noqa: E402
import _polite  # noqa: E402

STILL = ROOT / "stills" / "s54_guilt_laid_on_christ.png"
OUT_DIR = ROOT / "clips"
OUT_DIR.mkdir(exist_ok=True)

W, H, FPS = 1920, 1080, 30
D54, D55 = 12.7, 3.92  # ffprobe-verified spread durations, _PLAN.md table
TOTAL_DUR = D54 + D55

THREAD_START, THREAD_FADE = 0.6, 1.2  # gold thread fades in early in 54, then holds
GOAT_ANCHOR = (0.885, 0.70)     # goat + Aaron's hand vignette, bottom right
CHRIST_ANCHOR = (0.475, 0.575)  # Christ's chest -- the guilt laid on Him
GOLD = (185, 146, 74)
GOLD_BRIGHT = (226, 193, 118)   # thread's luminance-swell tone

# Focal Tour (R4) -- soft halo visits the still's 3 real elements in
# narration order, dimming the rest, instead of a flat crop/zoom push-in.
FOCAL_REGIONS = [
    {"bbox": [72, 55, 26, 35]},   # goat + Aaron's hand (the OT rite)
    {"bbox": [30, 18, 34, 58]},   # Christ -- the thread's far end
    {"bbox": [6, 52, 30, 42]},    # the verse letterpress block
]
TOUR_DIM_FLOOR = 0.30
TOUR_INITIAL_HOLD, TOUR_MOVE, TOUR_FINAL_HOLD = 0.8, 1.2, 2.0

# ---- Letterpress verse (Fable concept 1) -----------------------------------
F_BODY = "C:/Windows/Fonts/ZillaSlab-Bold.ttf"
BODY_SIZE = 40
LORD_SIZE = int(BODY_SIZE * 0.88)   # KJV small-caps convention for the Name
LINE_H = int(BODY_SIZE * 1.4)

INK_FINAL = (59, 46, 34)     # dried ink
INK_DARK = (36, 26, 18)      # fresh-pressed ink, eases to INK_FINAL
HIGHLIGHT = (239, 228, 205)  # embossed paper rim, catching the light
REF_GOLD = (138, 106, 42)

BLOCK_X_FRAC, BLOCK_Y_FRAC = 0.076, 0.573  # blank lower-left paper margin (Fable's read of the still)

LINES = [
    [("All we like sheep", BODY_SIZE)],
    [("have gone astray;", BODY_SIZE)],
    [("we have turned every one", BODY_SIZE)],
    [("to his own way;", BODY_SIZE)],
    [("and the ", BODY_SIZE), ("LORD", LORD_SIZE), (" hath laid on him", BODY_SIZE)],
    [("the iniquity of us all.", BODY_SIZE)],
]
PRESS_GROUPS = [(0, 1), (2, 3), (4, 5)]           # lines pressed together, in pairs
# Timed to land inside the focal tour's verse-block hold window (10.41-13.42,
# computed from FOCAL_REGIONS/TOUR_* above) -- light arrives, THEN the words.
PRESS_TIMES = [10.6, 11.6, 12.6]
PRESS_DUR = 0.10                                  # snappy thump, not a fade
COLOR_EASE_DUR = 0.5                              # ink drying

REF_TEXT = "ISAIAH 53:6"
REF_TIME = 13.0        # just after the cut into beat 2, still inside the verse hold
REF_PRESS_DUR = 0.15
STITCH_LEN = int(0.087 * W)


def lerp_color(c0, c1, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a + (b - a) * t) for a, b in zip(c0, c1))


# --------------------------------------------------------------- still prep

def scale_crop_16x9(im: Image.Image, w: int, h: int) -> Image.Image:
    """Crop to exact 16:9 (center) then resize -- avoids squash distortion."""
    iw, ih = im.size
    target_ratio = w / h
    src_ratio = iw / ih
    if src_ratio > target_ratio:
        new_w = int(ih * target_ratio)
        x0 = (iw - new_w) // 2
        im = im.crop((x0, 0, x0 + new_w, ih))
    elif src_ratio < target_ratio:
        new_h = int(iw / target_ratio)
        y0 = (ih - new_h) // 2
        im = im.crop((0, y0, iw, y0 + new_h))
    return im.resize((w, h), Image.LANCZOS)


# ------------------------------------------------------------- gold thread

def make_thread_layer(w: int, h: int, p0_frac, p1_frac, color, seed=9, n=16, bow=70, width=4) -> Image.Image:
    """Static gold-stitched-thread RGBA layer, full frame size, transparent bg."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0 = p0_frac[0] * w, p0_frac[1] * h
    x1, y1 = p1_frac[0] * w, p1_frac[1] * h
    rng = random.Random(seed)
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy) or 1
    nx, ny = -dy / length, dx / length
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x0 + dx * t
        y = y0 + dy * t
        off = bow * math.sin(t * math.pi) + rng.uniform(-3, 3)
        pts.append((x + nx * off, y + ny * off))
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=(*color, 255), width=width)
    r = width + 2
    d.ellipse([x0 - r, y0 - r, x0 + r, y0 + r], fill=(*color, 255))
    d.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=(*color, 255))
    return layer


def thread_opacity(t: float) -> float:
    if t < THREAD_START:
        return 0.0
    return smootherstep((t - THREAD_START) / THREAD_FADE)


def thread_swell(t_global: float) -> float:
    """One luminance swell on the thread right as the reference stamps in:
    rises 0.6s, decays 0.8s, otherwise 0."""
    rise, decay = 0.6, 0.8
    lt = t_global - REF_TIME
    if lt < 0:
        return 0.0
    if lt < rise:
        return smootherstep(lt / rise)
    lt2 = lt - rise
    if lt2 < decay:
        return 1.0 - smootherstep(lt2 / decay)
    return 0.0


# -------------------------------------------------------- letterpress verse

def make_line_mask(runs, fonts, pad=14):
    """runs: [(text, size), ...]. Returns (mask_L, w, h, pad, baseline_y_local)."""
    dummy = ImageDraw.Draw(Image.new("L", (1, 1)))
    widths = [dummy.textlength(t, font=fonts[s]) for t, s in runs]
    total_w = int(sum(widths)) + pad * 2
    max_ascent = max(fonts[s].getmetrics()[0] for _, s in runs)
    max_descent = max(fonts[s].getmetrics()[1] for _, s in runs)
    total_h = max_ascent + max_descent + pad * 2
    mask = Image.new("L", (total_w, total_h), 0)
    d = ImageDraw.Draw(mask)
    x = pad
    y_baseline = pad + max_ascent
    for (text, size), w in zip(runs, widths):
        font = fonts[size]
        d.text((x, y_baseline - font.getmetrics()[0]), text, font=font, fill=255)
        x += w
    return mask, total_w, total_h, pad, y_baseline


def compose_pressed_tile(mask: Image.Image, ink_color) -> Image.Image:
    """Ink pressed into paper: a soft halo (ink soaking into fibre), an
    embossed highlight rim (paper pushed up at the impression's edge), and
    the crisp main glyph fill -- all from the same fixed glyph mask."""
    w, h = mask.size
    halo_mask = mask.filter(ImageFilter.GaussianBlur(4))
    arr = np.asarray(mask, dtype=np.float32)
    dy, dx = 3, 2
    shifted = np.zeros_like(arr)
    shifted[dy:, dx:] = arr[:-dy, :-dx]
    rim = np.clip(shifted - arr, 0, 255).astype(np.uint8)
    rim_mask = Image.fromarray(rim, "L")

    tile = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    halo_layer = Image.new("RGBA", (w, h), (*INK_FINAL, 0))
    halo_layer.putalpha(halo_mask.point(lambda v: int(v * 0.10)))
    tile.alpha_composite(halo_layer)
    hi_layer = Image.new("RGBA", (w, h), (*HIGHLIGHT, 0))
    hi_layer.putalpha(rim_mask.point(lambda v: int(v * 0.30)))
    tile.alpha_composite(hi_layer)
    main_layer = Image.new("RGBA", (w, h), (*ink_color, 0))
    main_layer.putalpha(mask.point(lambda v: int(v * 0.92)))
    tile.alpha_composite(main_layer)
    return tile


def line_press_state(t_global: float, group_idx: int):
    """Returns None if not yet pressed, else (scale, alpha, ink_color)."""
    lt = t_global - PRESS_TIMES[group_idx]
    if lt < 0:
        return None
    if lt < PRESS_DUR:
        pop = lt / PRESS_DUR
        return 1.05 - 0.05 * pop, pop, INK_DARK
    ease = min(1.0, (lt - PRESS_DUR) / COLOR_EASE_DUR)
    return 1.0, 1.0, lerp_color(INK_DARK, INK_FINAL, ease)


def paste_tile(frame: Image.Image, tile: Image.Image, target_x: int, target_baseline_y: int,
                pad: int, baseline_local: int, scale: float, alpha: float):
    if alpha < 1.0:
        tile = tile.copy()
        r, g, b, a = tile.split()
        tile.putalpha(a.point(lambda v: int(v * alpha)))
    px = target_x - pad
    py = target_baseline_y - baseline_local
    if scale != 1.0:
        nw, nh = max(1, int(tile.width * scale)), max(1, int(tile.height * scale))
        scaled = tile.resize((nw, nh), Image.LANCZOS)
        cx, cy = px + tile.width / 2, py + tile.height / 2
        px, py = int(cx - nw / 2), int(cy - nh / 2)
        frame.alpha_composite(scaled, (px, py))
    else:
        frame.alpha_composite(tile, (int(px), int(py)))


def draw_letterspaced(d: ImageDraw.ImageDraw, xy, text, font, fill, spacing=3):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + spacing
    return x


REF_LETTER_SPACING = 3


def make_ref_tile(ref_font) -> Image.Image:
    """Gold stitch rule + letterspaced reference, static tile, popped in whole."""
    dummy = ImageDraw.Draw(Image.new("L", (1, 1)))
    ref_w = int(sum(dummy.textlength(ch, font=ref_font) for ch in REF_TEXT)
                + REF_LETTER_SPACING * (len(REF_TEXT) - 1))
    tw = max(STITCH_LEN, ref_w)
    th = int(ref_font.size * 1.9)
    tile = Image.new("RGBA", (tw + 8, th + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    d.line([(0, 4), (STITCH_LEN, 4)], fill=(*GOLD, 255), width=3)
    draw_letterspaced(d, (0, 14), REF_TEXT, ref_font, (*REF_GOLD, 255), spacing=REF_LETTER_SPACING)
    return tile


# --------------------------------------------------------------- focal tour

def apply_focal_tour(frame: Image.Image, schedule, t_global: float) -> Image.Image:
    """Dim everything but a soft halo around the tour's current element --
    replaces a flat crop/zoom push-in with light that visits the still's
    own named elements in narration order. See panel_animator/focal_tour.py."""
    cx, cy, r = center_at(schedule, t_global)
    arr = apply_halo(frame, cx, cy, r, dim_floor=TOUR_DIM_FLOOR)
    return Image.fromarray((np.clip(arr, 0.0, 1.0) * 255.0).astype(np.uint8))


# --------------------------------------------------------------- render

def render_frames_to_mp4(frames_fn, n_frames: int, out_mp4: Path):
    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for i in range(n_frames):
        t = i / FPS
        frame = frames_fn(t)
        frame.save(work / f"f{i:05d}.png")
    subprocess.run(
        ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
         str(out_mp4)],
        check=True, capture_output=True,
    )
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


def main():
    _polite.be_polite()
    base = scale_crop_16x9(Image.open(STILL).convert("RGB"), W, H)
    thread_layer = make_thread_layer(W, H, GOAT_ANCHOR, CHRIST_ANCHOR, GOLD)
    thread_bright = make_thread_layer(W, H, GOAT_ANCHOR, CHRIST_ANCHOR, GOLD_BRIGHT)

    fonts = {BODY_SIZE: ImageFont.truetype(F_BODY, BODY_SIZE),
             LORD_SIZE: ImageFont.truetype(F_BODY, LORD_SIZE)}
    ref_font = ImageFont.truetype(F_BODY, 24)

    line_masks = [make_line_mask(runs, fonts) for runs in LINES]
    body_ascent = fonts[BODY_SIZE].getmetrics()[0]
    block_x = int(BLOCK_X_FRAC * W)
    block_y = int(BLOCK_Y_FRAC * H)
    line_baseline_y = [block_y + i * LINE_H + body_ascent for i in range(len(LINES))]
    ref_tile = make_ref_tile(ref_font)
    ref_target_x = block_x
    ref_target_y = block_y + len(LINES) * LINE_H + 14

    tour_schedule = build_tour_schedule(FOCAL_REGIONS, TOTAL_DUR, W, H,
                                         TOUR_INITIAL_HOLD, TOUR_MOVE, TOUR_FINAL_HOLD)

    tile_cache: dict = {}

    def pressed_tile_for(li: int, color):
        key = (li, color)
        if key not in tile_cache:
            mask = line_masks[li][0]
            tile_cache[key] = compose_pressed_tile(mask, color)
        return tile_cache[key]

    def draw_verse(frame: Image.Image, t_global: float):
        for gi, group in enumerate(PRESS_GROUPS):
            for li in group:
                state = line_press_state(t_global, gi)
                if state is None:
                    continue
                scale, alpha, color = state
                mask, w, h, pad, base_local = line_masks[li]
                tile = pressed_tile_for(li, color)
                paste_tile(frame, tile, block_x, line_baseline_y[li], pad, base_local, scale, alpha)

    def draw_ref(frame: Image.Image, t_global: float):
        lt = t_global - REF_TIME
        if lt < 0:
            return
        if lt < REF_PRESS_DUR:
            pop = lt / REF_PRESS_DUR
            scale, alpha = 1.05 - 0.05 * pop, pop
        else:
            scale, alpha = 1.0, 1.0
        tile = ref_tile
        if alpha < 1.0:
            tile = tile.copy()
            r, g, b, a = tile.split()
            tile.putalpha(a.point(lambda v: int(v * alpha)))
        if scale != 1.0:
            nw, nh = max(1, int(tile.width * scale)), max(1, int(tile.height * scale))
            scaled = tile.resize((nw, nh), Image.LANCZOS)
            cx, cy = ref_target_x + tile.width / 2, ref_target_y + tile.height / 2
            frame.alpha_composite(scaled, (int(cx - nw / 2), int(cy - nh / 2)))
        else:
            frame.alpha_composite(tile, (ref_target_x, ref_target_y))

    def compose_frame(t_global: float) -> Image.Image:
        f = base.convert("RGBA")
        op = thread_opacity(min(t_global, D54))
        if op > 0:
            layer = thread_layer if op >= 1.0 else Image.blend(
                Image.new("RGBA", thread_layer.size, (0, 0, 0, 0)), thread_layer, op)
            swell = thread_swell(t_global)
            if swell > 0:
                layer = Image.blend(layer, thread_bright, swell * 0.6)
            f.alpha_composite(layer)
        draw_verse(f, t_global)
        draw_ref(f, t_global)
        return apply_focal_tour(f.convert("RGB"), tour_schedule, t_global)

    n54 = int(round(D54 * FPS))
    render_frames_to_mp4(lambda t: compose_frame(t), n54, OUT_DIR / "spread54_thread_leaf.mp4")

    n55 = int(round(D55 * FPS))
    render_frames_to_mp4(lambda t: compose_frame(D54 + t), n55, OUT_DIR / "spread55_isaiah536.mp4")


if __name__ == "__main__":
    main()
