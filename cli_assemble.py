"""Assembly stage — fit the rendered clips + narration into a deliverable 60s
vertical viral cut (+ an all-takes reel), with intelligent clip↔word matching,
a self-review panel, an independent red-team audit, and per-slot Vision verify.

Usage:
  .venv\\Scripts\\python.exe cli_assemble.py "<v1 folder>"
  .venv\\Scripts\\python.exe cli_assemble.py "<v1 folder>" --plan-only
  .venv\\Scripts\\python.exe cli_assemble.py "<v1 folder>" --clips all       # all 16 (may strobe)
  .venv\\Scripts\\python.exe cli_assemble.py "<v1 folder>" --clips 11        # default
  .venv\\Scripts\\python.exe cli_assemble.py "<v1 folder>" --no-reel --no-verify
  .venv\\Scripts\\python.exe cli_assemble.py "<v1 folder>" --hero 7 --speed-cap 2.2
  .venv\\Scripts\\python.exe cli_assemble.py "<v1 folder>" --rebuild --replan
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import config
from pipeline import agent_bridge, assembly_runner

agent_bridge.print_startup_banner()


def main() -> int:
    # Force UTF-8 stdout — the narration text carries em-dashes / curly quotes
    # that crash the default Windows cp1252 console.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser(
        description="Assemble the 60s viral cut + all-takes reel from the rendered "
                    "clips and the locked narration MP3."
    )
    ap.add_argument("v1_folder", type=Path,
                    help='Path to the narration v1 folder (must contain narration.mp3, '
                         '_turns/, and visual/<provider>/ clips).')
    ap.add_argument("--provider", choices=("hf", "nbp"), default="hf",
                    help="Which rendered clip set to assemble. Default: %(default)s.")
    ap.add_argument("--clips", default=str(config.ASSEMBLY_CLIP_BUDGET),
                    help='Body-clip budget for the viral cut: an integer, or "all" to '
                         'force every clip in (may strobe). Default: %(default)s.')
    ap.add_argument("--plan-only", action="store_true",
                    help="Plan + review only — no render. Writes edit_plan.json + index.html.")
    ap.add_argument("--no-reel", action="store_true", help="Skip the all-takes reel.")
    ap.add_argument("--no-verify", action="store_true", help="Skip the per-slot Vision audit.")
    ap.add_argument("--hero", type=int, default=0,
                    help="Force the hero scene index for the bookend (0 = let the planner choose).")
    ap.add_argument("--exclude", default="",
                    help="Comma-separated scene indices to drop from the cut (glitchy/hallucinated clips), e.g. 3,10.")
    ap.add_argument("--speed-cap", type=float, default=0.0,
                    help="Override the hard speed cap (default from config = %.1f)." % config.ASSEMBLY_SPEED_CAP)
    ap.add_argument("--rebuild", action="store_true", help="Re-render even if the cut exists.")
    ap.add_argument("--replan", action="store_true", help="Re-plan even if a LOCKED plan exists.")
    args = ap.parse_args()

    if not args.v1_folder.exists():
        raise SystemExit(f"v1 folder does not exist: {args.v1_folder}")
    if not (args.v1_folder / "narration.mp3").exists():
        raise SystemExit(f"No narration.mp3 under {args.v1_folder}. Run the audio stage first.")
    config.require_api_key()

    clips_arg = args.clips.strip().lower()
    if clips_arg in ("all", "16", "max"):
        clip_budget = 9999  # >= clip count -> all
    else:
        try:
            clip_budget = int(clips_arg)
        except ValueError:
            raise SystemExit(f"--clips must be an integer or 'all', got {args.clips!r}")

    if args.speed_cap > 0:
        config.ASSEMBLY_SPEED_CAP = args.speed_cap

    exclude: set[int] = set()
    if args.exclude.strip():
        try:
            exclude = {int(x) for x in args.exclude.replace(" ", "").split(",") if x}
        except ValueError:
            raise SystemExit(f"--exclude must be comma-separated integers, got {args.exclude!r}")

    print("=" * 64)
    print("  Salt and Light Kingdom — assembly stage")
    print("=" * 64)
    print(f"  v1:        {args.v1_folder}")
    print(f"  provider:  {args.provider}")
    print(f"  clips:     {'all' if clip_budget >= 9999 else clip_budget}")
    print(f"  speed cap: {config.ASSEMBLY_SPEED_CAP:.2f}x")
    print(f"  reel:      {not args.no_reel}   verify: {not args.no_verify}")
    print("=" * 64)

    result = assembly_runner.run_assembly(
        v1_folder=args.v1_folder,
        provider=args.provider,
        clip_budget=clip_budget,
        plan_only=args.plan_only,
        reel=not args.no_reel,
        verify=not args.no_verify,
        hero=args.hero,
        exclude=exclude,
        rebuild=args.rebuild,
        replan=args.replan,
    )

    overall = (result.independent_review or result.self_review).overall
    print("\n" + "=" * 64)
    print(f"  DONE — edit plan: {overall}  ({result.revisions_used} revision(s))")
    if result.viral_cut:
        print(f"  viral cut: {result.viral_cut}")
    if result.reel:
        print(f"  reel:      {result.reel}")
    if result.audit and result.audit.reroll_scene_indices:
        print(f"  verify flagged scenes: {result.audit.reroll_scene_indices}")
    if result.index_html:
        print(f"  review:    {result.index_html}")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
