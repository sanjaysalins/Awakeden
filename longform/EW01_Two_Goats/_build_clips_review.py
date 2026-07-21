"""Build a one-page clip-review gallery for the EW01 ink migration — all 25
animated clips inline (<video>), with scene id / title / tier. $0, no render.
Follows the _CLIPQC_REVIEW.html pattern. Writes v1/visual_16x9_inked/_CLIPS_REVIEW.html.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIR = HERE / "v1" / "visual_16x9_inked"
CLIPS = DIR / "clips"
plan = json.loads((DIR / "scene_plan.json").read_text(encoding="utf-8"))

# tier map mirrors _animate_inked.py
KLING = {6, 11, 13, 14, 18, 20, 21, 24}

cards = []
for s in plan["scenes"]:
    sid = s["id"]
    t = s["title"].lower()
    t = "".join(c if (c.isalnum() or c == " ") else "" for c in t)
    stem = f"{sid:02d}_{'_'.join(t.split())[:46]}"
    mp4 = CLIPS / f"{stem}.mp4"
    tier = "Kling 3.0" if sid in KLING else "Seedance"
    src = f"clips/{stem}.mp4" if mp4.exists() else ""
    vid = (f'<video src="{src}" loop muted playsinline controls preload="metadata"></video>'
           if src else '<div class="missing">clip missing</div>')
    cards.append(f"""
    <div class="card">
      <div class="hdr"><span class="num">#{sid:02d}</span> <span class="tier tier-{tier.split()[0].lower()}">{tier}</span></div>
      {vid}
      <div class="title">{s['title']}</div>
    </div>""")

html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>EW01 Two Goats — inked clips review (25)</title>
<style>
body {{ background:#0e0e0e; color:#eee; font-family:system-ui,sans-serif; margin:0; padding:24px; }}
h1 {{ font-size:20px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(420px,1fr)); gap:18px; }}
.card {{ background:#1b1b1b; border-radius:10px; overflow:hidden; border:1px solid #333; }}
.card video {{ width:100%; display:block; background:#000; }}
.hdr {{ padding:6px 10px; display:flex; gap:10px; align-items:center; }}
.num {{ font-weight:bold; color:#9cf; }}
.tier {{ font-size:11px; padding:2px 8px; border-radius:10px; }}
.tier-kling {{ background:#5a3; color:#fff; }}
.tier-seedance {{ background:#357; color:#fff; }}
.title {{ padding:0 10px 10px; font-size:14px; }}
.missing {{ padding:40px; text-align:center; color:#c66; }}
.tip {{ color:#999; font-size:13px; }}
</style></head><body>
<h1>EW01 Two Goats — 25 inked clips (frozen tableau, camera + living light)</h1>
<p class="tip">All 25 clip-QC'd: camera push + ambient light only, no invented motion.
Green = Kling 3.0 (multi-figure/crowd), Blue = Seedance (calm single-figure).
Scenes 8 (blood removed) and 21 (walking held) were re-rolled. Click any clip to play.</p>
<div class="grid">
{"".join(cards)}
</div>
</body></html>"""

out = DIR / "_CLIPS_REVIEW.html"
out.write_text(html, encoding="utf-8")
print("wrote", out)
