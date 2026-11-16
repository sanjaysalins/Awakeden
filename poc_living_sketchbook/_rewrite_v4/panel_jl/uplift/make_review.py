"""Builds uplift/_REVIEW.html (simple, big, click-to-zoom). Run after check_uplift.py."""
import json, subprocess, html
from pathlib import Path
UP = Path(__file__).resolve().parent
OLD = UP.parent / "video" / "jacobs_ladder_v3_sfx.mp4"
NEW = UP / "jl_uplift_final.mp4"
FR = UP / "review_frames"; FR.mkdir(exist_ok=True)
times = [(2.0, "the cover"), (5.5, "He ran. (pencil footprints)"), (9.5, "a man like that"), (16.0, "the ladder dream"), (24.0, "I will not leave thee"),
         (30.8, "Jacob woke afraid"), (34.8, "I knew it not (red circle)"), (40.5, "NEW: the Jesus page"), (47.5, "ascending and descending (arrows)"), (53.5, "NEW back cover")]
for t, _ in times:
    for tag, p in (("old", OLD), ("new", NEW)):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(p), "-frames:v", "1", "-vf", "scale=720:-2", "-q:v", "3", str(FR / f"{tag}_{t:05.1f}.jpg")])
gate = json.loads((UP / "gate_report.json").read_text(encoding="utf-8")) if (UP / "gate_report.json").exists() else {}
def uri(p): return "file:///" + str(p).replace("\\", "/")
rows = "".join(f'<div class="pair"><div class="cap">{html.escape(l)} <small>({t:.0f}s)</small></div><div class="ba"><figure><img class="z" src="review_frames/old_{t:05.1f}.jpg"><figcaption>OLD</figcaption></figure><figure><img class="z" src="review_frames/new_{t:05.1f}.jpg"><figcaption>NEW</figcaption></figure></div></div>' for t, l in times)
stills = "".join(f'<figure><img class="z" src="stills/{k}.png" loading="lazy"><figcaption>{l}</figcaption></figure>' for k, l in (("f07", "NEW F07 - the Jesus page"), ("back", "NEW back cover")))
grows = "".join(f'<tr class="{"ok" if v["pass"] else "bad"}"><td>{"PASS" if v["pass"] else "FAIL"}</td><td>{html.escape(k)}</td><td>{html.escape(v["evidence"])[:420]}</td></tr>' for k, v in gate.items() if not k.startswith("_"))
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jacob's Ladder - uplift</title>
<style>:root{{--bg:#faf6ee;--ink:#2b2622;--ok:#2f7d4f;--bad:#b3392b}}@media (prefers-color-scheme:dark){{:root{{--bg:#1d1b19;--ink:#efe8dc}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:18px/1.4 system-ui,sans-serif;padding:16px}}h1{{font-size:28px}}h2{{margin-top:36px}}
.players{{display:flex;gap:16px;flex-wrap:wrap}}.players figure{{flex:1 1 360px;margin:0}}video{{width:100%;max-height:82vh;background:#000}}
.ba{{display:flex;gap:12px}}.ba figure{{flex:1;margin:0}}img{{width:100%;display:block;border:1px solid #8886}}.pair{{margin:16px 0}}.cap{{font-weight:600;margin-bottom:4px}}
.row{{display:flex;gap:12px;flex-wrap:wrap}}.row figure{{flex:1 1 300px;margin:0}}table{{border-collapse:collapse;width:100%;font-size:15px}}td{{padding:6px 8px;border-bottom:1px solid #8884;vertical-align:top}}
tr.ok td:first-child{{color:var(--ok);font-weight:700}}tr.bad td:first-child{{color:var(--bad);font-weight:700}}figcaption{{font-size:14px;opacity:.7}}
.warn{{border-left:6px solid var(--bad);padding:6px 12px;margin:12px 0}}
#zoom{{display:none;position:fixed;inset:0;background:#000d;z-index:9;align-items:center;justify-content:center}}#zoom img{{max-width:96vw;max-height:96vh;width:auto;border:0}}</style></head><body>
<h1>Jacob's Ladder: old vs new</h1>
<p><b>New:</b> no freeze, no backwards play, no repeated pages. Jesus now has his own page. New back cover. A few pencil marks. Same voice and music, byte for byte.</p>
<div class="warn"><b>One known flaw:</b> in the ladder dream (about 12 to 20 s) one angel drifts to the left edge of the ladder near the end. Two takes had it. A third try was blocked, so nothing more was spent. Owner call: keep it, or buy one more try (about $0.63).</div>
<div class="players"><figure><video controls preload="metadata" src="{uri(OLD)}"></video><figcaption>OLD (shipped, not touched)</figcaption></figure>
<figure><video controls preload="metadata" src="{uri(NEW)}"></video><figcaption>NEW (uplift)</figcaption></figure></div>
<h2>Before and after (click to zoom)</h2>{rows}
<h2>The 2 new pictures (click to zoom)</h2><div class="row">{stills}</div>
<h2>Checks</h2><table>{grows}</table>
<h2>Money</h2><p>1,550 credits = $3.10 of the $3.80 cap. 2 stills x 40 = 80. Clips at 35 credits a second: F03 9 s, F04 10 s, F07 7 s, back cover 7 s = 1,155. One redo of F03 (9 s) = 315. Rejected: F03 take 1 and take 2 (angel leaves the ladder). A third F03 try was blocked by the permission system, not bought.</p>
<div id="zoom"><img></div>
<script>const z=document.getElementById('zoom'),zi=z.querySelector('img');document.querySelectorAll('img.z').forEach(i=>i.onclick=()=>{{zi.src=i.src;z.style.display='flex'}});z.onclick=()=>z.style.display='none';</script></body></html>"""
(UP / "_REVIEW.html").write_text(page, encoding="utf-8")
print("ok")
