"""Focused gallery of every still currently in the 3 v2 pilots, for delete/redo flagging."""
import json, html, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
from pipeline import coherence  # noqa

PILOTS = [
    ("Isaiah 53:5 — With His Stripes", "v2/pilot/isaiah_53_5_with_his_stripes/v1/visual/nbp"),
    ("Mockers' Words (v2)", "v2/pilot/mockers_words_ps22/v1/visual/nbp"),
    ("Zechariah 12:10 — The One They Pierced", "v2/pilot/zechariah_12_10_pierced/v1/visual/nbp"),
]

def fwd(p): return str(p).replace("\\", "/")

def badge(png):
    sc = png.with_suffix(png.suffix + ".coherence.json")
    if not sc.exists(): return ("PENDING", "#888")
    try: d = json.loads(sc.read_text(encoding="utf-8"))
    except Exception: return ("BAD-SC", "#a44")
    if not d.get("audited"): return ("UNAUD", "#888")
    return ("PASS", "#1c3") if d.get("passed") else ("FAIL", "#f44")

secs, total = [], 0
for title, rel in PILOTS:
    pngs = sorted((ROOT / rel).glob("*.png"))
    total += len(pngs)
    cards = []
    for p in pngs:
        v, col = badge(p)
        src = "file:///" + fwd(p)
        cards.append(
            f'<div class="c" data-p="{html.escape(fwd(p))}" onclick="f(this)">'
            f'<img loading="lazy" src="{html.escape(src)}">'
            f'<div class="m"><span class="b" style="background:{col}">{v}</span> '
            f'<span class="t">{p.name}</span></div><div class="flag">DELETE / REDO</div></div>')
    secs.append(f'<h2>{html.escape(title)} <small>({len(pngs)} stills)</small></h2>'
                f'<div class="row">{"".join(cards)}</div>')

doc = (
 '<!doctype html><meta charset=utf-8><title>Pilot stills — flag delete/redo</title>'
 '<style>body{background:#14161a;color:#eee;font-family:system-ui;margin:0}'
 '.bar{position:sticky;top:0;background:#0d0f12;border-bottom:1px solid #333;padding:12px 18px;z-index:9}'
 '.count{color:#ff5252;font-weight:700;font-size:20px}button{font-size:15px;padding:8px 14px;border:0;border-radius:8px;background:#2a6;color:#fff;cursor:pointer}'
 'h2{padding:6px 18px;margin:18px 0 4px;border-left:5px solid #555}small{color:#888}'
 '.row{display:flex;flex-wrap:wrap;gap:12px;padding:0 18px}'
 '.c{width:250px;background:#1d2026;border:3px solid #2a2e36;border-radius:9px;overflow:hidden;cursor:pointer;position:relative}'
 '.c.fl{border-color:#ff3b3b;box-shadow:0 0 0 2px #ff3b3b inset}.c img{width:100%;display:block;background:#000}'
 '.m{padding:7px 9px}.b{padding:1px 7px;border-radius:4px;color:#031;font-weight:700}.t{font-family:monospace;font-size:10px;color:#7fa}'
 '.flag{position:absolute;top:6px;right:6px;background:#ff3b3b;color:#fff;font-weight:700;padding:3px 7px;border-radius:6px;font-size:11px;display:none}.c.fl .flag{display:block}</style>'
 '<div class="bar"><b>Pilot stills — click any to flag DELETE / REDO</b> '
 '<span class="count"><span id="n">0</span> flagged</span> '
 '<button onclick="cp()">Copy flagged paths</button> <span style="color:#9a9">' + str(total) + ' stills</span></div>'
 + "".join(secs) +
 '<script>const F=new Set();function f(c){const p=c.dataset.p;if(c.classList.toggle("fl"))F.add(p);else F.delete(p);'
 'document.getElementById("n").textContent=F.size;}'
 'function cp(){navigator.clipboard.writeText([...F].sort().join("\\n"));alert(F.size+" paths copied — paste back to Claude");}</script>'
)
out = ROOT / "v2/coherence_audit/pilots_review.html"
out.write_text(doc, encoding="utf-8")
print(f"wrote {total} stills -> {out}")
