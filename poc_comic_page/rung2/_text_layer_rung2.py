"""Comic Page Pipeline POC -- Rung 2 FINAL PHASE, Step 5: text overlays for
pages 2, 3, 5 ($0, post-composite overlay). Reuses rung1's _text_layer.py
parchment-box + hand-wobbled-ink-border + drop-shadow drawing code verbatim.

Page 3 reuses rung1's EXACT timings/positions -- it is literally the same
narration window (21.04-33.14s) and same 2x2 layout as rung1's page 3.

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_text_layer_rung2.py <page> [<page> ...]
      where <page> in {page2, page3, page5}
"""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1080, 1920
INK = (32, 27, 27, 255)
PARCH = (232, 217, 181, 255)
SHADOW = (35, 31, 32, 90)
F_CAPTION = "C:/Windows/Fonts/georgiai.ttf"
OV_DIR = HERE / "_text_overlays"
OV_DIR.mkdir(parents=True, exist_ok=True)


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


# ---- per-page element config ----------------------------------------------
# each element: (tag, text, x, y, w, size, center, t_in, t_out)
PAGES = {
    "page2": dict(
        src=HERE / "page2_composite.mp4", out=HERE / "page2_with_text.mp4",
        elements=[
            # y=140: below the AWAKEDEN watermark (40,70,~200px) burned in at mux time
            ("ref", "JOHN 6:37", 30, 140, 230, 28, False, 8.60, 10.96),
        ],
        qc_ts=[0.5, 4.0, 8.6, 9.5, 10.9],
    ),
    "page3": dict(
        src=HERE / "page3_composite.mp4", out=HERE / "page3_with_text.mp4",
        elements=[
            ("ref", "JOHN 6:37", 30, 140, 230, 28, False, 0.2, 4.525),
            ("emphasis", "IN NO WISE", 560, 755, 490, 40, True, 5.02, 7.55),
        ],
        qc_ts=[0.5, 3.0, 5.5, 7.0, 9.0, 11.5],
    ),
    "page5": dict(
        src=HERE / "page5_composite.mp4", out=HERE / "page5_with_text.mp4",
        elements=[
            ("emphasis", "COME", 290, 870, 500, 48, True, 1.52, 5.86),
        ],
        qc_ts=[0.5, 1.5, 3.5, 5.9, 10.0, 13.5],
    ),
}


def build_page(page_key):
    cfg = PAGES[page_key]
    src, out = cfg["src"], cfg["out"]
    if not src.exists():
        raise SystemExit(f"missing source composite: {src}")

    ov_pngs = []
    for i, (tag, text, x, y, w, size, center, t_in, t_out) in enumerate(cfg["elements"]):
        rng = random.Random(2000 + i)
        img = draw_caption_box(text, x, y, w, size, rng, center=center)
        png = OV_DIR / f"{page_key}_{tag}.png"
        img.save(png)
        ov_pngs.append((png, t_in, t_out))
        print(f"{page_key} {tag:10s} '{text}'  t={t_in}-{t_out}  -> {png}")

    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src)]
    for png, _, _ in ov_pngs:
        cmd += ["-i", str(png)]
    filt_parts = []
    prev = "0:v"
    for i, (_, t_in, t_out) in enumerate(ov_pngs):
        label = f"v{i+1}"
        filt_parts.append(f"[{prev}][{i+1}:v]overlay=0:0:enable='between(t,{t_in},{t_out})'[{label}]")
        prev = label
    cmd += ["-filter_complex", ";".join(filt_parts), "-map", f"[{prev}]",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    print(f"wrote {out}")

    frames_dir = HERE / "clips" / "_frames" / f"_text_qc_{page_key}"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for t in cfg["qc_ts"]:
        fp = frames_dir / f"t{str(t).replace('.', '_')}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(out),
                        "-frames:v", "1", str(fp)], check=True)
    print(f"QC frames in {frames_dir}")


if __name__ == "__main__":
    pages = sys.argv[1:] or list(PAGES.keys())
    for p in pages:
        build_page(p)
