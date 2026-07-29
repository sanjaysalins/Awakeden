"""Piece 1 assembly step 2: the v2.1 LIVING COMIC compositor, re-pointed at the
Gold Seam rebuild's own extended clips (poc_comic_page/_piece1/clips/extended/).
Geometry/caption/timing logic is an exact copy of rung2/_compose_pages_v2.py --
the narration and its word-timing are UNCHANGED, only the pictures changed, so
every page dwell/caption/splash timestamp carries over verbatim. panel_a (the
Jesus splash source) now comes from this piece's own extended clips too, since
all 4 page-3 panels were freshly rendered for this rebuild (the old build
borrowed panel_a from rung1; this build doesn't need to).

  .venv\\Scripts\\python.exe poc_comic_page/_compose_piece1_pages.py page1
  .venv\\Scripts\\python.exe poc_comic_page/_compose_piece1_pages.py        # all, in order
"""
from __future__ import annotations
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
EXT = HERE / "_piece1" / "clips_v2" / "extended"
OUTDIR = HERE / "_piece1" / "pages_v2"
OUTDIR.mkdir(parents=True, exist_ok=True)

FPS = 30
W, H = 1080, 1920
SS = 1.18
MARGIN = 26
GUTTER = 12
BORDER_PX = 5
PAPER = (232, 217, 181)
INK = (35, 31, 32)
RED = (142, 31, 31)
F_CAPTION = "C:/Windows/Fonts/georgiai.ttf"

SLAM_DUR = 0.18
SLAM_SCALE = 1.22
DIM_BASE = 0.35
HANDOFF = 0.35
ALL_UP_AFTER = 1.8
ALL_UP_DUR = 0.8
WIPE_DUR = 0.30
CAP_FADE = 0.15

LAYOUTS = {
    "2x2":        [(0.0, 0.0, 0.5, 0.5), (0.5, 0.0, 0.5, 0.5),
                   (0.0, 0.5, 0.5, 0.5), (0.5, 0.5, 0.5, 0.5)],
    "2v":         [(0.0, 0.0, 1.0, 0.5), (0.0, 0.5, 1.0, 0.5)],
    "3-big-left": [(0.0, 0.0, 0.62, 1.0), (0.62, 0.0, 0.38, 0.5), (0.62, 0.5, 0.38, 0.5)],
    "3-big-top":  [(0.0, 0.0, 1.0, 0.58), (0.0, 0.58, 0.5, 0.42), (0.5, 0.58, 0.5, 0.42)],
}

PAGES = {
    "page1": dict(clips=[EXT / "p1a.mp4", EXT / "p1b.mp4"],
                  layout="2v", total=10.08, t_ins=[0.0, 5.2],
                  captions=[
                      (0, "tl", "Somewhere in you is the quiet fear", 0.0, 2.6, False),
                      (0, "bl", "that if you actually came to God,", 2.62, 5.0, False),
                      (1, "tl", "He'd look at your record and turn you away.", 5.2, 8.0, False),
                      (1, "bl", "That fear keeps you at the door,", 8.22, 10.08, False),
                  ]),
    "page2": dict(clips=[EXT / "p2a.mp4", EXT / "p2b.mp4", EXT / "p2c.mp4"],
                  layout="3-big-left", total=10.96, t_ins=[0.0, 3.6, 7.34],
                  captions=[
                      (0, "tl", "rehearsing whether you're allowed in.", 0.6, 3.2, False),
                      (1, "bl", "Jesus answers it before you can ask.", 3.24, 6.0, False),
                      (2, "tl", "But listen to His own words:", 6.04, 8.5, False),
                      (0, "page_bottom", "\u201cAll that the Father giveth me shall come to me;", 8.6, 10.96, True),
                  ]),
    "page3": dict(clips=[EXT / "panel_b.mp4", EXT / "panel_a.mp4",
                         EXT / "panel_c.mp4", EXT / "panel_d.mp4"],
                  layout="2x2", total=12.10, t_ins=[0.0, 3.02, 7.82, 10.1],
                  splash=dict(panel=1, t0=5.02, t1=7.55, ramp=0.28),
                  captions=[
                      (0, "page_bottom", "and him that cometh to me I will in no wise cast out.\u201d", 0.52, 4.6, True),
                      (2, "tl", "Not maybe. Not if you clean up first.", 7.82, 9.9, False),
                      (3, "bl", "You think your case might be the exception.", 10.1, 12.10, False),
                  ]),
    "page4": dict(clips=[EXT / "p4a.mp4", EXT / "p4b.mp4", EXT / "p4c.mp4"],
                  layout="3-big-left", total=10.64, t_ins=[0.0, 2.98, 6.5],
                  captions=[
                      (0, "tl", "Too far gone. Too late. Too much.", 0.4, 3.6, False),
                      (1, "bl", "But him that cometh has no fine print.", 4.46, 7.4, False),
                      (2, "tl", "The only way to be cast out is to never come.", 7.88, 10.64, False),
                  ]),
    "page5": dict(clips=[EXT / "p5a.mp4", EXT / "p5b.mp4", EXT / "p5c.mp4"],
                  layout="3-big-top", total=17.90, t_ins=None,
                  captions=[
                      (1, "tl", "Bring the record you're ashamed of.", 2.54, 4.9, False),
                      (0, "bl", "He already read it, and still said come.", 5.9, 8.1, False),
                      (2, "tl", "The door you've been rehearsing at was never locked.", 8.24, 11.2, False),
                  ]),
}
PAGE_ORDER = ["page1", "page2", "page3", "page4", "page5"]


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def _wobbled_rect(draw, box, width, seed, ink=INK):
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    jig = max(2, width)

    def jitter_line(p0, p1, n=5):
        pts = []
        for i in range(n + 1):
            t = i / n
            x = p0[0] + (p1[0] - p0[0]) * t
            y = p0[1] + (p1[1] - p0[1]) * t
            if 0 < i < n:
                x += rng.uniform(-jig, jig)
                y += rng.uniform(-jig, jig)
            pts.append((x, y))
        draw.line(pts, fill=ink, width=width, joint="curve")

    jitter_line((x0, y0), (x1, y0))
    jitter_line((x1, y0), (x1, y1))
    jitter_line((x1, y1), (x0, y1))
    jitter_line((x0, y1), (x0, y0))


