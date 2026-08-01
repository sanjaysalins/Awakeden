"""VAULT POC BATCH 2 -- the eleven remaining ideas from _IDEA_VAULT.md, $0,
real Storm assets, nothing locked. Rendered for the single selection page
(_ROUND6_SELECTION.html). Every device passes the desk test (memory:
feedback-device-must-live-in-the-book): a keeper's mark, a paper behavior,
or light on the desk -- never a designed graphic.

  ..\\..\\..\\.venv\\Scripts\\python.exe _build_vault2.py
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
sys.path.insert(0, str(STORM / "_vault_poc"))
from raking_light import scale_crop, _sweep_band, _probe  # noqa: E402
import _build_poc as K   # noqa: E402  keeper hand engine
import _build_vault as V  # noqa: E402  scribed verse + paper base

FPS = 30
W, H = 1080, 1920
GOLD = (185, 146, 74)
F_SECOND_HAND = "C:/Windows/Fonts/segoepr.ttf"   # a different person's hand


def render(name, frame_fn, dur):
    work = HERE / f"_{name}_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for i in range(int(dur * FPS)):
        frame_fn(i / FPS).save(work / f"f{i:05d}.png")
    out = HERE / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out}")


def ss(t):
    t = min(1.0, max(0.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


def still(name):
    return scale_crop(Image.open(STORM / "stills" / name).convert("RGB"), W, H)


# ---------------------------------------------------- 1 PERMANENCE SPLIT

def poc_permanence():
    base = V.paper_base(seed=23)
    saved = K.KEEPER_INK
    K.KEEPER_INK = (98, 76, 54)
    ev, ly = K.entry_events([("all of this will fade.", 0, 0)],
                             origin=(int(W * 0.24), int(H * 0.28)), size=52,
                             energy=0.2, seed=101, t0=0.4, dur=1.2)
    K.KEEPER_INK = saved

    saved_ink = V.INK
    V.INK = GOLD
    gold_layer = V.scribed_verse_layer("my words shall not pass away.", "LUKE 21:33",
                                        size=46, seed=102)
    V.INK = saved_ink

    # pre-composite the fresh keeper line + an aged twin to crossfade toward
    fresh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for _, i in ev:
        layer, x, y = ly[i]
        fresh.alpha_composite(layer, (x, y))
    aged = fresh.copy().filter(ImageFilter.GaussianBlur(0.7))
    fa = np.asarray(aged, np.float32)
    fa[..., 0] = np.clip(fa[..., 0] * 0.6 + 96, 0, 255)   # brown out
    fa[..., 1] = np.clip(fa[..., 1] * 0.6 + 74, 0, 255)
    fa[..., 2] = np.clip(fa[..., 2] * 0.6 + 52, 0, 255)
    fa[..., 3] *= 0.42
    aged = Image.fromarray(fa.astype(np.uint8), "RGBA")

    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    rng = random.Random(103)
    fox = np.zeros((H, W), np.float32)
    for _ in range(6):
        fx, fy = rng.uniform(0.1, 0.9) * W, rng.uniform(0.12, 0.9) * H
        fr = rng.uniform(40, 110)
        fox += rng.uniform(0.4, 0.8) * np.exp(-0.5 * (((xs - fx) ** 2 + (ys - fy) ** 2) / fr ** 2))
    fox = np.clip(fox, 0, 1)
    rust = np.array([168, 130, 86], np.float32)
    base_a = np.asarray(base, np.float32)

    T_AGE0, T_AGE1 = 2.2, 6.0

    def frame(t):
        age = ss((t - T_AGE0) / (T_AGE1 - T_AGE0))
        arr = base_a.copy()
        warm = np.array([230, 212, 172], np.float32)
        arr = arr * (1 - 0.35 * age) + warm[None, None, :] * (0.35 * age)
        fx3 = (fox * 0.20 * age)[..., None]
        arr = arr * (1 - fx3) + rust[None, None, :] * fx3
        out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
        if age <= 0:
            out2 = K.compose_at(out.convert("RGB"), ev, ly, t).convert("RGBA")
        else:
            mix = Image.blend(fresh, aged, age)
            out2 = out
            out2.alpha_composite(mix)
        out2.alpha_composite(gold_layer, (0, int(H * 0.40)))  # untouched, always
        return out2.convert("RGB")

    render("v2_01_permanence_split", frame, 7.0)


# ---------------------------------------------------- 2 DOG-EAR

def poc_dog_ear():
    base = still("s08_verse.png").convert("RGBA")
    C = (int(W * 0.955), int(H * 0.965))
    L_MAX = 185
    T0, DUR = 1.2, 0.45

    def frame(t):
        out = base.copy()
        p = ss((t - T0) / DUR)
        if p <= 0:
            return out.convert("RGB")
        L = int(L_MAX * p)
        d = ImageDraw.Draw(out)
        # under-page (what the corner used to cover)
        d.polygon([C, (C[0] - L, C[1]), (C[0], C[1] - L)], fill=(151, 128, 99, 255))
        # the folded-over flap: page back, shaded toward the crease
        flap = Image.new("RGBA", (L + 4, L + 4), (0, 0, 0, 0))
        fd = ImageDraw.Draw(flap)
        fd.polygon([(L, 0), (0, L), (0, 0)], fill=(243, 233, 206, 255))
        fl = np.asarray(flap, np.float32)
        yy, xx = np.mgrid[0:L + 4, 0:L + 4].astype(np.float32)
        shade = np.clip(1.0 - 0.22 * ((xx + yy) / max(1, L)), 0.72, 1.0)
        fl[..., :3] *= shade[..., None]
        flap = Image.fromarray(np.clip(fl, 0, 255).astype(np.uint8), "RGBA")
        # crease shadow along the diagonal, cast onto the page
        sh = Image.new("RGBA", (L + 30, L + 30), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sh)
        sd.line([(4, L + 10), (L + 10, 4)], fill=(30, 22, 14, 90), width=7)
        sh = sh.filter(ImageFilter.GaussianBlur(5))
        out.alpha_composite(sh, (C[0] - L - 12, C[1] - L - 12))
        out.alpha_composite(flap, (C[0] - L - 2, C[1] - L - 2))
        return out.convert("RGB")

    render("v2_02_dog_ear", frame, 4.0)
    print("[sfx] paper-fold cue at 1.2")


# ---------------------------------------------------- 3 THE PAGE BREATHES

def poc_breathes():
    im = Image.open(STORM / "stills" / "s04_asleep.png").convert("RGB")
    plate = scale_crop(im, int(W * 1.05), int(H * 1.05))
    PW, PH = plate.size

    def breathe_amp(t):
        if t < 5.5:
            return math.sin(2 * math.pi * t / 3.2)
        if t < 6.6:
            return 0.0                      # breath held -- dead still
        return math.sin(2 * math.pi * (t - 6.6) / 4.4)  # slower, deeper resume

    held = [None]

    def frame(t):
        a = breathe_amp(t)
        if a == 0.0 and held[0] is not None:
            return held[0]
        s = 1.0 + 0.006 * a
        nw, nh = int(PW * s), int(PH * s)
        big = plate.resize((nw, nh), Image.BILINEAR)
        x0 = (nw - W) // 2
        y0 = nh - H - (nh - H) // 2       # anchored low -- the spine end moves least
        out = big.crop((x0, y0, x0 + W, y0 + H))
        if a == 0.0:
            held[0] = out
        return out

    render("v2_03_page_breathes", frame, 8.5)


# ---------------------------------------------------- 4 RAIN-SHADOW

def poc_rain_shadow():
    base = still("s01_waves.png")
    base_a = np.asarray(base, np.float32)
    rng = random.Random(41)
    streaks = []
    for _ in range(26):
        sw_, sl = int(rng.uniform(26, 64)), int(rng.uniform(280, 680))
        blob = Image.new("L", (sw_ + 40, sl + 40), 0)
        bd = ImageDraw.Draw(blob)
        bd.ellipse([20, 20, 20 + sw_, 20 + sl], fill=int(rng.uniform(120, 200)))
        blob = blob.filter(ImageFilter.GaussianBlur(16))
        streaks.append((np.asarray(blob, np.float32) / 255.0,
                        rng.randint(-20, W - 20), rng.uniform(140, 260),
                        rng.uniform(0, H)))

    def frame(t):
        D = np.zeros((H, W), np.float32)
        for arr, x, speed, y0 in streaks:
            bh, bw = arr.shape
            y = int((y0 + speed * t) % (H + bh)) - bh
            ys0, ys1 = max(0, y), min(H, y + bh)
            xs0, xs1 = max(0, x), min(W, x + bw)
            if ys1 > ys0 and xs1 > xs0:
                D[ys0:ys1, xs0:xs1] += arr[ys0 - y:ys1 - y, xs0 - x:xs1 - x]
        D = np.clip(D, 0, 1.6) * 0.085
        dim = 0.985 + 0.015 * math.sin(2 * math.pi * t / 6.0)
        tint = np.array([0.88, 0.91, 0.97], np.float32)
        mod = (1.0 - D[..., None]) + D[..., None] * tint[None, None, :]
        return Image.fromarray(np.clip(base_a * mod * dim, 0, 255).astype(np.uint8))

    render("v2_04_rain_shadow", frame, 5.5)


# ---------------------------------------------------- 5 CANDLE-ONLY SPREAD

def poc_candle():
    base = still("s04_asleep.png")
    base_a = np.asarray(base, np.float32)
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    LAMP = (W * 0.295, H * 0.495)
    dist = np.sqrt((xs - LAMP[0]) ** 2 + (ys - LAMP[1]) ** 2)
    rng = random.Random(51)
    flick = [rng.uniform(-1, 1) for _ in range(400)]

    def R_of(t):
        if t < 0.8:
            return 3000.0
        if t < 2.4:
            return 3000.0 - (3000.0 - 330.0) * ss((t - 0.8) / 1.6)
        if t < 5.2:
            f = flick[int(t * 12) % 400] * 0.5 + flick[int(t * 5) % 400] * 0.5
            return 330.0 + 10.0 * f
        return 330.0 + (950.0 - 330.0) * ss((t - 5.2) / 1.6)

    warm = np.array([1.08, 1.00, 0.88], np.float32)
    cold = np.array([0.82, 0.87, 1.00], np.float32)

    def frame(t):
        R = R_of(t)
        lit = np.clip((R - dist) / 260.0 + 0.5, 0, 1)
        glow = np.clip(1.0 - dist / max(R, 1), 0, 1) ** 2
        gain = (cold[None, None, :] * 0.16) * (1 - lit[..., None]) \
            + (warm[None, None, :] * (1.0 + 0.10 * glow[..., None])) * lit[..., None]
        return Image.fromarray(np.clip(base_a * gain, 0, 255).astype(np.uint8))

    render("v2_05_candle_only", frame, 7.5)


# ---------------------------------------------------- 6 WAX SEAL

def poc_wax_seal():
    base = V.paper_base(seed=63, tint=(236, 224, 192))
    CX, CY = int(W * 0.5), int(H * 0.46)
    WAX_D, WAX_L = (128, 22, 18), (168, 52, 40)
    rng = random.Random(64)
    drips = [(0.8, 0.0), (1.35, -14.0), (1.75, 11.0)]
    T_PRESS, T_IMPRINT = 2.8, 3.05

    def blob_r(t):
        r = 0.0
        for (td, _off) in drips:
            if t >= td:
                r = math.sqrt(r * r + 42 ** 2) if r else 44.0
        if t >= T_PRESS:
            r *= 1.0 + 0.18 * ss((t - T_PRESS) / 0.3)
        return r

    def frame(t):
        out = base.convert("RGBA")
        d = ImageDraw.Draw(out, "RGBA")
        for (td, off) in drips:
            if td - 0.12 <= t < td:  # the falling drip, motion-streaked
                p = (t - (td - 0.12)) / 0.12
                yy = -40 + (CY - (-40)) * p
                d.ellipse([CX + off - 7, yy - 26, CX + off + 7, yy + 10], fill=(*WAX_D, 210))
        r = blob_r(t)
        if r > 0:
            pts = []
            for i in range(28):
                a = 2 * math.pi * i / 28
                rr = r * (1 + 0.06 * math.sin(3 * a + 1.2) + 0.03 * math.sin(7 * a))
                pts.append((CX + rr * math.cos(a), CY + rr * 0.86 * math.sin(a)))
            d.polygon(pts, fill=(*WAX_D, 250))
            hi = 1.0 - (0.65 * ss((t - T_PRESS) / 0.3) if t >= T_PRESS else 0.0)
            d.ellipse([CX - r * 0.45, CY - r * 0.5, CX + r * 0.05, CY - r * 0.12],
                      fill=(*WAX_L, int(120 * hi)))
        if t >= T_IMPRINT:
            p = ss((t - T_IMPRINT) / 0.35)
            a_im = int(200 * p)
            rng2 = random.Random(66)
            for seg in [((CX, CY - 46), (CX, CY + 46)), ((CX - 32, CY - 12), (CX + 32, CY - 12))]:
                pts = []
                for i in range(10):
                    q = i / 9
                    pts.append((seg[0][0] + (seg[1][0] - seg[0][0]) * q + rng2.uniform(-1.5, 1.5),
                                seg[0][1] + (seg[1][1] - seg[0][1]) * q + rng2.uniform(-1.5, 1.5)))
                d.line(pts, fill=(62, 10, 8, a_im), width=9)
                d.line([(px - 2, py - 2) for px, py in pts], fill=(*WAX_L, int(90 * p)), width=2)
            ring = blob_r(t) * 0.94
            d.ellipse([CX - ring, CY - ring * 0.86, CX + ring, CY + ring * 0.86],
                      outline=(*WAX_L, int(70 * p)), width=3)
        return out.convert("RGB")

    render("v2_06_wax_seal", frame, 5.5)
    print("[sfx] wax drips 0.8/1.35/1.75, press thump 2.8")
    print("[note] signet symbol here is a plain cross placeholder -- series symbol is a USER decision")


# ---------------------------------------------------- 7 BLIND EMBOSS

def poc_blind_emboss():
    base = V.paper_base(seed=71)
    base_a = np.asarray(base, np.float32)
    layer = V.scribed_verse_layer("and there was a great calm.", "", size=50, seed=72)
    M = np.zeros((H, W), np.float32)
    la = np.asarray(layer.split()[3], np.float32) / 255.0
    y0 = int(H * 0.34)
    M[y0:y0 + la.shape[0], :] = la[:, :W]
    M = np.asarray(Image.fromarray((M * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0)),
                   np.float32) / 255.0
    hi = np.roll(np.roll(M, -2, 0), -2, 1)   # pressed-through: light catches above-left
    lo = np.roll(np.roll(M, 2, 0), 2, 1)     # shadow pools below-right

    def frame(t):
        band = _sweep_band(W, H, t / 6.0, 620.0, 15.0)
        k = 0.55 + 1.1 * band
        arr = base_a + (hi * 26 - lo * 26)[..., None] * k[..., None]
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    render("v2_07_blind_emboss", frame, 6.0)
    print("[note] no ink anywhere -- the PREVIOUS episode's last line, pressed through the page above")


# ---------------------------------------------------- 8 FLYLEAF CENSUS

def poc_flyleaf():
    base = V.paper_base(seed=81, tint=(212, 192, 156))
    entries = [("the door \u2014 opened.", 0.28, 115, 105),
               ("jericho \u2014 fallen.", 0.345, 140, 106),
               ("the two goats \u2014 one sent.", 0.41, 165, 107)]
    saved = K.KEEPER_INK
    static = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for text, yf, alpha, seed in entries:
        K.KEEPER_INK = (88, 70, 50)
        ev, ly = K.entry_events([(text, 0, 0)], origin=(int(W * 0.17), int(H * yf)),
                                 size=46, energy=0.12, seed=seed, t0=0, dur=0.1)
        for _, i in ev:
            layer, x, y = ly[i]
            faded = layer.copy()
            fa = faded.split()[3].point(lambda v, a=alpha: min(v, a))
            faded.putalpha(fa)
            static.alpha_composite(faded, (x, y))
    K.KEEPER_INK = (66, 54, 42)
    ev_new, ly_new = K.entry_events([("the storm \u2014 stilled.", 0, 0)],
                                     origin=(int(W * 0.17), int(H * 0.475)), size=46,
                                     energy=0.1, seed=108, t0=1.4, dur=1.5)
    K.KEEPER_INK = saved

    def frame(t):
        out = base.convert("RGBA")
        out.alpha_composite(static)
        return K.compose_at(out.convert("RGB"), ev_new, ly_new, t)

    render("v2_08_flyleaf_census", frame, 5.5)


# ---------------------------------------------------- 9 PRICKED MARGIN

def poc_pricked():
    base = still("s07_eyes.png").convert("RGBA")
    d = ImageDraw.Draw(base)
    px = int(W * 0.952)
    pys = [int(H * (0.16 + 0.70 * i / 12)) for i in range(13)]
    for py in pys:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(96, 82, 62, 190))
        d.ellipse([px - 1, py + 2, px + 4, py + 5], fill=(255, 250, 236, 60))
    base_rgb = base.convert("RGB")
    T_MOVE = 2.0

    def glint(out, py, strength):
        if strength <= 0:
            return
        dd = ImageDraw.Draw(out, "RGBA")
        for rr, aa in [(11, 40), (7, 70), (4, 110)]:
            dd.ellipse([px - rr, py - rr, px + rr, py + rr],
                       fill=(255, 226, 160, int(aa * strength)))

    def frame(t):
        out = base_rgb.copy()
        p = ss((t - T_MOVE) / 0.4)
        glint(out, pys[4], 1.0 - p)
        glint(out, pys[5], p)
        return out

    render("v2_09_pricked_margin", frame, 4.5)
    print("[note] 13 pricks = this episode's 13 spreads; the lit one is where we ARE")


# ---------------------------------------------------- 10 THE SECOND HAND

def poc_second_hand():
    base = V.paper_base(seed=91, tint=(230, 216, 182))
    saved_ink, saved_font = K.KEEPER_INK, K.F_KEEPER
    K.KEEPER_INK = (110, 88, 62)
    ev1, ly1 = K.entry_events([("the storm \u2014 stilled.", 0, 0)],
                               origin=(int(W * 0.22), int(H * 0.33)), size=50,
                               energy=0.12, seed=111, t0=0, dur=0.1)
    static = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for _, i in ev1:
        layer, x, y = ly1[i]
        fa = layer.split()[3].point(lambda v: min(v, 150))
        layer = layer.copy()
        layer.putalpha(fa)
        static.alpha_composite(layer, (x, y))
    K.KEEPER_INK = (56, 52, 60)
    K.F_KEEPER = F_SECOND_HAND
    ev2, ly2 = K.entry_events([("this was my father's book.", 0, 0)],
                               origin=(int(W * 0.20), int(H * 0.43)), size=40,
                               energy=0.05, seed=112, t0=1.4, dur=1.8)
    K.KEEPER_INK, K.F_KEEPER = saved_ink, saved_font

    def frame(t):
        out = base.convert("RGBA")
        out.alpha_composite(static)
        return K.compose_at(out.convert("RGB"), ev2, ly2, t)

    render("v2_10_second_hand", frame, 5.5)


# ---------------------------------------------------- 11 TWO HANDS AT ONCE

def poc_two_hands():
    clip = STORM / "clips" / "s03_screaming.mp4"
    cw, ch, cfps = _probe(clip)
    work = HERE / "_two_hands_src"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-t", "4.5", "-i", str(clip),
                    str(work / "f%05d.png")], check=True)
    frames = sorted(work.glob("f*.png"))
    ev, ly = K.entry_events([("we could not out-row it.", 0, 0)],
                             origin=(int(W * 0.13), int(H * 0.012)), size=60,
                             energy=0.85, seed=121, t0=0.5, dur=2.4)

    out_work = HERE / "_v2_11_work"
    if out_work.exists():
        shutil.rmtree(out_work)
    out_work.mkdir()
    for i, fp in enumerate(frames):
        t = i / cfps
        fr = scale_crop(Image.open(fp).convert("RGB"), W, H)
        K.compose_at(fr, ev, ly, t).save(out_work / f"f{i:05d}.png")
    out = HERE / "v2_11_two_hands.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", f"{cfps:.3f}", "-i", str(out_work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    shutil.rmtree(out_work)
    print(f"[ok] {out}")
    print("[note] the drawing MOVES (real episode clip) while the Keeper writes -- simultaneity")


if __name__ == "__main__":
    poc_permanence()
    poc_dog_ear()
    poc_breathes()
    poc_rain_shadow()
    poc_candle()
    poc_wax_seal()
    poc_blind_emboss()
    poc_flyleaf()
    poc_pricked()
    poc_second_hand()
    poc_two_hands()
    print("VAULT2_POC_DONE")
