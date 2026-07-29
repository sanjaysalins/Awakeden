"""Piece 1 v3 "ALIVE" compositor -- the elevation pass over _compose_piece1_pages.py.
Same narration, same word timing, same page dwells. What changed (the 7 findings):

  1. DEAD PAPER KILLED: every panel slot shows its PENCIL SKETCH from second one
     (the page reads fully pencilled); on its slam the panel INKS IN via a noise
     reveal -- the comic literally draws itself as you read.
  2. BORDER BREAKS: on 2 key beats (page3 Jesus panel, page4 nailed scroll) the
     subject cutout overflows its panel border into the gutter.
  3. SFX LETTERING: a drawn THUD! burst pops on the nail slam (page4).
  4. AGED DARKER PAPER + vignette + grain so panels pop off the page.
  5. HERO SPLASH LANDING: page5's held tail becomes a full-bleed takeover of the
     new low-angle hero clip (the Bowed Camera's rationed shot, finally spent).
  6. PAGE TILT: a subtle slow perspective sway -- the page is a physical object.
  7. LINE-BOIL: calm close-up panels use the boiled clips (hand-inked wobble).
  Plus: red-letter captions get a gold inner border.

  .venv\\Scripts\\python.exe poc_comic_page/_compose_piece1_pages_v3.py page1
  .venv\\Scripts\\python.exe poc_comic_page/_compose_piece1_pages_v3.py        # all
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
BOIL = HERE / "_piece1" / "clips_v2" / "extended_boil"
SKETCH = HERE / "_piece1" / "stills_v2" / "_sketch"
CUTOUT = HERE / "_piece1" / "stills_v2" / "_cutout"
OUTDIR = HERE / "_piece1" / "pages_v3"
OUTDIR.mkdir(parents=True, exist_ok=True)

FPS = 30
W, H = 1080, 1920
SS = 1.18
MARGIN = 26
GUTTER = 12
BORDER_PX = 5
PAPER = (208, 192, 156)
INK = (35, 31, 32)
RED = (142, 31, 31)
GOLD = (201, 164, 92)
F_CAPTION = "C:/Windows/Fonts/georgiai.ttf"

SLAM_DUR = 0.18
SLAM_SCALE = 1.22
INK_IN_DUR = 0.18  # completes inside the slam flash so the reveal reads as impact energy
DIM_BASE = 0.5  # v3.1: 0.35 went muddy under the darker grade (adversarial fix 1)
HANDOFF = 0.35
ALL_UP_AFTER = 1.8
ALL_UP_DUR = 0.8
WIPE_DUR = 0.30
CAP_FADE = 0.15
SKETCH_ALPHA = 0.85
TILT_AMP = 5.0
TILT_PERIOD = 8.5

# calm close-ups that use the line-boiled clips
BOILED = {"p2c", "panel_c", "p5b", "p4a"}

# border-break cutouts: clip-stem -> (cell png, overflow scale)
# v3.1: the cutout is scaled about the SUBJECT'S OWN CENTROID so the figure
# stays pixel-registered over itself -- only the enlarged silhouette rim
# crosses the borders. Alpha keeps only the largest component (rembg junk).
BREAKS = {"panel_a": (CUTOUT / "panel_a_cell.png", 1.12),
          "p4b": (CUTOUT / "p4b_cell.png", 1.12)}

THUD = SKETCH / "_thud.png"

LAYOUTS = {
    "2x2":        [(0.0, 0.0, 0.5, 0.5), (0.5, 0.0, 0.5, 0.5),
                   (0.0, 0.5, 0.5, 0.5), (0.5, 0.5, 0.5, 0.5)],
    "2v":         [(0.0, 0.0, 1.0, 0.5), (0.0, 0.5, 1.0, 0.5)],
    "3-big-left": [(0.0, 0.0, 0.62, 1.0), (0.62, 0.0, 0.38, 0.5), (0.62, 0.5, 0.38, 0.5)],
    "3-big-top":  [(0.0, 0.0, 1.0, 0.58), (0.0, 0.58, 0.5, 0.42), (0.5, 0.58, 0.5, 0.42)],
}

PAGES = {
    "page1": dict(clips=[EXT / "p1a.mp4", EXT / "p1b.mp4"],
                  stems=["p1a", "p1b"],
                  layout="2v", total=10.08, t_ins=[0.0, 5.2],
                  captions=[
                      (0, "tl", "Somewhere in you is the quiet fear", 0.0, 2.6, False),
                      (0, "bl", "that if you actually came to God,", 2.62, 5.0, False),
                      (1, "tl", "He'd look at your record and turn you away.", 5.2, 8.0, False),
                      (1, "bl", "That fear keeps you at the door,", 8.22, 10.08, False),
                  ]),
    "page2": dict(clips=[EXT / "p2a.mp4", EXT / "p2b.mp4", EXT / "p2c.mp4"],
                  stems=["p2a", "p2b", "p2c"],
                  layout="3-big-left", total=10.96, t_ins=[0.0, 3.6, 7.34],
                  cam_sy_max=120,  # v3.1: never behead the p2b portrait (fix 4)
                  captions=[
                      (0, "tl", "rehearsing whether you're allowed in.", 0.6, 3.2, False),
                      (1, "bl", "Jesus answers it before you can ask.", 3.24, 6.0, False),
                      (2, "tl", "But listen to His own words:", 6.04, 8.5, False),
                      (0, "page_bottom", "\u201cAll that the Father giveth me shall come to me;", 8.6, 10.96, True),
                  ]),
    "page3": dict(clips=[EXT / "panel_b.mp4", EXT / "panel_a.mp4",
                         EXT / "panel_c.mp4", EXT / "panel_d.mp4"],
                  stems=["panel_b", "panel_a", "panel_c", "panel_d"],
                  layout="2x2", total=12.10, t_ins=[0.0, 3.02, 7.82, 10.1],
                  splash=dict(panel=1, t0=5.02, t1=7.55, ramp=0.28),
                  captions=[
                      (0, "page_bottom", "and him that cometh to me I will in no wise cast out.\u201d", 0.52, 4.6, True),
                      (2, "tl", "Not maybe. Not if you clean up first.", 7.82, 9.9, False),
                      (3, "bl", "You think your case might be the exception.", 10.1, 12.10, False),
                  ]),
    "page4": dict(clips=[EXT / "p4a.mp4", EXT / "p4b.mp4", EXT / "p4c.mp4"],
                  stems=["p4a", "p4b", "p4c"],
                  layout="3-big-left", total=10.64, t_ins=[0.0, 2.98, 6.5],
                  thud=dict(panel=1, t0=2.98, t1=4.9),
                  captions=[
                      (0, "tl", "Too far gone. Too late. Too much.", 0.4, 3.6, False),
                      (1, "bl", "But him that cometh has no fine print.", 4.46, 7.4, False),
                      (2, "tl", "The only way to be cast out is to never come.", 7.88, 10.64, False),
                  ]),
    "page5": dict(clips=[EXT / "p5a.mp4", EXT / "p5b.mp4", EXT / "p5c.mp4"],
                  stems=["p5a", "p5b", "p5c"],
                  layout="3-big-top", total=17.90, t_ins=None,
                  splash=dict(panel=2, t0=12.2, t1=10_000.0, ramp=0.55,
                              src=EXT / "p6_hero.mp4"),
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
    small = Image.new("L", (max(2, size[0] // 24), max(2, size[1] // 24)))
    small.putdata([rng.randint(0, 255) for _ in range(small.width * small.height)])
    return small.resize(size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(18))


def _paper_canvas(w, h, seed=11):
    """Aged paper: base tone + grain + corner vignette. Built once, copied per frame."""
    rng = random.Random(seed)
    base = Image.new("RGB", (w, h), PAPER)
    grain = Image.new("L", (w // 3, h // 3))
    grain.putdata([rng.randint(118, 138) for _ in range(grain.width * grain.height)])
    grain = grain.resize((w, h), Image.BICUBIC)
    base = Image.composite(
        ImageEnhance.Brightness(base).enhance(0.93), base,
        grain.point(lambda v: max(0, (v - 128) * 6)))
    vig = Image.new("L", (w // 4, h // 4), 0)
    dv = ImageDraw.Draw(vig)
    dv.ellipse([-vig.width * 0.25, -vig.height * 0.25,
                vig.width * 1.25, vig.height * 1.25], fill=255)
    vig = vig.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(80))
    dark = ImageEnhance.Brightness(base).enhance(0.82)
    return Image.composite(base, dark, vig)


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
    if red:
        # gold inner border -- the red-letter verse is the piece's one red moment
        inset = 9
        gpts = [(x * (bw - 2 * inset) / bw + inset, y * (bh - 2 * inset) / bh + inset)
                for x, y in pts]
        d.line(gpts, fill=(*GOLD, 255), width=3, joint="curve")
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
    clips, total, t_ins = list(cfg["clips"]), cfg["total"], cfg["t_ins"]
    stems = cfg["stems"]
    splash = cfg.get("splash")
    thud = cfg.get("thud")
    for i, stem in enumerate(stems):
        if stem in BOILED and (BOIL / f"{stem}.mp4").exists():
            clips[i] = BOIL / f"{stem}.mp4"
    n = len(clips)
    for c in clips:
        if not c.exists():
            raise SystemExit(f"[{page_key}] missing clip: {c}")
    if splash and "src" in splash and not splash["src"].exists():
        raise SystemExit(f"[{page_key}] missing splash src: {splash['src']}")

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

    # pencil sketch per cell, pre-scaled, faded onto paper
    sketches = []
    for p, stem in enumerate(stems):
        sp = SKETCH / f"{stem}_sketch.png"
        ox, oy, cw, ch = boxes[p]
        if sp.exists():
            im = Image.open(sp).convert("RGB")
            s = max(cw / im.width, ch / im.height)
            zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
            im = im.resize((zw, zh), Image.LANCZOS).crop(
                ((zw - cw) // 2, (zh - ch) // 2, (zw - cw) // 2 + cw, (zh - ch) // 2 + ch))
            paper_cell = Image.new("RGB", (cw, ch), PAPER)
            im = Image.blend(paper_cell, im, SKETCH_ALPHA)
            sketches.append(im)
        else:
            sketches.append(Image.new("RGB", (cw, ch), PAPER))

    # ink-in reveal masks (per cell, thresholded per frame)
    reveal_noise = [_noise_mask((boxes[p][2], boxes[p][3]), seed=500 + p) for p in range(n)]

    # border-break cutouts (cast shadow; scaled about the subject centroid so
    # the figure fully covers its own source -- no ghost head)
    breaks = {}
    for p, stem in enumerate(stems):
        if stem in BREAKS:
            path, scale = BREAKS[stem]
            if path.exists():
                import numpy as np
                import cv2
                cut = Image.open(path).convert("RGBA")
                a = np.array(cut.split()[3])
                n_lbl, lbl, stats, _ = cv2.connectedComponentsWithStats(
                    (a > 40).astype(np.uint8), connectivity=8)
                if n_lbl > 1:
                    big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
                    a = np.where(lbl == big, a, 0).astype(np.uint8)
                    cut.putalpha(Image.fromarray(a))
                ys, xs = np.nonzero(a)
                cyc = float(ys.mean()) if len(ys) else cut.height / 2
                cxc = float(xs.mean()) if len(xs) else cut.width / 2
                ox, oy, cw, ch = boxes[p]
                zw, zh = int(cut.width * scale), int(cut.height * scale)
                cut = cut.resize((zw, zh), Image.LANCZOS)
                sh = Image.new("RGBA", cut.size, (0, 0, 0, 0))
                sh.putalpha(cut.split()[3].point(lambda v: int(v * 0.45)))
                sh = sh.filter(ImageFilter.GaussianBlur(6))
                bx = int(ox + cxc - cxc * scale)
                by = int(oy + cyc - cyc * scale)
                breaks[p] = (cut, sh, bx, by)

    thud_img = None
    if thud and THUD.exists():
        thud_img = Image.open(THUD).convert("RGBA")
        # v3.1 fix 5: smaller, set BESIDE the nail in the empty sky corner,
        # never on top of the scroll it is shouting about
        tw = int(boxes[thud["panel"]][2] * 0.62)
        thud_img = thud_img.resize((tw, int(tw * thud_img.height / thud_img.width)),
                                   Image.LANCZOS)

    def camera_at(t: float) -> tuple[float, float]:
        acts_ = [activeness(p, t, t_ins, splash) for p in range(n)]
        w_ = [a if (t_ins is None or t >= t_ins[p]) else 0.0 for p, a in enumerate(acts_)]
        tw_ = sum(w_)
        if tw_ <= 0:
            return (ssw - W) / 2, (ssh - H) / 2
        fx_ = sum(a * c[0] for a, c in zip(w_, centers)) / tw_
        fy_ = sum(a * c[1] for a, c in zip(w_, centers)) / tw_
        sy_max = cfg.get("cam_sy_max", ssh - H)
        return (max(0, min(ssw - W, fx_ - W / 2)),
                max(0, min(min(ssh - H, sy_max), fy_ - H / 2)))

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

    work = OUTDIR / f"{page_key}_v3_work"
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
        if "src" in splash:
            cmd = ["ffmpeg", "-y", "-t", f"{t1 - t0 + 0.2:.3f}", "-i", str(splash["src"])]
        else:
            cmd = ["ffmpeg", "-y", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}",
                   "-i", str(clips[sp])]
        subprocess.run(cmd + [
            "-vf", f"scale={ssw}:{ssh}:force_original_aspect_ratio=increase,crop={ssw}:{ssh}",
            "-r", str(FPS), str(d / "f%05d.png")],
            check=True, capture_output=True)
        splash_frames = sorted(d.glob("f*.png"))
        splash_off = t0

    wipe_mask = _noise_mask((W, H)) if wipe_from else None
    prev_img = Image.open(wipe_from).convert("RGB") if wipe_from else None

    paper_base = _paper_canvas(ssw, ssh)
    tilt_phase = (hash(page_key) % 628) / 100.0

    out_dir = work / "grid_frames"
    out_dir.mkdir()
    n_frames = int(total * FPS)
    for i in range(n_frames):
        t = i / FPS
        acts = [activeness(p, t, t_ins, splash) for p in range(n)]
        canvas = paper_base.copy()
        draw = ImageDraw.Draw(canvas)

        for p in range(n):
            ox, oy, cw, ch = boxes[p]
            if t_ins is not None and t < t_ins[p]:
                # PENCIL STATE -- the page is already drawn, waiting for ink
                canvas.paste(sketches[p], (ox, oy))
                _wobbled_rect(draw, (ox, oy, ox + cw, oy + ch), 2, seed=1000 + p,
                              ink=(105, 95, 78))
                continue
            sh, sx_, sy_ = shadows[p]
            canvas.paste(sh, (sx_, sy_), sh)
            src = frame_dirs[p]
            cell = Image.open(src[i % len(src)]).convert("RGB")
            a = acts[p]
            cell = ImageEnhance.Brightness(cell).enhance(0.45 + 0.55 * a)
            cell = ImageEnhance.Contrast(cell).enhance(0.85 + 0.15 * a)
            if t_ins is not None:
                dt = t - t_ins[p]
                if dt < INK_IN_DUR:
                    # INK-IN: the live art floods over the pencil through noise
                    k = ease(dt / INK_IN_DUR)
                    thresh = int(255 * k)
                    mask = reveal_noise[p].point(lambda v: 255 if v < thresh else 0)
                    mask = mask.filter(ImageFilter.GaussianBlur(7))
                    cell = Image.composite(cell, sketches[p], mask)
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

            # BORDER BREAK -- the subject bursts past the panel edge
            if p in breaks and (t_ins is None or t >= t_ins[p] + SLAM_DUR):
                cut, shdw, bx, by = breaks[p]
                dt2 = (t - (t_ins[p] + SLAM_DUR)) if t_ins is not None else 1.0
                ka = ease(dt2 / 0.22)
                if ka > 0:
                    if ka >= 1.0:
                        canvas.paste(shdw, (bx + 8, by + 12), shdw)
                        canvas.paste(cut, (bx, by), cut)
                    else:
                        faded = cut.copy()
                        faded.putalpha(faded.split()[3].point(lambda v: int(v * ka)))
                        canvas.paste(faded, (bx, by), faded)

        if thud_img is not None and thud["t0"] <= t <= thud["t1"]:
            dt = t - thud["t0"]
            ox, oy, cw, ch = boxes[thud["panel"]]
            k = ease(min(1.0, dt / 0.2))
            s = 1.35 - 0.35 * k
            alpha = 1.0
            if thud["t1"] - t < 0.3:
                alpha = max(0.0, (thud["t1"] - t) / 0.3)
            ti = thud_img.resize((int(thud_img.width * s), int(thud_img.height * s)),
                                 Image.LANCZOS)
            if alpha < 1.0:
                ti.putalpha(ti.split()[3].point(lambda v: int(v * alpha)))
            tx = ox + int(cw * 0.72 - ti.width / 2)
            ty = oy + int(ch * 0.78 - ti.height / 2)
            canvas.paste(ti, (tx, ty), ti)

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

        # PAGE TILT -- the page is a physical object in your hands
        ph = 2 * math.pi * t / TILT_PERIOD + tilt_phase
        dx1 = TILT_AMP * math.sin(ph)
        dy1 = TILT_AMP * 0.6 * math.cos(ph * 0.8)
        pad = int(TILT_AMP * 2 + 2)
        big = Image.new("RGB", (W + 2 * pad, H + 2 * pad), PAPER)
        big.paste(frame, (pad, pad))
        quad = (pad - dx1, pad - dy1,
                pad - dx1 * 0.4, pad + H + dy1 * 0.5,
                pad + W + dx1 * 0.6, pad + H + dy1,
                pad + W + dx1, pad - dy1 * 0.4)
        frame = big.transform((W, H), Image.QUAD, quad, Image.BILINEAR)

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

    out_mp4 = OUTDIR / f"{page_key}_composite_v3.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-i", str(out_dir / "g%05d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-r", str(FPS), str(out_mp4)], check=True)
    last = sorted(out_dir.glob("g*.png"))[-1]
    last_png = OUTDIR / f"{page_key}_v3_last.png"
    shutil.copy(last, last_png)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")
    return last_png


def main():
    wanted = sys.argv[1:] or PAGE_ORDER
    cover_last = OUTDIR / "cover_last.png"
    last_by_page = {}
    for pk in PAGE_ORDER:
        if pk not in wanted:
            lp = OUTDIR / f"{pk}_v3_last.png"
            last_by_page[pk] = lp if lp.exists() else None
            continue
        idx = PAGE_ORDER.index(pk)
        if idx == 0:
            wipe_from = cover_last if cover_last.exists() else None
        else:
            wipe_from = last_by_page.get(PAGE_ORDER[idx - 1])
        last_by_page[pk] = render_page(pk, wipe_from)


if __name__ == "__main__":
    main()
