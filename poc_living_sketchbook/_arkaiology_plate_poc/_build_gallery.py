"""Build _GALLERY.html for the ArkAIology plate-pack POC (Bronze Serpent).
$0, no API calls -- reflects whatever PNGs exist in plates/.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_arkaiology_plate_poc/_build_gallery.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLATES = HERE / "plates"

CARDS = [
    ("bronze_plate_artifact_hero", "1 · Artifact hero (style_ref)", "The bronze serpent alone, un-gilded, isolated. Generated first; every other plate below is chained to it as an NBP reference."),
    ("bronze_plate_map_wilderness", "2 · Map", "Wilderness route, one gold line, no labels (added later in code)."),
    ("bronze_plate_comparison_split", "3 · Comparison split", "Serpent | gold divider | plain cross -- same pairing as the LONG pilot's own s46_thesis_pair."),
    ("bronze_plate_timeline_backplate", "4 · Timeline backplate", "Reserved for a future Numbers 21 -> 2 Kings 18 -> John 3:14 era timeline."),
    ("bronze_plate_wilderness_dusk", "5 · Wilderness dusk", "Cold-open / closer bookend -- distant camp, reserved sky."),
    ("bronze_plate_big_stat_backplate", "6 · Big-stat backplate", "Reserved for a future callout number; ghosted serpent motif, no number baked in."),
]

CSS = """
  body { background:#16181d; color:#e8e4d8; font-family:Georgia, serif; padding:28px 18px 90px; }
  .wrap { max-width:1400px; margin:0 auto; }
  h1 { color:#e9c877; font-size:1.6rem; margin-bottom:4px; }
  .sub { color:#9aa0ad; margin-bottom:24px; font-size:14px; max-width:90ch; }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(400px,1fr)); gap:18px; }
  .card { background:#1e2129; border-radius:8px; overflow:hidden; border:1px solid #333; }
  .card img { width:100%; display:block; background:#000; }
  .cap { padding:12px 14px; font-size:.9rem; color:#c9c4b6; }
  .cap b { color:#e8e4d8; display:block; margin-bottom:4px; }
"""


def build():
    cards = []
    for stem, title, desc in CARDS:
        png = PLATES / f"{stem}.png"
        if not png.exists():
            continue
        cards.append(f'<div class="card"><img src="plates/{stem}.png"><div class="cap"><b>{title}</b>{desc}</div></div>')
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>ArkAIology plate-pack POC -- Bronze Serpent</title>
<style>{CSS}</style></head><body><div class="wrap">
<h1>ArkAIology plate-pack recipe, tested on Bronze Serpent</h1>
<div class="sub">POC: does the sibling project's "one chained style_ref + flat light + one gold accent"
recipe translate to Bronze Serpent study-companion content? 6/6 clean, zero rerolls. $3.00 total.</div>
<div class="grid">{chr(10).join(cards)}</div>
</div></body></html>"""
    (HERE / "_GALLERY.html").write_text(html, encoding="utf-8")
    print(f"[gallery] {len(cards)} plates -> {HERE / '_GALLERY.html'}")


if __name__ == "__main__":
    build()
