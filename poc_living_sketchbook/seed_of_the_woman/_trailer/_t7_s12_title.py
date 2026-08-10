"""S12 ($0): the title card -- "The Seed of the Woman" arrives WHOLE (LAW
1, not letter-by-letter), $0 hand-lettering over dark aged paper, with a
gold underline flare, then a still hold before the hard cut into the
film's own s01 opening."""
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
DURATION = 2.6
HERE = Path(__file__).resolve().parent
dest = HERE / "clips" / "t_s12_title.mp4"

F_KEEPER = "C:/Windows/Fonts/Inkfree.ttf"
GOLD = (185, 146, 74)
INK = (238, 224, 200)  # light ink on dark paper

# dark aged-paper background (same tone family as the earlier overture work)
bg = np.full((H, W, 3), (18, 15, 13), dtype=np.uint8).astype(np.float32)
rng = np.random.default_rng(11)
bg += rng.normal(0, 2.2, (H, W, 1))
bg = bg.clip(0, 255).astype(np.uint8)
base = Image.fromarray(bg).convert("RGB")

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
