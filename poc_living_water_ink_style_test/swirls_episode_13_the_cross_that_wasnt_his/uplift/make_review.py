"""Builds uplift/_REVIEW.html (simple, click-to-zoom). Run after check_uplift.py."""
import json, subprocess, html
from pathlib import Path
UP = Path(__file__).resolve().parent; EP = UP.parent
OLD = EP / "swirls_episode_13_the_cross_that_wasnt_his_final_piano_sfx.mp4"; NEW = UP / "ep13_uplift_final.mp4"
FR = UP / "review_frames"; FR.mkdir(exist_ok=True)
times = [(2.0, "the cover (was frozen)"), (9.0, "Mark: led him out"), (14.0, "passed by (new close page)"), (24.5, "nobody asked him (new)"), (35.5, "through the gate (new)"),
         (40.9, "outside is 'without'"), (46.5, "blood carried in"), (52.0, "burned without the camp (new)"), (65.5, "out there (new)"), (70.0, "Let us go forth"),
         (75.5, "reproach is shame (new)"), (83.0, "Simon was forced out"), (93.0, "only the shame (new)"), (100.0, "the closing cover")]
for t, _ in times:
    for tag, p in (("old", OLD), ("new", NEW)):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(p), "-frames:v", "1", "-vf", "scale=540:-2", "-q:v", "3", str(FR / f"{tag}_{t:05.1f}.jpg")])
gate = json.loads((UP / "gate_report.json").read_text(encoding="utf-8"))
def uri(p): return "file:///" + str(p).replace("\\", "/")
rows = "".join(f'<div class="pair"><div class="cap">{html.escape(l)} <small>({t:.0f}s)</small></div><div class="ba"><figure><img class="z" src="review_frames/old_{t:05.1f}.jpg"><figcaption>OLD</figcaption></figure><figure><img class="z" src="review_frames/new_{t:05.1f}.jpg"><figcaption>NEW</figcaption></figure></div></div>' for t, l in times)
stills = "".join(f'<figure><img class="z" src="stills/{k}.png" loading="lazy"><figcaption>{k.upper()}</figcaption></figure>' for k in ("f01b", "f02b", "f03b", "f05b", "f06b", "f07b", "f09b"))
rej = "".join(f'<figure><img class="z" src="stills/{p.name}" loading="lazy"><figcaption>{html.escape(p.stem[9:])}</figcaption></figure>' for p in sorted((UP / "stills").glob("REJECTED_*.png")))
grows = "".join(f'<tr class="{"ok" if v["pass"] else "bad"}"><td>{"PASS" if v["pass"] else "FAIL"}</td><td>{html.escape(k)}</td><td>{html.escape(v["evidence"])[:520]}</td></tr>' for k, v in gate.items() if not k.startswith("_"))
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cross That Wasn't His - uplift</title>
<style>:root{{--bg:#faf6ee;--ink:#2b2622;--ok:#2f7d4f;--bad:#b3392b}}@media (prefers-color-scheme:dark){{:root{{--bg:#1d1b19;--ink:#efe8dc}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:18px/1.4 system-ui,sans-serif;padding:16px}}h1{{font-size:28px}}h2{{margin-top:36px}}
.players{{display:flex;gap:16px;flex-wrap:wrap}}.players figure{{flex:1 1 360px;margin:0}}video{{width:100%;max-height:82vh;background:#000}}
.ba{{display:flex;gap:12px}}.ba figure{{flex:1;margin:0}}img{{width:100%;display:block;border:1px solid #8886}}.pair{{margin:16px 0}}.cap{{font-weight:600;margin-bottom:4px}}
.row{{display:flex;gap:12px;flex-wrap:wrap}}.row figure{{flex:1 1 200px;margin:0}}table{{border-collapse:collapse;width:100%;font-size:15px}}td{{padding:6px 8px;border-bottom:1px solid #8884;vertical-align:top}}
tr.ok td:first-child{{color:var(--ok);font-weight:700}}tr.bad td:first-child{{color:var(--bad);font-weight:700}}figcaption{{font-size:14px;opacity:.7}}
#zoom{{display:none;position:fixed;inset:0;background:#000d;z-index:9;align-items:center;justify-content:center}}#zoom img{{max-width:96vw;max-height:96vh;width:auto;border:0}}</style></head><body>
<h1>The Cross That Wasn't His: old vs new</h1>
<p><b>New:</b> the frozen cover now moves. 7 new pages break up the long holds. No backwards play, no frozen fill. Pencil marks added. Same voice and music, byte for byte.</p>
<div class="players"><figure><video controls preload="metadata" src="{uri(OLD)}"></video><figcaption>OLD (shipped, not touched)</figcaption></figure>
<figure><video controls preload="metadata" src="{uri(NEW)}"></video><figcaption>NEW (uplift)</figcaption></figure></div>
<h2>Before and after (click to zoom)</h2>{rows}
<h2>The 7 new pages</h2><div class="row">{stills}</div>
<h2>Rejected takes</h2><div class="row">{rej}</div>
<h2>Checks</h2><table>{grows}</table>
<h2>My eye notes on the G-MOTION FAIL</h2><ul><li>Cover: the title band number is clouds and wall moving behind the title. The title itself is unchanged (looked at first and last frame). Not a real fail.</li><li>F02B: 24 to 108 blue pixels is dust shading, no ink on this page. Not a real fail. Small panel 2 (sandals) is dusted over by the end of the clip: weak, owner call.</li><li><b>Real:</b> F03B the blue thread on the stone shrinks and shifts as the foot lands (take 1 was worse). F06B the small bloom in the gate opening brightens a little (+29%). Both are mild; a 3rd take would cost 140 cr / 105 cr.</li><li>F06B gate is drawn as an arch; the shipped gate is square. F06B and F09B captions came out in quote marks. F07B: one of the three onlookers wears a head-cloth. F05B top panels wrap (panel 3 on a second row).</li></ul><h2>Money</h2><p>2,045 credits = $4.09 (cap 2,350 = $4.70). 10 stills x 40 cr = 400. Clips at 35 cr/s: cover 5 s, F01B 3, F02B 4, F03B 4 (+4 redo), F05B 5, F06B 3, F07B 5, F09B 7 (+7 redo) = 47 s = 1,645.</p>
<div id="zoom"><img></div>
<script>const z=document.getElementById('zoom'),zi=z.querySelector('img');document.querySelectorAll('img.z').forEach(i=>i.onclick=()=>{{zi.src=i.src;z.style.display='flex'}});z.onclick=()=>z.style.display='none';</script></body></html>"""
(UP / "_REVIEW.html").write_text(page, encoding="utf-8"); print("ok")
