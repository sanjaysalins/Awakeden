"""Per-pilot gallery of the CLIPS that compose each final mp4, in PLAY ORDER (from edit_plan),
each clip pulled from the pool OR the quarantine so it matches the video the user watched."""
import json, html
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent

PILOTS = [
    ("Isaiah 53:5 — With His Stripes", "v2/pilot/isaiah_53_5_with_his_stripes/v1"),
    ("Mockers' Words (v2)", "v2/pilot/mockers_words_ps22/v1"),
    ("Zechariah 12:10 — The One They Pierced", "v2/pilot/zechariah_12_10_pierced/v1"),
]

def fwd(p): return str(p).replace("\\", "/")

def find_clip(v1, idx):
    """The NN_*.mp4 for a scene index — visual/nbp first, else the quarantine mirror."""
    nbp = ROOT / v1 / "visual" / "nbp"
    hits = sorted(nbp.glob(f"{idx:02d}_*.mp4"))
    if hits: return hits[0], False
    q = ROOT / "_rejected_coherence" / v1 / "visual" / "nbp"
    hits = sorted(q.glob(f"{idx:02d}_*.mp4"))
    if hits: return hits[0], True
    return None, False

secs, total = [], 0
for title, v1 in PILOTS:
    d = json.loads((ROOT / v1 / "assembly/edit_plan.json").read_text(encoding="utf-8")).get("plan", {})
    order = [s.get("scene_index") for s in d.get("slots", [])]
    hero = d.get("hero_scene_index")
    seq = order + ([hero] if hero is not None else [])
    cards = []
    for n, idx in enumerate(seq):
        clip, quar = find_clip(v1, idx)
        is_hero = (idx == hero and n == len(seq) - 1)
        role = "HERO close" if is_hero else f"#{n+1}"
        if clip is None:
            cards.append(f'<div class="c miss"><div class="ph">scene {idx}<br>(clip missing)</div>'
                         f'<div class="m"><span class="t">{role} · sc{idx}</span></div></div>')
            continue
        total += 1
        src = "file:///" + fwd(clip)
        poster = clip.with_suffix(".png")
        pos = ('poster="file:///' + html.escape(fwd(poster)) + '"') if poster.exists() else ""
        qb = '<span class="qb">QUARANTINED (bad)</span>' if quar else ""
        cards.append(
            f'<div class="c{" q" if quar else ""}" data-p="{html.escape(fwd(clip))}">'
            f'<video src="{html.escape(src)}" {pos} loop muted controls preload="none" playsinline></video>'
            f'<div class="m" onclick="f(this.parentNode)"><span class="t">{role} · {clip.name}</span>{qb}'
            f'<span class="flag">DELETE / REDO</span></div></div>')
    secs.append(f'<h2>{html.escape(title)} <small>({len(seq)} clips in play order)</small></h2>'
                f'<div class="row">{"".join(cards)}</div>')

doc = (
 '<!doctype html><meta charset=utf-8><title>Pilot final CLIPS in order</title>'
 '<style>body{background:#14161a;color:#eee;font-family:system-ui;margin:0}'
 '.bar{position:sticky;top:0;background:#0d0f12;border-bottom:1px solid #333;padding:12px 18px;z-index:9}'
 '.count{color:#ff5252;font-weight:700;font-size:20px}button{font-size:15px;padding:8px 14px;border:0;border-radius:8px;background:#2a6;color:#fff;cursor:pointer}'
 'h2{padding:6px 18px;margin:18px 0 4px;border-left:5px solid #555}small{color:#888}'
 '.row{display:flex;flex-wrap:wrap;gap:12px;padding:0 18px}'
 '.c{width:250px;background:#1d2026;border:3px solid #2a2e36;border-radius:9px;overflow:hidden;position:relative}'
 '.c.q{border-color:#c80}.c.fl{border-color:#ff3b3b;box-shadow:0 0 0 2px #ff3b3b inset}'
 '.c video{width:100%;display:block;background:#000}.miss .ph{height:150px;display:flex;align-items:center;justify-content:center;color:#888;text-align:center}'
 '.m{padding:7px 9px;cursor:pointer;display:flex;flex-wrap:wrap;gap:4px;justify-content:space-between;align-items:center}'
 '.t{font-family:monospace;font-size:10px;color:#7fa}'
 '.qb{background:#c80;color:#111;font-weight:700;padding:1px 6px;border-radius:4px;font-size:9px}'
 '.flag{background:#ff3b3b;color:#fff;font-weight:700;padding:2px 7px;border-radius:6px;font-size:10px;display:none}.c.fl .flag{display:inline-block}</style>'
 '<div class="bar"><b>Clips IN each final, play order (matches the mp4 you watched)</b> '
 '<span class="count"><span id="n">0</span> flagged</span> '
 '<button onclick="cp()">Copy flagged paths</button> <button onclick="pa()" style="background:#36c">Play all</button>'
 '<span style="color:#9a9"> · gold = already quarantined</span></div>'
 + "".join(secs) +
 '<script>const F=new Set();function f(c){if(!c.dataset.p)return;const p=c.dataset.p;if(c.classList.toggle("fl"))F.add(p);else F.delete(p);'
 'document.getElementById("n").textContent=F.size;}'
 'function cp(){navigator.clipboard.writeText([...F].sort().join("\\n"));alert(F.size+" clip paths copied — paste back to Claude");}'
 'function pa(){document.querySelectorAll("video").forEach(v=>{v.play().catch(()=>{});});}</script>'
)
out = ROOT / "v2/coherence_audit/pilots_clips_review.html"
out.write_text(doc, encoding="utf-8")
print(f"wrote {total} clips (in play order, pool+quarantine) -> {out}")
