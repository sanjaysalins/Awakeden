"""Comic v6 preview frames ($0, PIL only). Run:
  .venv\\Scripts\\python.exe prophecy\\01_bethlehem\\comic_v6\\make_previews.py
Draws at 2x and scales down. Clean clip frames live in _frames/ (pulled with ffmpeg)."""
import math, random
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = Path(__file__).parent
FR = HERE / "_frames"
PUB = HERE.parents[2] / "_remotion" / "public"
S = 2
W, H = 1080 * S, 1920 * S
INK = (20, 16, 14, 255)
GOLD = (246, 185, 35, 255)
CREAM = (250, 243, 224, 255)
PAPER = (247, 244, 236, 255)
CAP_Y = (255, 214, 74, 255)


def font(name, px):
    return ImageFont.truetype(str(PUB / name), int(px * S))


def base(name):
    return Image.open(FR / name).convert("RGBA").resize((W, H), Image.LANCZOS)


def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def sc(pts):
    return [(x * S, y * S) for x, y in pts]


def wob_poly(box, seed, amp=2.2, step=40):
    """Hand-wobbled rectangle outline points (1x coords in, 2x out)."""
    r = random.Random(seed)
    x0, y0, x1, y1 = box
    pts = []
    def edge(ax, ay, bx, by):
        n = max(2, int(math.hypot(bx - ax, by - ay) / step))
        for i in range(n):
            t = i / n
            pts.append((ax + (bx - ax) * t + r.uniform(-amp, amp), ay + (by - ay) * t + r.uniform(-amp, amp)))
    edge(x0, y0, x1, y0); edge(x1, y0, x1, y1); edge(x1, y1, x0, y1); edge(x0, y1, x0, y0)
    pts.append(pts[0])
    return sc(pts)


def ink_frame(img, box, width=7, color=INK, seed=1, dashed=False):
    l = layer(); d = ImageDraw.Draw(l)
    pts = wob_poly(box, seed)
    if dashed:
        for i in range(0, len(pts) - 1, 2):
            d.line([pts[i], pts[i + 1]], fill=color, width=int(width * S))
    else:
        d.line(pts, fill=color, width=int(width * S), joint="curve")
    return Image.alpha_composite(img, l)


def halftone(box, color, r_top, r_bot, pitch=11, alpha=255):
    """45-degree dot screen inside box; dot radius runs r_top -> r_bot (1x px)."""
    x0, y0, x1, y1 = [int(v * S) for v in box]
    l = layer(); d = ImageDraw.Draw(l)
    p = pitch * S
    row = 0
    y = y0
    while y < y1:
        t = (y - y0) / max(1, y1 - y0)
        rad = (r_top + (r_bot - r_top) * t) * S
        if rad > 0.4:
            x = x0 + (p / 2 if row % 2 else 0)
            while x < x1:
                d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=color[:3] + (alpha,))
                x += p
        y += p / 2
        row += 1
    return l


def shade(img, box, rgba):
    l = layer(); ImageDraw.Draw(l).rectangle([v * S for v in box], fill=rgba)
    return Image.alpha_composite(img, l)


