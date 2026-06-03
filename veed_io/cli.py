"""Command-line interface for veed_io.

Examples
--------
List presets and which tier (price) they fall in::

    python -m veed_io.cli presets

Burn captions into a hosted clip with the glass style, download the result::

    python -m veed_io.cli subtitle --video https://example.com/clip.mp4 \
        --preset glass --out ./out/

Upload a LOCAL file first, then subtitle it::

    python -m veed_io.cli subtitle --video ./clip.mp4 --preset simple --out ./out/

Estimate cost for a 60s clip with a dynamic preset::

    python -m veed_io.cli estimate --seconds 60 --preset glass
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from .banner import charged_banner, confirm_spend
from .models import PresetCustomization, SubtitleRequest, TextCustomization
from .presets import BASIC_PRESETS, DYNAMIC_PRESETS, POSITIONS, SHADOWS
from .pricing import estimate_cost

# Assume a worst-case Short length when we cannot probe the real duration, so
# the spend estimate over-states rather than under-states.
_FALLBACK_SECONDS = 60.0


def _looks_like_url(value: str) -> bool:
    return value.startswith(("http://", "https://", "data:"))


def _probe_seconds(source: str) -> float | None:
    """Best-effort media duration via ffprobe (works on local paths and URLs)."""
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None
    try:
        out = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", source],
            capture_output=True, text=True, timeout=30,
        )
        return float(out.stdout.strip())
    except (ValueError, subprocess.SubprocessError):
        return None


def _build_customization(args: argparse.Namespace) -> PresetCustomization | None:
    baseline = None
    if args.baseline_font or args.baseline_weight or args.baseline_color:
        baseline = TextCustomization(
            font=args.baseline_font,
            weight=args.baseline_weight,
            color=args.baseline_color,
        )
    highlighted = None
    if args.highlight_font or args.highlight_weight or args.highlight_color:
        highlighted = TextCustomization(
            font=args.highlight_font,
            weight=args.highlight_weight,
            color=args.highlight_color,
        )
    if not any([args.position, args.shadow, baseline, highlighted]):
        return None
    return PresetCustomization(
        position=args.position,
        shadow=args.shadow,
        baseline=baseline,
        highlighted=highlighted,
    )


def cmd_presets(_args: argparse.Namespace) -> int:
    print("Dynamic presets (2x price):")
    print("  " + ", ".join(DYNAMIC_PRESETS))
    print("\nBasic presets (1x price):")
    print("  " + ", ".join(BASIC_PRESETS))
    return 0


def cmd_estimate(args: argparse.Namespace) -> int:
    print(estimate_cost(args.seconds, args.preset))
    return 0


def cmd_subtitle(args: argparse.Namespace) -> int:
    # Import here so `presets`/`estimate` work without fal-client installed.
    from .client import VeedError, VeedSubtitlesClient

    try:
        client = VeedSubtitlesClient()
    except VeedError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    # --- duration + SPEND GATE (before any upload or billable call) ---
    probe_source = args.video
    seconds = args.seconds or _probe_seconds(probe_source)
    if seconds is None:
        seconds = _FALLBACK_SECONDS
        print(f"note: could not probe duration; assuming {seconds:.0f}s for the "
              f"estimate (pass --seconds to be exact).")
    estimate = estimate_cost(seconds, args.preset)
    if not confirm_spend(estimate, assume_yes=args.yes):
        print("aborted - no spend.", file=sys.stderr)
        return 3

    video = args.video
    if not _looks_like_url(video):
        local = Path(video)
        if not local.is_file():
            print(f"error: {video} is neither a URL nor an existing file",
                  file=sys.stderr)
            return 2
        print(f"uploading {local} ...")
        video = client.upload_file(local)
        print(f"  -> {video}")

    srt_content = None
    if args.srt_content_file:
        srt_content = Path(args.srt_content_file).read_text(encoding="utf-8")

    request = SubtitleRequest(
        video_url=video,
        preset=args.preset,
        language=args.language,
        srt_file_url=args.srt_file,
        srt_content=srt_content,
        customization=_build_customization(args),
    )

    if args.async_submit:
        request_id = client.submit(request, webhook_url=args.webhook)
        print(f"submitted. request_id = {request_id}")
        print(f"fetch with:  python -m veed_io.cli fetch --request-id {request_id}")
        print(charged_banner(estimate))
        return 0

    print(f"running {client.model_id} (preset={args.preset}) ...")
    result = client.subtitle(request, on_log=lambda m: print(f"  {m}"))
    print(f"\ndone. video: {result.video_url}")
    if args.out:
        path = client.download(result, args.out)
        print(f"saved: {path.resolve()}")
    print(charged_banner(estimate))
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    from .client import VeedError, VeedSubtitlesClient

    try:
        client = VeedSubtitlesClient()
    except VeedError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    result = client.result(args.request_id)
    print(f"video: {result.video_url}")
    if args.out:
        path = client.download(result, args.out)
        print(f"saved: {path.resolve()}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="veed_io",
        description="Burn styled subtitles into video via VEED on fal.ai.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("presets", help="list presets by price tier").set_defaults(
        func=cmd_presets
    )

    est = sub.add_parser("estimate", help="estimate USD cost")
    est.add_argument("--seconds", type=float, required=True, help="video duration")
    est.add_argument("--preset", default="glass")
    est.set_defaults(func=cmd_estimate)

    run = sub.add_parser("subtitle", help="run a subtitling job")
    run.add_argument("--video", required=True, help="URL or local file path")
    run.add_argument("--preset", default="glass")
    run.add_argument("--language", help="source-audio BCP-47 code, e.g. en-US")
    run.add_argument("--srt-file", help="URL to an .srt (skips transcription)")
    run.add_argument("--srt-content-file", help="local .srt path (skips transcription)")
    run.add_argument("--position", choices=POSITIONS)
    run.add_argument("--shadow", choices=SHADOWS)
    run.add_argument("--baseline-font")
    run.add_argument("--baseline-weight", type=int)
    run.add_argument("--baseline-color")
    run.add_argument("--highlight-font")
    run.add_argument("--highlight-weight", type=int)
    run.add_argument("--highlight-color")
    run.add_argument("--out", help="download result to this file or directory")
    run.add_argument("--seconds", type=float,
                     help="video duration for the spend estimate (else ffprobe)")
    run.add_argument("--yes", action="store_true",
                     help="approve the spend without an interactive prompt")
    run.add_argument("--async", dest="async_submit", action="store_true",
                     help="submit to queue and print request_id instead of blocking")
    run.add_argument("--webhook", help="webhook URL for async completion")
    run.set_defaults(func=cmd_subtitle)

    fetch = sub.add_parser("fetch", help="fetch a previously submitted job")
    fetch.add_argument("--request-id", required=True)
    fetch.add_argument("--out", help="download result to this file or directory")
    fetch.set_defaults(func=cmd_fetch)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
