"""Bronze Serpent -- step 6: hand-written ink captions over the FULL episode
(living-sketchbook finishing-gap fix, user-approved 2026-08-01 -- see memory
`sketchbook-shorts-finishing-gap`). Promoted from the approved `_caption_test.py`
prototype (0-8.3s window, user reaction: "its good" after a bolder stroke pass)
to the full 71.5s cut. Same technique, same constants -- nothing about the
look changed, only the time range.

Post-process only -- overlays onto the already-watermarked
BRONZESERPENT_living_sketchbook_sfx.mp4, does not touch _s4/_s5/watermark.
Word-timed from the real alignment JSON, chunks break on a >=0.35s pause or
6 words. The one on-screen text device already in this episode (the John 3:14
Scribed Ink verse card, 42.4-43.6s) sits inside a real 1.57s speech pause
(42.316-43.887s per _TIMING.md) -- no word is being spoken then, so no caption
chunk naturally lands there. Kept an explicit skip anyway as a defensive
second check, not a fix for an observed clash.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_s6_captions.py
"""
import json
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
ALIGN_PATH = HERE / "_bronzeserpent_alignment.json"
SRC = HERE / "BRONZESERPENT_living_sketchbook_sfx.mp4"
OUT = HERE / "BRONZESERPENT_living_sketchbook_cc.mp4"

W, H = 1080, 1920
TOTAL = 71.5

F_KEEPER = "C:/Windows/Fonts/Inkfree.ttf"
INK = (35, 30, 26, 255)
PARCHMENT = (247, 242, 228)

CAPTION_Y_FRAC = 0.78
MAX_TEXT_W = int(W * 0.80)
GAP_BREAK = 0.35
MAX_WORDS = 6
MIN_CHUNK_DUR = 0.45
STROKE_W = 2

VERSE_CARD_T0, VERSE_CARD_T1 = 42.4, 43.6  # defensive skip, see module docstring


def load_words():
    return json.loads(ALIGN_PATH.read_text(encoding="utf-8"))


def chunk_words(words):
    chunks = []
    cur = []
    for w in words:
        if cur and (w["start"] - cur[-1]["end"] >= GAP_BREAK or len(cur) >= MAX_WORDS):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)

    merged = []
    for c in chunks:
        dur = c[-1]["end"] - c[0]["start"]
        if merged and dur < MIN_CHUNK_DUR and len(merged[-1]) + len(c) <= MAX_WORDS + 2:
            merged[-1].extend(c)
        else:
            merged.append(c)

    # defensive: drop (or trim) any chunk overlapping the verse-card window
    out = []
    for c in merged:
        t0, t1 = c[0]["start"], c[-1]["end"]
        if t1 >= VERSE_CARD_T0 and t0 <= VERSE_CARD_T1:
            continue
        out.append(c)
    return out


def render_chunk_png(chunk, seed):
    rng = random.Random(seed)
    text = " ".join(w["w"] for w in chunk)

    size = 58
    font = ImageFont.truetype(F_KEEPER, size)
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    while probe.textlength(text, font=font) > MAX_TEXT_W and size > 34:
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
        jx = rng.uniform(-2, 2)
        jy = rng.uniform(-3, 3)
        ang = rng.uniform(-1.6, 1.6)
        word_img = Image.new("RGBA", (int(wid) + 24, size + 24), (0, 0, 0, 0))
        wd = ImageDraw.Draw(word_img)
        wd.text((12, 8), w["w"], font=font, fill=INK, stroke_width=STROKE_W, stroke_fill=INK)
        word_img = word_img.rotate(ang, resample=Image.BICUBIC, expand=False)
        canvas.alpha_composite(word_img, (int(x + jx - 12), int(baseline_y + jy - 8)))
        x += wid + sp

    return canvas


def main():
    if not SRC.exists():
        raise SystemExit(f"missing base cut: {SRC}")
    words = load_words()
    chunks = chunk_words(words)
    print(f"[chunks] {len(chunks)} caption chunks across {TOTAL}s")

    work = HERE / "_caption_frames"
    work.mkdir(exist_ok=True)
    pngs = []
    for i, chunk in enumerate(chunks):
        img = render_chunk_png(chunk, seed=100 + i)
        p = work / f"cap_{i:03d}.png"
        img.save(p)
        pngs.append((p, chunk[0]["start"], chunk[-1]["end"]))

    inputs = ["-i", str(SRC)]
    filt_parts = []
    last = "0:v"
    for i, (p, t0, t1) in enumerate(pngs):
        inputs += ["-i", str(p)]
        idx = i + 1
        label = f"v{idx}"
        filt_parts.append(
            f"[{last}][{idx}:v]overlay=0:0:enable="
            f"'between(t,{t0:.3f},{t1 + 0.12:.3f})'[{label}]"
        )
        last = label

    filt = ";".join(filt_parts)
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs,
           "-filter_complex", filt, "-map", f"[{last}]", "-map", "0:a",
           "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(OUT)]
    subprocess.run(cmd, check=True)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
