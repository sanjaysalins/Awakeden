#!/usr/bin/env python
"""Base-elements SCRIPTURE-FACT gate (Step 2.5 of the base-elements library).

Closes the authenticity gap: the ref images were only ever checked as TEXT (the
5-CLI panel) + by eye. This validates each rendered reference PNG against the
Scripture-cited FACT CARDS authored on its card — the SAME both-ways check proven
on episodes (bib_validate.py), pointed at ref_library/ instead of an episode.

Per card that carries a `facts` block in ref_library/cards/cards.json:
  1. HYDRATE every citation with verbatim KJV (pipeline/scripture.py, cached) —
     an unverified `specified` fact is downgraded to `constrained` (no pass on a
     guess).
  2. AUDIT the rendered PNG against its SPECIFIED + CONSTRAINED facts via
     pipeline.bible_kb.verify_biblical_accuracy (Claude-Vision through the
     agent-bridge — NO metered API). Fail-closed: a specified violation = FAIL.
  3. Write a <NAME>.bib_audit.json sidecar + ref_library/_factcheck/index.html.

Exit non-zero if ANY ref FAILs or is SKIPPED, so the gate can't silently pass.

Run (service the agent-bridge vision requests from chat):
  .venv\\Scripts\\python.exe longform\\_base_elements_factcheck.py
  .venv\\Scripts\\python.exe longform\\_base_elements_factcheck.py --names NOAHS_ARK,ARK_DOOR
  .venv\\Scripts\\python.exe longform\\_base_elements_factcheck.py --facts-only   # hydrate + report, no image audit
"""
from __future__ import annotations
import argparse, html, json, sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))      # run from longform/ — put repo root on the path

import config  # noqa: F401  (loads .env; LLM_PROVIDER=agent keeps the dead API unused)
from pipeline import bible_kb
LIB = ROOT / "ref_library"
CARDS = LIB / "cards" / "cards.json"
AUD = LIB / "_factcheck"
SUBDIR = {"character": "characters", "object": "objects", "place": "places", "motif": "motifs"}


def png_for(card) -> Path:
    return LIB / SUBDIR[card["kind"]] / f"{card['name']}.png"


