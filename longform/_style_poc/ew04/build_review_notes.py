"""Build EW04_review.html — an INTERACTIVE notes gallery for every EW04 still.
Each still shows full-res (click to open) + an OK/FIX toggle + a notes box.
Notes auto-save in the browser (localStorage); a 'Copy all my notes' button puts
a clean summary on the clipboard to paste back. POC/scratchpad."""
import shutil
from pathlib import Path

POC = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\_style_poc")
STILLS = POC / "ew04" / "stills"
JES = POC / "jesus"
DEST = Path.home() / "Desktop" / "EW04_review"
(DEST / "img").mkdir(parents=True, exist_ok=True)

# (key, source path, label, caption)
ROWS = [
 ("01_hook_moses", STILLS / "01_hook_moses.png", "1 — Hook / Moses (wide)",
  "Aged Moses by firelight, hand opening to speak."),
 ("01b_moses_close", STILLS / "01b_moses_close.png", "1b — Moses (close)",
  "Tight on his half-lit face, eyes on the viewer."),
 ("02_judgment_plague", STILLS / "02_judgment_plague.png", "2 — The plague (single)",
  "A man fallen, a serpent striking, crowd in shadow."),
 ("02b_serpents_spread", STILLS / "02b_serpents_spread.png", "2b — The plague (wide)",
  "Live serpents reared over the whole camp, figures fleeing."),
 ("03_bronze_lifted", STILLS / "03_bronze_lifted.png", "3 — The bronze lifted (wide)",
  "Moses lifts the pole — serpent set on top, over the camp."),
 ("03b_serpent_atop_sky", STILLS / "03b_serpent_atop_sky.png", "3b — The bronze (hero close)",
  "Low-angle hero of the lifted serpent against the sky."),
 ("04_look_and_live", STILLS / "04_look_and_live.png", "4 — Look and live (wide)",
  "A bitten man turns his eyes UP to the lifted serpent."),
 ("04b_face_to_life", STILLS / "04b_face_to_life.png", "4b — Look and live (close)",
  "Stricken elder (neck-bite) turns up — colour returns."),
 ("05_night_teacher", STILLS / "05_night_teacher.png", "5 — Night teacher (two-shot)",
  "Jesus to Nicodemus by lamplight."),
 ("05b_jesus_speaks", STILLS / "05b_jesus_speaks.png", "5b — Night teacher (close)",
  "Warm close on Jesus speaking; the line lands."),
 ("cross_a", JES / "JESUS__cross__a.png", "6 — Crucifixion (a) — REUSE",
  "Inked Jesus lifted up on the cross (storm sky)."),
 ("cross_b", JES / "JESUS__cross__b.png", "6 — Crucifixion (b) — REUSE",
  "2nd crucifixion angle."),
 ("risen_b", JES / "JESUS__risen__b.png", "7 — The risen Christ — REUSE",
  "Risen Christ, the contemplative landing."),
]

cards = []
for key, src, label, cap in ROWS:
    name = key + ".png"
    if src.exists():
        shutil.copy2(src, DEST / "img" / name)
    cards.append(f"""<section data-key="{key}" data-label="{label}">
<h2>{label}</h2><div class=note>{cap}</div>
<a href="img/{name}" target="_blank"><img src="img/{name}"></a>
<div class=ctl>
  <label class=ok><input type=radio name="s_{key}" value="OK"> ✅ OK</label>
  <label class=fix><input type=radio name="s_{key}" value="FIX"> ⚠ FIX</label>
</div>
<textarea data-key="{key}" rows=2 placeholder="Your note — what to fix..."></textarea>
</section>""")

html = """<!doctype html><meta charset=utf-8><title>EW04 stills — review &amp; notes</title>
<style>
body{background:#0e0e10;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:24px;max-width:900px}
h1{margin:0 0 6px} .sub{color:#9ab;margin:0 0 18px;line-height:1.5}
.bar{position:sticky;top:0;background:#0e0e10;padding:12px 0;border-bottom:1px solid #2a2a30;z-index:5}
button{background:#2563eb;color:#fff;border:0;border-radius:7px;padding:10px 16px;font-size:15px;cursor:pointer}
button.sec{background:#333}
#status{color:#6f8;margin-left:12px;font-size:14px}
section{margin:0 0 26px;border-top:1px solid #2a2a30;padding-top:14px}
section.mark-FIX{border-left:4px solid #e0533a;padding-left:12px}
section.mark-OK{border-left:4px solid #2f9e44;padding-left:12px}
h2{margin:0 0 4px;color:#ffd98a;font-size:20px}
.note{color:#9ab;font-size:14px;margin:0 0 10px}
img{width:100%;max-width:460px;border-radius:8px;border:1px solid #333;display:block;background:#000}
.ctl{margin:10px 0 6px;display:flex;gap:18px}
.ctl label{cursor:pointer;font-size:15px;padding:4px 10px;border:1px solid #444;border-radius:6px}
textarea{width:100%;max-width:460px;background:#16161c;color:#eee;border:1px solid #3a3a44;
         border-radius:7px;padding:8px;font-size:14px;font-family:inherit}
</style>
<h1>EW04 — Bronze Serpent · still review</h1>
<p class=sub>Mark each still <b>OK</b> or <b>FIX</b> and type a note. It saves automatically in this
browser. When done, click <b>Copy all my notes</b> and paste them back to me in chat.</p>
<div class=bar>
  <button onclick="copyNotes()">📋 Copy all my notes</button>
  <button class=sec onclick="clearAll()">Clear</button>
  <span id=status></span>
</div>
""" + "".join(cards) + """
<script>
const KEY='ew04_review_notes';
function load(){
  let d={}; try{d=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
  document.querySelectorAll('section').forEach(s=>{
    const k=s.dataset.key, v=d[k]||{};
    const ta=s.querySelector('textarea'); if(ta) ta.value=v.note||'';
    if(v.status){const r=s.querySelector('input[value="'+v.status+'"]'); if(r)r.checked=true; s.classList.add('mark-'+v.status);}
  });
}
function save(){
  const d={};
  document.querySelectorAll('section').forEach(s=>{
    const k=s.dataset.key;
    const st=s.querySelector('input:checked');
    const ta=s.querySelector('textarea');
    d[k]={status:st?st.value:'', note:ta?ta.value:'', label:s.dataset.label};
    s.classList.remove('mark-OK','mark-FIX'); if(st)s.classList.add('mark-'+st.value);
  });
  localStorage.setItem(KEY,JSON.stringify(d));
}
document.addEventListener('input',save);
document.addEventListener('change',save);
function copyNotes(){
  let d={}; try{d=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
  let out='EW04 still review notes:\\n';
  document.querySelectorAll('section').forEach(s=>{
    const k=s.dataset.key, v=d[k]||{};
    if(v.status||v.note) out+='\\n['+(v.status||'?')+'] '+s.dataset.label+(v.note?' — '+v.note:'');
  });
  navigator.clipboard.writeText(out).then(()=>{document.getElementById('status').textContent='Copied! Paste into chat.';},
    ()=>{document.getElementById('status').textContent='Copy failed — select the text manually.'; alert(out);});
}
function clearAll(){if(confirm('Clear all your notes?')){localStorage.removeItem(KEY);location.reload();}}
load();
</script>
"""
out = DEST / "EW04_review.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
