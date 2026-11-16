"""Poster r1 finalists: real type on the art. $0."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
H = Path(__file__).parent; A = H/"art"; O = H/"final"; O.mkdir(exist_ok=True)
F = "C:/Windows/Fonts/impact.ttf"; W, HH = 1080, 1920
def cover(im):
    s = max(W/im.width, HH/im.height); im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    x = (im.width-W)//2; y = (im.height-HH)//2; return im.crop((x, y, x+W, y+HH))
def fit(d, t, size, maxw):
    f = ImageFont.truetype(F, size)
    while d.textlength(t, font=f) > maxw: size -= 4; f = ImageFont.truetype(F, size)
    return f, size
def poster(name, where, title=("THE JAR", "STAYED"), tag="SHE CAME FOR WATER."):
    im = cover(Image.open(A/f"{name}.png").convert("RGB")); d = ImageDraw.Draw(im)
    f1, s1 = fit(d, title[0], 230, W-110); f2, s2 = fit(d, title[1], 300, W-110)
    ft = ImageFont.truetype(F, 64)
    block = s1 + s2 + 40 + 100
    y = 90 if where == "top" else HH - block - 90
    for t, f, s in ((title[0], f1, s1), (title[1], f2, s2)):
        x = (W - d.textlength(t, font=f))/2
        d.text((x+12, y+14), t, font=f, fill=(0, 0, 0))
        d.text((x, y), t, font=f, fill=(255, 228, 0), stroke_width=14, stroke_fill=(0, 0, 0))
        y += s + 10
    tw = d.textlength(tag, font=ft); x = (W - tw)/2
    d.rounded_rectangle((x-30, y+18, x+tw+30, y+18+90), 14, fill=(0, 0, 0))
    d.text((x, y+26), tag, font=ft, fill=(255, 255, 255))
    im.save(O/f"{name}.jpg", quality=92); return im
FIN = {"left_gpt": "top", "fix1": "top", "fix2": "top"}
ims = [poster(n, w) for n, w in FIN.items()]
ph = Image.new("RGB", (len(ims)*200+20, 380), "white")
for i, im in enumerate(ims): ph.paste(im.resize((180, 320), Image.LANCZOS), (20+i*200, 30))
ph.save(O/"_PHONE.jpg", quality=90); print("ok")
