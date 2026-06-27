"""Build a review gallery of an episode's world-locked stills (id, title, which face-lock).
Usage: python _world_gallery.py EW01_Two_Goats"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _episode import resolve

ep = resolve(sys.argv)
cards = []
for s in ep.scenes:
    png = ep.png(s)
    refs = ", ".join(s.get("refs", [])) or "—"
    exists = png.exists()
    cls = "lock" if s.get("refs") else "free"
    src = png.name if exists else ""
    body = (f'<img src="{src}" loading="lazy">' if exists
            else '<div class="miss">not rendered</div>')
    cards.append(f"""<div class="card">
      <div class="h"><span class="n">#{s['id']:02d}</span><span class="r {cls}">{refs}</span></div>
      {body}<div class="t">{s['title']}</div></div>""")

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>{ep.slug} — world stills</title>
<style>
 body{{margin:0;background:#12131a;color:#e9e7e1;font-family:system-ui,Segoe UI,sans-serif}}
 header{{padding:16px 22px;background:#1a1c26;border-bottom:1px solid #333}}
 h1{{margin:0;font-size:18px}} p{{margin:6px 0 0;color:#9aa;font-size:13px}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px;padding:20px}}
 .card{{background:#1a1c26;border:1px solid #2c3140;border-radius:10px;overflow:hidden}}
 .card img{{width:100%;display:block;background:#000;aspect-ratio:16/9;object-fit:cover}}
 .miss{{aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;color:#666;background:#0c0d12}}
 .h{{display:flex;gap:8px;padding:8px 10px;align-items:center}}
 .n{{font-weight:700;color:#ffd479}}
 .r{{margin-left:auto;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:2px 8px;border-radius:20px}}
 .r.lock{{background:#1f3a2a;color:#8ce0a8}} .r.free{{background:#2a2f3d;color:#9aa}}
 .t{{padding:8px 10px;font-size:13px;color:#cfd2da;min-height:34px}}
</style></head><body>
<header><h1>{ep.title} — world-locked stills ({sum(1 for s in ep.scenes if ep.png(s).exists())}/{len(ep.scenes)})</h1>
<p>Green tag = a locked face attached (aaron / christ). Open each full-size to QC consistency, anatomy, period, signatures.</p></header>
<div class="grid">{''.join(cards)}</div></body></html>"""
out = ep.out / "_world_gallery.html"
out.write_text(html, encoding="utf-8")
print(out)
