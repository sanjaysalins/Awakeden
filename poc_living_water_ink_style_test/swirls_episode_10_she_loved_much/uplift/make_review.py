"""Builds uplift/_REVIEW.html (simple, big, click-to-zoom). Run after check_uplift.py."""
import json, subprocess, html
from pathlib import Path
UP = Path(__file__).resolve().parent
EP = UP.parent
OLD = EP / "swirls_episode_10_she_loved_much_final_piano_sfx.mp4"
NEW = UP / "ep10_uplift_final.mp4"
FR = UP / "review_frames"; FR.mkdir(exist_ok=True)
times = [(1.0, "cover"), (3.5, "F01: no kiss (ring)"), (11.5, "cover at the door (no title)"), (23.0, "F03A a tear lands"), (26.5, "F03B her hair"),
         (30.0, "F03C the ointment"), (42.0, "F04B answered anyway"), (47.5, "F05 tally marks"), (60.0, "F06B I suppose"), (71.5, "F08 red circle"),
         (81.0, "F08B the receipt"), (95.0, "F09B she walks out"), (104.0, "back cover (title no longer cropped)")]
for t, _ in times:
    for tag, p in (("old", OLD), ("new", NEW)):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(p), "-frames:v", "1", "-vf", "scale=720:-2", "-q:v", "3", str(FR / f"{tag}_{t:05.1f}.jpg")])
gate = json.loads((UP / "gate_report.json").read_text(encoding="utf-8")) if (UP / "gate_report.json").exists() else {}
def uri(p): return "file:///" + str(p).replace("\\", "/")
rows = "".join(f'<div class="pair"><div class="cap">{html.escape(l)} <small>({t:.0f}s)</small></div><div class="ba"><figure><img class="z" src="review_frames/old_{t:05.1f}.jpg"><figcaption>OLD</figcaption></figure><figure><img class="z" src="review_frames/new_{t:05.1f}.jpg"><figcaption>NEW</figcaption></figure></div></div>' for t, l in times)
stills = "".join(f'<figure><img class="z" src="stills/{k}.png" loading="lazy"><figcaption>{k.upper()}</figcaption></figure>' for k in ("f03a", "f03b", "f03c", "f04b", "f06b", "f08b", "f09b"))
grows = "".join(f'<tr class="{"ok" if v["pass"] else "bad"}"><td>{"PASS" if v["pass"] else "FAIL"}</td><td>{html.escape(k)}</td><td>{html.escape(v["evidence"])[:420]}</td></tr>' for k, v in gate.items() if not k.startswith("_"))
money = (UP / "spend_summary.txt").read_text(encoding="utf-8") if (UP / "spend_summary.txt").exists() else ""
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>She Loved Much - uplift review</title>
<style>:root{{--bg:#faf6ee;--ink:#2b2622;--ok:#2f7d4f;--bad:#b3392b}}@media (prefers-color-scheme:dark){{:root{{--bg:#1d1b19;--ink:#efe8dc}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:18px/1.4 system-ui,sans-serif;padding:16px}}h1{{font-size:28px}}h2{{margin-top:36px}}
.players{{display:flex;gap:16px;flex-wrap:wrap}}.players figure{{flex:1 1 360px;margin:0}}video{{width:100%;max-height:82vh;background:#000}}
.ba{{display:flex;gap:12px}}.ba figure{{flex:1;margin:0}}img{{width:100%;display:block;border:1px solid #8886}}.pair{{margin:16px 0}}.cap{{font-weight:600;margin-bottom:4px}}
.row{{display:flex;gap:12px;flex-wrap:wrap}}.row figure{{flex:1 1 200px;margin:0}}table{{border-collapse:collapse;width:100%;font-size:15px}}td{{padding:6px 8px;border-bottom:1px solid #8884;vertical-align:top}}
tr.ok td:first-child{{color:var(--ok);font-weight:700}}tr.bad td:first-child{{color:var(--bad);font-weight:700}}figcaption{{font-size:14px;opacity:.7}}
#zoom{{display:none;position:fixed;inset:0;background:#000d;z-index:9;align-items:center;justify-content:center}}#zoom img{{max-width:96vw;max-height:96vh;width:auto;border:0}}</style></head><body>
<h1>She Loved Much: old vs new</h1>
<p><b>New:</b> 7 new pages, so the kiss, the tears, the oil each get a real moving shot. The cover no longer cuts off the title. No zoom fill, no backwards play. Same voice and music, byte for byte.</p>
<div class="players"><figure><video controls preload="metadata" src="{uri(OLD)}"></video><figcaption>OLD (shipped, not touched)</figcaption></figure>
<figure><video controls preload="metadata" src="{uri(NEW)}"></video><figcaption>NEW (uplift)</figcaption></figure></div>
<h2>Before and after (click to zoom)</h2>{rows}
<h2>The 7 new pictures (click to zoom)</h2><div class="row">{stills}</div>
<h2>Checks</h2><table>{grows}</table>
<h2>Money</h2><pre style="white-space:pre-wrap">{html.escape(money)}</pre>
<div id="zoom"><img></div>
<script>const z=document.getElementById('zoom'),zi=z.querySelector('img');document.querySelectorAll('img.z').forEach(i=>i.onclick=()=>{{zi.src=i.src;z.style.display='flex'}});z.onclick=()=>z.style.display='none';</script></body></html>"""
(UP / "_REVIEW.html").write_text(page, encoding="utf-8")
print("ok")
