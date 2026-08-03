"""Bronze Serpent LONG -- step 10: hand-written ink captions, adapted from
the SHORT's own locked recipe (bronze_serpent/_s6_captions.py, user-approved
2026-08-01, memory `sketchbook-shorts-finishing-gap`) for LANDSCAPE (1920x1080
vs the short's 1080x1920) and this film's real ~592s length vs the short's
71.5s. Same technique, same look -- Inkfree font, ink + parchment scrim,
per-word jitter, word-timed chunks off the real alignment JSON. Nothing about
the DESIGN changed, only the canvas geometry, time range, and (new for this
length) BATCHING.

301 chunks over ~592s is too many overlay nodes for one ffmpeg filter graph
(the short's 71.5s cut never needed this) -- so this splits the film into
~60s SEGMENTS (same segment-then-concat shape _s7_assemble.py already uses),
overlays each segment's own caption chunks locally (retimed to segment-
relative t=0), then concats -- same technique as the short, just chunked so
each ffmpeg call stays small, fast, and resumable (segments already built
are skipped on a re-run).

Post-process only -- overlays onto the already-scored+sfx'd film, does not
touch _s7/_s8/_s9/watermark.

Two on-screen-lettering insert pages (s43 Scholar's-Margin diptych, s67
Gilded Proclamation) already bake their own verse text into the art itself
-- same clash this project's own SHORT captions already defended against for
its one verse card. Both windows are skipped here too, read live from
_spread_windows.json rather than hardcoded, so a future retiming stays safe.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s10_captions.py
  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s10_captions.py --rebuild   # ignore existing segments
"""
import argparse
import json
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
ALIGN_PATH = HERE / "_alignment.json"
WINDOWS_PATH = HERE / "_spread_windows.json"
SRC = HERE / "BRONZESERPENT_LONG_living_sketchbook_scored_sfx.mp4"
OUT = HERE / "BRONZESERPENT_LONG_living_sketchbook_cc.mp4"
SEG_DIR = HERE / "_caption_segments"
WORK = HERE / "_caption_frames"

W, H = 1920, 1080
SEG_LEN = 60.0

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

SKIP_NAMES = ("s43_insert_scholars_margin2", "s67_insert_gilded_proclamation2")


def load_words():
    return json.loads(ALIGN_PATH.read_text(encoding="utf-8"))


def skip_windows():
    rows = {r["name"]: r for r in json.loads(WINDOWS_PATH.read_text(encoding="utf-8"))}
    return [(rows[n]["start"], rows[n]["end"]) for n in SKIP_NAMES]


def chunk_words(words, skips):
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


def ffprobe_dur(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def build_segment(seg_idx, seg_t0, seg_t1, chunks_in_seg, rebuild):
    seg_out = SEG_DIR / f"seg_{seg_idx:03d}.mp4"
    if seg_out.exists() and not rebuild:
        print(f"  [skip] {seg_out.name} already built")
        return seg_out

    pngs = []
    for i, chunk in enumerate(chunks_in_seg):
        img = render_chunk_png(chunk, seed=1000 * seg_idx + i)
        p = WORK / f"seg{seg_idx:03d}_cap_{i:03d}.png"
        img.save(p)
        local_t0 = chunk[0]["start"] - seg_t0
        local_t1 = chunk[-1]["end"] - seg_t0
        pngs.append((p, local_t0, local_t1))

    inputs = ["-ss", f"{seg_t0:.3f}", "-t", f"{seg_t1 - seg_t0:.3f}", "-i", str(SRC)]
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

    if filt_parts:
        filt = ";".join(filt_parts)
        cmd = ["ffmpeg", "-y", "-v", "error", *inputs,
               "-filter_complex", filt, "-map", f"[{last}]", "-map", "0:a",
               "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", str(seg_out)]
    else:
        cmd = ["ffmpeg", "-y", "-v", "error", *inputs,
               "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", str(seg_out)]
    subprocess.run(cmd, check=True)
    print(f"  [ok] {seg_out.name} ({len(pngs)} caption chunks)")
    return seg_out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()

    if not SRC.exists():
        raise SystemExit(f"missing scored+sfx film: {SRC} -- run _s9_sfx.py first")
    SEG_DIR.mkdir(exist_ok=True)
    WORK.mkdir(exist_ok=True)

    total = ffprobe_dur(SRC)
    words = load_words()
    skips = skip_windows()
    chunks = chunk_words(words, skips)
    print(f"[chunks] {len(chunks)} caption chunks across {total:.1f}s, "
          f"{len(skips)} insert-page windows skipped")

    n_segs = int(total // SEG_LEN) + 1
    seg_files = []
    for seg_idx in range(n_segs):
        seg_t0 = seg_idx * SEG_LEN
        seg_t1 = min(total, seg_t0 + SEG_LEN)
        if seg_t0 >= total:
            break
        chunks_in_seg = [c for c in chunks if c[0]["start"] < seg_t1 and c[-1]["end"] > seg_t0]
        print(f"[seg {seg_idx:03d}] {seg_t0:.1f}-{seg_t1:.1f}s, {len(chunks_in_seg)} chunks")
        seg_files.append(build_segment(seg_idx, seg_t0, seg_t1, chunks_in_seg, args.rebuild))

    concat_list = SEG_DIR / "_concat_list.txt"
    concat_list.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in seg_files) + "\n",
        encoding="utf-8")
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
           "-i", str(concat_list), "-c", "copy", "-movflags", "+faststart", str(OUT)]
    print("[concat] joining segments...")
    subprocess.run(cmd, check=True)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
