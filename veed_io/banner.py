"""Loud, impossible-to-miss spend banners + a hard confirmation gate.

Every billable generation must print a banner and pass through ``confirm_spend``.
Colours use ANSI; on a dumb terminal they degrade to plain bold markers.
"""

from __future__ import annotations

import os
import sys

from .pricing import CostEstimate

# ANSI codes
_RESET = "\033[0m"
_BOLD = "\033[1m"
_BLINK = "\033[5m"
_FG_BLACK = "\033[30m"
_FG_WHITE = "\033[97m"
_FG_RED = "\033[91m"
_FG_YELLOW = "\033[93m"
_BG_RED = "\033[101m"      # bright red background
_BG_YELLOW = "\033[103m"   # bright yellow background


def _colour_enabled() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("VEED_FORCE_COLOR"):
        return True
    return sys.stdout.isatty()


def spend_banner(estimate: CostEstimate, *, kind: str = "ESTIMATE") -> str:
    """Build a giant spend banner for ``estimate``.

    ``kind`` is e.g. "ESTIMATE" (before) or "CHARGED" (after).
    """
    money = f"${estimate.usd:.2f} USD"
    detail = (
        f"{estimate.duration_seconds:.1f}s  x  ${0.10:.2f}/min  x  "
        f"{estimate.multiplier:g}  (preset: {estimate.preset})"
    )
    line = f"  $$$  VEED SPEND {kind}:  {money}  $$$  "
    width = max(len(line), len(detail) + 4) + 2
    bar = "=" * width

    if _colour_enabled():
        hot = f"{_BOLD}{_BG_RED}{_FG_WHITE}"
        warn = f"{_BOLD}{_FG_YELLOW}"
        return (
            f"\n{warn}{bar}{_RESET}\n"
            f"{hot}{line.center(width)}{_RESET}\n"
            f"{warn}  {detail.center(width - 4)}  {_RESET}\n"
            f"{warn}{bar}{_RESET}\n"
        )
    # Plain fallback (still shouty)
    return (
        f"\n{'#' * width}\n"
        f"### VEED SPEND {kind}: {money}\n"
        f"### {detail}\n"
        f"{'#' * width}\n"
    )


def confirm_spend(estimate: CostEstimate, *, assume_yes: bool = False) -> bool:
    """Show the banner and gate the spend.

    Returns True only if the user (or ``assume_yes`` / ``--yes``) approves.
    In a non-interactive context with no ``assume_yes``, this refuses (returns
    False) rather than silently spending.
    """
    print(spend_banner(estimate, kind="ESTIMATE"))
    if assume_yes:
        print(f"{_BOLD}--yes given: proceeding with ~${estimate.usd:.2f} spend.{_RESET}"
              if _colour_enabled() else
              f"--yes given: proceeding with ~${estimate.usd:.2f} spend.")
        return True

    if not sys.stdin.isatty():
        print("Refusing to spend: non-interactive and --yes not given.",
              file=sys.stderr)
        return False

    try:
        reply = input(
            f"Spend ~${estimate.usd:.2f}? Type 'yes' to proceed: "
        ).strip().lower()
    except EOFError:
        # No real input available -> fail closed, never spend on ambiguity.
        print("\nRefusing to spend: no confirmation received.", file=sys.stderr)
        return False
    return reply in ("y", "yes")


def charged_banner(estimate: CostEstimate) -> str:
    """Banner to print AFTER a job completes, restating what it cost."""
    return spend_banner(estimate, kind="CHARGED (est.)")
