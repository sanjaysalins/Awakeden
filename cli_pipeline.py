"""One seamless pipeline: topic → narration → images → clips → final cut, with
three human quality gates (you are the gate at audio, images, and clips).

Start a NEW topic (interactive series/episode pick, runs text + audio):
    .venv\\Scripts\\python.exe cli_pipeline.py

Then resume past each gate (the previous run prints the exact command):
    .venv\\Scripts\\python.exe cli_pipeline.py "<v1 folder>" --continue            # cross one gate
    .venv\\Scripts\\python.exe cli_pipeline.py "<v1 folder>" --reroll 6,11         # re-render weak images (GATE 2)
    .venv\\Scripts\\python.exe cli_pipeline.py "<v1 folder>" --hero 7 --continue   # set hero + continue (GATE 2)
    .venv\\Scripts\\python.exe cli_pipeline.py "<v1 folder>" --exclude 3,10 --continue  # drop clips + continue (GATE 2/3)

Excluding a bad IMAGE at GATE 2 skips paying Kling to animate it (cost saver).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Force UTF-8 stdout — narration text carries em-dashes / curly quotes.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import config
from pipeline import orchestrator
# Reuse cli.py's interactive choosers — no duplication.
from cli import _choose_series, _choose_episode, _prompt


def _parse_indices(s: str) -> set[int]:
    if not s.strip():
        return set()
    try:
        return {int(x) for x in s.replace(" ", "").split(",") if x}
    except ValueError:
        raise SystemExit(f"Expected comma-separated integers, got {s!r}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="End-to-end gospel-Short pipeline with human gates at "
                    "audio / images / clips."
    )
    ap.add_argument("v1_folder", type=Path, nargs="?",
                    help="Resume an existing v1 folder. Omit to start a NEW topic interactively.")
    ap.add_argument("--continue", dest="do_continue", action="store_true",
                    help="Cross the current gate and run the next stage.")
    ap.add_argument("--reroll", default="", help="GATE 2: re-render these image indices, e.g. 6,11.")
    ap.add_argument("--exclude", default="", help="GATE 2/3: drop these scene indices from the cut, e.g. 3,10.")
    ap.add_argument("--include", default="", help="Un-exclude scene indices you previously dropped, e.g. 4.")
    ap.add_argument("--hero", type=int, default=0, help="GATE 2: set the hero (bookend) scene index.")
    ap.add_argument("--provider", choices=("hf", "nbp"), default="",
                    help="Image/clip provider (default: hf, or whatever the v1 was started with).")
    args = ap.parse_args()

    config.require_api_key()

    if args.v1_folder is None:
        # Start a new topic.
        print("=" * 64)
        print("  Salt and Light Kingdom — full pipeline (new topic)")
        print("=" * 64)
        series = _choose_series()
        episode = _choose_episode(series)
        notes = _prompt("\nOptional notes / angle (Enter to skip): ")
        provider = args.provider or "hf"
        orchestrator.start(series, episode, notes=notes, provider=provider)
        return 0

    v1 = args.v1_folder
    if not v1.exists():
        raise SystemExit(f"v1 folder does not exist: {v1}")

    orchestrator.advance(
        v1,
        do_continue=args.do_continue,
        reroll=_parse_indices(args.reroll),
        exclude_add=_parse_indices(args.exclude),
        include_remove=_parse_indices(args.include),
        hero=args.hero,
        provider=args.provider,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
