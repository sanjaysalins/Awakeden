"""Owner pick (2026-11-14): frozen art + STOOD STILL / for one blind man. Judge fixes: tagline bigger + bone on dark so it reads small; whole block lifted so it clears Jesus's head. $0."""
from PIL import Image, ImageDraw, ImageFont
import compose as C
im = C.cover(Image.open(C.A/"frozen.png").convert("RGB"))
y = 150; im = C.soft_band(im, y - 40, y + 330, a=120)
d = ImageDraw.Draw(im)
f = C.fit(d, "STOOD STILL", C.FELL, 230, C.W - 110); t = "STOOD STILL"; x = (C.W - d.textlength(t, font=f))/2
d.text((x+4, y+6), t, font=f, fill=C.INK, stroke_width=3, stroke_fill=C.INK); d.text((x, y), t, font=f, fill=C.BONE, stroke_width=2, stroke_fill=C.BONE)
bb = d.textbbox((0, 0), t, font=f); ty = y + bb[3] + 18
tf = ImageFont.truetype(str(C.TELL), 124); tag = "for one blind man."
tw = d.textlength(tag, font=tf); tx = (C.W - tw)/2
d.text((tx, ty), tag, font=tf, fill=C.BONE, stroke_width=10, stroke_fill=C.BONE); d.text((tx, ty), tag, font=tf, fill=C.RED)
tb = d.textbbox((tx, ty), tag, font=tf)
im.save(C.O/"THUMB_FINAL_9x16.jpg", quality=93); im.resize((180, 320), Image.LANCZOS).save(C.O/"_phone_final.png")
print("tagline box", tb)
