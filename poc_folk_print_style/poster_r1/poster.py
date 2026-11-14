"""Movie-poster thumbnails for The Second Fire ($0 compositing). Usage: poster.py <name> (see POSTERS).
9:16 1080x1920 cover + 16:9 1920x1080 search version. Title = Bebas Neue, tagline/credits = Oswald."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

H = Path(__file__).resolve().parent
EP = H.parent
OUT = H / "out"
OUT.mkdir(exist_ok=True)
F = "C:/Windows/Fonts/"
CREAM, TEAL, ORANGE, INK = (247, 231, 196), (16, 52, 58), (239, 106, 74), (24, 30, 32)


def font(name, size):
    return ImageFont.truetype(F + name, size)


def cover(img, w, h, fx=0.5, fy=0.5, zoom=1.0):
    """Scale to cover w x h (times zoom), crop around focus fx, fy (0-1 of source)."""
    s = max(w / img.width, h / img.height) * zoom
    im = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = min(max(0, round(im.width * fx - w / 2)), im.width - w)
    y = min(max(0, round(im.height * fy - h / 2)), im.height - h)
    return im.crop((x, y, x + w, y + h))


def fade(im, y0, y1, col, a0=0, a1=235, top=False):
    """Vertical fade band of colour col from alpha a0 at y0 to a1 at y1."""
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(min(y0, y1), max(y0, y1)):
        t = (y - y0) / (y1 - y0)
        d.line([(0, y), (im.width, y)], fill=col + (round(a0 + (a1 - a0) * t),))
    if top:
        pass
    return Image.alpha_composite(im.convert("RGBA"), ov)


def text_c(d, cx, y, s, f, fill, spacing=0, shadow=None):
    w = d.textlength(s, font=f) + spacing * (len(s) - 1)
    x = cx - w / 2
    for ch in s:
        if shadow:
            d.text((x + shadow[0], y + shadow[1]), ch, font=f, fill=shadow[2])
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + spacing


def furniture(im, title, tagline, ty, title_size, tcol=CREAM, credit=True, tag_above=True):
    d = ImageDraw.Draw(im)
    W = im.width
    ft = font("BebasNeue-Regular.ttf", title_size)
    while d.textlength(title.upper(), font=ft) + 4 * len(title) > W * 0.88:  # fit the width
        title_size -= 4
        ft = font("BebasNeue-Regular.ttf", title_size)
    fg = font("Oswald-Regular.ttf", round(title_size * 0.34))
    sh = (6, 6, INK + (200,))
    if tagline and tag_above:
        text_c(d, W / 2, ty - round(title_size * 0.46), tagline.upper(), fg, CREAM, spacing=5)
    text_c(d, W / 2, ty, title.upper(), ft, tcol, spacing=4, shadow=sh)
    if tagline and not tag_above:
        text_c(d, W / 2, ty + round(title_size * 0.95), tagline.upper(), fg, CREAM, spacing=6)
    if credit:
        fc = font("Oswald-Regular.ttf", round(W * 0.034))
        text_c(d, W / 2, im.height - round(W * 0.07), "A STORY FROM JOHN 21", fc, CREAM, spacing=8)
    return im


def still(n):
    return Image.open(EP / "stills_full" / f"s{n:02d}.png").convert("RGB")


def wide(v, title, tagline):
    """16:9: the 9:16 art (no type) at full height on the left, a teal title panel on the right."""
    h = Image.new("RGBA", (1920, 1080), TEAL + (255,))
    art = v.resize((round(1080 * 1080 / 1920), 1080), Image.LANCZOS)
    h.paste(art, (0, 0))
    d = ImageDraw.Draw(h)
    cx = 608 + (1920 - 608) / 2
    ft = font("BebasNeue-Regular.ttf", 250)
    fg = font("Oswald-Light.ttf", 52)
    words = title.upper().split()
    lines = [" ".join(words[:-1]), words[-1]] if len(words) > 2 else [title.upper()]
    y = 540 - len(lines) * 120 - 40
    text_c(d, cx, y - 80, tagline.upper(), fg, CREAM, spacing=6)
    for ln in lines:
        text_c(d, cx, y, ln, ft, CREAM, spacing=6, shadow=(6, 6, INK + (200,)))
        y += 235
    fc = font("Oswald-Light.ttf", 34)
    text_c(d, cx, 980, "A STORY FROM JOHN 21", fc, CREAM, spacing=8)
    return h


def make(art, fy, title, tagline, where):
    v = cover(art, 1080, 1920, 0.5, fy)
    clean = v.copy()
    if where == "bottom":
        v = fade(v, 1330, 1920, TEAL, 0, 242)
        furniture(v, title, tagline, 1580, 230)
    else:
        v = fade(v, 0, 560, TEAL, 242, 0)
        furniture(v, title, tagline, 160, 230, tag_above=False)
    return v, wide(clean, title, tagline)


def p_split():  # A: the two fires (film picture 11)
    return make(still(11), 0.5, "The Second Fire", "One night. One sunrise.", "bottom")


def p_bread():  # B: bread into his hands (film picture 17)
    return make(still(17), 0.45, "The Second Fire", "He said no. Three times.", "bottom")


def art(n):
    return Image.open(H / "art" / f"{n}.png").convert("RGB")


def p_face():  # C: two-sided face (new art, take 2)
    return make(art("C2"), 0.5, "The Second Fire", "One man. Two fires.", "bottom")


def p_twice():  # D: same man twice (new art, take 1)
    return make(art("D1"), 0.5, "The Second Fire", "He said no at the first.", "bottom")


def p_tome():  # E: bread held out to the viewer (new art, take 1) -- halo-look risk flagged
    return make(art("E1"), 0.5, "The Second Fire", "He fed him first.", "top")


def p_coals():  # F: three cold coals (new art, take 1)
    return make(art("F1"), 0.5, "The Second Fire", "Once, they went out.", "top")


POSTERS = {"A_split": p_split, "B_bread": p_bread, "C_face": p_face, "D_twice": p_twice, "E_tome": p_tome, "F_coals": p_coals}

if __name__ == "__main__":
    for name in sys.argv[1:] or POSTERS:
        v, h = POSTERS[name]()
        v.convert("RGB").save(OUT / f"{name}_9x16.jpg", quality=92)
        h.convert("RGB").save(OUT / f"{name}_16x9.jpg", quality=92)
        print(name, "ok")
