"""Build COMIC.html — review the Phase A grid. Rows grouped by subject then style;
columns = models. Lets me compare models within a style and styles within a subject.
Scratchpad only."""
from pathlib import Path

HERE = Path(__file__).parent
COMIC = HERE / "comic"
MODELS = ["seedream_v4_5", "flux_2", "recraft_v4_1"]
STYLES = {"MI_brushink": "MI — seinen brush-ink", "WT_webtoon": "WT — flat webtoon",
          "NR_noir": "NR — noir + accent", "PG_painted": "PG — painted (control)"}
SUBJECTS = {"christ_face": "Christ-face (reverence gate)",
            "joseph_pit": "Joseph in pit (emotion/morph)",
            "joseph_action": "Joseph hauled (hands/crowd)"}

rows = []
for sk, slabel in SUBJECTS.items():
    rows.append(f'<h2 style="margin-top:34px">{slabel}</h2>')
    rows.append('<table><tr><th>style \\ model</th>' +
                "".join(f"<th>{m}</th>" for m in MODELS) + "</tr>")
    for st, stlabel in STYLES.items():
        cells = [f"<th style='text-align:left'>{stlabel}</th>"]
        for m in MODELS:
            f = COMIC / f"{st}__{m}__{sk}.png"
            if f.exists():
                cells.append(f'<td><a href="{f.name}" target="_blank">'
                             f'<img src="comic/{f.name}"></a></td>')
            else:
                cells.append('<td style="color:#a33">missing</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    rows.append("</table>")

html = f"""<!doctype html><meta charset=utf-8><title>Comic bake-off — Phase A</title>
<style>
body{{background:#111;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:24px}}
h1{{margin:0 0 4px}} .sub{{color:#9ab;margin:0 0 18px}}
table{{border-collapse:collapse;margin:8px 0}}
th{{padding:6px 10px;color:#cde;font-weight:600;font-size:14px;vertical-align:bottom}}
td{{padding:4px;border:1px solid #333;vertical-align:top}}
img{{width:240px;height:auto;display:block;border-radius:4px}}
a{{color:#7cf}}
</style>
<h1>Comic look bake-off — Phase A grid</h1>
<p class=sub>4 styles × 3 models × 3 subjects. Click any image for full-res.
Gate columns: reverence (Christ) · emotion/morph (pit) · hands/crowd (hauled).</p>
{''.join(rows)}
"""
out = HERE / "COMIC.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
