"""sheet.py out.jpg cols tile_w img1[:label] img2[:label] ...  -> contact sheet (PIL)."""
import sys
from PIL import Image, ImageDraw
out, cols, tw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
items = sys.argv[4:]
ims = []
for it in items:
    p, _, lab = it.partition("|")
    im = Image.open(p).convert("RGB"); th = int(tw * im.height / im.width); ims.append((im.resize((tw, th)), lab))
th = max(i.height for i, _ in ims); rows = (len(ims) + cols - 1) // cols
S = Image.new("RGB", (cols * tw, rows * (th + 18)), (30, 30, 30)); d = ImageDraw.Draw(S)
for k, (im, lab) in enumerate(ims):
    x, y = (k % cols) * tw, (k // cols) * (th + 18); S.paste(im, (x, y + 18)); d.text((x + 3, y + 3), lab, fill=(255, 255, 0))
S.save(out, quality=85)
