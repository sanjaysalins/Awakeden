"""Jericho — step 5: THE /living-sketchbook assembler. New devices, all $0:
word-timed VERSE REVEALS (gold marker sweep + reference card), hunt-and-lock
camera (j04), CountUp chip (13 LAPS), MarkerCircle draw-on, paperRip/inkSwipe
transitions, grain-boil paper life, Scripture-silence score ducks + low tone.

  .venv\\Scripts\\python.exe poc_living_sketchbook/jericho/_j5_assemble.py
"""
import json
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN  # noqa

HERE = Path(__file__).resolve().parent
CLIPS = HERE / "clips"
STILLS = HERE / "stills"
AUD = HERE / "audio"
OUT = HERE / "JERICHO_living_sketchbook.mp4"

W, H, FPS = 1080, 1920, 30
TOTAL = 64.8
INK = (30, 26, 24)
SCARLET = (158, 28, 24)
CREAM = (243, 233, 212)
HILITE = (250, 230, 90)
GOLD = (201, 164, 92)
F_BLACK = "C:/Windows/Fonts/ariblk.ttf"
F_VERSE = "C:/Windows/Fonts/georgiai.ttf"

TIMING = json.loads((AUD / "timing.json").read_text())
LINE = {ln["name"]: ln for ln in TIMING["lines"]}

# j04 hunt-and-lock: window/cord position as FRACTIONS of the j04 still
# (set after eye-checking the render; verify before final build)
J04_WIN = (0.610, 0.325)  # calibrated by eye against the rendered j04 still

SHOTS = [  # (name, t0, t1, kind)  kind: clip | still
    ("j01_walls", 0.0, 7.2, "clip"),
    ("j02_feet", 7.2, 10.9, "clip"),
    ("j03_laps", 10.9, 13.4, "still"),
    ("j04_wallface", 13.4, 16.6, "still"),
    ("j05_rahab", 16.6, 24.2, "clip"),
    ("j06_thread", 24.2, 27.7, "clip"),
    ("j07_trumpets", 27.7, 30.7, "clip"),
    ("j08_stage_a", 30.7, 32.6, "clip"),
    ("j09_stage_b", 32.6, 34.2, "clip"),
    ("j10_stage_c", 34.2, 38.2, "clip"),
    ("j11_spared", 38.2, 47.2, "clip"),
    ("j12_line", 47.2, 55.0, "clip"),
    ("j13_landing", 55.0, TOTAL, "clip"),
]

REVEALS = [  # (line, i0, i1, band_y_frac, ref_label)
    ("l4", 0, 8, 0.70, "JOSHUA 2:18"),
    ("l7", 4, 10, 0.72, "HEBREWS 11:31"),
    ("l8", 5, 9, 0.70, "MATTHEW 1:5"),
]

TRANSITIONS = [(27.7, "paperRip"), (55.0, "inkSwipe")]
WM_TOP = 160
GRAIN_ALPHA = 22


