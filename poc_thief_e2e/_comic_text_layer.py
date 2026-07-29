"""Comic text-box layer POC (2026-07-25): code-drawn speech bubbles + parchment
caption boxes overlaid on an ALREADY-ANIMATED recomposited comic page — $0, no
generation spend, PIL + ffmpeg only.

Why post-composite text (locked reasoning, COMIC_STRIP_NATIVE_SPEC.md section 3):
baked text garbles under animation ("FLESH UNT THE BUCKS OF HE AIR"), costs a
full re-render to fix a typo, and can't be timed to narration. Code-drawn text
on top of the finished panel clips is crisp, KJV-verbatim-checkable, timed, and
free to fix.

Source: poc_thief_e2e/clips/_crop_test/page2_recomposite.mp4  (1536x2752, 12s,
grid_choreography 2x2 spotlight sweep, per_panel=3s)
Text: Luke 23:40-43 KJV, verbatim from data/kjv_cache.json. Jesus' words in
red-letter per printed-KJV convention (design choice to confirm with user).

Run:
  .venv\\Scripts\\python.exe poc_thief_e2e/_comic_text_layer.py
"""
from __future__ import annotations

import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
SRC = HERE / "clips" / "_crop_test" / "page2_recomposite.mp4"
OUT_DIR = HERE / "clips" / "_text_layer"
OV_DIR = OUT_DIR / "overlays"
OUT_MP4 = OUT_DIR / "page2_with_text.mp4"

W, H = 1536, 2752
INK = (32, 27, 27, 255)
RED_LETTER = (139, 26, 26, 255)
IVORY = (247, 243, 230, 255)
PARCH = (232, 217, 181, 255)
SHADOW = (35, 31, 32, 80)

F_BUBBLE = "C:/Windows/Fonts/comicbd.ttf"
F_CAPTION = "C:/Windows/Fonts/georgiai.ttf"

# (kind, text, geometry..., t_in). All coords in 1536x2752 canvas space.
# bubble: (cx, cy) ellipse centre, max text width px, tail anchor point.
# caption: (x, y) top-left, box width px.
# NOTE (learned by eye-check): grid_choreography's virtual camera slides the
# panel art under these static overlays — the top row compresses once the
# focus moves on. So top-row text must anchor near the TOP of its cell, and
# tails aim at where the mouth sits during that panel's focus window. The
# production tool should draw text cell-relative inside the choreography pass.
ELEMENTS = [
    dict(kind="bubble", t_in=0.7, cx=390, cy=185, tw=470, size=38,
         tail=(40, 720),  # speaker (the penitent) is OFF-PANEL LEFT — the
         # figure drawn in this panel reads as Christ; the tail must never
         # attribute the rebuke to him
         text="Dost not thou fear God, seeing thou art in the same condemnation?"),
    dict(kind="caption", t_in=0.2, x=260, y=336, w=420, size=32,
         text="But the other answering rebuked him, saying,"),
    dict(kind="bubble", t_in=3.5, cx=1020, cy=290, tw=430, size=36,
         tail=(1240, 1120),
         text="And we indeed justly; for we receive the due reward of our deeds: "
              "but this man hath done nothing amiss."),
    dict(kind="bubble", t_in=6.5, cx=520, cy=1560, tw=400, size=38,
         tail=(480, 2220), tail_cap=340,
         text="Lord, remember me when thou comest into thy kingdom."),
    dict(kind="caption", t_in=9.3, x=800, y=1412, w=430, size=34,
         text="And Jesus said unto him,"),
    dict(kind="bubble", t_in=9.8, cx=1030, cy=1930, tw=440, size=38,
         tail=(1145, 1855), red=True,  # below the face, short tail UP to the
         # chin — never cover the speaker's mouth
         text="Verily I say unto thee, To day shalt thou be with me in paradise."),
]


