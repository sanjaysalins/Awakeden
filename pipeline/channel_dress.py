"""pipeline/channel_dress.py — $0 YouTube channel banner + avatar.

Banner: 2560x1440 from the inked crane_cross_soldiers still (Psalm-22 rebuild),
composed so the face + outstretched arms sit inside the 1546x423 all-device safe
strip, with the red AWAKEDEN wordmark + tagline on the sand at the left of the strip.
Avatar: 800x800 ivory disc, red ring, Georgia 'A' - matches the watermark identity.

  .venv\\Scripts\\python.exe pipeline/channel_dress.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_brand"

STRIP = [   # the channel's thesis in four inked panels — the red thread of Scripture
    (ROOT / "batches/cluster_01_cross/pierced_zech1210/visual/zechariah_night_scroll.png", "WRITTEN"),
    (ROOT / "batches/cluster_01_cross/pierced_zech1210/visual/face_on_cross.png", "PIERCED"),
    (ROOT / "batches/cluster_01_cross/into_thy_hands_luke2346/visual/bowed_head_finished.png", "FINISHED"),
    (ROOT / "batches/cluster_02_resurrection/sign_of_jonah_matt1240/visual/stone_rolled_dawn.png", "RISEN"),
]


def _panel(src: Path, w: int, h: int) -> "Image.Image":
    img = Image.open(src).convert("RGB")
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    img = img.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    sw, sh = img.size
    x, y = (sw - w) // 2, min((sh - h) // 3, sh - h)   # faces live high
    return img.crop((x, y, x + w, y + h))

RED = (168, 35, 29)
IVORY = (245, 240, 208)
INK = (18, 14, 10)
# website identity (assets/css/site.css): AWAK bone + EDEN red-bright w/ glow,
# Archivo Black — Arial Black (ariblk) is the closest installed face
BONE = (236, 234, 228)      # --bone
RED_BRIGHT = (229, 48, 61)  # --red-bright
SITE_INK = (12, 14, 18)     # --ink
GEORGIA_B = r"C:\Windows\Fonts\georgiab.ttf"
GEORGIA_I = r"C:\Windows\Fonts\georgiai.ttf"
ARIAL_B = r"C:\Windows\Fonts\arialbd.ttf"
ARIAL_BLK = r"C:\Windows\Fonts\ariblk.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(ARIAL_B, size)


def wordmark_width(size: int, tracking: float = 0.14) -> float:
    f = font(ARIAL_BLK, size)
    tmp = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    return sum(tmp.textlength(ch, font=f) + size * tracking for ch in "AWAKEDEN")


def draw_split_char(im: Image.Image, xy: tuple, ch: str, f: ImageFont.FreeTypeFont,
                    size: int, c1: tuple, c2: tuple) -> None:
    """Draw one glyph split diagonally: top-left half c1 (bone), bottom-right half c2
    (red) — the shared E where AWAKE becomes EDEN."""
    pad = size // 3
    tile_w, tile_h = size * 2 + pad, size * 2 + pad
    t1 = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 0))
    ImageDraw.Draw(t1).text((pad, pad), ch, font=f, fill=c1 + (255,))
    t2 = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 0))
    ImageDraw.Draw(t2).text((pad, pad), ch, font=f, fill=c2 + (255,))
    bbox = t1.getbbox()
    if not bbox:
        return
    x0, y0, x1, y1 = bbox
    mask = Image.new("L", (tile_w, tile_h), 0)
    # red = right of the diagonal running from glyph top-right to bottom-left
    ImageDraw.Draw(mask).polygon([(x1, y0), (x1, y1), (x0, y1)], fill=255)
    t1.paste(t2, (0, 0), Image.composite(t2.split()[3], Image.new("L", mask.size, 0), mask))
    im.paste(t1, (int(xy[0]) - pad, int(xy[1]) - pad), t1)


def draw_wordmark(im: Image.Image, x: float, y: float, size: int,
                  tracking: float = 0.14, glow: bool = True, shadow: bool = False) -> float:
    """Site wordmark exactly as site.css renders it: AWAK bone + EDEN red-bright
    (with the site's red glow), letterspaced Arial Black. (User call 2026-07-21:
    match the website - the earlier shared split-E is retired.)"""
    f = font(ARIAL_BLK, size)
    if glow:
        from PIL import ImageFilter
        gl = Image.new("RGBA", im.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(gl)
        cx = x
        for i, ch in enumerate("AWAKEDEN"):
            if i >= 4:
                gd.text((cx, y), ch, font=f, fill=RED_BRIGHT + (160,))
            cx += gd.textlength(ch, font=f) + size * tracking
        gl = gl.filter(ImageFilter.GaussianBlur(size * 0.09))
        im.paste(Image.alpha_composite(im.convert("RGBA"), gl).convert("RGB"), (0, 0))
    dr = ImageDraw.Draw(im, "RGBA")
    cx = x
    for i, ch in enumerate("AWAKEDEN"):
        if shadow:
            dr.text((cx + max(2, size // 30), y + max(2, size // 30)), ch,
                    font=f, fill=(0, 0, 0, 210))
        dr.text((cx, y), ch, font=f, fill=BONE if i < 4 else RED_BRIGHT)
        cx += dr.textlength(ch, font=f) + size * tracking
    return cx


def banner():
    W, H = 2560, 1440
    sx0, sy0, sx1, sy1 = 507, 508, 2053, 931          # all-device safe strip
    im = Image.new("RGB", (W, H), SITE_INK)
    dr = ImageDraw.Draw(im, "RGBA")

    # faint oversized split-E on the TV-only edges (texture, never in the strip)
    f_ghost = font(ARIAL_BLK, 900)
    dr.text((W - 620, H - 780), "E", font=f_ghost, fill=(236, 234, 228, 13))
    dr.text((-240, -230), "E", font=f_ghost, fill=(229, 48, 61, 11))

    # ---- four story panels on the red thread (sized FIRST; text fits after) --
    pw, ph, gap = 224, 330, 26
    py = sy0 + 22
    total = 4 * pw + 3 * gap
    x0 = sx1 - total - 12                              # panels own the strip's right
    left_w = x0 - sx0 - 60                             # room left for the words

    # ---- left block: wordmark + tagline + the thread's origin ---------------
    lx = sx0 + 10
    size = fit_word_size(left_w - 20, 0.10)
    draw_wordmark(im, lx, sy0 + 88, size, tracking=0.10)
    dr = ImageDraw.Draw(im, "RGBA")
    f_tag = font(GEORGIA_I, 34)
    dr.text((lx + 4, sy0 + 196), "Finding Jesus in the whole Bible,", font=f_tag, fill=BONE)
    dr.text((lx + 4, sy0 + 246), "one panel at a time.", font=f_tag, fill=BONE)
    dr.line([(lx + 6, sy0 + 322), (lx + 200, sy0 + 322)], fill=RED_BRIGHT, width=5)

    thread_y = py + ph // 2
    dr.line([(x0 - 52, thread_y), (sx1 - 8, thread_y)], fill=RED_BRIGHT + (210,), width=6)
    f_cap = font(GEORGIA_B, 27)
    for i, (src, word) in enumerate(STRIP):
        panel = _panel(src, pw, ph)
        tile = Image.new("RGBA", (pw + 22, ph + 22), (0, 0, 0, 0))
        ImageDraw.Draw(tile).rectangle([0, 0, pw + 21, ph + 21], fill=IVORY + (255,))
        tile.paste(panel, (11, 11))
        tile = tile.rotate((-1.4, 1.1, -0.9, 1.3)[i], expand=True, resample=Image.BICUBIC)
        tx = x0 + i * (pw + gap) - (tile.width - pw) // 2
        ty = py - (tile.height - ph) // 2
        im.paste(tile, (tx, ty), tile)
        dr = ImageDraw.Draw(im, "RGBA")
        cw = dr.textlength(word, font=f_cap) + 34
        cx = x0 + i * (pw + gap) + (pw - cw) / 2
        cy = py + ph - 2
        dr.rounded_rectangle([cx, cy, cx + cw, cy + 45], radius=8,
                             fill=IVORY + (255,), outline=INK + (255,), width=3)
        dr.text((cx + 17, cy + 6), word, font=f_cap, fill=INK)

    OUT.mkdir(exist_ok=True)
    p = OUT / "channel_banner.png"
    im.save(p)
    # safe-strip preview so the user can check what phones/desktop show
    im.crop((sx0, sy0, sx1, sy1)).save(OUT / "channel_banner_SAFE_PREVIEW.png")
    print(f"banner  -> {p}")


def fit_word_size(max_w: float, tracking: float = 0.08) -> int:
    """Largest font size whose AWAKEDEN width fits max_w (grows from tiny)."""
    size = 8
    while wordmark_width(size + 2, tracking) <= max_w:
        size += 2
    return size


def word_bbox(size: int, tracking: float = 0.08) -> tuple:
    """(w, cap_top, cap_bottom) of the drawn word, measured, for true centering."""
    w = int(wordmark_width(size, tracking)) + size
    tmp = Image.new("RGBA", (w, size * 3), (0, 0, 0, 0))
    dr = ImageDraw.Draw(tmp)
    f = font(ARIAL_BLK, size)
    cx = 0.0
    for ch in "AWAKEDEN":
        dr.text((cx, size), ch, font=f, fill=(255, 255, 255, 255))
        cx += dr.textlength(ch, font=f) + size * tracking
    bb = tmp.getbbox()
    return (bb[2] - bb[0]), bb[1] - size, bb[3] - size   # width, top-off, bottom-off


def draw_word_centered(im: Image.Image, box: tuple, tracking: float = 0.08,
                       glow: bool = False) -> None:
    """Draw the one-word mark optically centered inside box=(x0,y0,x1,y1)."""
    bw, bh = box[2] - box[0], box[3] - box[1]
    size = fit_word_size(bw, tracking)
    w, top_off, bot_off = word_bbox(size, tracking)
    glyph_h = bot_off - top_off
    x = box[0] + (bw - w) / 2
    y = box[1] + (bh - glyph_h) / 2 - top_off
    draw_wordmark(im, x, y, size, tracking=tracking, glow=glow)


def avatar():
    """The channel in one glyph: the split E (AWAKE|EDEN hinge) inside an ivory
    comic-panel frame — the medium (panel), the name (E), the Scripture thread
    (red) — bold enough to read at 32px beside a comment, circle-crop safe."""
    px = 800
    # the inked art fills the circle: crown of thorns, head bowed — the channel's
    # most recognizable panel — with the whole word on an ink chip beneath
    art = _panel(ROOT / "batches/cluster_01_cross/into_thy_hands_luke2346/visual"
                        / "bowed_head_finished.png", px, px)
    im = art.convert("RGB")
    dr = ImageDraw.Draw(im, "RGBA")
    # soft ink gradient at the bottom half so the chip band sits naturally
    for i in range(int(px * 0.42)):
        a = int(150 * (i / (px * 0.42)) ** 1.6)
        dr.line([(0, int(px * 0.58) + i), (px, int(px * 0.58) + i)],
                fill=(12, 14, 18, a))
    # ink chip + the whole word (circle is narrower at this height — keep margins)
    dr.rounded_rectangle([px * 0.13, px * 0.615, px * 0.87, px * 0.775],
                         radius=20, fill=(12, 14, 18, 215), outline=IVORY + (235,), width=5)
    draw_word_centered(im, (px * 0.17, px * 0.65, px * 0.83, px * 0.74), glow=True)
    p = OUT / "channel_avatar.png"
    im.save(p)
    # round preview — exactly what the circular crop shows
    mask = Image.new("L", (px, px), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, px, px], fill=255)
    prev = Image.new("RGB", (px, px), (255, 255, 255))
    prev.paste(im, (0, 0), mask)
    prev.save(OUT / "channel_avatar_ROUND_PREVIEW.png")
    print(f"avatar  -> {p}")


if __name__ == "__main__":
    banner()
    avatar()
