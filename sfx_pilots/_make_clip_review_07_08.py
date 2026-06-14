"""Build a clip-review gallery (inline videos) for Psalm 22 shorts #07 + #08."""
import os, json, html

ROOT = r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross\v1\shorts"
OUT = os.path.join(ROOT, "_REVIEW_07_08_clips.html")

SHORTS = ["07_The_Body_Foretold", "08_I_Thirst"]

def scenes_for(short):
    p = os.path.join(ROOT, short, "visual", "scene_plan.json")
    d = json.load(open(p, encoding="utf-8"))
    arr = d["plan"]["scenes"] if "plan" in d else d["scenes"]
    return {s["index"]: s for s in arr}

cards = []
for short in SHORTS:
    by = scenes_for(short)
    title = short.replace("_", " ")
    cards.append(f'<h2 style="margin:34px 8px 6px;font-size:26px">{html.escape(title)}</h2>')
    cards.append('<div class="grid">')
    nbp = os.path.join(ROOT, short, "visual", "nbp")
    for idx in sorted(by):
        sc = by[idx]
        # find the mp4 for this scene by its index prefix
        mp4 = None
        for fn in os.listdir(nbp):
            if fn.endswith(".mp4") and fn[:2] == f"{idx:02d}":
                mp4 = fn
                break
        if not mp4:
            continue
        rel = f"{short}/visual/nbp/{mp4}"
        poster = rel[:-4] + ".png"
        # cache-buster from the mp4's mtime so the browser fetches the latest re-animation
        try:
            cb = int(os.path.getmtime(os.path.join(nbp, mp4)))
        except OSError:
            cb = 0
        relv = f"{rel}?t={cb}"
        posterv = f"{poster}?t={cb}"
        cards.append(f'''
        <div class="card">
          <video src="{relv}" poster="{posterv}" controls loop muted playsinline preload="metadata"></video>
          <div class="meta">
            <div class="hd"><span class="num">{idx:02d}</span> {html.escape(sc["title"])}</div>
            <div class="note">{html.escape(sc.get("emotional_tone",""))}</div>
          </div>
        </div>''')
    cards.append('</div>')

doc = f'''<!doctype html><html><head><meta charset="utf-8">
<title>Psalm 22 #07 + #08 - CLIP review</title>
<style>
 body{{background:#141414;color:#eee;font-family:Segoe UI,Arial,sans-serif;margin:0;padding:20px}}
 h1{{font-size:30px;margin:8px}}
 .lead{{color:#bbb;margin:8px;max-width:920px;line-height:1.5}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px;padding:8px}}
 .card{{background:#222;border:2px solid #333;border-radius:10px;overflow:hidden;display:flex;flex-direction:column}}
 .card video{{width:100%;display:block;background:#000;cursor:pointer}}
 .meta{{padding:9px 12px}}
 .hd{{font-size:15px;font-weight:600;margin-bottom:4px}}
 .num{{display:inline-block;background:#444;border-radius:5px;padding:1px 7px;margin-right:5px;font-size:13px}}
 .note{{font-size:12.5px;color:#bbb}}
</style></head><body>
<h1>Psalm 22 shorts - CLIP review: #07 The Body Foretold &amp; #08 I Thirst</h1>
<p class="lead">Each card is the animated 10s Kling clip (▶ play / loops, muted). Watch for: melting / morphing faces or hands,
warping, or motion that looks wrong. Tell me the scene numbers to redo and I'll re-animate them (and rebuild the cut).
If a clip won't play, click it or use the browser controls.</p>
{''.join(cards)}
</body></html>'''

open(OUT, "w", encoding="utf-8").write(doc)
print("wrote", OUT)
