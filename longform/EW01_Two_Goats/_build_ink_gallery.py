"""Ink-variants bake-off gallery: 6 ink styles, same subject (Jesus)."""
from pathlib import Path

OUT = Path(__file__).resolve().parent / "_ink_bakeoff"
HTML = OUT / "_INK_BAKEOFF.html"
STYLES = [("clean_comic", "1 · Clean comic (baseline)"), ("ligne_claire", "2 · Ligne claire (clean-line)"),
          ("comic_halftone", "3 · Retro comic + halftone dots"), ("woodcut", "4 · Woodcut / engraving"),
          ("noir_spot", "5 · Noir B&W + spot red"), ("heavy_black", "6 · Heavy-black brush"),
          ("colour_woodcut", "7 · Colour woodcut / lino"), ("ink_watercolour", "8 · Ink + watercolour wash"),
          ("duotone", "9 · Duotone (black + crimson)"), ("sumi_e", "10 · Sumi-e brush"),
          ("scratchboard", "11 · Scratchboard (white-on-black)"), ("illuminated", "12 · Illuminated + gold")]


def main():
    cards = []
    for name, label in STYLES:
        p = OUT / f"{name}.png"
        u = p.resolve().as_uri() if p.exists() else ""
        img = f"<img src='{u}'>" if u else "<div class='miss'>rendering…</div>"
        cards.append(f"<figure><figcaption>{label}</figcaption>{img}</figure>")
    html = f"""<!doctype html><meta charset=utf-8>
<title>Ink styles bake-off</title>
<style>
 body{{background:#14110d;color:#f0e9dc;font-family:system-ui,Arial;margin:0;padding:26px}}
 h1{{font-size:22px;margin:0 0 4px}} p.sub{{color:#b7ab97;margin:0 0 22px}}
 .grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
 figure{{margin:0}} figcaption{{font-size:15px;color:#e9c877;font-weight:700;margin:0 0 6px}}
 img{{width:100%;border-radius:7px;display:block;box-shadow:0 5px 20px rgba(0,0,0,.5)}}
 .miss{{padding:80px;text-align:center;background:#221e18;border-radius:7px;color:#8a7f6c}}
 @media(max-width:820px){{.grid{{grid-template-columns:1fr}}}}
</style>
<h1>Ink styles — same Jesus, 6 different ink looks</h1>
<p class='sub'>Pick the number you like best. Then I test it on more subjects.</p>
<div class='grid'>{''.join(cards)}</div>
"""
    HTML.write_text(html, encoding="utf-8")
    print(f"file:///{str(HTML).replace(chr(92), '/')}")


if __name__ == "__main__":
    main()
