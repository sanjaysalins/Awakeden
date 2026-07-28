"""ArkAIology skill-adaptation HONEST TEST: the 'flap' kinetic-word treatment
(/vox-type split-flap airport/train departure-board digits, used by
ArkAIology for day-counts like "DAY 4 OF 6") adapted into our
living-sketchbook palette.

This is a fairness test, not an endorsement -- the concern going in is that a
split-flap board is an unmistakably 20th-century mechanical object, which may
read as anachronistic pasted onto an ancient Bible setting. The adaptation
attempted here tries as hard as honestly possible to make it feel OLD/ANALOG
instead of modern:

  - the "flap" cells become individual CARVED WOODEN TILES (not plastic
    flip-cards) sitting in slots cut into a wooden frame/plank
  - each digit is rendered in ZillaSlab-Bold with the show's locked
    stamped-texture technique (alpha = glyph mask x blurred noise), PLUS a
    bas-relief shadow/highlight pass so it reads as gouged and pigment-rubbed
    rather than printed
  - the frame is a hand-wobbled rectangle in faded brown ink (same wobble
    technique as poc_living_sketchbook/_lettering_compare/_render_candidates.py
    render_current_hated()'s box border), filled with a grain-textured wood
    plank, corner pegs, and a lashed rope tie -- signalling hand-built object,
    not manufactured housing
  - each tile is independently rotated/offset a couple of degrees/pixels so
    the pair reads as two separate hand-made objects, not machine-uniform
    slots
  - the whole board is tilted and drop-shadowed as though genuinely propped
    in the scene, not a flat screen graphic

The word "LAPS" is rendered separately in the show's ALREADY-LOCKED INK STAMP
display-type technique (SKILL.md section 5) -- this test isolates the ONE
new device under test (the flap/tally board) rather than re-testing lettering
that's already decided.

Test content: "13 LAPS" -- Jericho's own march-count beat (Joshua 6, 13 total
circuits of the wall).

  .venv\\Scripts\\python.exe poc_living_sketchbook/_skill_adaptations/vox_flap/_render.py
"""
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
JERICHO = HERE.parents[1] / "jericho"
OUT = HERE
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920

INK = (35, 30, 26)
RUBRIC = (150, 26, 22)
CREAM = (238, 226, 194)
BROWN_INK = (94, 61, 33)          # faded brown ink -- the frame outline
WOOD_BASE = (150, 112, 68)        # plank / frame base tone
WOOD_TILE = (172, 132, 82)        # tile base tone (a shade lighter -- reads as a distinct inset object)
WOOD_DARK = (72, 48, 27)
WOOD_LIGHT = (198, 168, 118)

F_ZILLA_BOLD = "C:/Windows/Fonts/ZillaSlab-Bold.ttf"
F_ZILLA_SEMI = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"


# ============================================================ shared primitives (from _lettering_compare)
def base_canvas(still_path):
    im = Image.open(still_path).convert("RGB")
    s = max(W / im.width, H / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))


def wobbled_points(bbox, seed, jitter=3.0, n_per_edge=9):
    x0, y0, x1, y1 = bbox
    rng = random.Random(seed)
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    pts = []
    for (ax, ay), (bx, by) in zip(corners, corners[1:]):
        for i in range(n_per_edge):
            t = i / n_per_edge
            pts.append((ax + (bx - ax) * t + rng.uniform(-jitter, jitter),
                        ay + (by - ay) * t + rng.uniform(-jitter, jitter)))
    pts.append(pts[0])
    return pts


def wobbled_rect(draw, bbox, seed, jitter=3.0, width=4, color=BROWN_INK, n_per_edge=9):
    """Hand-drawn wobbled rectangle outline -- same technique as
    _lettering_compare/_render_candidates.py render_current_hated()'s box
    border, generalized into a reusable helper."""
    pts = wobbled_points(bbox, seed, jitter, n_per_edge)
    draw.line(pts, fill=(*color, 255), width=width, joint="curve")
    return pts


