"""vox-ghost POC: adapt ArkAIology's /vox-type "ghost" kinetic word into our own
visual language.

THEIR version (poc_living_sketchbook/_lettering_compare/ark_ref/ts1_20.png):
a giant word rendered as flat translucent/hollow-outline letters laid on top of
the scene -- a clean flat-vector graphic, letting the art show through evenly.
That flatness is exactly the "alien UI chip" quality the living-sketchbook
skill (.claude/skills/living-sketchbook/SKILL.md section 5) now forbids: every
letter must look HAND-MADE, pressed into the page, never a floating screen
element.

OUR version: the word reads as a wooden letterpress block PRESSED into damp
paper -- a shallow debossed impression, not a flat overlay. No new colour
fills the letter's middle; only two very soft rims do the work:
  - a warm highlight where the upper-facing surface of the impression
    catches the raking museum light (top edge of every stroke/counter)
  - a warm ink-shadow where it pools on the lower-facing surface
  - a faint warm ink-bleed halo just outside the letter, like a heavy press
    weeping slightly into the fibres
  - a very slight overall darken (10%) across the letter interior so it
    reads as a shallow depression -- the paper's own texture/colour still
    shows through, just a touch pressed-down
plus a very slight overall darken across the interior so the shape reads as
a depression while the paper's own grain and colour still show through.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_skill_adaptations/vox_ghost/_render.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
STILL = HERE.parents[1] / "jericho" / "stills" / "j07_trumpets.png"
OUT = HERE

W, H = 1080, 1920
F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"
WORD = "BELIEVED"

HIGHLIGHT = np.array([255, 248, 222], dtype=np.float32)  # warm paper catching light
SHADOW = np.array([48, 32, 20], dtype=np.float32)        # warm ink-dark shadow
HALO = np.array([132, 78, 46], dtype=np.float32)         # warm bled-ink brown


def base_canvas(path):
    """Same crop-to-fill pattern as _lettering_compare/_render_candidates.py."""
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))


def fit_font(word, target_w):
    size = 260
    bbox = None
    font = None
    tmp = Image.new("L", (10, 10))
    d = ImageDraw.Draw(tmp)
    while size > 60:
        font = ImageFont.truetype(F_ZILLA, size)
        bbox = d.textbbox((0, 0), word, font=font)
        if bbox[2] - bbox[0] <= target_w:
            return font, bbox
        size -= 4
    return font, bbox


def build_mask_patch(word, font, bbox, pad):
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    patch = Image.new("L", (bw + 2 * pad, bh + 2 * pad), 0)
    d = ImageDraw.Draw(patch)
    d.text((pad - bbox[0], pad - bbox[1]), word, font=font, fill=255)
    # letterpress into damp paper never leaves a razor edge
    patch = patch.filter(ImageFilter.GaussianBlur(0.9))
    return patch


def emboss_composite(canvas, word, cy, target_w_frac=0.84):
    target_w = int(W * target_w_frac)
    font, bbox = fit_font(word, target_w)
    pad = 46
    mask_patch = build_mask_patch(word, font, bbox, pad)
    pw, ph = mask_patch.size
    mask = np.array(mask_patch, dtype=np.float32) / 255.0

    dy = 7  # rim shift -- subtle, this is a SHALLOW impression
    up = np.roll(mask, -dy, axis=0)
    down = np.roll(mask, dy, axis=0)
    highlight_rim = np.clip(up - mask, 0.0, 1.0)
    shadow_rim = np.clip(down - mask, 0.0, 1.0)

    def soften(band, radius):
        img = Image.fromarray((band * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius))
        return np.array(img, dtype=np.float32) / 255.0

    highlight_rim = soften(highlight_rim, 2.4)
    shadow_rim = soften(shadow_rim, 2.4)

    # ink-bleed halo: dilate the mask outward, subtract the mask, blur heavily --
    # a ring "weeping" out past the impression on every side
    dilated = np.array(
        Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(13)),
        dtype=np.float32) / 255.0
    halo_ring = soften(np.clip(dilated - mask, 0.0, 1.0), 9)

    px = (W - pw) // 2
    py = int(cy - ph / 2)

    canvas_arr = np.array(canvas, dtype=np.float32)
    patch = canvas_arr[py:py + ph, px:px + pw, :]

    a = (halo_ring * 0.16)[..., None]
    patch[:] = patch * (1 - a) + HALO * a

    depress = (mask * 0.10)[..., None]
    patch[:] = patch * (1 - depress)

    a = (highlight_rim * 0.60)[..., None]
    patch[:] = patch * (1 - a) + HIGHLIGHT * a

    a = (shadow_rim * 0.55)[..., None]
    patch[:] = patch * (1 - a) + SHADOW * a

    canvas_arr[py:py + ph, px:px + pw, :] = patch
    return Image.fromarray(np.clip(canvas_arr, 0, 255).astype(np.uint8))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    canvas = base_canvas(STILL)
    canvas = emboss_composite(canvas, WORD, cy=H * 0.24)
    out_path = OUT / "ghost_believed.png"
    canvas.save(out_path)
    print(f"[ok] wrote {out_path}")


if __name__ == "__main__":
    main()
