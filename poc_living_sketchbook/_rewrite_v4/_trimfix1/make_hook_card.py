"""Hook card 0-2.0 s with words SPOKEN at 0.08-1.58 ('Snakes were killing my people.'), same look as the shipped card (dark scrim rows, white + gold Impact)."""
from PIL import Image, ImageDraw, ImageFont
import sys
F = "C:/Windows/Fonts/impact.ttf"
im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
rows = [("SNAKES WERE", (255,255,255), (308,437)), ("KILLING MY PEOPLE.", (241,191,77), (458,587))]
f = ImageFont.truetype(F, 100)
for text, col, (y0, y1) in rows:
    bb = d.textbbox((0,0), text, font=f); w = bb[2]-bb[0]
    x0 = (1080 - w)//2 - 26; x1 = x0 + w + 52
    d.rectangle((x0, y0, x1, y1), fill=(20,18,16,179))
    cy = (y0+y1)//2
    d.text(((1080-w)//2 - bb[0], cy - (bb[1]+bb[3])//2), text, font=f, fill=col+(255,))
    print(text, w, x0, x1)
im.save(sys.argv[1] if len(sys.argv) > 1 else "hook_card.png")
