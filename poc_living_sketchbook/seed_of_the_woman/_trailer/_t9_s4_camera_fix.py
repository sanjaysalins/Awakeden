"""S4 redo ($0): Kling v1 pushed the camera in far tighter than asked AND
changed Eve's expression (mouth opened) despite an explicit "hold exact
expression" instruction -- same class of failure as S3's rejected v1.
Replaces it with a $0 hunt_and_lock push over the ALREADY-APPROVED still,
gentle and centered between the figures and the light (not a tight face
crop), so both faces stay fully visible and byte-identical throughout."""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\panel_animator")
import hunt_and_lock  # noqa: E402

W, H, FPS = 1920, 1080, 30
DURATION = 4.0
HERE = Path(__file__).resolve().parent
still = HERE / "stills" / "t_s4_hiding_light.png"
dest = HERE / "clips" / "t_s4_hiding_light_camerafix.mp4"

target_frac = (0.62, 0.45)  # gentle push toward the figures+light, not a tight face crop
src = Image.open(still).convert("RGB")
big = hunt_and_lock.scale_crop(src, int(W * 1.35), int(H * 1.35))  # gentler upscale than UPSCALE=1.6, less aggressive push
bw, bh = big.size
n = int(round(DURATION * FPS))

proc = subprocess.Popen(
    ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
     "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
     "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast", str(dest)],
    stdin=subprocess.PIPE, stderr=subprocess.PIPE,
)
try:
    for i in range(n):
        t = i / FPS
        k = hunt_and_lock.ease(t / DURATION)
        cx = bw * 0.5 + (target_frac[0] * bw - bw * 0.5) * k
        cy = bh * 0.5 + (target_frac[1] * bh - bh * 0.5) * k
        z = 1.0 + 0.18 * k
        vw, vh = int(W / z), int(H / z)
        x0 = max(0, min(bw - vw, int(cx - vw / 2)))
        y0 = max(0, min(bh - vh, int(cy - vh / 2)))
        frame = big.crop((x0, y0, x0 + vw, y0 + vh)).resize((W, H), Image.LANCZOS)
        proc.stdin.write(np.asarray(frame, dtype=np.uint8).tobytes())
finally:
    proc.stdin.close()
    _, err = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg encode failed:\n{err.decode(errors='replace')[-2000:]}")
print(f"[done] {dest}")
