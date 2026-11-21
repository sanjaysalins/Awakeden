r"""holdfix1 forsaken hook card: same look as the pinned v5hook (Impact 104, white line + gold F2C14E line, black@0.64 boxes at y148-277 / 298-427)
but the words spoken in the first 2 s: FROM THE CROSS, / IN HIS DARKEST HOUR."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
P = Path(r"F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_01_cross\forsaken_cry_ps221\visual\_holdfix1_pool"); P.mkdir(exist_ok=True)
im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
def line(txt, y0, y1, fill, size=104, pad=25):
    f = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", size)
    bb = d.textbbox((0, 0), txt, font=f); w = bb[2] - bb[0]; h = bb[3] - bb[1]
    x0 = (1080 - w) // 2 - pad
    d.rectangle([x0, y0, x0 + w + 2 * pad, y1], fill=(0, 0, 0, 163))
    tx = (1080 - w) // 2 - bb[0]; ty = y0 + ((y1 - y0) - h) // 2 - bb[1]
    d.text((tx + 3, ty + 3), txt, font=f, fill=(0, 0, 0, 255)); d.text((tx, ty), txt, font=f, fill=fill)
    print(txt, "box", x0, x0 + w + 2 * pad)
line("FROM THE CROSS,", 148, 277, (255, 255, 255, 255))
line("IN HIS DARKEST HOUR", 298, 427, (242, 193, 78, 255), size=96)
im.save(P / "hookcard.png")
