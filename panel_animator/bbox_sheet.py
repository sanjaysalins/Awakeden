"""bbox_sheet.py -- grid-overlay tool so picking a motion-device bounding box
takes seconds instead of a minute of eyeballing. Born from the Day of
Atonement retrospective: Raking Light became a lazy zero-bbox default on
21/76 spreads (28%) purely because it's the only hold device that doesn't
need a per-still bbox pick -- pure tooling friction, not a creative choice
(memory `day-of-atonement-retro-learnings` fix #2).

Draws a labeled 10%-grid (5%-minor-tick) over each still, scale-cropped to
the film's own 1920x1080 frame -- the SAME percent-of-frame units every
device's own "bbox": [x, y, w, h] param already uses (x,y = top-left corner,
w,h = width/height, all 0-100; see panel_animator/focal_tour.py::focal_to_px).
Read the numbers straight off the sheet, no more eyeballing.

  .venv\\Scripts\\python.exe panel_animator/bbox_sheet.py <still.png> [<still2.png> ...] [--out <dir>] [--grid 10]
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FONT_PATH = "C:/Windows/Fonts/consola.ttf"


def scale_crop(src: Path, dst: Path) -> None:
    """Match the film's own scale-crop-to-1920x1080 convention exactly."""
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src),
         "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
         "-frames:v", "1", str(dst)],
        check=True,
    )


def draw_grid(img: Image.Image, major: int, minor: int) -> Image.Image:
    canvas = img.convert("RGB").copy()
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype(FONT_PATH, 20)
    except OSError:
        font = ImageFont.load_default()

    def line(x0, y0, x1, y1, alpha_minor=False):
        # double-stroke (black under white) so it reads on any art
        w = 1
        draw.line([x0, y0, x1, y1], fill=(0, 0, 0), width=w + 1)
        draw.line([x0, y0, x1, y1], fill=(255, 255, 255) if not alpha_minor else (220, 220, 220), width=w)

    for pct in range(0, 101, minor):
        x = round(pct / 100.0 * W)
        line(x, 0, x, H, alpha_minor=(pct % major != 0))
    for pct in range(0, 101, minor):
        y = round(pct / 100.0 * H)
        line(0, y, W, y, alpha_minor=(pct % major != 0))

    for pct in range(0, 101, major):
        x = round(pct / 100.0 * W)
        label = f"{pct}"
        draw.rectangle([x + 2, 2, x + 2 + len(label) * 12 + 4, 24], fill=(0, 0, 0))
        draw.text((x + 4, 3), label, font=font, fill=(255, 255, 0))
    for pct in range(0, 101, major):
        y = round(pct / 100.0 * H)
        label = f"{pct}"
        draw.rectangle([2, y + 2, 2 + len(label) * 12 + 4, y + 24], fill=(0, 0, 0))
        draw.text((4, y + 3), label, font=font, fill=(255, 255, 0))

    return canvas


def build_sheet(still: Path, out_dir: Path, major: int, minor: int) -> Path:
    with tempfile.TemporaryDirectory() as td:
        cropped = Path(td) / "crop.png"
        scale_crop(still, cropped)
        img = Image.open(cropped)
        sheet = draw_grid(img, major, minor)
    out = out_dir / f"{still.stem}_bboxsheet.png"
    sheet.save(out)
    return out


def write_index(out_dir: Path, sheets: list[Path]) -> Path:
    rows = "\n".join(
        f'<div style="margin:12px 0"><h3>{s.stem}</h3>'
        f'<img src="{s.name}" style="width:100%;max-width:1200px;border:1px solid #444"></div>'
        for s in sheets
    )
    html = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>bbox sheets</title>"
        "<style>body{background:#111;color:#eee;font-family:sans-serif;padding:20px}</style>"
        f"</head><body><h1>bbox sheets ({len(sheets)})</h1>{rows}</body></html>"
    )
    out = out_dir / "bbox_sheet_index.html"
    out.write_text(html, encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stills", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--grid", type=int, default=10, help="major grid line spacing in percent")
    args = ap.parse_args()

    out_dir = args.out or args.stills[0].parent
    out_dir.mkdir(parents=True, exist_ok=True)
    minor = max(1, args.grid // 2)

    sheets = []
    for still in args.stills:
        if not still.exists():
            sys.exit(f"missing still: {still}")
        sheet = build_sheet(still, out_dir, args.grid, minor)
        sheets.append(sheet)
        print(f"  [ok] {sheet}")

    idx = write_index(out_dir, sheets)
    print(f"[done] {len(sheets)} sheet(s) -> {idx}")


if __name__ == "__main__":
    main()
