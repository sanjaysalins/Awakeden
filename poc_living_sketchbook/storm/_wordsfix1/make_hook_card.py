"""Rebuild the shipped storm WHY IS HE ASLEEP IN THE STORM? hook card (0-2.0 s) as a 1080x1920 RGBA overlay, matched to jericho_v4_cc_v5hook.mp4 geometry."""
from PIL import Image, ImageDraw, ImageFont
import sys
F = "C:/Windows/Fonts/impact.ttf"
im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
rows = [("WHY IS HE ASLEEP", (255, 255, 255), (159, 538, 919, 667), (182, 894)), ("IN THE STORM?", (241, 191, 77), (210, 688, 869, 817), (237, 843))]
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
