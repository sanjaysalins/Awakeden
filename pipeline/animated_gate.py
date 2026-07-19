"""Animated-percentage gate for livingpage builds (every-screen-animated rule).

The 2026-07-17 locked rule (memory comic-grid-cost-tiered-animation, refined
2026-07-19): every screen must carry real generative animation — Ken Burns /
dyncam is only a fallback, and within a grid at least one cell must be a real
clip. Until 2026-07-19 (second session) the builders REPORTED
`kling_or_punch_or_slam_pct` in the DoD but nothing exited non-zero on a low
value — a silent slideshow regression shipped fine. This module is the teeth.

A beat counts as animated if any panel plays a real clip ("kling" in sources —
typography/infographic panel clips register the same way) OR the beat carries
a punch or slam (the beat visibly moves). Same formula as the DoD number.

Thresholds are corpus-calibrated against every shipped spec_report (2026-07-19):
shipped minimum is 75 (father_forgive_them short, Isaiah 53 inked full), so
75 is the grandfather floor — below it the slideshow is back and the build
blocks. New work should sit near 100 per the locked rule; 75–89 WARNs with
the dead-beat list so the gap is visible, never silent.

Only a real `--clips` render is gated: a stills-only preview build is
all-dyncam by design and would spuriously fail.
"""
from __future__ import annotations

FAIL_BELOW = 75   # corpus floor — every shipped piece >= 75; below = block (exit 5 in builders)
WARN_BELOW = 90   # the locked rule wants ~100 on new work; visible nag zone


def dead_beats(report: list[dict]) -> list[int]:
    """Beats with no real clip, no punch, no slam — the static screens."""
    return [r["beat"] for r in report
            if "kling" not in r.get("sources", [])
            and not r.get("punch") and not r.get("slams")]


def animated_pct(report: list[dict]) -> int:
    """Identical formula to the DoD's kling_or_punch_or_slam_pct."""
    return round(100 * (len(report) - len(dead_beats(report))) / len(report))


def check(report: list[dict], *, clips: bool) -> int:
    """0 = pass, 1 = block. `clips=False` (stills-only preview) is report-only."""
    if not report:
        return 0
    pct = animated_pct(report)
    dead = dead_beats(report)
    if not clips:
        if dead:
            print(f"[animated-gate] stills-only build, not gated — {pct}% "
                  f"(dead beats now: {dead})")
        return 0
    if pct < FAIL_BELOW:
        print(f"\nANIMATED-GATE BLOCK: only {pct}% of beats carry a real clip/punch/slam "
              f"(< {FAIL_BELOW}%, the shipped-corpus floor). Static beats: {dead}.\n"
              f"Animate them (Seedance/Kling/typography panel) or add punch/slam energy — "
              f"or --skip-animated-gate with user approval.")
        return 1
    if pct < WARN_BELOW:
        print(f"[animated-gate] WARN {pct}% < {WARN_BELOW}% — static beats: {dead} "
              f"(locked rule wants every screen animated; passes the {FAIL_BELOW}% floor)")
    return 0
