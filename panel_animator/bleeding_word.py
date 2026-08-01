#!/usr/bin/env python
"""Bleeding Word -- one drop, one word, once (Round 6 promotion, panel-revised
2026-07-30, `poc_living_sketchbook/_FABLE_ROUND6_THE_KEEPER.md` build card 4).
Promotes the bloom (radial wet darkening + edge dissolve + 2-3 descending
trails) from `poc_living_sketchbook/storm/_bold_poc/_build_bold.py` poc_3.

GOVERNORS (episode-design rules, only the word-locator half is enforced by
code):
  - Keeper's words ONLY -- the Word never bleeds (LAW 1). This module has no
    way to tell a Keeper word from a Scribed-Ink verse; the caller must only
    ever point `locate_word()` at a `keeper_hand.KeeperEntry`.
  - The bled word is THE word the episode is about -- <=1 per episode.
  - The drop lands ON the word's own ink, never on the art -- `locate_word()`
    exists precisely so a caller never has to hand-compute textlength offsets
    the way the original POC did (its `x_fear` calculation was a one-off,
    still-image-specific hack).
  - Foley: a single `drop`-family one-shot at impact (`ink_drop` in
    `scriptorium_foley.py`'s existing DEVICE_SOUND_MAP).

API:
    from bleeding_word import locate_word, BleedingWord
    import keeper_hand as K

    entry = K.KeeperEntry([("~~storm~~ ~~wind~~ fear.", 0, 0), ...],
                           origin=(390, 1686), size=64, energy=0.85, seed=41,
                           t0=0.5, dur=2.2, skid=True)
    cx, cy = locate_word(entry, line_index=0, word="fear.")
    bleed = BleedingWord(cx, cy, drop_t=3.2, seed=21)
    frame = entry.compose(frame, t)
    frame = bleed.compose(frame, t)
    cues = bleed.foley_cues()

Usage (CLI):
    .venv\\Scripts\\python.exe panel_animator\\bleeding_word.py --demo --still <still.png> --out demo.mp4 --duration 6
    .venv\\Scripts\\python.exe panel_animator\\bleeding_word.py --selftest
"""
from __future__ import annotations

import argparse
import random
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from raking_light import scale_crop  # noqa: E402 -- reuse, don't duplicate
import keeper_hand as K  # noqa: E402 -- reuse the Keeper's own font/layout, don't duplicate

FPS = 30
W, H = 1080, 1920


