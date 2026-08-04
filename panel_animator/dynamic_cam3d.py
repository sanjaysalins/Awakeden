"""Dynamic Cam 3D -- deterministic orbit/arc/swoop camera moves on a single
flat still, with ZERO repaint risk. Ported from two per-episode copies
(longform/04_The_Bronze_Serpent/dynamic_cam.py, .../02_Psalm_22.../dynamic_cam.py)
into one shared, project-agnostic module.

Why this exists: Kling/veo "orbit"/"rotate" moves on flat 2D art actually
REPAINT the image to fake the new angle -- our own bake-offs found this
morphs faces and invents detail. This gets the orbit/arc/swoop FEEL by
treating the still as a rigid plane floating in 3D and moving a virtual
camera over it (pure PIL PERSPECTIVE transform, one homography per frame).
Nothing is ever regenerated, so nothing can be invented, garbled, or grown
that wasn't in the original still -- the technique is faithful by
construction, not by prompting. Use this INSTEAD of a generative clip
whenever a spread's own content makes prompt-locking risky (a figure that
keeps drifting/animating despite "hold perfectly still" instructions, a
wide/aerial composition that would read better as a real camera move than
frozen-with-ambient-dust) rather than spending another generative attempt
fighting the same invention risk.

First fix use: `poc_living_sketchbook/day_of_atonement`'s s53 crucifixion
clip kept animating the robe (billowing/swinging) despite three tightened
Seedance prompts -- swapped to `arc` here instead of a 4th generative
attempt, since the failure mode (unwanted body/garment motion) can't
recur when nothing is being regenerated at all.

Moves:
  arc      - camera yaws across the plane (a 3D pan) + slow push -- the
             orbit-around-the-subject feel, no morph
  swoop    - a diagonal craning push toward the focus with mild pitch
  push     - baseline straight zoom (no yaw/pitch) -- the "boring" case,
             kept for A/B comparison, not usually the final pick
  tour     - hard-cut gallery framings (full -> punch -> lateral -> full)
             with a micro push inside each shot
  parallax - 2.5D depth: rembg cuts the nearest subject, background pushes
             slowly, foreground pushes more + counter-drifts -- real depth
             from one flat plate

$0 every run: PIL/numpy geometry + ffmpeg encode. `parallax`/`tour`'s rembg
step downloads a small model on first use, then is local/free.

Usage:
    from dynamic_cam3d import render_move
    render_move(Path("stills/s53.png"), "arc", duration=4.0, focus=(0.5, 0.35),
                dest=Path("clips/s53.mp4"))

    # amp scales the move's intensity (1.0 = the tuned default; 0.6 = gentler)
    render_move(still, "swoop", 4.0, (0.5, 0.4), dest, amp=0.8)
"""
from __future__ import annotations
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

OUT_W, OUT_H, FPS = 1920, 1080, 30
D = 3.2       # virtual camera distance (perspective strength)
COVER = 1.18  # over-scale so a tilted plane always fills the frame


def _coeffs(dst, src):
    """8 perspective coeffs mapping OUTPUT quad (dst) -> INPUT quad (src)."""
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
    xr = x * math.cos(yaw)
    zr = x * math.sin(yaw)
    yr = y * math.cos(pitch)
    zr += y * math.sin(pitch)
    denom = D - zr
    X = (xr * D / denom) * scale * COVER
    Y = (yr * D / denom) * scale * COVER
    X += (focus[0] * 2 - 1) * (scale - 1.0) * 0.6
    Y += (focus[1] * 2 - 1) * (scale - 1.0) * 0.6
    return X, Y


def _ease(t: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))


def _encode(frames_dir: Path, dest: Path) -> Path:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", str(frames_dir / "f%04d.png"), "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", str(dest)], check=True)
    return dest


def _tour_shots(still: Path, focus):
    """Hard-cut framings for a gallery tour. A `<still>.tour.json` sidecar
    (list of [fx,fy,zoom]) wins; else auto-derive full->punch->lateral->full."""
    import json
    tp = still.with_name(still.stem + ".tour.json")
    if tp.exists():
        return [tuple(s) for s in json.loads(tp.read_text())]
    fx, fy = focus
    lx = min(0.82, max(0.18, fx + 0.20))
    return [(0.5, 0.46, 1.0), (fx, fy, 2.0), (lx, fy, 1.9), (0.5, 0.46, 1.0)]


