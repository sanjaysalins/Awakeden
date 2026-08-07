"""hunt_and_lock.py -- promoted from poc_living_sketchbook/jericho/_j5_assemble.py's
hunt_frame()/marker_ellipse() (Round 9, proven on Jericho's cord-in-the-wall
reveal). Generalized into a shared $0 device: a drift -> hunt -> lock camera
move that finds a named point in a still and circles it with a hand-drawn
marker ellipse. Promoted specifically because the Seed of the Woman LONG
independent-review panel (2026-08-07) caught it being planned as "the
device's literal design case" while it only existed as one-off episode-local
code -- same class of gap the retrospective this episode is proving exists
to catch.

  .venv\\Scripts\\python.exe panel_animator/hunt_and_lock.py <still.png> <out.mp4> <duration> <fx> <fy> [W] [H]
"""
import math
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

FPS = 30
UPSCALE = 1.6
SCARLET = (168, 34, 34)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def scale_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def marker_ellipse(frame: Image.Image, cx, cy, rx, ry, prog, width=7, seed=31) -> None:
    if prog <= 0:
        return
    d = ImageDraw.Draw(frame)
    rng = random.Random(seed)
    n = int(72 * min(1.0, prog))
    pts = []
    for i in range(n + 1):
        a = -math.pi / 2 + i / 72 * 2 * math.pi * 1.04
        pts.append((cx + (rx + rng.uniform(-3, 3)) * math.cos(a),
                    cy + (ry + rng.uniform(-3, 3)) * math.sin(a)))
    if len(pts) > 1:
        d.line(pts, fill=SCARLET, width=width, joint="curve")


def hunt_frame(big: Image.Image, t_rel: float, dur: float, target_frac: tuple[float, float],
               W: int, H: int, marker_rx: float, marker_ry: float) -> Image.Image:
    """target_frac = (fx, fy), 0..1 fraction of the UPSCALED canvas where the hunt
    locks. Three phases (drift/hunt/lock), identical math to the proven Jericho
    original -- only the hardcoded window position became a parameter."""
    bw, bh = big.size
    wx, wy = target_frac[0] * bw, target_frac[1] * bh
    p1, p2 = 0.45, 0.75
    k = t_rel / dur
    if k < p1:
        kk = ease(k / p1)
        cx = bw * 0.35 + (bw * 0.55 - bw * 0.35) * kk
        cy = bh * 0.62 - (bh * 0.62 - bh * 0.45) * kk
        z = 1.0
    elif k < p2:
        kk = ease((k - p1) / (p2 - p1))
        cx = bw * 0.55 + (wx - bw * 0.55) * kk
        cy = bh * 0.45 + (wy - bh * 0.45) * kk
        z = 1.0 + 0.5 * kk
    else:
        kk = ease((k - p2) / (1 - p2))
        cx, cy = wx, wy
        z = 1.5 + 0.9 * kk
    vw, vh = int(W / z), int(H / z)
    x0 = max(0, min(bw - vw, int(cx - vw / 2)))
    y0 = max(0, min(bh - vh, int(cy - vh / 2)))
    frame = big.crop((x0, y0, x0 + vw, y0 + vh)).resize((W, H), Image.LANCZOS)
    lock_prog = 0.0 if k < p2 else (k - p2) / (1 - p2)
    if lock_prog > 0:
        sx = (wx - x0) / vw * W
        sy = (wy - y0) / vh * H
        marker_ellipse(frame, sx, sy, marker_rx, marker_ry, lock_prog)
    return frame


def render(still_path: Path, dest_path: Path, duration: float, target_frac: tuple[float, float],
           W: int = 1920, H: int = 1080, marker_rx: float = 130, marker_ry: float = 170) -> None:
    src = Image.open(still_path).convert("RGB")
    big = scale_crop(src, int(W * UPSCALE), int(H * UPSCALE))
    n_frames = int(round(duration * FPS))
    proc = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "fast", str(dest_path)],
        stdin=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    try:
        for i in range(n_frames):
            frame = hunt_frame(big, i / FPS, duration, target_frac, W, H, marker_rx, marker_ry)
            proc.stdin.write(np.asarray(frame, dtype=np.uint8).tobytes())
    finally:
        proc.stdin.close()
        _, err = proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(f"hunt_and_lock ffmpeg encode failed:\n{err.decode(errors='replace')[-2000:]}")


if __name__ == "__main__":
    still, out, dur, fx, fy = sys.argv[1:6]
    W = int(sys.argv[6]) if len(sys.argv) > 6 else 1920
    H = int(sys.argv[7]) if len(sys.argv) > 7 else 1080
    render(Path(still), Path(out), float(dur), (float(fx), float(fy)), W, H)
    print(f"[ok] {out}")
