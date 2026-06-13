"""cli_upload.py — Stage 5: generate verified, panel-reviewed upload metadata
(title / description / tags / hashtags) for a finished video, ready to paste into
YouTube, TikTok, Facebook and Instagram.

Usage:
  .venv\\Scripts\\python.exe cli_upload.py "<media folder>"                # one media
  .venv\\Scripts\\python.exe cli_upload.py "<media folder>" --panel        # + external CLI panel
  .venv\\Scripts\\python.exe cli_upload.py "<series v1 folder>" --all-shorts  # every short in the series
  .venv\\Scripts\\python.exe cli_upload.py "<media folder>" --no-redteam-fail # don't exit nonzero on gate fail

A "media folder" is a short folder (.../shorts/NN_Title) or a long-form v1 folder.
Output: <media>/upload/upload_kit.json + upload_kit.md
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pipeline import upload_runner


def _discover_shorts(v1_folder: str) -> list[str]:
    shorts = Path(v1_folder).resolve() / "shorts"
    if not shorts.is_dir():
        return []
    return [str(p) for p in sorted(shorts.iterdir())
            if p.is_dir() and (p / "narration.creation.json").is_file()]


def main() -> int:
    ap = argparse.ArgumentParser(description="Stage 5 — verified upload metadata kit")
    ap.add_argument("media", help="a finished media folder (short or long-form v1)")
    ap.add_argument("--panel", action="store_true", help="also run the external CLI panel per media")
    ap.add_argument("--all-shorts", action="store_true", help="treat <media> as a v1 folder; run every short")
    ap.add_argument("--no-fail", action="store_true", help="exit 0 even if a gate fails")
    args = ap.parse_args()

    targets = _discover_shorts(args.media) if args.all_shorts else [args.media]
    if not targets:
        print(f"[upload] no media found under {args.media}", file=sys.stderr)
        return 2

    any_fail = False
    for t in targets:
        print(f"\n=== Upload kit: {Path(t).name} ===")
        res = upload_runner.run_one(t, run_panel=args.panel)
        kit = res["kit"]
        print(f"  status: {kit.status}  gates: {'PASS' if res['gates_pass'] else 'FAIL'}")
        for g in kit.gates:
            print(f"    {'OK ' if g.passed else 'XX '} {g.gate} {g.name}: {g.detail}")
        print(f"  -> {res['paths']['md']}")
        if res.get("panel_dir"):
            print(f"  -> panel: {res['panel_dir']}")
        any_fail = any_fail or not res["gates_pass"]

    return 1 if (any_fail and not args.no_fail) else 0


if __name__ == "__main__":
    raise SystemExit(main())
