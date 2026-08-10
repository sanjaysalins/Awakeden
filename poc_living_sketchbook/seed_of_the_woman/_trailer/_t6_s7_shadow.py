"""S7 ($0): a shadow advancing over the motionless serpent, reusing the
EXACT shadow-sweep technique already proven in the main episode's
build_s55 (poc_living_sketchbook/seed_of_the_woman/_s6_assemble.py) --
never asks a paid animator to touch the serpent at all, guaranteeing zero
distortion/hallucination risk on the trailer's doctrinally sensitive beat."""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\panel_animator")
import hunt_and_lock  # noqa: E402 -- reused only for its ease() curve

W, H, FPS = 1920, 1080, 30
DURATION = 5.22  # measured directly via ffmpeg silencedetect on the real narration.mp3:
# segment 1 (narrator) ends at 13.829s, segment 3 (narrator) begins at
# 19.049s -- the GOD quote + its pre/post pauses fill exactly that gap
HERE = Path(__file__).resolve().parent
still = HERE / "stills" / "t_s7_serpent_shadow_base.png"
dest = HERE / "clips" / "t_s7_shadow_sweep.mp4"

base = Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS)
base_arr = np.asarray(base, dtype=np.float32)

# measured via bbox_sheet.py against the actual rendered still
shadow_source_frac = (0.85, 0.12)   # off-frame upper-right, where the shadow enters from
head_frac = (0.58, 0.635)           # the serpent's own head/neck position

sx, sy = shadow_source_frac[0] * W, shadow_source_frac[1] * H
hx, hy = head_frac[0] * W, head_frac[1] * H
yy, xx = np.mgrid[0:H, 0:W]
xx, yy = xx.astype(np.float32), yy.astype(np.float32)

n = max(1, int(round(DURATION * FPS)))
sweep_dur = DURATION * 0.75
radius = 150.0
frames = dest.parent / (dest.stem + "_frames")
frames.mkdir(parents=True, exist_ok=True)
for i in range(n):
    t = i / FPS
    k = hunt_and_lock.ease(min(1.0, t / sweep_dur))
    lead_x, lead_y = sx + (hx - sx) * k, sy + (hy - sy) * k
    dist = np.sqrt((xx - lead_x) ** 2 + (yy - lead_y) ** 2)
    darken = np.clip(1.0 - dist / radius, 0.0, 1.0) * 0.6 * k
    arr = base_arr * (1.0 - darken[..., None])
    Image.fromarray(arr.clip(0, 255).astype(np.uint8)).save(frames / f"f{i:05d}.png")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
                "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)], check=True)
import shutil
shutil.rmtree(frames)
print(f"[done] {dest}")