def write_html(rows: list[dict], out: Path) -> None:
    def esc(x): return html.escape(str(x))
    cells = []
    for r in rows:
        png = r["png"]
        img = (f"<img src='file:///{esc(png.replace(chr(92), '/'))}'>" if png else "<div class=noimg>no PNG</div>")
        v = r["verdict"]
        cls = {"PASS": "pass", "FAIL": "fail", "SKIP": "skip", "FACTS": "skip"}.get(v, "skip")
        viol = ""
        if r.get("specified_violations") or r.get("constrained_violations"):
            sv = "".join(f"<li class=sv><b>SPECIFIED:</b> {esc(x['claim'])} → <i>{esc(x['actual'])}</i></li>"
                         for x in r.get("specified_violations", []))
            cv = "".join(f"<li class=cv><b>CONSTRAINED:</b> {esc(x['claim'])} → <i>{esc(x['actual'])}</i></li>"
                         for x in r.get("constrained_violations", []))
            viol = f"<ul class=viol>{sv}{cv}</ul>"
        facts = "".join(
            f"<div class='fact {f['bucket']}'><b>{f['bucket'].upper()}</b> {esc(f['claim'])}"
            f"<div class=ref>{esc(', '.join(f['scripture']))} {'✓' if f['verified'] else '✗'}</div>"
            f"{('<div class=kjv>'+esc(f['kjv_text'])+'</div>') if f['kjv_text'] else ''}</div>"
            for f in r["facts"])
        cells.append(
            f"<div class=card><div class=col-img>{img}<div class=cap>{esc(r['name'])} "
            f"<span class='verdict {cls}'>{v}</span></div><div class=note>{esc(r.get('notes',''))}</div>{viol}</div>"
            f"<div class=col-facts>{facts or '<i>(no facts)</i>'}</div></div>")
    css = """
    body{font-family:system-ui,Segoe UI,sans-serif;margin:0;background:#14110d;color:#eee}
    header{padding:16px 22px;background:#1d1810;border-bottom:1px solid #3a2f1f}
    h1{margin:0;font-size:19px} .sub{color:#b9a;font-size:13px;margin-top:4px}
    .card{display:flex;gap:16px;padding:16px 22px;border-bottom:1px solid #2a2218}
    .col-img{flex:0 0 300px} .col-facts{flex:1}
    img{width:300px;border-radius:6px;display:block;background:#000}
    .noimg{width:300px;height:200px;background:#222;display:flex;align-items:center;justify-content:center;color:#777;border-radius:6px}
    .cap{font-size:14px;color:#cfc6b8;margin:6px 0}
    .verdict{display:inline-block;padding:2px 8px;border-radius:5px;font-size:12px;font-weight:700}
    .pass{background:#16361b;color:#9be8a6} .fail{background:#3d1414;color:#ff9c9c} .skip{background:#3a3110;color:#e8d59b}
    .fact{margin:0 0 9px;padding:7px 9px;border-radius:6px;background:#1f1a12;border-left:3px solid #555}
    .fact.specified{border-color:#d9a441} .fact.constrained{border-color:#5a86c4} .fact.free{border-color:#666}
    .ref{font-size:12px;color:#8fb0d8;margin-top:3px} .kjv{font-size:12px;color:#cdbf9c;font-style:italic;margin-top:3px}
    .viol{margin:8px 0;padding-left:18px} .sv{color:#ff9c9c} .cv{color:#ffd28a} .note{font-size:12px;color:#aaa;margin-top:4px}
    """
    doc = (f"<!doctype html><meta charset=utf-8><title>Ref fact-check</title><style>{css}</style>"
           f"<header><h1>Base-elements — Scripture-fact gate</h1>"
           f"<div class=sub>specified = Bible states it (image MUST match) · constrained = must not contradict</div></header>"
           f"{''.join(cells)}")
    out.write_text(doc, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--names", default="", help="comma list of card names (default: every card with facts)")
    ap.add_argument("--facts-only", action="store_true", help="hydrate + report citations, skip image audit")
    args = ap.parse_args()
    only = set(n.strip() for n in args.names.split(",") if n.strip())

    cards = json.load(open(CARDS, encoding="utf-8"))
    todo = [c for c in cards if c.get("facts") and (not only or c["name"] in only)]
    AUD.mkdir(parents=True, exist_ok=True)
    print(f"cards with facts: {sum(1 for c in cards if c.get('facts'))}  to-check: {len(todo)}")

    rows, fails, skips = [], [], []
    for c in todo:
        facts = [bible_kb.FactCard.from_json(f) for f in c["facts"]]
        bible_kb.hydrate_citations(facts)
        png = png_for(c)
        row = {"name": c["name"], "kind": c["kind"], "png": str(png) if png.exists() else "",
               "facts": [asdict(f) for f in facts], "notes": ""}
        n_unver = sum(1 for f in facts if f.scripture and not f.verified)
        if args.facts_only:
            row["verdict"] = "FACTS"; row["notes"] = f"{n_unver} unverified citation(s)"
        elif not png.exists():
            row["verdict"] = "SKIP"; row["notes"] = "no rendered PNG"; skips.append(c["name"])
        else:
            print(f"  auditing {c['name']} ...", flush=True)
            a = bible_kb.verify_biblical_accuracy(c["name"], c["canonical"], facts, [], png.read_bytes())
            row["specified_violations"] = a.specified_violations
            row["constrained_violations"] = a.constrained_violations
            row["notes"] = a.notes
            if a.skipped:
                row["verdict"] = "SKIP"; skips.append(c["name"])
            elif a.passed:
                row["verdict"] = "PASS"
            else:
                row["verdict"] = "FAIL"; fails.append(c["name"])
            rec = asdict(a); rec["image_sha256"] = bible_kb.sha_bytes(png.read_bytes())
            png.with_suffix(".bib_audit.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"    [{row['verdict']}] {a.notes[:90]}", flush=True)
        rows.append(row)

    out = AUD / "index.html"
    write_html(rows, out)
    link = "file:///" + str(out).replace("\\", "/")
    print(f"\n[factcheck] {len(rows)} checked · {len(fails)} FAIL · {len(skips)} SKIP")
    if fails: print("  FAIL:", ", ".join(fails))
    if skips: print("  SKIP:", ", ".join(skips))
    print(f"[factcheck] REVIEW -> {link}")
    return 3 if (fails or skips) else 0


if __name__ == "__main__":
    sys.exit(main())
