"""Hand-written ink caption PROTOTYPE (living-sketchbook finishing-gap fix,
see memory `sketchbook-shorts-finishing-gap` -- captions were reopened, not
settled, and the plan calls for a look-and-feel test before committing to a
retrofit across all 6 shipped pieces).

Post-process only -- does NOT touch _s4_assemble.py or the render pipeline.
Overlays hand-lettered (Inkfree.ttf, same "quick pencil hand" register as the
Keeper's Hand marginalia -- see storm/_keeper_poc/_build_poc.py F_KEEPER) caption
chunks onto the ALREADY-FINISHED BRONZESERPENT_living_sketchbook_sfx.mp4, word-
timed from the real alignment JSON. Chunks break on a >=0.35s pause or 5 words,
whichever comes first. Sits at H*0.78 -- clear of the 9:16 bottom-18% platform-UI
band and the right ~10-12% comment rail (shorts-caption-safe-zone memory). A soft
low-opacity parchment scrim (not a solid modern subtitle bar) sits behind the text
for legibility against busy art.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_caption_test.py
"""
import json
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
ALIGN_PATH = HERE / "_bronzeserpent_alignment.json"
SRC = HERE / "BRONZESERPENT_living_sketchbook_sfx.mp4"
OUT = HERE / "_caption_test_0_8.mp4"

W, H = 1080, 1920
TEST_T0, TEST_T1 = 0.0, 8.3  # s01 + s02 -- one full sentence + a natural chunk break

F_KEEPER = "C:/Windows/Fonts/Inkfree.ttf"
INK = (35, 30, 26, 255)
PARCHMENT = (247, 242, 228)

CAPTION_Y_FRAC = 0.78     # clear of the bottom-18% UI band (0.82 floor)
MAX_TEXT_W = int(W * 0.80)  # 8% side margins, clear of the right comment rail
GAP_BREAK = 0.35
MAX_WORDS = 6
MIN_CHUNK_DUR = 0.45  # merge a too-short tail chunk into its predecessor


def load_words():
    return json.loads(ALIGN_PATH.read_text(encoding="utf-8"))


def chunk_words(words, t0, t1):
    chunks = []
    cur = []
    for w in words:
        if w["start"] < t0 or w["end"] > t1:
            if w["start"] >= t1:
                break
            continue
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
    return merged


def render_chunk_png(chunk, seed):
    """One transparent 1080x1920 PNG per chunk -- static hand-lettered line
    (not a stroke-by-stroke write-on; captions must track speech pace, the
    slow animated write is reserved for the rare LAW-1 emphasis moments the
    Scribed Ink verse card already owns)."""
    rng = random.Random(seed)
    text = " ".join(w["w"] for w in chunk)

    size = 58
    font = ImageFont.truetype(F_KEEPER, size)
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    while probe.textlength(text, font=font) > MAX_TEXT_W and size > 34:
        size -= 2
        font = ImageFont.truetype(F_KEEPER, size)

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # lay out words left-to-right with small per-word jitter (rotation/baseline)
    # for a hand-written feel, centered as a block
    sp = probe.textlength(" ", font=font)
    widths = [probe.textlength(w["w"], font=font) for w in chunk]
    total_w = sum(widths) + sp * (len(chunk) - 1)
    x = (W - total_w) / 2
    baseline_y = int(H * CAPTION_Y_FRAC)

    # scrim: soft rounded parchment card behind the text, tight to its bounds
    pad_x, pad_y = 22, 14
    scrim = Image.new("RGBA", (int(total_w) + pad_x * 2, size + pad_y * 2), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    sd.rounded_rectangle(
        [0, 0, scrim.width - 1, scrim.height - 1], radius=14,
        fill=(*PARCHMENT, 158))
    scrim = scrim.filter(ImageFilter.GaussianBlur(0.6))
    canvas.alpha_composite(scrim, (int(x - pad_x), int(baseline_y - pad_y)))

    for w, wid in zip(chunk, widths):
        jx = rng.uniform(-2, 2)
        jy = rng.uniform(-3, 3)
        ang = rng.uniform(-1.6, 1.6)
        word_img = Image.new("RGBA", (int(wid) + 24, size + 24), (0, 0, 0, 0))
        wd = ImageDraw.Draw(word_img)
        wd.text((12, 8), w["w"], font=font, fill=INK, stroke_width=2, stroke_fill=INK)
        word_img = word_img.rotate(ang, resample=Image.BICUBIC, expand=False)
        canvas.alpha_composite(word_img, (int(x + jx - 12), int(baseline_y + jy - 8)))
        x += wid + sp

    return canvas


def main():
    words = load_words()
    chunks = chunk_words(words, TEST_T0, TEST_T1)
    if not chunks:
        raise SystemExit("no words in test window")

    work = HERE / "_caption_test_frames"
    work.mkdir(exist_ok=True)
    pngs = []
    for i, chunk in enumerate(chunks):
        img = render_chunk_png(chunk, seed=100 + i)
        p = work / f"cap_{i:02d}.png"
        img.save(p)
        pngs.append((p, chunk[0]["start"], chunk[-1]["end"]))
        print(f"  chunk {i}: {chunk[0]['start']:.2f}-{chunk[-1]['end']:.2f}s  "
              f"\"{' '.join(w['w'] for w in chunk)}\"")

    inputs = ["-ss", str(TEST_T0), "-t", str(TEST_T1 - TEST_T0), "-i", str(SRC)]
    filt_parts = []
    last = "0:v"
    for i, (p, t0, t1) in enumerate(pngs):
        inputs += ["-i", str(p)]
        idx = i + 1
        # overlay times are relative to the trimmed clip (subtract TEST_T0)
        rt0, rt1 = t0 - TEST_T0, t1 - TEST_T0
        POP = 0.08
        label = f"v{idx}"
        filt_parts.append(
            f"[{last}][{idx}:v]overlay=0:0:enable="
            f"'between(t,{rt0:.3f},{rt1 + 0.12:.3f})'[{label}]"
        )
        last = label

    filt = ";".join(filt_parts)
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs,
           "-filter_complex", filt, "-map", f"[{last}]", "-map", "0:a",
           "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", str(OUT)]
    subprocess.run(cmd, check=True)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
