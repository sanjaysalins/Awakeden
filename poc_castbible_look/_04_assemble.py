"""cast-bible look POC — step 4: assemble the 30s taste piece.
Documentary rostrum-camera moves over the sketch spreads (push/drift/pull),
the Seedance rain window, glow pulse on the radiant door, editorial typography
pops (Arial Black + yellow highlighter + ink-red verse cards, red-letter for
Jesus' words), then narration + cold-to-warm score + SFX, INV-26 hold.

  .venv\\Scripts\\python.exe poc_castbible_look/_04_assemble.py
"""
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN  # noqa

HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
CLIPS = HERE / "clips"
AUD = HERE / "audio"
OUT = HERE / "NOAH_THE_DOOR_castbible_poc.mp4"

W, H, FPS = 1920, 1080, 30
TOTAL = 30.5
INK = (30, 26, 24)
RED = (168, 34, 28)
CREAM = (243, 233, 212)
HILITE = (250, 230, 90)
F_BLACK = "C:/Windows/Fonts/ariblk.ttf"

SCORE_FEAR = ROOT / "music_library" / "clips" / "lonely_searching_a.mp3"
SCORE_GRACE = ROOT / "music_library" / "clips" / "sacred_grace_rise_a.mp3"
SND = ROOT / "sound_library" / "clips"

# (still, t0, t1, move, p0, p1)  move: push | pull | drift | rainclip | glowpush
SHOTS = [
    ("s1_builder", 0.0, 5.6, "push", 1.00, 1.07),
    ("s2_rain", 5.6, 10.8, "rainclip", 1.00, 1.04),
    ("s3_shut", 10.8, 14.1, "push", 1.02, 1.10),
    ("s4_onedoor", 14.1, 16.5, "drift", 1.03, 1.03),
    ("s5_thedoor", 16.5, 23.0, "glowpush", 1.00, 1.06),
    ("s6_landing", 23.0, TOTAL, "pull", 1.08, 1.00),
]


