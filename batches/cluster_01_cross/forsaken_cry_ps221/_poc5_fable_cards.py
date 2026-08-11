"""POC v5 -- replaces the flat Arial Black yellow/red cards (rejected: doesn't
belong on hand-painted sketchbook paper) with a genuinely book-native design,
per Fable's spec (2026-08-11): a torn-parchment letterpress title, the
existing gold-stitch citation (reused near-verbatim), and a compressed
red-letter quote card (Illuminated Rubric's own grammar, apparatus stripped
for short-form pace). All three vendor REAL primitives from
poc_living_sketchbook/day_of_atonement/_s3_thread_leaf_54_55.py
(make_line_mask/compose_pressed_tile/paste_tile/draw_letterspaced/
make_ref_tile) and _devices.py (RUBRIC/GOLD/_radial_gain concept), not
reinvented -- same book, same ink, same gold, as the shipped sketchbook longs.

Everything else (sketchbook art, real push-in motion, Noah's hand-ink
caption) is unchanged from POC4.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/forsaken_cry_ps221/_poc5_fable_cards.py
"""
import json
import math
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.resolve().parents[2]
sys.path.insert(0, str(ROOT / "poc_castbible_look"))
from _polite import be_polite  # noqa: E402

AUD = HERE / "audio" / "narration.mp3"
STILLS = HERE / "_poc_sketchbook_stills"
WORK = HERE / "_poc5_work"
SILENT = HERE / "_poc5_silent.mp4"
OUT = HERE / "_POC5_fable_cards.mp4"

W, H, FPS = 1080, 1920, 30

# ---- Noah's exact caption constants (unchanged, locked standard) ---------
F_KEEPER = "C:/Windows/Fonts/Inkfree.ttf"
CAP_INK = (35, 30, 26, 255)
PARCHMENT = (247, 242, 228)
CAPTION_Y_FRAC = 0.86
MAX_TEXT_W = int(W * 0.72)
GAP_BREAK = 0.35
MAX_WORDS = 6
MIN_CHUNK_DUR = 0.45
STROKE_W = 2
FONT_SIZE0 = 46
FONT_SIZE_MIN = 30

# ---- real sketchbook-book primitives, vendored from _s3_thread_leaf_54_55.py
# and _devices.py (day_of_atonement) -- same ink, same gold, as the shipped longs
F_BODY = "C:/Windows/Fonts/ZillaSlab-Bold.ttf"
INK_FINAL = (59, 46, 34)
INK_DARK = (36, 26, 18)
HIGHLIGHT = (239, 228, 205)
GOLD = (185, 146, 74)
REF_GOLD = (138, 106, 42)
RUBRIC = (150, 26, 22)
PLATE_COLOR = (222, 208, 178)


def lerp_color(c0, c1, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a + (b - a) * t) for a, b in zip(c0, c1))


def make_line_mask(runs, fonts, pad=14):
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


def compose_pressed_tile(mask, ink_color):
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


def draw_letterspaced(d, xy, text, font, fill, spacing=3):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + spacing
    return x


def torn_plate(w, h, seed=0, jitter=5, step=10):
    """A parchment label with hand-torn deckled edges on all 4 sides --
    same jittered-polygon technique as storm/_s6_assemble.py's _torn_deckle,
    applied to a rectangle instead of a full page edge."""
    rng = random.Random(seed)
    pts = []
    for x in range(0, w + 1, step):
        pts.append((x, rng.uniform(-jitter, jitter)))
    for y in range(0, h + 1, step):
        pts.append((w + rng.uniform(-jitter, jitter), y))
    for x in range(w, -1, -step):
        pts.append((x, h + rng.uniform(-jitter, jitter)))
    for y in range(h, -1, -step):
        pts.append((rng.uniform(-jitter, jitter), y))
    pad = jitter + 2
    poly = [(x + pad, y + pad) for x, y in pts]
    canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    d.polygon(poly, fill=(*PLATE_COLOR, 170))
    canvas = canvas.filter(ImageFilter.GaussianBlur(0.8))
    return canvas