def wrap(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
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


def wobble_poly(cx: float, cy: float, rx: float, ry: float,
                rng: random.Random, n: int = 56, j: float = 4.0):
    import math
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        r_j = 1.0 + rng.uniform(-j, j) / max(rx, ry)
        pts.append((cx + rx * r_j * math.cos(a), cy + ry * r_j * math.sin(a)))
    return pts


def draw_bubble(el: dict, rng: random.Random) -> Image.Image:
    import math
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(F_BUBBLE, el["size"])
    lines = wrap(el["text"].upper(), font, el["tw"])
    line_h = el["size"] + 10
    tw = max(font.getbbox(ln)[2] for ln in lines)
    th = line_h * len(lines)
    rx = tw / 2 * 1.22 + 30
    ry = th / 2 * 1.35 + 26
    cx, cy = el["cx"], el["cy"]
    # keep the ellipse on-canvas
    cx = max(rx + 8, min(W - rx - 8, cx))
    cy = max(ry + 8, min(H - ry - 8, cy))

    # tail geometry: base on ellipse edge toward anchor, capped length
    ax, ay = el["tail"]
    ang = math.atan2(ay - cy, ax - cx)
    edge = (cx + rx * 0.92 * math.cos(ang), cy + ry * 0.92 * math.sin(ang))
    dist = math.hypot(ax - edge[0], ay - edge[1])
    cap = min(dist, float(el.get("tail_cap", 270)))
    tip = (edge[0] + cap * math.cos(ang), edge[1] + cap * math.sin(ang))
    spread = 0.38
    b1 = (cx + rx * 0.9 * math.cos(ang - spread), cy + ry * 0.9 * math.sin(ang - spread))
    b2 = (cx + rx * 0.9 * math.cos(ang + spread), cy + ry * 0.9 * math.sin(ang + spread))

    poly = wobble_poly(cx, cy, rx, ry, rng)
    # drop shadow (bubble + tail), offset like a print layer
    sh = ImageDraw.Draw(img)
    sh.polygon([(x + 9, y + 12) for x, y in poly], fill=SHADOW)
    sh.polygon([(b1[0] + 9, b1[1] + 12), (tip[0] + 9, tip[1] + 12),
                (b2[0] + 9, b2[1] + 12)], fill=SHADOW)
    # tail under the bubble body
    d.polygon([b1, tip, b2], fill=IVORY, outline=INK)
    d.line([b1, tip, b2], fill=INK, width=6, joint="curve")
    # bubble body
    d.polygon(poly, fill=IVORY)
    d.line(poly + [poly[0]], fill=INK, width=7, joint="curve")
    # second, lighter jittered stroke for the hand-inked feel
    poly2 = wobble_poly(cx, cy, rx - 2, ry - 2, rng)
    d.line(poly2 + [poly2[0]], fill=INK, width=2, joint="curve")

    color = RED_LETTER if el.get("red") else INK
    y0 = cy - th / 2 + 2
    for i, ln in enumerate(lines):
        lw = font.getbbox(ln)[2]
        d.text((cx - lw / 2, y0 + i * line_h), ln, font=font, fill=color)
    return img


def draw_caption(el: dict, rng: random.Random) -> Image.Image:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(F_CAPTION, el["size"])
    pad = 20
    lines = wrap(el["text"], font, el["w"] - 2 * pad)
    line_h = el["size"] + 8
    bw = max(font.getbbox(ln)[2] for ln in lines) + 2 * pad
    bh = line_h * len(lines) + 2 * pad - 4
    x, y = el["x"], el["y"]

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
        d.text((x + pad, y + pad - 4 + i * line_h), ln, font=font, fill=INK)
    return img


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing source clip: {SRC}")
    OV_DIR.mkdir(parents=True, exist_ok=True)

    overlays = []
    for i, el in enumerate(ELEMENTS):
        rng = random.Random(1000 + i)
        img = draw_bubble(el, rng) if el["kind"] == "bubble" else draw_caption(el, rng)
        p = OV_DIR / f"el{i}_{el['kind']}.png"
        img.save(p)
        overlays.append((p, el["t_in"]))
        print(f"overlay {p.name} (t_in={el['t_in']})")

    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(SRC)]
    for p, _ in overlays:
        cmd += ["-i", str(p)]
    steps, prev = [], "0:v"
    for i, (_, t_in) in enumerate(overlays):
        out = f"v{i}"
        steps.append(f"[{prev}][{i + 1}:v]overlay=0:0:enable='gte(t,{t_in})'[{out}]")
        prev = out
    cmd += ["-filter_complex", ";".join(steps), "-map", f"[{prev}]",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUT_MP4)]
    subprocess.run(cmd, check=True)
    print(f"wrote {OUT_MP4}")

    frames_dir = OUT_DIR / "_frames"
    frames_dir.mkdir(exist_ok=True)
    for t in [1.0, 4.5, 7.5, 10.2, 11.9]:
        fp = frames_dir / f"t{str(t).replace('.', '_')}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i",
                        str(OUT_MP4), "-frames:v", "1", str(fp)], check=True)
    print(f"QC frames in {frames_dir}")


if __name__ == "__main__":
    main()