def _render_tour(still: Path, dur: float, focus, dest: Path, work: Path) -> Path:
    img = Image.open(still).convert("RGB").resize((OUT_W, OUT_H), Image.LANCZOS)
    shots = _tour_shots(still, focus)
    n = max(1, int(dur * FPS))
    per = max(1, int(1.25 * FPS))
    fd = work / f"{still.stem}_tour_frames"
    fd.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        shot = min(len(shots) - 1, i // per)
        local = (i - shot * per) / per
        fx, fy, z0 = shots[shot]
        z = z0 * (1.0 + 0.05 * _ease(local))
        cw, ch = OUT_W / z, OUT_H / z
        cx, cy = fx * OUT_W, fy * OUT_H
        left = min(max(cx - cw / 2, 0), OUT_W - cw)
        top = min(max(cy - ch / 2, 0), OUT_H - ch)
        crop = img.crop((int(left), int(top), int(left + cw), int(top + ch))).resize((OUT_W, OUT_H), Image.LANCZOS)
        crop.save(fd / f"f{i:04d}.png")
    return _encode(fd, dest)


def _render_parallax(still: Path, dur: float, focus, dest: Path, work: Path) -> Path:
    from rembg import remove
    base_img = Image.open(still).convert("RGB").resize((OUT_W, OUT_H), Image.LANCZOS)
    cut = remove(base_img).convert("RGBA").resize((OUT_W, OUT_H), Image.LANCZOS)
    n = max(1, int(dur * FPS))
    fd = work / f"{still.stem}_parallax_frames"
    fd.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0.0
        e = _ease(t)
        bz = 1.0 + 0.06 * e
        bg = base_img.resize((int(OUT_W * bz), int(OUT_H * bz)), Image.LANCZOS)
        bdx = int((bg.width - OUT_W) * (0.5 + 0.08 * (e - 0.5) * 2))
        bdy = int((bg.height - OUT_H) * 0.5)
        frame = bg.crop((bdx, bdy, bdx + OUT_W, bdy + OUT_H)).convert("RGBA")
        fz = 1.0 + 0.14 * e
        fg = cut.resize((int(OUT_W * fz), int(OUT_H * fz)), Image.LANCZOS)
        fdx = int((fg.width - OUT_W) * focus[0] - OUT_W * 0.03 * (e - 0.5) * 2)
        fdy = int((fg.height - OUT_H) * focus[1])
        fdx = min(max(fdx, 0), fg.width - OUT_W)
        fdy = min(max(fdy, 0), fg.height - OUT_H)
        frame.alpha_composite(fg.crop((fdx, fdy, fdx + OUT_W, fdy + OUT_H)))
        frame.convert("RGB").save(fd / f"f{i:04d}.png")
    return _encode(fd, dest)


def render_move(still: Path, move: str, duration: float, focus: tuple[float, float],
                 dest: Path, amp: float = 1.0, work: Path | None = None) -> Path:
    """move: 'arc' | 'swoop' | 'push' | 'tour' | 'parallax'. focus: (x,y) in
    [0,1] image space, the point the move is biased toward/orbits around.
    amp scales arc/swoop/push intensity (1.0 = tuned default)."""
    work = work or dest.parent / "_dyncam_work"
    work.mkdir(parents=True, exist_ok=True)
    if move == "tour":
        return _render_tour(still, duration, focus, dest, work)
    if move == "parallax":
        return _render_parallax(still, duration, focus, dest, work)

    src_img = Image.open(still).convert("RGB").resize((OUT_W, OUT_H), Image.LANCZOS)
    src_quad = [(0, 0), (OUT_W, 0), (OUT_W, OUT_H), (0, OUT_H)]
    corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    n = max(1, int(duration * FPS))
    frames_dir = work / f"{still.stem}_{move}_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0.0
        e = _ease(t)
        if move == "arc":
            yaw = math.radians(7.0 * amp) * (2 * e - 1)
            pitch, scale = 0.0, 1.0 + 0.10 * amp * e
        elif move == "swoop":
            yaw = math.radians(4.0 * amp) * (2 * e - 1)
            pitch = math.radians(5.0 * amp) * (e - 0.5)
            scale = 1.0 + 0.16 * amp * e
        else:  # push
            yaw = pitch = 0.0
            scale = 1.0 + 0.12 * amp * e
        proj = [_project(c, yaw, pitch, scale, focus) for c in corners]
        dst = [((X + 1) / 2 * OUT_W, (Y + 1) / 2 * OUT_H) for (X, Y) in proj]
        frame = src_img.transform((OUT_W, OUT_H), Image.PERSPECTIVE, _coeffs(dst, src_quad),
                                   Image.BICUBIC, fillcolor=(12, 10, 8))
        frame.save(frames_dir / f"f{i:04d}.png")
    return _encode(frames_dir, dest)