def ease(t):
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def type_img(text, size, fill, hilite=False, card=False):
    font = ImageFont.truetype(F_BLACK, size)
    pad = int(size * 0.35)
    bb = font.getbbox(text)
    tw = bb[2] - bb[0]
    img = Image.new("RGBA", (tw + 4 * pad, int(size * 1.5) + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x, y = 2 * pad, pad
    if card:
        d.rectangle([x - pad, y - int(pad * 0.4), x + tw + pad, y + int(size * 1.25)],
                    fill=(*SCARLET, 255))
        d.text((x, y), text, font=font, fill=(*CREAM, 255))
    else:
        if hilite:
            d.rectangle([x - int(pad * 0.5), y + int(size * 0.18),
                         x + tw + int(pad * 0.5), y + int(size * 1.08)],
                        fill=(*HILITE, 215))
        d.text((x + 4, y + 5), text, font=font, fill=(0, 0, 0, 70))
        d.text((x, y), text, font=font, fill=(*fill, 255))
    return img.rotate(-1.5, expand=True, resample=Image.BICUBIC)


OVERLAY_TYPE = [
    (33.0, 35.8, type_img("THE WALL FELL DOWN FLAT.", 58, INK, hilite=True), 0.50, 0.22),
    (60.6, TOTAL - 0.4, type_img("BIND EVERYTHING TO IT.", 72, INK, hilite=True), 0.50, 0.72),
]


def build_reveal_assets():
    out = []
    fnt = ImageFont.truetype(F_VERSE, 58)
    for line, i0, i1, band_y, ref in REVEALS:
        words = LINE[line]["words"][i0:i1 + 1]
        clean = [w["w"].replace("\u201c", "").replace("\u201d", "") for w in words]
        widths = [fnt.getbbox(w + " ")[2] for w in clean]
        out.append(dict(words=words, clean=clean, widths=widths, band_y=band_y,
                        ref_img=type_img(ref, 30, INK, card=True),
                        t0=words[0]["s"], t1=words[-1]["e"], font=fnt))
    return out


def draw_reveal(frame, rv, t):
    if t < rv["t0"] - 0.05 or t > rv["t1"] + 2.6:
        return
    total_w = sum(rv["widths"])
    max_w = int(W * 0.90)
    scale = min(1.0, max_w / total_w)
    fnt = rv["font"] if scale == 1.0 else ImageFont.truetype(F_VERSE, max(30, int(58 * scale)))
    widths = [fnt.getbbox(w + " ")[2] for w in rv["clean"]]
    total_w = sum(widths)
    x0 = (W - total_w) // 2
    y = int(H * rv["band_y"])
    band = Image.new("RGBA", (total_w + 70, int(58 * scale * 2.0)), (232, 217, 181, 216))
    frame.paste(band, (x0 - 35, y - int(58 * scale * 0.45)), band)
    d = ImageDraw.Draw(frame)
    x = x0
    swept = 0
    for w, cw in zip(rv["words"], widths):
        if t >= w["s"]:
            k = ease(min(1.0, (t - w["s"]) / 0.14))
            # gold marker sweeps under the already-spoken words
            if t >= w["e"]:
                swept = x + cw - x0
            txt = w["w"].replace("\u201c", "").replace("\u201d", "")
            col = tuple(int(c) for c in INK) + (int(255 * k),)
            ov = Image.new("RGBA", (cw + 8, int(58 * 1.6)), (0, 0, 0, 0))
            ImageDraw.Draw(ov).text((0, int((1 - k) * 8)), txt, font=fnt, fill=col)
            frame.paste(ov, (x, y), ov)
        x += cw
    if swept > 0:
        d.rectangle([x0, y + int(58 * 1.12), x0 + swept, y + int(58 * 1.12) + 8],
                    fill=(*GOLD, 255))
    if t >= rv["t1"] + 0.15:
        k = ease(min(1.0, (t - rv["t1"] - 0.15) / 0.15))
        ri = rv["ref_img"]
        s = 1.3 - 0.3 * k
        ri2 = ri.resize((int(ri.width * s), int(ri.height * s)), Image.LANCZOS)
        if k < 1.0:
            ri2.putalpha(ri2.split()[3].point(lambda v: int(v * k)))
        frame.paste(ri2, ((W - ri2.width) // 2, y + int(58 * 1.55)), ri2)


def countup_chip(frame, t):
    if not (11.0 <= t <= 13.3):
        return
    n = min(13, 1 + int(12 * ease(min(1.0, (t - 11.0) / 1.1))))
    img = type_img(f"{n} LAPS", 84, INK, hilite=True)
    frame.paste(img, (int(W * 0.5 - img.width / 2), int(H * 0.16)), img)


def marker_ellipse(frame, cx, cy, rx, ry, prog, width=7):
    if prog <= 0:
        return
    d = ImageDraw.Draw(frame)
    rng = random.Random(31)
    n = int(72 * min(1.0, prog))
    pts = []
    for i in range(n + 1):
        a = -math.pi / 2 + i / 72 * 2 * math.pi * 1.04
        pts.append((cx + (rx + rng.uniform(-3, 3)) * math.cos(a),
                    cy + (ry + rng.uniform(-3, 3)) * math.sin(a)))
    if len(pts) > 1:
        d.line(pts, fill=SCARLET, width=width, joint="curve")


def noise_layers():
    layers = []
    for seed in range(8):
        rng = random.Random(100 + seed)
        small = Image.new("L", (W // 4, H // 4))
        small.putdata([rng.randint(0, 255) for _ in range(small.width * small.height)])
        layers.append(small.resize((W, H), Image.BILINEAR))
    return layers


def scale_crop(im, w, h):
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def hunt_frame(big, t_rel, dur):
    """j04: wide -> drift -> fast lock onto the window. big = 1.6x canvas."""
    bw, bh = big.size
    wx, wy = J04_WIN[0] * bw, J04_WIN[1] * bh
    p1, p2 = 0.45, 0.75  # phase splits: drift / hunt / lock
    k = t_rel / dur
    if k < p1:
        kk = ease(k / p1)
        cx = bw * 0.35 + (bw * 0.55 - bw * 0.35) * kk
        cy = bh * 0.62 - (bh * 0.62 - bh * 0.45) * kk
        z = 1.0
    elif k < p2:
        kk = ease((k - p1) / (p2 - p1))
        cx = bw * 0.55 + (wx - bw * 0.55) * kk
        cy = bh * 0.45 + (wy - bh * 0.45) * kk
        z = 1.0 + 0.5 * kk
    else:
        kk = ease((k - p2) / (1 - p2))
        cx, cy = wx, wy
        z = 1.5 + 0.9 * kk
    vw, vh = int(W / z), int(H / z)
    x0 = max(0, min(bw - vw, int(cx - vw / 2)))
    y0 = max(0, min(bh - vh, int(cy - vh / 2)))
    frame = big.crop((x0, y0, x0 + vw, y0 + vh)).resize((W, H), Image.LANCZOS)
    lock_prog = 0.0 if k < p2 else (k - p2) / (1 - p2)
    if lock_prog > 0:
        sx = (wx - x0) / vw * W
        sy = (wy - y0) / vh * H
        marker_ellipse(frame, sx, sy, 130, 170, lock_prog)
    return frame


def transition_mask(kind, k):
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    if kind == "inkSwipe":
        edge = int((W + 500) * k) - 250
        d.polygon([(0, 0), (edge, 0), (edge - 250, H), (0, H)], fill=255)
        return m.filter(ImageFilter.GaussianBlur(4))
    rng = random.Random(77)
    edge = int((W + 300) * k) - 150
    pts = [(0, 0)]
    y = 0
    while y <= H:
        pts.append((edge + rng.randint(-70, 70), y))
        y += 60
    pts += [(0, H)]
    d.polygon(pts, fill=255)
    return m.filter(ImageFilter.GaussianBlur(2))


def main():
    work = HERE / "_frames"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()

    frames = {}
    for name, t0, t1, kind in SHOTS:
        if kind == "clip":
            src = CLIPS / f"{name}.mp4"
            if not src.exists():
                raise SystemExit(f"missing clip: {src}")
            d = work / f"_{name}"
            d.mkdir()
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
                            "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                            "-r", str(FPS), str(d / "f%05d.png")], check=True)
            frames[name] = sorted(d.glob("f*.png"))
        else:
            frames[name] = Image.open(STILLS / f"{name}.png").convert("RGB")

    j04_big = None
    if isinstance(frames.get("j04_wallface"), Image.Image):
        j04_big = scale_crop(frames["j04_wallface"], int(W * 1.6), int(H * 1.6))

    reveals = build_reveal_assets()
    grain = noise_layers()

    n_frames = int(TOTAL * FPS)
    outdir = work / "grid"
    outdir.mkdir()
    trans_at = {}
    for tt, kind in TRANSITIONS:
        trans_at[tt] = kind

    prev_last = {}
    for i in range(n_frames):
        t = i / FPS
        shot = next((s for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1])
        name, t0, t1, kind = shot
        if kind == "still":
            if name == "j04_wallface":
                frame = hunt_frame(j04_big, t - t0, t1 - t0)
            else:
                base = frames[name]
                z = 1.03 + 0.05 * ease((t - t0) / (t1 - t0))
                zw, zh = int(W * z), int(H * z)
                frame = scale_crop(base, zw, zh).crop(
                    ((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))
        else:
            seq = frames[name]
            li = int((t - t0) * FPS)
            n = len(seq)
            cyc = 2 * n - 2 if n > 1 else 1
            j = li % cyc
            if j >= n:
                j = cyc - j
            frame = Image.open(seq[j]).convert("RGB")
            if name == "j10_stage_c" and t - t0 > 2.4:
                k = ease((t - t0 - 2.4) / (t1 - t0 - 2.4))
                z = 1.0 + 0.18 * k
                zw, zh = int(W * z), int(H * z)
                fr2 = frame.resize((zw, zh), Image.LANCZOS)
                cx = int(zw * 0.5 + (J04_WIN[0] - 0.5) * 0.5 * zw * k)
                cy = int(zh * 0.42)
                x0 = max(0, min(zw - W, cx - W // 2))
                y0 = max(0, min(zh - H, cy - H // 2))
                frame = fr2.crop((x0, y0, x0 + W, y0 + H))

        # transitions: reveal the incoming shot over the previous frame
        for tt, tkind in trans_at.items():
            if tt <= t < tt + 0.4 and prev_last.get("img") is not None:
                k = ease((t - tt) / 0.4)
                mask = transition_mask(tkind, k)
                frame = Image.composite(frame, prev_last["img"], mask)

        countup_chip(frame, t)
        for rv in reveals:
            draw_reveal(frame, rv, t)
        for (ti, to, img, cxf, cyf) in OVERLAY_TYPE:
            if ti <= t <= to:
                dt = t - ti
                k = ease(min(1.0, dt / 0.18))
                s2 = 1.30 - 0.30 * k
                oi = img.resize((int(img.width * s2), int(img.height * s2)), Image.LANCZOS)
                if k < 1.0:
                    oi.putalpha(oi.split()[3].point(lambda v: int(v * k)))
                ox = int(W * cxf - oi.width / 2)
                oy = max(WM_TOP, int(H * cyf - oi.height / 2))
                frame.paste(oi, (ox, oy), oi)

        # grain-boil: the page is never digitally frozen
        g = grain[i % len(grain)]
        frame = Image.composite(
            frame.point(lambda v: min(255, v + 6)), frame,
            g.point(lambda v: GRAIN_ALPHA if v > 236 else 0))

        if t + 1 / FPS >= (next((s[2] for s in SHOTS if s[1] <= t < s[2]), TOTAL)):
            prev_last["img"] = frame.copy()
        frame.save(outdir / f"g{i:05d}.png")

    silent = HERE / "_silent.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-i", str(outdir / "g%05d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-r", str(FPS), str(silent)], check=True)

    SND = ROOT / "sound_library" / "clips"
    MUS = ROOT / "music_library" / "clips"
    vdur = TOTAL
    silence = "".join(
        f"volume=0.22:enable='between(t,{a},{b})',"
        for a, b in [(24.1, 27.6), (40.1, 43.4), (49.0, 51.3)])
    filt = (
        f"[1:a]{AFMT},apad=whole_dur={vdur},asplit=2[main][key];"
        f"[2:a]{AFMT},atrim=0:{vdur},afade=t=in:st=0:d=1.5,"
        f"afade=t=out:st=36.5:d=3.5,volume=-9dB,{silence}anull[musA];"
        f"[3:a]{AFMT},adelay=38200|38200,atrim=0:{vdur},"
        f"afade=t=in:st=38.2:d=2.5,afade=t=out:st={vdur - 2.0:.1f}:d=2.0,"
        f"volume=-8dB,{silence}anull[musB];"
        f"[musA][musB]amix=inputs=2:normalize=0[mus];"
        f"[mus][key]sidechaincompress={SIDECHAIN}[musd];"
        f"[4:a]{AFMT},atrim=0:{vdur},volume=-26dB[wind];"
        f"[5:a]atrim=0:5.5,volume=-16dB,adelay=7300|7300,{AFMT}[march];"
        f"[6:a]atrim=0:3.2,volume=-8dB,adelay=28300|28300,{AFMT}[shofar];"
        f"[7:a]atrim=0:3.0,volume=-11dB,adelay=30800|30800,{AFMT}[shout];"
        f"[8:a]atrim=0:3.4,volume=0.5,adelay=32600|32600,{AFMT}[rumble];"
        f"[9:a]atrim=0:0.9,lowpass=f=700,volume=0.55,asplit=3[b1][b2][b3];"
        f"[b1]adelay=32650|32650,{AFMT}[boomA];"
        f"[b2]adelay=33000|33000,{AFMT}[boomB];"
        f"[b3]adelay=60600|60600,{AFMT}[boomC];"
        f"[10:a]atrim=0:3.4,volume=-22dB,asplit=3[r1][r2][r3];"
        f"[r1]adelay=24100|24100,{AFMT}[tonA];"
        f"[r2]adelay=40100|40100,{AFMT}[tonB];"
        f"[r3]adelay=49000|49000,{AFMT}[tonC];"
        f"[main][musd][wind][march][shofar][shout][rumble][boomA][boomB][boomC]"
        f"[tonA][tonB][tonC]amix=inputs=13:normalize=0,"
        f"alimiter=limit=0.97,aresample=44100[mix]"
    )
    subprocess.run(["ffmpeg", "-y", "-v", "error",
                    "-i", str(silent), "-i", str(AUD / "narration.mp3"),
                    "-i", str(MUS / "lonely_searching_a.mp3"),
                    "-i", str(MUS / "sacred_grace_rise_a.mp3"),
                    "-i", str(SND / "wind_desert_bleak.mp3"),
                    "-i", str(SND / "footsteps_dirt_approach.mp3"),
                    "-i", str(SND / "shofar_blast.mp3"),
                    "-i", str(SND / "crowd_shout_mob.mp3"),
                    "-i", str(SND / "rumble_deep_sub.mp3"),
                    "-i", str(SND / "impact_low_boom.mp3"),
                    "-i", str(SND / "rumble_deep_sub.mp3"),
                    "-filter_complex", filt,
                    "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-t", f"{vdur}",
                    str(OUT)], check=True)
    shutil.rmtree(work)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
