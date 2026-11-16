import json, html
base = r"F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_living_comic"
ep = json.load(open(base + r"\episode_mockers.json", encoding="utf-8"))
rows = ""
for p in ep["panels"]:
    flags = []
    if p.get("ink_wake"): flags.append("ink wake")
    if p.get("sacred"): flags.append("sacred: no sfx")
    bal = [b["text"] for b in ep["balloons"] if p["t"][0] - 1e-6 <= b["t"][0] < p["t"][1]]
    cards = [" ".join(c["lines"]) for c in ep["cards"] if p["t"][0] - 1e-6 <= c["t"][0] < p["t"][1]]
    rows += "<tr><td><b>%s</b><br>%.1f-%.1fs</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
        html.escape(p["id"]), p["t"][0], p["t"][1], html.escape(p["beat"]), html.escape(p["still_prompt"]),
        html.escape(p["clip_tier"] + ((" · " + ", ".join(flags)) if flags else "")),
        html.escape(" | ".join(cards + bal)) or "-")
c = ep["cost_estimate"]
page = """<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Piece 2 Panel Map</title>
<style>:root{--bg:#f7f3ea;--ink:#1b1b1b;--card:#fff;--gold:#b8860b;--mute:#555;--red:#b3261e;--grn:#1e7a3c}
@media (prefers-color-scheme:dark){:root{--bg:#15171c;--ink:#f1ede2;--card:#20232a;--gold:#e0b44a;--mute:#aaa;--red:#ff8a80;--grn:#7fd99a}}
body{margin:0;background:var(--bg);color:var(--ink);font:20px/1.5 system-ui,Segoe UI,sans-serif;padding:0 16px 60px}.w{max-width:1100px;margin:auto}
h1{font-size:2rem;margin:26px 0 4px}h2{font-size:1.4rem;margin:30px 0 8px;border-left:8px solid var(--gold);padding-left:12px}
.box{background:var(--card);border-radius:12px;padding:14px 18px;margin:12px 0}.pick{border:3px solid var(--gold)}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:10px;overflow:hidden}td,th{padding:8px 9px;text-align:left;border-bottom:1px solid #8883;font-size:.9rem;vertical-align:top}th{background:#8882}
.g{color:var(--grn);font-weight:700}li{margin:6px 0}</style></head><body><div class=w>
<h1>Piece 2: The Mockers' Words</h1><p>Psalm 22:7-8 + Matthew 27. Panel map only. No stills, no clips, no spend.</p>
<div class="box pick"><b>Gates: <span class=g>8 of 8 PASS</span>.</b> The gate found one real fault (a Psalm balloon on screen 1.7s, needs 2.2s) and I fixed it.<br>
Jesus never speaks in this piece. <b>Zero invented lines.</b> Every balloon is KJV: David (Ps 22:7-8) and the mocker (Matt 27:43, 27:40).<br>
Words are locked (KJV verbatim, 78.0s voice already recorded).</div>
<h2>14 panels, one big panel at a time</h2>
<table><tr><th>Panel</th><th>Narration beat</th><th>Still idea (new Gold Seam still needed)</th><th>Clip tier</th><th>Cards and balloons</th></tr>""" + rows + """</table>
<h2>Estimated cost (NOT an order)</h2><ul><li>Stills: """ + html.escape(c["stills"]) + """</li><li>Clips: """ + html.escape(c["clips"]) + """</li><li>Voice: $0, audio exists</li><li><b>""" + html.escape(c["total"]) + """</b></li></ul>
<h2>Still to do before any spend ($0)</h2><ul>
<li>5 guardrail questions as a blind panel on these locked words (the rule came after the 07-03 panel).</li>
<li>Reuse-first check: do any existing mockers clips fit a panel?</li>
<li>Landing: add 3.0s hold at the end (audio and video together).</li>
<li>Witness Edge debuts here (foreground crowd silhouette). It was only tested once.</li></ul>
<div class="box pick"><b>My pick:</b> run the guardrail panel on the words now ($0). If it passes, I quote the stills price from your real invoice and ask for a yes before rendering anything.</div>
</div></body></html>"""
open(base + r"\_MOCKERS_PANEL_MAP.html", "w", encoding="utf-8").write(page)
print("ok")
