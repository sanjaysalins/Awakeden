"""Render every layout template as a static page (PIL, $0) into one contact sheet —
the comic-layout vocabulary, anchor-aware so main elements are never sliced.
Fractured-hero templates demo one hero clip broken into expressive anchor crops."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import comic_engine as ce

EW = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\_style_poc\ew04")
ST = EW / "stills"
S = Path(__file__).parent


def C(slug, motion="static", bias=(0.5, 0.5), zoom=1.0, anchors=None):
    return {"path": str(ST / f"{slug}.png"), "motion": motion,
            "bias": list(bias), "zoom": zoom, "anchors": anchors or []}


# Jesus hero anchors for fracture: (zoom, bias_x, bias_y) — full / eyes / mouth / candle
J = [(1.0, 0.5, 0.40), (2.4, 0.5, 0.28), (2.6, 0.5, 0.52), (2.7, 0.82, 0.86)]
MOSES = [(1.0, 0.22, 0.38), (2.6, 0.20, 0.27), (2.4, 0.26, 0.62)]  # full / eye / beard

DEMOS = [
    ("full",       [C("05b_jesus_speaks", bias=(0.5, 0.40))], {"type": "redletter", "text": "And as Moses lifted up the serpent in the wilderness, even so must the Son of man be lifted up.", "speaker": "JESUS", "ref": "JOHN 3"}),
    ("two_v",      [C("01b_moses_close", bias=(0.20, 0.40)), C("01_hook_moses")], {"type": "caption", "text": "My people were dying of snakebite."}),
    ("split_v",    [C("05_night_teacher")], {"type": "caption", "text": "From the far side of my life, the Teacher answered:"}),
    ("stack_h",    [C("02_judgment_plague"), C("02b_serpents_spread")], {"type": "caption", "text": "The venom was the judgment our sin had earned."}),
    ("big_inset",  [C("03b_serpent_atop_sky"), C("04b_face_to_life", bias=(0.5, 0.35))], {"type": "caption", "text": "Lift it high — and the bitten will live."}),
    ("triptych_v", [C("08_bitten_multitude")], {"type": "caption", "text": "You who are bitten — that is every one of us."}),
    ("strip_h3",   [C("03_bronze_lifted"), C("04_look_and_live"), C("03b_serpent_atop_sky")], {"type": "caption", "text": "Forge it. Lift it. Look, and live."}),
    ("quad",       [C("01_hook_moses"), C("02_judgment_plague"), C("03_bronze_lifted"), C("04_look_and_live")], {"type": "caption", "text": "The whole story, in four beats."}),
    ("hero_frac3", [C("05b_jesus_speaks", anchors=J)], {"type": "caption", "text": "FRACTURED HERO — full + eyes + candle"}),
    ("hero_frac4", [C("05b_jesus_speaks", anchors=J)], {"type": "caption", "text": "FRACTURED HERO 2x2"}),
    ("hero_band3", [C("05b_jesus_speaks", anchors=[J[0], J[1], J[3]])], {"type": "caption", "text": "FRACTURED HERO — three strips"}),
]

pages = []
for tpl, clips, cap in DEMOS:
    out = S / f"_tpl_{tpl}.png"
    ce.render_still_page(tpl, clips, cap, out)
    pages.append((tpl, out)); print("rendered", tpl, flush=True)

cols, tw, th = 4, 300, 533
rows = (len(pages) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (tw + 16) + 16, rows * (th + 56) + 16), (28, 28, 32))
d = ImageDraw.Draw(sheet); f = ImageFont.truetype(ce.FONT, 30)
for i, (tpl, p) in enumerate(pages):
    r, c = divmod(i, cols)
    x = 16 + c * (tw + 16); y = 16 + r * (th + 56)
    d.text((x + 6, y), tpl, font=f, fill=(245, 245, 245))
    sheet.paste(Image.open(p).resize((tw, th)), (x, y + 40))
sheet.save(S / "templates_showcase.png")
print("SHEET ->", S / "templates_showcase.png", flush=True)
