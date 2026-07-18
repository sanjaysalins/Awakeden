#!/usr/bin/env python
"""Halftone + print-texture grade pass -- a final polish pass that pushes a
rendered clip from "nice 2D illustration" toward "looks like an actual
printed comic": a subtle 45-degree halftone dot screen (multiply-blended,
so it reads in the shading/midtones, not as a flat overlay), a couple pixels
of CMYK-style channel misregistration, and light film grain.

$0, deterministic: one PIL-generated tileable dot texture + an ffmpeg filter
chain. No per-clip regeneration needed -- the texture is reusable across
every episode (like the ink caption band / arrow).

Usage:
    python print_grade.py --clip clip.mp4 --out clip_graded.mp4
        [--halftone 0.10] [--fringe 2] [--grain 6]
"""
from __future__ import annotations
import argparse
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"


def make_halftone_screen(w: int, h: int, cell: int = 10, angle_deg: float = 45.0) -> Image.Image:
    """A full-frame 45-degree dot screen sized exactly to the clip (dots drawn
    directly at WxH, not stretched from a small tile -- stretching a tile
    would distort the dot pitch/shape). Dark dots on a transparent field;
    multiply-blend this over the clip so paper/print texture shows in the
    midtones without flattening the highlights."""
    import math
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    a = math.radians(angle_deg)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    r = cell * 0.34
    diag = int((w ** 2 + h ** 2) ** 0.5) // 2 + cell
    for i in range(-diag // cell, diag // cell):
        for j in range(-diag // cell, diag // cell):
            x = w / 2 + (i * cell) * ux + (j * cell) * vx
            y = h / 2 + (i * cell) * uy + (j * cell) * vy
            if -r <= x <= w + r and -r <= y <= h + r:
                d.ellipse([x - r, y - r, x + r, y + r], fill=(20, 16, 12, 235))
    return img


def ensure_texture(w: int, h: int) -> Path:
    ASSETS.mkdir(exist_ok=True)
    texture = ASSETS / f"halftone_screen_{w}x{h}.png"
    if not texture.exists():
        make_halftone_screen(w, h).save(texture)
        print(f"wrote {texture}")
    return texture


def _duration(clip: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(clip)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def render(clip: Path, out_mp4: Path, halftone: float, fringe: int, grain: int):
    w, h = _probe(clip)
    texture = ensure_texture(w, h)
    dur = _duration(clip)

    # `-loop 1` makes the still an infinite stream; `blend` doesn't stop on the
    # shorter input on its own, and `-shortest` on the output didn't cut it
    # either -- ffmpeg kept encoding well past the clip's real length. Capping
    # the looped image input to the clip's own duration with `-t` bounds the
    # whole filter graph deterministically.
    filter_complex = (
        f"[0:v][1:v]blend=all_mode=multiply:all_opacity={halftone}[ht];"
        f"[ht]rgbashift=rh=-{fringe}:bh={fringe}[fr];"
        f"[fr]noise=alls={grain}:allf=t+u[out]"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(clip), "-loop", "1", "-t", f"{dur:.3f}", "-i", str(texture),
         "-filter_complex", filter_complex, "-map", "[out]", "-map", "0:a?",
         "-t", f"{dur:.3f}",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-shortest", str(out_mp4)],
        check=True, capture_output=True,
    )
    print(f"[ok] {out_mp4}")


def _probe(clip: Path) -> tuple[int, int]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", str(clip)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    w, h = out.split("x")
    return int(w), int(h)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--halftone", type=float, default=0.07, help="0..1 multiply opacity")
    ap.add_argument("--fringe", type=int, default=1, help="px channel misregistration")
    ap.add_argument("--grain", type=int, default=5, help="ffmpeg noise strength")
    a = ap.parse_args()
    render(Path(a.clip), Path(a.out), a.halftone, a.fringe, a.grain)
