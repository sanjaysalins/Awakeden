r"""bib_validate.py — Biblical-Universe accuracy pipeline (drive + check stills).

Runs the bible_kb stage on one episode and proves it works:

  1. DERIVE  per-scene biblical FACT CARDS from the narration + scene plan
             (LLM via agent-bridge), pull from bible_kb/, then HYDRATE every
             citation with verbatim KJV (scripture.py) — fail-closed on guesses.
  2. PANEL   write a clean fact_sheet.md and fan it to the 5-CLI independent
             panel (independent_review.py --type biblical-facts): are the FACTS
             sound + correctly cited? (the "proven independently" half)
  3. AUDIT   Claude-Vision audit each rendered still against its SPECIFIED +
             CONSTRAINED facts (image-vs-facts), fail-closed on a specified
             violation. (the "the picture obeys" half)
  4. REPORT  write _bible_check/index.html — facts, panel verdicts, image
             verdicts, violations with citations.

Both ways enforced (the locked non-negotiable): the facts AND the picture.

Usage (PowerShell):
  .venv\Scripts\python.exe bib_validate.py "<v1 folder>"
  .venv\Scripts\python.exe bib_validate.py "<v1 folder>" --scenes 1,2,3,7,9
  .venv\Scripts\python.exe bib_validate.py "<v1 folder>" --facts-only      # derive+panel, no image audit
  .venv\Scripts\python.exe bib_validate.py "<v1 folder>" --audit-only      # reuse scene_facts.json, just audit PNGs
  .venv\Scripts\python.exe bib_validate.py "<v1 folder>" --no-panel
"""
from __future__ import annotations

import argparse
import html
import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

import config
from pipeline import bible_kb


# ---------------------------------------------------------------------------
# Locate the episode's artifacts (tolerant of long-form + short layouts)
# ---------------------------------------------------------------------------
def locate(vfolder: Path) -> dict:
    narration = None
    for cand in (vfolder / "narration.md", vfolder / "narration.spoken.txt"):
        if cand.exists():
            narration = cand
            break
    scene_plan = None
    for cand in (
        vfolder / "visual_16x9" / "scene_plan.json",
        vfolder / "visual" / "scene_plan.json",
        vfolder / "scene_plan.json",
        # living-page batch pieces (cluster shorts) — beats spec instead of scene plan
        vfolder / "visual" / "livingpage_short.spec.json",
        vfolder / "visual" / "mocomic_v2.spec.json",
    ):
        if cand.exists():
            scene_plan = cand
            break
    images_dir = scene_plan.parent if scene_plan else vfolder
    return {"narration": narration, "scene_plan": scene_plan, "images_dir": images_dir}


def find_png(images_dir: Path, sid: int, title: str = "") -> Path | None:
    hits = sorted(images_dir.glob(f"{sid:02d}_*.png"))
    if hits:
        return hits[0]
    # living-page batch stills are named by slug (the scene title), not NN_ prefixed
    if title and (images_dir / f"{title}.png").exists():
        return images_dir / f"{title}.png"
    return None


def _write_facts(facts_path: Path, ep, scene_plan) -> None:
    """Persist scene_facts.json BOUND to the scene_plan it was built from (sha256),
    so the chokepoint can detect a stale fact sheet by content, not mtime."""
    d = ep.to_json()
    d["scene_plan_sha256"] = (
        bible_kb.sha_file(scene_plan) if scene_plan and Path(scene_plan).exists() else "")
    facts_path.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------------------
