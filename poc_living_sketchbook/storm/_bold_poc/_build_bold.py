"""BOLD POC (pre-lock taste test) -- four brave devices on real Storm spreads,
all $0 deterministic:

  1  bold_1_erasure.mp4    s01: at the rebuke the storm is SCRUBBED OUT --
     violent eraser strokes wipe the drawing to blank paper (crumbs left
     behind), hold on the blankness, then one steady Keeper line:
     "and it was gone." He didn't fight the storm; He removed it.
  2  bold_2_torn_page.mp4  s03 -> s04: the Keeper RIPS the panic page out of
     the book on camera -- grab, lift, tear away right (white deckle on the
     flying page), the next page already waiting beneath. Rip SFX cue at the
     release. GOVERNOR: never tear out a page carrying the Word.
  3  bold_3_bleed.mp4      s01: the panic entry writes, then a drop hits
     "fear." and it BLOOMS -- ink darkening, blurring, running down the page
     in thin trails. Rain or tears; the page doesn't say.
  4  bold_4_dive.mp4       s01: the camera starts at the masthead and
     PLUNGES down the mast to the waterline -- one drawing, one drop,
     arriving with a shudder. (POC crops the 2k still directly; production
     would supersample the composite so the zoom stays crisp.)

  ..\\..\\..\\.venv\\Scripts\\python.exe _build_bold.py
"""
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
STORM = HERE.parent
sys.path.insert(0, str(STORM.parents[1] / "panel_animator"))
sys.path.insert(0, str(STORM / "_keeper_poc"))
from raking_light import scale_crop  # noqa: E402
from _build_poc import entry_events, compose_at, KEEPER_INK, F_KEEPER  # noqa: E402

FPS = 30
W, H = 1080, 1920
PAPER = (238, 226, 194)


def render(name, frame_fn, dur):
    work = HERE / f"_{name}_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    n = int(dur * FPS)
    for i in range(n):
        frame_fn(i / FPS).save(work / f"f{i:05d}.png")
    out = HERE / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out}")


