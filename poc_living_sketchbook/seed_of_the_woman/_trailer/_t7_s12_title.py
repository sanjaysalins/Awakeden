"""S12 ($0): the title card -- "The Seed of the Woman" arrives WHOLE (LAW
1, not letter-by-letter), $0 hand-lettering over the film's own "eden to
cross" hero still (not a blank card -- the same image the montage lands
on, so the cut into the title is a continuation, not a jump to black),
with a gold underline flare, then a still hold before the hard cut into
the film's own s01 opening."""
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
DURATION = 2.6
HERE = Path(__file__).resolve().parent
dest = HERE / "clips" / "t_s12_title.mp4"
BG_STILL = HERE.parent / "stills" / "s45_eden_to_cross.png"

F_KEEPER = "C:/Windows/Fonts/Inkfree.ttf"
GOLD = (185, 146, 74)
INK = (238, 224, 200)  # light ink, held legible by the scrim below

# the film's own eden-to-cross still, cover-scaled + center-cropped to
# 1920x1080 (same convention as every other trailer beat), then a dark
# vertical scrim (strongest across the text band, fading at top/bottom)
# so the hand-lettering stays legible without hiding the art
still = Image.open(BG_STILL).convert("RGB")
sw, sh = still.size
scale = max(W / sw, H / sh)
still = still.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
sw, sh = still.size
left, top = (sw - W) // 2, (sh - H) // 2
still = still.crop((left, top, left + W, top + H))

scrim = np.zeros((H, W), dtype=np.float32)
yy = np.arange(H)
band_center, band_half = H * 0.5, H * 0.30
falloff = np.clip(1.0 - np.abs(yy - band_center) / band_half, 0.0, 1.0) ** 1.4
scrim[:, :] = falloff[:, None] * 0.62
scrim_rgba = np.zeros((H, W, 4), dtype=np.uint8)
scrim_rgba[..., 3] = (scrim * 255).astype(np.uint8)
scrim_img = Image.fromarray(scrim_rgba, mode="RGBA")
base = still.convert("RGBA")
base.alpha_composite(scrim_img)
base = base.convert("RGB")

font = ImageFont.truetype(F_KEEPER, 118)
text = "The Seed of the Woman"
probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
bbox = probe.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
tx, ty = (W - tw) // 2 - bbox[0], (H - th) // 2 - bbox[1] - 20

text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(text_layer)
d.text((tx, ty), text, font=font, fill=(*INK, 255), stroke_width=1, stroke_fill=(*INK, 255))

line_y = ty + th + 55
line_x0, line_x1 = tx - 10, tx + tw + 10
gold_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(gold_layer)
gd.line([(line_x0, line_y), (line_x1, line_y)], fill=(*GOLD, 255), width=4)

n = int(round(DURATION * FPS))
frames = dest.parent / (dest.stem + "_frames")
frames.mkdir(parents=True, exist_ok=True)
title_in_end = 0.35
line_start, line_end = 0.35, 0.85
for i in range(n):
    t = i / FPS
    frame = base.convert("RGBA").copy()
    text_alpha = min(1.0, t / title_in_end)
    tl = text_layer.copy()
    tl.putalpha(tl.split()[3].point(lambda a, ta=text_alpha: int(a * ta)))
    frame.alpha_composite(tl)
    if t >= line_start:
        line_prog = min(1.0, (t - line_start) / (line_end - line_start))
        cur_x1 = int(line_x0 + (line_x1 - line_x0) * line_prog)
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gld = ImageDraw.Draw(gl)
        gld.line([(line_x0, line_y), (max(line_x0 + 1, cur_x1), line_y)], fill=(*GOLD, 255), width=4)
        frame.alpha_composite(gl)
    frame.convert("RGB").save(frames / f"f{i:05d}.png")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.png"),
                "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)], check=True)
import shutil
shutil.rmtree(frames)
print(f"[done] {dest}")
