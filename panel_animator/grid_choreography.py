#!/usr/bin/env python
"""Camera choreography across a live 2x2 grid -- instead of every panel just
looping independently in its fixed cell, a virtual "page camera" racks focus
toward whichever panel currently holds attention (slight push + brighten)
while the other three dim, then smoothly moves on to the next. Pure post-
process over already-rendered clips, no new generation.

$0, deterministic: PIL per-frame compositing + ffmpeg encode.

Usage:
    python grid_choreography.py --clips a.mp4 b.mp4 c.mp4 d.mp4 --out grid.mp4
        [--per-panel 1.2] [--transition 0.35]
"""
from __future__ import annotations
import argparse
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageEnhance

FPS = 30
W, H = 1920, 1080
CW, CH = W // 2, H // 2
CENTERS = [(CW // 2, CH // 2), (CW + CW // 2, CH // 2),
           (CW // 2, CH + CH // 2), (CW + CW // 2, CH + CH // 2)]  # TL,TR,BL,BR


def _probe_fps(clip: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", str(clip)],
        capture_output=True, text=True, check=True).stdout.strip()
    num, den = out.split("/")
    return float(num) / float(den)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def activeness(panel_i: int, t: float, per_panel: float, trans: float, n: int) -> float:
    """0..1 how 'in focus' panel_i is at time t, smoothly crossfading at boundaries."""
    cur = int(t // per_panel) % n
    frac = (t % per_panel) / per_panel
    local_trans = trans / per_panel
    if panel_i == cur:
        if frac < local_trans:
            return ease(0.5 + 0.5 * frac / local_trans)          # rising from prior cut
        if frac > 1 - local_trans:
            return ease(0.5 + 0.5 * (1 - frac) / local_trans)    # falling into next cut
        return 1.0
    nxt = (cur + 1) % n
    if panel_i == nxt and frac > 1 - local_trans:
        return ease(0.5 * (frac - (1 - local_trans)) / local_trans)
    prv = (cur - 1) % n
    if panel_i == prv and frac < local_trans:
        return ease(0.5 * (1 - frac / local_trans))
    return 0.0


def render(clips: list[Path], out_mp4: Path, per_panel: float, trans: float):
    fps = _probe_fps(clips[0])
    duration = per_panel * len(clips)
    n_frames = int(duration * fps)

    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    frame_dirs = []
    for i, c in enumerate(clips):
        d = work / f"src{i}"
        d.mkdir()
        subprocess.run(["ffmpeg", "-y", "-i", str(c), "-t", f"{duration:.3f}",
                        "-vf", f"scale={CW}:{CH}:force_original_aspect_ratio=increase,crop={CW}:{CH}",
                        "-r", str(fps), str(d / "f%05d.png")],
                       check=True, capture_output=True)
        frame_dirs.append(sorted(d.glob("f*.png")))

    out_dir = work / "grid_frames"
    out_dir.mkdir()
    n = len(clips)
    for i in range(n_frames):
        t = i / fps
        acts = [activeness(p, t, per_panel, trans, n) for p in range(n)]
        canvas = Image.new("RGB", (W, H))
        for p in range(n):
            src_frames = frame_dirs[p]
            cell = Image.open(src_frames[min(i, len(src_frames) - 1)]).convert("RGB")
            a = acts[p]
            bright = 0.45 + 0.55 * a
            cell = ImageEnhance.Brightness(cell).enhance(bright)
            cell = ImageEnhance.Contrast(cell).enhance(0.85 + 0.15 * a)
            if a > 0.02:
                zoom = 1.0 + 0.05 * a
                zw, zh = int(CW * zoom), int(CH * zoom)
                cell = cell.resize((zw, zh), Image.LANCZOS)
                cell = cell.crop(((zw - CW) // 2, (zh - CH) // 2,
                                   (zw - CW) // 2 + CW, (zh - CH) // 2 + CH))
            cx, cy = (p % 2) * CW, (p // 2) * CH
            canvas.paste(cell, (cx, cy))

        # virtual page camera: push toward the attention-weighted centroid
        tw = sum(acts) or 1.0
        fx = sum(a * c[0] for a, c in zip(acts, CENTERS)) / tw
        fy = sum(a * c[1] for a, c in zip(acts, CENTERS)) / tw
        cam_zoom = 1.10
        bigw, bigh = int(W * cam_zoom), int(H * cam_zoom)
        big = canvas.resize((bigw, bigh), Image.LANCZOS)
        sx = fx * cam_zoom - W / 2
        sy = fy * cam_zoom - H / 2
        sx = max(0, min(bigw - W, sx))
        sy = max(0, min(bigh - H, sy))
        frame = big.crop((int(sx), int(sy), int(sx) + W, int(sy) + H))
        frame.save(out_dir / f"g{i:05d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", str(out_dir / "g%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--clips", nargs=4, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--per-panel", type=float, default=1.2, dest="per_panel")
    ap.add_argument("--transition", type=float, default=0.35, dest="trans")
    a = ap.parse_args()
    render([Path(c) for c in a.clips], Path(a.out), a.per_panel, a.trans)