def text_tilt(img, cx, cy, text, fnt, fill, stroke=10, stroke_fill=INK, rot=0, shadow=(8, 10), parts=None):
    """Outlined comic display lettering, centred on (cx, cy), with a hard ink drop shadow."""
    tmp = Image.new("RGBA", (W, int(H / 3)), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    parts = parts or [(text, fill)]
    total = sum(d.textlength(t, font=fnt) for t, _ in parts)
    x = (W - total) / 2; y = tmp.height / 2
    for dx, dy, shadow_pass in ((shadow[0] * S, shadow[1] * S, True), (0, 0, False)):
        xx = x
        for t, c in parts:
            d.text((xx + dx, y + dy), t, font=fnt, anchor="lm", fill=INK if shadow_pass else c,
                   stroke_width=int(stroke * S), stroke_fill=INK if shadow_pass else stroke_fill)
            xx += d.textlength(t, font=fnt)
    tmp = tmp.rotate(rot, resample=Image.BICUBIC, expand=True)
    l = layer(); l.alpha_composite(tmp, (int(cx * S - tmp.width / 2), int(cy * S - tmp.height / 2)))
    return Image.alpha_composite(img, l)


def burst(img, cx, cy, r_in, r_out, n=14, fill=GOLD, outline=INK, ow=6, seed=3, rot=0):
    r = random.Random(seed); pts = []
    for i in range(n * 2):
        a = rot + math.pi * i / n
        rad = (r_out * r.uniform(0.82, 1.12)) if i % 2 == 0 else (r_in * r.uniform(0.9, 1.1))
        pts.append((cx + math.cos(a) * rad, cy + math.sin(a) * rad))
    l = layer(); d = ImageDraw.Draw(l); p = sc(pts)
    d.polygon(p, fill=fill); d.line(p + [p[0]], fill=outline, width=int(ow * S), joint="curve")
    return Image.alpha_composite(img, l)


def speed_lines(img, box, origin, n=46, color=(255, 255, 255, 235), seed=5, inner=0.45):
    """Radial speed wedges clipped to box, pointing at origin (1x)."""
    r = random.Random(seed); l = layer(); d = ImageDraw.Draw(l)
    ox, oy = origin; R = 2400
    for i in range(n):
        a = r.uniform(0, math.tau); w = r.uniform(0.004, 0.016); r0 = R * r.uniform(inner * 0.2, inner * 0.42)
        d.polygon(sc([(ox + math.cos(a) * r0, oy + math.sin(a) * r0),
                      (ox + math.cos(a - w) * R, oy + math.sin(a - w) * R),
                      (ox + math.cos(a + w) * R, oy + math.sin(a + w) * R)]), fill=color)
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rectangle([v * S for v in box], fill=255)
    l.putalpha(ImageChops.multiply(l.getchannel("A"), m))
    return Image.alpha_composite(img, l)


def footprint(img, cx, cy, size, ang_deg, gold=False, ticks=False):
    """One shoe print. Hollow dashed = a step not taken. Gold with ink outline = a step taken."""
    w = int(size * S * 3); t = Image.new("RGBA", (w, w), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    c = w / 2; a = size * S
    sole = [c - a * 0.5, c - a * 1.05, c + a * 0.5, c + a * 0.25]
    heel = [c - a * 0.36, c + a * 0.38, c + a * 0.36, c + a * 1.02]
    if gold:
        for b in (sole, heel):
            d.ellipse(b, fill=GOLD, outline=INK, width=max(3, int(a * 0.13)))
        d.ellipse([c - a * 0.25, c - a * 0.8, c - a * 0.02, c - a * 0.45], fill=(255, 240, 170, 255))
    else:
        for b in (sole, heel):
            d.ellipse(b, fill=(10, 14, 30, 120), outline=INK, width=max(5, int(a * 0.26)))
            for k in range(0, 360, 36):
                d.arc(b, k, k + 22, fill=(255, 255, 255, 255), width=max(3, int(a * 0.14)))
    t = t.rotate(-ang_deg, resample=Image.BICUBIC)
    l = layer(); l.alpha_composite(t, (int(cx * S - w / 2), int(cy * S - w / 2)))
    if ticks and gold:  # three little action ticks behind the heel
        d2 = ImageDraw.Draw(l); rad = math.radians(ang_deg)
        bx, by = cx - math.sin(rad) * -size * 1.5, cy + math.cos(rad) * size * 1.5
        for k in (-0.5, 0, 0.5):
            dx, dy = math.sin(rad + k) * size * 0.9, -math.cos(rad + k) * size * 0.9
            d2.line(sc([(bx - dx * 0.2, by - dy * 0.2), (bx - dx, by - dy)]), fill=(255, 255, 255, 255), width=int(max(3, size * 0.14) * S))
    return Image.alpha_composite(img, l)


def trail(img, pts, sizes, gold_upto=0, ticks=False):
    for i, ((x, y), s) in enumerate(zip(pts, sizes)):
        nx, ny = pts[min(i + 1, len(pts) - 1)]; px, py = pts[max(i - 1, 0)]
        ang = math.degrees(math.atan2(nx - px, -(ny - py)))
        off = (s * 0.55) * (1 if i % 2 else -1); rad = math.radians(ang)
        img = footprint(img, x + math.cos(rad) * off, y + math.sin(rad) * off, s, ang, gold=i < gold_upto, ticks=ticks)
    return img


def pill(img, cy, lines, hi=(), said=None, top_tab=None):
    """Owner-locked Mockers pill: see-through, rounded, Kalam. hi = words boxed in gold."""
    f = font("Kalam-Bold.ttf", 54); l = layer(); d = ImageDraw.Draw(l)
    h = 46 + 62 * len(lines); x0, x1 = 100, 980; y0 = cy - h / 2
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, (y0 + h) * S], radius=46 * S, fill=(244, 242, 236, 178), outline=(20, 16, 14, 150), width=4 * S)
    for li, line in enumerate(lines):
        words = line.split(" "); sp = d.textlength(" ", font=f)
        tw = sum(d.textlength(w, font=f) for w in words) + sp * (len(words) - 1)
        x = 540 * S - tw / 2; y = (y0 + 23 + 62 * li + 31) * S
        for w in words:
            ww = d.textlength(w, font=f)
            if w.strip(".,:?") in hi:
                d.rounded_rectangle([x - 8 * S, y - 30 * S, x + ww + 8 * S, y + 30 * S], radius=10 * S, fill=GOLD)
            d.text((x, y), w, font=f, anchor="lm", fill=INK if (said is None or w in said) else (20, 16, 14, 120))
            x += ww + sp
    img = Image.alpha_composite(img, l)
    return img


