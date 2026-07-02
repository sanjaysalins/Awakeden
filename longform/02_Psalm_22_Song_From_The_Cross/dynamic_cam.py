#!/usr/bin/env python
"""Deterministic DYNAMIC camera moves for a flat inked comic panel — dimensional energy, ZERO morph.

The Kling clips only do gentle push/pull (safe but samey). Orbit/rotate on Kling REPAINTS flat art
(our veo/direct-Kling bake-offs: rotate-POV moves morph + invent). This gets the orbit/arc FEEL by
treating the still as a plane in 3D and moving a virtual camera over it — pure geometry (PIL
perspective per frame), so nothing is ever repainted. Faithful by construction.

Moves:
  arc      - camera yaws across the panel (a 3D pan) + slow push -> the flat art gains dimension
  swoop    - a diagonal craning push toward the focus with mild pitch
  push     - baseline (for the A/B) : straight zoom, the current look

  ...\\python.exe longform/02_Psalm_22_Song_From_The_Cross/dynamic_cam.py <slug> [--move arc] [--compare]
"""
import argparse, math, subprocess
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
POOL = HERE / "v1" / "visual_16x9_inked"
WORK = POOL / "_dyncam_work"; WORK.mkdir(parents=True, exist_ok=True)
OUT_W, OUT_H, FPS = 1920, 1080, 30         # full res
D = 3.2                                     # virtual camera distance (perspective strength)
COVER = 1.18                                # over-scale so a tilted plane always fills the frame


def _coeffs(dst, src):
    """8 perspective coeffs mapping OUTPUT quad (dst) -> INPUT quad (src), for PIL PERSPECTIVE."""
    A = []
    for (xd, yd), (xs, ys) in zip(dst, src):
        A.append([xd, yd, 1, 0, 0, 0, -xs * xd, -xs * yd])
        A.append([0, 0, 0, xd, yd, 1, -ys * xd, -ys * yd])
    A = np.array(A, dtype=float)
    b = np.array([c for pt in src for c in pt], dtype=float)
    return np.linalg.solve(A, b)


def _project(corner_xy, yaw, pitch, scale, focus):
    """Project a normalised plane corner (x,y in [-1,1]) through a yawed/pitched/scaled camera."""
    x, y = corner_xy
    # rotate the plane about the vertical axis (yaw) then the horizontal axis (pitch)
    xr = x * math.cos(yaw)
    zr = x * math.sin(yaw)
    yr = y * math.cos(pitch)
    zr += y * math.sin(pitch)
    denom = D - zr
    X = (xr * D / denom) * scale * COVER
    Y = (yr * D / denom) * scale * COVER
    # bias toward the focus point (focus in [0,1] image space -> [-1,1])
    X += (focus[0] * 2 - 1) * (scale - 1.0) * 0.6
    Y += (focus[1] * 2 - 1) * (scale - 1.0) * 0.6
    return X, Y


def render_move(still: Path, move: str, dur: float, focus, dest: Path) -> Path:
    src_img = Image.open(still).convert("RGB").resize((OUT_W, OUT_H), Image.LANCZOS)
    src_quad = [(0, 0), (OUT_W, 0), (OUT_W, OUT_H), (0, OUT_H)]
    corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    n = max(1, int(dur * FPS))
    frames_dir = WORK / f"{still.stem}_{move}_frames"; frames_dir.mkdir(exist_ok=True)
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0.0
        e = 0.5 - 0.5 * math.cos(math.pi * t)          # ease in-out 0..1
        if move == "arc":
            yaw = math.radians(7.0) * (2 * e - 1)       # sweep -7deg -> +7deg
            pitch, scale = 0.0, 1.0 + 0.10 * e
        elif move == "swoop":
            yaw = math.radians(4.0) * (2 * e - 1)
            pitch = math.radians(5.0) * (e - 0.5)       # slight craning pitch
            scale = 1.0 + 0.16 * e
        else:                                           # push (baseline)
            yaw = pitch = 0.0; scale = 1.0 + 0.12 * e
        proj = [_project(c, yaw, pitch, scale, focus) for c in corners]
        dst = [((X + 1) / 2 * OUT_W, (Y + 1) / 2 * OUT_H) for (X, Y) in proj]
        frame = src_img.transform((OUT_W, OUT_H), Image.PERSPECTIVE, _coeffs(dst, src_quad),
                                  Image.BICUBIC, fillcolor=(12, 10, 8))
        frame.save(frames_dir / f"f{i:04d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", str(frames_dir / "f%04d.png"), "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", str(dest)], check=True)
    return dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("--move", default="arc")
    ap.add_argument("--dur", type=float, default=5.0); ap.add_argument("--compare", action="store_true")
    a = ap.parse_args()
    still = POOL / f"{a.slug}.png"
    import json
    anc_p = POOL / f"{a.slug}.anchor.json"
    focus = json.loads(anc_p.read_text())["focus"] if anc_p.exists() else [0.5, 0.4]
    if a.compare:
        clips = [render_move(still, m, a.dur, focus, WORK / f"{a.slug}_{m}.mp4")
                 for m in ("push", "arc", "swoop")]
        # 1x3 side-by-side compare
        lab = WORK / "_labels.txt"
        cmd = ["ffmpeg", "-y", "-loglevel", "error"]
        for c in clips:
            cmd += ["-i", str(c)]
        fc = ("[0:v]drawtext=text='push (current)':x=10:y=10:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6[a];"
              "[1:v]drawtext=text='arc (new)':x=10:y=10:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6[b];"
              "[2:v]drawtext=text='swoop (new)':x=10:y=10:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6[c];"
              "[a][b][c]hstack=inputs=3[v]")
        out = POOL / f"_dyncam_compare_{a.slug}.mp4"
        cmd += ["-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out)]
        subprocess.run(cmd, check=True)
        print(f"DONE -> {out}\n  file:///{str(out).replace(chr(92),'/')}")
    else:
        out = render_move(still, a.move, a.dur, focus, POOL / f"_dyncam_{a.slug}_{a.move}.mp4")
        print(f"DONE -> {out}\n  file:///{str(out).replace(chr(92),'/')}")


if __name__ == "__main__":
    main()
