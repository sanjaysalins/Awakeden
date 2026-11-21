r"""linefix1 hook card PNG (1080x1920 transparent): same look/position as the pinned v5hook card (white line + gold line on dark boxes,
y 922-1038 / 1072-1188) but the NEW spoken words: IF YOU ARE AFRAID / TO DIE."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
H = Path(__file__).resolve().parent
FONT = r"C:\Windows\Fonts\Oswald-Bold.ttf"
im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
def line(txt, y0, y1, fill, boxa, size=94, pad=26):
    f = ImageFont.truetype(FONT, size)
    bb = d.textbbox((0, 0), txt, font=f)
    w = bb[2] - bb[0]; h = bb[3] - bb[1]
    x0 = (1080 - w) // 2 - pad
    d.rectangle([x0, y0, x0 + w + 2 * pad, y1], fill=(0, 0, 0, boxa))
    tx = (1080 - w) // 2 - bb[0]; ty = y0 + ((y1 - y0) - h) // 2 - bb[1]
    for ox, oy in ((3, 3),):
        d.text((tx + ox, ty + oy), txt, font=f, fill=(0, 0, 0, 255))
    d.text((tx, ty), txt, font=f, fill=fill)
line("IF YOU ARE AFRAID", 922, 1038, (255, 255, 255, 255), 215)
line("TO DIE", 1072, 1188, (241, 191, 77, 255), 150)
im.save(H / "_linefix1_pool" / "hookcard_new.png"); print("ok")