def stamped_alpha(text, font, seed, pad=16, stroke=2):
    """alpha = glyph mask x blurred noise -- the show's locked rough-pressed
    ink-stamp texture (see render_display_stamp in _render_candidates.py)."""
    tmp = Image.new("L", (10, 10))
    td = ImageDraw.Draw(tmp)
    bb = td.textbbox((0, 0), text, font=font, stroke_width=stroke)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    mask = Image.new("L", (tw + 2 * pad, th + 2 * pad), 0)
    md = ImageDraw.Draw(mask)
    md.text((pad - bb[0], pad - bb[1]), text, font=font, fill=255, stroke_width=stroke, stroke_fill=255)
    rng = random.Random(seed)
    noise = Image.new("L", mask.size)
    noise.putdata([rng.randint(50, 255) for _ in range(mask.size[0] * mask.size[1])])
    noise = noise.filter(ImageFilter.GaussianBlur(1.0))
    a = (np.array(mask).astype(float) / 255.0) * (np.array(noise).astype(float) / 255.0)
    a = np.clip(a * 1.6, 0, 1) * 255
    return Image.fromarray(a.astype("uint8")), mask


# ============================================================ new for this test: wood + carve
def wood_grain(size, seed, lo=100, hi=190):
    w, h = size
    rng = random.Random(seed)
    cols = max(1, w // 3)
    row = [rng.randint(lo, hi) for _ in range(cols)]
    strip = Image.new("L", (cols, 1))
    strip.putdata(row)
    strip = strip.resize((w, h), Image.BILINEAR)
    strip = strip.filter(ImageFilter.GaussianBlur(2.2))
    return strip


def wood_fill(size, base_color, seed):
    grain = wood_grain(size, seed)
    g = np.array(grain).astype(float) / 145.0  # ~0.7..1.3 multiplier
    base = np.array(Image.new("RGB", size, base_color)).astype(float)
    out = np.clip(base * g[..., None], 0, 255).astype("uint8")
    return Image.fromarray(out, "RGB")


def carved_glyph(text, font, seed, ink_color=INK):
    """Bas-relief carved-into-wood numeral: a recessed dark shadow + a warm
    light-catch on the upper-left lip + the rough stamped ink/pigment rubbed
    into the groove -- so it reads as gouged and painted, not printed."""
    alpha, mask = stamped_alpha(text, font, seed)
    w, h = alpha.size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (w, h), (*WOOD_DARK, 0))
    shadow.putalpha(mask.point(lambda v: int(v * 0.55)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(1.4))
    layer.alpha_composite(shadow, (2, 3))
    hi = Image.new("RGBA", (w, h), (*WOOD_LIGHT, 0))
    hi.putalpha(mask.point(lambda v: int(v * 0.42)))
    hi = hi.filter(ImageFilter.GaussianBlur(1.0))
    layer.alpha_composite(hi, (-2, -2))
    ink = Image.new("RGBA", (w, h), (*ink_color, 0))
    ink.putalpha(alpha)
    layer.alpha_composite(ink, (0, 0))
    return layer


def build_tile(ch, size, seed, rot_deg):
    w, h = size
    tile = wood_fill(size, WOOD_TILE, seed).convert("RGBA")
    d = ImageDraw.Draw(tile)
    wobbled_rect(d, (5, 5, w - 5, h - 5), seed + 1, jitter=2.2, width=3, color=WOOD_DARK)
    font = ImageFont.truetype(F_ZILLA_BOLD, int(h * 0.60))
    glyph = carved_glyph(ch, font, seed + 2)
    gx = (w - glyph.width) // 2
    gy = (h - glyph.height) // 2 - 6
    tile.alpha_composite(glyph, (gx, gy))
    return tile.rotate(rot_deg, expand=True, resample=Image.BICUBIC)


def build_board():
    tile_w, tile_h = 210, 300
    gap, pad = 24, 34
    frame_w = pad * 2 + tile_w * 2 + gap
    frame_h = pad * 2 + tile_h
    margin = 90  # room for shadow + rotation expand
    layer = Image.new("RGBA", (frame_w + 2 * margin, frame_h + 2 * margin), (0, 0, 0, 0))

    # -- the plank/frame itself --
    fx0, fy0 = margin, margin
    fx1, fy1 = fx0 + frame_w, fy0 + frame_h
    plank = wood_fill((frame_w, frame_h), WOOD_BASE, seed=7).convert("RGBA")
    pd = ImageDraw.Draw(plank)
    outer_pts = wobbled_points((3, 3, frame_w - 3, frame_h - 3), seed=8, jitter=4.0)
    pd.line(outer_pts, fill=(*BROWN_INK, 255), width=6, joint="curve")
    # inner bevel line just inside the outer border (reads as a carved lip)
    inner_pts = wobbled_points((14, 14, frame_w - 14, frame_h - 14), seed=9, jitter=2.5)
    pd.line(inner_pts, fill=(*WOOD_DARK, 180), width=2, joint="curve")
    layer.alpha_composite(plank, (fx0, fy0))
    d = ImageDraw.Draw(layer)

    # -- carved divider groove between the two digit slots --
    div_x = fx0 + pad + tile_w + gap // 2
    div_pts = [(div_x + random.Random(12).uniform(-2, 2), fy0 + pad - 6 + i)
               for i in range(0, frame_h - 2 * pad + 12, 10)]
    d.line(div_pts, fill=(*WOOD_DARK, 210), width=5, joint="curve")

    # -- the two digit tiles, each independently made --
    t1 = build_tile("1", (tile_w, tile_h), seed=21, rot_deg=-1.7)
    t2 = build_tile("3", (tile_w, tile_h), seed=41, rot_deg=1.3)
    layer.alpha_composite(t1, (fx0 + pad - 3, fy0 + pad + 5))
    layer.alpha_composite(t2, (fx0 + pad + tile_w + gap + 4, fy0 + pad - 3))

    # -- corner pegs (lashed construction, not a manufactured hinge) --
    for (px, py) in [(fx0 + 16, fy0 + 16), (fx1 - 16, fy0 + 16),
                      (fx0 + 16, fy1 - 16), (fx1 - 16, fy1 - 16)]:
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(*WOOD_DARK, 255))
        d.ellipse([px - 3, py - 3, px + 1, py + 1], fill=(*WOOD_LIGHT, 200))

    # -- a lashed rope tie across the top, knotted at both ends --
    rng = random.Random(55)
    rope_y = fy0 + 14
    rope = [(fx0 + 10, rope_y)]
    for i in range(1, 14):
        t = i / 13
        rope.append((fx0 + 10 + (frame_w - 20) * t, rope_y + rng.uniform(-4, 4)))
    d.line(rope, fill=(*WOOD_DARK, 230), width=4, joint="curve")
    d.line([(x, y + 5) for x, y in rope], fill=(*WOOD_DARK, 140), width=2, joint="curve")
    for kx in (fx0 + 10, fx1 - 10):
        d.ellipse([kx - 6, rope_y - 6, kx + 6, rope_y + 6], outline=(*WOOD_DARK, 230), width=3)

    # -- a few worn tally scratches along the bottom rail (texture only) --
    for i in range(5):
        sx = fx0 + pad + 10 + i * 9
        d.line([(sx, fy1 - 12), (sx + 3, fy1 - 24)], fill=(*WOOD_DARK, 160), width=2)

    # -- drop shadow, built into the same layer so it rotates in lockstep --
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.polygon(outer_pts, fill=(15, 10, 6, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    shadow_layer = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    shadow_layer.alpha_composite(shadow, (fx0 + 14, fy0 + 18))
    combined = Image.alpha_composite(shadow_layer, layer)

    return combined.rotate(-2.1, expand=True, resample=Image.BICUBIC)


def render_laps_word(canvas, cy):
    text = "LAPS"
    font = ImageFont.truetype(F_ZILLA_SEMI, 118)
    alpha, _ = stamped_alpha(text, font, seed=63)
    inked = Image.new("RGBA", alpha.size, (*RUBRIC, 0))
    inked.putalpha(alpha)
    rot = inked.rotate(-1.3, expand=True, resample=Image.BICUBIC)
    ox = (W - rot.width) // 2
    canvas.alpha_composite(rot, (ox, cy))
    return cy + rot.height


def main():
    canvas = base_canvas(JERICHO / "stills" / "j03_laps.png").convert("RGBA")
    board = build_board()
    bx = (W - board.width) // 2
    by = 190
    canvas.alpha_composite(board, (bx, by))
    render_laps_word(canvas, by + board.height - 40)
    out_path = OUT / "flap_13laps.png"
    canvas.convert("RGB").save(out_path)
    print(f"[ok] wrote {out_path}")


if __name__ == "__main__":
    main()
