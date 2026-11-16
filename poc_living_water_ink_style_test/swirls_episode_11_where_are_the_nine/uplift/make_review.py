"""Builds uplift/_REVIEW.html (simple, big, click-to-zoom). Run after check_uplift.py."""
import json, subprocess, html
from pathlib import Path
UP = Path(__file__).resolve().parent; EP = UP.parent
OLD = EP / "swirls_episode_11_where_are_the_nine_final_piano_sfx.mp4"; NEW = UP / "ep11_uplift_final.mp4"
FR = UP / "review_frames"; FR.mkdir(exist_ok=True)
times = [(2.0, "the cover"), (6.0, "Only one came back"), (11.2, "NEW: at a distance"), (14.5, "have mercy on us"), (21.0, "Go shew yourselves (was frozen)"),
         (28.2, "NEW: they were cleansed"), (32.5, "One turned back (was zoom)"), (38.5, "fell down on his face (was zoom)"), (44.0, "Were there not ten? (was zoom)"),
         (49.0, "NEW: where are the nine?"), (58.0, "Arise, go thy way"), (64.0, "NEW: kept walking"), (70.0, "faith (face fixed)"), (76.0, "NEW: footprints"), (81.0, "the end")]
for t, _ in times:
    for tag, p in (("old", OLD), ("new", NEW)):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(p), "-frames:v", "1", "-vf", "scale=720:-2", "-q:v", "3", str(FR / f"{tag}_{t:05.1f}.jpg")])
gate = json.loads((UP / "gate_report.json").read_text(encoding="utf-8")) if (UP / "gate_report.json").exists() else {}
spend = json.loads((UP / "spend_summary.json").read_text(encoding="utf-8")) if (UP / "spend_summary.json").exists() else {}
def uri(p): return "file:///" + str(p).replace("\\", "/")
rows = "".join(f'<div class="pair"><div class="cap">{html.escape(l)} <small>({t:.0f}s)</small></div><div class="ba"><figure><img class="z" src="review_frames/old_{t:05.1f}.jpg"><figcaption>OLD</figcaption></figure><figure><img class="z" src="review_frames/new_{t:05.1f}.jpg"><figcaption>NEW</figcaption></figure></div></div>' for t, l in times)
stills = "".join(f'<figure><img class="z" src="stills/{k}_small.jpg" loading="lazy"><figcaption>{k.upper()}</figcaption></figure>' for k in ("f01b", "f04b", "f07b", "f09b", "f10b"))
face = '<div class="ba"><figure><img class="z" src="stills/old_f10_small.jpg"><figcaption>OLD F10 - wrong face</figcaption></figure><figure><img class="z" src="stills/f10_small.jpg"><figcaption>NEW F10 - same man as the other pages</figcaption></figure></div>'
grows = "".join(f'<tr class="{"ok" if v["pass"] else "bad"}"><td>{"PASS" if v["pass"] else "FAIL"}</td><td>{html.escape(k)}</td><td>{html.escape(v["evidence"])[:700]}</td></tr>' for k, v in gate.items() if not k.startswith("_"))
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Where Are the Nine - uplift</title>
<style>:root{{--bg:#faf6ee;--ink:#2b2622;--ok:#2f7d4f;--bad:#b3392b}}@media (prefers-color-scheme:dark){{:root{{--bg:#1d1b19;--ink:#efe8dc}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:18px/1.4 system-ui,sans-serif;padding:16px}}h1{{font-size:28px}}h2{{margin-top:36px}}
.players{{display:flex;gap:16px;flex-wrap:wrap}}.players figure{{flex:1 1 360px;margin:0}}video{{width:100%;max-height:82vh;background:#000}}
.ba{{display:flex;gap:12px}}.ba figure{{flex:1;margin:0}}img{{width:100%;display:block;border:1px solid #8886}}.pair{{margin:16px 0}}.cap{{font-weight:600;margin-bottom:4px}}
.row{{display:flex;gap:12px;flex-wrap:wrap}}.row figure{{flex:1 1 180px;margin:0}}table{{border-collapse:collapse;width:100%;font-size:15px}}td{{padding:6px 8px;border-bottom:1px solid #8884;vertical-align:top}}
tr.ok td:first-child{{color:var(--ok);font-weight:700}}tr.bad td:first-child{{color:var(--bad);font-weight:700}}figcaption{{font-size:14px;opacity:.7}}
#zoom{{display:none;position:fixed;inset:0;background:#000d;z-index:9;align-items:center;justify-content:center}}#zoom img{{max-width:96vw;max-height:96vh;width:auto;border:0}}</style></head><body>
<h1>Where Are the Nine: old vs new</h1>
<p><b>New:</b> the bad clips are replaced (frozen, zooming, glowing). Five new short shots. The healed man now has his real face. Pencil marks added. Same voice and music, byte for byte.</p>
<div class="players"><figure><video controls preload="metadata" src="{uri(OLD)}"></video><figcaption>OLD (shipped, not touched)</figcaption></figure>
<figure><video controls preload="metadata" src="{uri(NEW)}"></video><figcaption>NEW (uplift)</figcaption></figure></div>
<h2>The face fix (click to zoom)</h2>{face}
<h2>Before and after (click to zoom)</h2>{rows}
<h2>New pictures (click to zoom)</h2><div class="row">{stills}</div>
<h2>Checks</h2><table>{grows}</table>
<h2>Money</h2><p>{html.escape(spend.get("text", ""))}</p>
<div id="zoom"><img></div>
<script>const z=document.getElementById('zoom'),zi=z.querySelector('img');document.querySelectorAll('img.z').forEach(i=>i.onclick=()=>{{zi.src=i.src;z.style.display='flex'}});z.onclick=()=>z.style.display='none';</script></body></html>"""
(UP / "_REVIEW.html").write_text(page, encoding="utf-8"); print("ok")
