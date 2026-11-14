"""Thumbs v2 after the upload red team (5/5 REVISE): one tagline on both, 'HE SAID NO AT THE FIRST ONE.' (opens 'what was the
first fire?' instead of giving away the last line); wide = art cropped 3:4 and larger (Fable/Opus: teal panel was 2/3). $0."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
H = Path(__file__).resolve().parent
sys.path.insert(0, str(H.parent / "poster_r1"))
import poster as P  # noqa: E402
OUT = H.parent / "thumbs" / "v2"; OUT.mkdir(parents=True, exist_ok=True)
TAG = "At the first fire, Peter said no."


def wide(art, fy):
    h = Image.new("RGBA", (1920, 1080), P.TEAL + (255,))
    a = P.cover(art, 1000, 1080, 0.5, fy, zoom=1.0)
    h.paste(a, (0, 0))
    d = ImageDraw.Draw(h)
    cx = 1000 + (1920 - 1000) / 2
    ft = P.font("BebasNeue-Regular.ttf", 205)
    fg = P.font("Oswald-Regular.ttf", 46)
    P.text_c(d, cx, 250, TAG.upper(), fg, P.CREAM, spacing=4)
    P.text_c(d, cx, 340, "THE SECOND", ft, P.CREAM, spacing=6, shadow=(6, 6, P.INK + (200,)))
    P.text_c(d, cx, 560, "FIRE", ft, P.CREAM, spacing=6, shadow=(6, 6, P.INK + (200,)))
    P.text_c(d, cx, 980, "A STORY FROM JOHN 21", P.font("Oswald-Regular.ttf", 36), P.CREAM, spacing=8)
    return h


burn = Image.open(H / "art" / "burnB_gpt2.png").convert("RGB")
dbl = Image.open(H / "art" / "doubleB_gpt1.png").convert("RGB")
v, _ = P.make(burn, 0.5, "The Second Fire", TAG, "bottom")
v.convert("RGB").save(OUT / "SECOND_FIRE_thumb_shorts_9x16.jpg", quality=93)
wide(dbl, 0.56).convert("RGB").save(OUT / "SECOND_FIRE_thumb_wide_16x9.jpg", quality=93)
print("ok")