def chip(img, x, y, text, fill=GOLD, rot=0, px=28, fnt="Kalam-Bold.ttf", pad=14, hh=42, radius=16, fg=INK):
    f = font(fnt, px); d0 = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    tw = d0.textlength(text, font=f); w = int(tw + pad * 2 * S); h = int(hh * S)
    t = Image.new("RGBA", (w + 16 * S, h + 16 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rounded_rectangle([4 * S + 4 * S, 4 * S + 5 * S, w + 8 * S, h + 9 * S], radius=radius * S, fill=INK)  # hard ink shadow
    d.rounded_rectangle([4 * S, 4 * S, w + 4 * S, h + 4 * S], radius=radius * S, fill=fill, outline=INK, width=3 * S)
    d.text((4 * S + w / 2, 4 * S + h / 2), text, font=f, anchor="mm", fill=fg)
    t = t.rotate(rot, resample=Image.BICUBIC, expand=True)
    l = layer(); l.alpha_composite(t, (int(x * S), int(y * S)))
    return Image.alpha_composite(img, l), (w / S + 8)


def caption_box(img, x, y, text, rot=-2, px=40):
    """Small yellow comic place-caption (square corners, ink border, hard shadow)."""
    return chip(img, x, y, text, fill=CAP_Y, rot=rot, px=px, fnt="Bangers.ttf", pad=16, hh=58, radius=3)[0]


def print_grade(img, seed=9):
    """Cheap stand-in for panel_animator/print_grade: paper grain + faint dot screen in the darks."""
    rng = np.random.default_rng(seed)
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    g = rng.normal(0, 5.0, (H // 2, W // 2)).astype(np.float32)
    g = np.asarray(Image.fromarray(g).resize((W, H), Image.BILINEAR))
    lum = a.mean(2, keepdims=True) / 255.0
    yy, xx = np.mgrid[0:H, 0:W]
    p = 7 * S
    dots = ((((xx + yy) % p) - p / 2) ** 2 + (((xx - yy) % p) - p / 2) ** 2) < (1.5 * S) ** 2
    a = a + g[..., None] + dots[..., None] * (1 - lum) * 16
    a = a * np.array([1.01, 0.995, 0.96], dtype=np.float32)  # warm paper
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


def finish(img, out):
    img = print_grade(img).resize((1080, 1920), Image.LANCZOS).convert("RGB")
    img.save(HERE / out); print("wrote", HERE / out)


# ---------------------------------------------------------------- the map PANEL (ink + flat colour + dots)
def map_panel(img, box, gold_upto=0, ticks=False, seed=2):
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    l = layer(); d = ImageDraw.Draw(l)
    for i in range(int(h * S)):  # night gradient, same family as the painted road panel
        t = i / (h * S)
        d.line([(x0 * S, y0 * S + i), (x1 * S, y0 * S + i)], fill=(int(30 - 14 * t), int(52 - 26 * t), int(118 - 52 * t), 255))
    img = Image.alpha_composite(img, l)
    img = Image.alpha_composite(img, halftone((x0, y0, x1, y0 + h * 0.55), (86, 124, 214), 3.4, 0.0, pitch=13, alpha=150))
    l = layer(); d = ImageDraw.Draw(l); r = random.Random(seed)
    # the Dead Sea, right edge
    sea = [(x1 - 105 + math.cos(a) * (52 + 14 * math.sin(a * 3)) + 18 * math.sin(a), y0 + h * 0.42 + math.sin(a) * h * 0.33) for a in [i * math.tau / 40 for i in range(40)]]
    d.polygon(sc(sea), fill=(42, 150, 170, 255)); d.line(sc(sea + [sea[0]]), fill=INK, width=7 * S, joint="curve")
    # hills: chunky inked comic mountains, light side + shadow side
    for hx, hy, hs in [(110, 120, 60), (230, 330, 46), (90, 470, 54), (640, 110, 50), (820, 560, 44), (520, 330, 40), (300, 560, 50), (760, 250, 36)]:
        cx, cy = x0 + hx, y0 + hy
        d.polygon(sc([(cx - hs, cy + hs * 0.7), (cx, cy - hs * 0.7), (cx + hs, cy + hs * 0.7)]), fill=(52, 84, 160, 255))
        d.polygon(sc([(cx, cy - hs * 0.7), (cx + hs, cy + hs * 0.7), (cx + hs * 0.15, cy + hs * 0.7)]), fill=(14, 22, 54, 255))
        d.line(sc([(cx - hs, cy + hs * 0.7), (cx, cy - hs * 0.7), (cx + hs, cy + hs * 0.7)]), fill=INK, width=7 * S, joint="curve")
    jx, jy = x0 + 300, y0 + h * 0.30   # Jerusalem
    bx, by = x0 + 690, y0 + h * 0.72   # Bethlehem
    # the short road: pale band with ink edges
    road = [(jx + 20, jy + 70), (jx + 90, jy + 130), (jx + 200, jy + 150), (bx - 190, by - 110), (bx - 110, by - 40), (bx - 20, by + 10)]
    d.line(sc(road), fill=INK, width=96 * S, joint="curve"); d.line(sc(road), fill=(106, 132, 196, 255), width=80 * S, joint="curve")

    def town(cx, cy, k, big):
        body = (226, 168, 66, 255); dark = (150, 96, 40, 255)
        bw, bh = 150 * k, 70 * k
        d.rectangle(sc([(cx - bw, cy - bh), (cx + bw, cy + bh)]), fill=body, outline=INK, width=7 * S)
        d.rectangle(sc([(cx + bw * 0.35, cy - bh), (cx + bw, cy + bh)]), fill=dark, outline=INK, width=7 * S)
        n = 7 if big else 4
        for i in range(n):  # battlements
            xx = cx - bw + (2 * bw) * i / n
            d.rectangle(sc([(xx + 4, cy - bh - 22 * k), (xx + (2 * bw) / n - 10, cy - bh)]), fill=body if i < n * 0.66 else dark, outline=INK, width=6 * S)
        d.pieslice(sc([(cx - 34 * k, cy - 20 * k), (cx + 34 * k, cy + bh * 2)]), 180, 360, fill=(20, 16, 14, 255))  # gate
        if big:
            d.pieslice(sc([(cx - bw * 0.7, cy - bh - 86 * k), (cx - bw * 0.1, cy - bh + 30 * k)]), 180, 360, fill=(240, 196, 92, 255), outline=INK, width=7 * S)
            d.rectangle(sc([(cx + bw * 0.5, cy - bh - 70 * k), (cx + bw * 0.8, cy - bh)]), fill=dark, outline=INK, width=7 * S)
        else:
            d.polygon(sc([(cx - bw * 0.5, cy - bh - 4), (cx, cy - bh - 70 * k), (cx + bw * 0.5, cy - bh - 4)]), fill=body, outline=INK)
            d.line(sc([(cx - bw * 0.5, cy - bh - 4), (cx, cy - bh - 70 * k), (cx + bw * 0.5, cy - bh - 4)]), fill=INK, width=7 * S, joint="curve")
        for i in range(3 if big else 2):  # lit windows
            wx = cx - bw * 0.75 + i * bw * 0.42
            d.rectangle(sc([(wx, cy - bh * 0.5), (wx + 16 * k, cy - bh * 0.5 + 24 * k)]), fill=(255, 236, 150, 255), outline=INK, width=4 * S)
    town(jx, jy, 1.0, True); town(bx, by + 40, 0.72, False)
    img = Image.alpha_composite(img, l)
    img = Image.alpha_composite(img, halftone((jx + 52, jy - 70, jx + 150, jy + 70), (20, 16, 14), 2.2, 3.4, pitch=10, alpha=120))
    img = burst(img, bx, by - 70, 20, 52, n=8, fill=GOLD, ow=5, seed=4, rot=0.2)   # the star over Bethlehem
    pts = [road[0]] ; segs = list(zip(road[:-1], road[1:]))
    L = [math.dist(a, b) for a, b in segs]; tot = sum(L)
    pts = []
    for k in range(7):  # 7 prints, evenly spaced along the road
        t = tot * (0.10 + 0.80 * k / 6); i = 0
        while t > L[i]: t -= L[i]; i += 1
        (ax, ay), (bx2, by2) = segs[i]; pts.append((ax + (bx2 - ax) * t / L[i], ay + (by2 - ay) * t / L[i]))
    img = trail(img, pts, [27] * 7, gold_upto=gold_upto, ticks=ticks)
    map_panel.pts = pts
    img = caption_box(img, jx - 285, jy + 88, "JERUSALEM", rot=-2)
    img = caption_box(img, bx - 370, by + 50, "BETHLEHEM", rot=1.5)
    return img


# ---------------------------------------------------------------- 1. the hook: "Did they go?"
def p1():
    img = base("clip_P1_3.6.png")
    road = (8, 1257, 1072, 1914)
    img = ink_frame(img, road, width=9, seed=11)
    pts = [(520, 1850), (575, 1770), (650, 1705), (745, 1668), (772, 1622), (700, 1588), (742, 1560)]
    img = trail(img, pts, [58, 49, 41, 33, 26, 20, 15])
    f = font("Bangers.ttf", 168)
    img = text_tilt(img, 520, 1352, "", f, CREAM, stroke=11, rot=4, parts=[("DID THEY ", CREAM), ("GO?", GOLD)])
    finish(img, "preview_1.png")


# ---------------------------------------------------------------- 2. "Bethlehem was close by." (the map is a PANEL)
def p2():
    img = base("clip_P1_2.6.png")
    box = (8, 598, 1072, 1249)
    img = shade(img, (0, 580, 1080, 1268), PAPER)
    img = map_panel(img, box, gold_upto=0)
    img = ink_frame(img, box, width=9, seed=21)
    img = pill(img, 1322, ["Bethlehem was close by."], hi=("Bethlehem",))
    finish(img, "preview_2.png")


# ---------------------------------------------------------------- 3. "There, God's promise came true" (sacred: no slam)
def p3():
    img = base("clip_P3_1.5.png")
    # rack focus: the two lower panels step back under a blue dot screen. Nothing touches the manger.
    for b in ((0, 639, 1080, 1294), (0, 1310, 1080, 1920)):
        img = shade(img, b, (12, 18, 46, 120))
        img = Image.alpha_composite(img, halftone(b, (10, 14, 34), 2.6, 2.6, pitch=11, alpha=130))
    # the Promise Panel: the dashed frame from Micah's beat is now one solid gold line, drawn on slowly
    box = (10, 8, 1070, 622)
    img = ink_frame(img, box, width=15, color=INK, seed=31)
    img = ink_frame(img, box, width=9, color=GOLD, seed=31)
    img, w1 = chip(img, 40, 602, "MICAH 5:2")
    img, _ = chip(img, 40 + w1 + 6, 602, "CAME TRUE", fill=CREAM)
    img = pill(img, 760, ["There, God's promise", "came true:"], hi=("came", "true"))
    finish(img, "preview_3.png")


# ---------------------------------------------------------------- 4. the slam: "The wise men WENT"
def p4():
    img = base("clip_P1_7.9.png")
    box = (8, 390, 1072, 1163)
    img = shade(img, (0, 368, 1080, 1186), PAPER)
    img = map_panel(img, box, gold_upto=4, ticks=True)
    # the print landing right now gets the impact burst (panel_animator/impact_burst)
    hx, hy = map_panel.pts[4]
    img = burst(img, hx, hy, 46, 96, n=11, fill=(255, 255, 255, 255), ow=5, seed=6)
    img = footprint(img, hx, hy, 30, 120, gold=True)
    img = ink_frame(img, box, width=9, seed=41)
    # the camel panel SLAMS in over the experts, tilted, and breaks the map panel's top border
    cam = Image.open(FR / "clip_P3_4.5.png").convert("RGBA").crop((0, 584, 1080, 1312)).resize((int(1010 * S), int(680 * S * 1010 / 1080 * 1080 / 1010 * 0.935)), Image.LANCZOS)
    cw, ch = cam.size
    card = Image.new("RGBA", (cw + 40 * S, ch + 40 * S), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rectangle([26 * S, 30 * S, cw + 38 * S, ch + 40 * S], fill=INK)                 # hard ink drop shadow
    cd.rectangle([0, 0, cw + 20 * S, ch + 20 * S], fill=PAPER, outline=INK, width=4 * S)  # white gutter
    card.alpha_composite(cam, (10 * S, 10 * S))
    cd.rectangle([10 * S, 10 * S, cw + 10 * S, ch + 10 * S], outline=INK, width=8 * S)
    card = card.rotate(3.2, resample=Image.BICUBIC, expand=True)
    img = speed_lines(img, (0, 0, 1080, 380), (540, 200), n=70, color=(255, 255, 255, 215), seed=12)
    l = layer(); l.alpha_composite(card, (int(8 * S), int(-250 * S))); img = Image.alpha_composite(img, l)
    f = font("Bangers.ttf", 150)
    img = text_tilt(img, 810, 372, "WENT", f, GOLD, stroke=10, rot=-7)
    img = pill(img, 1178, ["The wise men went,"], hi=("went",))
    finish(img, "preview_4.png")


if __name__ == "__main__":
    p1(); p2(); p3(); p4()
