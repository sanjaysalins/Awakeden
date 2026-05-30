"""Interactive CLI: craft one 60-second gospel short at a time.

    python cli.py                 # interactive
    python cli.py --no-audio      # write the folder but skip the audio pipeline

Pick a series, pick an episode (or enter a custom topic), add optional notes,
and the engine generates -> red-team reviews -> revises -> writes the narration
folder -> runs the audio pipeline.
"""
from __future__ import annotations

import argparse
import sys

# Windows consoles default to cp1252; force UTF-8 so em dashes / symbols don't crash.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import config
from pipeline import agent_bridge, runner
from pipeline.series import Episode, Series, load_series

agent_bridge.print_startup_banner()


def _prompt(msg: str) -> str:
    try:
        return input(msg).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")
        raise SystemExit(0)


def _choose_series() -> Series:
    series = load_series()
    print("\nSeries:")
    for i, s in enumerate(series, 1):
        print(f"  {i:2d}. {s.name}  ({s.brand}) — {len(s.episodes)} episodes")
    while True:
        choice = _prompt("Pick a series number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(series):
            return series[int(choice) - 1]
        print("  Enter a valid number.")


def _choose_episode(series: Series) -> Episode:
    print(f"\n{series.name} — episodes:")
    for i, e in enumerate(series.episodes, 1):
        print(f"  {i:2d}. {e.title}  ({e.primary_ref})")
    print(f"  {len(series.episodes) + 1:2d}. [Custom topic in this series]")
    while True:
        choice = _prompt("Pick an episode number: ")
        if choice.isdigit():
            n = int(choice)
            if 1 <= n <= len(series.episodes):
                return series.episodes[n - 1]
            if n == len(series.episodes) + 1:
                return _custom_episode()
        print("  Enter a valid number.")


def _custom_episode() -> Episode:
    title = _prompt("  Topic / title: ")
    ref = _prompt("  Primary KJV reference (e.g. John 3:16): ")
    theme = _prompt("  One-line theme (optional): ")
    return Episode(title=title, primary_ref=ref, refs=[ref], theme=theme)


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a 60-second gospel short narration.")
    ap.add_argument("--no-audio", action="store_true",
                    help="Write the narration folder but skip running the audio pipeline.")
    args = ap.parse_args()

    config.require_api_key()  # fail fast with a clear message

    print("=" * 64)
    print("  Salt and Light Kingdom — 60s Short Narration Engine")
    print("=" * 64)

    series = _choose_series()
    episode = _choose_episode(series)
    notes = _prompt("\nOptional notes / angle (press Enter to skip): ")

    result = runner.create_narration(
        series, episode, notes=notes, run_audio=not args.no_audio
    )

    print("\n" + "=" * 64)
    if config.INDEPENDENT_REVIEW:
        print(f"  DONE — independent audit: {result.review.overall} "
              f"(self-review: {result.self_review.overall}), "
              f"{result.revisions_used} revision(s)")
    else:
        print(f"  DONE — verdict {result.review.overall}, "
              f"{result.revisions_used} revision(s)")
    print(f"  Structure: {result.structure.name}")
    print(f"  Folder: {result.folder}")
    print(f"  Review: {result.folder / 'narration.creation-review.md'}")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
