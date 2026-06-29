"""Build a side-by-side compare gallery of the 9 POC stills: rows = beats, cols = looks."""
from pathlib import Path
OUT = Path(__file__).parent
STILLS = OUT / "stills"
LOOKS = [("A", "Cinematic Realism"), ("B", "Doré Engraving"), ("C", "Elemental Macro")]
BEATS = [("M1", "Beat 1 — Betrayal (sold / the pit)"),
         ("M2", "Beat 2 — Mercy (bowed / bread)"),
         ("M3", "Beat 3 — Christ (arms thrown wide)")]

def find(look, beat):
    hits = sorted(STILLS.glob(f"{look}_*_{beat}_*.png"))
    return hits[0] if hits else None

cards = []
for bk, blabel in BEATS:
    row = [f'<h2>{blabel}</h2>', '<div class="row">']
    for lk, llabel in LOOKS:
        p = find(lk, bk)
        if p:
            row.append(f'<figure><img src="stills/{p.name}"><figcaption>{lk} · {llabel}</figcaption></figure>')
        else:
            row.append(f'<figure class="missing"><div>…rendering<br>{lk} · {llabel}</div></figure>')
    row.append('</div>')
    cards.append("\n".join(row))

html = f"""<!doctype html><meta charset=utf-8>
<title>Visual POC — 3 looks bake-off (EW03 Joseph)</title>
<style>
 body{{background:#111;color:#eee;font-family:system-ui,Segoe UI,sans-serif;margin:24px;}}
 h1{{font-weight:600}} h2{{margin:32px 0 8px;color:#ffd479}}
 .row{{display:flex;gap:14px;flex-wrap:wrap}}
 figure{{margin:0;width:300px}}
 img{{width:300px;border-radius:8px;display:block;box-shadow:0 4px 18px #000}}
 figcaption{{padding:6px 2px;font-size:14px;color:#bbb}}
 .missing div{{width:300px;height:533px;border:1px dashed #555;border-radius:8px;
   display:flex;align-items:center;justify-content:center;text-align:center;color:#777}}
</style>
<h1>Visual uniqueness POC — Joseph (oil look set aside)</h1>
<p>Same 3 story beats, three candidate looks. Pick what feels fresh + not AI-slop.</p>
{"".join(cards)}
"""
(OUT / "GALLERY.html").write_text(html, encoding="utf-8")
print("wrote", OUT / "GALLERY.html")