# Fact-sheet markdown (CLEAN artifact for the panel — no status / priming)
# ---------------------------------------------------------------------------
def fact_sheet_md(ep: bible_kb.EpisodeFacts) -> str:
    def render(f: bible_kb.FactCard) -> str:
        lines = [f"- **[{f.bucket.upper()}]** {f.claim}"]
        if f.scripture:
            lines.append(f"  - Scripture: {', '.join(f.scripture)}")
        if f.kjv_text:
            for ln in f.kjv_text.splitlines():
                lines.append(f"  - KJV: {ln}")
        elif f.scripture:
            lines.append("  - KJV: *(citation could NOT be verified)*")
        if f.historical_note:
            lines.append(f"  - Historical (secondary): {f.historical_note}")
        if f.visual_directive:
            lines.append(f"  - Visual: {f.visual_directive}")
        if f.banned_anachronisms:
            lines.append(f"  - Must NOT show: {'; '.join(f.banned_anachronisms)}")
        return "\n".join(lines)

    out = [f"# Biblical fact sheet — {ep.episode}", ""]
    out.append(f"Source narration: {Path(ep.source_narration).name}")
    out.append(f"Source scene plan: {Path(ep.source_scene_plan).name}")
    out.append("")
    out.append("Buckets: **specified** = the Bible states this visual fact (image MUST match) · "
               "**constrained** = the image must not contradict it · **free** = artistic licence.")
    out.append("")
    if ep.world_facts:
        out.append("## World facts (apply to every scene)")
        out += [render(f) for f in ep.world_facts]
        out.append("")
    for s in ep.scenes:
        out.append(f"## Scene {s.sid} — {s.title}")
        out.append(f"*Depicts:* {s.subject_block}")
        out.append("")
        out += [render(f) for f in s.facts] if s.facts else ["- (no facts derived)"]
        out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# HTML report
