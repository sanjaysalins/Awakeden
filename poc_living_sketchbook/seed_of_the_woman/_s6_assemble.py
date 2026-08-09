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
import math
import random
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
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

ALIGNMENT = json.loads((HERE / "_alignment.json").read_text(encoding="utf-8"))

NARRATION = ROOT / "longform" / "05_The_Seed_Of_The_Woman" / "v1" / "narration.mp3"
OUT = HERE / "SEEDOFTHEWOMAN_LONG_living_sketchbook.mp4"

F_KEEPER = "C:/Windows/Fonts/Inkfree.ttf"
INK = (35, 30, 26, 255)
RUBRIC = (150, 26, 22, 255)  # matches panel_animator's own RUBRIC (annotators_circle.py etc.)
GOLD = (185, 146, 74)        # matches panel_animator's own GOLD / thread_device.GOLD
BODY_SIZE = 40               # matches _devices.py's own BODY_SIZE


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
    """hunt_and_lock ($0 real camera push) toward Adam and Eve -- HERO-
    STILLS CINEMATIC PASS (2026-08-09): the still was redesigned (steep
    high-angle framing, off-center couple, foreground bough) but the OLD
    animation was dramatic_spotlight alone -- a light-dim/re-brighten
    pulse with the couple pixel-identical start to end, zero real camera
    motion on the film's own cold-open hook shot. Target measured via
    panel_animator/bbox_sheet.py's grid overlay against the new render
    (couple sit at roughly 63%,58% of frame), not eyeballed. Same proven
    device as s16/s28/s33/s41; scarlet lock-marker skipped -- this is a
    quiet dread beat, not a "found it" reveal."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import hunt_and_lock  # noqa: E402
    still = STILLS / "s01_something_wrong.png"
    src = Image.open(still).convert("RGB")
    big = hunt_and_lock.scale_crop(src, int(W * hunt_and_lock.UPSCALE), int(H * hunt_and_lock.UPSCALE))
    bw, bh = big.size
    target_frac = (0.64, 0.60)
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        x0, y0, vw, vh, _lock_prog, _wxy = hunt_and_lock.hunt_window(bw, bh, t, duration, target_frac, W, H)
        frame = big.crop((x0, y0, x0 + vw, y0 + vh)).resize((W, H), Image.LANCZOS)
        frame.save(frames / f"f{i:05d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


def build_clip_hold(dest, duration, clip_path, play_dur=None):
    """Play the real clip forward once, then hold the last played frame for
    the remainder. `play_dur` optionally caps how much of the raw clip
    plays before the hold begins -- useful when the clip's own final frame
    (e.g. the tightest zoom of a paid provider's push-in) crops something
    important off-screen or loses the paper deckle-edge border; capping
    playback slightly earlier lands the freeze-hold on a better-framed
    moment instead (HERO-STILLS CINEMATIC PASS, 2026-08-09: s44's raw
    6.04s clip's own last frame crops the serpent's tail off-screen)."""
    cdur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(clip_path)],
        capture_output=True, text=True).stdout.strip())
    play = min(cdur, play_dur) if play_dur is not None else cdur
    if play >= duration:
        _run(["ffmpeg", "-y", "-v", "error", "-i", str(clip_path), "-t", f"{duration:.3f}",
              "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
              "-an", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])
    else:
        hold = duration - play
        _run(["ffmpeg", "-y", "-v", "error", "-i", str(clip_path), "-t", f"{play:.3f}",
              "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                     f"tpad=stop_mode=clone:stop_duration={hold:.3f}",
              "-an", "-t", f"{duration:.3f}", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
              "-r", str(FPS), str(dest)])


def render_line_png(line, seed, ink=None):
    """One line's own PNG, sized to its own bbox -- rendered separately (not
    baked into one flat card image) so each line can be given its own
    word-timed press-in arrival below. A single static overlay for the
    whole 12s card is exactly the FROZEN-SPREAD defect class motion_lint
    exists to catch (memory `day-of-atonement-retro-learnings` fix #3) --
    caught on THIS card's own first lint run, fixed here rather than
    silenced. `ink` overrides the default ink color (e.g. RUBRIC red-letter
    for direct LORD/Christ speech, per this project's locked
    "red-letter speaker = the speaker" rule)."""
    ink = ink or INK
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
        d.text((x, 10 + jy), text, font=font, fill=ink, stroke_width=1, stroke_fill=ink)
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


def build_s16(dest, duration, doa):
    """hunt_and_lock (panel_animator/hunt_and_lock.py) -- the drift-hunt-lock
    camera move, target_frac read from _devices.py's own DEVICE_ASSIGNMENTS
    so the bbox picked via bbox_sheet.py stays the single source of truth."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import hunt_and_lock  # noqa: E402
    still = STILLS / "s16_sentencing_tableau.png"
    poc_devices = load_devices_here()
    entry = poc_devices.DEVICE_ASSIGNMENTS["s16_watch_closely"]
    target_frac = tuple(entry["params"]["target_frac"])
    hunt_and_lock.render(still, dest, duration, target_frac, W, H)


def build_s07(dest, duration, doa):
    """Scribed Ink composite, $0 -- reuses s06's OWN already-rendered still
    (Eve's turned profile + serpent, cropped tight on her + the serpent's
    shadow at the bottom edge), not a new render. Fast press-in (39 glyphs
    over this spread's ~3.5s window)."""
    bg = STILLS / "s06_blame_circle.png"
    cropped = SEG_DIR / "_s07_bg_crop.png"
    _run(["ffmpeg", "-y", "-v", "error", "-i", str(bg), "-vf",
          f"crop=iw*0.50:ih*0.90:iw*0.48:ih*0.05,"
          f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"boxblur=1:1,eq=brightness=0.03", "-frames:v", "1", str(cropped)])
    poc_devices = load_devices_here()
    card = poc_devices.VERSE_CARDS["s07_beguiled_card"]
    lines = card["lines"]

    line_imgs = [render_line_png(line, seed=142 + i) for i, line in enumerate(lines)]
    y = int(H * 0.10)
    positions = []
    for im in line_imgs:
        x = int((W - im.width) / 2)
        positions.append((x, y))
        y += im.height + 16

    inputs = ["-loop", "1", "-i", str(cropped)]
    filt_parts = []
    last = "0:v"
    press_start, press_gap, press_fade = 0.2, 0.5, 0.3
    for i, (im, (x, y)) in enumerate(zip(line_imgs, positions)):
        p = SEG_DIR / f"_s07_line{i}.png"
        im.save(p)
        inputs += ["-loop", "1", "-i", str(p)]
        idx = i + 1
        t0 = press_start + i * press_gap
        faded, label = f"f{idx}", f"v{idx}"
        filt_parts.append(f"[{idx}:v]format=rgba,fade=t=in:st={t0:.2f}:d={press_fade}:alpha=1[{faded}]")
        filt_parts.append(f"[{last}][{faded}]overlay=0+{x}:0+{y}:enable='gte(t,{t0:.2f})'[{label}]")
        last = label
    filt = ";".join(filt_parts)
    _run(["ffmpeg", "-y", "-v", "error", *inputs, "-t", f"{duration:.3f}",
          "-filter_complex", filt, "-map", f"[{last}]",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])
    cropped.unlink(missing_ok=True)
    for i in range(len(lines)):
        (SEG_DIR / f"_s07_line{i}.png").unlink(missing_ok=True)


def build_s09(dest, duration, doa):
    """candle_only ($0) -- a gentle breathing pulse (flat base radius +
    flicker noise, NOT the shrinking 'fear closes it down' curve day_of_
    atonement's s43 uses) centered on the gold fleck's own real pixel
    position, picked via bbox_sheet.py against the actual rendered still."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import candle_only  # noqa: E402
    still = STILLS / "s09_unexpected_place.png"
    poc_devices = load_devices_here()
    anchor_frac = poc_devices.DEVICE_ASSIGNMENTS["s09_unexpected_place"]["params"]["anchor_frac"]
    ax, ay = anchor_frac[0] * W, anchor_frac[1] * H
    src = Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS)
    base_curve = lambda t: 45.0  # noqa: E731 -- flat: breathing comes from flicker_R's noise, not a trend
    R_of_t = candle_only.flicker_R(base_curve, seed=90, amplitude=8.0)
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        frame = candle_only.apply_candle(src, i / FPS, (ax, ay), R_of_t)
        frame.save(frames / f"f{i:04d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%04d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


def build_s13(dest, duration, doa):
    still = STILLS / "s13_the_fruit.png"
    poc_devices = load_devices_here()
    bbox = poc_devices.DEVICE_ASSIGNMENTS["s13_the_fruit"]["params"]["bbox"]
    doa._spotlight_family("dramatic_spotlight", still, dest, duration, bbox)


def build_s14(dest, duration, doa):
    """wash-creep ADVANCE ($0) -- REDESIGNED 2026-08-08: motion_lint caught
    the first version (raw eden_ref.png reuse) as FROZEN-SPREAD, p95=0.000
    -- eden_ref.png has no real blue-grey wash region for isolate_storm_
    wash()'s HSV band to find, so nothing ever advanced. Now uses a
    DEDICATED still (stills/s14_death_enters.png) that actually has the
    ink-blue wash bled in at the edges, matching Storm's own s01/s04
    pattern (the wash must be real content in the still, not synthesized
    by this device)."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import wash_creep  # noqa: E402
    base = wash_creep.scale_crop(Image.open(STILLS / "s14_death_enters.png").convert("RGB"), W, H)
    mask = wash_creep.isolate_storm_wash(base)
    n = max(1, int(round(duration * wash_creep.FPS)))
    # NOT wash_creep._build_frame_plan (module default ADVANCE_MAX=15px over
    # the FULL clip regardless of duration -- calibrated for Storm's own
    # shorter spreads, too slow-moving to clear motion_lint's threshold on
    # this spread's 5.9s window, real p95=0.090 < 0.15). Own plan, same
    # monotonic ease-in advance shape, more total travel (34px) for a
    # longer spread -- still pure ADVANCE, no backrun/retreat (reserved
    # for s52's payoff per _PLAN.md).
    ADVANCE_MAX_LOCAL = 34.0
    plan = [(wash_creep._ease(i / max(1, n - 1)) * ADVANCE_MAX_LOCAL, False) for i in range(n)]
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i, (advance_px, backrun) in enumerate(plan):
        frame = wash_creep.apply_wash_creep(base, advance_px, mask=mask, backrun=backrun)
        frame.save(frames / f"f{i:05d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(wash_creep.FPS),
          "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


def build_s15(dest, duration, doa):
    """parallax_25d ($0) -- rembg extracts Adam+Eve (the near rim) as the
    foreground depth layer against the far-garden base plate."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import parallax_25d  # noqa: E402
    still = STILLS / "s15_the_breach.png"
    poc_devices = load_devices_here()
    params = poc_devices.DEVICE_ASSIGNMENTS["s15_the_breach"]["params"]
    raw = dest.parent / (dest.stem + "_raw.mp4")
    parallax_25d.render(still, raw, duration, params["fg_amp"], params["bg_amp"])
    _run(["ffmpeg", "-y", "-v", "error", "-i", str(raw),
          "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])
    raw.unlink(missing_ok=True)


def build_s19(dest, duration, doa):
    """Scribed Ink composite, $0 -- reuses s18's OWN already-rendered still
    (the serpent alone, high angle) as the card background, per _PLAN.md's
    device column. Same press-in pattern as build_s07."""
    bg = STILLS / "s18_turns_to_serpent.png"
    cropped = SEG_DIR / "_s19_bg_crop.png"
    _run(["ffmpeg", "-y", "-v", "error", "-i", str(bg), "-vf",
          f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"boxblur=1:1,eq=brightness=0.03", "-frames:v", "1", str(cropped)])
    poc_devices = load_devices_here()
    card = poc_devices.VERSE_CARDS["s19_curse_card"]
    lines = card["lines"]

    line_imgs = [render_line_png(line, seed=219 + i) for i, line in enumerate(lines)]
    y = int(H * 0.10)
    positions = []
    for im in line_imgs:
        x = int((W - im.width) / 2)
        positions.append((x, y))
        y += im.height + 16

    inputs = ["-loop", "1", "-i", str(cropped)]
    filt_parts = []
    last = "0:v"
    press_start, press_gap, press_fade = 0.4, 0.9, 0.4
    for i, (im, (x, y)) in enumerate(zip(line_imgs, positions)):
        p = SEG_DIR / f"_s19_line{i}.png"
        im.save(p)
        inputs += ["-loop", "1", "-i", str(p)]
        idx = i + 1
        t0 = press_start + i * press_gap
        faded, label = f"f{idx}", f"v{idx}"
        filt_parts.append(f"[{idx}:v]format=rgba,fade=t=in:st={t0:.2f}:d={press_fade}:alpha=1[{faded}]")
        filt_parts.append(f"[{last}][{faded}]overlay=0+{x}:0+{y}:enable='gte(t,{t0:.2f})'[{label}]")
        last = label
    filt = ";".join(filt_parts)
    _run(["ffmpeg", "-y", "-v", "error", *inputs, "-t", f"{duration:.3f}",
          "-filter_complex", filt, "-map", f"[{last}]",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])
    cropped.unlink(missing_ok=True)
    for i in range(len(lines)):
        (SEG_DIR / f"_s19_line{i}.png").unlink(missing_ok=True)


def _s21_composed_base():
    """s20's own extreme-close-up art + the gold thread drawn across it at
    FULL opacity -- the one shared background s21/s22 both build from
    (s22's own _PREFLIGHT.md description: 'the curse-dark page with the
    gold thread behind'). Cached to a file so callers don't re-render it."""
    cache = SEG_DIR / "_s21_base.png"
    if cache.exists():
        return cache
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import thread_device  # noqa: E402
    poc_devices = load_devices_here()
    params = poc_devices.DEVICE_ASSIGNMENTS["s21_gold_woven_in"]["params"]
    base = Image.open(STILLS / "s20_pure_curse.png").convert("RGB").resize((W, H), Image.LANCZOS)
    thread = thread_device.make_thread_layer(W, H, params["p0_frac"], params["p1_frac"], thread_device.GOLD,
                                              width=params.get("width", 4))
    out = base.convert("RGBA")
    out.alpha_composite(thread)
    out.convert("RGB").save(cache)
    return cache


def build_s21(dest, duration, doa):
    """thread_device ($0) -- the gold thread's FIRST appearance, drawn over
    s20's own already-approved extreme-close-up art (not a new render, see
    _s2_stills.py's note). Fade-in + one luminance swell."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import thread_device  # noqa: E402
    poc_devices = load_devices_here()
    params = poc_devices.DEVICE_ASSIGNMENTS["s21_gold_woven_in"]["params"]
    base = Image.open(STILLS / "s20_pure_curse.png").convert("RGB").resize((W, H), Image.LANCZOS)
    thread = thread_device.make_thread_layer(W, H, params["p0_frac"], params["p1_frac"], thread_device.GOLD,
                                              width=params.get("width", 4))
    thread_bright = thread_device.make_thread_layer(W, H, params["p0_frac"], params["p1_frac"],
                                                      thread_device.GOLD_BRIGHT, width=params.get("width", 4))
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        op = thread_device.thread_opacity(t, params["fade_start"], params["fade_dur"])
        swell = thread_device.thread_swell(t, params["swell_time"])
        frame = base.convert("RGBA")
        if op > 0:
            layer = Image.blend(thread.convert("RGB"), thread_bright.convert("RGB"), swell).convert("RGBA")
            layer.putalpha(thread.split()[3].point(lambda v: int(v * op)))
            frame.alpha_composite(layer)
        frame.convert("RGB").save(frames / f"f{i:04d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%04d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


def build_s22(dest, duration, doa):
    """Illuminated Rubric, $0 -- LOCAL adaptation of day_of_atonement's own
    s16/s52 device (NOT cross-imported: that function reads day_of_
    atonement's own ALIGNMENT/LAST_WORD_END module globals directly, which
    would silently apply the WRONG episode's narration timing to this
    episode's card). Reuses the same real building blocks (thread_device
    for the background, held_breath.energy_envelope for the breathing
    glow) with THIS episode's own alignment. LAW 1: the verse arrives as
    ONE whole block, never word-by-word. Gen 3:15 is direct LORD speech
    (narration.md: "Multi-voice: the_LORD voices Gen 3:14-15") -> red-letter."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    from held_breath import energy_envelope  # noqa: E402
    base_path = _s21_composed_base()
    base = Image.open(base_path).convert("RGB")
    energy = energy_envelope(ALIGNMENT, st.LAST_WORD_END_ESTIMATE, floor=0.25, ramp=0.15)
    abs_start = st.by_name["s22_promise_card"][2]

    lines = [
        [("And I will put enmity between thee and the woman,", BODY_SIZE)],
        [("and between thy seed and her seed;", BODY_SIZE)],
        [("it shall bruise thy head,", BODY_SIZE)],
        [("and thou shalt bruise his heel.", BODY_SIZE)],
    ]
    line_imgs = [render_line_png(line, seed=522 + i, ink=RUBRIC) for i, line in enumerate(lines)]
    block_x, y = int(W * 0.08), int(H * 0.14)
    positions = []
    for im in line_imgs:
        positions.append((block_x, y))
        y += im.height + 18
    cap_cx, cap_cy = block_x + 30, positions[0][1] + line_imgs[0].height // 2
    gold_ellipse = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gold_ellipse).ellipse(
        [cap_cx - 70, cap_cy - 60, cap_cx + 70, cap_cy + 60], fill=(*GOLD, 130))

    n = max(1, int(round(duration * FPS)))
    press_t = 1.2
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        e = energy(abs_start + t)
        gain = 1.0 + 0.08 * e * (0.5 + 0.5 * math.sin(2 * math.pi * (t % 4.0) / 4.0))
        arr = (np.asarray(base, dtype=np.float32) * gain).clip(0, 255).astype(np.uint8)
        frame = Image.fromarray(arr).convert("RGBA")
        if t >= press_t:
            frame.alpha_composite(gold_ellipse)
            for im, (x, y) in zip(line_imgs, positions):
                frame.alpha_composite(im, (x, y))
        frame.convert("RGB").save(frames / f"f{i:04d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%04d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


def build_s23(dest, duration, doa):
    """$0 hold: s22's own last frame, held, + line_boil grain wobble
    (panel_animator/line_boil.py) so 'sacred stillness -- nothing moves but
    the grain' reads as genuinely alive on motion_lint, not frozen."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import line_boil  # noqa: E402
    s22_seg = SEG_DIR / "seg_s22_promise_card.mp4"
    if not s22_seg.exists():
        raise SystemExit("build_s23 needs s22_promise_card built first")
    held = dest.parent / (dest.stem + "_held.mp4")
    last_png = dest.parent / (dest.stem + "_last.png")
    _run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.1", "-i", str(s22_seg),
          "-frames:v", "1", str(last_png)])
    _run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(last_png), "-t", f"{duration:.3f}",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(held)])
    poc_devices = load_devices_here()
    amount = poc_devices.DEVICE_ASSIGNMENTS["s23_let_that_land"]["params"]["amount"]
    line_boil.render(held, dest, amount)
    held.unlink(missing_ok=True)
    last_png.unlink(missing_ok=True)


