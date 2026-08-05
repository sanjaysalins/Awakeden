#!/usr/bin/env python
"""Through-the-Object Cut -- the cut itself preaches the connection. Adapted
from ArkAIology's `visual_bakeoff/iris_mask.py::radial_iris()` (a sibling
project's own $0 deterministic primitive), but the centre is placed on a
MEANINGFUL DRAWN ELEMENT of the outgoing scene that the incoming scene
fulfils or echoes -- the growing circle opens exactly where that element
sits, so scene B visibly arrives THROUGH scene A's own content, not through
an arbitrary point. The feathered edge is additionally run through
ink_transition.py's own organic noise field (the same reveal-field
generator behind the approved blot/wipe transitions) instead of a plain
Gaussian-blurred circle, so it reads as a wet wash blooming from that
element rather than a clean lens iris -- staying inside this project's own
ink vocabulary rather than importing a foreign "camera iris" look.

No camera movement, no repaint of either still -- a pure radial + noise-
field alpha mask, deterministic.

Usage:
    python through_object_cut.py --a stillA.png --b stillB.png --out clip.mp4 \\
        --center 0.62,0.30 [--duration 1.6]
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ink_transition import make_reveal_field  # noqa: E402  -- reuse the approved organic noise field

FPS = 30
W, H = 1920, 1080


def _ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def _scale_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def render(still_a: Path, still_b: Path, out_mp4: Path, center: tuple, duration: float = 1.6,
           feather: int = 40, edge_weight: float = 0.35, w: int = W, h: int = H):
    a = _scale_crop(Image.open(still_a).convert("RGB"), w, h)
    b = _scale_crop(Image.open(still_b).convert("RGB"), w, h)

    cx, cy = center[0] * w, center[1] * h
    max_r = (w ** 2 + h ** 2) ** 0.5

    # organic noise field, blended with the radial distance from the chosen
    # anchor point so the growing edge is mottled/wet-looking (ink_transition's
    # own vocabulary) rather than a razor-clean circle.
    noise_field = make_reveal_field("blot", (center[0], center[1]), w=w, h=h)
    yy, xx = np.mgrid[0:h, 0:w]
    radial = np.sqrt(((xx - cx) / w) ** 2 + ((yy - cy) / h) ** 2)
    radial = (radial - radial.min()) / (radial.max() - radial.min())
    combined = edge_weight * noise_field + (1 - edge_weight) * radial
    combined = (combined - combined.min()) / (combined.max() - combined.min())

    work = out_mp4.parent / (out_mp4.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n = max(1, int(round(duration * FPS)))
    for i in range(n):
        t = _ease(i / max(1, n - 1))
        edge = feather / max_r
        mask = np.clip((t - (combined - edge)) / (2 * edge), 0, 1)
        mask_img = Image.fromarray((mask * 255).astype(np.uint8), "L")
        frame = Image.composite(b, a, mask_img)
        frame.save(work / f"f{i:04d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%04d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--center", required=True, help="x,y fractions of frame")
    ap.add_argument("--duration", type=float, default=1.6)
    a = ap.parse_args()
    cx, cy = (float(v) for v in a.center.split(","))
    render(Path(a.a), Path(a.b), Path(a.out), (cx, cy), a.duration)
