"""Two Goats — step 4: assemble the full ~70.8s episode. Real word-timed
spread windows (from the offline WhisperX forced-alignment, 189/189 exact).
Illuminated Rubric for the Isaiah 53:6 Scripture-voice beat, Ink Stamp for
2 display words, straight hard cuts for the veil-tear multi-stage event,
paperRip/inkSwipe transitions elsewhere, grain-boil, Scripture-silence score
duck under the Isaiah quote.

  .venv\\Scripts\\python.exe poc_living_sketchbook/two_goats/_g4_assemble.py
"""
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN  # noqa

HERE = Path(__file__).resolve().parent
CLIPS = HERE / "clips"
AUD = HERE / "audio"
OUT = HERE / "TWO_GOATS_living_sketchbook.mp4"

W, H, FPS = 1080, 1920, 30
TOTAL = 70.8
INK = (35, 30, 26)
RUBRIC = (150, 26, 22)
GOLD = (185, 146, 74)
FADED_INK = (75, 62, 48)

F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"
F_ZILLA_I = "C:/Windows/Fonts/ZillaSlab-Italic.ttf"
F_OLDENGL = "C:/Windows/Fonts/OLDENGL.TTF"

SHOTS = [  # (name, t0, t1)
    ("g01_hook", 0.00, 6.81),
    ("g02_bloodgoat", 6.81, 13.09),
    ("g03_scapegoat", 13.09, 18.47),
    ("g04_intodesert", 18.47, 22.80),
    ("g05_onepay_onecarry", 22.80, 26.42),
    ("g06_yearsasked", 26.42, 31.10),
    ("g07_bothhalves", 31.10, 34.76),
    ("g08_jesuspivot", 34.76, 43.62),
    ("g09_isaiah536", 43.62, 47.91),
    ("g10_finished", 47.91, 52.99),
    ("g11_veil_whole", 52.99, 54.20),
    ("g12_veil_tearing", 54.20, 55.40),
    ("g13_veil_torn", 55.40, 63.40),
    ("g14_landing", 63.40, TOTAL),
]
TRANSITIONS = {31.10: "paperRip", 55.40: "inkSwipe"}
WM_TOP = 160


