"""Face bake-off gallery: rows = looks, cols = the 3 face subjects. See what breaks."""
from pathlib import Path
OUT = Path(__file__).parent
FACES = OUT / "faces"
LOOKS = [("R_chiaroscuro","R · Photoreal chiaroscuro"),("B_engraving","B · Dore engraving"),
         ("D_inknovel","D · Graphic-novel ink"),("F_claymation","F · Claymation"),
         ("G_charcoal","G · Charcoal drawing"),("W_woodcut","W · Durer woodcut")]
SUBJ = [("joseph_pit","Joseph (young) — anguish"),
        ("joseph_weep","Joseph (vizier) — weeping"),
        ("christ_face","Christ — face, front-on")]

rows = []
for lk, llabel in LOOKS:
    cells = [f'<h2>{llabel}</h2>', '<div class="row">']
    for sk, slabel in SUBJ:
        p = FACES / f"{lk}__{sk}.png"
        if p.exists():
            cells.append(f'<figure><img src="faces/{p.name}"><figcaption>{slabel}</figcaption></figure>')
        else:
            cells.append(f'<figure class="missing"><div>…rendering<br>{slabel}</div></figure>')
    cells.append('</div>')
    rows.append("\n".join(cells))

html = f"""<!doctype html><meta charset=utf-8>
<title>Face bake-off — what holds, what breaks (EW03 Joseph)</title>
<style>
 body{{background:#111;color:#eee;font-family:system-ui,Segoe UI,sans-serif;margin:24px;}}
 h1{{font-weight:600}} h2{{margin:34px 0 8px;color:#ffd479}}
 .row{{display:flex;gap:14px;flex-wrap:wrap}}
 figure{{margin:0;width:300px}}
 img{{width:300px;border-radius:8px;display:block;box-shadow:0 4px 18px #000}}
 figcaption{{padding:6px 2px;font-size:14px;color:#bbb}}
 .missing div{{width:300px;height:533px;border:1px dashed #555;border-radius:8px;
   display:flex;align-items:center;justify-content:center;text-align:center;color:#777}}
 p.note{{color:#9bd;max-width:760px}}
</style>
<h1>Face bake-off — what holds emotion, what breaks</h1>
<p class=note>6 looks &times; 3 hardest faces. Realism is rendered to show where it FAILS in close-up,
not to crown it. Watch for: waxy skin, dead eyes, melted hands, uncanny Christ.</p>
{"".join(rows)}
"""
(OUT / "FACES.html").write_text(html, encoding="utf-8")
print("wrote", OUT / "FACES.html")
