"""Animated comic-strip compositor (deterministic — no model, no hallucination).

Each panel = inked still + slow push-in + comic furniture that POPS IN forced-
aligned to the narration:
  - caption box  (parchment, top)  -> the NARRATOR's line
  - speech balloon (white, tail)    -> a quoted speaker's words (KJV red-letter)

Furniture is drawn in PIL and composited per-frame, NEVER baked into the AI image
(so the model can't garble the lettering — honours the 'never animate writing' rule).
Pop-in = scale 0.84 -> 1.04 -> 1.0 overshoot + alpha 0->1 over ~0.30s.
"""
from __future__ import annotations
import json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

S = Path(__file__).parent
FONT = r"C:\Windows\Fonts\comicbd.ttf"
INK = (20, 16, 10, 255)
W, H, FPS = 1440, 2560, 30          # work at native still size; encode downscales
POP = 0.30                          # pop-in duration (s)


# ---------- text helpers ----------
def _wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------- furniture: each returns a full-canvas RGBA layer + scale anchor ----------
def caption_layer(text, font_sz=58):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    font = ImageFont.truetype(FONT, font_sz)
    mx, top = 64, 70
    inner_w = W - 2 * mx - 64
    lines = _wrap(d, text.upper(), font, inner_w)
    lh = font_sz + 16
    box_h = len(lines) * lh + 48
    d.rounded_rectangle([mx, top, W - mx, top + box_h], radius=20,
                        fill=(245, 234, 208, 255), outline=INK, width=10)
    y = top + 24
    for ln in lines:
        d.text((mx + 32, y), ln, font=font, fill=INK); y += lh
    anchor = (W // 2, top)                       # grow downward from the top edge
    return layer, anchor


def balloon_layer(text, center, tail_to, w, font_sz=56):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    font = ImageFont.truetype(FONT, font_sz)
    lines = _wrap(d, text, font, w - 80)
    lh = font_sz + 14
    h = len(lines) * lh + 64
    cx, cy = center
    box = [cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2]
    bx, by = (box[0] + box[2]) // 2, box[1]       # tail leaves top-centre
    d.polygon([(bx - 52, by + 12), (bx + 52, by + 12), tail_to], fill=(251, 251, 246, 255))
    d.line([(bx - 52, by + 12), tail_to, (bx + 52, by + 12)], fill=INK, width=9, joint="curve")
    d.rounded_rectangle(box, radius=64, fill=(251, 251, 246, 255), outline=INK, width=9)
    y = box[1] + 32
    for ln in lines:
        tw = d.textlength(ln, font=font)
        d.text(((box[0] + box[2]) / 2 - tw / 2, y), ln, font=font, fill=INK); y += lh
    return layer, center


def _ease_pop(p):
    """0..1 -> scale with slight overshoot, plus alpha (0..1)."""
    if p >= 1.0:
        return 1.0, 1.0
    a = p                                         # alpha linear
    s = 0.84 + (1.04 - 0.84) * (1 - (1 - p) ** 2)
    if p > 0.8:
        s = 1.04 + (1.0 - 1.04) * ((p - 0.8) / 0.2)
    return s, a


def _paste_furniture(frame, layer, anchor, scale, alpha):
    if alpha <= 0:
        return frame
    if scale != 1.0:
        sw, sh = int(W * scale), int(H * scale)
        scaled = layer.resize((sw, sh), Image.LANCZOS)
        ax, ay = anchor
        ox, oy = int(ax * (1 - scale)), int(ay * (1 - scale))
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        canvas.paste(scaled, (ox, oy), scaled)
        layer = canvas
    if alpha < 1.0:
        r, g, b, a = layer.split()
        a = a.point(lambda v: int(v * alpha))
        layer = Image.merge("RGBA", (r, g, b, a))
    frame.alpha_composite(layer)
    return frame


def encode(frames, out, audio=None, ss=None, t=None, out_w=1080, out_h=1920):
    raw = S / "_frames"
    raw.mkdir(exist_ok=True)
    for f in raw.glob("*.png"):
        f.unlink()
    for i, fr in enumerate(frames):
        fr.save(raw / f"{i:04d}.png")
    silent = S / "_silent.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", str(raw / "%04d.png"), "-vf", f"scale={out_w}:{out_h}",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                    "-preset", "medium", str(silent)], check=True)
    if audio:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent)]
        cmd += ["-ss", str(ss), "-t", str(t), "-i", str(audio)] if ss is not None else ["-i", str(audio)]
        cmd += ["-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                "-b:a", "192k", "-shortest", str(out)]
        subprocess.run(cmd, check=True)
    else:
        silent.replace(out)
    print("wrote", out)