def ease(t):
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def type_img(text, size, fill, hilite=False, underline=None, card=False):
    font = ImageFont.truetype(F_BLACK, size)
    lines = text.split("\n")
    pad = int(size * 0.35)
    line_h = int(size * 1.18)
    tw = max(font.getbbox(ln)[2] for ln in lines)
    th = line_h * len(lines)
    img = Image.new("RGBA", (tw + 4 * pad, th + 3 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = pad
    for ln in lines:
        bb = font.getbbox(ln)
        x = 2 * pad
        if card:
            d.rectangle([x - pad, y - int(pad * 0.4),
                         x + bb[2] + pad, y + line_h], fill=(*RED, 255))
            d.text((x, y), ln, font=font, fill=(*CREAM, 255))
        else:
            if hilite:
                d.rectangle([x - int(pad * 0.5), y + int(size * 0.18),
                             x + bb[2] + int(pad * 0.5), y + int(size * 1.08)],
                            fill=(*HILITE, 215))
            d.text((x + 4, y + 5), ln, font=font, fill=(0, 0, 0, 70))
            d.text((x, y), ln, font=font, fill=(*fill, 255))
            if underline:
                d.rectangle([x, y + int(size * 1.12), x + bb[2], y + int(size * 1.12) + 10],
                            fill=(*underline, 255))
        y += line_h
    return img.rotate(-1.5, expand=True, resample=Image.BICUBIC)


# (t_in, t_out, img, cx_frac, cy_frac)
OVERLAYS = [
    (1.2, 5.5, type_img("THE BUILDER.", 58, INK, hilite=True), 0.80, 0.14),
    (11.0, 13.95, type_img("AND THE LORD\nSHUT HIM IN.", 96, INK, hilite=True), 0.32, 0.36),
    (11.5, 13.95, type_img("GENESIS 7:16", 34, INK, card=True), 0.24, 0.62),
    (14.15, 16.45, type_img("ONE DOOR.", 150, INK, hilite=True), 0.50, 0.46),
    (17.0, 22.95, type_img("I AM THE DOOR.", 110, RED, underline=(201, 164, 92)), 0.50, 0.22),
    (17.5, 22.95, type_img("JOHN 10:9", 34, INK, card=True), 0.50, 0.40),
    (26.3, TOTAL - 0.1, type_img("STILL OPEN.", 96, INK, hilite=True), 0.50, 0.74),
]


def load_frames_16x9(name):
    im = Image.open(STILLS / f"{name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - W) // 2, (zh - H) // 2,
                    ((zw - W) // 2) + W, ((zh - H) // 2) + H))


def main():
    rain_frames = []
    rain_mp4 = CLIPS / "s2_rain.mp4"
    work = HERE / "_frames"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    if rain_mp4.exists():
        d = work / "_rain"
        d.mkdir()
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(rain_mp4),
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                        "-r", str(FPS), str(d / "r%05d.png")], check=True)
        rain_frames = sorted(d.glob("r*.png"))

    base = {name: load_frames_16x9(name) for name, *_ in SHOTS}

    n_frames = int(TOTAL * FPS)
    for i in range(n_frames):
        t = i / FPS
        shot = next(s for s in SHOTS if s[1] <= t < s[2] or s is SHOTS[-1] and t >= s[1])
        name, t0, t1, move, p0, p1 = shot
        k = ease((t - t0) / max(0.001, t1 - t0))
        if move == "rainclip" and rain_frames:
            fi = min(len(rain_frames) - 1, int((t - t0) * FPS))
            src = Image.open(rain_frames[fi]).convert("RGB")
        else:
            src = base[name]
        z = p0 + (p1 - p0) * k
        if move == "drift":
            z = p0
        zw, zh = int(W * z), int(H * z)
        frame = src.resize((zw, zh), Image.LANCZOS)
        dx = (zw - W) // 2
        dy = (zh - H) // 2
        if move == "drift":
            dy += int(-18 * k)
        frame = frame.crop((dx, dy, dx + W, dy + H))
        if move == "glowpush":
            frame = ImageEnhance.Brightness(frame).enhance(1.0 + 0.045 * math.sin(t * 2.2))

        for (ti, to, img, cxf, cyf) in OVERLAYS:
            if ti <= t <= to:
                dt = t - ti
                ka = ease(min(1.0, dt / 0.18))
                s2 = 1.30 - 0.30 * ka
                oi = img.resize((int(img.width * s2), int(img.height * s2)), Image.LANCZOS)
                if ka < 1.0:
                    oi.putalpha(oi.split()[3].point(lambda v: int(v * ka)))
                ox = int(W * cxf - oi.width / 2)
                oy = int(H * cyf - oi.height / 2)
                frame.paste(oi, (ox, oy), oi)

        frame.save(work / f"f{i:05d}.png")

    silent = HERE / "_silent.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-r", str(FPS), str(silent)], check=True)

    vdur = TOTAL
    filt = (
        f"[1:a]{AFMT},apad=whole_dur={vdur},asplit=2[main][key];"
        f"[2:a]{AFMT},atrim=0:{vdur},afade=t=in:st=0:d=1.5,"
        f"afade=t=out:st=15.5:d=3.5,volume=-9dB[musA];"
        f"[3:a]{AFMT},adelay=16500|16500,atrim=0:{vdur},"
        f"afade=t=in:st=16.5:d=2.5,afade=t=out:st={vdur - 2.0:.1f}:d=2.0,volume=-8dB[musB];"
        f"[musA][musB]amix=inputs=2:normalize=0[mus];"
        f"[mus][key]sidechaincompress={SIDECHAIN}[musd];"
        f"[4:a]{AFMT},atrim=0:{vdur},volume=-25dB[wind];"
        f"[5:a]atrim=0:5,volume=-13dB,adelay=5600|5600,{AFMT}[thn];"
        f"[6:a]atrim=0:1.0,lowpass=f=700,volume=0.55,adelay=11400|11400,{AFMT}[shut];"
        f"[7:a]atrim=0:2.2,volume=-13dB,adelay=16600|16600,{AFMT}[creak];"
        f"[main][musd][wind][thn][shut][creak]amix=inputs=6:normalize=0,"
        f"alimiter=limit=0.97,aresample=44100[mix]"
    )
    subprocess.run(["ffmpeg", "-y", "-v", "error",
                    "-i", str(silent), "-i", str(AUD / "narration.mp3"),
                    "-i", str(SCORE_FEAR), "-i", str(SCORE_GRACE),
                    "-i", str(SND / "wind_desert_bleak.mp3"),
                    "-i", str(SND / "thunder_low_roll.mp3"),
                    "-i", str(SND / "impact_low_boom.mp3"),
                    "-i", str(SND / "door_gate_creak.mp3"),
                    "-filter_complex", filt,
                    "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-t", f"{vdur}",
                    str(OUT)], check=True)
    shutil.rmtree(work)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
