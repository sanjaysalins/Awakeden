"""Visual-stage CLI: run scene planning (and, once V5/V8 land, image rendering
and Kling animation) against a locked narration v1 folder.

    cli_visual.py "<path-to-v1>"                    # default: full pipeline (when available)
    cli_visual.py "<path-to-v1>" --plan-only        # Phase A: paper scene plan + reviews
    cli_visual.py "<path-to-v1>" --provider hf      # use HuggingFace instead of Nano Banana Pro

V3 only supports --plan-only end-to-end. Phases B/C land in later chunks.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Windows consoles default to cp1252; force UTF-8 so em dashes / non-ASCII
# in the scene plan don't crash mid-stream.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import config
from pipeline import agent_bridge, visual_runner

agent_bridge.print_startup_banner()


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Run the visual stage (scene plan + image render + Kling animation) "
                    "against an existing locked narration v1 folder."
    )
    ap.add_argument("v1_folder", type=Path,
                    help='Path to the narration v1 folder, e.g. '
                         '".../narration/12 The Kiss That Cut Off the Bargain/v1"')
    ap.add_argument("--provider", choices=("nbp", "hf"),
                    default=config.VISUAL_DEFAULT_PROVIDER,
                    help="Image provider (Nano Banana Pro or HuggingFace). Default: %(default)s.")
    ap.add_argument("--plan-only", action="store_true",
                    help="Phase A only — scene plan + reviews + paper cohesion. No image renders.")
    ap.add_argument("--no-render", action="store_true",
                    help="Alias of --plan-only.")
    ap.add_argument("--no-animate", action="store_true",
                    help="Phases A+B — render images but skip Kling animation. (V8 wires this.)")
    ap.add_argument("--short-only", action=argparse.BooleanOptionalAction, default=True,
                    help="Render only the short_priority subset of scenes. Default on.")
    ap.add_argument("--max-retries", type=int, default=config.MAX_NBP_RETRIES,
                    help="Per-image content-audit retries before giving up. Default: %(default)s.")
    ap.add_argument("--kling-skip-audit", action="store_true",
                    help="Pass --skip-audit to image_to_kling.py. Use when the Stage A.5 "
                         "audit nit-picks positional/wording details and rejects cut plans "
                         "that would render fine (see HANDOVER.md for the documented hazard).")
    ap.add_argument("--replan", action="store_true",
                    help="Ignore an existing LOCKED scene_plan.json and regenerate it "
                         "(cut-aware re-plan: hero_candidate + inserts from the audio timeline).")
    args = ap.parse_args()

    if not args.v1_folder.exists():
        raise SystemExit(f"v1 folder does not exist: {args.v1_folder}")
    if not (args.v1_folder / "narration.creation.json").exists():
        raise SystemExit(
            f"No narration.creation.json under {args.v1_folder}. "
            "Run the text pipeline (cli.py) first."
        )

    config.require_api_key()

    print("=" * 64)
    print("  Salt and Light Kingdom — visual stage")
    print("=" * 64)
    print(f"  v1 folder:  {args.v1_folder}")
    print(f"  provider:   {args.provider}")
    print(f"  plan only:  {args.plan_only or args.no_render}")
    print(f"  no animate: {args.no_animate}")
    print(f"  short only: {args.short_only}")
    print("=" * 64)

    result = visual_runner.create_visuals(
        v1_folder=args.v1_folder,
        provider=args.provider,
        short_only=args.short_only,
        animate=not args.no_animate,
        plan_only=args.plan_only or args.no_render,
        kling_skip_audit=args.kling_skip_audit,
        replan=args.replan,
    )

    print("\n" + "=" * 64)
    review_label = "independent" if result.independent_review else "self"
    overall = (result.independent_review or result.self_review).overall
    print(f"  DONE — scene plan {review_label}: {overall}  "
          f"({result.revisions_used} revision(s))")
    print(f"  Paper cohesion:  {'PASS' if result.paper_cohesion.passed else 'FAIL'}")
    if result.rendered:
        passed = sum(1 for _, _, a in result.rendered if a.passed)
        print(f"  Rendered ({result.provider_used}): {passed}/{len(result.rendered)} passed content audit")
    print(f"  Folder:          {result.folder}")
    print(f"  Review:          {result.folder / 'scene_plan.review.md'}")
    if result.independent_review:
        print(f"  Independent:     {result.folder / 'scene_plan.independent-review.md'}")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
