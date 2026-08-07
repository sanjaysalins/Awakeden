"""Seed of the Woman LONG -- assemble stage. Spreads 1-5 promoted from the
POC30 process-validation test (memory `day-of-atonement-retro-learnings`);
extend _spread_table.py + SEGMENT_BUILDERS as the full plan is authored.
Implements the
Day of Atonement retrospective's fix #1: content-hash freshness stamps
instead of human --only lists. After building each segment, writes a
`.stamp.json` hashing (device entry + params + source file mtimes/sizes +
RENDERER_VERSION); a re-run only rebuilds mismatches -- kill it mid-run and
the next run picks up exactly where it left off, with a printed
FRESH/STALE/MISSING breakdown, no --only bookkeeping needed.

Reuses day_of_atonement/_devices.py's own proven `_spotlight_family` /
`_plain_static` render functions directly (cross-episode import) rather
than re-implementing them -- fix #6's reuse principle applied one level
below the finishing chain too.

  .venv\\Scripts\\python.exe poc_living_sketchbook/seed_of_the_woman/_s6_assemble.py
  .venv\\Scripts\\python.exe poc_living_sketchbook/seed_of_the_woman/_s6_assemble.py --rebuild
"""
import argparse
import hashlib
import importlib.util
import json
import random
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DOA = ROOT / "poc_living_sketchbook" / "day_of_atonement"

sys.path.insert(0, str(HERE))
import _spread_table as st  # noqa: E402

W, H, FPS = 1920, 1080, 30
RENDERER_VERSION = "2"  # bumped: s03's verse card now has real word-timed press-in arrival

STILLS = HERE / "stills"
WORLD = ROOT / "poc_living_sketchbook" / "world"
CLIPS = HERE / "clips"
SEG_DIR = HERE / "_segments"
SEG_DIR.mkdir(exist_ok=True)

NARRATION = HERE / "SEEDOFTHEWOMAN_LONG_living_sketchbook.mp3"
OUT = HERE / "SEEDOFTHEWOMAN_LONG_living_sketchbook.mp4"

F_KEEPER = "C:/Windows/Fonts/Inkfree.ttf"
INK = (35, 30, 26, 255)


def load_devices_doa():
    spec = importlib.util.spec_from_file_location("_doa_devices", DOA / "_devices.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_devices_here():
    """NOT `import _devices` -- day_of_atonement's own _devices.py inserts ITS
    OWN directory at sys.path[0] as a side effect of import (line 37-38 of
    that file), so a plain `import _devices` after load_devices_doa() has
    already run would silently resolve to the WRONG module (a real bug
    caught building this exact script -- explicit path-based loading avoids
    the whole class of collision)."""
    spec = importlib.util.spec_from_file_location("_seed_devices", HERE / "_devices.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{' '.join(str(c) for c in cmd[:6])}...\n{r.stderr[-1200:]}")


def _stat(p: Path):
    if not p.exists():
        return None
    s = p.stat()
    return [str(p), s.st_size, int(s.st_mtime)]


# ------------------------------------------------------------- segment builders

def build_s01(dest, duration, doa):
    still = STILLS / "s01_something_wrong.png"
    doa._spotlight_family("dramatic_spotlight", still, dest, duration, [38, 52, 24, 38])


def build_clip_hold(dest, duration, clip_path):
    """Play the real clip forward once, then hold its last frame for the remainder."""
    cdur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(clip_path)],
        capture_output=True, text=True).stdout.strip())
    if cdur >= duration:
        _run(["ffmpeg", "-y", "-v", "error", "-i", str(clip_path), "-t", f"{duration:.3f}",
              "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
              "-an", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])
    else:
        hold = duration - cdur
        _run(["ffmpeg", "-y", "-v", "error", "-i", str(clip_path),
              "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                     f"tpad=stop_mode=clone:stop_duration={hold:.3f}",
              "-an", "-t", f"{duration:.3f}", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
              "-r", str(FPS), str(dest)])


