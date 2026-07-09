#!/usr/bin/env python3
"""Generate per-study 1200x630 social share cards (assets/og/<slug>.jpg).

LOCAL tool — needs the source paintings (gitignored media), so it is NOT run by
Netlify. Run it locally whenever a preview_source changes, then commit the cards:

  python _website/make_og_cards.py
  git add _website/assets/og/

build_catalog.py references assets/og/<slug>.jpg when it exists, else falls back
to the global assets/og-cover.jpg.
"""
from __future__ import annotations

from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import build_catalog as bc

SITE = Path(__file__).resolve().parent
OUT = SITE / "assets" / "og"
W, H = 1200, 630
BONE = (236, 234, 228)
RED = (229, 48, 61)
CREAM = (244, 239, 230)
DIM = (180, 170, 150)


def font(bold: bool, size: int) -> ImageFont.FreeTypeFont:
    name = "georgiab.ttf" if bold else "georgia.ttf"
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
    except OSError:
        return ImageFont.load_default()


def font_black(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", size)
    except OSError:
        return font(True, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def resolve(item) -> Path | None:
    src = bc.resolve_source(item.get("preview_source") or "")
    if src and src.name == "scene_plan.json":
        src = bc.find_hero_png_from_scene_plan(src) or src
    if src and src.suffix.lower() in (".png", ".jpg", ".jpeg") and src.is_file():
        return src
    return None


def card(src: Path, title: str, ref: str, out: Path) -> None:
    art = Image.open(src).convert("RGB")
    # blurred, darkened ambient background (cover-fit)
    sw, sh = art.size
    scale = max(W / sw, H / sh)
    bg = art.resize((int(sw * scale), int(sh * scale)), Image.LANCZOS)
    bx, by = (bg.width - W) // 2, (bg.height - H) // 2
    bg = bg.crop((bx, by, bx + W, by + H)).filter(ImageFilter.GaussianBlur(20))
    bg = Image.composite(Image.new("RGB", (W, H), (8, 7, 10)), bg, Image.new("L", (W, H), 150))
    # crisp full painting on the left (contain)
    box_w, box_h = 360, 500
    a = art.copy()
    a.thumbnail((box_w, box_h), Image.LANCZOS)
    ax, ay = 80, (H - a.height) // 2
    bg.paste(a, (ax, ay))
    d = ImageDraw.Draw(bg)
    d.rectangle([ax - 1, ay - 1, ax + a.width, ay + a.height], outline=BONE, width=2)
    # text panel on the right: the AWAK|EDEN two-colour mark (new dress)
    tx = ax + box_w + 70
    kicker = font_black(30)
    d.text((tx, 150), "AWAK", font=kicker, fill=BONE)
    d.text((tx + d.textlength("AWAK", font=kicker), 150), "EDEN", font=kicker, fill=RED)
    y = 205
    for line in wrap(d, title, font(True, 52), W - tx - 70):
        d.text((tx, y), line, font=font(True, 52), fill=CREAM)
        y += 64
    d.text((tx, y + 12), ref, font=font(False, 30), fill=DIM)
    out.parent.mkdir(parents=True, exist_ok=True)
    bg.save(out, "JPEG", quality=86)


def main() -> int:
    manifest = yaml.safe_load((SITE / "manifest.yaml").read_text(encoding="utf-8"))
    made = 0
    for item in manifest.get("items", []):
        src = resolve(item)
        if not src:
            print(f"  skip {item['slug']} (no source painting)")
            continue
        card(src, item["title"], item.get("ref", ""), OUT / f"{item['slug']}.jpg")
        made += 1
        print(f"  card {item['slug']} <- {src.name}")
    print(f"Wrote {made} share cards -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
