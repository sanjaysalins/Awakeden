from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
D = Path(__file__).parent; src = Image.open(D.parent.parent/"stills/t4.png").convert("RGB")
W, H = 1080, 1920
s = max(W/src.width, H/src.height); im0 = src.resize((round(src.width*s), round(src.height*s)), Image.LANCZOS)
im0 = im0.crop(((im0.width-W)//2, (im0.height-H)//2, (im0.width-W)//2+W, (im0.height-H)//2+H))
F = "C:/Windows/Fonts/impact.ttf"
V = {"P3": ["HE KNEW IT ALL", "AND STAYED"], "P3b": ["HE KNEW HER", "AND STAYED"], "P1": ["HE KNEW", "EVERYTHING"]}
for k, lines in V.items():
    im = im0.copy(); d = ImageDraw.Draw(im); y = 110
    for i, t in enumerate(lines):
        size = 200 if i == len(lines)-1 else 150
        f = ImageFont.truetype(F, size)
        while d.textlength(t, font=f) > W-120: size -= 6; f = ImageFont.truetype(F, size)
        x = (W - d.textlength(t, font=f))/2
        d.text((x, y), t, font=f, fill=(255, 230, 0) if i else (255, 255, 255), stroke_width=12, stroke_fill=(0, 0, 0))
        y += size + 20
    im.save(D/f"thumb_{k}.jpg", quality=90); im.resize((180, 320), Image.LANCZOS).save(D/f"thumb_{k}_phone.jpg", quality=90)
print("ok")
