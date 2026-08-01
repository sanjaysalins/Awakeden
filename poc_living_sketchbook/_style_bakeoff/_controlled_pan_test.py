"""Controlled-camera test for Style 3 (Scholar's Margin) -- proves the intended motion
language for this style: a deterministic $0 camera move over the static diagram, NEVER
generative animation (which would garble the baked lettering). Same smootherstep-eased
crop+resize technique already proven in this repo (Storm's s13 landing push-in, mapengine's
Voyage Camera) -- no new dependency, no AI call.

Reading-order pan: open close on the OT type (the serpent) -> glide right across the arrow
to the NT fulfilment (the cross) -> pull back to the full two-panel comparison, wide, holding
on both labels legible.
"""
import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "style3_margin_typology.png"
OUT_FRAMES = HERE / "_pan_frames"
OUT_MP4 = HERE / "style3_controlled_pan_test.mp4"

W, H = 1080, 1920
FPS = 30
DUR = 5.5


def ease(t: float) -> float:
    return t * t * (3 - 2 * t)


# Keyframes: (t, cx_frac, cy_frac, zoom) -- cx/cy as fraction of source image, zoom 1.0 = full frame
KEYFRAMES = [
    (0.00, 0.20, 0.42, 1.85),   # close on the serpent/pole
    (0.35, 0.20, 0.42, 1.85),   # hold
    (0.72, 0.62, 0.35, 1.85),   # glide right across the arrow to the cross
    (1.00, 0.50, 0.50, 1.00),   # pull back to the full wide comparison
]


def camera_at(t_frac: float):
    for (t0, cx0, cy0, z0), (t1, cx1, cy1, z1) in zip(KEYFRAMES, KEYFRAMES[1:]):
        if t0 <= t_frac <= t1:
            local = 0.0 if t1 == t0 else (t_frac - t0) / (t1 - t0)
            k = ease(local)
            cx = cx0 + (cx1 - cx0) * k
            cy = cy0 + (cy1 - cy0) * k
            # log-space zoom interpolation (Voyage Camera technique) for constant-feel speed
            import math
            z = math.exp(math.log(z0) + (math.log(z1) - math.log(z0)) * k)
            return cx, cy, z
    return KEYFRAMES[-1][1], KEYFRAMES[-1][2], KEYFRAMES[-1][3]


def main():
    src = Image.open(SRC).convert("RGB")
    sw, sh = src.size
    # supersample the source once for zoom headroom (Voyage Camera lesson)
    super_scale = 2.0
    src_big = src.resize((int(sw * super_scale), int(sh * super_scale)), Image.LANCZOS)
    bw, bh = src_big.size

    if OUT_FRAMES.exists():
        for f in OUT_FRAMES.glob("*.png"):
            f.unlink()
    OUT_FRAMES.mkdir(exist_ok=True)

    n_frames = int(DUR * FPS)
    target_aspect = W / H
    for i in range(n_frames):
        t_frac = i / (n_frames - 1)
        cx_f, cy_f, zoom = camera_at(t_frac)
        cx, cy = cx_f * bw, cy_f * bh
        # crop window sized so its aspect matches output, scaled by zoom (bigger zoom = smaller crop)
        crop_h = bh / zoom
        crop_w = crop_h * target_aspect
        x0 = max(0, min(bw - crop_w, cx - crop_w / 2))
        y0 = max(0, min(bh - crop_h, cy - crop_h / 2))
        frame = src_big.crop((x0, y0, x0 + crop_w, y0 + crop_h)).resize((W, H), Image.LANCZOS)
        frame.save(OUT_FRAMES / f"f{i:05d}.png")

    subprocess.run(
        ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(OUT_FRAMES / "f%05d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), str(OUT_MP4)],
        check=True, capture_output=True)
    for f in OUT_FRAMES.glob("*.png"):
        f.unlink()
    OUT_FRAMES.rmdir()
    print(f"[ok] {OUT_MP4}")


if __name__ == "__main__":
    main()