def make_ref_tile(ref_text, size):
    ref_font = ImageFont.truetype(F_BODY, size)
    dummy = ImageDraw.Draw(Image.new("L", (1, 1)))
    stitch_len = int(0.35 * size * len(ref_text) * 0.6)
    ref_w = int(sum(dummy.textlength(ch, font=ref_font) for ch in ref_text) + 3 * (len(ref_text) - 1))
    tw = max(stitch_len, ref_w)
    th = int(size * 1.9)
    tile = Image.new("RGBA", (tw + 8, th + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    d.line([(0, 4), (stitch_len, 4)], fill=(*GOLD, 255), width=4)
    draw_letterspaced(d, (0, 14), ref_text, ref_font, (*REF_GOLD, 255), spacing=3)
    return tile


def render_title_card(text, dt):
    if dt < -0.05:
        return None
    dt = max(0.0, dt)
    font = ImageFont.truetype(F_BODY, 78)
    mask, mw, mh, mpad, baseline = make_line_mask([(text, 78)], {78: font}, pad=26)
    ink_ease = min(1.0, max(0.0, (dt - 0.12) / 0.5))
    ink_color = lerp_color(INK_DARK, INK_FINAL, ink_ease)
    tile = compose_pressed_tile(mask, ink_color)

    plate_w, plate_h = mw + 16, mh + 30
    plate = torn_plate(plate_w, plate_h, seed=abs(hash(text)) % 1000)
    canvas = Image.new("RGBA", plate.size, (0, 0, 0, 0))
    canvas.alpha_composite(plate, (0, 0))
    tx, ty = (plate.width - mw) // 2, (plate.height - mh) // 2 - 4
    canvas.alpha_composite(tile, (tx, ty))

    if dt >= 0.35:
        up = min(1.0, (dt - 0.35) / 0.25)
        ud = ImageDraw.Draw(canvas)
        x0 = tx + mpad
        x1_full = tx + mw - mpad
        cur_x1 = x0 + (x1_full - x0) * up
        uy = ty + baseline + 8
        rng = random.Random(7)
        pts, xx = [], x0
        while xx < cur_x1:
            pts.append((xx, uy + rng.uniform(-2, 2)))
            xx += 7
        pts.append((cur_x1, uy + rng.uniform(-2, 2)))
        if len(pts) >= 2:
            ud.line(pts, fill=(*INK_FINAL, 255), width=2, joint="curve")

    press = min(1.0, dt / 0.12)
    scale = 1.06 - 0.06 * press
    if scale != 1.0:
        nw, nh = max(1, int(canvas.width * scale)), max(1, int(canvas.height * scale))
        canvas = canvas.resize((nw, nh), Image.LANCZOS)
    if press < 1.0:
        r, g, b, a = canvas.split()
        canvas.putalpha(a.point(lambda v: int(v * press)))
    return canvas


def render_citation_card(text, dt):
    if dt < -0.05:
        return None
    dt = max(0.0, dt)
    tile = make_ref_tile(text, 30)
    press = min(1.0, dt / 0.15)
    scale = 1.05 - 0.05 * press
    if scale != 1.0:
        nw, nh = max(1, int(tile.width * scale)), max(1, int(tile.height * scale))
        tile = tile.resize((nw, nh), Image.LANCZOS)
    if press < 1.0:
        r, g, b, a = tile.split()
        tile.putalpha(a.point(lambda v: int(v * press)))
    return tile


def render_quote_card(lines, dt):
    if dt < -0.05:
        return None
    dt = max(0.0, dt)
    body_size = 44
    font = ImageFont.truetype(F_BODY, body_size)
    fonts = {body_size: font}
    line_masks = [make_line_mask([(ln, body_size)], fonts, pad=10) for ln in lines]
    line_h = int(body_size * 1.35)
    max_w = max(m[1] for m in line_masks)
    citation_h = int(30 * 1.9) + 8 + 14  # make_ref_tile's own height + the +6 gap below the text
    plate_w, plate_h = max_w + 90, line_h * len(lines) + 40 + citation_h

    press = min(1.0, dt / 0.12)
    ink_ease = min(1.0, max(0.0, (dt - 0.12) / 0.4))
    ink_color = lerp_color(INK_DARK, RUBRIC, ink_ease) if ink_ease < 1.0 else RUBRIC

    plate = torn_plate(plate_w, plate_h, seed=99)
    canvas = Image.new("RGBA", plate.size, (0, 0, 0, 0))
    canvas.alpha_composite(plate, (0, 0))

    y = 20
    cap_h = int(body_size * 1.6)
    for i, (mask, mw, mh, mpad, baseline) in enumerate(line_masks):
        x = 70 if i == 0 else 20
        if i == 0:
            swell = max(0.0, 1.0 - dt / 0.4)
            gs = int(cap_h * 1.6)
            glow = Image.new("RGBA", (gs, gs), (0, 0, 0, 0))
            gd = ImageDraw.Draw(glow)
            gd.ellipse([gs * 0.15, gs * 0.15, gs * 0.85, gs * 0.85],
                       fill=(*GOLD, int(210 + 45 * swell)))
            glow = glow.filter(ImageFilter.GaussianBlur(gs * 0.12))
            canvas.alpha_composite(glow, (x - gs // 2 + 14, y - (gs - cap_h) // 2))
        tile = compose_pressed_tile(mask, ink_color)
        canvas.alpha_composite(tile, (x, y))
        y += line_h

    citation_dt = dt - 0.5
    if citation_dt >= -0.05:
        ref_tile = render_citation_card("MATTHEW 27:46", citation_dt)
        if ref_tile:
            canvas.alpha_composite(ref_tile, (20, y + 6))

    scale = 1.06 - 0.06 * press
    if scale != 1.0:
        nw, nh = max(1, int(canvas.width * scale)), max(1, int(canvas.height * scale))
        canvas = canvas.resize((nw, nh), Image.LANCZOS)
    if press < 1.0:
        r, g, b, a = canvas.split()
        canvas.putalpha(a.point(lambda v: int(v * press)))
    return canvas


# (still, window_start, window_end, zoom_end)
SEGMENTS = [
    ("s_golgotha_sketchbook.png", 9.8, 15.05, 1.06),
    ("s_bowedhead_sketchbook.png", 27.15, 31.9, 1.07),
]

CAPTION_SKIPS = [(0.3, 3.6), (5.25, 9.5)]

# (kind, t_in, cx_frac, cy_frac, payload)
CARD_EVENTS = [
    ("title", 0.3, 0.50, 0.15, "THE FORSAKEN CRY."),
    ("quote", 5.6, 0.50, 0.24, ["WHY HAST THOU", "FORSAKEN ME?"]),
]


def chunk_words(words, skips, hard_breaks=()):
    chunks, cur = [], []
    for w in words:
        crossed_seam = any(cur and cur[-1]["end"] <= b <= w["start"] for b in hard_breaks)
        if cur and (w["start"] - cur[-1]["end"] >= GAP_BREAK or len(cur) >= MAX_WORDS or crossed_seam):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    merged = []
    for c in chunks:
        d = c[-1]["end"] - c[0]["start"]
        seam = merged and any(merged[-1][-1]["end"] <= b <= c[0]["start"] for b in hard_breaks)
        if merged and d < MIN_CHUNK_DUR and len(merged[-1]) + len(c) <= MAX_WORDS + 2 and not seam:
            merged[-1].extend(c)
        else:
            merged.append(c)
    out = []
    for c in merged:
        t0, t1 = c[0]["start"], c[-1]["end"]
        if any(t1 >= s0 and t0 <= s1 for s0, s1 in skips):
            continue
        out.append(c)
    return out


def render_chunk_png(chunk, seed):
    rng = random.Random(seed)
    text = " ".join(w["w"] for w in chunk)
    size = FONT_SIZE0
    font = ImageFont.truetype(F_KEEPER, size)
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    while probe.textlength(text, font=font) > MAX_TEXT_W and size > FONT_SIZE_MIN:
        size -= 2
        font = ImageFont.truetype(F_KEEPER, size)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sp = probe.textlength(" ", font=font)
    widths = [probe.textlength(w["w"], font=font) for w in chunk]
    total_w = sum(widths) + sp * (len(chunk) - 1)
    x = (W - total_w) / 2
    baseline_y = int(H * CAPTION_Y_FRAC)
    pad_x, pad_y = 22, 14
    scrim = Image.new("RGBA", (int(total_w) + pad_x * 2, size + pad_y * 2), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    sd.rounded_rectangle([0, 0, scrim.width - 1, scrim.height - 1], radius=14, fill=(*PARCHMENT, 158))
    scrim = scrim.filter(ImageFilter.GaussianBlur(0.6))
    canvas.alpha_composite(scrim, (int(x - pad_x), int(baseline_y - pad_y)))
    for w, wid in zip(chunk, widths):
        jx, jy, ang = rng.uniform(-2, 2), rng.uniform(-3, 3), rng.uniform(-1.6, 1.6)
        word_img = Image.new("RGBA", (int(wid) + 24, size + 24), (0, 0, 0, 0))
        wd = ImageDraw.Draw(word_img)
        wd.text((12, 8), w["w"], font=font, fill=CAP_INK, stroke_width=STROKE_W, stroke_fill=CAP_INK)
        word_img = word_img.rotate(ang, resample=Image.BICUBIC, expand=False)
        canvas.alpha_composite(word_img, (int(x + jx - 12), int(baseline_y + jy - 8)))
        x += wid + sp
    return canvas


def ease(t):
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def main():
    be_polite()
    WORK.mkdir(exist_ok=True)

    all_words = json.loads((HERE / "audio" / "alignment.json").read_text(encoding="utf-8"))
    words, running = [], 0.0
    seg_bounds = []
    for (name, t0, t1, zend) in SEGMENTS:
        dur = t1 - t0
        seg_bounds.append((running, running + dur, name, zend))
        for w in all_words:
            if w["start"] >= t0 and w["end"] <= t1:
                words.append({"w": w["w"], "start": w["start"] - t0 + running, "end": w["end"] - t0 + running})
        running += dur
    total = running

    hard_breaks = [s[0] for s in seg_bounds[1:]]
    chunks = chunk_words(words, CAPTION_SKIPS, hard_breaks)
    print(f"[chunks] {len(chunks)} caption chunks")
    cap_pngs = [(render_chunk_png(c, seed=100 + i), c[0]["start"], c[-1]["end"]) for i, c in enumerate(chunks)]

    bases = {}
    for (name, t0, t1, zend) in SEGMENTS:
        im = Image.open(STILLS / name).convert("RGB")
        s = max(W / im.width, H / im.height)
        zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
        bases[name] = (im.resize((zw, zh), Image.LANCZOS), zw, zh)

    n_frames = int(total * FPS)
    proc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(SILENT)],
        stdin=subprocess.PIPE)

    for i in range(n_frames):
        t = i / FPS
        seg_t0, seg_t1, name, zend = next(s for s in seg_bounds if s[0] <= t < s[1] or s is seg_bounds[-1])
        base, zw, zh = bases[name]
        k = ease((t - seg_t0) / max(0.001, seg_t1 - seg_t0))
        z = 1.00 + (zend - 1.00) * k
        fw, fh = int(zw * z), int(zh * z)
        frame = base.resize((fw, fh), Image.LANCZOS).convert("RGBA")
        dx, dy = (fw - W) // 2, (fh - H) // 2
        frame = frame.crop((dx, dy, dx + W, dy + H))

        for (img, c0, c1) in cap_pngs:
            if c0 <= t <= c1 + 0.12:
                frame.alpha_composite(img)

        for (kind, t_in, cx, cy, payload) in CARD_EVENTS:
            dt = t - t_in
            if dt < -0.05 or dt > 3.9:
                continue
            tile = render_title_card(payload, dt) if kind == "title" else render_quote_card(payload, dt)
            if tile:
                ox, oy = int(W * cx - tile.width / 2), int(H * cy - tile.height / 2)
                frame.alpha_composite(tile, (ox, oy))

        proc.stdin.write(frame.convert("RGB").tobytes())
    proc.stdin.close()
    proc.wait()
    print(f"[ok] {SILENT}")

    aud_segs = []
    for (name, t0, t1, zend) in SEGMENTS:
        out = WORK / f"aud_{name}.aac"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(AUD),
                         "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}",
                         "-c:a", "aac", "-b:a", "192k", str(out)], check=True)
        aud_segs.append(out)
    concat_list = WORK / "_aud_concat.txt"
    concat_list.write_text("\n".join(f"file '{p.resolve().as_posix()}'" for p in aud_segs) + "\n", encoding="utf-8")
    aud_out = WORK / "_aud_full.aac"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                     "-i", str(concat_list), "-c", "copy", str(aud_out)], check=True)

    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(SILENT), "-i", str(aud_out),
                     "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                     "-b:a", "192k", "-t", f"{total:.3f}", str(OUT)], check=True)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
