"""Balloon redesign — 3 styles over the SAME hero frame (the user picked C). $0."""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import motion_comic as mc

EW = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\_style_poc\ew04")
ANIM = EW / "anim"
S = mc.S
PW, PH = 1080, 1920
INK = (18, 14, 8, 255)
FONT = mc.FONT
TXT = "And as Moses lifted up the serpent in the wilderness, even so must the Son of man be lifted up."

frame = S / "_hero_frame.png"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "2.0", "-i",
                str(ANIM / "EW04__05b_jesus_speaks.mp4"), "-frames:v", "1",
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                str(frame)], check=True)
base = Image.open(frame).convert("RGBA")


def style_A(img):
    d = ImageDraw.Draw(img); font = ImageFont.truetype(FONT, 46)
    cx, cy = 360, 1440; w, txt_w = 660, 540
    lines = mc._wrap(d, TXT, font, txt_w); lh = 58; th = len(lines) * lh
    rx, ry = w // 2, th // 2 + 70
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.ellipse([cx - rx + 10, cy - ry + 12, cx + rx + 10, cy + ry + 12], fill=(0, 0, 0, 90))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
    tail_to = (650, 980)
    d.polygon([(cx + 120, cy - ry + 30), (cx + 220, cy - ry + 70), tail_to], fill=(252, 252, 248, 255))
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(252, 252, 248, 255), outline=INK, width=7)
    d.line([(cx + 120, cy - ry + 30), tail_to], fill=INK, width=7)
    d.line([(cx + 220, cy - ry + 70), tail_to], fill=INK, width=7)
    y = cy - th // 2
    for ln in lines:
        tw = d.textlength(ln, font=font); d.text((cx - tw / 2, y), ln, font=font, fill=INK); y += lh


def style_B(img):
    d = ImageDraw.Draw(img); font = ImageFont.truetype(FONT, 48); w = 680
    lines = mc._wrap(d, TXT, font, w - 76); lh = 60; h = len(lines) * lh + 56
    cx, cy = 365, 1440; box = [cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2]
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([box[0] + 9, box[1] + 11, box[2] + 9, box[3] + 11],
                                         radius=40, fill=(0, 0, 0, 95))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    tail_to = (655, 985); bx = box[2] - 90
    d.polygon([(bx - 30, box[1] + 6), (bx + 40, box[1] + 6), tail_to], fill=(251, 251, 246, 255))
    d.line([(bx - 30, box[1] + 6), tail_to, (bx + 40, box[1] + 6)], fill=INK, width=6, joint="curve")
    d.rounded_rectangle(box, radius=40, fill=(251, 251, 246, 255), outline=INK, width=6)
    d.rounded_rectangle([box[0] + 9, box[1] + 9, box[2] - 9, box[3] - 9], radius=32,
                        outline=(120, 96, 60, 200), width=2)
    y = box[1] + 28
    for ln in lines:
        tw = d.textlength(ln, font=font); d.text((cx - tw / 2, y), ln, font=font, fill=INK); y += lh


def style_C(img):
    d = ImageDraw.Draw(img); font = ImageFont.truetype(FONT, 50); tag_font = ImageFont.truetype(FONT, 34)
    mx = 46; inner = PW - 2 * mx - 56
    lines = mc._wrap(d, TXT, font, inner); lh = 62
    top = PH - (len(lines) * lh + 150); box = [mx, top, PW - mx, PH - 60]
    d.rounded_rectangle([mx, top - 8, mx + 250, top + 48], radius=10, fill=(150, 28, 24, 255), outline=INK, width=4)
    d.text((mx + 24, top + 4), "JESUS  ·  JOHN 3", font=tag_font, fill=(255, 248, 240, 255))
    d.rounded_rectangle([box[0], top + 50, box[2], box[3]], radius=16, fill=(250, 248, 244, 255), outline=INK, width=7)
    y = top + 74
    for ln in lines:
        d.text((box[0] + 28, y), ln, font=font, fill=(150, 28, 24, 255)); y += lh


for name, fn in (("A_ellipse", style_A), ("B_inked_rect", style_B), ("C_redletter_bar", style_C)):
    out = base.copy(); fn(out); out.convert("RGB").save(S / f"balloon_{name}.png")

imgs = [Image.open(S / f"balloon_{n}.png") for n in ("A_ellipse", "B_inked_rect", "C_redletter_bar")]
tw = PW // 2
sheet = Image.new("RGB", (tw * 3 + 40, PH // 2 + 60), (30, 30, 34))
d = ImageDraw.Draw(sheet); tf = ImageFont.truetype(FONT, 30)
labels = ["A  classic ellipse", "B  inked rounded-rect", "C  red-letter bar  <- PICKED"]
for i, (im, lb) in enumerate(zip(imgs, labels)):
    th = im.resize((tw, PH // 2)); x = 10 + i * (tw + 10)
    sheet.paste(th, (x, 50)); d.text((x + 8, 12), lb, font=tf, fill=(240, 240, 240))
sheet.save(S / "balloon_compare.png")
print("wrote", S / "balloon_compare.png")
