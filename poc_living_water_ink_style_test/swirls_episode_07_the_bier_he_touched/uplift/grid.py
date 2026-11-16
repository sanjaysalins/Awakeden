import sys
from PIL import Image, ImageDraw
src, out, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
im = Image.open(src).convert("RGB").resize((1080, 1936), Image.LANCZOS).crop((0, 8, 1080, 1928))
c = im.crop((x0, y0, x1, y1)); d = ImageDraw.Draw(c)
for x in range((x0 // 50 + 1) * 50, x1, 50):
    d.line([(x - x0, 0), (x - x0, y1 - y0)], fill=(255, 0, 0) if x % 100 == 0 else (255, 160, 160), width=1)
    if x % 100 == 0: d.text((x - x0 + 2, 2), str(x), fill=(255, 0, 0))
for y in range((y0 // 50 + 1) * 50, y1, 50):
    d.line([(0, y - y0), (x1 - x0, y - y0)], fill=(0, 0, 255) if y % 100 == 0 else (160, 160, 255), width=1)
    if y % 100 == 0: d.text((2, y - y0 + 2), str(y), fill=(0, 0, 255))
c.save(out)
