"""Build ONE self-contained HTML page of every still for human flagging.

The user flags stills that are BAD but the pipeline did NOT catch (false negatives) — those
flags become the ground-truth calibration set for the IMG-COHERENT gate (spec §A6).

Each card shows: the still (full-size on click), its source short, the full ABSOLUTE path
(selectable), the pipeline's COHERENCE verdict (PASS / FAIL / PENDING from *.png.coherence.json)
and the legacy IMG-* audit verdict (*.png.audit.json). A 🚩 toggle marks it bad; a sticky bar
exports the flagged absolute paths (copy / download JSON).

Run: .venv\\Scripts\\python.exe v2\\coherence_audit\\build_review_page.py
Out: v2\\coherence_audit\\stills_review.html
"""
from __future__ import annotations
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent          # repo root
OUT = Path(__file__).resolve().parent / "stills_review.html"


def _stills() -> list[Path]:
    pngs: list[Path] = []
    # scene render dirs (shorts / pilots / longform)
    for base in ("longform", "v2/pilot"):
        for p in (ROOT / base).rglob("*.png"):
            s = str(p).replace("\\", "/")
            if "/visual/" not in s:
                continue
            if any(t in s for t in ("_qc", "_old", "_rejected", "_clipqc", "/refs/", "/_audit")):
                continue
            pngs.append(p)
    # libraries
    for base in ("image_library", "_library"):
        for p in (ROOT / base).rglob("*.png"):
            s = str(p).replace("\\", "/")
            if any(t in s for t in ("_qc", "/refs/")):
                continue
            pngs.append(p)
    return sorted(set(pngs))


def _read_json(p: Path) -> dict | None:
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _coh_badge(png: Path):
    d = _read_json(png.with_suffix(".png.coherence.json"))
    if d is None:
        return ("PENDING", "pending", "")
    if not d.get("audited"):
        return ("UNAUDITED", "pending", d.get("note", ""))
    if d.get("passed"):
        return ("PASS", "pass", "")
    return ("FAIL", "fail", "; ".join(d.get("fail_reasons") or []))


def _aud_badge(png: Path):
    d = _read_json(png.with_suffix(".png.audit.json"))
    if d is None:
        return ("—", "none")
    return ("PASS", "pass") if d.get("passed") else ("FAIL", "fail")


def _group(p: Path) -> str:
    s = str(p.relative_to(ROOT)).replace("\\", "/")
    for marker in ("/shorts/",):
        if marker in s:
            head = s.split("/visual/")[0]
            return head.split("/shorts/")[0].split("/")[-1] + " / " + head.split("/shorts/")[-1]
    return s.split("/visual/")[0] if "/visual/" in s else s.rsplit("/", 1)[0]


