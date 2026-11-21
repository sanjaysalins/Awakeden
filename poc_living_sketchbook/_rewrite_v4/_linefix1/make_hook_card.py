"""Rebuild the shipped 'WHO SURVIVED / WHEN JERICHO FELL?' hook card (0-2.0 s) as a 1080x1920 RGBA overlay, matched to jericho_v4_cc_v5hook.mp4 geometry."""
from PIL import Image, ImageDraw, ImageFont
import sys
F = "C:/Windows/Fonts/impact.ttf"
im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
rows = [("WHO SURVIVED", (255, 255, 255), (207, 308, 873, 438), (229, 847)), ("WHEN JERICHO FELL?", (241, 191, 77), (101, 458, 975, 588), (124, 953))]
for text, col, box, (x0, x1) in rows:
    d.rectangle(box, fill=(20, 18, 16, 179))
    # size so ink width matches the shipped card
    lo, hi = 60, 200
    for _ in range(20):
        s = (lo + hi) / 2; f = ImageFont.truetype(F, int(round(s)))
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] > (x1 - x0): hi = s
        else: lo = s
    f = ImageFont.truetype(F, int(round(lo))); bb = d.textbbox((0, 0), text, font=f)
    cy = (box[1] + box[3]) // 2
    d.text((x0 - bb[0], cy - (bb[1] + bb[3]) // 2 - 0), text, font=f, fill=col + (255,))
    print(text, int(round(lo)), bb)
im.save(sys.argv[1] if len(sys.argv) > 1 else "hook_card.png")
