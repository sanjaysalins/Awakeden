#!/usr/bin/env python
r"""stills_gate.py — mandatory STILLS-FIRST human gate + quality rubric (#1 + #2).

Root cause it fixes (2026-07-07): the batch/living-page renderers (`_render_stills.py`)
run ONLY a $0 prompt text-lint — no pixel audit, no human checkpoint — so the sole
defence before animation/rebuild spend was one agent's manual eyeball. This adds:

  #1 HUMAN GATE  — after render, emit a contact sheet + review page; NO animate/rebuild
                   spend until every still is human-approved (hash-bound, fail-closed).
  #2 QUALITY RUBRIC — every still is scored (by the in-chat agent, not the renderer) on
                   anatomy / believable / reads-as-intended / not-grotesque / style-consistent
                   — a whole-set quality pass, not a single-element checklist.

Both verdicts are hash-bound to the PNG: re-render a still and its approval + quality
go stale, so the gate re-fails (like the bible_gate chokepoint).

Usage:
  .venv\Scripts\python.exe stills_gate.py <piece> --build          # contact sheet + review.html + gate.json (pending)
  .venv\Scripts\python.exe stills_gate.py --rubric                 # print the quality rubric
  .venv\Scripts\python.exe stills_gate.py <piece> --quality <slug> <PASS|FAIL> --axes anatomy,believable,... --notes "..."
  .venv\Scripts\python.exe stills_gate.py <piece> --approve <slug|all> [--notes "..."]
  .venv\Scripts\python.exe stills_gate.py <piece> --apply <feedback.json>   # apply exported review decisions
  .venv\Scripts\python.exe stills_gate.py <piece> --check [--stage animate|build]   # fail-closed (exit 3)

`<piece>` = the episode folder (its `visual/` holds the stills). Grandfathered: a piece
with no `.stills_gate.json` and BUILD never run is skipped by --check (warn), so long-form
and legacy pieces are unaffected until you opt them in with --build.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

from render_lint.verify import is_production_png  # reuse the story-still filter

RUBRIC_AXES = ["anatomy", "believable", "reads_as_intended", "not_grotesque", "style_consistent",
               "world_consistent"]
RUBRIC = """QUALITY RUBRIC (#2) — score EVERY still, viewing the whole set as a contact sheet first.
A still PASSes only if ALL five axes pass. Judge the image, not just the one thing you changed.
  - anatomy         : hands/faces/limbs correct; no extra/merged/missing parts, no floating objects.
  - believable      : nothing fantasy or incongruous (no giant/ornamental hardware, no gibberish
                      text or signs, no random props); physically plausible AND physically CONNECTED
                      — a nailed hand is PINNED to the cross (not a floating palm), a crucified/bound
                      figure is actually attached, objects connect to whatever holds them.
  - reads_as_intended: at a glance it reads as the intended subject + action (e.g. a MOCKING crowd
                      actually looks hostile, not like mourners).
  - not_grotesque   : wounds/blood are restrained and reverent — not gaping black holes, gore, or horror.
  - style_consistent: matches the inked graphic-novel style AND the rest of this set (faces, palette).
  - world_consistent: every RECURRING subject (the tomb, the stone, a character's face/dress, a
                      location) looks like the SAME thing in every still it appears in — same shape,
                      same materials, same scale. Judge from the contact sheet, side by side; one
                      episode is ONE world (a disc stone in one still cannot be a boulder in another)."""


def _visual(piece: Path) -> Path:
    return piece if piece.name == "visual" else piece / "visual"


def _stills(piece: Path) -> list[Path]:
    v = _visual(piece)
    return sorted(p for p in v.glob("*.png") if is_production_png(p))


def _hash(png: Path) -> str:
    return hashlib.sha256(png.read_bytes()).hexdigest()[:16]


def _gate_path(piece: Path) -> Path:
    return _visual(piece) / ".stills_gate.json"


def _load_gate(piece: Path) -> dict:
    p = _gate_path(piece)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"stills": {}}


def _save_gate(piece: Path, g: dict) -> None:
    _gate_path(piece).write_text(json.dumps(g, indent=2), encoding="utf-8")


# ---------------- #1 build: contact sheet + review page + pending gate ----------------
def _contact_sheet(stills: list[Path], out: Path, cols: int = 5) -> None:
    from PIL import Image, ImageDraw
    tw, th, pad, lab = 300, 533, 8, 22
    rows = (len(stills) + cols - 1) // cols
    W = cols * (tw + pad) + pad
    H = rows * (th + lab + pad) + pad
    sheet = Image.new("RGB", (W, H), (12, 12, 14))
    d = ImageDraw.Draw(sheet)
    for i, s in enumerate(stills):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = pad + r * (th + lab + pad)
        try:
            im = Image.open(s).convert("RGB")
            im.thumbnail((tw, th))
            sheet.paste(im, (x + (tw - im.width) // 2, y + lab + (th - im.height) // 2))
        except Exception as e:
            d.text((x + 4, y + lab + 4), f"[open error] {e}", fill=(220, 90, 90))
        d.text((x + 4, y + 4), s.stem, fill=(245, 196, 81))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=88)


def _furl(p: Path) -> str:
    return "file:///" + str(p).replace("\\", "/")


def _review_html(piece: Path, stills: list[Path]) -> str:
    v = _visual(piece)
    scenes = []
    for s in stills:
        clip = v / "clips" / f"{s.stem}.mp4"
        q = v / f"{s.stem}.quality.json"
        qv, qn = None, ""
        if q.exists():
            qd = json.loads(q.read_text(encoding="utf-8"))
            qv, qn = qd.get("verdict"), qd.get("notes", "")
        scenes.append({"slug": s.stem, "png": _furl(s),
                       "clip": _furl(clip) if clip.exists() else "", "quality": qv, "qnotes": qn})
    data = json.dumps(scenes)
    tpl = r"""<!doctype html><html><head><meta charset="utf-8"><title>Stills gate — __NAME__</title>
<style>
 body{background:#0f0f11;color:#eee;font-family:system-ui,Arial,sans-serif;margin:0;padding:18px 22px 110px}
 h1{font-size:20px;margin:0 0 2px} .sub{color:#9aa;font-size:13px;margin-bottom:14px}
 .contact{width:100%;max-width:1500px;border:1px solid #333;border-radius:8px;margin-bottom:20px}
 .card{background:#191920;border:1px solid #333;border-radius:12px;padding:14px;margin:0 0 16px;display:flex;gap:18px;flex-wrap:wrap}
 .card.approved{border-color:#3a7} .card.rejected{border-color:#c55}
 .col{flex:1;min-width:290px}
 .slug{font-family:monospace;color:#7ec8ff;font-size:15px}
 .q{font-size:12px;margin:2px 0 6px} .q.PASS{color:#6d6} .q.FAIL{color:#e77} .q.none{color:#888}
 .qn{font-size:12px;color:#cb9;background:#141410;border:1px solid #3a3520;border-radius:6px;padding:6px 8px;margin:0 0 8px;white-space:pre-wrap}
 img,video{max-width:100%;width:330px;border-radius:6px;display:block;background:#000}
 .btns{margin-top:8px} .btns button{font-size:14px;margin:0 8px 0 0;padding:7px 16px;border-radius:8px;border:1px solid #555;background:#26262e;color:#eee;cursor:pointer}
 .btns button.a.on{background:#3a7;border-color:#3a7;color:#fff} .btns button.r.on{background:#c55;border-color:#c55;color:#fff}
 textarea{width:100%;box-sizing:border-box;height:52px;background:#111;color:#eee;border:1px solid #444;border-radius:6px;padding:6px;font-size:13px;margin-top:8px}
 .noclip{color:#c66;font-size:13px;padding:16px 0}
 #bar{position:fixed;left:0;right:0;bottom:0;background:#1c1c24;border-top:1px solid #444;padding:10px 22px;display:flex;gap:12px;align-items:center}
 #bar button{font-size:14px;padding:8px 16px;border-radius:8px;border:none;background:#3a7;color:#fff;cursor:pointer}
 #out{position:fixed;inset:5%;background:#111;border:1px solid #555;border-radius:10px;padding:16px;display:none;z-index:9;flex-direction:column}
 #out textarea{flex:1;height:auto;background:#0a0a0a;color:#8f8;font-family:monospace}
</style></head><body>
<h1>Stills gate — __NAME__</h1>
<div class="sub">Look at the WHOLE set first. Then Approve/Reject each still and add notes. Nothing gets animated or rebuilt until you approve. Then Export and paste back.</div>
<img class="contact" src="__CONTACT__">
<div id="app"></div>
<div id="bar"><button onclick="exportAll()">⬇ Export decisions (paste back to me)</button>
<span class="sub" style="margin:0">approve = keep · needs rebuild = redo (add a note saying what to fix)</span></div>
<div id="out"><b>Paste this back into the chat:</b><textarea id="ot" readonly></textarea>
<div style="margin-top:10px"><button onclick="copyOut()">Copy</button>
<button style="background:#555" onclick="document.getElementById('out').style.display='none'">Close</button></div></div>
<script>
const S=__DATA__; const st={};
S.forEach(s=>st[s.slug]={decision:null,notes:""});
function render(){const a=document.getElementById('app');a.innerHTML='';
 S.forEach(s=>{const c=document.createElement('div');c.className='card';c.id='c-'+s.slug;
  const qc=s.quality?('q '+s.quality):'q none';const qt=s.quality?('agent quality: '+s.quality):'agent quality: (not scored)';
  const qn=s.qnotes?`<div class="qn">📋 agent audit: ${s.qnotes}</div>`:'';
  c.innerHTML=`<div class="col"><div class="slug">${s.slug}</div><div class="${qc}">${qt}</div>${qn}
   <a href="${s.png}" target="_blank" title="open full-res"><img src="${s.png}"></a></div>
   <div class="col">${s.clip?`<video src="${s.clip}" controls loop muted playsinline></video>`:`<div class="noclip">— no clip yet —</div>`}
   <div class="btns"><button class="a" data-s="${s.slug}">✓ Approve</button><button class="r" data-s="${s.slug}">✗ Needs REBUILD</button></div>
   <textarea data-s="${s.slug}" placeholder="notes (what's wrong / how to rebuild it)"></textarea></div>`;
  a.appendChild(c);});
 document.querySelectorAll('.btns button').forEach(b=>b.onclick=()=>{const s=b.dataset.s;const dec=b.classList.contains('a')?'approve':'reject';
  st[s].decision=dec;const card=document.getElementById('c-'+s);card.className='card '+(dec==='approve'?'approved':'rejected');
  card.querySelectorAll('.a,.r').forEach(x=>x.classList.remove('on'));b.classList.add('on');});
 document.querySelectorAll('textarea[data-s]').forEach(t=>t.oninput=()=>st[t.dataset.s].notes=t.value);}
function exportAll(){const out=S.map(s=>({slug:s.slug,decision:st[s.slug].decision,notes:st[s.slug].notes.trim()||undefined}))
  .filter(x=>x.decision||x.notes);
 document.getElementById('ot').value="STILLS GATE DECISIONS ("+"__NAME__"+")\n"+JSON.stringify(out,null,2);
 document.getElementById('out').style.display='flex';}
function copyOut(){const t=document.getElementById('ot');t.select();document.execCommand('copy');}
render();
</script></body></html>"""
    return (tpl.replace("__DATA__", data).replace("__NAME__", piece.name)
            .replace("__CONTACT__", _furl(v / "_review" / "contact.jpg")))


def build(piece: Path) -> None:
    stills = _stills(piece)
    if not stills:
        sys.exit(f"no production stills in {_visual(piece)}")
    v = _visual(piece)
    _contact_sheet(stills, v / "_review" / "contact.jpg")
    (v / "_review" / "review.html").write_text(_review_html(piece, stills), encoding="utf-8")
    g = _load_gate(piece)
    g["stills"] = {s.stem: {"hash": _hash(s),
                            **{k: g["stills"].get(s.stem, {}).get(k) for k in ("quality", "quality_hash", "approved", "approved_hash")}}
                   for s in stills}
    _save_gate(piece, g)
    review = _furl(v / "_review" / "review.html")
    print(f"BUILT stills gate for {piece.name}: {len(stills)} stills (all PENDING review)")
    print(f"  contact sheet: {_furl(v / '_review' / 'contact.jpg')}")
    print(f"  REVIEW PAGE : {review}")
    print("  -> agent: run --rubric, score each still with --quality; user: approve in the review page.")


def record_quality(piece: Path, slug: str, verdict: str, axes: str, notes: str) -> None:
    v = _visual(piece)
    png = v / f"{slug}.png"
    if not png.exists():
        sys.exit(f"no such still: {slug}")
    h = _hash(png)
    (v / f"{slug}.quality.json").write_text(json.dumps({
        "slug": slug, "hash": h, "verdict": verdict.upper(),
        "axes": {a: (a in [x.strip() for x in axes.split(",") if x.strip()]) for a in RUBRIC_AXES},
        "notes": notes, "reviewer": "in-chat-agent",
    }, indent=2), encoding="utf-8")
    g = _load_gate(piece)
    g.setdefault("stills", {}).setdefault(slug, {})["hash"] = h
    g["stills"][slug]["quality"] = verdict.upper()
    g["stills"][slug]["quality_hash"] = h
    _save_gate(piece, g)
    print(f"quality {verdict.upper()} recorded for {slug}")


def approve(piece: Path, slugs: list[str], notes: str = "") -> None:
    g = _load_gate(piece)
    v = _visual(piece)
    targets = [s.stem for s in _stills(piece)] if slugs == ["all"] else slugs
    for slug in targets:
        png = v / f"{slug}.png"
        if not png.exists():
            print(f"  skip (no still): {slug}"); continue
        h = _hash(png)
        g.setdefault("stills", {}).setdefault(slug, {})["hash"] = h
        g["stills"][slug]["approved"] = True
        g["stills"][slug]["approved_hash"] = h
        if notes:
            g["stills"][slug]["approve_notes"] = notes
    _save_gate(piece, g)
    print(f"approved: {', '.join(targets)}")


def apply_feedback(piece: Path, feedback_json: Path) -> None:
    """Apply the review page's exported decisions: approve the approved, mark rejects for redo."""
    txt = feedback_json.read_text(encoding="utf-8")
    txt = txt[txt.index("["):txt.rindex("]") + 1]  # tolerate a leading title line
    decisions = json.loads(txt)
    ap = [d["slug"] for d in decisions if d.get("decision") == "approve"]
    rej = [(d["slug"], d.get("notes", "")) for d in decisions if d.get("decision") == "reject"]
    if ap:
        approve(piece, ap)
    g = _load_gate(piece)
    for slug, note in rej:
        g.setdefault("stills", {}).setdefault(slug, {})["approved"] = False
        g["stills"][slug]["reject_notes"] = note
    _save_gate(piece, g)
    print(f"applied: {len(ap)} approved, {len(rej)} rejected (need redo)")
    for slug, note in rej:
        print(f"  REJECT {slug}: {note}")


def check(piece: Path, stage: str = "animate") -> int:
    g = _load_gate(piece)
    if not g.get("stills"):
        print(f"[stills-gate] no gate for {piece.name} (grandfathered — run --build to enforce). SKIP.")
        return 0
    problems = []
    for s in _stills(piece):
        rec = g["stills"].get(s.stem, {})
        h = _hash(s)
        if rec.get("quality") != "PASS" or rec.get("quality_hash") != h:
            problems.append(f"{s.stem}: quality not PASS/current ({rec.get('quality')})")
        if not rec.get("approved") or rec.get("approved_hash") != h:
            problems.append(f"{s.stem}: NOT human-approved / stale (re-rendered since approval)")
    if problems:
        print(f"[stills-gate] BLOCKED before {stage} — {len(problems)} still(s) not GREEN:")
        for p in problems:
            print("   X", p)
        print("  Fix: score with --quality, get user approval in the review page (--apply), then re-check.")
        return 3
    print(f"[stills-gate] GREEN — all {len(g['stills'])} stills quality-PASS + human-approved. OK to {stage}.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("piece", nargs="?", help="episode folder (holds visual/)")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--rubric", action="store_true")
    ap.add_argument("--quality", nargs="+", metavar=("SLUG", "VERDICT"), help="<slug> <PASS|FAIL>")
    ap.add_argument("--axes", default="", help="comma list of PASSING axes for --quality")
    ap.add_argument("--approve", default="", help="slug or 'all'")
    ap.add_argument("--apply", default="", help="exported review feedback json file")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--stage", default="animate")
    ap.add_argument("--notes", default="")
    a = ap.parse_args()
    if a.rubric:
        print(RUBRIC); return
    if not a.piece:
        ap.error("piece folder required")
    piece = Path(a.piece).resolve()
    if a.build:
        build(piece)
    elif a.quality:
        record_quality(piece, a.quality[0], a.quality[1], a.axes, a.notes)
    elif a.approve:
        approve(piece, [s.strip() for s in a.approve.split(",")], a.notes)
    elif a.apply:
        apply_feedback(piece, Path(a.apply))
    elif a.check:
        sys.exit(check(piece, a.stage))
    else:
        ap.error("pick an action: --build / --rubric / --quality / --approve / --apply / --check")


if __name__ == "__main__":
    main()
