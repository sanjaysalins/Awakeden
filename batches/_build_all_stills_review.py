# -*- coding: utf-8 -*-
"""ALL_STILLS_REVIEW.html — every still USED by every published cluster piece, in beat order,
with per-still FEEDBACK CAPTURE: PASS / FIX buttons + a note box per card (saved in the browser's
localStorage as you type), a sticky toolbar counting flags, and one COPY FEEDBACK button that
copies a paste-ready markdown list (piece/slug + note) for the chat. $0, no LLM."""
import json, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLUSTERS = [ROOT / "cluster_01_cross", ROOT / "cluster_02_resurrection"]
OUT = ROOT / "ALL_STILLS_REVIEW.html"

sections, total_stills = [], 0
for cl in CLUSTERS:
    for piece in sorted(p for p in cl.iterdir() if p.is_dir() and not p.name.startswith("_")):
        v = piece / "visual"
        spec_p = v / "livingpage_short.spec.json"
        cards, order = [], []
        used = {}  # slug -> {beats:[], motions:set, cap:str}
        if spec_p.is_file():
            spec = json.loads(spec_p.read_text(encoding="utf-8"))
            for i, b in enumerate(spec.get("beats", []), 1):
                cap = (b.get("cap", {}) or {}).get("text", "") or ""
                for c in b.get("clips", []) or []:
                    slug = c.get("slug")
                    if not slug:
                        continue
                    if slug not in used:
                        used[slug] = {"beats": [], "motions": set(), "cap": cap}
                        order.append(slug)
                    used[slug]["beats"].append(i)
                    if c.get("motion"):
                        used[slug]["motions"].add(c["motion"])
        else:
            for png in sorted(v.glob("*.png")):
                used[png.stem] = {"beats": [], "motions": set(), "cap": "(no spec — listing all stills)"}
                order.append(png.stem)
        for slug in order:
            png = v / f"{slug}.png"
            if not png.is_file():
                continue
            info = used[slug]
            rel = png.relative_to(ROOT).as_posix()
            kling = (v / "clips" / f"{slug}.mp4").is_file()
            fill = '<span class="k">KLING clip</span>' if kling else '<span class="d">dyncam ($0)</span>'
            beats = ", ".join(map(str, info["beats"])) or "—"
            key = f"{piece.name}/{slug}"
            total_stills += 1
            cards.append(
                f'<div class="card" data-key="{key}"><a href="{rel}" target="_blank">'
                f'<img src="{rel}" loading="lazy"></a>'
                f'<div class="meta"><b>{slug}</b> · beats {beats} · {fill}'
                f'<div class="cap">{info["cap"][:110]}</div></div>'
                f'<div class="fb"><button class="ok" onclick="mark(this,\'pass\')">PASS</button>'
                f'<button class="bad" onclick="mark(this,\'fix\')">FIX</button>'
                f'<textarea placeholder="what to fix…" oninput="note(this)"></textarea></div></div>')
        if cards:
            sections.append(
                f'<h2>{cl.name.split("_", 2)[-1]} / {piece.name} <span class="n">({len(cards)} stills)</span></h2>'
                f'<div class="grid">{"".join(cards)}</div>')

