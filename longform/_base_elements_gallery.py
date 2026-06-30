#!/usr/bin/env python
"""Build a browser review gallery of the rendered base-element reference images.

Scans ref_library/{characters,objects,places,motifs}/*.png and lays them out as
cards (image + name + kind/block + canonical). $0. Run after a render batch.

  .venv\\Scripts\\python.exe longform\\_base_elements_gallery.py
  -> ref_library/_gallery.html
"""
import html, json, os
from pathlib import Path

LIB = Path(__file__).resolve().parents[1] / "ref_library"
SUBS = [("characters", "CHARACTER"), ("objects", "OBJECT"),
        ("places", "PLACE"), ("motifs", "MOTIF")]


def main():
    cards = {c["name"]: c for c in json.load(open(LIB / "cards" / "cards.json", encoding="utf-8"))}
    sections, total = [], 0
    for sub, label in SUBS:
        d = LIB / sub
        if not d.exists():
            continue
        pngs = sorted(d.glob("*.png"))
        if not pngs:
            continue
        cells = []
        for p in pngs:
            name = p.stem
            c = cards.get(name, {})
            canon = html.escape(c.get("canonical", ""))
            block = c.get("block", "")
            rel = f"{sub}/{p.name}"
            cells.append(
                f'<figure><img src="{rel}" loading="lazy">'
                f'<figcaption><b>{html.escape(name)}</b> '
                f'<span class="blk">{html.escape(block)}</span>'
                f'<div class="c">{canon}</div></figcaption></figure>')
            total += 1
        sections.append(f'<h2>{label} <span class="muted">({len(pngs)})</span></h2>'
                        f'<div class="grid">{"".join(cells)}</div>')

    doc = f"""<!doctype html><meta charset="utf-8">
<title>Awakeden Base-Elements — rendered refs</title>
<style>
 body{{font:14px system-ui,Segoe UI,Arial;margin:22px;background:#15171c;color:#eee}}
 h1{{margin:0 0 12px}} .muted{{color:#8a93a6;font-weight:400}}
 h2{{margin:26px 0 8px;border-bottom:1px solid #333;padding-bottom:4px}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}}
 figure{{margin:0;background:#1d2027;border:1px solid #2c313b;border-radius:10px;overflow:hidden}}
 img{{width:100%;display:block;background:#000;aspect-ratio:9/16;object-fit:cover}}
 figcaption{{padding:8px 10px;font-size:12px}}
 .blk{{color:#7fd1a8;font-size:11px;border:1px solid #2c5;border-radius:5px;padding:1px 5px;margin-left:4px}}
 .c{{color:#aeb6c4;margin-top:5px;font-size:11px;line-height:1.4;max-height:6.5em;overflow:auto}}
</style>
<h1>Awakeden Base-Elements — rendered references <span class="muted">({total})</span></h1>
{''.join(sections)}
"""
    out = LIB / "_gallery.html"
    out.write_text(doc, encoding="utf-8")
    print(f"{total} refs -> {out}")


if __name__ == "__main__":
    main()
