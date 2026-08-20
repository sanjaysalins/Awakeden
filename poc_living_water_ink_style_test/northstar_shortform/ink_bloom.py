"""Live Ink Hold — a small, safe, MANUALLY-POINTED variant of the "the ink
keeps bleeding during the hold" idea Fable proposed. wash_creep's own
HSV-based color isolation was tried first and rejected: sampled directly
against this style's actual renders, the swirl's blue and Jesus's indigo
robe overlap heavily in hue (verified visually — a full HSV mask lit up the
robe, not the swirl, see northstar_shortform session notes). Rather than a
global color mask, this darkens/deepens a small soft radial zone AT A
MANUALLY-VERIFIED POINT inside the swirl (eyeballed per shot, well clear of
any robe/figure) — same underlying math as focal_tour's halo (a Gaussian
radial field), but multiplying toward a blue-ink tone instead of brightness.

$0, deterministic PIL/numpy. Not a claim of botanical/physical accuracy —
a controlled "the ink is still settling" pulse, capped small.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

INK_TONE = np.array([46.0, 74.0, 128.0])  # deep wet-ink blue, multiply target


def apply_ink_bloom(frame: Image.Image, cx_frac: float, cy_frac: float,
                     radius_frac: float, strength: float) -> Image.Image:
    """Darken/deepen a soft radial zone centered at (cx_frac, cy_frac) (0..1 of
    frame size) toward INK_TONE. strength in [0,1]: 0 = no-op, larger = the
    zone reads more like freshly-deepened wet ink. Keep strength small
    (<=0.35) — this is a pulse, not a repaint."""
    if strength <= 0.001:
        return frame.convert("RGB")
    rgb = frame.convert("RGB")
    w, h = rgb.size
    arr = np.asarray(rgb, dtype=np.float32)
    cx, cy = cx_frac * w, cy_frac * h
    radius = radius_frac * min(w, h)
    y_grid, x_grid = np.mgrid[0:h, 0:w].astype(np.float32)
    dist_sq = (x_grid - cx) ** 2 + (y_grid - cy) ** 2
    sigma = max(radius * 0.6, 1.0)
    field = np.exp(-dist_sq / (2.0 * sigma ** 2)) * strength
    field = field[..., None]
    out = arr * (1 - field) + INK_TONE[None, None, :] * field
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def render_hold(last_frame_png: Path, out_mp4: Path, duration: float,
                 cx_frac: float, cy_frac: float, radius_frac: float,
                 max_strength: float, energy_fn, t0_global: float,
                 w: int, h: int, fps: int = 30) -> None:
    """Render `duration` seconds of the ink-bloom hold, starting from a still
    frame, ease-in over the first ~45% then hold, modulated frame-by-frame by
    energy_fn(t_global) in [0,1] (held_breath's envelope)."""
    import subprocess
    base = Image.open(last_frame_png).convert("RGB")
    if base.size != (w, h):
        s = max(w / base.width, h / base.height)
        base = base.resize((int(base.width * s + 0.5), int(base.height * s + 0.5)), Image.LANCZOS)
        base = base.crop(((base.width - w) // 2, (base.height - h) // 2,
                          (base.width - w) // 2 + w, (base.height - h) // 2 + h))

    n = max(1, int(round(duration * fps)))
    work = out_mp4.parent / (out_mp4.stem + "_work")
    work.mkdir(parents=True, exist_ok=True)
    ramp_frac = 0.45
    for i in range(n):
        t_local = i / fps
        ramp = min(1.0, t_local / max(0.01, duration * ramp_frac))
        ramp = ramp * ramp * (3 - 2 * ramp)  # smoothstep
        e = energy_fn(t0_global + t_local)
        strength = max_strength * ramp * e
        frame = apply_ink_bloom(base, cx_frac, cy_frac, radius_frac, strength)
        frame.save(work / f"f{i:05d}.png")

    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-framerate", str(fps),
         "-i", str(work / "f%05d.png"),
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         str(out_mp4)],
        check=True,
    )
    for f in work.glob("*.png"):
        f.unlink()
    work.rmdir()
