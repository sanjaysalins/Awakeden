#!/usr/bin/env python
"""Held Breath -- a pacing ENGINE, not a visual effect. Reads a narration's
word-alignment for real silences (gaps >= a threshold, default 0.35s) and
produces an energy(t) envelope in [floor, 1.0] that every other paper-layer
device (tide_mark, wash_creep, damp_cockle, raking_light, ...) multiplies its
own amplitude/advance/progress by. During a real silence the page goes
quiet -- motion damps toward the floor and eases back on the next word.
Never a true freeze (see Locked Lessons): a floor > 0 keeps grain-boil-class
life in the frame during the deepest part of a hold.

$0, deterministic. No image processing of its own -- pure function of time,
built from the alignment JSON already produced by veed_io/aligner.py.

Usage (library):
    from held_breath import energy_envelope
    energy = energy_envelope(words, total_duration=63.0)
    amp = base_amplitude * energy(t)   # multiply into ANY other device's params

Usage (demo/inspection):
    python held_breath.py --demo --align <alignment.json> --duration 63.0
        prints the detected gap table (matches the brief's own table format)
    python held_breath.py --demo-clip --still <png> --out <mp4> --align <alignment.json> --duration 8 --t0 8.5
        renders an 8s clip starting at t0=8.5s (straddling the "asleep." gap)
        showing damp_cockle's amplitude WITH and WITHOUT Held Breath modulation,
        side by side, so the damping is visible in motion, not just in a table.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def _ease(t: float) -> float:
    """Smoothstep, 0..1 -> 0..1."""
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def find_gaps(words: list[dict], threshold: float = 0.35) -> list[tuple[float, float]]:
    """Return [(gap_start, gap_end), ...] for every silence >= threshold
    between consecutive aligned words. gap_start = prev word's end,
    gap_end = next word's start."""
    gaps = []
    for i in range(1, len(words)):
        g0 = words[i - 1]["end"]
        g1 = words[i]["start"]
        if g1 - g0 >= threshold:
            gaps.append((g0, g1))
    return gaps


def energy_envelope(words: list[dict], total_duration: float, threshold: float = 0.35,
                     floor: float = 0.25, ramp: float = 0.15):
    """Returns a function energy(t) -> float in [floor, 1.0].

    1.0 during speech. For any gap >= threshold, eases down to `floor` over
    `ramp` seconds after the gap starts, holds at floor through the middle
    of the gap, eases back to 1.0 over `ramp` seconds before the gap ends.
    A gap shorter than 2*ramp still dips (proportionally less deep) rather
    than being skipped -- there is no silent gap this envelope ignores.
    """
    gaps = find_gaps(words, threshold)

    def energy(t: float) -> float:
        if t < 0 or t > total_duration:
            return 1.0
        for g0, g1 in gaps:
            if g0 <= t <= g1:
                span = g1 - g0
                r = min(ramp, span / 2)  # shrink the ramp on very short gaps
                if t < g0 + r:
                    k = _ease((t - g0) / r) if r > 0 else 1.0
                    return 1.0 - k * (1.0 - floor)
                if t > g1 - r:
                    k = _ease((g1 - t) / r) if r > 0 else 1.0
                    return 1.0 - k * (1.0 - floor)
                return floor
        return 1.0

    return energy


def _print_gap_table(words, total_duration, threshold):
    gaps = find_gaps(words, threshold)
    print(f"[held-breath] {len(gaps)} gap(s) >= {threshold}s in a {total_duration}s narration:\n")
    print(f"{'gap':>14} {'len':>6}  after / before")
    for g0, g1 in sorted(gaps, key=lambda g: g[1] - g[0], reverse=True):
        # find the surrounding words for context
        before = next((w["w"] for w in words if abs(w["end"] - g0) < 1e-6), "?")
        after = next((w["w"] for w in words if abs(w["start"] - g1) < 1e-6), "?")
        print(f"{g0:6.2f}-{g1:5.2f} {g1-g0:5.2f}s  after \"{before}\" before \"{after}\"")


def _demo_clip(args):
    from PIL import Image
    sys.path.insert(0, str(HERE))
    import damp_cockle  # sibling device, used purely as a demonstration modulation target

    words = json.load(open(args.align, encoding="utf-8"))
    energy = energy_envelope(words, args.duration_total, floor=0.2, ramp=0.15)

    still = Image.open(args.still).convert("RGB")
    base = damp_cockle.scale_crop(still, 1080, 1920) if hasattr(damp_cockle, "scale_crop") else still
    W, H = base.size

    work = Path(args.out).parent / (Path(args.out).stem + "_work")
    work.mkdir(parents=True, exist_ok=True)
    n = int(args.duration * 30)
    for i in range(n):
        t_local = i / 30
        t_global = args.t0 + t_local
        e = energy(t_global)
        left = damp_cockle.apply_damp_cockle(base.copy(), t=t_global, amplitude=1.0)       # unmodulated
        right = damp_cockle.apply_damp_cockle(base.copy(), t=t_global, amplitude=e)         # Held-Breath modulated
        combo = Image.new("RGB", (W * 2 + 8, H), (20, 20, 20))
        combo.paste(left, (0, 0))
        combo.paste(right, (W + 8, 0))
        combo = combo.resize((W, H // 1))  # keep height, just for a compact side-by-side preview
        combo.save(work / f"f{i:05d}.png")
    subprocess.run(["ffmpeg", "-y", "-framerate", "30", "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(args.out)], check=True)
    print(f"[ok] {args.out}  (left=unmodulated amplitude, right=Held-Breath-damped, "
          f"window t={args.t0:.2f}-{args.t0 + args.duration:.2f}s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="print the gap table")
    ap.add_argument("--demo-clip", action="store_true", help="render a comparison clip")
    ap.add_argument("--align", help="path to *_alignment.json")
    ap.add_argument("--duration", type=float, default=8.0, help="demo-clip render length")
    ap.add_argument("--duration-total", type=float, default=None,
                     help="total narration duration (for --demo table / envelope); "
                          "defaults to the last word's end time")
    ap.add_argument("--threshold", type=float, default=0.35)
    ap.add_argument("--still", help="still png for --demo-clip")
    ap.add_argument("--out", help="output mp4 for --demo-clip")
    ap.add_argument("--t0", type=float, default=0.0, help="start timestamp (global, seconds) for --demo-clip")
    a = ap.parse_args()

    words = json.load(open(a.align, encoding="utf-8")) if a.align else []
    total = a.duration_total or (words[-1]["end"] + 3.0 if words else 0.0)

    if a.demo:
        _print_gap_table(words, total, a.threshold)
    elif a.demo_clip:
        _demo_clip(a)
    else:
        ap.print_help()
