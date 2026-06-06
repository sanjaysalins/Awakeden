"""Build a single self-contained index.html gallery of the 16:9 long-form stills.
EPISODE-GENERIC: pass an episode slug/dir as the first arg (bare = Isaiah).
Zoomed-out responsive grid (every scene with #NN + title); click any tile for a
full-screen lightbox (arrow keys / click to navigate). Relative image paths, so it
works offline by just opening the file. No dependencies."""
import sys, json, html
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _episode import resolve  # noqa: E402

ep = resolve(sys.argv)
OUT = ep.out
EP_TITLE = ep.title
scenes = ep.scenes

cards, slides = [], []
for i, s in enumerate(scenes):
    fn = ep.png(s).name
    if not (OUT / fn).exists():
        continue
    title = html.escape(s["title"]); mvt = html.escape(str(s.get("mvt", "")))
    is_redone = bool(s.get("redone"))
    badge = "REDONE" if is_redone else "kept"
    bcls = "redone" if is_redone else "kept"
    t0, t1 = s["t"]
    cards.append(f"""
    <figure class="card" onclick="openLb({i})">
      <div class="thumbwrap"><img loading="lazy" src="{fn}" alt="{title}"></div>
      <figcaption><span class="num">#{s['id']:02d}</span>
        <span class="badge {bcls}">{badge}</span>
        <span class="ttl">{title}</span>
        <span class="meta">{mvt} · {t0:.0f}–{t1:.0f}s</span></figcaption>
    </figure>""")
    slides.append({"src": fn, "n": s["id"], "title": s["title"], "mvt": str(s.get("mvt", "")),
                   "redone": is_redone})

doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(EP_TITLE)} — 16:9 stills</title>
<style>
  :root{{color-scheme:dark}}
  body{{margin:0;background:#14110d;color:#e9e0cf;font:15px/1.4 -apple-system,Segoe UI,Roboto,sans-serif}}
  header{{padding:16px 20px;border-bottom:1px solid #332b20;position:sticky;top:0;background:#14110dee;backdrop-filter:blur(6px);z-index:5}}
  h1{{margin:0;font-size:18px;font-weight:600}}
  .sub{{color:#9c8e74;font-size:13px;margin-top:3px}}
  .controls{{margin-top:8px}}
  .controls button{{background:#2a2318;color:#e9e0cf;border:1px solid #4a3f2c;border-radius:6px;padding:5px 11px;cursor:pointer;font-size:13px}}
  .controls button.on{{background:#6b5836;border-color:#8a724a}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;padding:18px}}
  .card{{margin:0;background:#1d1810;border:1px solid #332b20;border-radius:10px;overflow:hidden;cursor:zoom-in;transition:transform .08s,border-color .12s}}
  .card:hover{{transform:translateY(-2px);border-color:#7a6238}}
  .thumbwrap{{aspect-ratio:16/9;background:#000;overflow:hidden}}
  .thumbwrap img{{width:100%;height:100%;object-fit:cover;display:block}}
  figcaption{{padding:8px 10px;display:flex;flex-wrap:wrap;gap:6px;align-items:center}}
  .num{{font-weight:700;color:#e7c98a}}
  .ttl{{flex:1 1 100%;order:3;color:#cdbf9f;font-size:13px}}
  .meta{{flex:1 1 100%;order:4;color:#80745c;font-size:11px}}
  .badge{{font-size:10px;padding:2px 6px;border-radius:20px;letter-spacing:.04em}}
  .badge.redone{{background:#5a3e1f;color:#ffd89b}}
  .badge.kept{{background:#26331f;color:#a9d191}}
  body.only-redone .card.kepthide{{display:none}}
  /* lightbox */
  #lb{{position:fixed;inset:0;background:#000000ee;display:none;align-items:center;justify-content:center;z-index:20;flex-direction:column}}
  #lb.show{{display:flex}}
  #lb img{{max-width:96vw;max-height:84vh;object-fit:contain;box-shadow:0 0 40px #000}}
  #lbcap{{margin-top:10px;color:#e9e0cf;font-size:15px}}
  #lbcap .num{{color:#e7c98a;font-weight:700;margin-right:8px}}
  .nav{{position:fixed;top:0;height:100%;width:18%;display:flex;align-items:center;cursor:pointer;color:#fff7;font-size:40px;user-select:none}}
  .nav:hover{{color:#fff}}
  #prev{{left:0;justify-content:flex-start;padding-left:18px}}
  #next{{right:0;justify-content:flex-end;padding-right:18px}}
  #close{{position:fixed;top:12px;right:18px;color:#fff9;font-size:30px;cursor:pointer;z-index:21}}
  .hint{{color:#80745c;font-size:12px;margin-top:4px}}
</style></head><body>
<header>
  <h1>{html.escape(EP_TITLE)} · long-form 16:9 stills</h1>
  <div class="sub">{len(slides)} scenes · <b style="color:#ffd89b">{sum(s['redone'] for s in slides)} redone</b> · {sum(not s['redone'] for s in slides)} kept · click any tile to zoom</div>
  <div class="controls">
    <button id="bAll" class="on" onclick="filt(false)">Show all</button>
    <button id="bRedone" onclick="filt(true)">Only redone</button>
  </div>
</header>
<main class="grid" id="grid">{''.join(cards)}</main>

<div id="lb" onclick="if(event.target.id==='lb')closeLb()">
  <span id="close" onclick="closeLb()">✕</span>
  <span id="prev" class="nav" onclick="step(-1)">‹</span>
  <span id="next" class="nav" onclick="step(1)">›</span>
  <img id="lbimg" src="">
  <div id="lbcap"></div>
  <div class="hint">← → to move · Esc to close</div>
</div>

<script>
const S = {json.dumps(slides)};
let cur = 0;
const lb=document.getElementById('lb'), lbimg=document.getElementById('lbimg'), lbcap=document.getElementById('lbcap');
function openLb(i){{cur=i;render();lb.classList.add('show');}}
function closeLb(){{lb.classList.remove('show');}}
function step(d){{cur=(cur+d+S.length)%S.length;render();}}
function render(){{const s=S[cur];lbimg.src=s.src;
  lbcap.innerHTML='<span class="num">#'+String(s.n).padStart(2,'0')+'</span>'+s.title+' — <span style="color:#9c8e74">'+s.mvt+(s.redone?' · redone':'')+'</span>';}}
function filt(only){{document.body.classList.toggle('only-redone',only);
  document.getElementById('bRedone').classList.toggle('on',only);
  document.getElementById('bAll').classList.toggle('on',!only);}}
// tag kept cards for filtering
document.querySelectorAll('.card').forEach((c,i)=>{{if(!S[i].redone)c.classList.add('kepthide');}});
document.addEventListener('keydown',e=>{{if(!lb.classList.contains('show'))return;
  if(e.key==='Escape')closeLb();else if(e.key==='ArrowRight')step(1);else if(e.key==='ArrowLeft')step(-1);}});
</script></body></html>"""

idx = OUT / "index.html"
idx.write_text(doc, encoding="utf-8")
print(f"[done] {idx}  ({len(slides)} scenes, {sum(s['redone'] for s in slides)} redone)")
