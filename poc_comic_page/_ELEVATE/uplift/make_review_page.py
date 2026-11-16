r"""make_review_page.py: the owner page for the pilot. Simple, big, short words. $0. Never opens anything.
Writes <piece>\visual\uplift_v1\_PILOT_REVIEW.html + before/after stills into uplift_v1\_review_stills\.
"""
import json, subprocess
from pathlib import Path

P = Path(r"F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_01_cross\woman_behold_john1926\visual")
U = P / "uplift_v1"
OLD = P / "woman_behold_john1926_sfx_v5hook.mp4"
NEW = P / "woman_behold_john1926_uplift_v1.mp4"
ST = U / "_review_stills"
ST.mkdir(exist_ok=True)
gates = json.loads((U / "gates_result.json").read_text(encoding="utf-8"))

PAIRS = [  # (time s, short title, plain words)
    (10.6, "Thirty years later", "Before: one picture cut 3 ways. After: the shadow on the wall, then the real cross. The gold thread joins them."),
    (20.6, "He sees her wound", "Before: John and Mary cut 3 ways. After: His face, then her face. A dotted sight line joins them."),
    (30.3, "Woman, behold thy son", "Before: two strangers kneeling. After: Mary and John, and Jesus as He speaks. No marks here."),
    (34.6, "Behold thy mother", "Before: a nail in a hand. After: John's face, then Mary's."),
    (42.7, "A son. A home.", "Before: Simeon and the baby. After: Mary and John, tied by a gold thread."),
    (45.2, "While judgment fell on him", "Before: his face cut 3 ways. After: one full picture of His face."),
]
for i, (t, _, _) in enumerate(PAIRS, 1):
    for tag, f in (("old", OLD), ("new", NEW)):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", str(f), "-frames:v", "1", "-vf", "scale=540:960",
                        str(ST / f"p{i}_{tag}.jpg")], check=True)
marks = [m for m in gates.get("_marks", [])]
rows = ""
for g in ("U1", "U2", "U3", "U4", "U5", "U6a", "U6b/U7", "U8", "U9"):
    r = gates.get(g)
    if not r:
        continue
    st = "PASS" if r["pass"] else ("NOT RUN" if r["pass"] is None else "FAIL")
    cls = {"PASS": "ok", "FAIL": "bad", "NOT RUN": "na"}[st]
    rows += f"<tr><td>{g}</td><td class='{cls}'>{st}</td><td>{r['evidence'][:420]}</td></tr>"
pairs_html = "".join(
    f"<h3>{i}. {t_}</h3><p>{w}</p><div class='pair'><figure><img src='_review_stills/p{i}_old.jpg' onclick='z(this)'><figcaption>BEFORE</figcaption></figure>"
    f"<figure><img src='_review_stills/p{i}_new.jpg' onclick='z(this)'><figcaption>AFTER</figcaption></figure></div>"
    for i, (t, t_, w) in enumerate(PAIRS, 1))
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pilot review - Woman, Behold Thy Son</title>
<style>
:root{{--bg:#fbf6e9;--ink:#14100c;--card:#fff;--ok:#1a7f37;--bad:#b3261e;--na:#8a6d00}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#17130f;--ink:#f4ecd8;--card:#241e18}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:20px/1.5 Georgia,serif;padding:16px}}
h1{{font-size:34px}} h2{{font-size:28px;margin-top:40px}} h3{{font-size:24px;margin-bottom:0}}
.vids{{display:flex;gap:16px;flex-wrap:wrap}} .vids figure{{margin:0;flex:1 1 320px}}
video{{width:100%;max-height:82vh;background:#000;border-radius:10px}}
figcaption{{font-weight:bold;font-size:22px;margin:6px 0}}
.pair{{display:flex;gap:12px}} .pair figure{{flex:1;margin:0}} .pair img{{width:100%;border-radius:8px;cursor:zoom-in}}
button{{font:inherit;font-size:22px;padding:12px 24px;border-radius:10px;border:2px solid var(--ink);background:var(--card);color:var(--ink)}}
table{{border-collapse:collapse;width:100%;font-size:16px}} td{{border-bottom:1px solid #8884;padding:6px;vertical-align:top}}
.ok{{color:var(--ok);font-weight:bold}} .bad{{color:var(--bad);font-weight:bold}} .na{{color:var(--na);font-weight:bold}}
#zoom{{display:none;position:fixed;inset:0;background:#000d;z-index:9;align-items:center;justify-content:center}} #zoom img{{max-width:96vw;max-height:96vh}}
</style></head><body>
<h1>Woman, Behold Thy Son: the pilot</h1>
<p>Same voice. Same words. Same music. Only the pictures and the little hand marks changed.</p>
<p><button onclick="both()">Play both together</button> <button onclick="stopAll()">Stop</button></p>
<div class="vids">
<figure><figcaption>OLD (shipped)</figcaption><video id="a" src="../woman_behold_john1926_sfx_v5hook.mp4" controls playsinline></video></figure>
<figure><figcaption>NEW (pilot)</figcaption><video id="b" src="../woman_behold_john1926_uplift_v1.mp4" controls playsinline></video></figure>
</div>
<h2>What changed (click a picture to make it big)</h2>
{pairs_html}
<h2>The 4 little marks</h2>
<p>1. Gold thread: shadow on the wall to the real cross (never on Jesus). 2. Dotted sight line: His look to her face. 3. Dotted road: John takes her home. 4. Gold thread: Mary to John, tied in a knot on "home". None while Jesus speaks. None on the last shot.</p>
<h2>Checks</h2>
<table>{rows}</table>
<p><b>My pick:</b> look at the two videos, then tell me: better, same, or worse? If better, I run the same method on Empty Tomb next.</p>
<div id="zoom" onclick="this.style.display='none'"><img id="zi"></div>
<script>
function z(i){{document.getElementById('zi').src=i.src.replace('.jpg','.jpg');document.getElementById('zoom').style.display='flex'}}
function both(){{var a=document.getElementById('a'),b=document.getElementById('b');a.currentTime=0;b.currentTime=0;a.play();b.play()}}
function stopAll(){{document.getElementById('a').pause();document.getElementById('b').pause()}}
</script></body></html>"""
(U / "_PILOT_REVIEW.html").write_text(html, encoding="utf-8")
print("written", U / "_PILOT_REVIEW.html")
