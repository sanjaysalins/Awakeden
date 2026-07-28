"""Door episode sketch POC — step 4: assemble the full ~58s episode.
12 animated sketch spreads (pingpong-looped where the window outruns the
clip), editorial type overlays, the LOCKED narration.mp3, cold-to-warm score
turning at the door-opening (43.8s), SFX, INV-26 hold.

  .venv\\Scripts\\python.exe poc_castbible_look/episode_door/_e4_assemble.py
"""
import math
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN  # noqa

HERE = Path(__file__).resolve().parent
CLIPS = HERE / "clips"
OUT = HERE / "AT_THE_DOOR_sketch_poc.mp4"

W, H, FPS = 1080, 1920, 30
TOTAL = 58.3
INK = (30, 26, 24)
RED = (168, 34, 28)
CREAM = (243, 233, 212)
HILITE = (250, 230, 90)
GOLD = (201, 164, 92)
F_BLACK = "C:/Windows/Fonts/ariblk.ttf"

NARR = (ROOT.parent / "PythonProject1" / "jesus" / "narration" /
        "36_In_No_Wise_Cast_Out" / "v1" / "narration.mp3")
SCORE_FEAR = ROOT / "music_library" / "clips" / "lonely_searching_a.mp3"
SCORE_GRACE = ROOT / "music_library" / "clips" / "sacred_grace_rise_a.mp3"
SND = ROOT / "sound_library" / "clips"

SHOTS = [
    ("d01_hook", 0.0, 5.2), ("d02_record", 5.2, 10.1),
    ("d03_rehearsing", 10.1, 13.3), ("d04_answered", 13.3, 16.1),
    ("d05_hiswords", 16.1, 18.7), ("d06_verse", 18.7, 25.6),
    ("d07_exception", 25.6, 31.1), ("d08_toofargone", 31.1, 36.7),
    ("d09_nailed", 36.7, 43.8), ("d10_opendoor", 43.8, 48.7),
    ("d11_welcome", 48.7, 52.0), ("d12_landing", 52.0, TOTAL),
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
                d.rectangle([x, y + int(size * 1.12), x + bb[2], y + int(size * 1.12) + 9],
                            fill=(*underline, 255))
        y += line_h
    return img.rotate(-1.5, expand=True, resample=Image.BICUBIC)


OVERLAYS = [
    (3.0, 5.1, type_img("AT THE DOOR.", 54, INK, hilite=True), 0.50, 0.12),
    (21.6, 25.5, type_img("IN NO WISE CAST OUT.", 60, RED, underline=GOLD), 0.50, 0.135),
    (22.1, 25.5, type_img("JOHN 6:37", 30, INK, card=True), 0.50, 0.66),
    (34.0, 36.6, type_img("TOO FAR GONE.", 76, INK, hilite=True), 0.50, 0.24),
    (37.8, 40.4, type_img("NO FINE PRINT.", 76, INK, hilite=True), 0.50, 0.72),
    (53.2, 57.9, type_img("NEVER LOCKED.", 84, INK, hilite=True), 0.50, 0.74),
]

WM_ZONE_H = 160  # keep type below the top-left watermark band


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
        print(f"[frames] {name}: {len(frames[name])}")

    n_frames = int(TOTAL * FPS)
    outdir = work / "grid"
    outdir.mkdir()
    for i in range(n_frames):
        t = i / FPS
        shot = next((s for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1])
        name, t0, t1 = shot
        seq = frames[name]
        li = int((t - t0) * FPS)
        n = len(seq)
        cycle = 2 * n - 2 if n > 1 else 1
        j = li % cycle
        if j >= n:
            j = cycle - j
        frame = Image.open(seq[j]).convert("RGB")

        for (ti, to, img, cxf, cyf) in OVERLAYS:
            if ti <= t <= to:
                dt = t - ti
                ka = ease(min(1.0, dt / 0.18))
                s2 = 1.30 - 0.30 * ka
                oi = img.resize((int(img.width * s2), int(img.height * s2)), Image.LANCZOS)
                if ka < 1.0:
                    oi.putalpha(oi.split()[3].point(lambda v: int(v * ka)))
                ox = int(W * cxf - oi.width / 2)
                oy = max(WM_ZONE_H, int(H * cyf - oi.height / 2))
                frame.paste(oi, (ox, oy), oi)

        frame.save(outdir / f"g{i:05d}.png")

    silent = HERE / "_silent.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-i", str(outdir / "g%05d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-r", str(FPS), str(silent)], check=True)

    vdur = TOTAL
    filt = (
        f"[1:a]{AFMT},apad=whole_dur={vdur},asplit=2[main][key];"
        f"[2:a]{AFMT},atrim=0:{vdur},afade=t=in:st=0:d=1.5,"
        f"afade=t=out:st=42.3:d=4.0,volume=-9dB[musA];"
        f"[3:a]{AFMT},adelay=43800|43800,atrim=0:{vdur},"
        f"afade=t=in:st=43.8:d=2.5,afade=t=out:st={vdur - 2.0:.1f}:d=2.0,volume=-8dB[musB];"
        f"[musA][musB]amix=inputs=2:normalize=0[mus];"
        f"[mus][key]sidechaincompress={SIDECHAIN}[musd];"
        f"[4:a]{AFMT},atrim=0:{vdur},volume=-25dB[wind];"
        f"[5:a]atrim=0:2.2,volume=-12dB,adelay=43900|43900,{AFMT}[creak];"
        f"[6:a]atrim=0:1.2,volume=0.4,adelay=37800|37800,{AFMT}[nail];"
        f"[7:a]atrim=0:0.8,lowpass=f=800,volume=0.3,asplit=3[b1][b2][b3];"
        f"[b1]adelay=21600|21600,{AFMT}[boomA];"
        f"[b2]adelay=34000|34000,{AFMT}[boomB];"
        f"[b3]adelay=53200|53200,{AFMT}[boomC];"
        f"[main][musd][wind][creak][nail][boomA][boomB][boomC]"
        f"amix=inputs=8:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
    )
    subprocess.run(["ffmpeg", "-y", "-v", "error",
                    "-i", str(silent), "-i", str(NARR),
                    "-i", str(SCORE_FEAR), "-i", str(SCORE_GRACE),
                    "-i", str(SND / "wind_desert_bleak.mp3"),
                    "-i", str(SND / "door_gate_creak.mp3"),
                    "-i", str(SND / "nail_strike_single.mp3"),
                    "-i", str(SND / "impact_low_boom.mp3"),
                    "-filter_complex", filt,
                    "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-t", f"{vdur}",
                    str(OUT)], check=True)
    shutil.rmtree(work)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
