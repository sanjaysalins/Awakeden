"""POC v3 -- fixes 2 real defects found in POC2 by eye:
1. Captions used _short_captions.py's OWN historically-tuned 9:16 constants
   (CAPTION_Y_FRAC=0.78, MAX_TEXT_W=80% width, font start 58) instead of
   Noah's actual proportions (_finish_long.py: 0.86, 72%, 46) -- close family
   (same font/ink/scrim), but NOT the same relative size/position. Ported
   Noah's exact fractions onto this 9:16 canvas here so they're genuinely
   the same standard, not two independently-tuned scripts that merely look
   similar. (chunk_words/render_chunk_png below are Noah's own constants,
   copied verbatim from _finish_long.py, not reinvented.)
2. POC2 used a flat static hold on each still -- violates this project's own
   locked no-static rule. Replaced with a real $0 push-in camera move, same
   eased-zoom technique Noah's OWN _04_assemble.py uses on every one of its
   shots (cosine ease, gradual scale 1.00->1.06), piped as raw frames
   directly into ffmpeg (no per-frame PNGs written to disk).

  .venv\\Scripts\\python.exe batches/cluster_01_cross/forsaken_cry_ps221/_poc3_final_sketchbook.py
"""
import json
import math
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.resolve().parents[2]
sys.path.insert(0, str(ROOT / "poc_castbible_look"))
from _polite import be_polite  # noqa: E402

AUD = HERE / "audio" / "narration.mp3"
STILLS = HERE / "_poc_sketchbook_stills"
WORK = HERE / "_poc3_work"
SILENT = HERE / "_poc3_silent.mp4"
MUXED = HERE / "_poc3_muxed.mp4"
OUT = HERE / "_POC3_sketchbook_art_captions_motion.mp4"

W, H, FPS = 1080, 1920, 30

# ---- Noah's exact caption constants (_finish_long.py, verbatim) ----------
F_KEEPER = "C:/Windows/Fonts/Inkfree.ttf"
INK = (35, 30, 26, 255)
PARCHMENT = (247, 242, 228)
CAPTION_Y_FRAC = 0.86
MAX_TEXT_W = int(W * 0.72)
GAP_BREAK = 0.35
MAX_WORDS = 6
MIN_CHUNK_DUR = 0.45
STROKE_W = 2
FONT_SIZE0 = 46
FONT_SIZE_MIN = 30

# (still, window_start, window_end, zoom_end)
SEGMENTS = [
    ("s_golgotha_sketchbook.png", 9.8, 15.05, 1.06),
    ("s_bowedhead_sketchbook.png", 27.15, 31.9, 1.07),
]


def ease(t):
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def chunk_words(words, skips):
    chunks, cur = [], []
    for w in words:
        if cur and (w["start"] - cur[-1]["end"] >= GAP_BREAK or len(cur) >= MAX_WORDS):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    merged = []
    for c in chunks:
        d = c[-1]["end"] - c[0]["start"]
        if merged and d < MIN_CHUNK_DUR and len(merged[-1]) + len(c) <= MAX_WORDS + 2:
            merged[-1].extend(c)
        else:
            merged.append(c)
    out = []
    for c in merged:
        t0, t1 = c[0]["start"], c[-1]["end"]
        if any(t1 >= s0 and t0 <= s1 for s0, s1 in skips):
            continue
        out.append(c)
    return out


