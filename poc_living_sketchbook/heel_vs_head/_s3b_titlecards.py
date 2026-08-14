"""Heel vs Head -- step 3b: overlay the LOCKED sketchbook title/verse-card
standard (yellow/black title, red/white-outline quote, red/cream citation)
onto the already-assembled core cut. Ported from the sibling shorts' own
_s3b_titlecards.py -- same locked standard, including the shrink-to-fit
width-safety fix (MAX_CARD_W).

Reads HEELVSHEAD_living_sketchbook.mp4, overlays the cards, writes back
to the same filename (via a temp intermediate).

Quote+citation pair sits over s04's own window (23.21-34.78s) -- the
exact moment the narration speaks the KJV quote (Genesis 3:15's "it
shall bruise thy head, and thou shalt bruise his heel").

  .venv\\Scripts\\python.exe poc_living_sketchbook/heel_vs_head/_s3b_titlecards.py
"""
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SRC = HERE / "HEELVSHEAD_living_sketchbook.mp4"
TMP = HERE / "_titlecards_tmp.mp4"

W, H, FPS = 1080, 1920, 30
SCALE = W / 1920  # port Noah's 16:9 absolute font sizes onto this 9:16 canvas

F_BLACK = "C:/Windows/Fonts/ariblk.ttf"
CARD_INK = (30, 26, 24)
RED = (168, 34, 28)
CREAM = (243, 233, 212)
HILITE = (250, 230, 90)

SIZE_MAP = {"hilite": 66, "quote": 100, "card": 34}

# Shrink-to-fit width ceiling -- a long quote line can otherwise exceed the
# 1080px frame and clip off both edges (real bug found 2026-08-13, see
# memory sketchbook-title-verse-card-standard-LOCKED).
MAX_CARD_W = int(W * 0.84)
MIN_SCALE = 0.55


def _fit_size(lines, size):
    fitted = size
    while fitted > size * MIN_SCALE and fitted > 20:
        font = ImageFont.truetype(F_BLACK, fitted)
        pad = int(fitted * 0.35)
        tw = max(font.getbbox(ln)[2] for ln in lines)
        if tw + 4 * pad <= MAX_CARD_W:
            break
        fitted -= 2
    return fitted


def type_img(text, size, kind):
    """Verbatim port of forsaken_cry_ps221/_poc4_full_standard.py's type_img(),
    plus the shrink-to-fit width ceiling."""
    lines = text.split("\n")
    size = _fit_size(lines, size)
    font = ImageFont.truetype(F_BLACK, size)
    pad = int(size * 0.35)
    line_h = int(size * 1.18)
    tw = max(font.getbbox(ln)[2] for ln in lines)
    th = line_h * len(lines)
    canvas_w = tw + 4 * pad  # tight box hugging the text -- not a wide banner
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
            d.text((x, y), ln, font=font, fill=(*RED, 255),
                   stroke_width=3, stroke_fill=(255, 255, 255, 255))
        else:
            d.rectangle([x - int(pad * 0.5), y + int(size * 0.18),
                         x + bb[2] + int(pad * 0.5), y + int(size * 1.08)], fill=(*HILITE, 215))
            d.text((x + 4, y + 5), ln, font=font, fill=(110, 110, 110, 190))
            d.text((x, y), ln, font=font, fill=(*CARD_INK, 255))
        y += line_h
    return img.rotate(-1.5, expand=True, resample=Image.BICUBIC)


def final_size(kind):
    return int(SIZE_MAP[kind] * SCALE) if kind == "quote" else SIZE_MAP[kind]


def ease(t):
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


# (t0, t1, kind, text, cx_frac, cy_frac)
CARD_DEFS = [
    (0.3, 3.5, "hilite", "HEEL VS. HEAD.", 0.50, 0.09),
    (23.5, 34.5, "quote", "IT SHALL BRUISE\nTHY HEAD, AND THOU\nSHALT BRUISE HIS HEEL.", 0.50, 0.15),
    (23.8, 34.5, "card", "GENESIS 3:15", 0.50, 0.37),
]


def main():
    if not SRC.exists():
        raise SystemExit(f"missing: {SRC}")

    cards = [(t0, t1, type_img(text, final_size(kind), kind), cx, cy)
             for (t0, t1, kind, text, cx, cy) in CARD_DEFS]

    dur_out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(SRC)],
        capture_output=True, text=True, check=True)
    total = float(dur_out.stdout.strip())
    n_frames = int(round(total * FPS))
    print(f"[src] {SRC.name} {total:.3f}s, {n_frames} frames")

    reader = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(SRC), "-f", "rawvideo",
         "-pix_fmt", "rgb24", "-r", str(FPS), "-"],
        stdout=subprocess.PIPE)
    writer = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(TMP)],
        stdin=subprocess.PIPE)

    frame_bytes = W * H * 3
    i = 0
    while True:
        buf = reader.stdout.read(frame_bytes)
        if len(buf) < frame_bytes:
            break
        t = i / FPS
        frame = Image.frombytes("RGB", (W, H), buf).convert("RGBA")
        for (t0, t1, img, cxf, cyf) in cards:
            if t0 <= t <= t1:
                dt = t - t0
                k = ease(min(1.0, dt / 0.18))
                s2 = 1.30 - 0.30 * k
                oi = img.resize((int(img.width * s2), int(img.height * s2)), Image.LANCZOS)
                if k < 1.0:
                    oi.putalpha(oi.split()[3].point(lambda v: int(v * k)))
                ox = int(W * cxf - oi.width / 2)
                oy = int(H * cyf - oi.height / 2)
                frame.alpha_composite(oi, (ox, oy))
        writer.stdin.write(frame.convert("RGB").tobytes())
        i += 1

    reader.stdout.close()
    reader.wait()
    writer.stdin.close()
    writer.wait()
    print(f"[ok] {TMP} ({i} frames)")

    final = HERE / "HEELVSHEAD_living_sketchbook.mp4"
    backup = HERE / "_HEELVSHEAD_prewatermark_nocards.mp4"
    final.replace(backup)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(TMP), "-i", str(backup),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy",
         str(final)], check=True)
    TMP.unlink()
    print(f"[ok] {final} (title cards muxed with original audio; pre-card backup: {backup.name})")


if __name__ == "__main__":
    main()
