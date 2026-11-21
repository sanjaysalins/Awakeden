"""Rebuild the shipped hook card ("A PROMISE / INSIDE THE CURSE?", 0-2.0 s) as a 1080x1920 RGBA overlay, fitted to the pinned v5hook geometry
(box rects, ink boxes and alpha measured from the pinned final vs its source)."""
from PIL import Image, ImageDraw, ImageFont
import sys
F = "C:/Windows/Fonts/impact.ttf"
im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
# text, colour, box (x0,y0,x1,y1), ink bbox (x0,y0,x1,y1) measured on the pinned film
rows = [("A PROMISE", (252, 252, 251), (324, 1148, 755, 1266), (346, 1170, 730, 1244)),
        ("INSIDE THE CURSE?", (241, 191, 77), (173, 1298, 905, 1416), (199, 1320, 881, 1394))]
for text, col, (bx0, by0, bx1, by1), (ix0, iy0, ix1, iy1) in rows:
    d.rectangle((bx0, by0, bx1, by1), fill=(2, 1, 1, 166))
    lo, hi = 40, 260
    for _ in range(24):
        s = (lo + hi) / 2; f = ImageFont.truetype(F, int(round(s)))
        bb = d.textbbox((0, 0), text, font=f)
        if (bb[2] - bb[0]) > (ix1 - ix0): hi = s
        else: lo = s
    f = ImageFont.truetype(F, int(round(lo))); bb = d.textbbox((0, 0), text, font=f)
    d.text((ix0 - bb[0], (iy0 + iy1) // 2 - (bb[1] + bb[3]) // 2), text, font=f, fill=col + (255,))
    print(text, int(round(lo)), bb)
im.save(sys.argv[1] if len(sys.argv) > 1 else "hook_card.png")