def build_s25(dest, duration, doa):
    """thread_device gleam-pass ($0) -- the thread already drawn across
    s25's own art (no fade-in, per _PLAN.md's device column), just the
    luminance swell as it 'rises past the top edge'."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import thread_device  # noqa: E402
    poc_devices = load_devices_here()
    params = poc_devices.DEVICE_ASSIGNMENTS["s25_promise_in_curse"]["params"]
    base = Image.open(STILLS / "s25_promise_in_curse.png").convert("RGB").resize((W, H), Image.LANCZOS)
    thread = thread_device.make_thread_layer(W, H, params["p0_frac"], params["p1_frac"], thread_device.GOLD,
                                              width=params.get("width", 4))
    thread_bright = thread_device.make_thread_layer(W, H, params["p0_frac"], params["p1_frac"],
                                                      thread_device.GOLD_BRIGHT, width=params.get("width", 4))
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        swell = thread_device.thread_swell(t, params["swell_time"])
        layer = Image.blend(thread.convert("RGB"), thread_bright.convert("RGB"), swell).convert("RGBA")
        layer.putalpha(thread.split()[3])
        frame = base.convert("RGBA")
        frame.alpha_composite(layer)
        frame.convert("RGB").save(frames / f"f{i:04d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%04d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


# ---- the study copy: Gen 3:15 in the Keeper's own hand, ONE fixed
# letterform anchor (seed+params) reused identically at every future
# appearance (s26/40/46/47/60/66 per _PREFLIGHT.md's asset table) -- the
# independent-review panel flagged an unanchored re-dress as "the same
# failure class as face drift" for doctrinally load-bearing text
# ("it shall bruise thy head," never "he"); this constant IS the anchor.
STUDY_COPY_SEED = 2615
# STYLING FIX ROUND 4 2026-08-08 (user): "still don't like it... more
# larger and perhaps be done in the way we did in the later part of the
# clip." Round 3's fix (SIZE=12, centered on the tiny blank-page prop)
# was gate-clean but read as cramped -- the "later part" cards (s29,
# s32, s34/35) are all big, LEFT-FLUSH dark-ink hand-lettering sitting
# confidently across the real desk art, never confined to one small
# prop. Matched that register directly: SIZE now equals BODY_SIZE (the
# same size the plate cards use), left-aligned from a fixed block
# position instead of centered-in-a-rect.
STUDY_COPY_SIZE = BODY_SIZE
STUDY_COPY_LINES = [
    "And I will put enmity between thee and the woman,",
    "and between thy seed and her seed;",
    "it shall bruise thy head,",
    "and thou shalt bruise his heel.",
]
# left-flush block position: the real open-desk band in this still,
# measured directly -- clear of the corner clutter-photos and the lit
# oil lamp (top-right); widest line (892px at SIZE=40) ends at x=1392,
# short of the far-right clutter.
STUDY_COPY_BLOCK_X = 500
STUDY_COPY_BLOCK_Y0 = 460


def _study_copy_layout():
    """Returns (line_imgs, positions, her_seed_bbox) -- pure geometry, no
    file I/O, so build_s26 and any future re-dress can both call this and
    get byte-identical placement."""
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    font = ImageFont.truetype(F_KEEPER, STUDY_COPY_SIZE)
    line_h = STUDY_COPY_SIZE + 16
    gap = 18
    x0, y = STUDY_COPY_BLOCK_X, STUDY_COPY_BLOCK_Y0
    line_imgs, positions = [], []
    for i, text in enumerate(STUDY_COPY_LINES):
        im = render_line_png([(text, STUDY_COPY_SIZE)], seed=STUDY_COPY_SEED + i, ink=RUBRIC)
        line_imgs.append(im)
        positions.append((x0, y))
        y += line_h + gap
    # "her seed" lives in line index 1
    prefix_w = probe.textlength("and between thy seed and ", font=font)
    word_w = probe.textlength("her seed", font=font)
    lx, ly = positions[1]
    her_seed_bbox = (int(lx + prefix_w), int(ly), int(lx + prefix_w + word_w), int(ly + line_h))
    return line_imgs, positions, her_seed_bbox


def build_s26(dest, duration, doa):
    """The study copy + the episode's ONE Annotator's Circle ($0). The
    text is a static prop ("already written", per _PLAN.md -- not a live
    scribing, so no per-line press-in); only the circle animates, landing
    on "her seed" at its real spoken moment (162.105s, from _alignment.
    json -- verified, not guessed)."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import annotators_circle  # noqa: E402
    still = STILLS / "s26_her_seed_study.png"
    base = Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA")
    line_imgs, positions, her_seed_bbox = _study_copy_layout()
    for im, (x, y) in zip(line_imgs, positions):
        base.alpha_composite(im, (int(x), int(y)))

    abs_start = st.by_name["s26_her_seed_study"][2]
    circle_start = 162.105 - abs_start
    # Round 4 (user): after STUDY_COPY_SIZE grew to match the "later
    # part" register (see above), re-tuned the circle against the much
    # bigger "her seed" bbox via the same local simulator -- pad_x=0.55,
    # pad_y=1.5, stroke=20 lands at p95=0.164 (clears T_frozen=0.15 with
    # margin) and reads as a proportionate ring, not a blob, against the
    # bigger text.
    circle_dur = 1.0
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        progress = max(0.0, min(1.0, (t - circle_start) / circle_dur))
        frame = annotators_circle.apply_annotators_circle(
            base.copy(), bbox=her_seed_bbox, progress=progress, color=annotators_circle.RUBRIC,
            pad_x_frac=0.55, pad_y_frac=1.5, stroke_width=20)
        frame.convert("RGB").save(frames / f"f{i:05d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


def build_s27(dest, duration, doa):
    """The descent-line is already drawn INTO the still's own art (the
    rendered image already shows the hand-drawn line linking the father-
    figures -- see _s2_stills.py's prompt note); this device stays a
    plain held frame + line_boil grain wobble so "quick graphite marks"
    reads as hand-inked-alive rather than a locked digital still, same
    pattern as build_s23's card hold."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import line_boil  # noqa: E402
    still = STILLS / "s27_line_of_fathers.png"
    held = dest.parent / (dest.stem + "_held.mp4")
    _run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(still), "-t", f"{duration:.3f}",
          "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(held)])
    line_boil.render(held, dest, 0.5)
    held.unlink(missing_ok=True)



def build_s30(dest, duration, doa):
    """hunt_and_lock ($0 real camera push), replacing the raw Kling clip --
    same fix as s28/s33 (batch 4 review: paid render had near-zero real
    motion, confirmed by eye-checking 2s-apart frames). FIRST tried
    parallax_25d (Mary as the near foreground layer) -- twice: default
    tuned amplitude (24.0/9.0, s15_the_breach's own values) landed at
    p95=0.131, and widening further (36.0/14.0) actually landed LOWER
    (0.125), just under motion_lint's T_frozen=0.15 either way. That
    non-monotonic response means rembg's segmentation isn't finding a
    clean, stable foreground cutout on this still (warm robe against a
    similarly warm/pale background) -- more amplitude on a bad mask
    doesn't reliably mean more visible motion. Switched to hunt_and_lock,
    which doesn't depend on segmentation at all. FIRST target was the
    descending light's own brightest pixel (1361,80) -- rejected after an
    eye-check: that whole region is a large blown-out glow with no
    surrounding detail, so the lock phase's 2.4x zoom landed on a
    near-blank void. Retargeted to Mary's own clasped hands (1393,1135 in
    the still's 2752x1536 space -> 0.506, 0.739) -- real fabric/finger
    detail survives the full push, and it's a stronger devotional beat
    besides (her own answer forming)."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import hunt_and_lock  # noqa: E402
    still = STILLS / "s30_annunciation.png"
    hunt_and_lock.render(still, dest, duration, (0.506, 0.739), W, H)


def build_s33(dest, duration, doa):
    """hunt_and_lock ($0 real camera push), replacing the raw Seedance clip
    -- same fix as s28. target_frac reuses the SAME measured brightest-
    pixel this episode already found for this exact still (1866,543 in
    1920x1080 -- see naming_plate.html's origin-point comment), so the
    camera now physically arrives right where s34/s35's plate animation
    begins -- s33 and the naming plate read as one continuous move rather
    than two unrelated shots."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import hunt_and_lock  # noqa: E402
    still = STILLS / "s33_trajectory.png"
    hunt_and_lock.render(still, dest, duration, (1866 / 1920, 543 / 1080), W, H)


def build_s29(dest, duration, doa):
    """Illuminated Rubric, $0 -- formal peak 2/2 (Gal 4:4, "the promise
    KEPT"). LOCAL adaptation of build_s22's same technique (own alignment,
    not day_of_atonement's), first-warm-palette page. NOT red-letter --
    Gal 4:4 is Paul writing ABOUT the LORD, not the LORD's own first-
    person speech (per [[redletter-speaker-is-speaker]], contrast s22)."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    from held_breath import energy_envelope  # noqa: E402
    # BACKGROUND FIX 2026-08-08 (user, batch 4 review round 2): this was a
    # flat procedural gradient, not a real still -- missed in the first
    # pass because it isn't one of the "remotion" render_dom_clip.py
    # plates, but the complaint is identical (user: "why is s29 still on
    # blank background... always overlay on an existing still"). Its own
    # old comment claimed to follow "build_s22... a standalone card like
    # s22" -- but s22 actually uses a REAL composed still
    # (_s21_composed_base()), so this had already diverged from its own
    # stated precedent. Now uses s27's own line-of-fathers art: Gal 4:4's
    # "fulness of the time" IS the whole genealogical line arriving, and
    # the walking-figures band sits low enough that this text block
    # (upper-left, unchanged position) never competes with them.
    base = Image.open(STILLS / "s27_line_of_fathers.png").convert("RGB").resize((W, H), Image.LANCZOS)
    energy = energy_envelope(ALIGNMENT, st.LAST_WORD_END_ESTIMATE, floor=0.25, ramp=0.15)
    abs_start = st.by_name["s29_fulness_card"][2]

    lines = [
        [("But when the fulness of the time was come,", BODY_SIZE)],
        [("God sent forth his Son, made of a woman,", BODY_SIZE)],
        [("made under the law.", BODY_SIZE)],
    ]
    line_imgs = [render_line_png(line, seed=629 + i) for i, line in enumerate(lines)]
    block_x, y = int(W * 0.08), int(H * 0.14)
    positions = []
    for im in line_imgs:
        positions.append((block_x, y))
        y += im.height + 18
    cap_cx, cap_cy = block_x + 16, positions[0][1] + line_imgs[0].height // 2
    gold_ellipse = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gold_ellipse).ellipse(
        [cap_cx - 42, cap_cy - 42, cap_cx + 42, cap_cy + 42], fill=(*GOLD, 130))

    n = max(1, int(round(duration * FPS)))
    press_t = 0.8
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        e = energy(abs_start + t)
        # amplitude halved (0.08 -> 0.04) vs the old flat-gradient version --
        # an 8% brightness pulse read as gentle "breathing" on a flat color
        # field but risks looking like flicker on a detailed photo.
        gain = 1.0 + 0.04 * e * (0.5 + 0.5 * math.sin(2 * math.pi * (t % 4.0) / 4.0))
        arr = (np.asarray(base, dtype=np.float32) * gain).clip(0, 255).astype(np.uint8)
        frame = Image.fromarray(arr).convert("RGBA")
        if t >= press_t:
            frame.alpha_composite(gold_ellipse)
            for im, (x, y) in zip(line_imgs, positions):
                frame.alpha_composite(im, (x, y))
        frame.convert("RGB").save(frames / f"f{i:05d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


def build_s28(dest, duration, doa):
    """Eve + the gold thread reaching to the far glow ($0 thread overlay),
    now over a REAL hunt_and_lock camera push toward the light instead of
    a frozen clip -- batch 4 review (user, 2026-08-08): "the animations
    done in kling or veo is very very very basic... the camera is so very
    simple and basic." Eye-checked the raw Seedance clip's frames 2s apart
    and confirmed near pixel-identical -- almost no real generated motion.
    Reuses the SAME camera device already proven on s16, driven straight
    from the still (the target IS the thread's own light endpoint, so the
    camera lands exactly where the thread points). The thread's endpoints
    are re-projected into each frame's moving crop window
    (hunt_and_lock.hunt_window) instead of drawn once in fixed screen
    space, so it keeps tracking Eve and the light as the camera moves.
    hunt_and_lock's own scarlet lock-marker is skipped here -- the gold
    thread already IS this shot's "found it" device; a second marker
    would be redundant."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import hunt_and_lock  # noqa: E402
    import thread_device  # noqa: E402
    still = STILLS / "s28_clue_lights_up.png"
    p0_frac, p1_frac = (0.30, 0.72), (0.641, 0.525)
    src = Image.open(still).convert("RGB")
    big = hunt_and_lock.scale_crop(src, int(W * hunt_and_lock.UPSCALE), int(H * hunt_and_lock.UPSCALE))
    bw, bh = big.size
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        x0, y0, vw, vh, _lock_prog, _wxy = hunt_and_lock.hunt_window(bw, bh, t, duration, p1_frac, W, H)
        frame = big.crop((x0, y0, x0 + vw, y0 + vh)).resize((W, H), Image.LANCZOS).convert("RGBA")
        sx0, sy0 = hunt_and_lock.project_point(p0_frac[0], p0_frac[1], bw, bh, x0, y0, vw, vh, W, H)
        sx1, sy1 = hunt_and_lock.project_point(p1_frac[0], p1_frac[1], bw, bh, x0, y0, vw, vh, W, H)
        thread = thread_device.make_thread_layer(
            W, H, (sx0 / W, sy0 / H), (sx1 / W, sy1 / H), thread_device.GOLD, width=14)
        thread_bright = thread_device.make_thread_layer(
            W, H, (sx0 / W, sy0 / H), (sx1 / W, sy1 / H), thread_device.GOLD_BRIGHT, width=14)
        swell = thread_device.thread_swell(t, 3.0)
        layer = Image.blend(thread.convert("RGB"), thread_bright.convert("RGB"), swell).convert("RGBA")
        layer.putalpha(thread.split()[3])
        frame.alpha_composite(layer)
        frame.convert("RGB").save(frames / f"f{i:05d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


def build_s31(dest, duration, doa):
    """Composite verse-over-art, $0 -- Luke 1:35b letters over s30's OWN
    already-rendered annunciation art (not a new render, same reuse
    pattern as s07-over-s06), positioned in the calm dark field to the
    LEFT of Mary's figure, never over the light or her silhouette (per
    _PREFLIGHT.md's letterer law). NOT red-letter -- this is the angel's
    speech, not the LORD's own first-person voice (contrast s22)."""
    bg = STILLS / "s30_annunciation.png"
    cropped = SEG_DIR / "_s31_bg_crop.png"
    _run(["ffmpeg", "-y", "-v", "error", "-i", str(bg), "-vf",
          f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"boxblur=1:1,eq=brightness=-0.02", "-frames:v", "1", str(cropped)])
    lines = [
        [("that holy thing which shall be born of thee", BODY_SIZE)],
        [("shall be called the Son of God.", BODY_SIZE)],
    ]
    line_imgs = [render_line_png(line, seed=331 + i) for i, line in enumerate(lines)]
    x0 = int(W * 0.07)
    y = int(H * 0.66)
    positions = []
    for im in line_imgs:
        positions.append((x0, y))
        y += im.height + 16
    # underline swash under the second line (the designated phrase)
    lx, ly = positions[1]
    swash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(swash).line(
        [(lx, ly + line_imgs[1].height + 4), (lx + line_imgs[1].width, ly + line_imgs[1].height + 4)],
        fill=INK[:3] + (200,), width=3)

    inputs = ["-loop", "1", "-i", str(cropped)]
    filt_parts = []
    last = "0:v"
    press_start, press_gap, press_fade = 0.3, 0.55, 0.4
    for i, (im, (x, y)) in enumerate(zip(line_imgs, positions)):
        p = SEG_DIR / f"_s31_line{i}.png"
        im.save(p)
        inputs += ["-loop", "1", "-i", str(p)]
        idx = i + 1
        t0 = press_start + i * press_gap
        faded, label = f"f{idx}", f"v{idx}"
        filt_parts.append(f"[{idx}:v]format=rgba,fade=t=in:st={t0:.2f}:d={press_fade}:alpha=1[{faded}]")
        filt_parts.append(f"[{last}][{faded}]overlay=0+{x}:0+{y}:enable='gte(t,{t0:.2f})'[{label}]")
        last = label
    swash_path = SEG_DIR / "_s31_swash.png"
    swash.save(swash_path)
    inputs += ["-loop", "1", "-i", str(swash_path)]
    swash_t0 = press_start + len(lines) * press_gap
    filt_parts.append(f"[{len(lines) + 1}:v]format=rgba,fade=t=in:st={swash_t0:.2f}:d=0.3:alpha=1[fsw]")
    filt_parts.append(f"[{last}][fsw]overlay=0:0:enable='gte(t,{swash_t0:.2f})'[vout]")
    filt = ";".join(filt_parts)
    _run(["ffmpeg", "-y", "-v", "error", *inputs, "-t", f"{duration:.3f}",
          "-filter_complex", filt, "-map", "[vout]",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])
    cropped.unlink(missing_ok=True)
    swash_path.unlink(missing_ok=True)
    for i in range(len(lines)):
        (SEG_DIR / f"_s31_line{i}.png").unlink(missing_ok=True)


INFOGRAPHIC = HERE / "_infographic"


def build_s32(dest, duration, doa):
    """The Honest Match plate ($0, deliberate style-break infographic
    insert -- memory feedback-infographic-insert-override, design by
    Fable 2026-08-08). Rendered once via panel_animator/render_dom_clip.py
    from _infographic/honest_plate.html; here it's just trimmed to the
    segment's exact duration, same pattern as every other pre-rendered
    source clip in this dispatch table."""
    src = INFOGRAPHIC / "honest_plate.mp4"
    _run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-t", f"{duration:.3f}",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])


def _naming_plate_offset(name: str) -> float:
    """Seconds into naming_plate.html's own 28.20s master timeline where
    `name`'s spread begins -- t=0 of the master IS s34's spread start."""
    return st.by_name[name][2] - st.by_name["s34_naming_serpent"][2]


def build_s34(dest, duration, doa):
    """The Naming Docket plate, entry 1/3 (the serpent, Rev 12:9) -- same
    deliberate style-break as s32. s34/s35(/s36) are ONE continuous
    render (_infographic/naming_plate.mp4) split at the real window
    boundaries per Fable's extensibility design -- never re-rendered
    per-segment, so the seam between s34 and s35 is pixel-continuous by
    construction."""
    src = INFOGRAPHIC / "naming_plate.mp4"
    offset = _naming_plate_offset("s34_naming_serpent")
    _run(["ffmpeg", "-y", "-v", "error", "-ss", f"{offset:.3f}", "-i", str(src),
          "-t", f"{duration:.3f}",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])


def build_s35(dest, duration, doa):
    """The Naming Docket plate, entry 2/3 (the mission, 1 John 3:8) --
    continuation of s34's same rendered plate, see build_s34."""
    src = INFOGRAPHIC / "naming_plate.mp4"
    offset = _naming_plate_offset("s35_naming_mission")
    _run(["ffmpeg", "-y", "-v", "error", "-ss", f"{offset:.3f}", "-i", str(src),
          "-t", f"{duration:.3f}",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])


def build_s36(dest, duration, doa):
    """The Naming Docket plate, entry 3/3 (the crushing, Rom 16:20) --
    continuation of s34's same rendered plate, see build_s34.
    motion_lint FROZEN-SPREAD fix: this window's own press-in events are
    brief (0.32s each) against a long mostly-static hold -- added
    line_boil grain (same $0 post-process, same amount, as s27's proven
    fix) rather than touching the shared plate's own timeline, which
    s34/s35 also depend on."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import line_boil  # noqa: E402
    src = INFOGRAPHIC / "naming_plate.mp4"
    offset = _naming_plate_offset("s36_naming_crushing")
    raw = dest.parent / (dest.stem + "_raw.mp4")
    _run(["ffmpeg", "-y", "-v", "error", "-ss", f"{offset:.3f}", "-i", str(src),
          "-t", f"{duration:.3f}",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(raw)])
    line_boil.render(raw, dest, 0.5)
    raw.unlink(missing_ok=True)


# ------------------------------------------------------- batch 5 (2026-08-08+, spreads 37-45)

def build_s37(dest, duration, doa):
    """Thread Device ($0) -- the gold thread-sprout rising from the seed
    through the stacked page-edges, fading and swelling into visibility
    (thread_opacity fade-in + thread_swell). Seed position measured
    against the real still (brightest-pixel scan, not eyeballed):
    (1338,1275) in the still's own 2752x1536 space -> (0.486, 0.830).
    motion_lint FROZEN-SPREAD fix: width=10 only reached p95=0.050 --
    same "thin gold line on a huge frame" issue s21/s25 already hit;
    widened to 26 (matching that precedent's own range)."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import thread_device  # noqa: E402
    still = STILLS / "s37_promise_planted.png"
    base = Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA")
    p0_frac, p1_frac = (0.486, 0.830), (0.50, 0.32)
    thread = thread_device.make_thread_layer(W, H, p0_frac, p1_frac, thread_device.GOLD, width=26)
    thread_bright = thread_device.make_thread_layer(W, H, p0_frac, p1_frac, thread_device.GOLD_BRIGHT, width=26)
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        opacity = thread_device.thread_opacity(t, start=duration * 0.25, fade=duration * 0.5)
        swell = thread_device.thread_swell(t, duration * 0.75, rise=0.6, decay=0.8)
        layer = Image.blend(thread.convert("RGB"), thread_bright.convert("RGB"), swell).convert("RGBA")
        alpha = thread.split()[3].point(lambda a, opacity=opacity: int(a * opacity))
        layer.putalpha(alpha)
        frame = base.copy()
        frame.alpha_composite(layer)
        frame.convert("RGB").save(frames / f"f{i:05d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


def build_s38(dest, duration, doa):
    """raking-light ($0, this episode's ONE use per _PLAN.md) -- the
    lamp's own light sweeping the cooled, pulled-back desk once,
    register-dropped ("gold dimmed deliberately"). held-breath's energy
    scales the sweep's own small strength range so the beat still
    breathes quietly rather than a flat mechanical pass ("quiet point
    2").
    motion_lint FROZEN-SPREAD fix: k=0.02-0.032 (within the module's own
    "keep small" guidance) only reached p95=0.020 -- a narrow sweep band
    only affects a small fraction of a 1920-wide frame at any moment, so
    even a "normal" k barely moves the whole-frame average. Widened the
    band (650px -> 1200px) rather than pushing k to an unnaturally high,
    obvious-video-filter value -- more of the frame sweeps at once, k
    itself only nudged up slightly."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import raking_light  # noqa: E402
    import line_boil  # noqa: E402
    from held_breath import energy_envelope  # noqa: E402
    still = STILLS / "s38_skeptic_quiet.png"
    base = raking_light.scale_crop(Image.open(still).convert("RGB"), W, H)
    tooth = raking_light.paper_tooth_highpass(base)
    energy = energy_envelope(ALIGNMENT, st.LAST_WORD_END_ESTIMATE, floor=0.25, ramp=0.15)
    abs_start = st.by_name["s38_skeptic_quiet"][2]
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        progress = t / duration
        e = energy(abs_start + t)
        # round 2: k=0.05-0.08 + band=1200px only reached p95=0.059, still
        # short of 0.15. Pushed k further (band already covers most of
        # the frame's width, little more room there).
        k = 0.14 + 0.04 * e
        frame = raking_light.apply_raking_light(base, progress, tooth=tooth, k=k,
                                                 band_width_px=1200.0, angle_deg=15.0)
        frame.save(frames / f"f{i:05d}.png")
    raw = dest.parent / (dest.stem + "_raw.mp4")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(raw)])
    import shutil as _shutil
    _shutil.rmtree(frames)
    # round 3: k pushed to 0.14-0.18 still only reached p95=0.091 --
    # raking_light alone has diminishing returns past this point. Added
    # line_boil as a supplementary pass instead of pushing k further,
    # same reliable fix already proven on s36/s39 this batch.
    line_boil.render(raw, dest, 0.6)
    raw.unlink(missing_ok=True)


def build_s39(dest, duration, doa):
    """$0 reuse of s38's own wide-desk art, cropped tight to the desk's
    own near margin, with the Keeper's own hand writing the honest (not
    panicked) objection -- energy 0.35 per _PLAN.md, one entry, same
    reuse pattern as s07-over-s06.
    motion_lint FROZEN-SPREAD fix: a single small corner phrase only
    reached p95=0.038 across a 7.7s hold -- same small-ink-area issue as
    everything else in this batch. Rather than change the entry's own
    calm energy/size (that's the authored beat, not a bug), added
    line_boil grain over the whole composited hold, same $0 post-process
    already proven on s27/s36."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import keeper_hand as KH  # noqa: E402
    import line_boil  # noqa: E402
    still = STILLS / "s38_skeptic_quiet.png"
    src = Image.open(still).convert("RGB")
    sw, sh = src.size
    crop = src.crop((int(sw * 0.16), int(sh * 0.30), int(sw * 0.62), int(sh * 0.75))).resize((W, H), Image.LANCZOS)
    entry = KH.KeeperEntry(
        ["Just a snake story?"], origin=(int(W * 0.12), int(H * 0.58)),
        size=60, energy=0.35, seed=139, t0=0.4, dur=2.2)
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        frame = entry.compose(crop, t)
        frame.save(frames / f"f{i:05d}.png")
    raw = dest.parent / (dest.stem + "_raw.mp4")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(raw)])
    import shutil as _shutil
    _shutil.rmtree(frames)
    # motion_lint FROZEN-SPREAD fix round 2: amount=0.5 got p95=0.144, a
    # hair under T_frozen=0.15. Pushed to 0.8.
    line_boil.render(raw, dest, 0.8)
    raw.unlink(missing_ok=True)


def build_s40(dest, duration, doa):
    """$0 hold: the "her seed" study copy recalled on the blank left
    page (same text/RUBRIC color as s26, a deliberate callback -- "the
    ordinary reading given real weight"), the graphite descent-sketches
    already rendered on the right. focal-tour (dramatic_spotlight)
    shifts attention from the copy to the sketches across the hold;
    line_boil grain wobble over the whole thing so held stillness reads
    alive, not locked."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import focal_tour  # noqa: E402
    import line_boil  # noqa: E402
    still = STILLS / "s40_partly_fair.png"
    base = Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA")
    callback_size = 28
    lines = [
        [("And I will put enmity between thee and the woman,", callback_size)],
        [("and between thy seed and her seed;", callback_size)],
        [("it shall bruise thy head,", callback_size)],
        [("and thou shalt bruise his heel.", callback_size)],
    ]
    line_imgs = [render_line_png(line, seed=4029 + i, ink=RUBRIC) for i, line in enumerate(lines)]
    x0, y = int(W * 0.09), int(H * 0.32)
    for im in line_imgs:
        base.alpha_composite(im, (x0, y))
        y += im.height + 14
    composed = SEG_DIR / "_s40_composed.png"
    base.convert("RGB").save(composed)

    raw = dest.parent / (dest.stem + "_raw.mp4")
    focal_regions = [
        {"bbox": [4, 20, 42, 60]},   # the study copy, left
        {"bbox": [52, 8, 44, 88]},   # the graphite sketches, right
    ]
    focal_tour.render_clip(composed, focal_regions, "dramatic_spotlight", duration, W, H, raw)
    line_boil.render(raw, dest, 0.5)
    raw.unlink(missing_ok=True)
    composed.unlink(missing_ok=True)


def build_s41(dest, duration, doa):
    """$0 camera pan (a gentle continuous glide, never zooming past
    ~1.35x) -- the paid clip was tried TWICE and BOTH providers invented
    content on this densely-detailed still: Kling (duration=6 wasn't a
    valid seedance1_5 value, silently fell back to Kling) re-folded
    several page-tips between frames; the retry on the INTENDED Seedance
    provider (duration fixed to 8s) instead bloomed new ink-blot marks
    that weren't in the source, visible as early as 2.7s in. Two
    different providers hallucinating the SAME still is the signal to
    stop paying and use a $0 procedural move instead (memory
    [[feedback-static-ai-clips-need-real-camera]]) -- this is the exact
    same pixels the whole time, so nothing can be invented."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import hunt_and_lock  # noqa: E402
    still = STILLS / "s41_shape_of_canon.png"
    src = Image.open(still).convert("RGB")
    big = hunt_and_lock.scale_crop(src, int(W * 1.35), int(H * 1.35))
    bw, bh = big.size
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        k = hunt_and_lock.ease(t / duration)
        cx = bw * 0.32 + (bw * 0.68 - bw * 0.32) * k
        cy = bh * 0.55
        x0 = max(0, min(bw - W, int(cx - W / 2)))
        y0 = max(0, min(bh - H, int(cy - H / 2)))
        frame = big.crop((x0, y0, x0 + W, y0 + H))
        frame.save(frames / f"f{i:05d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


def build_s42(dest, duration, doa):
    """focal-tour ($0) -- visits the three vignettes in narration order
    (the serpent named / the Son destroying the works / the woman's
    child) via a soft light halo, dramatic_spotlight style. Bbox regions
    read off the actual composed still (Jesus dominant center, serpent
    duller at left, mother+child duller at right -- redesigned per the
    SP-G6 fix, see _s2_stills.py's re-roll note)."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import focal_tour  # noqa: E402
    still = STILLS / "s42_from_within.png"
    focal_regions = [
        {"bbox": [4, 18, 34, 62]},    # the serpent, left
        {"bbox": [34, 2, 34, 96]},    # Jesus, center
        {"bbox": [70, 22, 26, 55]},   # mother + child, right
    ]
    focal_tour.render_clip(still, focal_regions, "dramatic_spotlight", duration, W, H, dest)


def build_s45(dest, duration, doa):
    """hunt_and_lock camera push ($0) toward the cross, Thread Device
    ($0) reprojected into the moving crop -- Eden to the cross (this
    spread's thread is NOT pre-drawn in the still, unlike s25's
    convention -- deliberately, to avoid trusting the image model with a
    coherent gold line across such a wide composition; added procedurally
    like s37/s42 instead). Endpoints measured against the real still, not
    eyeballed: Eden's own ground-line at the left (0.12, 0.72), the
    cross's base at the right (dark-pixel scan found its silhouette at
    (2400,890) in the still's 2752x1536 space -> (0.872, 0.58); nudged
    down slightly to its base, 0.66).
    HERO-STILLS CINEMATIC PASS FIX (2026-08-09, parallel review): the
    prior version composited the thread onto a 100% static base -- zero
    camera motion for the full clip, the exact "freeze-hold with a
    graphic mistaken for motion" failure this pass exists to catch. Now
    reuses the SAME hunt_and_lock camera push already proven on s16/s28/
    s33, targeting the cross itself (p1_frac) so the shot's true subject
    gets real visual weight by the end -- same reprojection pattern as
    s28 (thread endpoints tracked into each frame's moving crop via
    hunt_and_lock.hunt_window/project_point, scarlet lock-marker skipped
    since the gold thread is already this shot's "arrived" device).
    motion_lint FROZEN-SPREAD fix carried over: thread width=26 (a thin
    10px line on a huge frame under-registers on the luminance-diff
    metric, same issue as s37/s21/s25)."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import hunt_and_lock  # noqa: E402
    import thread_device  # noqa: E402
    still = STILLS / "s45_eden_to_cross.png"
    p0_frac, p1_frac = (0.12, 0.72), (0.872, 0.66)
    src = Image.open(still).convert("RGB")
    big = hunt_and_lock.scale_crop(src, int(W * hunt_and_lock.UPSCALE), int(H * hunt_and_lock.UPSCALE))
    bw, bh = big.size
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        x0, y0, vw, vh, _lock_prog, _wxy = hunt_and_lock.hunt_window(bw, bh, t, duration, p1_frac, W, H)
        frame = big.crop((x0, y0, x0 + vw, y0 + vh)).resize((W, H), Image.LANCZOS).convert("RGBA")
        sx0, sy0 = hunt_and_lock.project_point(p0_frac[0], p0_frac[1], bw, bh, x0, y0, vw, vh, W, H)
        sx1, sy1 = hunt_and_lock.project_point(p1_frac[0], p1_frac[1], bw, bh, x0, y0, vw, vh, W, H)
        thread = thread_device.make_thread_layer(
            W, H, (sx0 / W, sy0 / H), (sx1 / W, sy1 / H), thread_device.GOLD, width=26)
        thread_bright = thread_device.make_thread_layer(
            W, H, (sx0 / W, sy0 / H), (sx1 / W, sy1 / H), thread_device.GOLD_BRIGHT, width=26)
        opacity = thread_device.thread_opacity(t, start=duration * 0.15, fade=duration * 0.4)
        swell = thread_device.thread_swell(t, duration * 0.6, rise=0.6, decay=0.8)
        layer = Image.blend(thread.convert("RGB"), thread_bright.convert("RGB"), swell).convert("RGBA")
        alpha = thread.split()[3].point(lambda a, opacity=opacity: int(a * opacity))
        layer.putalpha(alpha)
        frame.alpha_composite(layer)
        frame.convert("RGB").save(frames / f"f{i:05d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


# ---------------------------------------------------------- batch 6 (2026-08-09, spreads 46-55)

def build_s46(dest, duration, doa):
    """Local flame-flicker ($0) -- a small warm glow breathes ONLY on the
    lamp's own drawn flame; everything else in the frame (including the
    page region s47's text overlay needs byte-static) is untouched.
    REJECTED v1 (caught on eye-check, not shipped): candle_only.
    apply_candle's radial light-BUDGET crushed the entire desk to near-
    black outside a ~50px radius (COLD_GAIN=0.16) -- that module is built
    for a tiny point-of-light accent in an already-dark scene (its own
    proven case, s09, is a single gold fleck), not for lighting an entire
    medium desk shot. This is a plain additive glow instead, reusing only
    candle_only's flicker_R curve for the breathing rhythm. Anchor
    measured via bbox_sheet.py against the actual rendered still."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import candle_only  # noqa: E402 -- reused only for its flicker_R curve
    still = STILLS / "s46_look_again.png"
    poc_devices = load_devices_here()
    anchor_frac = poc_devices.DEVICE_ASSIGNMENTS["s46_look_again"]["params"]["anchor_frac"]
    ax, ay = anchor_frac[0] * W, anchor_frac[1] * H
    src = np.asarray(Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS), dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.sqrt((xx - ax) ** 2 + (yy - ay) ** 2)
    # FROZEN-SPREAD fix (2026-08-09): a 90px/amplitude=0.35 glow only
    # touched a tiny fraction of the 1920x1080 frame -- p95=0.018, the
    # same "too-thin-to-register" class of miss as this episode's thread-
    # device spreads (s21/s25/s37/s45). Widened radius + strength; still
    # local to the lamp, nowhere near s47's page region.
    glow_mask = np.clip(1.0 - dist / 170.0, 0.0, 1.0) ** 2
    base_curve = lambda t: 1.0  # noqa: E731 -- flat: breathing comes from flicker_R's own noise
    flick = candle_only.flicker_R(base_curve, seed=460, amplitude=0.6)
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        strength = max(0.0, flick(t)) * 130.0
        boost = glow_mask * strength
        arr = np.clip(src + boost[..., None] * np.array([1.0, 0.75, 0.35], np.float32), 0, 255).astype(np.uint8)
        Image.fromarray(arr).save(frames / f"f{i:05d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


def build_s47(dest, duration, doa):
    """Scribed Ink composite, $0 -- Gen 3:15b re-study over s46's OWN
    already-rendered desk art (not a new render), page-full per the
    camera table. Red-letter (RUBRIC): the LORD's own Gen 3:14-15 speech
    restudied, same voice as s22's card."""
    bg = STILLS / "s46_look_again.png"
    cropped = SEG_DIR / "_s47_bg_crop.png"
    _run(["ffmpeg", "-y", "-v", "error", "-i", str(bg), "-vf",
          f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"boxblur=1:1,eq=brightness=0.03", "-frames:v", "1", str(cropped)])
    poc_devices = load_devices_here()
    card = poc_devices.VERSE_CARDS["s47_two_wounds_card"]
    lines = card["lines"]

    line_imgs = [render_line_png(line, seed=470 + i, ink=RUBRIC) for i, line in enumerate(lines)]
    y = int(H * 0.35)
    positions = []
    for im in line_imgs:
        x = int((W - im.width) / 2)
        positions.append((x, y))
        y += im.height + 20

    inputs = ["-loop", "1", "-i", str(cropped)]
    filt_parts = []
    last = "0:v"
    press_start, press_gap, press_fade = 0.5, 1.1, 0.5
    for i, (im, (x, y)) in enumerate(zip(line_imgs, positions)):
        p = SEG_DIR / f"_s47_line{i}.png"
        im.save(p)
        inputs += ["-loop", "1", "-i", str(p)]
        idx = i + 1
        t0 = press_start + i * press_gap
        faded, label = f"f{idx}", f"v{idx}"
        filt_parts.append(f"[{idx}:v]format=rgba,fade=t=in:st={t0:.2f}:d={press_fade}:alpha=1[{faded}]")
        filt_parts.append(f"[{last}][{faded}]overlay=0+{x}:0+{y}:enable='gte(t,{t0:.2f})'[{label}]")
        last = label
    filt = ";".join(filt_parts)
    _run(["ffmpeg", "-y", "-v", "error", *inputs, "-t", f"{duration:.3f}",
          "-filter_complex", filt, "-map", f"[{last}]",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])
    cropped.unlink(missing_ok=True)
    for i in range(len(lines)):
        (SEG_DIR / f"_s47_line{i}.png").unlink(missing_ok=True)


def build_s49(dest, duration, doa):
    """dramatic_spotlight ($0) -- a soft light pulse over the whole
    frozen standoff (raised heel above, serpent's head below), bbox
    spanning both per _PREFLIGHT.md's own device note. No camera move,
    no paid animator, on purpose -- the highest doctrinal-stakes frame
    in the film (SERPENT.md rule #6: the head-crush is NEVER an impact
    frame, freeze the instant before)."""
    still = STILLS / "s49_head_crush.png"
    poc_devices = load_devices_here()
    bbox = poc_devices.DEVICE_ASSIGNMENTS["s49_head_crush"]["params"]["bbox"]
    doa._spotlight_family("dramatic_spotlight", still, dest, duration, bbox)


def build_s50(dest, duration, doa):
    """hunt_and_lock ($0 real camera push) toward the crucified figure,
    combined with a slow darkness-deepen luminance ramp -- a GLORY beat
    ("the lens kneels," _PREFLIGHT.md E2 point 2), flipped from the
    original plan's paid Seedance clip (batch-6 quote) to avoid any risk
    of a generative animator inventing storm-cloud motion on this film's
    "darkness, never storm" sky. Target measured via bbox_sheet.py
    against the actual rendered still."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import hunt_and_lock  # noqa: E402
    still = STILLS / "s50_that_is_the_cross.png"
    poc_devices = load_devices_here()
    target_frac = tuple(poc_devices.DEVICE_ASSIGNMENTS["s50_that_is_the_cross"]["params"]["target_frac"])
    src = Image.open(still).convert("RGB")
    big = hunt_and_lock.scale_crop(src, int(W * hunt_and_lock.UPSCALE), int(H * hunt_and_lock.UPSCALE))
    bw, bh = big.size
    n = max(1, int(round(duration * FPS)))
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        x0, y0, vw, vh, _lock_prog, _wxy = hunt_and_lock.hunt_window(bw, bh, t, duration, target_frac, W, H)
        frame = big.crop((x0, y0, x0 + vw, y0 + vh)).resize((W, H), Image.LANCZOS)
        gain = 1.0 - 0.12 * (t / duration)  # darkness thickens very slightly across the hold
        arr = (np.asarray(frame, dtype=np.float32) * gain).clip(0, 255).astype(np.uint8)
        Image.fromarray(arr).save(frames / f"f{i:05d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


def build_s52(dest, duration, doa):
    """wash-creep RETREAT ($0) over s50's OWN already-rendered art (not a
    new render) -- the dark sky isolated as the "storm wash," retreating
    to reveal more of the hillside as the moment holds; its last trace
    naturally lingers nearest the cross, per the still's own composition
    (mirror of s14's ADVANCE -- the payoff planted when s14 was built,
    per that function's own docstring)."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import wash_creep  # noqa: E402
    base = wash_creep.scale_crop(Image.open(STILLS / "s50_that_is_the_cross.png").convert("RGB"), W, H)
    mask = wash_creep.isolate_storm_wash(base)
    n = max(1, int(round(duration * wash_creep.FPS)))
    ADVANCE_MAX_LOCAL = 30.0
    plan = [(ADVANCE_MAX_LOCAL - wash_creep._ease(i / max(1, n - 1)) * (2 * ADVANCE_MAX_LOCAL), False)
            for i in range(n)]
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i, (advance_px, backrun) in enumerate(plan):
        frame = wash_creep.apply_wash_creep(base, advance_px, mask=mask, backrun=backrun)
        frame.save(frames / f"f{i:05d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(wash_creep.FPS),
          "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


def build_s53(dest, duration, doa):
    """Scribed Ink composite, $0 -- Heb 2:14b over s51's OWN already-
    rendered art, re-framed (not a new render). NOT red-letter -- this is
    the writer of Hebrews explaining Christ, not the LORD's own first-
    person voice (contrast s47/s22).
    REDESIGNED (2026-08-09, v1 rejected on eye-check): the original
    "letters in the dark sky field" plan assumed a wide open-sky margin
    like s51's own full still, but this close reverent crop leaves almost
    no clear sky -- v1's text landed directly across Christ's face,
    illegible against His hair. Fixed with make_ink_assets.torn_band's
    standard parchment-caption-band technique (CLAUDE.md's own default
    text treatment): a real opaque parchment patch positioned across the
    crossbeam/rope area at the TOP of frame (busy wood/rope, not His
    face), guaranteeing legibility regardless of what's behind it."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import make_ink_assets  # noqa: E402
    bg = STILLS / "s51_bearing_wages.png"
    cropped = SEG_DIR / "_s53_bg_crop.png"
    _run(["ffmpeg", "-y", "-v", "error", "-i", str(bg), "-vf",
          f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"boxblur=1:1,eq=brightness=-0.04", "-frames:v", "1", str(cropped)])
    band_path = SEG_DIR / "_s53_band.png"
    if not band_path.exists():
        make_ink_assets.torn_band(w=1750, h=280, out=str(band_path))
    band = Image.open(band_path).convert("RGBA")
    base = Image.open(cropped).convert("RGBA")
    base.alpha_composite(band, (int(W * 0.045), 24))
    base.convert("RGB").save(cropped)
    poc_devices = load_devices_here()
    card = poc_devices.VERSE_CARDS["s53_through_death_card"]
    lines = card["lines"]

    line_imgs = [render_line_png(line, seed=530 + i) for i, line in enumerate(lines)]
    x0 = int(W * 0.075)
    y = int(H * 0.06)
    positions = []
    for im in line_imgs:
        positions.append((x0, y))
        y += im.height + 14

    inputs = ["-loop", "1", "-i", str(cropped)]
    filt_parts = []
    last = "0:v"
    press_start, press_gap, press_fade = 0.4, 0.9, 0.4
    for i, (im, (x, y)) in enumerate(zip(line_imgs, positions)):
        p = SEG_DIR / f"_s53_line{i}.png"
        im.save(p)
        inputs += ["-loop", "1", "-i", str(p)]
        idx = i + 1
        t0 = press_start + i * press_gap
        faded, label = f"f{idx}", f"v{idx}"
        filt_parts.append(f"[{idx}:v]format=rgba,fade=t=in:st={t0:.2f}:d={press_fade}:alpha=1[{faded}]")
        filt_parts.append(f"[{last}][{faded}]overlay=0+{x}:0+{y}:enable='gte(t,{t0:.2f})'[{label}]")
        last = label
    filt = ";".join(filt_parts)
    _run(["ffmpeg", "-y", "-v", "error", *inputs, "-t", f"{duration:.3f}",
          "-filter_complex", filt, "-map", f"[{last}]",
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(dest)])
    cropped.unlink(missing_ok=True)
    for i in range(len(lines)):
        (SEG_DIR / f"_s53_line{i}.png").unlink(missing_ok=True)


def build_s55(dest, duration, doa):
    """Bespoke shadow-sweep ($0), E6-I -- the SAME still as s54 (a held
    device, not a new render): the cross-beam's own shadow travels from
    the cross's position onto the serpent's shadow-head and holds there.
    No new content, no impact, no strike, no gore -- the shadow of the
    cross IS the crushing (SERPENT.md rule #6: the narration's own
    theology does the visual work, not a literal strike). Endpoints
    measured via bbox_sheet.py against the actual rendered still."""
    sys.path.insert(0, str(ROOT / "panel_animator"))
    import hunt_and_lock  # noqa: E402 -- reused only for its ease() curve
    poc_devices = load_devices_here()
    params = poc_devices.DEVICE_ASSIGNMENTS["s55_the_inversion"]["params"]
    cross_frac, head_frac = params["cross_frac"], params["head_frac"]
    base = Image.open(STILLS / "s54_seeming_win.png").convert("RGB").resize((W, H), Image.LANCZOS)
    base_arr = np.asarray(base, dtype=np.float32)
    cx, cy = cross_frac[0] * W, cross_frac[1] * H
    hx, hy = head_frac[0] * W, head_frac[1] * H
    yy, xx = np.mgrid[0:H, 0:W]
    xx, yy = xx.astype(np.float32), yy.astype(np.float32)
    n = max(1, int(round(duration * FPS)))
    sweep_dur = duration * 0.55
    radius = 130.0
    frames = dest.parent / (dest.stem + "_frames")
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / FPS
        k = hunt_and_lock.ease(min(1.0, t / sweep_dur))
        lead_x, lead_y = cx + (hx - cx) * k, cy + (hy - cy) * k
        dist = np.sqrt((xx - lead_x) ** 2 + (yy - lead_y) ** 2)
        darken = np.clip(1.0 - dist / radius, 0.0, 1.0) * 0.55 * k
        arr = base_arr * (1.0 - darken[..., None])
        Image.fromarray(arr.clip(0, 255).astype(np.uint8)).save(frames / f"f{i:05d}.png")
    _run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    import shutil as _shutil
    _shutil.rmtree(frames)


SEGMENT_BUILDERS = {
    "s01_something_wrong": lambda dest, dur, doa: build_s01(dest, dur, doa),
    "s02_the_hiding": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s02_the_hiding.mp4"),
    "s03_verse_card": lambda dest, dur, doa: build_s03(dest, dur, doa),
    "s04_god_walking": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s04_god_walking.mp4"),
    "s05_where_art_thou": lambda dest, dur, doa: build_s05(dest, dur, doa),
    # test-tier (2026-08-07, independent-review staged build order)
    "s06_blame_circle": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s06_blame_circle.mp4"),
    "s16_watch_closely": lambda dest, dur, doa: build_s16(dest, dur, doa),
    # batch 2 (2026-08-08, spreads 7-15)
    "s07_beguiled_card": lambda dest, dur, doa: build_s07(dest, dur, doa),
    "s08_coming_apart": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s08_coming_apart.mp4"),
    "s09_unexpected_place": lambda dest, dur, doa: build_s09(dest, dur, doa),
    "s10_judgment_falls": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s10_judgment_falls.mp4"),
    "s11_afraid_of_presence": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s11_afraid_of_presence.mp4"),
    "s12_creatures_word": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s12_creatures_word.mp4"),
    "s13_the_fruit": lambda dest, dur, doa: build_s13(dest, dur, doa),
    "s14_death_enters": lambda dest, dur, doa: build_s14(dest, dur, doa),
    "s15_the_breach": lambda dest, dur, doa: build_s15(dest, dur, doa),
    # s51 (Jesus multi-pose anchor, out-of-order per the plan's own note)
    "s51_bearing_wages": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s51_bearing_wages.mp4"),
    # batch 3 (2026-08-08, spreads 17-25, movement 3 close)
    "s17_not_adam_not_eve": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s17_not_adam_not_eve.mp4"),
    "s18_turns_to_serpent": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s18_turns_to_serpent.mp4"),
    "s19_curse_card": lambda dest, dur, doa: build_s19(dest, dur, doa),
    "s20_pure_curse": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s20_pure_curse.mp4"),
    "s21_gold_woven_in": lambda dest, dur, doa: build_s21(dest, dur, doa),
    "s22_promise_card": lambda dest, dur, doa: build_s22(dest, dur, doa),
    "s23_let_that_land": lambda dest, dur, doa: build_s23(dest, dur, doa),
    "s24_before_their_sentences": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s24_before_their_sentences.mp4"),
    "s25_promise_in_curse": lambda dest, dur, doa: build_s25(dest, dur, doa),
    # batch 4 (2026-08-08+, spreads 26-35, movement 4)
    "s26_her_seed_study": lambda dest, dur, doa: build_s26(dest, dur, doa),
    "s27_line_of_fathers": lambda dest, dur, doa: build_s27(dest, dur, doa),
    "s28_clue_lights_up": lambda dest, dur, doa: build_s28(dest, dur, doa),
    "s29_fulness_card": lambda dest, dur, doa: build_s29(dest, dur, doa),
    "s30_annunciation": lambda dest, dur, doa: build_s30(dest, dur, doa),
    "s31_holy_thing_card": lambda dest, dur, doa: build_s31(dest, dur, doa),
    "s32_honest_match": lambda dest, dur, doa: build_s32(dest, dur, doa),
    "s33_trajectory": lambda dest, dur, doa: build_s33(dest, dur, doa),
    "s34_naming_serpent": lambda dest, dur, doa: build_s34(dest, dur, doa),
    "s35_naming_mission": lambda dest, dur, doa: build_s35(dest, dur, doa),
    "s36_naming_crushing": lambda dest, dur, doa: build_s36(dest, dur, doa),
    "s37_promise_planted": lambda dest, dur, doa: build_s37(dest, dur, doa),
    "s38_skeptic_quiet": lambda dest, dur, doa: build_s38(dest, dur, doa),
    "s39_snake_story": lambda dest, dur, doa: build_s39(dest, dur, doa),
    "s40_partly_fair": lambda dest, dur, doa: build_s40(dest, dur, doa),
    "s41_shape_of_canon": lambda dest, dur, doa: build_s41(dest, dur, doa),
    "s42_from_within": lambda dest, dur, doa: build_s42(dest, dur, doa),
    "s43_under_your_feet": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s43_under_your_feet.mp4"),
    "s44_stands_on_one": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s44_stands_on_one.mp4", play_dur=5.0),
    "s45_eden_to_cross": lambda dest, dur, doa: build_s45(dest, dur, doa),
    # batch 6 (2026-08-09, spreads 46-55, "the crushing")
    "s46_look_again": lambda dest, dur, doa: build_s46(dest, dur, doa),
    "s47_two_wounds_card": lambda dest, dur, doa: build_s47(dest, dur, doa),
    "s48_heel_strike": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s48_heel_strike.mp4"),
    "s49_head_crush": lambda dest, dur, doa: build_s49(dest, dur, doa),
    "s50_that_is_the_cross": lambda dest, dur, doa: build_s50(dest, dur, doa),
    # s51_bearing_wages already wired above (out-of-order anchor, built
    # 2026-08-07) -- not re-listed here to avoid a duplicate dict key.
    "s52_judgment_on_him": lambda dest, dur, doa: build_s52(dest, dur, doa),
    "s53_through_death_card": lambda dest, dur, doa: build_s53(dest, dur, doa),
    "s54_seeming_win": lambda dest, dur, doa: build_clip_hold(dest, dur, CLIPS / "s54_seeming_win.mp4"),
    "s55_the_inversion": lambda dest, dur, doa: build_s55(dest, dur, doa),
}

SOURCE_FILES = {
    "s01_something_wrong": [STILLS / "s01_something_wrong.png"],
    "s02_the_hiding": [CLIPS / "s02_the_hiding.mp4"],
    "s03_verse_card": [WORLD / "eden_ref.png", HERE / "_devices.py"],
    "s04_god_walking": [CLIPS / "s04_god_walking.mp4"],
    "s05_where_art_thou": [STILLS / "s05_where_art_thou.png"],
    "s06_blame_circle": [CLIPS / "s06_blame_circle.mp4"],
    "s16_watch_closely": [STILLS / "s16_sentencing_tableau.png", HERE / "_devices.py"],
    "s07_beguiled_card": [STILLS / "s06_blame_circle.png", HERE / "_devices.py"],
    "s08_coming_apart": [CLIPS / "s08_coming_apart.mp4"],
    "s09_unexpected_place": [STILLS / "s09_unexpected_place.png", HERE / "_devices.py"],
    "s10_judgment_falls": [CLIPS / "s10_judgment_falls.mp4"],
    "s11_afraid_of_presence": [CLIPS / "s11_afraid_of_presence.mp4"],
    "s12_creatures_word": [CLIPS / "s12_creatures_word.mp4"],
    "s13_the_fruit": [STILLS / "s13_the_fruit.png", HERE / "_devices.py"],
    "s14_death_enters": [STILLS / "s14_death_enters.png"],
    "s15_the_breach": [STILLS / "s15_the_breach.png", HERE / "_devices.py"],
    "s51_bearing_wages": [CLIPS / "s51_bearing_wages.mp4"],
    "s17_not_adam_not_eve": [CLIPS / "s17_not_adam_not_eve.mp4"],
    "s18_turns_to_serpent": [CLIPS / "s18_turns_to_serpent.mp4"],
    "s19_curse_card": [STILLS / "s18_turns_to_serpent.png", HERE / "_devices.py"],
    "s20_pure_curse": [CLIPS / "s20_pure_curse.mp4"],
    "s21_gold_woven_in": [STILLS / "s20_pure_curse.png", HERE / "_devices.py"],
    "s22_promise_card": [STILLS / "s20_pure_curse.png", HERE / "_devices.py", HERE / "_alignment.json"],
    "s23_let_that_land": [SEG_DIR / "seg_s22_promise_card.mp4", HERE / "_devices.py"],
    "s24_before_their_sentences": [CLIPS / "s24_before_their_sentences.mp4"],
    "s25_promise_in_curse": [STILLS / "s25_promise_in_curse.png", HERE / "_devices.py"],
    "s26_her_seed_study": [STILLS / "s26_her_seed_study.png", HERE / "_alignment.json"],
    "s27_line_of_fathers": [STILLS / "s27_line_of_fathers.png"],
    "s28_clue_lights_up": [STILLS / "s28_clue_lights_up.png"],
    "s29_fulness_card": [STILLS / "s27_line_of_fathers.png", HERE / "_alignment.json"],
    "s30_annunciation": [STILLS / "s30_annunciation.png"],
    "s31_holy_thing_card": [STILLS / "s30_annunciation.png"],
    "s32_honest_match": [INFOGRAPHIC / "honest_plate.mp4"],
    "s33_trajectory": [STILLS / "s33_trajectory.png"],
    "s34_naming_serpent": [INFOGRAPHIC / "naming_plate.mp4"],
    "s35_naming_mission": [INFOGRAPHIC / "naming_plate.mp4"],
    "s36_naming_crushing": [INFOGRAPHIC / "naming_plate.mp4"],
    "s37_promise_planted": [STILLS / "s37_promise_planted.png"],
    "s38_skeptic_quiet": [STILLS / "s38_skeptic_quiet.png"],
    "s39_snake_story": [STILLS / "s38_skeptic_quiet.png"],
    "s40_partly_fair": [STILLS / "s40_partly_fair.png"],
    "s41_shape_of_canon": [STILLS / "s41_shape_of_canon.png"],
    "s42_from_within": [STILLS / "s42_from_within.png"],
    "s43_under_your_feet": [CLIPS / "s43_under_your_feet.mp4"],
    "s44_stands_on_one": [CLIPS / "s44_stands_on_one.mp4"],
    "s45_eden_to_cross": [STILLS / "s45_eden_to_cross.png"],
    # batch 6 (2026-08-09, spreads 46-55)
    "s46_look_again": [STILLS / "s46_look_again.png", HERE / "_devices.py"],
    "s47_two_wounds_card": [STILLS / "s46_look_again.png", HERE / "_devices.py"],
    "s48_heel_strike": [CLIPS / "s48_heel_strike.mp4"],
    "s49_head_crush": [STILLS / "s49_head_crush.png", HERE / "_devices.py"],
    "s50_that_is_the_cross": [STILLS / "s50_that_is_the_cross.png", HERE / "_devices.py"],
    "s52_judgment_on_him": [STILLS / "s50_that_is_the_cross.png"],
    "s53_through_death_card": [STILLS / "s51_bearing_wages.png", HERE / "_devices.py"],
    "s54_seeming_win": [CLIPS / "s54_seeming_win.mp4"],
    "s55_the_inversion": [STILLS / "s54_seeming_win.png", HERE / "_devices.py"],
}


def compute_hash(name: str, duration: float) -> str:
    payload = {
        "name": name,
        "renderer_version": RENDERER_VERSION,
        "duration": round(duration, 3),
        "sources": [_stat(p) for p in SOURCE_FILES[name]],
    }
    blob = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def build_segment(num, name, duration, doa, rebuild, progress_path):
    dest = SEG_DIR / f"seg_{name}.mp4"
    stamp_path = SEG_DIR / f"{name}.stamp.json"
    new_hash = compute_hash(name, duration)
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