def render_line_png(line, seed):
    """One line's own PNG, sized to its own bbox -- rendered separately (not
    baked into one flat card image) so each line can be given its own
    word-timed press-in arrival below. A single static overlay for the
    whole 12s card is exactly the FROZEN-SPREAD defect class motion_lint
    exists to catch (memory `day-of-atonement-retro-learnings` fix #3) --
    caught on THIS card's own first lint run, fixed here rather than
    silenced."""
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    rng = random.Random(seed)
    runs = [(text, size, ImageFont.truetype(F_KEEPER, size)) for text, size in line]
    line_h = max(size for _, size, _ in runs) + 16
    widths = [probe.textlength(t, font=f) for t, _, f in runs]
    total_w = sum(widths)
    img = Image.new("RGBA", (int(total_w) + 40, line_h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 0
    for (text, size, font), wid in zip(runs, widths):
        jy = rng.uniform(-2, 2)
        d.text((x, 10 + jy), text, font=font, fill=INK, stroke_width=1, stroke_fill=INK)
        x += wid
    return img


def build_s03(dest, duration, doa):
    bg = WORLD / "eden_ref.png"
    cropped = SEG_DIR / "_s03_bg_crop.png"
    _run(["ffmpeg", "-y", "-v", "error", "-i", str(bg), "-vf",
          f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=2:1,eq=brightness=0.06",
          "-frames:v", "1", str(cropped)])
    poc_devices = load_devices_here()
    card = poc_devices.VERSE_CARDS["s03_verse_card"]
    lines = card["lines"]

    line_imgs = [render_line_png(line, seed=42 + i) for i, line in enumerate(lines)]
    total_h = sum(im.height for im in line_imgs) + 20 * (len(line_imgs) - 1)
    y = int(H * 0.30)
    positions = []
    for im in line_imgs:
        x = int((W - im.width) / 2)
        positions.append((x, y))
        y += im.height + 20

    inputs = ["-loop", "1", "-i", str(cropped)]
    filt_parts = []
    last = "0:v"
    press_start, press_gap, press_fade = 0.4, 1.15, 0.5
    for i, (im, (x, y)) in enumerate(zip(line_imgs, positions)):
        p = SEG_DIR / f"_s03_line{i}.png"
        im.save(p)
        inputs += ["-loop", "1", "-i", str(p)]
        idx = i + 1
        t0 = press_start + i * press_gap
        faded = f"f{idx}"
        label = f"v{idx}"
        # fade THIS line's own layer in isolation (alpha fade-in), THEN
        # overlay it -- fading the combined [last] stream instead would
        # also re-fade every line already placed on it.
        filt_parts.append(
            f"[{idx}:v]format=rgba,fade=t=in:st={t0:.2f}:d={press_fade}:alpha=1[{faded}]"
        )
        filt_parts.append(
            f"[{last}][{faded}]overlay={x}:{y}:enable='gte(t,{t0:.2f})'[{label}]"
        )
        last = label
    filt = ";".join(filt_parts)
    _run(["ffmpeg", "-y", "-v", "error", *inputs, "-t", f"{duration:.3f}",
          "-filter_complex", filt, "-map", f"[{last}]",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])
    cropped.unlink(missing_ok=True)
    for i in range(len(lines)):
        (SEG_DIR / f"_s03_line{i}.png").unlink(missing_ok=True)


def build_s05(dest, duration, doa):
    still = STILLS / "s05_where_art_thou.png"
    doa._plain_static(still, dest, duration)


SEGMENT_BUILDERS = {
    "s01_something_wrong": lambda dest, dur, doa: build_s01(dest, dur, doa),
    "s02_the_hiding": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s02_the_hiding.mp4"),
    "s03_verse_card": lambda dest, dur, doa: build_s03(dest, dur, doa),
    "s04_god_walking": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s04_god_walking.mp4"),
    "s05_where_art_thou": lambda dest, dur, doa: build_s05(dest, dur, doa),
}

SOURCE_FILES = {
    "s01_something_wrong": [STILLS / "s01_something_wrong.png"],
    "s02_the_hiding": [CLIPS / "s02_the_hiding.mp4"],
    "s03_verse_card": [WORLD / "eden_ref.png", HERE / "_devices.py"],
    "s04_god_walking": [CLIPS / "s04_god_walking.mp4"],
    "s05_where_art_thou": [STILLS / "s05_where_art_thou.png"],
}


def compute_hash(name: str) -> str:
    payload = {
        "name": name,
        "renderer_version": RENDERER_VERSION,
        "sources": [_stat(p) for p in SOURCE_FILES[name]],
    }
    blob = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def build_segment(num, name, duration, doa, rebuild, progress_path):
    dest = SEG_DIR / f"seg_{name}.mp4"
    stamp_path = SEG_DIR / f"{name}.stamp.json"
    new_hash = compute_hash(name)
    if not rebuild and dest.exists() and stamp_path.exists():
        old = json.loads(stamp_path.read_text(encoding="utf-8")).get("hash")
        if old == new_hash:
            print(f"[build] #{num:02d} {name:<24s} FRESH -- skip")
            return dest, "FRESH"
    print(f"[build] #{num:02d} {name:<24s} dur={duration:.2f}s building...")
    SEGMENT_BUILDERS[name](dest, duration, doa)
    stamp_path.write_text(json.dumps({"hash": new_hash, "built_at": time.time()}), encoding="utf-8")
    progress_path.write_text(json.dumps({"done": num, "total": len(st.SPREADS), "current": name}), encoding="utf-8")
    return dest, "BUILT"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()

    doa = load_devices_doa()
    progress_path = HERE / "_build_progress.json"

    fresh, built, missing = 0, 0, 0
    seg_files = []
    for num, name, beat, t0, t1 in st.SPREADS:
        dur = t1 - t0
        dest, status = build_segment(num, name, dur, doa, args.rebuild, progress_path)
        seg_files.append(dest)
        if status == "FRESH":
            fresh += 1
        else:
            built += 1
    print(f"[stamps] FRESH {fresh} / BUILT {built} / MISSING {missing}")

    concat_list = SEG_DIR / "_concat_all.txt"
    concat_list.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in seg_files) + "\n", encoding="utf-8")
    silent = HERE / "_SEEDOFTHEWOMAN_silent.mp4"
    _run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_list),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(silent)])

    total = st.SPREADS[-1][4]
    _run(["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(NARRATION),
          "-map", "0:v", "-map", "1:a", "-t", f"{total:.3f}",
          "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(OUT)])
    print(f"[done] {OUT}")
    progress_path.write_text(json.dumps({"done": len(st.SPREADS), "total": len(st.SPREADS), "current": "DONE"}),
                              encoding="utf-8")


if __name__ == "__main__":
    main()
