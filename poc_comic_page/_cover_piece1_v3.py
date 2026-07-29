"""v3: the 2-second COMIC COVER cold-open. The film finally announces what it
is: a comic book. Masthead + title slam + issue box over the door art, then
the assembly ink-wipes it into page 1 (compositor picks up cover_last.png).

  .venv\\Scripts\\python.exe poc_comic_page/_cover_piece1_v3.py
"""
import math
import random
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ART = HERE / "_piece1" / "stills_v2" / "panel_b_door.png"
OUTDIR = HERE / "_piece1" / "pages_v3"
OUTDIR.mkdir(parents=True, exist_ok=True)

import importlib.util
spec = importlib.util.spec_from_file_location("_c3", HERE / "_compose_piece1_pages_v3.py")
C3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C3)

W, H = 1080, 1920
FPS = 30
DUR = 1.3  # v3.1: 2.0s taxed the hook -- first word must land fast (adversarial fix 2)
PAPER = C3.PAPER
INK = C3.INK
RED = (176, 32, 28)
IVORY = (238, 226, 194)
F_BOLD = "C:/Windows/Fonts/georgiab.ttf"

MARGIN = 26
MAST_H = 240


def ease(t):
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def spaced_text(draw, xy, text, font, fill, spacing, stroke=0, stroke_fill=None,
                anchor_center_x=None):
    widths = [font.getbbox(ch)[2] - font.getbbox(ch)[0] for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x, y = xy
    if anchor_center_x is not None:
        x = anchor_center_x - total // 2
    for ch, w_ in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill,
                  stroke_width=stroke, stroke_fill=stroke_fill)
        x += w_ + spacing
    return total


def build_masthead():
    band = Image.new("RGBA", (W, MAST_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(band)
    f_main = ImageFont.truetype(F_BOLD, 118)
    f_sub = ImageFont.truetype(F_BOLD, 34)
    # AWAK in ink + EDEN in red, one continuous word, letter-spaced
    sp = 6
    widths = [f_main.getbbox(ch)[2] - f_main.getbbox(ch)[0] for ch in "AWAKEDEN"]
    total = sum(widths) + sp * 7
    x = (W - total) // 2
    y = 34
    for i, ch in enumerate("AWAKEDEN"):
        col = INK if i < 4 else RED
        d.text((x, y), ch, font=f_main, fill=col, stroke_width=3, stroke_fill=IVORY)
        x += widths[i] + sp
    spaced_text(d, (0, y + 132), "C O M I C S", f_sub, INK, 4, anchor_center_x=W // 2)
    return band


def build_title():
    img = Image.new("RGBA", (W, 560), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f1 = ImageFont.truetype(F_BOLD, 128)
    f2 = ImageFont.truetype(F_BOLD, 158)
    y = 0
    for line, f in (("IN NO WISE", f1), ("CAST OUT", f2)):
        bb = f.getbbox(line)
        tw = bb[2] - bb[0]
        x = (W - tw) // 2 - bb[0]
        # drop shadow, thick ink stroke, ivory fill
        d.text((x + 7, y + 9), line, font=f, fill=(20, 16, 14, 160), stroke_width=10,
               stroke_fill=(20, 16, 14, 160))
        d.text((x, y), line, font=f, fill=IVORY, stroke_width=10, stroke_fill=(*INK, 255))
        y += (bb[3] - bb[1]) + 46
    return img.crop(img.getbbox())


def build_issue_box():
    img = Image.new("RGBA", (300, 170), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rng = random.Random(9)
    pts = []
    corners = [(6, 6), (272, 6), (272, 150), (6, 150), (6, 6)]
    for (x0, y0), (x1, y1) in zip(corners, corners[1:]):
        for i in range(7):
            t = i / 7
            pts.append((x0 + (x1 - x0) * t + rng.uniform(-2.5, 2.5),
                        y0 + (y1 - y0) * t + rng.uniform(-2.5, 2.5)))
    pts.append(pts[0])
    d.polygon(pts, fill=(*IVORY, 255))
    d.line(pts, fill=(*INK, 255), width=5, joint="curve")
    f1 = ImageFont.truetype(F_BOLD, 60)
    f2 = ImageFont.truetype(F_BOLD, 30)
    bb = f1.getbbox("No. 1")
    d.text(((278 - bb[2]) // 2, 22), "No. 1", font=f1, fill=(*RED, 255))
    bb = f2.getbbox("JOHN 6:37")
    d.text(((278 - bb[2]) // 2, 100), "JOHN 6:37", font=f2, fill=(*INK, 255))
    return img.rotate(-4, expand=True, resample=Image.BICUBIC)


def main():
    art_full = Image.open(ART).convert("RGB")
    paper = C3._paper_canvas(W, H, seed=23)

    art_box = (MARGIN + 6, MAST_H + 10, W - MARGIN - 6, H - MARGIN - 8)
    aw, ah = art_box[2] - art_box[0], art_box[3] - art_box[1]

    masthead = build_masthead()
    title = build_title()
    tw = int(W * 0.86)
    title = title.resize((tw, int(tw * title.height / title.width)), Image.LANCZOS)
    issue = build_issue_box()

    work = OUTDIR / "cover_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()

    n_frames = int(DUR * FPS)
    for i in range(n_frames):
        t = i / FPS
        frame = paper.copy()
        d = ImageDraw.Draw(frame)

        # art panel with slow push-in (crop width-wise from the square source)
        s = 1.0 + 0.05 * (t / DUR)
        srch = art_full.height / s
        srcw = srch * aw / ah
        cx0 = (art_full.width - srcw) / 2
        cy0 = (art_full.height - srch) / 2 * 0.7
        art = art_full.crop((int(cx0), int(cy0), int(cx0 + srcw), int(cy0 + srch)))
        art = art.resize((aw, ah), Image.LANCZOS)
        frame.paste(art, (art_box[0], art_box[1]))
        C3._wobbled_rect(d, (art_box[0], art_box[1], art_box[2], art_box[3]),
                         6, seed=77)

        frame.paste(masthead, (0, 0), masthead)

        # title slams at 0.25
        if t >= 0.25:
            dt = t - 0.25
            k = ease(min(1.0, dt / 0.18))
            s2 = 1.35 - 0.35 * k
            ti = title.resize((int(title.width * s2), int(title.height * s2)),
                              Image.LANCZOS)
            if dt < 0.18:
                ti = ImageEnhance.Brightness(ti).enhance(1.0 + 0.3 * (1 - k))
            tx = (W - ti.width) // 2
            ty = int(H * 0.60) - ti.height // 2
            frame.paste(ti, (tx, ty), ti)

        # issue box stamps at 0.55
        if t >= 0.55:
            dt = t - 0.55
            k = ease(min(1.0, dt / 0.15))
            s3 = 1.45 - 0.45 * k
            ib = issue.resize((int(issue.width * s3), int(issue.height * s3)),
                              Image.LANCZOS)
            frame.paste(ib, (W - ib.width - 30, MAST_H + 26), ib)

        frame.save(work / f"c{i:05d}.png")

    out_mp4 = OUTDIR / "cover_composite_v3.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-i", str(work / "c%05d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-r", str(FPS), str(out_mp4)], check=True)
    last = sorted(work.glob("c*.png"))[-1]
    shutil.copy(last, OUTDIR / "cover_last.png")
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    main()
