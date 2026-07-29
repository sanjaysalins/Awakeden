#!/usr/bin/env python
"""POC — 'Infographic Animator' analog in our locked ink/parchment style.

Same technique family as mapengine.py (frame-by-frame PIL compositing +
ffmpeg encode, dashed-glow line reveal, pill-plaque labels, gentle camera
push) applied to a TYPOLOGY comparison card instead of a map route:
Numbers 21:9 (bronze serpent lifted up) -> John 3:14 (the Son lifted up).

$0, deterministic, no generative model involved.
"""
from __future__ import annotations
import math
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
FPS = 30
DURATION_S = 6.0

# palette lifted straight from mapengine.py (locked ink/gold/cream)
INK = (54, 36, 22)
PARCHMENT_LO = (35, 27, 20)
PARCHMENT_HI = (58, 46, 34)
ROUTE = (168, 44, 28)
GLOW = (214, 96, 52)
GOLD = (196, 150, 62)
PILL = (241, 228, 200, 235)

FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/BOOKOSB.TTF", 64)
FONT_LABEL = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 40)
FONT_REF = ImageFont.truetype("C:/Windows/Fonts/georgiai.ttf", 30)

LEFT = (W * 0.27, H * 0.52)
RIGHT = (W * 0.73, H * 0.52)


def make_parchment() -> Image.Image:
    """Procedural ink/parchment backdrop — vignette + grain, no external asset."""
    yy, xx = np.mgrid[0:H, 0:W]
    cx, cy = W / 2, H / 2
    d = np.sqrt(((xx - cx) / (W * 0.75)) ** 2 + ((yy - cy) / (H * 0.75)) ** 2)
    t = np.clip(d, 0, 1)
    base = np.zeros((H, W, 3), dtype=float)
    for c in range(3):
        base[..., c] = PARCHMENT_HI[c] * (1 - t) + PARCHMENT_LO[c] * t
    rng = np.random.default_rng(7)
    grain = rng.normal(0, 5.0, (H, W, 1))
    base = np.clip(base + grain, 0, 255).astype("uint8")
    img = Image.fromarray(base, "RGB")
    return img.filter(ImageFilter.GaussianBlur(0.6))


def draw_serpent_icon(layer: Image.Image, cx: float, cy: float, alpha: float, scale: float = 1.0):
    if alpha <= 0.02:
        return
    ic = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ic)
    pts = []
    n = 40
    for i in range(n + 1):
        t = i / n
        x = cx - 70 * scale + 140 * scale * t
        y = cy + 46 * scale * math.sin(t * math.pi * 2.4) * (1 - t * 0.15)
        pts.append((x, y))
    d.line(pts, fill=(*GOLD, 255), width=int(7 * scale), joint="curve")
    hx, hy = pts[-1]
    d.ellipse([hx - 9 * scale, hy - 9 * scale, hx + 9 * scale, hy + 9 * scale], fill=(*GOLD, 255))
    # pole
    d.line([(cx, cy + 70 * scale), (cx, cy - 90 * scale)], fill=(*INK, 255), width=int(6 * scale))
    if alpha < 1:
        ic.putalpha(ic.getchannel("A").point(lambda a: int(a * alpha)))
    layer.alpha_composite(ic)


def draw_cross_icon(layer: Image.Image, cx: float, cy: float, alpha: float, scale: float = 1.0):
    if alpha <= 0.02:
        return
    ic = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ic)
    d.line([(cx, cy - 90 * scale), (cx, cy + 90 * scale)], fill=(*GOLD, 255), width=int(9 * scale))
    d.line([(cx - 55 * scale, cy - 30 * scale), (cx + 55 * scale, cy - 30 * scale)],
           fill=(*GOLD, 255), width=int(9 * scale))
    if alpha < 1:
        ic.putalpha(ic.getchannel("A").point(lambda a: int(a * alpha)))
    layer.alpha_composite(ic)


def draw_plaque(layer: Image.Image, cx: float, y: float, ref: str, label: str, alpha: float):
    if alpha <= 0.02:
        return
    pl = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(pl)
    bb = d.textbbox((0, 0), label, font=FONT_LABEL)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad_x, pad_y = 26, 16
    box = [cx - tw / 2 - pad_x, y - th / 2 - pad_y, cx + tw / 2 + pad_x, y + th / 2 + pad_y]
    d.rounded_rectangle(box, radius=14, fill=PILL, outline=(*INK, 255), width=2)
    d.text((cx - tw / 2, y - th / 2 - bb[1]), label, font=FONT_LABEL, fill=(*INK, 255))
    rbb = d.textbbox((0, 0), ref, font=FONT_REF)
    rtw = rbb[2] - rbb[0]
    d.text((cx - rtw / 2, box[3] + 10), ref, font=FONT_REF, fill=(*GOLD, 255))
    if alpha < 1:
        pl.putalpha(pl.getchannel("A").point(lambda a: int(a * alpha)))
    layer.alpha_composite(pl)


