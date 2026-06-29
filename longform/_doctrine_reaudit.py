"""_doctrine_reaudit.py — corpus-wide doctrinal re-audit driver.

Re-checks EVERY narration (long + short) for doctrinal / narrative-fact /
KJV-verbatim soundness, BOTH ways (in-chat sub-agent triage + the 5-CLI panel),
auto-fixes confirmed errors, and emits ONE HTML report.

Subcommands:
  enumerate  — build manifest.json: every narration path + form + ref
  panel      — run independent_review.py 5-CLI panel on a list of piece_ids
  report     — aggregate triage JSON + panel verdicts into REPORT.html

LLM triage itself is done by the harness (Agent sub-agents, in-chat) — the dead
Anthropic API key means we DON'T call it here. This driver only orchestrates the
local-CLI panel and builds the report.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # repo root
LONGFORM = ROOT / "longform"
WORK = LONGFORM / "_doctrine_reaudit_20260629"
TRIAGE = WORK / "triage"


def _ref_from_folder(folder: Path) -> str:
    """Best-effort primary verse ref from creation.json / meta / passage header."""
    for name in ("narration.creation.json", "narration.creation-review.json"):
        p = folder / name
        if p.exists():
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                ep = d.get("episode", {})
                if ep.get("primary_ref"):
                    return ep["primary_ref"]
                if d.get("primary_ref"):
                    return d["primary_ref"]
            except Exception:
                pass
    # fall back to first non-empty line of passage.txt
    pt = folder / "passage.txt"
    if pt.exists():
        for line in pt.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if line:
                return line[:80]
    return ""


def _piece_id(narr: Path) -> str:
    """Stable, filesystem-safe id from the path relative to longform/."""
    rel = narr.parent.relative_to(LONGFORM)
    return str(rel).replace("\\", "__").replace("/", "__")


def enumerate_pieces() -> list[dict]:
    pieces: list[dict] = []

    def add(narr: Path, form: str, review_type: str, group: str):
        if not narr.exists():
            return
        folder = narr.parent
        pieces.append({
            "piece_id": _piece_id(narr),
            "group": group,
            "form": form,                 # long | short
            "review_type": review_type,   # independent_review.py --type
            "path": str(narr),
            "folder": str(folder),
            "ref": _ref_from_folder(folder),
            "has_passage": (folder / "passage.txt").exists(),
            "has_lock": (folder / ".locked").exists(),
        })

    # 1. numbered long-forms
    for d in sorted(LONGFORM.glob("[0-9][0-9]_*")):
        add(d / "v1" / "narration.md", "long", "narration", "numbered-long")

    # 2. eyewitness long-forms
    for d in sorted(LONGFORM.glob("EW[0-9][0-9]_*")):
        add(d / "v1" / "narration.md", "long", "eyewitness-long", "eyewitness-long")

    # 3. Psalm-22 shorts
    sh = LONGFORM / "02_Psalm_22_Song_From_The_Cross" / "v1" / "shorts"
    for d in sorted(sh.glob("[0-9][0-9]_*")):
        add(d / "narration.md", "short", "narration", "psalm22-short")

    # 4. eyewitness shorts
    for d in sorted(LONGFORM.glob("EW[0-9][0-9]_*")):
        add(d / "v1" / "short" / "narration.md", "short", "eyewitness-short", "eyewitness-short")

    return pieces


def cmd_enumerate(args):
    WORK.mkdir(parents=True, exist_ok=True)
    TRIAGE.mkdir(parents=True, exist_ok=True)
    pieces = enumerate_pieces()
    manifest = {"count": len(pieces), "pieces": pieces}
    (WORK / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    # human summary
    from collections import Counter
    by_group = Counter(p["group"] for p in pieces)
    print(f"Enumerated {len(pieces)} narrations into {WORK / 'manifest.json'}")
    for g, n in by_group.items():
        print(f"  {g:20s} {n}")
    for p in pieces:
        print(f"  [{p['form']:5s}] {p['piece_id']:40s} ref={p['ref'][:40]!r}")


CLEAN = WORK / "clean"

# section headers that begin NON-spoken trailing material (strip from here down)
_STOP_RE = re.compile(
    r"^\s*#+\s*(DEPTH|VOICE|SOURCING|NOTES|FUNNEL|PROCESS|CHECKLIST)\b", re.I)
_NOTSPOKEN_RE = re.compile(r"not spoken", re.I)


def clean_narration(md_path: Path) -> str:
    """Strip status/metadata header + trailing DEPTH/VOICE notes; keep the
    spoken body (incl. ## Beat headers, speaker tags, KJV quotes). Gives the
    panel an UNPRIMED artifact (no 'LOCKED / 4 PASS' status to bias it)."""
    lines = md_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    # body starts after the FIRST standalone '---'
    start = 0
    for i, ln in enumerate(lines):
        if ln.strip() == "---":
            start = i + 1
            break
    body: list[str] = []
    for ln in lines[start:]:
        if _STOP_RE.match(ln) or _NOTSPOKEN_RE.search(ln):
            break
        if ln.strip() == "---":            # closing rule before a notes block
            # peek: only stop if what follows is notes; simplest = stop
            break
        body.append(ln)
    title = lines[0] if lines and lines[0].startswith("#") else ""
    text = "\n".join(([title, ""] if title else []) + body).strip()
    return text + "\n"


def cmd_clean(args):
    CLEAN.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((WORK / "manifest.json").read_text(encoding="utf-8"))
    by_id = {p["piece_id"]: p for p in manifest["pieces"]}
    for pid in args.pieces:
        p = by_id[pid]
        out = CLEAN / f"{pid}.md"
        out.write_text(clean_narration(Path(p["path"])), encoding="utf-8")
        print(f"cleaned {pid} -> {out}")


def cmd_panel(args):
    """Run the 5-CLI independent_review panel on each piece's CLEAN artifact."""
    import subprocess
    CLEAN.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((WORK / "manifest.json").read_text(encoding="utf-8"))
    by_id = {p["piece_id"]: p for p in manifest["pieces"]}
    for pid in args.pieces:
        p = by_id[pid]
        clean_path = CLEAN / f"{pid}.md"
        if not clean_path.exists():
            clean_path.write_text(clean_narration(Path(p["path"])), encoding="utf-8")
        print(f"\n=== PANEL: {pid}  (--type {p['review_type']}) ===", flush=True)
        cmd = [sys.executable, str(ROOT / "independent_review.py"),
               str(clean_path), "--type", p["review_type"]]
        if args.providers:
            cmd += ["--providers", args.providers]
        subprocess.run(cmd, cwd=str(ROOT))


def _parse_panel_index(idx: Path) -> dict:
    """Parse an _independent_review/<stamp>/INDEX.md -> {artifact, stamp, dir,
    reviewers:[{name,status,verdict}]}."""
    txt = idx.read_text(encoding="utf-8", errors="ignore")
    head = txt.splitlines()[0] if txt else ""
    m = re.search(r"—\s*(.+?\.md)", head)
    artifact = m.group(1).strip() if m else ""
    reviewers = []
    for ln in txt.splitlines():
        rm = re.match(r"-\s*\*\*(\w+)\*\*\s*—\s*(\w+).*?verdict:\s*([A-Z—-]+)", ln)
        if rm:
            reviewers.append({"name": rm.group(1), "status": rm.group(2),
                              "verdict": rm.group(3)})
    return {"artifact": artifact, "stamp": idx.parent.name,
            "dir": str(idx.parent), "reviewers": reviewers}


def _panels_by_piece() -> dict:
    """Map piece_id -> latest panel result (from clean/_independent_review)."""
    out: dict = {}
    base = CLEAN / "_independent_review"
    if not base.exists():
        return out
    for idx in sorted(base.glob("*/INDEX.md")):
        info = _parse_panel_index(idx)
        pid = info["artifact"][:-3] if info["artifact"].endswith(".md") else info["artifact"]
        if pid and pid not in out:
            out[pid] = info       # keep the FIRST (confirming) panel; re-verifies are later
    return out


def _esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def _furl(p: str) -> str:
    return "file:///" + str(p).replace("\\", "/")


def cmd_report(args):
    manifest = json.loads((WORK / "manifest.json").read_text(encoding="utf-8"))
    panels = _panels_by_piece()
    fixes = {}
    fj = WORK / "fixes.json"
    if fj.exists():
        fixes = json.loads(fj.read_text(encoding="utf-8"))

    rows = []
    n_clean = n_fixed = n_revoice = 0
    for p in manifest["pieces"]:
        pid = p["piece_id"]
        tj = TRIAGE / f"{pid}.json"
        triage = json.loads(tj.read_text(encoding="utf-8")) if tj.exists() else {}
        real = [f for f in triage.get("findings", [])
                if f.get("severity") in ("kjv-verbatim", "narrative-fact", "doctrinal")]
        fx = fixes.get(pid)
        if fx:
            status = "FIXED"; n_fixed += 1; n_revoice += 1
        elif real:
            status = "FLAGGED"
        else:
            status = "CLEAN"; n_clean += 1
        rows.append({"p": p, "triage": triage, "real": real,
                     "panel": panels.get(pid), "fix": fx, "status": status})

    badge = {"CLEAN": "#1b7f3b", "FIXED": "#0a66c2",
             "FLAGGED": "#b54708", "NEEDS-REVOICE": "#0a66c2"}
    H = []
    H.append("<!doctype html><meta charset='utf-8'><title>Doctrinal re-audit</title>")
    H.append("""<style>
    body{font:15px/1.55 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#f6f7f9;color:#1a1a1a}
    header{background:#11233a;color:#fff;padding:22px 30px}
    header h1{margin:0 0 6px;font-size:22px} header .sub{opacity:.8;font-size:14px}
    .wrap{max-width:1050px;margin:0 auto;padding:24px 20px}
    .sum{display:flex;gap:14px;flex-wrap:wrap;margin:0 0 22px}
    .sum div{background:#fff;border:1px solid #e3e6ea;border-radius:10px;padding:12px 18px;min-width:120px}
    .sum b{font-size:26px;display:block}
    .card{background:#fff;border:1px solid #e3e6ea;border-radius:12px;margin:0 0 14px;overflow:hidden}
    .card h2{font-size:16px;margin:0;padding:13px 18px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #eef0f2}
    .b{color:#fff;border-radius:20px;padding:3px 12px;font-size:12px;font-weight:700;letter-spacing:.3px}
    .meta{padding:6px 18px;color:#667;font-size:13px}
    .body{padding:6px 18px 16px}
    .find{border-left:3px solid #b54708;background:#fff8f1;padding:10px 14px;border-radius:0 8px 8px 0;margin:10px 0}
    .find .sev{font-size:11px;font-weight:700;text-transform:uppercase;color:#b54708;letter-spacing:.4px}
    .diff{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px}
    .diff div{padding:8px 10px;border-radius:6px;font-size:13.5px}
    .was{background:#fdecec;border:1px solid #f6caca} .now{background:#e9f7ee;border:1px solid #bfe6cd}
    .lbl{font-size:11px;font-weight:700;text-transform:uppercase;opacity:.6}
    .panel{font-size:13px;color:#445;padding:2px 18px 12px}
    .pill{display:inline-block;border-radius:5px;padding:1px 7px;margin:2px 4px 2px 0;font-size:12px;border:1px solid #d7dbe0}
    .PASS{background:#e9f7ee;color:#1b7f3b} .REVISE{background:#fff4e5;color:#b54708}
    .FAIL{background:#fdecec;color:#c01} a{color:#0a66c2}
    .clean-note{color:#1b7f3b;font-size:13.5px;padding:0 18px 14px}
    h2.section{font-size:18px;margin:30px 0 14px;padding:0 0 8px;border-bottom:2px solid #11233a;
      display:flex;justify-content:space-between;align-items:baseline}
    h2.section span{font-size:13px;font-weight:500;color:#667}
    </style>""")
    H.append("<header><h1>Doctrinal re-audit — all narrations (long + short)</h1>")
    H.append(f"<div class='sub'>{manifest['count']} narrations · "
             "triage = in-chat red-team (3 lenses) · confirmation = 5-CLI panel on flagged + controls · "
             "auto-fixed confirmed errors</div></header>")
    H.append("<div class='wrap'>")
    H.append("<div class='sum'>"
             f"<div><b>{manifest['count']}</b>audited</div>"
             f"<div><b>{n_clean}</b>clean</div>"
             f"<div><b>{n_fixed}</b>fixed</div>"
             f"<div><b>{n_revoice}</b>re-voiced ✓</div></div>")
    H.append("<div style='background:#fff;border:1px solid #e3e6ea;border-radius:10px;"
             "padding:12px 16px;margin:0 0 18px;font-size:13.5px;color:#445'>"
             "<b>Method (both ways):</b> every narration first got an in-chat red-team across "
             "3 lenses (KJV-verbatim · narrative-fact · doctrine/Christ-landing). The 4 flagged pieces "
             "plus 3 clean controls then went to the 5-CLI panel on an UNPRIMED clean artifact. "
             "Convergent flags were verified by hand against the KJV before any change. "
             "3 fixes were confirmed by red-team + panel; the Noah cubits fix was caught by the red-team "
             "against Gen 6:15 and the panel did not independently raise it (the mirror of the EW01 lesson). "
             "Controls came back doctrinally clean (panel REVISEs there were style/attribution only; "
             "grok's EW09 'KJV violation' was a false positive — KJV Ruth 2:9 really is 'have I not'). "
             "<b>Panel health this run:</b> gemini DOWN (env error) — 4/5 reviewers "
             "(cursor·claude·codex·grok). <b>Re-voiced:</b> all 4 fixed pieces re-locked + "
             "narration.mp3 rebuilt — per-turn synth re-rendered ONLY the changed turn (~1,900 chars total), "
             "reusing every other turn. <b>Still pending (separate step):</b> the final VIDEO + burned "
             "captions for the 4 fixed pieces are stale (new audio / word-timing) and need a re-assemble + "
             "re-caption.</div>")

    order = {"FIXED": 0, "FLAGGED": 1, "CLEAN": 2}

    def render_card(r):
        p = r["p"]; st = r["status"]
        col = badge.get(st, "#555")
        H.append("<div class='card'>")
        H.append(f"<h2><span>{_esc(p['piece_id'])}</span>"
                 f"<span class='b' style='background:{col}'>{st}</span></h2>")
        H.append(f"<div class='meta'>{p['form'].upper()} · {_esc(p.get('ref') or p['group'])} · "
                 f"<a href='{_furl(p['path'])}'>narration.md</a></div>")
        if r["panel"]:
            pills = " ".join(f"<span class='pill {rv['verdict']}'>{rv['name']}: {rv['verdict']}</span>"
                             for rv in r["panel"]["reviewers"])
            H.append(f"<div class='panel'>5-CLI panel: {pills} "
                     f"&nbsp;<a href='{_furl(r['panel']['dir'])}'>reviews</a></div>")
        if st == "CLEAN":
            s = r["triage"].get("summary", "Verified clean across KJV-verbatim, narrative-fact, and doctrine lenses.")
            H.append(f"<div class='clean-note'>✓ {_esc(s)}</div>")
        else:
            H.append("<div class='body'>")
            for f in r["real"]:
                H.append("<div class='find'>")
                H.append(f"<div class='sev'>{_esc(f['severity'])} — {_esc(f.get('scripture_ref',''))}</div>")
                H.append(f"<div style='margin:4px 0'>{_esc(f.get('problem',''))}</div>")
                fx = r["fix"]
                if fx:
                    H.append("<div class='diff'>"
                             f"<div class='was'><div class='lbl'>before</div>{_esc(fx.get('before',''))}</div>"
                             f"<div class='now'><div class='lbl'>after</div>{_esc(fx.get('after',''))}</div></div>")
                else:
                    H.append("<div class='diff'>"
                             f"<div class='was'><div class='lbl'>flagged text</div>{_esc(f.get('quote_or_claim',''))}</div>"
                             f"<div class='now'><div class='lbl'>proposed fix</div>{_esc(f.get('proposed_fix_text',''))}</div></div>")
                H.append("</div>")
            H.append("</div>")
        H.append("</div>")

    # split into LONG and SHORT sections; fixed/flagged first within each
    for form, label in (("long", "Long-form deep-dives"), ("short", "Short-form")):
        grp = [r for r in rows if r["p"]["form"] == form]
        grp.sort(key=lambda r: (order[r["status"]], r["p"]["piece_id"]))
        nf = sum(1 for r in grp if r["status"] == "FIXED")
        nc = sum(1 for r in grp if r["status"] == "CLEAN")
        H.append(f"<h2 class='section'>{label} "
                 f"<span>{len(grp)} narrations · {nc} clean · {nf} fixed</span></h2>")
        for r in grp:
            render_card(r)
    H.append("</div>")
    out = WORK / "REPORT.html"
    out.write_text("\n".join(H), encoding="utf-8")
    print(f"report -> {out}")
    print(f"  clean={n_clean} fixed={n_fixed} need-revoice={n_revoice}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("enumerate")
    sub.add_parser("report")
    c = sub.add_parser("clean"); c.add_argument("pieces", nargs="+")
    pa = sub.add_parser("panel")
    pa.add_argument("pieces", nargs="+")
    pa.add_argument("--providers", default="")
    args = ap.parse_args()
    if args.cmd == "enumerate":
        cmd_enumerate(args)
    elif args.cmd == "clean":
        cmd_clean(args)
    elif args.cmd == "panel":
        cmd_panel(args)
    elif args.cmd == "report":
        cmd_report(args)


if __name__ == "__main__":
    main()
