"""Build one combined review gallery: stills + shipping clips for #02/#03/#04/#06,
scroll scenes badged so the user can review before any re-render spend. $0/offline."""
from pathlib import Path

ROOT = Path(__file__).parent
SHORTS = [
    ("02_The_Mockers_Words", "The Mockers' Words"),
    ("03_The_Forsaken_Cry", "The Forsaken Cry"),
    ("04_Declared_To_The_Brethren", "Declared To The Brethren"),
    ("06_The_Ends_Of_The_Earth", "The Ends Of The Earth"),
]
# scene-number -> (badge, note)
FLAGS = {
    "02_The_Mockers_Words": {2: ("warn", "lamp scroll - smaller text, borderline"),
                              3: ("bad", "garbled pseudo-Hebrew + big thumb"),
                              12: ("warn", "thousand-years diptych scroll - borderline")},
    "03_The_Forsaken_Cry": {2: ("warn", "lamp scroll - borderline"),
                             3: ("bad", "dense garbled Hebrew"),
                             12: ("warn", "thousand-years diptych scroll - borderline")},
    "04_Declared_To_The_Brethren": {2: ("warn", "psalm-turns scroll - borderline"),
                                     3: ("bad", "garbled letters on scroll"),
                                     7: ("ok", "blank codex edge - NO text, looks fine"),
                                     12: ("warn", "thousand-years diptych scroll - borderline")},
    "06_The_Ends_Of_The_Earth": {2: ("bad", "full scroll of garbled Hebrew")},
}
BADGE = {"bad": ("#c0392b", "RE-RENDER"), "warn": ("#b8860b", "CHECK"), "ok": ("#2e7d32", "OK")}

def cards(folder):
    nbp = ROOT / folder / "visual" / "nbp"
    out = []
    for png in sorted(nbp.glob("[0-9][0-9]_*.png")):
        n = int(png.stem[:2])
        mp4 = png.with_suffix(".mp4")
        rel_png = f"{folder}/visual/nbp/{png.name}"
        rel_mp4 = f"{folder}/visual/nbp/{mp4.name}"
        flag = FLAGS.get(folder, {}).get(n)
        badge = ""
        ring = ""
        if flag:
            color, label = BADGE[flag[0]]
            badge = f'<div class="badge" style="background:{color}">{label}<br><span>{flag[1]}</span></div>'
            ring = f"box-shadow:0 0 0 4px {color};"
        media = (f'<video src="{rel_mp4}" poster="{rel_png}" muted loop controls playsinline></video>'
                 if mp4.exists() else f'<img src="{rel_png}">')
        out.append(f'<div class="card" style="{ring}">{badge}{media}'
                   f'<div class="cap">#{n:02d} {png.stem[3:].replace("-"," ")}</div></div>')
    return "\n".join(out)

sections = []
for folder, title in SHORTS:
    final = ROOT / folder / "assembly" / "viral_cut_sfx_captioned.mp4"
    final_rel = f"{folder}/assembly/viral_cut_sfx_captioned.mp4"
    fin = (f'<video class="final" src="{final_rel}" controls playsinline></video>'
           if final.exists() else "<i>no final yet</i>")
    sections.append(f'<h2>{folder.split("_")[0]} &mdash; {title}</h2>'
                    f'<div class="final-wrap"><b>Shipping final (SFX + captions):</b><br>{fin}</div>'
                    f'<div class="grid">{cards(folder)}</div>')

html = """<!doctype html><meta charset=utf-8><title>Psalm 22 scroll review</title>
<style>
body{background:#14110d;color:#e8e0cf;font-family:Segoe UI,system-ui,sans-serif;margin:0;padding:24px}
h1{color:#f0d98a}h2{color:#f0d98a;margin-top:48px;border-top:1px solid #3a342a;padding-top:18px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}
.card{background:#1e1a14;border-radius:10px;overflow:hidden;position:relative}
.card video,.card img{width:100%;display:block;background:#000}
.cap{padding:8px 10px;font-size:13px;color:#c8bfa8}
.badge{position:absolute;top:0;left:0;right:0;z-index:2;color:#fff;font-weight:700;
  font-size:12px;text-align:center;padding:4px}
.badge span{font-weight:400;font-size:10px;opacity:.9}
.final{width:340px;border-radius:10px;background:#000}.final-wrap{margin:10px 0 20px}
.legend{font-size:14px;color:#c8bfa8}.legend b{padding:2px 6px;border-radius:4px;color:#fff}
</style>
<h1>Psalm 22 shorts &mdash; scroll review (#02 / #03 / #04 / #06)</h1>
<p class=legend>
<b style="background:#c0392b">RE-RENDER</b> garbled text, fix needed &nbsp;
<b style="background:#b8860b">CHECK</b> borderline, your call &nbsp;
<b style="background:#2e7d32">OK</b> looks fine on a second look<br><br>
Each card = the still + the clip that currently ships. Press play on any clip. The big
player at the top of each section is the finished captioned short.</p>
""" + "\n".join(sections)

out = ROOT / "_SCROLL_REVIEW.html"
out.write_text(html, encoding="utf-8")
print(out)
