"""cli_publish.py — Stage 6: the PUBLISHER. One command, the whole publish pack.

Folds the Upload Kit (Stage 5) in and adds the Furgiven-style delivery layer:

  harvest facts -> AUTO-DRAFT copy (upload_engine) -> stamp footer -> UK-G1..G7 gates
  -> in-engine red-team -> (external 5-CLI panel) -> render per-platform PACK files
  + captions.srt (from the finished video's words.json) + a clickable, copy-button
  PUBLISH_INDEX.html -> GREEN gate (publish_check). It NEVER uploads — paste-ready.

A "media folder" is a short folder (.../shorts/NN_Title) or a long-form v1 folder.
Reads ONLY this repo's content; HF-POC's fg-publish is fully independent of it.

Usage:
  .venv\\Scripts\\python.exe cli_publish.py "<short or v1 folder>"
  .venv\\Scripts\\python.exe cli_publish.py "<v1 folder>" --all-shorts
  .venv\\Scripts\\python.exe cli_publish.py "<media>" --no-panel        # skip the external panel
  .venv\\Scripts\\python.exe cli_publish.py "<media>" --strict           # WARN -> FAIL
  .venv\\Scripts\\python.exe cli_publish.py "<media>" --index            # rebuild the index only
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pipeline import (
    publish_check,
    publish_pack,
    upload_engine,
    upload_gates,
    upload_runner,
)
from pipeline.publish_pack import LONG_PLATFORMS, PLATFORM_FILE, SHORT_PLATFORMS


def _discover_shorts(v1_folder: str) -> list[str]:
    shorts = Path(v1_folder).resolve() / "shorts"
    if not shorts.is_dir():
        return []
    return [str(p) for p in sorted(shorts.iterdir())
            if p.is_dir() and (p / "narration.creation.json").is_file()]


def _have_pack(media: str, is_long: bool) -> bool:
    pub = Path(media).resolve() / "publish"
    plats = LONG_PLATFORMS if is_long else SHORT_PLATFORMS
    return pub.is_dir() and all((pub / PLATFORM_FILE[p]).exists() for p in plats)


def _process(media: str, *, run_panel: bool, index_only: bool, redraft: bool) -> dict:
    """Draft -> gate -> red-team -> (panel) -> render pack, OR refresh an existing pack.

    A re-run over an existing pack does NOT silently re-draft (that would waste an LLM
    call and discard your panel/hand edits): it rebuilds the kit FROM the on-disk copy
    and refreshes the mechanical files (srt, _source, index). Pass --redraft to throw
    the copy away and generate + panel from scratch.
    """
    facts = upload_engine.harvest_facts(media)
    refresh_only = index_only or (_have_pack(media, facts.format == "long") and not redraft)

    if refresh_only:
        kit, _missing = publish_check._kit_from_pack(media, upload_gates.load_specs())
        pack = publish_pack.write_unit_pack(kit, force=False)
        return {"name": Path(media).name, "pack": pack, "res": None, "refreshed": True}

    raw = upload_engine.generate(facts)                       # AUTO-DRAFT (one LLM call)
    res = upload_runner.run_one(media, run_panel=run_panel, raw_override=raw)
    pack = publish_pack.write_unit_pack(res["kit"], force=redraft)
    return {"name": Path(media).name, "pack": pack, "res": res, "refreshed": False}


def main() -> int:
    ap = argparse.ArgumentParser(description="Stage 6 — the publisher (one-command publish pack)")
    ap.add_argument("media", help="a finished media folder (short or long-form v1)")
    ap.add_argument("--all-shorts", action="store_true", help="treat <media> as a v1 folder; do every short")
    ap.add_argument("--no-panel", action="store_true", help="skip the external 5-CLI panel red-team")
    ap.add_argument("--strict", action="store_true", help="promote WARN to FAIL in the gate")
    ap.add_argument("--index", action="store_true", help="refresh srt + PUBLISH_INDEX.html from the on-disk copy (no LLM, no overwrite)")
    ap.add_argument("--redraft", action="store_true", help="throw away existing copy and auto-draft + panel from scratch")
    ap.add_argument("--copy-ok", action="store_true", help="after RE-READING the copy against the current final, clear the copy-staleness stamp")
    ap.add_argument("--no-fail", action="store_true", help="exit 0 even if a gate fails")
    args = ap.parse_args()

    targets = _discover_shorts(args.media) if args.all_shorts else [args.media]
    if not targets:
        print(f"[publish] no media found under {args.media}", file=sys.stderr)
        return 2

    units: list[dict] = []
    summaries: list[dict] = []
    for t in targets:
        print(f"\n=== Publish pack: {Path(t).name} ===")
        u = _process(t, run_panel=not args.no_panel and not args.index,
                     index_only=args.index, redraft=args.redraft)
        if args.copy_ok:
            src_p = Path(t).resolve() / "publish" / "_source.json"
            src = json.loads(src_p.read_text(encoding="utf-8"))
            src["copy_final_sha"] = src.get("final_sha", "")
            src_p.write_text(json.dumps(src, indent=2, ensure_ascii=False), encoding="utf-8")
            print("  copy-ok: copy stamp cleared against the current final "
                  "(you re-read the copy, right?)")
        summaries.append(u)
        pack = u["pack"]
        if u.get("refreshed"):
            print("  refreshed from on-disk copy (no LLM, no re-draft) - pass --redraft to regenerate")
        if pack.get("srt_note"):
            print(f"  WARN  {pack['srt_note']}")
        if u["res"]:
            kit = u["res"]["kit"]
            print(f"  draft gates: {'PASS' if u['res']['gates_pass'] else 'FAIL'}  "
                  f"(red-team verdict: {kit.redteam.splitlines()[0] if kit.redteam else 'n/a'})")
            if u["res"].get("panel_dir"):
                print(f"  panel -> {u['res']['panel_dir']}")
        units.append({"title": Path(t).name,
                      "platforms": [(lbl, p) for lbl, p in pack["platforms"]],
                      "video": pack["video"]})

    # one clickable index covering everything processed
    if args.all_shorts:
        root = Path(args.media).resolve() / "publish"
        root.mkdir(exist_ok=True)
    else:
        root = Path(summaries[0]["pack"]["pub"])
    idx = publish_pack.build_index(root, units)
    print(f"\nindex: {idx}")
    print(f"open:  file:///{str(idx.resolve()).replace(chr(92), '/')}")

    # the GREEN gate, per unit
    print("\n--- GATE ---")
    all_green = True
    for t in targets:
        green = publish_check.report(t, strict=args.strict,
                                     sibling_titles=upload_runner._sibling_titles(t))
        all_green = all_green and green

    return 0 if (all_green or args.no_fail) else 1


if __name__ == "__main__":
    sys.exit(main())
