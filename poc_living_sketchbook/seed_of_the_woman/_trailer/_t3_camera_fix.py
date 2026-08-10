"""S3 redo ($0), v2 -- same design as v1 (hunt_and_lock tracking push, no
marker, over the already-approved running still) but piping raw frames
directly to ffmpeg via stdin instead of writing individual PNGs to disk --
v1 was writing ~4MB PNGs one at a time and was still on frame 39/120 after
several minutes; the raw-pipe pattern (same as hunt_and_lock.render()
itself) is the proven-fast method used everywhere else in this project."""
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
still = HERE / "stills" / "t_s3_running.png"
dest = HERE / "clips" / "t_s3_running_camerafix.mp4"

target_frac = (0.50, 0.45)  # between the two figures, chest-height
src = Image.open(still).convert("RGB")
big = hunt_and_lock.scale_crop(src, int(W * hunt_and_lock.UPSCALE), int(H * hunt_and_lock.UPSCALE))
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
        x0, y0, vw, vh, _lock_prog, _wxy = hunt_and_lock.hunt_window(bw, bh, t, DURATION, target_frac, W, H)
        frame = big.crop((x0, y0, x0 + vw, y0 + vh)).resize((W, H), Image.LANCZOS)
        proc.stdin.write(np.asarray(frame, dtype=np.uint8).tobytes())
finally:
    proc.stdin.close()
    _, err = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg encode failed:\n{err.decode(errors='replace')[-2000:]}")
print(f"[done] {dest}")