# ---------------------------------------------------------------------------
def write_html(ep: bible_kb.EpisodeFacts, audits: dict[int, bible_kb.BiblicalAudit],
               images_dir: Path, panel_dir: Path | None, out_html: Path) -> None:
    def esc(x): return html.escape(str(x))

    def fact_html(f: bible_kb.FactCard) -> str:
        cls = {"specified": "spec", "constrained": "con", "free": "free"}.get(f.bucket, "con")
        ver = "✓" if f.verified else "✗"
        kjv = f"<div class=kjv>{esc(f.kjv_text)}</div>" if f.kjv_text else (
            "<div class=kjv bad>citation NOT verified</div>" if f.scripture else "")
        vis = f"<div class=vis>🎨 {esc(f.visual_directive)}</div>" if f.visual_directive else ""
        ban = f"<div class=ban>🚫 {esc('; '.join(f.banned_anachronisms))}</div>" if f.banned_anachronisms else ""
        return (f"<div class='fact {cls}'><span class=b>{f.bucket}</span> "
                f"<span class=v title='citations verified'>{ver}</span> {esc(f.claim)}"
                f"<div class=ref>{esc(', '.join(f.scripture))}</div>{kjv}{vis}{ban}</div>")

    rows = []
    for s in ep.scenes:
        png = find_png(images_dir, s.sid, s.title)
        img = f"<img src='file:///{esc(str(png).replace(chr(92), '/'))}'>" if png else "<div class=noimg>no PNG</div>"
        a = audits.get(s.sid)
        if a is None:
            verdict = "<span class='verdict skip'>not audited</span>"
            viol = ""
        elif a.skipped:
            verdict = "<span class='verdict skip'>SKIPPED — review by eye</span>"
            viol = f"<div class=note>{esc(a.notes)}</div>"
        elif a.passed:
            verdict = "<span class='verdict pass'>PASS — biblically faithful</span>"
            viol = f"<div class=note>{esc(a.notes)}</div>"
        else:
            verdict = "<span class='verdict fail'>FAIL — contradicts Scripture</span>"
            sv = "".join(f"<li class=sv><b>SPECIFIED:</b> {esc(v['claim'])} -> <i>{esc(v['actual'])}</i></li>"
                         for v in a.specified_violations)
            cv = "".join(f"<li class=cv><b>CONSTRAINED:</b> {esc(v['claim'])} -> <i>{esc(v['actual'])}</i></li>"
                         for v in a.constrained_violations)
            viol = f"<ul class=viol>{sv}{cv}</ul><div class=note>{esc(a.notes)}</div>"
        facts = "".join(fact_html(f) for f in s.facts) or "<i>(no facts)</i>"
        rows.append(
            f"<div class=scene><div class=col-img>{img}<div class=cap>#{s.sid} {esc(s.title)}</div>{verdict}{viol}</div>"
            f"<div class=col-facts>{facts}</div></div>")

    world = "".join(fact_html(f) for f in ep.world_facts)
    panel_link = (f"<p>Independent fact panel -> <a href='file:///{esc(str(panel_dir).replace(chr(92),'/'))}/INDEX.md'>"
                  f"{esc(str(panel_dir))}\\INDEX.md</a></p>" if panel_dir else "")
    css = """
    body{font-family:system-ui,Segoe UI,sans-serif;margin:0;background:#14110d;color:#eee}
    header{padding:18px 24px;background:#1d1810;border-bottom:1px solid #3a2f1f}
    h1{margin:0 0 4px;font-size:20px} .sub{color:#b9a;font-size:13px}
    .world{padding:14px 24px;background:#1a160f;border-bottom:1px solid #2a2218}
    .scene{display:flex;gap:18px;padding:18px 24px;border-bottom:1px solid #2a2218}
    .col-img{flex:0 0 360px} .col-facts{flex:1}
    img{width:360px;border-radius:6px;display:block} .noimg{width:360px;height:200px;background:#222;display:flex;align-items:center;justify-content:center;color:#777;border-radius:6px}
    .cap{font-size:13px;color:#cfc6b8;margin:6px 0}
    .verdict{display:inline-block;padding:3px 9px;border-radius:5px;font-size:12px;font-weight:600}
    .pass{background:#16361b;color:#9be8a6} .fail{background:#3d1414;color:#ff9c9c} .skip{background:#3a3110;color:#e8d59b}
    .fact{margin:0 0 10px;padding:8px 10px;border-radius:6px;background:#1f1a12;border-left:3px solid #555}
    .fact.spec{border-color:#d9a441} .fact.con{border-color:#5a86c4} .fact.free{border-color:#666}
    .b{font-size:10px;text-transform:uppercase;letter-spacing:.5px;color:#caa;margin-right:6px}
    .v{color:#9be8a6;font-weight:700;margin-right:4px}
    .ref{font-size:12px;color:#8fb0d8;margin-top:3px} .kjv{font-size:12px;color:#cdbf9c;font-style:italic;margin-top:3px;white-space:pre-wrap} .kjv.bad{color:#ff9c9c}
    .vis{font-size:12px;color:#bfe0bf;margin-top:3px} .ban{font-size:12px;color:#e0a0a0;margin-top:3px}
    .viol{margin:8px 0;padding-left:18px} .sv{color:#ff9c9c} .cv{color:#ffd28a} .note{font-size:12px;color:#aaa;margin-top:4px}
    """
    doc = (f"<!doctype html><meta charset=utf-8><title>Bible check — {esc(ep.episode)}</title>"
           f"<style>{css}</style>"
           f"<header><h1>Biblical-accuracy check — {esc(ep.episode)}</h1>"
           f"<div class=sub>specified = Bible states it (must match) · constrained = must not contradict · free = licence</div>"
           f"{panel_link}</header>"
           f"<div class=world><b>World facts</b>{world}</div>"
           f"{''.join(rows)}")
    out_html.write_text(doc, encoding="utf-8")


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("vfolder", help="path to the episode v1 folder")
    ap.add_argument("--scenes", default="", help="comma list of scene ids to limit to")
    ap.add_argument("--facts-only", action="store_true", help="derive + panel only, skip image audit")
    ap.add_argument("--audit-only", action="store_true", help="reuse scene_facts.json, just audit PNGs")
    ap.add_argument("--no-derive", action="store_true",
                    help="reuse (hand-corrected) scene_facts.json: re-hydrate citations + re-panel, "
                         "skip LLM derivation. For the correction loop.")
    ap.add_argument("--no-panel", action="store_true", help="skip the 5-CLI fact panel")
    ap.add_argument("--providers", default="cursor,claude,gemini,codex,grok")
    args = ap.parse_args()

    vfolder = Path(args.vfolder).resolve()
    if not vfolder.is_dir():
        print(f"not a folder: {vfolder}", file=sys.stderr)
        return 2
    loc = locate(vfolder)
    if not loc["scene_plan"]:
        print(f"no scene_plan.json found under {vfolder}", file=sys.stderr)
        return 2
    episode = vfolder.parent.name if vfolder.name.startswith("v") else vfolder.name
    out_dir = vfolder / "_bible_check"
    out_dir.mkdir(parents=True, exist_ok=True)
    facts_path = out_dir / "scene_facts.json"
    scene_ids = [int(x) for x in args.scenes.split(",") if x.strip()] or None

    # 1. DERIVE + HYDRATE (or reuse) ----------------------------------------
    if (args.audit_only or args.no_derive) and facts_path.exists():
        ep = bible_kb.EpisodeFacts.from_json(json.loads(facts_path.read_text(encoding="utf-8")))
        if args.no_derive:
            # re-hydrate every fact so hand-added/edited citations get verbatim KJV + verified flags
            bible_kb.hydrate_citations(ep.world_facts)
            for s in ep.scenes:
                bible_kb.hydrate_citations(s.facts)
            _write_facts(facts_path, ep, loc["scene_plan"])
            n_unver = sum(1 for f in ep.world_facts + [x for s in ep.scenes for x in s.facts]
                          if f.scripture and not f.verified)
            print(f"[bible] re-hydrated hand-corrected facts ({n_unver} unverified citations) -> {facts_path}")
        else:
            print(f"[bible] reusing {facts_path}")
    else:
        if not loc["narration"]:
            print(f"no narration found under {vfolder}", file=sys.stderr)
            return 2
        print(f"[bible] deriving facts: {episode}  ({len(scene_ids) if scene_ids else 'all'} scenes)")
        ep = bible_kb.build_episode_facts(
            episode, loc["narration"], loc["scene_plan"], scene_ids=scene_ids)
        _write_facts(facts_path, ep, loc["scene_plan"])
        n_facts = len(ep.world_facts) + sum(len(s.facts) for s in ep.scenes)
        n_spec = sum(1 for f in ep.world_facts + [x for s in ep.scenes for x in s.facts] if f.bucket == "specified")
        n_unver = sum(1 for f in ep.world_facts + [x for s in ep.scenes for x in s.facts]
                      if f.scripture and not f.verified)
        print(f"[bible] {n_facts} facts ({n_spec} specified) · {n_unver} unverified citations -> {facts_path}")

    # fact sheet (clean artifact)
    sheet = out_dir / "fact_sheet.md"
    sheet.write_text(fact_sheet_md(ep), encoding="utf-8")
    print(f"[bible] fact sheet -> {sheet}")

    # 2. PANEL (facts sound?) -----------------------------------------------
    panel_dir = None
    if not args.no_panel and not args.audit_only:
        print("[bible] fanning fact sheet to the independent panel ...")
        try:
            subprocess.run(
                [sys.executable, str(Path(__file__).parent / "independent_review.py"),
                 str(sheet), "--type", "biblical-facts", "--providers", args.providers],
                check=False)
            irs = sorted((sheet.parent / "_independent_review").glob("*"))
            panel_dir = irs[-1] if irs else None
        except Exception as e:
            print(f"[bible] panel error (continuing): {e}")

    # 3. AUDIT (picture obeys?) ---------------------------------------------
    audits: dict[int, bible_kb.BiblicalAudit] = {}
    if not args.facts_only:
        for s in ep.scenes:
            png = find_png(loc["images_dir"], s.sid, s.title)
            if not png:
                print(f"  scene {s.sid}: no PNG — skipped")
                continue
            print(f"  scene {s.sid}: auditing {png.name} ...")
            pb = png.read_bytes()
            a = bible_kb.verify_biblical_accuracy(
                s.title, s.subject_block, s.facts, ep.world_facts, pb)
            audits[s.sid] = a
            rec = asdict(a)
            # BIND the audit to the exact PNG bytes + facts it ran against (anti-stale/anti-tamper)
            rec["image_sha256"] = bible_kb.sha_bytes(pb)
            rec["facts_sha256"] = bible_kb.scene_facts_sha(s)
            (png.with_suffix(".bib_audit.json")).write_text(
                json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
            tag = "SKIP" if a.skipped else ("PASS" if a.passed else "FAIL")
            print(f"           [{tag}] {a.notes[:80]}")

    # 4. REPORT --------------------------------------------------------------
    out_html = out_dir / "index.html"
    write_html(ep, audits, loc["images_dir"], panel_dir, out_html)
    fails = [sid for sid, a in audits.items() if not a.passed and not a.skipped]
    skipped = [sid for sid, a in audits.items() if a.skipped]
    print(f"\n[bible] DONE - {len(audits)} audited, {len(fails)} FAIL biblical accuracy: {fails or '-'}")
    link = "file:///" + str(out_html).replace("\\", "/")
    print(f"[bible] REVIEW -> {link}")
    # Fail-closed at the shell level: a FAILED or SKIPPED audit must not exit 0,
    # or automation/agent flows silently treat a failing run as success.
    if fails or skipped:
        print(f"[bible] NON-ZERO EXIT — {len(fails)} failed, {len(skipped)} skipped audit(s).")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
