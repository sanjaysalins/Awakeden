#!/usr/bin/env python
"""cli_livingpage.py — ONE resumable entry point for a living-page batch piece (P2-4).

Detects the piece's position purely from artifacts on disk (idempotent — nothing is
trusted from a state file), prints a status board with the EXACT next command, and
with --continue runs the next step itself when it is $0. PAID steps (BytePlus stills,
Kling animation) and HUMAN gates (stills approval) are never auto-run — the exact
command is printed and the machine stops, per INV-20 (ask before spending) and the
stills-first human gate.

  .venv\\Scripts\\python.exe cli_livingpage.py "<piece dir>"              # status board
  .venv\\Scripts\\python.exe cli_livingpage.py "<piece dir>" --continue   # run next $0 step
  .venv\\Scripts\\python.exe cli_livingpage.py "<piece dir>" --json       # machine-readable

Stages (in order):
  narration -> voice -> spec -> manifest -> stills -> stills-gate -> animate
  -> build -> score -> sfx -> register
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
BUILDER = ROOT / "longform" / "02_Psalm_22_Song_From_The_Cross" / "build_livingpage_16x9.py"


@dataclass
class Step:
    name: str
    done: bool
    detail: str
    next_cmd: str = ""          # exact command to run when not done
    auto: bool = False          # safe for --continue to run itself ($0, no human gate)


def _mtime(p: Path) -> float:
    return p.stat().st_mtime if p.exists() else 0.0


def _sfx_builder(slug: str) -> Path | None:
    """The sfx_pilots build script carrying this piece's layer map ($0, reuse-only
    from sound_library). Cluster-1 pieces live in build_cluster1_sfx.py's PIECES dict;
    later clusters get bespoke build_<piece>_sfx.py scripts."""
    for p in sorted((ROOT / "sfx_pilots").glob("build_*.py")):
        try:
            if slug in p.read_text(encoding="utf-8"):
                return p
        except OSError:
            continue
    return None


def detect(piece: Path) -> list[Step]:
    steps: list[Step] = []
    q = f'"{piece}"'

    # 1. narration
    nar = piece / "narration.md"
    steps.append(Step("narration", nar.is_file(),
                      "narration.md present" if nar.is_file() else "no narration.md",
                      "write the narration (/narrate or /witness), then place narration.md here"))

    # 2. voice
    mp3 = piece / "audio" / "narration.mp3"
    align = piece / "audio" / "alignment.json"
    steps.append(Step("voice", mp3.is_file() and align.is_file(),
                      "narration.mp3 + alignment.json" if mp3.is_file() and align.is_file()
                      else "audio/narration.mp3 or alignment.json missing",
                      "/voice (PythonProject1 per_turn_synth) then align — HUMAN GATE 1: approve by ear"))

    # 3. beats spec
    spec = piece / "visual" / "livingpage_short.spec.json"
    steps.append(Step("spec", spec.is_file(),
                      spec.name if spec.is_file() else "no livingpage_short.spec.json",
                      "author the beats spec (livingpage skill choreography)"))

    # 4. manifest
    pj_path = piece / "piece.json"
    pj = json.loads(pj_path.read_text(encoding="utf-8")) if pj_path.is_file() else None
    steps.append(Step("manifest", pj is not None,
                      f"piece.json ({len(pj['stills']['jobs'])} stills)" if pj else "no piece.json",
                      "author piece.json (stills prompts / moves / score / register)"))
    if pj is None:
        return steps

    # 5. stills rendered
    jobs = pj["stills"]["jobs"]
    missing = [s for s in jobs if not (piece / "visual" / f"{s}.png").exists()]
    steps.append(Step("stills", not missing,
                      f"{len(jobs)} stills on disk" if not missing else
                      f"{len(missing)} missing: {missing[:4]}{'...' if len(missing) > 4 else ''}",
                      f"{PY} run_piece.py {q} --stage stills --render   [PAID ~${len(missing) * 0.05:.2f}]"))

    # 6. stills gate (fail-closed sidecars + hash-bound human approval)
    from render_lint.verify import gate_dir
    g = gate_dir(piece / "visual")
    blocked = (g.get("failed") or []) + (g.get("unaudited") or [])
    sg = subprocess.run([PY, str(ROOT / "stills_gate.py"), str(piece), "--check"],
                        capture_output=True, text=True)
    gate_ok = not blocked and sg.returncode == 0
    detail = ("sidecars PASS + human gate GREEN" if gate_ok else
              (f"{len(blocked)} still(s) blocked: {blocked[:3]}" if blocked
               else f"stills_gate --check: {(sg.stdout or sg.stderr).strip().splitlines()[-1][:80] if (sg.stdout or sg.stderr).strip() else 'not GREEN'}"))
    steps.append(Step("stills-gate", gate_ok, detail,
                      f"{PY} stills_gate.py {q} --build   [HUMAN GATE 2: rubric + approve]"))

    # 7. animate (hash-fresh clips for every move)
    import run_piece as RP
    an = pj.get("animate")
    if an:
        pending = []
        for slug, prompt in RP.animate_prompts(pj).items():
            still = piece / "visual" / f"{slug}.png"
            out = piece / "visual" / "clips" / f"{slug}.mp4"
            if RP._clip_state(still, out, prompt, an) in ("missing", "stale"):
                pending.append(slug)
        steps.append(Step("animate", not pending,
                          f"{len(an['moves'])} clips hash-fresh" if not pending else
                          f"{len(pending)} to render: {pending[:4]}",
                          f"{PY} run_piece.py {q} --stage animate   [PAID ~${len(pending) * 0.65:.2f} Kling]"))
    else:
        steps.append(Step("animate", True, "(no animate section — clips come from elsewhere)"))

    # 8. build (preview newer than spec + clips + stills, AND provenance: a manual
    # no---clips rebuild writes the same preview filename with all-dyncam pixels —
    # the report's clips_build stamp is the only way to tell (red-team 2026-07-19).
    # Reports predating the stamp have no key = legacy pass; explicit false blocks.
    preview = piece / "visual" / "livingpage_short.spec_preview.mp4"
    newest_src = max([_mtime(spec)] +
                     [_mtime(p) for p in (piece / "visual").glob("*.png")] +
                     [_mtime(c) for c in (piece / "visual" / "clips").glob("*.mp4")] or [0])
    report_p = piece / "visual" / "livingpage_short.spec_report.json"
    no_clips_build = False
    if report_p.is_file():
        try:
            no_clips_build = json.loads(report_p.read_text(encoding="utf-8")).get(
                "clips_build") is False
        except (json.JSONDecodeError, OSError):
            pass
    build_ok = preview.exists() and _mtime(preview) >= newest_src and not no_clips_build
    steps.append(Step("build", build_ok,
                      "preview newer than every source" if build_ok else
                      ("preview built WITHOUT --clips (all-dyncam) — rebuild with --clips"
                       if no_clips_build else
                       ("preview STALE (a source changed)" if preview.exists() else "no preview built")),
                      f'{PY} "{BUILDER}" --pool "{piece / "visual"}" --spec livingpage_short.spec.json '
                      f"--clips --page 1080x1920 --no-ticks", auto=True))

    # 9. score (scored mp4 newer than preview + manifest; retime staleness)
    scored = piece / Path(pj["score"]["out"]) if pj.get("score") else None
    score_ok = bool(scored and scored.exists() and _mtime(scored) >= _mtime(preview)
                    and _mtime(scored) >= _mtime(pj_path))
    warn = ""
    if align.is_file() and _mtime(align) > _mtime(pj_path):
        score_ok, warn = False, " (alignment NEWER than piece.json — run --stage retime first)"
    steps.append(Step("score", score_ok,
                      (scored.name if score_ok else f"scored output stale/missing{warn}"),
                      f"{PY} run_piece.py {q} --stage retime && --stage score" if warn else
                      f"{PY} run_piece.py {q} --stage score", auto=not warn))

    # 10. sfx bed — the living-page FINAL is <out>_sfx.mp4 (caption policy: the comic
    # boxes ARE the captions), built $0 from sound_library by the piece's layer map
    if scored is not None:
        sfx_out = scored.with_name(scored.name.replace("_scored", "_sfx"))
        builder = _sfx_builder(piece.name)
        sfx_ok = sfx_out.exists() and _mtime(sfx_out) >= _mtime(scored)
        if builder is not None:
            flt = f" {piece.name}" if builder.name == "build_cluster1_sfx.py" else ""
            cmd = f'{PY} "{builder}"{flt}'
        else:
            cmd = "author the sfx layer map in sfx_pilots/ (see build_cluster1_sfx.py)"
        steps.append(Step("sfx", sfx_ok,
                          sfx_out.name if sfx_ok else
                          (f"{sfx_out.name} STALE (scored cut is newer)" if sfx_out.exists()
                           else f"no {sfx_out.name}"),
                          cmd, auto=builder is not None))

    # 11. register (asset index rows exist for this piece)
    try:
        idx = json.loads((ROOT / "asset_index.json").read_text(encoding="utf-8"))
        entries = idx.get("assets", idx if isinstance(idx, list) else [])
        n_rows = sum(1 for a in entries if isinstance(a, dict) and a.get("piece") == pj["piece"])
    except Exception:
        n_rows = 0
    steps.append(Step("register", n_rows > 0,
                      f"{n_rows} asset rows indexed" if n_rows else "no asset_index rows",
                      f"{PY} run_piece.py {q} --stage register", auto=True))
    return steps


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="resumable living-page piece runner")
    ap.add_argument("piece")
    ap.add_argument("--continue", dest="advance", action="store_true",
                    help="run the next step if it is $0/no-human-gate; else print it")
    ap.add_argument("--json", action="store_true", help="machine-readable status")
    a = ap.parse_args(argv)
    piece = Path(a.piece).resolve()
    if not piece.is_dir():
        print(f"not a folder: {piece}", file=sys.stderr)
        return 2
    steps = detect(piece)
    if a.json:
        print(json.dumps([s.__dict__ for s in steps], indent=2, ensure_ascii=False))
        return 0

    print(f"\n== {piece.name} — living-page position ==")
    nxt = None
    for s in steps:
        mark = "DONE" if s.done else ("NEXT" if nxt is None else "    ")
        if not s.done and nxt is None:
            nxt = s
        print(f"  [{mark}] {s.name:12} {s.detail}")
    if nxt is None:
        print("\n  COMPLETE — every stage is current. (website refresh: "
              f"{PY} _website\\build_readpage.py --force)")
        return 0
    print(f"\n  NEXT -> {nxt.name}: {nxt.next_cmd}")
    if a.advance:
        if not nxt.auto:
            print("  (paid or human-gated — not auto-running; execute the command above.)")
            return 3
        print(f"  --continue: running it...")
        r = subprocess.run(nxt.next_cmd, shell=True)
        return r.returncode
    return 1 if nxt else 0


if __name__ == "__main__":
    sys.exit(main())