def ease(t):
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def wrap_text(text, font, max_w, draw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def stamped_text(text, font_path, size, color, letter_spacing=0, max_w=None):
    """INK STAMP grammar (SKILL.md sec.5): glyph mask x blurred noise, no box."""
    font = ImageFont.truetype(font_path, size)
    tmp = Image.new("L", (10, 10))
    td = ImageDraw.Draw(tmp)
    lines = wrap_text(text, font, max_w, td) if max_w else [text]
    line_h = int(size * 1.2)
    if letter_spacing:
        line_widths = [sum(td.textlength(ch, font=font) for ch in ln) +
                       letter_spacing * (len(ln) - 1) for ln in lines]
    else:
        line_widths = [td.textlength(ln, font=font) for ln in lines]
    tw = int(max(line_widths)) + 4
    th = line_h * len(lines) + 4
    pad = 24
    stamp = Image.new("L", (tw + 2 * pad, th + 2 * pad), 0)
    sd = ImageDraw.Draw(stamp)
    for i, ln in enumerate(lines):
        y = pad + i * line_h
        x0 = pad + (tw - line_widths[i]) / 2
        if letter_spacing:
            x = x0
            for ch in ln:
                sd.text((x, y), ch, font=font, fill=255)
                x += td.textlength(ch, font=font) + letter_spacing
        else:
            sd.text((x0, y), ln, font=font, fill=255)
    rng = random.Random(len(text))
    noise = Image.new("L", stamp.size)
    noise.putdata([rng.randint(70, 255) for _ in range(stamp.width * stamp.height)])
    noise = noise.filter(ImageFilter.GaussianBlur(1.0))
    a = (np.array(stamp).astype(float) / 255.0) * (np.array(noise).astype(float) / 255.0)
    a = np.clip(a * 1.5, 0, 1) * 255
    alpha = Image.fromarray(a.astype("uint8"))
    inked = Image.new("RGBA", stamp.size, (*color, 0))
    inked.putalpha(alpha)
    return inked


def illuminated_rubric_card(dropcap, body, ref):
    """Gold-leaf dropped capital + printed-Bible serif body + hairline rules
    + rubric reference. Proven grammar from _lettering_compare/_render_candidates.py."""
    img = Image.new("RGBA", (W, 460), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    dropcap_font = ImageFont.truetype(F_OLDENGL, 120)
    body_font = ImageFont.truetype(F_ZILLA_I, 42)
    ref_font = ImageFont.truetype(F_ZILLA, 24)
    margin = 90
    y0 = 40
    d.line([(margin, y0 - 18), (W - margin, y0 - 18)], fill=(*FADED_INK, 150), width=2)
    cap_bb = d.textbbox((0, 0), dropcap, font=dropcap_font)
    cap_w = cap_bb[2] - cap_bb[0]
    d.text((margin - cap_bb[0], y0), dropcap, font=dropcap_font, fill=(*GOLD, 255),
          stroke_width=2, stroke_fill=(*INK, 255))
    body_x0 = margin + cap_w + 16
    max_w = W - margin - body_x0
    lines = wrap_text(body, body_font, max_w, d)
    ly = y0 + 8
    for i, ln in enumerate(lines):
        x0 = body_x0 if i == 0 else margin
        d.text((x0, ly), ln, font=body_font, fill=(*INK, 255))
        ly += 54
    d.line([(margin, ly + 4), (W - margin, ly + 4)], fill=(*FADED_INK, 150), width=2)
    rb = d.textlength(ref, font=ref_font)
    d.text(((W - rb) / 2, ly + 20), ref, font=ref_font, fill=(*RUBRIC, 235))
    return img.crop((0, 0, W, ly + 60))


def scale_crop(im, w, h):
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def noise_layers():
    layers = []
    for seed in range(8):
        rng = random.Random(200 + seed)
        small = Image.new("L", (W // 4, H // 4))
        small.putdata([rng.randint(0, 255) for _ in range(small.width * small.height)])
        layers.append(small.resize((W, H), Image.BILINEAR))
    return layers


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
    for name, t0, t1 in SHOTS:
        src = CLIPS / f"{name}.mp4"
        if not src.exists():
            raise SystemExit(f"missing clip: {src}")
        d = work / f"_{name}"
        d.mkdir()
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                        "-r", str(FPS), str(d / "f%05d.png")], check=True)
        frames[name] = sorted(d.glob("f*.png"))

    isaiah_card = illuminated_rubric_card(
        "A", "nd the LORD hath laid on him the iniquity of us all.", "ISAIAH 53:6")
    finished_stamp = stamped_text("FINISHED.", F_ZILLA, 84, RUBRIC, letter_spacing=2)
    onepay_stamp = stamped_text("ONE TO PAY. ONE TO CARRY.", F_ZILLA, 52, INK,
                                letter_spacing=1, max_w=820)
    walkin_stamp = stamped_text("WALK IN.", F_ZILLA, 90, INK, letter_spacing=2)

    OVERLAYS = [  # (t0, t1, img, cx_frac, cy_frac)
        # ends well BEFORE g10 (47.91) starts -- the letterer law: type never
        # covers a face, and g10's Jesus fills this exact screen region.
        (43.9, 47.55, isaiah_card, 0.5, 0.735),
        (51.88, 55.0, finished_stamp, 0.5, 0.22),
        (23.0, 26.1, onepay_stamp, 0.5, 0.20),
        (67.0, TOTAL - 0.3, walkin_stamp, 0.5, 0.74),
    ]

    grain = noise_layers()
    n_frames = int(TOTAL * FPS)
    outdir = work / "grid"
    outdir.mkdir()

    prev_last = {"img": None}
    for i in range(n_frames):
        t = i / FPS
        shot = next((s for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1])
        name, t0, t1 = shot
        seq = frames[name]
        li = int((t - t0) * FPS)
        n = len(seq)
        cyc = 2 * n - 2 if n > 1 else 1
        j = li % cyc
        if j >= n:
            j = cyc - j
        frame = Image.open(seq[j]).convert("RGB")

        for tt, kind in TRANSITIONS.items():
            if tt <= t < tt + 0.4 and prev_last["img"] is not None:
                k = ease((t - tt) / 0.4)
                mask = transition_mask(kind, k)
                frame = Image.composite(frame, prev_last["img"], mask)

        for (oi0, oi1, img, cxf, cyf) in OVERLAYS:
            if oi0 <= t <= oi1:
                dt = t - oi0
                k = ease(min(1.0, dt / 0.18))
                s2 = 1.28 - 0.28 * k
                oimg = img.resize((int(img.width * s2), int(img.height * s2)), Image.LANCZOS)
                if k < 1.0:
                    oimg.putalpha(oimg.split()[3].point(lambda v: int(v * k)))
                ox = int(W * cxf - oimg.width / 2)
                oy = max(WM_TOP, int(H * cyf - oimg.height / 2))
                frame.paste(oimg, (ox, oy), oimg)

        g = grain[i % len(grain)]
        frame = Image.composite(
            frame.point(lambda v: min(255, v + 6)), frame,
            g.point(lambda v: 22 if v > 236 else 0))

        if abs(t + 1 / FPS - t1) < 1 / FPS:
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
    silence = "volume=0.22:enable='between(t,43.6,47.9)',"
    filt = (
        f"[1:a]{AFMT},apad=whole_dur={vdur},asplit=2[main][key];"
        f"[2:a]{AFMT},atrim=0:{vdur},afade=t=in:st=0:d=1.5,"
        f"afade=t=out:st=52.0:d=3.0,volume=-9dB,{silence}anull[musA];"
        f"[3:a]{AFMT},adelay=53200|53200,atrim=0:{vdur},"
        f"afade=t=in:st=53.2:d=2.5,afade=t=out:st={vdur - 2.0:.1f}:d=2.0,"
        f"volume=-8dB[musB];"
        f"[musA][musB]amix=inputs=2:normalize=0[mus];"
        f"[mus][key]sidechaincompress={SIDECHAIN}[musd];"
        f"[4:a]{AFMT},atrim=0:{vdur},volume=-27dB[amb];"
        f"[5:a]atrim=0:1.4,volume=0.55,adelay=54100|54100,{AFMT}[rip];"
        f"[6:a]atrim=0:0.9,lowpass=f=700,volume=0.4,adelay=54300|54300,{AFMT}[boom];"
        f"[main][musd][amb][rip][boom]amix=inputs=5:normalize=0,"
        f"alimiter=limit=0.97,aresample=44100[mix]"
    )
    subprocess.run(["ffmpeg", "-y", "-v", "error",
                    "-i", str(silent), "-i", str(AUD / "narration.mp3"),
                    "-i", str(MUS / "lonely_searching_a.mp3"),
                    "-i", str(MUS / "sacred_grace_rise_a.mp3"),
                    "-i", str(SND / "air_hollow_desolate.mp3"),
                    "-i", str(SND / "veil_tearing.mp3"),
                    "-i", str(SND / "impact_low_boom.mp3"),
                    "-filter_complex", filt,
                    "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-t", f"{vdur}",
                    str(OUT)], check=True)
    shutil.rmtree(work)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