def _noise_mask(size, seed=7):
    rng = random.Random(seed)
    small = Image.new("L", (size[0] // 24, size[1] // 24))
    small.putdata([rng.randint(0, 255) for _ in range(small.width * small.height)])
    return small.resize(size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(18))


def _wrap(text, font, max_w):
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


def _caption_img(text, max_w, size, red, seed):
    font = ImageFont.truetype(F_CAPTION, size)
    pad = int(size * 0.66)
    lines = _wrap(text, font, max_w - 2 * pad)
    line_h = size + int(size * 0.28)
    text_w = max(font.getbbox(ln)[2] for ln in lines)
    bw = text_w + 2 * pad
    bh = line_h * len(lines) + 2 * pad - int(size * 0.2)
    sh = int(size * 0.3)
    img = Image.new("RGBA", (bw + sh + 4, bh + sh + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([sh, sh, bw + sh, bh + sh], fill=(35, 31, 32, 90))
    d.rectangle([0, 0, bw, bh], fill=(232, 217, 181, 255))
    rng = random.Random(seed)
    pts = []
    corners = [(0, 0), (bw, 0), (bw, bh), (0, bh), (0, 0)]
    for (x0, y0), (x1, y1) in zip(corners, corners[1:]):
        for i in range(9):
            t = i / 9
            pts.append((x0 + (x1 - x0) * t + rng.uniform(-2.5, 2.5),
                        y0 + (y1 - y0) * t + rng.uniform(-2.5, 2.5)))
    pts.append(pts[0])
    d.line(pts, fill=(*INK, 255), width=5, joint="curve")
    fill = (*RED, 255) if red else (*INK, 255)
    for i, ln in enumerate(lines):
        ln_w = font.getbbox(ln)[2]
        d.text(((bw - ln_w) / 2, pad - int(size * 0.15) + i * line_h), ln, font=font, fill=fill)
    return img


def activeness(p, t, t_ins, splash):
    if t_ins is None:
        return 1.0
    if t < t_ins[p]:
        return 0.0
    entered = [i for i in range(len(t_ins)) if t >= t_ins[i]]
    live = max(entered, key=lambda i: t_ins[i])
    last_in = max(t_ins)
    if t > last_in + ALL_UP_AFTER:
        k = ease((t - last_in - ALL_UP_AFTER) / ALL_UP_DUR)
        base = DIM_BASE + (1.0 - DIM_BASE) * k
    else:
        base = DIM_BASE
    if splash and splash["t0"] <= t <= splash["t1"]:
        return 1.0 if p == splash["panel"] else 0.25
    if p == live:
        return 1.0
    dt = t - t_ins[live]
    if dt < HANDOFF:
        prevs = [i for i in entered if i != live]
        if prevs and p == max(prevs, key=lambda i: t_ins[i]):
            return 1.0 - (1.0 - base) * ease(dt / HANDOFF)
    return base


def render_page(page_key: str, wipe_from: Path | None) -> Path:
    cfg = PAGES[page_key]
    rects = LAYOUTS[cfg["layout"]]
    clips, total, t_ins = cfg["clips"], cfg["total"], cfg["t_ins"]
    splash = cfg.get("splash")
    n = len(clips)
    for c in clips:
        if not c.exists():
            raise SystemExit(f"[{page_key}] missing clip: {c}")

    ssw, ssh = int(W * SS), int(H * SS)
    m = MARGIN * SS
    iw, ih = W * SS - 2 * m, H * SS - 2 * m
    boxes = []
    for fx, fy, fw, fh in rects:
        x0, y0 = m + fx * iw, m + fy * ih
        x1, y1 = m + (fx + fw) * iw, m + (fy + fh) * ih
        g = GUTTER * SS / 2
        boxes.append((int(x0 + g), int(y0 + g),
                      int(x1 - g) - int(x0 + g), int(y1 - g) - int(y0 + g)))
    centers = [(ox + cw / 2, oy + ch / 2) for ox, oy, cw, ch in boxes]

    shadows = []
    for (ox, oy, cw, ch) in boxes:
        off = int(7 * SS)
        pad = int(18 * SS)
        sh = Image.new("RGBA", (cw + 2 * pad, ch + 2 * pad), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle([pad, pad, pad + cw, pad + ch], fill=(20, 16, 14, 85))
        sh = sh.filter(ImageFilter.GaussianBlur(int(5 * SS)))
        shadows.append((sh, ox - pad + off, oy - pad + int(off * 1.3)))

    def camera_at(t: float) -> tuple[float, float]:
        acts_ = [activeness(p, t, t_ins, splash) for p in range(n)]
        w_ = [a if (t_ins is None or t >= t_ins[p]) else 0.0 for p, a in enumerate(acts_)]
        tw_ = sum(w_)
        if tw_ <= 0:
            return (ssw - W) / 2, (ssh - H) / 2
        fx_ = sum(a * c[0] for a, c in zip(w_, centers)) / tw_
        fy_ = sum(a * c[1] for a, c in zip(w_, centers)) / tw_
        return (max(0, min(ssw - W, fx_ - W / 2)),
                max(0, min(ssh - H, fy_ - H / 2)))

    caps = []
    WM_ZONE = (25, 55, 255, 145)
    for ci, (p, anchor, text, t_in, t_out, red) in enumerate(cfg.get("captions", [])):
        ox, oy, cw, ch = boxes[p]
        size = int(30 * SS)
        sx0, sy0 = camera_at(min(t_in + 0.05, total - 0.01))
        if anchor == "page_bottom":
            img = _caption_img(text, int(W * 0.86), int(33 * SS), red, seed=3000 + ci)
            cx = int((W - img.width) / 2)
            cy = int(H - MARGIN - img.height - 10)
        else:
            img = _caption_img(text, min(int(cw * 0.92), int(560 * SS)), size, red, seed=3000 + ci)
            inset = -6
            if anchor == "tl":
                cx, cy = int(ox - sx0) + inset, int(oy - sy0) + inset
            else:
                cx, cy = int(ox - sx0) + inset, int(oy + ch - sy0) - img.height + 6
        cx = max(8, min(cx, W - img.width - 8))
        cy = max(8, min(cy, H - img.height - 8))
        if cx < WM_ZONE[2] and cy < WM_ZONE[3]:
            cy = WM_ZONE[3] + 8
        caps.append(dict(img=img, x=cx, y=cy, t_in=t_in, t_out=t_out))

    work = OUTDIR / f"{page_key}_v2_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()

    frame_dirs = []
    for i, (c, (ox, oy, cw, ch)) in enumerate(zip(clips, boxes)):
        d = work / f"src{i}"
        d.mkdir()
        subprocess.run(["ffmpeg", "-y", "-i", str(c),
                        "-vf", f"scale={cw}:{ch}:force_original_aspect_ratio=increase,crop={cw}:{ch}",
                        "-r", str(FPS), str(d / "f%05d.png")],
                       check=True, capture_output=True)
        frame_dirs.append(sorted(d.glob("f*.png")))

    splash_frames = []
    if splash:
        sp = splash["panel"]
        t0 = max(0.0, splash["t0"] - splash["ramp"] - 0.1)
        t1 = min(total, splash["t1"] + splash["ramp"] + 0.1)
        d = work / "splash_full"
        d.mkdir()
        subprocess.run(["ffmpeg", "-y", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}",
                        "-i", str(clips[sp]),
                        "-vf", f"scale={ssw}:{ssh}:force_original_aspect_ratio=increase,crop={ssw}:{ssh}",
                        "-r", str(FPS), str(d / "f%05d.png")],
                       check=True, capture_output=True)
        splash_frames = sorted(d.glob("f*.png"))
        splash_off = t0

    wipe_mask = _noise_mask((W, H)) if wipe_from else None
    prev_img = Image.open(wipe_from).convert("RGB") if wipe_from else None

    out_dir = work / "grid_frames"
    out_dir.mkdir()
    n_frames = int(total * FPS)
    for i in range(n_frames):
        t = i / FPS
        acts = [activeness(p, t, t_ins, splash) for p in range(n)]
        canvas = Image.new("RGB", (ssw, ssh), PAPER)
        draw = ImageDraw.Draw(canvas)

        for p in range(n):
            if t_ins is not None and t < t_ins[p]:
                continue
            sh, sx_, sy_ = shadows[p]
            canvas.paste(sh, (sx_, sy_), sh)
            src = frame_dirs[p]
            cell = Image.open(src[i % len(src)]).convert("RGB")
            a = acts[p]
            cell = ImageEnhance.Brightness(cell).enhance(0.45 + 0.55 * a)
            cell = ImageEnhance.Contrast(cell).enhance(0.85 + 0.15 * a)
            ox, oy, cw, ch = boxes[p]
            if t_ins is not None:
                dt = t - t_ins[p]
                if dt < SLAM_DUR:
                    k = ease(dt / SLAM_DUR)
                    s = SLAM_SCALE - (SLAM_SCALE - 1.0) * k
                    zw, zh = int(cw * s), int(ch * s)
                    cell = cell.resize((zw, zh), Image.LANCZOS).crop(
                        ((zw - cw) // 2, (zh - ch) // 2,
                         (zw - cw) // 2 + cw, (zh - ch) // 2 + ch))
                    cell = ImageEnhance.Brightness(cell).enhance(1.0 + 0.22 * (1 - k))
            canvas.paste(cell, (ox, oy))
            _wobbled_rect(draw, (ox, oy, ox + cw, oy + ch), int(BORDER_PX * SS), seed=1000 + p)

        if splash:
            sp, t0, t1, ramp = splash["panel"], splash["t0"], splash["t1"], splash["ramp"]
            if t0 - ramp <= t <= t1 + ramp and splash_frames:
                if t < t0:
                    k = ease((t - (t0 - ramp)) / ramp)
                elif t > t1:
                    k = 1.0 - ease((t - t1) / ramp)
                else:
                    k = 1.0
                ox, oy, cw, ch = boxes[sp]
                bx = int(ox + (0 - ox) * k)
                by = int(oy + (0 - oy) * k)
                bw = int(cw + (ssw - cw) * k)
                bh = int(ch + (ssh - ch) * k)
                fi = min(len(splash_frames) - 1, max(0, int((t - splash_off) * FPS)))
                big = Image.open(splash_frames[fi]).convert("RGB").resize((bw, bh), Image.LANCZOS)
                canvas.paste(big, (bx, by))
                _wobbled_rect(draw, (bx, by, bx + bw, by + bh), int(BORDER_PX * SS), seed=1000 + sp)

        sx, sy = camera_at(t)
        frame = canvas.crop((int(sx), int(sy), int(sx) + W, int(sy) + H))

        for c in caps:
            if c["t_in"] <= t <= c["t_out"]:
                k = ease((t - c["t_in"]) / CAP_FADE) if t - c["t_in"] < CAP_FADE else 1.0
                img = c["img"]
                if k < 1.0:
                    mask = img.split()[3].point(lambda v: int(v * k))
                    frame.paste(img, (c["x"], c["y"] + int((1 - k) * 8)), mask)
                else:
                    frame.paste(img, (c["x"], c["y"]), img)

        if prev_img is not None and t < WIPE_DUR:
            k = ease(t / WIPE_DUR)
            thresh = int(255 * k)
            mask = wipe_mask.point(lambda v: 255 if v < thresh else 0)
            mask = mask.filter(ImageFilter.GaussianBlur(6))
            frame = Image.composite(frame, prev_img, mask)

        frame.save(out_dir / f"g{i:05d}.png")

    out_mp4 = OUTDIR / f"{page_key}_composite_v2.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-i", str(out_dir / "g%05d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-r", str(FPS), str(out_mp4)], check=True)
    last = sorted(out_dir.glob("g*.png"))[-1]
    last_png = OUTDIR / f"{page_key}_v2_last.png"
    shutil.copy(last, last_png)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")
    return last_png


def main():
    wanted = sys.argv[1:] or PAGE_ORDER
    last_by_page = {}
    for pk in PAGE_ORDER:
        if pk not in wanted:
            lp = OUTDIR / f"{pk}_v2_last.png"
            last_by_page[pk] = lp if lp.exists() else None
            continue
        idx = PAGE_ORDER.index(pk)
        wipe_from = last_by_page.get(PAGE_ORDER[idx - 1]) if idx > 0 else None
        last_by_page[pk] = render_page(pk, wipe_from)


if __name__ == "__main__":
    main()
