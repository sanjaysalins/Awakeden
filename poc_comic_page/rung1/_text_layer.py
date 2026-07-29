"""Comic Page Pipeline POC -- Rung 1 Phase 2, Step 6: text layer over the
finished page composite ($0, post-composite overlay -- production will draw
text in-pass; this POC overlays it after, per _comic_text_layer.py's proven
pattern: parchment box, Georgia italic, wobbled ink border, drop shadow).

Two elements, page-relative seconds (page window is narration 21.04-33.14s):
  REF box       "JOHN 6:37"    top-left corner of the TL cell, small.
  EMPHASIS box  "IN NO WISE"   parchment band, centered in the TR cell's
                                lower third, timed to the word "wise" in the
                                STANDALONE "In no wise." emphasis line (NOT
                                the "will in no wise cast out" KJV-quote
                                occurrence) from narration.alignment.json.
Never more than one on screen at once.

  .venv\\Scripts\\python.exe poc_comic_page/rung1/_text_layer.py
"""
from __future__ import annotations
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SRC = HERE / "page3_composite.mp4"
OUT_MP4 = HERE / "page3_with_text.mp4"
OV_DIR = HERE / "_text_overlays"

W, H = 1080, 1920
INK = (32, 27, 27, 255)
PARCH = (232, 217, 181, 255)
SHADOW = (35, 31, 32, 90)
F_CAPTION = "C:/Windows/Fonts/georgiai.ttf"

# ---- timing (see _text_layer_timing_check.py for the derivation) ----------
# TL focus window 0-3.025s -> REF appears at 0.2, ends at TL_end+1.5 = 4.525
# TR focus window 3.025-6.05s -> EMPHASIS starts at word "wise" (26.06s) minus
# page start (21.04s) = 5.02s, ends at TR_end+1.5 = 7.55
REF_T_IN, REF_T_OUT = 0.2, 4.525
EMPH_T_IN, EMPH_T_OUT = 5.02, 7.55
assert REF_T_OUT <= EMPH_T_IN, "REF/EMPHASIS windows overlap -- must truncate REF end to EMPHASIS start"


def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if font.getbbox(trial)[2] <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_caption_box(text, x, y, w, size, rng, center=False):
    """Parchment box with a hand-wobbled ink border + drop shadow. If
    `center` is False the box is sized tightly to the text (top-left anchor,
    like the REF tag). If True, the box is drawn at the FIXED width `w` (a
    band) with the text centered inside it (like the EMPHASIS band)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(F_CAPTION, size)
    pad = 20
    lines = wrap(text, font, w - 2 * pad)
    line_h = size + 8
    text_w = max(font.getbbox(ln)[2] for ln in lines)
    bh = line_h * len(lines) + 2 * pad - 4
    bw = w if center else (text_w + 2 * pad)

    d.rectangle([x + 8, y + 10, x + bw + 8, y + bh + 10], fill=SHADOW)
    d.rectangle([x, y, x + bw, y + bh], fill=PARCH)
    # hand-wobbled ink border
    pts = []
    corners = [(x, y), (x + bw, y), (x + bw, y + bh), (x, y + bh), (x, y)]
    for (x0, y0), (x1, y1) in zip(corners, corners[1:]):
        for i in range(9):
            t = i / 9
            pts.append((x0 + (x1 - x0) * t + rng.uniform(-2.5, 2.5),
                        y0 + (y1 - y0) * t + rng.uniform(-2.5, 2.5)))
    pts.append(pts[0])
    d.line(pts, fill=INK, width=5, joint="curve")

    for i, ln in enumerate(lines):
        ln_w = font.getbbox(ln)[2]
        tx = x + (bw - ln_w) / 2 if center else x + pad
        d.text((tx, y + pad - 4 + i * line_h), ln, font=font, fill=INK)
    return img


def main():
    if not SRC.exists():
        raise SystemExit(f"missing source composite: {SRC}")
    OV_DIR.mkdir(parents=True, exist_ok=True)

    rng1 = random.Random(1001)
    ref_img = draw_caption_box("JOHN 6:37", x=30, y=40, w=230, size=28, rng=rng1, center=False)
    ref_png = OV_DIR / "ref_box.png"
    ref_img.save(ref_png)

    rng2 = random.Random(1002)
    emph_img = draw_caption_box("IN NO WISE", x=560, y=755, w=490, size=40, rng=rng2, center=True)
    emph_png = OV_DIR / "emphasis_box.png"
    emph_img.save(emph_png)

    print(f"REF box   '{'JOHN 6:37'}'  t={REF_T_IN}-{REF_T_OUT}  -> {ref_png}")
    print(f"EMPHASIS  '{'IN NO WISE'}' t={EMPH_T_IN}-{EMPH_T_OUT}  -> {emph_png}")

    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(SRC), "-i", str(ref_png), "-i", str(emph_png),
           "-filter_complex",
           f"[0:v][1:v]overlay=0:0:enable='between(t,{REF_T_IN},{REF_T_OUT})'[v1];"
           f"[v1][2:v]overlay=0:0:enable='between(t,{EMPH_T_IN},{EMPH_T_OUT})'[v2]",
           "-map", "[v2]", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUT_MP4)]
    subprocess.run(cmd, check=True)
    print(f"wrote {OUT_MP4}")

    frames_dir = HERE / "clips" / "_frames" / "_text_qc"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for t in [0.5, 3.0, 5.5, 7.0, 9.0, 11.5]:
        fp = frames_dir / f"t{str(t).replace('.', '_')}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(OUT_MP4),
                        "-frames:v", "1", str(fp)], check=True)
    print(f"QC frames in {frames_dir}")


if __name__ == "__main__":
    main()