def build() -> Path:
    stills = _stills()
    groups: dict[str, list[Path]] = {}
    for p in stills:
        groups.setdefault(_group(p), []).append(p)

    cards = []
    for g in sorted(groups):
        cards.append(f'<h2 class="grp">{html.escape(g)} <span class="gn">({len(groups[g])})</span></h2>')
        cards.append('<div class="row">')
        for p in groups[g]:
            ap = str(p).replace("\\", "/")
            src = "file:///" + ap
            coh_txt, coh_cls, coh_why = _coh_badge(p)
            aud_txt, aud_cls = _aud_badge(p)
            why = f'<div class="why">{html.escape(coh_why)}</div>' if coh_why else ""
            cards.append(f'''<div class="card" data-path="{html.escape(ap)}" onclick="flag(this)">
  <div class="imgwrap"><img loading="lazy" src="{html.escape(src)}" alt=""></div>
  <div class="meta">
    <span class="badge {coh_cls}">coherence: {coh_txt}</span>
    <span class="badge {aud_cls}">audit: {aud_txt}</span>
    {why}
    <div class="path">{html.escape(ap)}</div>
  </div>
  <div class="flagtag">🚩 BAD</div>
</div>''')
        cards.append('</div>')

    doc = f'''<!doctype html><html><head><meta charset="utf-8">
<title>Stills review — flag the bad ones the pipeline missed</title>
<style>
 body{{font-family:system-ui,Arial,sans-serif;margin:0;background:#14161a;color:#e8e6e0}}
 .bar{{position:sticky;top:0;z-index:9;background:#0d0f12;border-bottom:1px solid #333;
   padding:12px 18px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}}
 .bar b{{font-size:18px}} .count{{font-size:20px;color:#ff5252;font-weight:700}}
 button{{font-size:15px;padding:8px 14px;border-radius:8px;border:0;cursor:pointer;background:#2a6;color:#fff}}
 button.alt{{background:#36c}} .hint{{color:#9a9;font-size:13px}}
 h2.grp{{padding:6px 18px;margin:22px 0 6px;border-left:5px solid #555;font-size:17px}}
 .gn{{color:#888;font-weight:400}}
 .row{{display:flex;flex-wrap:wrap;gap:14px;padding:0 18px}}
 .card{{width:300px;background:#1d2026;border:3px solid #2a2e36;border-radius:10px;overflow:hidden;
   cursor:pointer;position:relative;transition:border-color .1s}}
 .card:hover{{border-color:#567}}
 .card.flagged{{border-color:#ff3b3b;box-shadow:0 0 0 2px #ff3b3b inset}}
 .imgwrap{{background:#000;text-align:center}} .card img{{max-width:100%;display:block;margin:auto}}
 .meta{{padding:8px 10px;font-size:12px}}
 .badge{{display:inline-block;padding:2px 7px;border-radius:5px;margin:2px 4px 2px 0;font-weight:600}}
 .pass{{background:#1c3;color:#031}} .fail{{background:#f44;color:#fff}}
 .pending{{background:#888;color:#111}} .none{{background:#444;color:#bbb}}
 .why{{color:#ffb3b3;margin:4px 0;font-size:11px}}
 .path{{color:#7fa;word-break:break-all;font-family:monospace;font-size:10px;margin-top:5px;user-select:all}}
 .flagtag{{position:absolute;top:6px;right:6px;background:#ff3b3b;color:#fff;font-weight:700;
   padding:3px 8px;border-radius:6px;font-size:12px;display:none}}
 .card.flagged .flagtag{{display:block}}
 #out{{width:100%;height:120px;background:#0d0f12;color:#7fa;border:1px solid #333;font-family:monospace;display:none}}
</style></head><body>
<div class="bar">
  <b>Flag the BAD stills the pipeline missed</b>
  <span class="count"><span id="n">0</span> flagged</span>
  <button onclick="copyList()">Copy flagged paths</button>
  <button class="alt" onclick="dl()">Download JSON</button>
  <button class="alt" onclick="toggleOut()">Show/hide list</button>
  <span class="hint">Click a card to flag/unflag. Red border = flagged. {len(stills)} stills total.</span>
</div>
<textarea id="out" readonly></textarea>
{''.join(cards)}
<script>
 const flagged=new Set();
 function flag(c){{const p=c.dataset.path; if(c.classList.toggle('flagged'))flagged.add(p);else flagged.delete(p);
   document.getElementById('n').textContent=flagged.size; render();}}
 function list(){{return [...flagged].sort();}}
 function render(){{document.getElementById('out').value=list().join('\\n');}}
 function copyList(){{navigator.clipboard.writeText(list().join('\\n'));
   alert(flagged.size+' path(s) copied. Paste them back to Claude.');}}
 function dl(){{const b=new Blob([JSON.stringify({{flagged_bad:list()}},null,2)],{{type:'application/json'}});
   const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='flagged_bad.json';a.click();}}
 function toggleOut(){{const o=document.getElementById('out');o.style.display=o.style.display=='block'?'none':'block';render();}}
</script>
</body></html>'''
    OUT.write_text(doc, encoding="utf-8")
    return OUT


if __name__ == "__main__":
    out = build()
    n = len(_stills())
    print(f"wrote {n} stills -> {out}")
