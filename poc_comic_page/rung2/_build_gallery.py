"""Rung 2 Phase A gallery build — page-grid mockups + character drift sheet
+ _STILLS_REVIEW.html. $0, PIL only. (Designer-run: the executor's session
died after finishing its renders + charsheet crops.)"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
ST = HERE / "stills"
PAPER = (232, 217, 181)
INK = (35, 31, 32)

LAYOUTS = {
    "2v": [(0, 0, 1, .5), (0, .5, 1, .5)],
    "3-big-left": [(0, 0, .62, 1), (.62, 0, .38, .5), (.62, .5, .38, .5)],
    "3-big-top": [(0, 0, 1, .58), (0, .58, .5, .42), (.5, .58, .5, .42)],
}
PAGES = [
    ("page1", "2v", ["p1a_night_door.png", "p1b_hesitant_hand.png"]),
    ("page2", "3-big-left", ["p2a_rehearsing.png", "p2b_jesus_speaks.png", "p2c_light_line.png"]),
    ("page4", "3-big-left", ["p4a_turning_away.png", "p4b_open_hands.png", "p4c_empty_doorway.png"]),
    ("page5", "3-big-top", ["p5a_the_welcome.png", "p5b_record_received.png", "p5c_never_locked.png"]),
]
W, H, G = 540, 960, 5


def cover_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    r, tr = im.width / im.height, w / h
    if r > tr:
        nw = int(im.height * tr)
        im = im.crop(((im.width - nw) // 2, 0, (im.width + nw) // 2, im.height))
    else:
        nh = int(im.width / tr)
        im = im.crop((0, (im.height - nh) // 2, im.width, (im.height + nh) // 2))
    return im.resize((w, h), Image.LANCZOS)


def build_page(name, layout, files):
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    for (fx, fy, fw, fh), f in zip(LAYOUTS[layout], files):
        x, y = int(fx * W) + G, int(fy * H) + G
        w, h = int(fw * W) - 2 * G, int(fh * H) - 2 * G
        page.paste(cover_crop(Image.open(ST / f), w, h), (x, y))
        d.rectangle([x, y, x + w, y + h], outline=INK, width=3)
    out = HERE / f"_mock_{name}.png"
    page.save(out)
    return out.name


def build_strip(prefix, label):
    crops = sorted(ST.glob(f"_charsheet/{prefix}_*.png"))
    if not crops:
        return None
    hgt = 360
    ims = []
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    for c in crops:
        im = Image.open(c)
        im = im.resize((int(im.width * hgt / im.height), hgt), Image.LANCZOS)
        fr = Image.new("RGB", (im.width, hgt + 34), PAPER)
        fr.paste(im, (0, 0))
        ImageDraw.Draw(fr).text((6, hgt + 6), c.stem.split("_", 1)[1], fill=INK, font=font)
        ims.append(fr)
    strip = Image.new("RGB", (sum(i.width for i in ims) + G * (len(ims) + 1), hgt + 34 + 2 * G), PAPER)
    x = G
    for i in ims:
        strip.paste(i, (x, G))
        x += i.width + G
    out = HERE / f"_charsheet_{label}.png"
    strip.save(out)
    return out.name


mocks = [build_page(*p) for p in PAGES]
strips = [s for s in (build_strip("jesus", "jesus"), build_strip("seeker", "seeker"),
                      build_strip("door", "door"), build_strip("ledger", "ledger")) if s]

rows = "".join(
    f'<h2>{t}</h2><img src="{m}" style="width:340px;border:1px solid #555">'
    for t, m in zip(["Page 1 — the fear (2v)", "Page 2 — the words (3-big-left)",
                     "Page 4 — no fine print (3-big-left)", "Page 5 — the landing (3-big-top)"], mocks))
sheet = "".join(f'<h2>Drift check — {s.split("_")[-1].split(".")[0]}</h2>'
                f'<img src="{s}" style="max-width:100%">' for s in strips)
panels = "".join(
    f'<div style="display:inline-block;margin:8px;text-align:center">'
    f'<img src="stills/{f}" style="height:420px"><br><small>{f}</small></div>'
    for _, _, fs in PAGES for f in fs)

(HERE / "_STILLS_REVIEW.html").write_text(f"""<!doctype html><html><head><meta charset="utf-8">
<title>Rung 2 stills gate — In No Wise pages 1/2/4/5</title>
<style>body{{background:#1a1715;color:#e8dfc8;font-family:Georgia,serif;margin:24px}}
h1{{font-size:22px}} h2{{font-size:17px;margin-top:28px}}</style></head><body>
<h1>Rung 2 stills gate — 11 panels, pages 1 / 2 / 4 / 5</h1>
<p>Mockups show each page in its REAL grid geometry (center-cropped like the composite will).
Two failed renders were caught + re-rolled by the executor's self-check (baked text on p1a;
an extra figure on p4a) — kept on disk as *_FAILED.png.</p>
{rows}{sheet}
<h2>All panels, full</h2>{panels}
</body></html>""", encoding="utf-8")
print("gallery built:", HERE / "_STILLS_REVIEW.html")
