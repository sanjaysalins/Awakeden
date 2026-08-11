"""POC v4 -- the FULL standard on one short: sketchbook art + real push-in
motion + Noah's hand-ink caption + the new yellow/black title card + red/
cream verse-citation card, all in one piece, so it can be judged as a whole
before any retrofit decision on the 3 already-shipped longs.

Builds on POC3 (same 2 stills, same real narration/timing, same Noah-exact
caption fractions) and adds the second locked layer: title/citation cards,
copied verbatim from poc_castbible_look/_04_assemble.py's type_img()/OVERLAYS
recipe (Arial Black, yellow hilite / red+cream card / red+gold-underline
quote), font sizes scaled by the 1080/1920 width ratio so they read the same
relative size as Noah's own 16:9 cards. New caption skip-windows added so the
spoken caption never doubles under an active title/citation card -- same
discipline Noah's own captions use around its own title cards.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/forsaken_cry_ps221/_poc4_full_standard.py
"""
import json
import math
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.resolve().parents[2]
sys.path.insert(0, str(ROOT / "poc_castbible_look"))
from _polite import be_polite  # noqa: E402

AUD = HERE / "audio" / "narration.mp3"
STILLS = HERE / "_poc_sketchbook_stills"
WORK = HERE / "_poc4_work"
SILENT = HERE / "_poc4_silent.mp4"
OUT = HERE / "_POC4_full_standard.mp4"

W, H, FPS = 1080, 1920, 30
SCALE = W / 1920  # port Noah's 16:9 absolute font sizes onto this 9:16 canvas

# ---- Noah's exact caption constants (_finish_long.py, verbatim) ----------
F_KEEPER = "C:/Windows/Fonts/Inkfree.ttf"
INK = (35, 30, 26, 255)
PARCHMENT = (247, 242, 228)
CAPTION_Y_FRAC = 0.86
MAX_TEXT_W = int(W * 0.72)
GAP_BREAK = 0.35
MAX_WORDS = 6
MIN_CHUNK_DUR = 0.45
STROKE_W = 2
FONT_SIZE0 = 46
FONT_SIZE_MIN = 30

# ---- title/citation card constants (_04_assemble.py, verbatim colors) ----
F_BLACK = "C:/Windows/Fonts/ariblk.ttf"
CARD_INK = (30, 26, 24)
RED = (168, 34, 28)
CREAM = (243, 233, 212)
HILITE = (250, 230, 90)

# (still, window_start, window_end, zoom_end)
SEGMENTS = [
    ("s_golgotha_sketchbook.png", 9.8, 15.05, 1.06),
    ("s_bowedhead_sketchbook.png", 27.15, 31.9, 1.07),
]

# skip windows in the COMPACT poc-local timeline (seg0 local = real-9.8,
# seg1 local = real-27.15+5.25)
CAPTION_SKIPS = [(0.3, 3.5), (5.25, 9.6)]

# (t_in, t_out, card_img_builder, cx_frac, cy_frac) in poc-local time
CARD_DEFS = [
    (0.3, 3.5, "hilite", "THE FORSAKEN CRY.", 0.50, 0.09),
    (5.6, 9.5, "quote", "WHY HAST THOU\nFORSAKEN ME?", 0.50, 0.20),
    (6.0, 9.5, "card", "MATTHEW 27:46", 0.50, 0.38),
]


def ease(t):
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def type_img(text, size, kind):
    font = ImageFont.truetype(F_BLACK, size)
    lines = text.split("\n")
    pad = int(size * 0.35)
    line_h = int(size * 1.18)
    tw = max(font.getbbox(ln)[2] for ln in lines)
    th = line_h * len(lines)
    canvas_w = tw + 4 * pad  # tight box hugging the text, like Noah's own -- not a wide banner
    img = Image.new("RGBA", (canvas_w, th + 3 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = pad
    for ln in lines:
        bb = font.getbbox(ln)
        x = 2 * pad
        if kind == "card":
            d.rectangle([x - pad, y - int(pad * 0.4), x + bb[2] + pad, y + line_h], fill=(*RED, 255))
            d.text((x, y), ln, font=font, fill=(*CREAM, 255))
        elif kind == "quote":
            # red text with a white outline (echoes the citation card's red+cream
            # pairing below it), no drop shadow, no underline
            d.text((x, y), ln, font=font, fill=(*RED, 255),
                   stroke_width=3, stroke_fill=(255, 255, 255, 255))
        else:
            d.rectangle([x - int(pad * 0.5), y + int(size * 0.18),
                         x + bb[2] + int(pad * 0.5), y + int(size * 1.08)], fill=(*HILITE, 215))
            d.text((x + 4, y + 5), ln, font=font, fill=(110, 110, 110, 190))
            d.text((x, y), ln, font=font, fill=(*CARD_INK, 255))
        y += line_h
    return img.rotate(-1.5, expand=True, resample=Image.BICUBIC)


SIZE_MAP = {"hilite": 66, "quote": 110, "card": 34}


def final_size(kind):
    # hilite/card use Noah's own real pixel sizes directly (52 is "slightly
    # smaller" than Noah's 58; 34 for the citation is Noah's GENESIS 7:16
    # size verbatim) -- only "quote" still scales down for the narrower canvas.
    return int(SIZE_MAP[kind] * SCALE) if kind == "quote" else SIZE_MAP[kind]


CARDS = [(t0, t1, type_img(text, final_size(kind), kind), cx, cy)
         for (t0, t1, kind, text, cx, cy) in CARD_DEFS]


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
        wd.text((12, 8), w["w"], font=font, fill=INK, stroke_width=STROKE_W, stroke_fill=INK)
        word_img = word_img.rotate(ang, resample=Image.BICUBIC, expand=False)
        canvas.alpha_composite(word_img, (int(x + jx - 12), int(baseline_y + jy - 8)))
        x += wid + sp
    return canvas


def main():
    be_polite()
    WORK.mkdir(exist_ok=True)

    all_words = json.loads((HERE / "audio" / "alignment.json").read_text(encoding="utf-8"))
    words, running = [], 0.0
    seg_bounds = []
    for (name, t0, t1, zend) in SEGMENTS:
        dur = t1 - t0
        seg_bounds.append((running, running + dur, name, zend, t0))
        for w in all_words:
            if w["start"] >= t0 and w["end"] <= t1:
                words.append({"w": w["w"], "start": w["start"] - t0 + running, "end": w["end"] - t0 + running})
        running += dur
    total = running

    hard_breaks = [s[0] for s in seg_bounds[1:]]  # force a break at every segment seam
    chunks = chunk_words(words, CAPTION_SKIPS, hard_breaks)
    print(f"[chunks] {len(chunks)} caption chunks (after skip windows)")
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
        seg_t0, seg_t1, name, zend, real_t0 = next(s for s in seg_bounds if s[0] <= t < s[1] or s is seg_bounds[-1])
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

        for (ti, to, img, cxf, cyf) in CARDS:
            if ti <= t <= to:
                dt = t - ti
                ka = ease(min(1.0, dt / 0.18))
                s2 = 1.30 - 0.30 * ka
                oi = img.resize((int(img.width * s2), int(img.height * s2)), Image.LANCZOS)
                if ka < 1.0:
                    oi.putalpha(oi.split()[3].point(lambda v: int(v * ka)))
                ox = int(W * cxf - oi.width / 2)
                oy = int(H * cyf - oi.height / 2)
                frame.alpha_composite(oi, (ox, oy))

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
