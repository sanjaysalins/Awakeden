"""Builds uplift/_REVIEW.html (simple, big, click-to-zoom). Run after check_uplift.py."""
import json, subprocess, html
from pathlib import Path
UP = Path(__file__).resolve().parent
EP = UP.parent
OLD = EP / "swirls_episode_07_the_bier_he_touched_final_piano_sfx.mp4"
NEW = UP / "ep07_uplift_final.mp4"
FR = UP / "review_frames"; FR.mkdir(exist_ok=True)
times = [(3.0, "the cover"), (9.0, "the law"), (15.0, "kept their distance (NEW page)"), (18.2, "toward her (NEW page)"), (22.0, "Weep not"),
         (27.5, "he touched the bier (NEW real clip)"), (31.5, "they stood still (clip)"), (37.0, "it did not work that way (NEW page)"), (43.0, "Arise (clip)"),
         (47.0, "he sat up"), (53.0, "Death did not spread"), (58.5, "the only direction (NEW page)"), (63.5, "what is his instead (NEW page)"), (69.0, "back cover (real clip)")]
for t, _ in times:
    for tag, p in (("old", OLD), ("new", NEW)):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(p), "-frames:v", "1", "-vf", "scale=720:-2", "-q:v", "3", str(FR / f"{tag}_{t:05.1f}.jpg")])
gate = json.loads((UP / "gate_report.json").read_text(encoding="utf-8")) if (UP / "gate_report.json").exists() else {}
spend = json.loads((UP / "spend_summary.json").read_text(encoding="utf-8")) if (UP / "spend_summary.json").exists() else {}
def uri(p): return "file:///" + str(p).replace("\\", "/")
rows = "".join(f'<div class="pair"><div class="cap">{html.escape(l)} <small>({t:.0f}s)</small></div><div class="ba"><figure><img class="z" src="review_frames/old_{t:05.1f}.jpg"><figcaption>OLD</figcaption></figure><figure><img class="z" src="review_frames/new_{t:05.1f}.jpg"><figcaption>NEW</figcaption></figure></div></div>' for t, l in times)
stills = "".join(f'<figure><img class="z" src="stills/{k}.png" loading="lazy"><figcaption>{k.upper()}</figcaption></figure>' for k in ("f01b", "f02a", "f03a", "f03b", "f06b", "f06c"))
grows = "".join(f'<tr class="{"ok" if v["pass"] else "bad"}"><td>{"PASS" if v["pass"] else "FAIL"}</td><td>{html.escape(k)}</td><td>{html.escape(v["evidence"])[:420]}</td></tr>' for k, v in gate.items() if not k.startswith("_"))
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Bier He Touched - uplift</title>
<style>:root{{--bg:#faf6ee;--ink:#2b2622;--ok:#2f7d4f;--bad:#b3392b}}@media (prefers-color-scheme:dark){{:root{{--bg:#1d1b19;--ink:#efe8dc}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:18px/1.4 system-ui,sans-serif;padding:16px}}h1{{font-size:28px}}h2{{margin-top:36px}}
.players{{display:flex;gap:16px;flex-wrap:wrap}}.players figure{{flex:1 1 360px;margin:0}}video{{width:100%;max-height:82vh;background:#000}}
.ba{{display:flex;gap:12px}}.ba figure{{flex:1;margin:0}}img{{width:100%;display:block;border:1px solid #8886}}.pair{{margin:16px 0}}.cap{{font-weight:600;margin-bottom:4px}}
.row{{display:flex;gap:12px;flex-wrap:wrap}}.row figure{{flex:1 1 220px;margin:0}}table{{border-collapse:collapse;width:100%;font-size:15px}}td{{padding:6px 8px;border-bottom:1px solid #8884;vertical-align:top}}
tr.ok td:first-child{{color:var(--ok);font-weight:700}}tr.bad td:first-child{{color:var(--bad);font-weight:700}}figcaption{{font-size:14px;opacity:.7}}
#zoom{{display:none;position:fixed;inset:0;background:#000d;z-index:9;align-items:center;justify-content:center}}#zoom img{{max-width:96vw;max-height:96vh;width:auto;border:0}}</style></head><body>
<h1>The Bier He Touched: old vs new</h1>
<p><b>New:</b> the touch, \"Arise\" and the back cover are now real moving clips (they were slow zooms on a still). 6 new pictures added so every line has its own page. No backwards play, no frozen fill. 5 pencil marks. Same voice and music, byte for byte. Elijah idea not built (words not decided).</p>
<div class="players"><figure><video controls preload="metadata" src="{uri(OLD)}"></video><figcaption>OLD (shipped, not touched)</figcaption></figure>
<figure><video controls preload="metadata" src="{uri(NEW)}"></video><figcaption>NEW (uplift)</figcaption></figure></div>
<h2>Before and after (click to zoom)</h2>{rows}
<h2>The 6 new pictures (click to zoom)</h2><div class="row">{stills}</div>
<h2>Not built (waits for the Elijah words decision)</h2><p>Nothing was skipped for pictures. The Elijah line (1 Kings 17:21-23 to Luke 7:15) is NOT in this film. If it is added, the cut moves and F05/F06 timings must be re-fitted. Extra widow close-up shot (+$0.27) also not bought.</p><h2>Checks</h2><table>{grows}</table>
<h2>Money</h2><p>{html.escape(spend.get("text", ""))}</p>
<div id="zoom"><img></div>
<script>const z=document.getElementById('zoom'),zi=z.querySelector('img');document.querySelectorAll('img.z').forEach(i=>i.onclick=()=>{{zi.src=i.src.replace('360','360');z.style.display='flex'}});z.onclick=()=>z.style.display='none';</script></body></html>"""
(UP / "_REVIEW.html").write_text(page, encoding="utf-8")
print("ok")