def _smootherstep(t: float) -> float:
    t = min(1.0, max(0.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


def _strip_strike_markers(word: str) -> str:
    if word.startswith("~~") and word.endswith("~~") and len(word) > 4:
        return word[2:-2]
    return word


def locate_word(entry: "K.KeeperEntry", line_index: int, word: str, occurrence: int = 1):
    """Find the pixel center (cx, cy) of ONE word within a
    `keeper_hand.KeeperEntry`'s laid-out text, so a drop can land on the
    word's OWN ink without hand-computing textlength offsets per episode the
    way the approved POC did. `word` matches the literal token text (strip
    any `~~strike~~` markers yourself or pass the bare word -- both work);
    `occurrence` picks the Nth match if the word repeats. Raises ValueError
    if not found. Uses the SAME font/size/origin the entry itself draws
    with, so the returned point always lands on the real rendered glyphs."""
    text, dx, dy = entry.lines[line_index]
    font = ImageFont.truetype(K.F_KEEPER, entry.size)
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    sp = probe.textlength(" ", font=font)
    target = _strip_strike_markers(word)
    seen = 0
    x = 0.0
    for raw in text.split():
        tok = _strip_strike_markers(raw)
        tw = probe.textlength(tok, font=font)
        if tok == target:
            seen += 1
            if seen == occurrence:
                cx = int(entry.origin[0] + dx + x + tw * 0.5)
                cy = int(entry.origin[1] + dy + entry.size * 0.55)
                return (cx, cy)
        x += tw + sp
    raise ValueError(f"word {word!r} (occurrence {occurrence}) not found in "
                      f"line {line_index} ({text!r}) of this KeeperEntry")


class BleedingWord:
    """One drop, landing on one word's own ink at `drop_t`, blooming: radial
    wet darkening + local blur (the letters lose their edges) + 2-3 thin ink
    trails finding their way down the page. Unchanged math from the approved
    POC (`_bold_poc/_build_bold.py::poc_3`), generalized off a caller-supplied
    impact point instead of a hardcoded still-specific offset."""

    def __init__(self, cx: int, cy: int, drop_t: float, seed: int = 21,
                 n_trails: int = 3, bloom_dur: float = 0.6, trail_dur: float = 1.2):
        self.cx, self.cy, self.drop_t = cx, cy, drop_t
        self.bloom_dur, self.trail_dur = bloom_dur, trail_dur
        rng = random.Random(seed)
        n_trails = max(2, min(3, n_trails))
        self.trails = [(cx + rng.randint(-14, 14), rng.uniform(40, 85), rng.uniform(1.5, 2.6))
                        for _ in range(n_trails)]

    def compose(self, frame: Image.Image, t: float) -> Image.Image:
        if t < self.drop_t:
            return frame
        out = frame.convert("RGB")
        arr = np.asarray(out, np.float32).copy()
        cx, cy = self.cx, self.cy
        h, w, _ = arr.shape
        p = _smootherstep((t - self.drop_t) / self.bloom_dur)

        y0, y1 = max(0, cy - 90), min(h, cy + 90)
        x0, x1 = max(0, cx - 90), min(w, cx + 90)
        if y1 > y0 and x1 > x0:
            ys, xs = np.mgrid[y0:y1, x0:x1]
            r = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
            R = 8 + 26 * p
            disc = np.clip((R - r) / 10.0, 0, 1)
            region = arr[y0:y1, x0:x1]
            blur = np.asarray(Image.fromarray(region.astype(np.uint8))
                               .filter(ImageFilter.GaussianBlur(2.2)), np.float32)
            region[:] = region * (1 - disc[..., None] * 0.5) + blur * (disc[..., None] * 0.5)
            region[:] *= (1.0 - 0.30 * p * disc)[..., None]

        pr = _smootherstep((t - self.drop_t - 0.25) / self.trail_dur)
        im2 = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGB")
        if pr > 0:
            d = ImageDraw.Draw(im2, "RGBA")
            for (tx, tlen, twid) in self.trails:
                ln = tlen * pr
                d.line([(tx, cy + 12), (tx, cy + 12 + ln)], fill=(58, 48, 40, 150), width=int(twid))
        return im2

    def foley_cues(self):
        """A single `ink_drop` one-shot at impact."""
        return [("ink_drop", self.drop_t, 0.3)]


# ---------------------------------------------------------------------- demo


def _render(name: str, frame_fn, dur: float, outdir: Path):
    work = outdir / f"_{name}_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    n = int(dur * FPS)
    for i in range(n):
        frame_fn(i / FPS).save(work / f"f{i:05d}.png")
    out = outdir / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out}")


def render_demo(still: Path, out_mp4: Path, duration: float):
    base = scale_crop(Image.open(still).convert("RGB"), W, H)
    entry = K.KeeperEntry(
        [("~~storm~~ ~~wind~~ fear.", 0, 0), ("water at our knees", 40, 100)],
        origin=(int(W * 0.36), int(H * 0.878)), size=64, energy=0.85, seed=41,
        t0=0.5, dur=2.2, skid=True)
    cx, cy = locate_word(entry, line_index=0, word="fear.")
    bleed = BleedingWord(cx, cy, drop_t=3.2, seed=21)

    def frame(t):
        out = entry.compose(base, t)
        return bleed.compose(out, t)

    _render(out_mp4.stem, frame, duration, out_mp4.parent)


# ------------------------------------------------------------------ selftest


def run_selftests() -> int:
    ok = True

    def check(cond, label):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {label}")
        ok = ok and cond

    # 1. locate_word finds a struck word by its bare text
    entry = K.KeeperEntry(
        [("~~storm~~ ~~wind~~ fear.", 0, 0)], origin=(100, 1700), size=64,
        energy=0.85, seed=41, t0=0.5, dur=2.2)
    cx, cy = locate_word(entry, 0, "fear.")
    check(cx > 100 and cy > 1700, f"locate_word found 'fear.' at ({cx},{cy}), right of origin")

    cx0, _ = locate_word(entry, 0, "storm")
    check(cx0 < cx, f"'storm' (first word, x={cx0}) sits left of 'fear.' (x={cx})")

    # 2. missing word raises
    try:
        locate_word(entry, 0, "nonexistent")
        check(False, "missing word raises ValueError")
    except ValueError:
        check(True, "missing word raises ValueError")

    # 3. no bleed before drop_t, frame changes at/after it
    base = Image.new("RGB", (W, H), (238, 226, 194))
    bleed = BleedingWord(400, 1000, drop_t=1.0, seed=21)
    before = np.asarray(bleed.compose(base, 0.5))
    after = np.asarray(bleed.compose(base, 1.5))
    check(np.array_equal(before, np.asarray(base)), "before drop_t, frame is unchanged")
    check(not np.array_equal(after, np.asarray(base)), "after drop_t, the bloom has darkened the region")

    # 4. foley cue is a single ink_drop one-shot at drop_t
    cues = bleed.foley_cues()
    check(cues == [("ink_drop", 1.0, 0.3)], f"foley_cues() is a single ink_drop at drop_t: {cues}")

    print(f"\n{'ALL PASS' if ok else 'FAILURES ABOVE'}")
    return 0 if ok else 1


# -------------------------------------------------------------------- CLI


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="render a demo clip from a still")
    ap.add_argument("--still", help="source still (--demo mode)")
    ap.add_argument("--out", help="output mp4 (--demo mode)")
    ap.add_argument("--duration", type=float, default=5.5, help="--demo clip length, seconds")
    ap.add_argument("--selftest", action="store_true", help="run the engine self-tests")
    a = ap.parse_args()

    if a.selftest:
        raise SystemExit(run_selftests())
    if a.demo:
        if not a.still or not a.out:
            ap.error("--demo requires --still and --out")
        render_demo(Path(a.still), Path(a.out), a.duration)
    else:
        ap.print_help()