def render_chunk_png(chunk, seed):
    rng = random.Random(seed)
    text = " ".join(w["w"] for w in chunk)
    size = FONT_SIZE0
    font = ImageFont.truetype(F_KEEPER, size)
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    while probe.textlength(text, font=font) > MAX_TEXT_W and size > FONT_SIZE_MIN:
        size -= 2
        font = ImageFont.truetype(F_KEEPER, size)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sp = probe.textlength(" ", font=font)
    widths = [probe.textlength(w["w"], font=font) for w in chunk]
    total_w = sum(widths) + sp * (len(chunk) - 1)
    x = (W - total_w) / 2
    baseline_y = int(H * CAPTION_Y_FRAC)
    pad_x, pad_y = 22, 14
    scrim = Image.new("RGBA", (int(total_w) + pad_x * 2, size + pad_y * 2), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    sd.rounded_rectangle([0, 0, scrim.width - 1, scrim.height - 1], radius=14, fill=(*PARCHMENT, 158))
    scrim = scrim.filter(ImageFilter.GaussianBlur(0.6))
    canvas.alpha_composite(scrim, (int(x - pad_x), int(baseline_y - pad_y)))
    for w, wid in zip(chunk, widths):
        jx, jy, ang = rng.uniform(-2, 2), rng.uniform(-3, 3), rng.uniform(-1.6, 1.6)
        word_img = Image.new("RGBA", (int(wid) + 24, size + 24), (0, 0, 0, 0))
        wd = ImageDraw.Draw(word_img)
        wd.text((12, 8), w["w"], font=font, fill=INK, stroke_width=STROKE_W, stroke_fill=INK)
        word_img = word_img.rotate(ang, resample=Image.BICUBIC, expand=False)
        canvas.alpha_composite(word_img, (int(x + jx - 12), int(baseline_y + jy - 8)))
        x += wid + sp
    return canvas


def build_pushin_clip(src_png: Path, dur: float, zoom_end: float, out: Path):
    im = Image.open(src_png).convert("RGB")
    s = max(W / im.width, H / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    base = im.resize((zw, zh), Image.LANCZOS)
    n_frames = int(dur * FPS)
    proc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out)],
        stdin=subprocess.PIPE)
    for i in range(n_frames):
        k = ease(i / max(1, n_frames - 1))
        z = 1.00 + (zoom_end - 1.00) * k
        fw, fh = int(zw * z), int(zh * z)
        frame = base.resize((fw, fh), Image.LANCZOS)
        dx, dy = (fw - W) // 2, (fh - H) // 2
        frame = frame.crop((dx, dy, dx + W, dy + H))
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    proc.wait()


def main():
    be_polite()
    WORK.mkdir(exist_ok=True)

    clip_files = []
    for i, (name, t0, t1, zend) in enumerate(SEGMENTS):
        out = WORK / f"seg_{i}.mp4"
        print(f"[motion] {name} push-in 1.00->{zend} over {t1 - t0:.2f}s ...")
        build_pushin_clip(STILLS / name, t1 - t0, zend, out)
        clip_files.append(out)

    concat_list = WORK / "_concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in clip_files) + "\n", encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                     "-i", str(concat_list), "-c", "copy", str(SILENT)], check=True)
    print(f"[ok] {SILENT}")

    aud_segs = []
    for i, (name, t0, t1, zend) in enumerate(SEGMENTS):
        out = WORK / f"aud_{i}.aac"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(AUD),
                         "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}",
                         "-c:a", "aac", "-b:a", "192k", str(out)], check=True)
        aud_segs.append(out)
    aud_concat_list = WORK / "_aud_concat.txt"
    aud_concat_list.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in aud_segs) + "\n", encoding="utf-8")
    aud_out = WORK / "_aud_full.aac"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                     "-i", str(aud_concat_list), "-c", "copy", str(aud_out)], check=True)

    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(SILENT), "-i", str(aud_out),
                     "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                     "-b:a", "192k", str(MUXED)], check=True)
    print(f"[ok] {MUXED}")

    all_words = json.loads((HERE / "audio" / "alignment.json").read_text(encoding="utf-8"))
    words = []
    running = 0.0
    for (name, t0, t1, zend) in SEGMENTS:
        dur = t1 - t0
        for w in all_words:
            if w["start"] >= t0 and w["end"] <= t1:
                words.append({"w": w["w"], "start": w["start"] - t0 + running,
                              "end": w["end"] - t0 + running})
        running += dur

    chunks = chunk_words(words, skips=[])
    print(f"[chunks] {len(chunks)}")
    pngs = []
    for i, c in enumerate(chunks):
        img = render_chunk_png(c, seed=100 + i)
        p = WORK / f"cap_{i:03d}.png"
        img.save(p)
        pngs.append((p, c[0]["start"], c[-1]["end"]))

    inputs = ["-i", str(MUXED)]
    filt_parts, last = [], "0:v"
    for i, (p, t0, t1) in enumerate(pngs):
        inputs += ["-i", str(p)]
        idx, label = i + 1, f"v{i + 1}"
        filt_parts.append(f"[{last}][{idx}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1 + 0.12:.3f})'[{label}]")
        last = label
    filt = ";".join(filt_parts)
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", filt,
           "-map", f"[{last}]", "-map", "0:a", "-c:v", "libx264", "-crf", "18",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", str(OUT)]
    subprocess.run(cmd, check=True)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