def draw_connector(layer: Image.Image, progress: float):
    """Dashed glowing line drawn left -> right, same technique as mapengine.draw_route."""
    if progress <= 0:
        return
    x0, y0 = LEFT[0] + 90, LEFT[1]
    x1, y1 = RIGHT[0] - 90, RIGHT[1]
    tip_x = x0 + (x1 - x0) * progress
    glow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    d = ImageDraw.Draw(layer)
    dash, gap = 22, 14
    x = x0
    while x < tip_x:
        seg_end = min(x + dash, tip_x)
        gd.line([(x, y0), (seg_end, y1)], fill=(*GLOW, 255), width=14)
        x = seg_end + gap
    layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(8)))
    x = x0
    while x < tip_x:
        seg_end = min(x + dash, tip_x)
        d.line([(x, y0), (seg_end, y1)], fill=(*ROUTE, 255), width=5)
        x = seg_end + gap
    # arrowhead at the tip once it nears the right node
    if progress > 0.92:
        ah = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        ad = ImageDraw.Draw(ah)
        ad.polygon([(tip_x, y1), (tip_x - 22, y1 - 12), (tip_x - 22, y1 + 12)], fill=(*GOLD, 255))
        layer.alpha_composite(ah)


def draw_title(layer: Image.Image, alpha: float):
    if alpha <= 0.02:
        return
    tl = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(tl)
    title = "THE PATTERN"
    sub = "lifted up in the wilderness  •  lifted up on the tree"
    bb = d.textbbox((0, 0), title, font=FONT_TITLE)
    tw = bb[2] - bb[0]
    cx = W / 2
    d.text((cx - tw / 2, 70), title, font=FONT_TITLE, fill=(*GOLD, 255))
    sbb = d.textbbox((0, 0), sub, font=FONT_REF)
    d.text((cx - (sbb[2] - sbb[0]) / 2, 150), sub, font=FONT_REF, fill=(230, 220, 200, 255))
    if alpha < 1:
        tl.putalpha(tl.getchannel("A").point(lambda a: int(a * alpha)))
    layer.alpha_composite(tl)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def apply_camera(frame: Image.Image, zoom: float) -> Image.Image:
    if zoom <= 1.0001:
        return frame
    cw, ch = W / zoom, H / zoom
    x0 = (W - cw) / 2
    y0 = (H - ch) / 2 - 20
    return frame.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)


def render(out_mp4: Path):
    n_frames = int(DURATION_S * FPS)
    parchment = make_parchment()

    frames_dir = out_mp4.parent / (out_mp4.stem + "_frames")
    if frames_dir.exists():
        shutil.rmtree(frames_dir)
    frames_dir.mkdir(parents=True)

    # timeline (seconds): title in 0-0.8 | left node 0.4-1.0 | connector 1.2-3.0
    # | right node 3.0-3.6 | hold | title-out fade last 0.8s
    for idx in range(n_frames):
        t = idx / FPS
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))

        title_a = ease((t - 0.1) / 0.6)
        draw_title(layer, min(title_a, 1.0))

        left_a = ease((t - 0.4) / 0.6)
        draw_serpent_icon(layer, LEFT[0], LEFT[1] - 40, min(left_a, 1.0))
        draw_plaque(layer, LEFT[0], LEFT[1] + 90, "NUMBERS 21:9", "LIFTED UP THE SERPENT",
                    min(left_a, 1.0))

        conn_prog = ease((t - 1.2) / 1.8)
        draw_connector(layer, min(conn_prog, 1.0))

        right_a = ease((t - 3.0) / 0.6)
        draw_cross_icon(layer, RIGHT[0], RIGHT[1] - 40, min(right_a, 1.0))
        draw_plaque(layer, RIGHT[0], RIGHT[1] + 90, "JOHN 3:14", "LIFTED UP THE SON",
                    min(right_a, 1.0))

        frame = parchment.convert("RGBA").copy()
        frame.alpha_composite(layer)
        zoom = 1.0 + 0.05 * (idx / n_frames)
        apply_camera(frame.convert("RGB"), zoom).save(frames_dir / f"f{idx:05d}.png")

    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
         "-i", str(frames_dir / "f%05d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), str(out_mp4)],
        check=True,
    )
    shutil.rmtree(frames_dir)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    render(Path(__file__).resolve().parent / "POC2_infographic_animator.mp4")
