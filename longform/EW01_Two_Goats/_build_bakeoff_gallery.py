"""Bake-off gallery: 3 subjects x 2 styles, side by side (2026-07-23)."""
from pathlib import Path

OUT = Path(__file__).resolve().parent / "_style_bakeoff"
HTML = OUT / "_BAKEOFF.html"
SUBJECTS = [("jesus", "Jesus — as himself"), ("cross", "Jesus — on the cross"),
            ("noah", "Noah — ark, rainbow, animals")]


def uri(name):
    p = OUT / name
    return p.resolve().as_uri() if p.exists() else ""


def cell(name):
    u = uri(name)
    return f"<img src='{u}'>" if u else "<div class='miss'>rendering…</div>"


def main():
    rows = []
    for key, title in SUBJECTS:
        rows.append(f"""
        <div class='row'>
          <div class='ti'>{title}</div>
          <div class='pair'>
            <figure><figcaption>INKED (old look)</figcaption>{cell(f'{key}_inked.png')}</figure>
            <figure><figcaption>PAINTED (new look)</figcaption>{cell(f'{key}_painted.png')}</figure>
          </div>
        </div>""")
    html = f"""<!doctype html><meta charset=utf-8>
<title>Style bake-off — inked vs painted</title>
<style>
 body{{background:#14110d;color:#f0e9dc;font-family:system-ui,Arial;margin:0;padding:26px}}
 h1{{font-size:22px;margin:0 0 4px}} p.sub{{color:#b7ab97;margin:0 0 24px}}
 .row{{margin:0 0 34px}} .ti{{font-size:18px;color:#e9c877;font-weight:700;margin:0 0 8px}}
 .pair{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
 figure{{margin:0}} figcaption{{font-size:13px;color:#b7ab97;margin:0 0 5px;letter-spacing:1px}}
 img{{width:100%;border-radius:7px;display:block;box-shadow:0 5px 20px rgba(0,0,0,.5)}}
 .miss{{padding:70px;text-align:center;background:#221e18;border-radius:7px;color:#8a7f6c}}
 @media(max-width:900px){{.pair{{grid-template-columns:1fr}}}}
</style>
<h1>Style bake-off — which look is better?</h1>
<p class='sub'>Same 3 subjects. Left = OLD inked. Right = NEW painted. Pick the column you like.</p>
{''.join(rows)}
"""
    HTML.write_text(html, encoding="utf-8")
    print(f"file:///{str(HTML).replace(chr(92), '/')}")


if __name__ == "__main__":
    main()