html = f"""<!doctype html><meta charset="utf-8"><title>All stills used — cluster review</title>
<style>body{{font-family:system-ui,sans-serif;background:#111;color:#eee;margin:20px;padding-top:54px}}
h1{{font-size:20px}} h2{{font-size:15px;margin:28px 0 8px;color:#f9d776}} .n{{color:#888;font-weight:400}}
p{{color:#ccc;font-size:13px;max-width:900px}}
.grid{{display:flex;flex-wrap:wrap;gap:10px}}
.card{{background:#1c1c1c;border:2px solid #333;border-radius:8px;padding:8px;width:180px}}
.card img{{width:100%;border-radius:4px;display:block}}
.card.pass{{border-color:#2a6}} .card.fix{{border-color:#c33;background:#241414}}
.meta{{font-size:11px;color:#bbb;margin-top:6px}} .cap{{color:#777;margin-top:3px;font-style:italic}}
.k{{color:#8cf}} .d{{color:#8f8}}
.fb{{margin-top:6px}} .fb button{{font-size:11px;padding:2px 10px;margin-right:6px;border-radius:10px;
border:1px solid #555;background:#222;color:#ddd;cursor:pointer}}
.card.pass .ok{{background:#2a6;color:#fff}} .card.fix .bad{{background:#c33;color:#fff}}
.fb textarea{{width:100%;margin-top:5px;background:#181818;color:#eee;border:1px solid #444;
border-radius:4px;font-size:11px;min-height:34px;box-sizing:border-box;display:none}}
.card.fix textarea{{display:block}}
#bar{{position:fixed;top:0;left:0;right:0;background:#000c;border-bottom:1px solid #333;
padding:9px 20px;font-size:13px;z-index:9;display:flex;gap:14px;align-items:center;backdrop-filter:blur(4px)}}
#bar button{{font-size:12px;padding:4px 14px;border-radius:12px;border:1px solid #666;
background:#222;color:#eee;cursor:pointer}} #bar .copy{{background:#f9d776;color:#000;font-weight:700}}
#count{{color:#f88;font-weight:700}}</style>
<div id="bar"><span>Stills review — <span id="count">0 flagged</span></span>
<button class="copy" onclick="copyFb()">COPY FEEDBACK for the chat</button>
<button onclick="clearFb()">clear all</button><span id="msg" style="color:#8f8"></span></div>
<h1>Every still used in the published pieces — {total_stills} stills (generated {time.strftime("%Y-%m-%d %H:%M")})</h1>
<p>Click an image = FULL-RES. Under each still: <b>PASS</b> (green) or <b>FIX</b> (red — a note box
appears; say what's wrong: doctrine, period, anatomy, style…). Everything saves in this browser as
you click/type. When you're done press <b>COPY FEEDBACK</b> and paste it into the chat — I'll re-drive
exactly those stills from the fact cards.</p>
{chr(10).join(sections)}
<script>
const KEY="jitb_stills_fb_v1";
let db=JSON.parse(localStorage.getItem(KEY)||"{{}}");
function save(){{localStorage.setItem(KEY,JSON.stringify(db));refresh();}}
function mark(btn,st){{const c=btn.closest(".card"),k=c.dataset.key;
 db[k]=db[k]||{{}};db[k].status=(db[k].status===st?"":st);save();}}
function note(ta){{const k=ta.closest(".card").dataset.key;db[k]=db[k]||{{}};db[k].note=ta.value;
 localStorage.setItem(KEY,JSON.stringify(db));countFb();}}
function refresh(){{document.querySelectorAll(".card").forEach(c=>{{
 const e=db[c.dataset.key]||{{}};c.classList.toggle("pass",e.status==="pass");
 c.classList.toggle("fix",e.status==="fix");
 const ta=c.querySelector("textarea");if(e.note!==undefined&&ta.value!==e.note)ta.value=e.note;}});countFb();}}
function countFb(){{const n=Object.values(db).filter(e=>e.status==="fix").length;
 document.getElementById("count").textContent=n+" flagged";}}
function copyFb(){{const lines=[];
 for(const[k,e]of Object.entries(db)){{if(e.status==="fix")lines.push("- "+k+": "+(e.note||"(no note)"));}}
 const txt=lines.length?"STILLS FEEDBACK\\n"+lines.join("\\n"):"STILLS FEEDBACK: all pass";
 navigator.clipboard.writeText(txt).then(()=>{{const m=document.getElementById("msg");
 m.textContent="copied "+lines.length+" item(s) — paste in the chat";setTimeout(()=>m.textContent="",4000);}});}}
function clearFb(){{if(confirm("Clear ALL feedback?")){{db={{}};save();}}}}
refresh();
</script>"""
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT}  ({total_stills} stills)")
