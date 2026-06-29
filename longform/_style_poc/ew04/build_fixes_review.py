"""Build EW04_fixes.html — focused review of the 4 rerolled stills (the user's
FIX notes). Shows each fixed still full-res + what was changed + an OK/redo toggle.
POC/scratchpad."""
import shutil
from pathlib import Path

POC = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\_style_poc")
STILLS = POC / "ew04" / "stills"
JES = POC / "jesus"
DEST = Path.home() / "Desktop" / "EW04_fixes"
(DEST / "img").mkdir(parents=True, exist_ok=True)

# (key, source, label, your original note, what I changed)
ROWS = [
 ("02b_serpents_spread", STILLS / "02b_serpents_spread.png", "2b — The plague (wide)",
  "the snakes are huge and are bigger than the tents",
  "Snakes redrawn normal-sized, low on the ground, far smaller than the people and tents."),
 ("03b_serpent_atop_sky", STILLS / "03b_serpent_atop_sky.png", "3b — The bronze (hero close)",
  "it does not match the snake pole ref grid we created before",
  "Rebuilt to match the BRONZE_SERPENT_STANDARD ref: slim single bronze serpent in a clean upright S on a SMALL stacked-ring ferrule, rough staff with branch-stubs, head up. No big collar, no flame, not wrapped."),
 ("04b_face_to_life", STILLS / "04b_face_to_life.png", "4b — Look and live (close)",
  "there is a snake tattoo on his neck, redo it",
  "Removed the snake entirely. Now just a real bite wound — two puncture dots in red, bruised swelling."),
 ("cross_a", JES / "JESUS__cross__a.png", "6 — Crucifixion (a) — REUSE",
  "the crucifixion is not accurate, chck the nails",
  "Fixed the nails: now driven THROUGH the hands and THROUGH the feet (small dark round nail-heads + blood) — no more cross/dagger-shaped spikes, no studs in the beam ends. Plain wood cross, crown of thorns, loincloth, dark Golgotha sky."),
]

cards = []
for key, src, label, note, change in ROWS:
    name = key + ".png"
    if src.exists():
        shutil.copy2(src, DEST / "img" / name)
    cards.append(f"""<section data-key="{key}" data-label="{label}">
<h2>{label}</h2>
<div class=note><b>You said:</b> {note}</div>
<div class=fixed><b>Fixed:</b> {change}</div>
<a href="img/{name}" target="_blank"><img src="img/{name}"></a>
<div class=ctl>
  <label class=ok><input type=radio name="s_{key}" value="OK"> ✅ Good now</label>
  <label class=fix><input type=radio name="s_{key}" value="FIX"> ⚠ Still needs work</label>
</div>
<textarea data-key="{key}" rows=2 placeholder="Any note..."></textarea>
</section>""")

html = """<!doctype html><meta charset=utf-8><title>EW04 fixes — review</title>
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
h2{margin:0 0 6px;color:#ffd98a;font-size:20px}
.note{color:#ffb4a0;font-size:14px;margin:0 0 4px}
.fixed{color:#9fe6b0;font-size:14px;margin:0 0 10px}
img{width:100%;max-width:460px;border-radius:8px;border:1px solid #333;display:block;background:#000}
.ctl{margin:10px 0 6px;display:flex;gap:18px}
.ctl label{cursor:pointer;font-size:15px;padding:4px 10px;border:1px solid #444;border-radius:6px}
textarea{width:100%;max-width:460px;background:#16161c;color:#eee;border:1px solid #3a3a44;
         border-radius:7px;padding:8px;font-size:14px;font-family:inherit}
</style>
<h1>EW04 — the 4 fixes</h1>
<p class=sub>I rerolled the 4 stills you flagged. Mark each <b>Good now</b> or <b>Still needs work</b>.
Click <b>Copy notes</b> and paste back. Once you approve, I re-animate only these and move to score + captions.</p>
<div class=bar>
  <button onclick="copyNotes()">📋 Copy notes</button>
  <button class=sec onclick="clearAll()">Clear</button>
  <span id=status></span>
</div>
""" + "".join(cards) + """
<script>
const KEY='ew04_fixes_notes';
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
  let out='EW04 fixes review:\\n';
  document.querySelectorAll('section').forEach(s=>{
    const k=s.dataset.key, v=d[k]||{};
    out+='\\n['+(v.status||'?')+'] '+s.dataset.label+(v.note?' — '+v.note:'');
  });
  navigator.clipboard.writeText(out).then(()=>{document.getElementById('status').textContent='Copied! Paste into chat.';},
    ()=>{document.getElementById('status').textContent='Copy failed — select manually.'; alert(out);});
}
function clearAll(){if(confirm('Clear?')){localStorage.removeItem(KEY);location.reload();}}
load();
</script>
"""
out = DEST / "EW04_fixes.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
