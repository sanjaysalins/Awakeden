#!/usr/bin/env python
"""Build a static self-contained STILLS REVIEW page: every still in the full Psalm-22 spec as a card
with a REDO checkbox + a notes textarea, and a 'Copy my notes' button that gathers only the flagged
ones into paste-back text. Opens via file:// (images are siblings). $0.

  ...python longform/02_Psalm_22_Song_From_The_Cross/build_review_html.py
"""
import html, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
POOL = HERE / "v1" / "visual_16x9_inked"
SPEC = POOL / "mocomic_16x9_full.spec.json"

beats = json.loads(SPEC.read_text(encoding="utf-8"))["beats"]
# distinct slugs in first-appearance order + their context (beat #, caption, new?)
seen = {}
for i, b in enumerate(beats, 1):
    cap = b.get("cap", {})
    ctx = cap.get("text", "") if cap.get("type") == "caption" else (cap.get("text", "") if cap.get("type") == "redletter" else "")
    for c in b["clips"]:
        s = c["slug"]
        if s not in seen:
            seen[s] = {"beat": i, "ctx": ctx, "new": c.get("src") == "new"}
slugs = list(seen.items())

cards = []
for idx, (slug, meta) in enumerate(slugs, 1):
    exists = (POOL / f"{slug}.png").exists()
    badge = '<span class="badge new">NEW</span>' if meta["new"] else '<span class="badge">reuse</span>'
    miss = '' if exists else '<span class="badge miss">MISSING</span>'
    ctx = html.escape(meta["ctx"][:90])
    cards.append(f'''
    <div class="card" data-slug="{slug}">
      <div class="imgwrap"><img loading="lazy" src="{slug}.png" alt="{slug}"></div>
      <div class="meta"><b>{idx}. {slug}</b> {badge}{miss}<div class="ctx">beat {meta["beat"]} · {ctx}</div></div>
      <label class="redo"><input type="checkbox" class="chk"> <span>REDO this still</span></label>
      <textarea class="note" placeholder="Notes: what's wrong / what to change..."></textarea>
    </div>''')

page = f'''<!doctype html><html><head><meta charset="utf-8"><title>Psalm 22 — Stills Review</title>
<style>
 body{{font-family:system-ui,Arial,sans-serif;margin:0;background:#f4f2ec;color:#1a1712}}
 header{{position:sticky;top:0;background:#1a1712;color:#f4f2ec;padding:14px 20px;z-index:10;box-shadow:0 2px 8px #0006}}
 header h1{{margin:0 0 4px;font-size:20px}} header p{{margin:0;font-size:14px;opacity:.85}}
 .bar{{display:flex;gap:12px;align-items:center;margin-top:10px}}
 button{{font-size:16px;padding:10px 18px;border:0;border-radius:8px;background:#c8321a;color:#fff;cursor:pointer;font-weight:700}}
 button:hover{{background:#a8280f}} .count{{font-size:15px;font-weight:700}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(440px,1fr));gap:18px;padding:20px}}
 .card{{background:#fff;border:2px solid #ddd;border-radius:12px;overflow:hidden;transition:border-color .15s}}
 .card.flagged{{border-color:#c8321a;box-shadow:0 0 0 3px #c8321a33}}
 .imgwrap{{background:#000;aspect-ratio:16/9}} .imgwrap img{{width:100%;height:100%;object-fit:contain;display:block}}
 .meta{{padding:8px 12px;font-size:15px}} .ctx{{font-size:12px;color:#666;margin-top:3px}}
 .badge{{font-size:11px;padding:2px 7px;border-radius:10px;background:#e5e0d5;margin-left:6px}}
 .badge.new{{background:#1f7a34;color:#fff}} .badge.miss{{background:#c8321a;color:#fff}}
 label.redo{{display:flex;align-items:center;gap:8px;padding:6px 12px;font-size:16px;font-weight:700;cursor:pointer}}
 label.redo input{{width:22px;height:22px}}
 textarea.note{{width:calc(100% - 24px);margin:0 12px 12px;min-height:52px;font-size:15px;padding:8px;border:1px solid #ccc;border-radius:6px;font-family:inherit}}
 #out{{width:100%;min-height:120px;font-size:14px;margin-top:10px;display:none;padding:10px;border-radius:8px;font-family:ui-monospace,monospace}}
</style></head><body>
<header>
  <h1>Psalm 22 — Stills Review ({len(slugs)} stills)</h1>
  <p>Tick <b>REDO</b> and type a note on any still you want changed. Then click <b>Copy my notes</b> and paste them back to me.</p>
  <div class="bar"><button onclick="collect()">📋 Copy my notes</button><span class="count" id="cnt">0 flagged</span></div>
  <textarea id="out" readonly></textarea>
</header>
<div class="grid">{''.join(cards)}</div>
<script>
 function refresh(){{
   let n=0;
   document.querySelectorAll('.card').forEach(c=>{{
     const on=c.querySelector('.chk').checked || c.querySelector('.note').value.trim();
     c.classList.toggle('flagged', !!on); if(on) n++;
   }});
   document.getElementById('cnt').textContent = n+' flagged';
 }}
 document.addEventListener('input', refresh);
 function collect(){{
   const lines=[];
   document.querySelectorAll('.card').forEach(c=>{{
     const note=c.querySelector('.note').value.trim();
     if(c.querySelector('.chk').checked || note)
       lines.push('- '+c.dataset.slug+': '+(note||'redo'));
   }});
   const txt = lines.length ? 'REDO NOTES:\\n'+lines.join('\\n') : 'No stills flagged.';
   const out=document.getElementById('out'); out.style.display='block'; out.value=txt;
   navigator.clipboard && navigator.clipboard.writeText(txt);
   out.select();
 }}
</script></body></html>'''

dest = POOL / "_STILLS_REVIEW.html"
dest.write_text(page, encoding="utf-8")
print(f"wrote {dest}\n  file:///{str(dest).replace(chr(92),'/')}")
