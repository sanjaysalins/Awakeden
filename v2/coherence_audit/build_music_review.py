import json, html
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
designs = {d["title"]: d for d in json.loads((ROOT / "v2/coherence_audit/music_designs.json").read_text(encoding="utf-8"))}
shorts = [(d.name, d) for d in sorted((ROOT / "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts").glob("*"))]
shorts += [(d.name, d / "v1") for d in sorted((ROOT / "v2/pilot").glob("*"))]
def fwd(p): return str(p).replace("\\", "/")
cards = []
for title, folder in shorts:
    f = folder / "assembly/viral_cut_sfx_music_captioned.mp4"
    if not f.exists():
        continue
    lens = designs.get(title, {}).get("winner_lens", "").split("(")[0].split("—")[0].strip()
    why = html.escape(designs.get(title, {}).get("why", "")[:200])
    cards.append(
        f'<div class="c"><video src="file:///{html.escape(fwd(f))}" controls preload="none" playsinline></video>'
        f'<div class="m"><b>{html.escape(title)}</b><div class="l">{html.escape(lens)}</div>'
        f'<div class="w">{why}</div></div></div>')
doc = ('<!doctype html><meta charset=utf-8><title>Music review — all scores</title>'
 '<style>body{background:#14161a;color:#eee;font-family:system-ui;margin:0;padding:16px}'
 'h1{font-size:20px}.row{display:flex;flex-wrap:wrap;gap:16px}'
 '.c{width:300px;background:#1d2026;border:1px solid #333;border-radius:10px;overflow:hidden}'
 '.c video{width:100%;display:block;background:#000}.m{padding:9px 11px}.l{color:#ffd24d;font-size:12px;margin-top:3px}'
 '.w{color:#9aa;font-size:11px;margin-top:5px}</style>'
 '<h1>Panel-designed scores — ear-review all (tap to play)</h1><div class="row">' + "".join(cards) + '</div>')
out = ROOT / "v2/coherence_audit/music_review.html"
out.write_text(doc, encoding="utf-8")
print(f"wrote {len(cards)} -> {out}")