def smootherstep(t):
    t = min(1.0, max(0.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


# ---------------------------------------------------------------- 1 ERASURE


def _eraser_strokes(region, seed=5):
    """Scrub strokes in wrist order, heavily overlapped and angle-jittered so
    no row banding survives, ending with four flat-of-the-eraser polish sweeps
    that leave the region fully clean. Crumbs only near the end of the scrub
    (they accumulate as the work finishes), sparse."""
    x0, y0, x1, y1 = region
    rng = random.Random(seed)
    raw = []
    sw = (x1 - x0) // 6
    row_h = int(sw * 0.55)       # 45% overlap between rows
    y = y0 + row_h // 2
    row = 0
    while y < y1 + row_h:
        xs = list(range(x0, x1, int((x1 - x0) * 0.18)))
        if row % 2:
            xs = xs[::-1]
        for x in xs:
            raw.append((x, y, math.radians(8 + rng.uniform(-11, 11)),
                        (x1 - x0) * rng.uniform(0.42, 0.60), sw * rng.uniform(0.9, 1.35)))
        row += 1
        y += row_h
    # polish pass: four broad sweeps covering the region edge to edge
    band_h = (y1 - y0) / 4
    for i in range(4):
        raw.append((x0, y0 + band_h * (i + 0.5), math.radians(4),
                    (x1 - x0) * 1.1, band_h * 1.5))

    strokes = []
    n_total = len(raw)
    for si, (x, y, ang, ln, wd) in enumerate(raw):
        cx, cy = x + ln * 0.45, y
        dx, dy = math.cos(ang) * ln / 2, -math.sin(ang) * ln / 2
        pad = int(wd)
        bx0, by0 = int(min(cx - dx, cx + dx) - pad), int(min(cy - dy, cy + dy) - pad)
        bx1, by1 = int(max(cx - dx, cx + dx) + pad), int(max(cy - dy, cy + dy) + pad)
        layer = Image.new("L", (bx1 - bx0, by1 - by0), 0)
        d = ImageDraw.Draw(layer)
        d.line([(cx - dx - bx0, cy - dy - by0), (cx + dx - bx0, cy + dy - by0)],
               fill=255, width=int(wd))
        layer = layer.filter(ImageFilter.GaussianBlur(wd * 0.22))
        crumbs = []
        if si > n_total * 0.7:   # crumbs arrive late, sparse, near stroke bottoms
            crumbs = [(rng.uniform(0, bx1 - bx0), rng.uniform(0.5, 1.0) * (by1 - by0),
                       rng.uniform(1.2, 2.8), rng.randint(40, 80)) for _ in range(rng.randint(0, 2))]
        strokes.append(((bx0, by0, bx1, by1), np.asarray(layer, np.float32) / 255.0, crumbs))
    return strokes


def poc_1():
    base = scale_crop(Image.open(STORM / "stills" / "s01_waves.png").convert("RGB"), W, H)
    # blank sheet: the spread's own cream + grain, only INSIDE the drawn area
    # (the collage border survives -- the eraser takes the drawing, not the book)
    nrng = np.random.default_rng(11)
    blank = np.zeros((H, W, 3), np.float32)
    blank[..., 0], blank[..., 1], blank[..., 2] = PAPER
    grain = np.asarray(Image.fromarray(np.clip(nrng.standard_normal((H, W)) * 40 + 128, 0, 255)
                                        .astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)),
                        np.float32) / 255.0 - 0.5
    blank *= (1.0 + 0.05 * grain)[..., None]

    region = (int(W * 0.06), int(H * 0.05), int(W * 0.94), int(H * 0.90))
    strokes = _eraser_strokes(region, seed=5)
    n = len(strokes)
    base_a = np.asarray(base, np.float32)

    # the erased state is not fog -- it is blank paper with a 7% PENCIL GHOST
    # of the drawing's own dark linework (what a real eraser leaves behind)
    lum = np.asarray(base.convert("L"), np.float32)
    ghost = np.clip((115.0 - lum) / 115.0, 0, 1)
    ghost = np.asarray(Image.fromarray((ghost * 255).astype(np.uint8))
                        .filter(ImageFilter.GaussianBlur(1.3)), np.float32) / 255.0 * 0.09
    ghost_gray = np.array([120, 112, 100], np.float32)
    erased = blank * (1 - ghost[..., None]) + ghost_gray[None, None, :] * ghost[..., None]

    T0, DUR = 0.8, 1.3   # violent -- the whole storm gone in ~1.3s
    accum = np.zeros((H, W), np.float32)
    k_done = [0]
    crumb_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(crumb_layer)

    events, layers = entry_events([("and it was gone.", 0, 0)],
                                   origin=(int(W * 0.33), int(H * 0.46)), size=48,
                                   energy=0.10, seed=61, t0=3.2, dur=1.5)

    def frame(t):
        p = (t - T0) / DUR
        k = 0 if p <= 0 else (n if p >= 1 else int(p * n))
        for i in range(k_done[0], k):
            (bx0, by0, bx1, by1), m, crumbs = strokes[i]
            sl = accum[max(0, by0):by1, max(0, bx0):bx1]
            mm = m[max(0, by0) - by0:, max(0, bx0) - bx0:][:sl.shape[0], :sl.shape[1]]
            np.maximum(sl, mm, out=sl)
            for (cxx, cyy, r, a) in crumbs:
                cd.ellipse([bx0 + cxx - r, by0 + cyy - r, bx0 + cxx + r, by0 + cyy + r],
                           fill=(70, 62, 52, a))
        k_done[0] = max(k_done[0], k)
        m3 = accum[..., None]
        out = Image.fromarray(np.clip(base_a * (1 - m3) + erased * m3, 0, 255).astype(np.uint8))
        out = out.convert("RGBA")
        out.alpha_composite(crumb_layer)
        return compose_at(out.convert("RGB"), events, layers, t)

    render("bold_1_erasure", frame, 5.5)
    print("[sfx] eraser scrub cue 0.8-2.1")


# ---------------------------------------------------------------- 2 TORN PAGE


def poc_2():
    above = scale_crop(Image.open(STORM / "stills" / "s03_screaming.png").convert("RGB"), W, H).convert("RGBA")
    below = scale_crop(Image.open(STORM / "stills" / "s04_asleep.png").convert("RGB"), W, H)

    # white torn deckle down the flying page's left edge (the tear remnant)
    rng = random.Random(13)
    deckle = Image.new("RGBA", (46, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(deckle)
    pts = [(46, 0)]
    for y in range(0, H, 14):
        pts.append((14 + rng.uniform(-9, 9), y))
    pts += [(46, H)]
    dd.polygon(pts, fill=(247, 242, 228, 255))

    GRAB, RIP, GONE = 0.9, 1.5, 1.95

    def frame(t):
        out = below.convert("RGBA")
        if t >= GONE:
            return out.convert("RGB")
        page = above.copy()
        if t >= RIP - 0.35:  # deckle shows as the page starts to give
            page.alpha_composite(deckle, (0, 0))
        if t < GRAB:
            ang, dx, dy, lift = 0.0, 0, 0, 0.0
        elif t < RIP:
            p = smootherstep((t - GRAB) / (RIP - GRAB))
            ang, dx, dy, lift = -2.2 * p, int(8 * p), int(-6 * p), p
        else:
            p = ((t - RIP) / (GONE - RIP)) ** 1.8   # accelerates away
            ang = -2.2 - 16 * p
            dx = int(8 + (W * 1.45) * p)
            dy = int(-6 - (H * 0.22) * p)
            lift = 1.0
        page = page.rotate(ang, center=(60, int(H * 0.6)), resample=Image.BICUBIC)
        if lift > 0:
            sil = page.split()[3].point(lambda a: min(a, int(70 * lift)))
            shadow = Image.new("RGBA", page.size, (25, 18, 12, 0))
            shadow.putalpha(sil)
            shadow = shadow.filter(ImageFilter.GaussianBlur(6 + 10 * lift))
            out.alpha_composite(shadow, (dx + int(10 * lift), dy + int(14 * lift)))
        out.alpha_composite(page, (dx, dy))
        return out.convert("RGB")

    render("bold_2_torn_page", frame, 4.5)
    print("[sfx] page-rip cue at 1.5")


# ---------------------------------------------------------------- 3 BLEED


def poc_3():
    base = scale_crop(Image.open(STORM / "stills" / "s01_waves.png").convert("RGB"), W, H)
    events, layers = entry_events(
        [("~~storm~~ ~~wind~~ fear.", 0, 0),
         ("water at our knees", 40, 100)],
        origin=(int(W * 0.36), int(H * 0.878)), size=64, energy=0.85,
        seed=41, t0=0.5, dur=2.2, skid=True)

    # locate "fear." on line 1 with the same font metrics keeper_line used
    font = ImageFont.truetype(F_KEEPER, 64)
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    sp = probe.textlength(" ", font=font)
    x_fear = (probe.textlength("storm", font=font) + sp
              + probe.textlength("wind", font=font) + sp
              + probe.textlength("fear.", font=font) * 0.5)
    cx = int(W * 0.36 + x_fear)
    cy = int(H * 0.878 + 64 * 0.55)

    DROP = 3.2
    rng = random.Random(21)
    trails = [(cx + rng.randint(-14, 14), rng.uniform(40, 85), rng.uniform(1.5, 2.6))
              for _ in range(3)]

    def frame(t):
        out = compose_at(base, events, layers, t)
        if t < DROP:
            return out
        p = smootherstep((t - DROP) / 0.6)
        arr = np.asarray(out, np.float32)
        ys, xs = np.mgrid[max(0, cy - 90):cy + 90, max(0, cx - 90):cx + 90]
        r = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
        R = 8 + 26 * p
        disc = np.clip((R - r) / 10.0, 0, 1)
        # wet darkening + local smear (the letters lose their edges)
        region = arr[max(0, cy - 90):cy + 90, max(0, cx - 90):cx + 90]
        blur = np.asarray(Image.fromarray(region.astype(np.uint8))
                           .filter(ImageFilter.GaussianBlur(2.2)), np.float32)
        region[:] = region * (1 - disc[..., None] * 0.5) + blur * (disc[..., None] * 0.5)
        region[:] *= (1.0 - 0.30 * p * disc)[..., None]
        # run trails: thin ink threads finding their way down
        pr = smootherstep((t - DROP - 0.25) / 1.2)
        if pr > 0:
            im2 = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGB")
            d = ImageDraw.Draw(im2, "RGBA")
            for (tx, tlen, twid) in trails:
                ln = tlen * pr
                d.line([(tx, cy + 12), (tx + rng.uniform(-1, 1), cy + 12 + ln)],
                       fill=(58, 48, 40, 150), width=int(twid))
            return im2
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    render("bold_3_bleed", frame, 5.5)
    print("[sfx] single drop cue at 3.2")


# ---------------------------------------------------------------- 4 DIVE


def poc_4():
    src = Image.open(STORM / "stills" / "s01_waves.png").convert("RGB")
    SW, SH = src.size

    def viewport(zoom, cx_f, cy_f):
        vh = SH / zoom
        vw = vh * (W / H)
        cx, cy = cx_f * SW, cy_f * SH
        x0 = min(max(0, cx - vw / 2), SW - vw)
        y0 = min(max(0, cy - vh / 2), SH - vh)
        crop = src.crop((int(x0), int(y0), int(x0 + vw), int(y0 + vh)))
        return crop.resize((W, H), Image.LANCZOS)

    HOLD, FALL, SETTLE = 0.6, 1.6, 0.25
    rng = random.Random(31)

    def frame(t):
        if t < HOLD:
            z, cx_f, cy_f, shake = 1.9, 0.52, 0.14, 0.0
        elif t < HOLD + FALL:
            p = ((t - HOLD) / FALL) ** 1.6          # a fall: slow release, fast drop
            p = smootherstep(p)
            z = 1.9 - 0.35 * p
            cx_f = 0.52 - 0.05 * p
            cy_f = 0.14 + 0.60 * p
            shake = 0.0
        else:
            z, cx_f, cy_f = 1.55, 0.47, 0.74
            b = t - (HOLD + FALL)
            shake = 3.0 * math.exp(-b / 0.07) * math.sin(2 * math.pi * b / 0.1)
        fr = viewport(z, cx_f, cy_f + shake / SH)
        if shake:
            fr = fr.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, shake), resample=Image.BILINEAR)
        return fr.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))

    render("bold_4_dive", frame, 4.5)
    print("[sfx] whoosh-drop + arrival thud at ~2.2 (arrival leads the wave-hit beat)")


if __name__ == "__main__":
    poc_1()
    poc_2()
    poc_3()
    poc_4()
    print("BOLD_POC_DONE")
