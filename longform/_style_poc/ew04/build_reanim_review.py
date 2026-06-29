"""Focused review page for the 2 RE-ANIMATED EW04 clips (3b + cross).
Embeds the new mp4s + an OK/redo toggle each. POC/scratchpad."""
import shutil
from pathlib import Path

POC = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\_style_poc")
DEST = Path.home() / "Desktop" / "EW04_reanim"
(DEST / "clips").mkdir(parents=True, exist_ok=True)

ROWS = [
 ("03b", POC / "ew04" / "anim" / "EW04__03b_serpent_atop_sky.mp4",
  "3b — The bronze (hero close)",
  "Re-animated off the fixed still: slow reverent push-in tilting up to the lifted bronze serpent. Serpent stays solid cast metal (no slither/morph), corner clean, embers drift at the base."),
 ("cross", POC / "anim_jesus" / "JESUS__cross__a.mp4",
  "6 — Crucifixion (a)",
  "Re-animated off the fixed still: slow solemn push-in, storm sky churns. Christ stays still, nails through hands + feet held correct, no morph."),
]

cards = []
for key, src, label, change in ROWS:
    name = key + ".mp4"
    if src.exists():
        shutil.copy2(src, DEST / "clips" / name)
    cards.append(f"""<section data-key="{key}" data-label="{label}">
<h2>{label}</h2>
<div class=fixed>{change}</div>
<video src="clips/{name}" controls loop muted playsinline></video>
<div class=ctl>
  <label class=ok><input type=radio name="s_{key}" value="OK"> ✅ Good</label>
  <label class=fix><input type=radio name="s_{key}" value="FIX"> ⚠ Redo</label>
</div>
<textarea data-key="{key}" rows=2 placeholder="Any note..."></textarea>
</section>""")

html = """<!doctype html><meta charset=utf-8><title>EW04 re-animated — review</title>
<style>
body{background:#0e0e10;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:24px;max-width:760px}
h1{margin:0 0 6px} .sub{color:#9ab;margin:0 0 18px;line-height:1.5}
.bar{position:sticky;top:0;background:#0e0e10;padding:12px 0;border-bottom:1px solid #2a2a30;z-index:5}
button{background:#2563eb;color:#fff;border:0;border-radius:7px;padding:10px 16px;font-size:15px;cursor:pointer}
button.sec{background:#333} #status{color:#6f8;margin-left:12px;font-size:14px}
section{margin:0 0 26px;border-top:1px solid #2a2a30;padding-top:14px}
section.mark-FIX{border-left:4px solid #e0533a;padding-left:12px}
section.mark-OK{border-left:4px solid #2f9e44;padding-left:12px}
h2{margin:0 0 6px;color:#ffd98a;font-size:20px}
.fixed{color:#9fe6b0;font-size:14px;margin:0 0 10px}
video{width:100%;max-width:360px;border-radius:8px;border:1px solid #333;display:block;background:#000}
.ctl{margin:10px 0 6px;display:flex;gap:18px}
.ctl label{cursor:pointer;font-size:15px;padding:4px 10px;border:1px solid #444;border-radius:6px}
textarea{width:100%;max-width:360px;background:#16161c;color:#eee;border:1px solid #3a3a44;
         border-radius:7px;padding:8px;font-size:14px;font-family:inherit}
</style>
<h1>EW04 — re-animated clips</h1>
<p class=sub>The 2 clips you approved as stills, now animated. Mark each <b>Good</b> or <b>Redo</b>,
hit <b>Copy notes</b>, paste back. Once good, I assemble to ~70s with the narration, then score + SFX + captions.</p>
<div class=bar>
  <button onclick="copyNotes()">📋 Copy notes</button>
  <button class=sec onclick="clearAll()">Clear</button>
  <span id=status></span>
</div>
""" + "".join(cards) + """
<script>
const KEY='ew04_reanim_notes';
function load(){let d={};try{d=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
  document.querySelectorAll('section').forEach(s=>{const k=s.dataset.key,v=d[k]||{};
    const ta=s.querySelector('textarea');if(ta)ta.value=v.note||'';
    if(v.status){const r=s.querySelector('input[value="'+v.status+'"]');if(r)r.checked=true;s.classList.add('mark-'+v.status);}});}
function save(){const d={};document.querySelectorAll('section').forEach(s=>{const k=s.dataset.key;
    const st=s.querySelector('input:checked');const ta=s.querySelector('textarea');
    d[k]={status:st?st.value:'',note:ta?ta.value:'',label:s.dataset.label};
    s.classList.remove('mark-OK','mark-FIX');if(st)s.classList.add('mark-'+st.value);});
  localStorage.setItem(KEY,JSON.stringify(d));}
document.addEventListener('input',save);document.addEventListener('change',save);
function copyNotes(){let d={};try{d=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
  let out='EW04 re-animated review:\\n';
  document.querySelectorAll('section').forEach(s=>{const k=s.dataset.key,v=d[k]||{};
    out+='\\n['+(v.status||'?')+'] '+s.dataset.label+(v.note?' — '+v.note:'');});
  navigator.clipboard.writeText(out).then(()=>{document.getElementById('status').textContent='Copied! Paste into chat.';},
    ()=>{document.getElementById('status').textContent='Copy failed.';alert(out);});}
function clearAll(){if(confirm('Clear?')){localStorage.removeItem(KEY);location.reload();}}
load();
</script>
"""
out = DEST / "EW04_reanim.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
