"""Judges' fixes on the pick (turned + LOUDER): tagline 1.5x, warm glow behind tiny Jesus. $0."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import compose as C
im = C.cover(Image.open(C.A/"turned.png").convert("RGB"))
# glow behind Jesus (find the brightest column in the top band)
g = Image.new("L", im.size, 0); dg = ImageDraw.Draw(g)
dg.ellipse((540-150, 110-200, 540+150, 110+200), fill=150); g = g.filter(ImageFilter.GaussianBlur(55))
glow = Image.composite(Image.new("RGB", im.size, (255, 236, 190)), Image.new("RGB", im.size, (0, 0, 0)), g)
im = ImageChops.screen(im, glow)
y = 400; im = C.soft_band(im, y - 30, y + 380)
d = ImageDraw.Draw(im)
f = C.fit(d, "LOUDER", C.SHOUT, 300, C.W - 120); x = (C.W - d.textlength("LOUDER", font=f))/2
d.text((x-5, y-6), "LOUDER", font=f, fill=C.BONE, stroke_width=12, stroke_fill=C.BONE); d.text((x, y), "LOUDER", font=f, fill=C.RED)
bb = d.textbbox((0, 0), "LOUDER", font=f); ty = y + bb[3] + 22
tf = ImageFont.truetype(str(C.TELL), 128); tag = "Everyone said hush."
tw = d.textlength(tag, font=tf); tx = (C.W - tw)/2
d.text((tx+4, ty+5), tag, font=tf, fill=C.INK, stroke_width=3, stroke_fill=C.INK); d.text((tx, ty), tag, font=tf, fill=C.BONE)
im.save(C.O/"THUMB_FINAL_9x16.jpg", quality=93)
im.resize((180, 320), Image.LANCZOS).save(C.O/"_phone_final.png")
print("ok", ty, tw)
