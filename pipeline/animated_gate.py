"""Animated-percentage gate for livingpage builds (every-screen-animated rule).

The 2026-07-17 locked rule (memory comic-grid-cost-tiered-animation, refined
2026-07-19): every screen must carry real generative animation — Ken Burns /
dyncam is only a fallback, and within a grid at least one cell must be a real
clip. Until 2026-07-19 (second session) the builders REPORTED
`kling_or_punch_or_slam_pct` in the DoD but nothing exited non-zero on a low
value — a silent slideshow regression shipped fine. This module is the teeth.

TWO dimensions, both corpus-calibrated against every shipped spec_report
(2026-07-19 sweep, all 23 livingpage reports):

1. Composite (the DoD formula): a beat is alive if any panel plays a real
   clip ("kling" in sources — typography/infographic panel clips register the
   same way) OR the beat carries a punch or slam. Shipped floor = 75
   (father_forgive_them short, Isaiah 53 inked full) -> FAIL below 75.
2. Real-clip floor (red-team F3, 2026-07-19): punch/slams are $0 ffmpeg edit
   effects, and on punch/slam-heavy specs (thirty_pieces = 78% on punch/slam
   ALONE) the composite floor passes with an EMPTY or mis-pathed clips dir —
   a zero-real-clip slideshow with a green gate. So beats with an actual
   "kling" source get their own floor: shipped minimum is 42% (Isaiah 53)
   -> FAIL below 40, and 0 real clips is called out explicitly.

WARN band: below 80 (red-team F5 recalibration — at the original 90 roughly
half the approved corpus WARNed on rebuild, gold master included, which
trains the signal to be ignored; at 80 only the three true outliers nag).

Only a real `--clips` render is gated: a stills-only preview build is
all-dyncam by design and would spuriously fail. The builders stamp
`clips_build` into the report JSON so downstream (cli_livingpage) can refuse
to score a no-clips preview (red-team F1).

Known, accepted cost (red-team 2026-07-19): the gate consumes the builders'
per-beat `report`, which is only complete after the segment-render loop — so a
blocked `--clips` build pays the full ffmpeg render before exiting 5 (and a
batch_advance retry pays it twice). A pre-render spec classifier could give
the verdict in milliseconds, but it would duplicate `source()`'s
classification logic in a second place — the exact fork-drift disease these
gates exist to prevent. Report-based = authoritative, zero drift; run
`--lint --clips` first ($0) when the outcome is in doubt.
"""
from __future__ import annotations

FAIL_BELOW = 75        # composite corpus floor — every shipped piece >= 75
REAL_FAIL_BELOW = 40   # real-clip corpus floor — shipped minimum 42% (Isaiah 53)
WARN_BELOW = 80        # nag zone: only the corpus outliers (75/76), not the gold master (89)


def dead_beats(report: list[dict]) -> list[int]:
    """Beats with no real clip, no punch, no slam — the static screens."""
    return [r["beat"] for r in report
            if "kling" not in r.get("sources", [])
            and not r.get("punch") and not r.get("slams")]


def animated_pct(report: list[dict]) -> int:
    """Identical formula to the DoD's kling_or_punch_or_slam_pct."""
    return round(100 * (len(report) - len(dead_beats(report))) / len(report))


def real_clip_pct(report: list[dict]) -> int:
    """Beats where at least one panel plays an actual rendered clip."""
    return round(100 * sum(1 for r in report if "kling" in r.get("sources", []))
                 / len(report))


def check(report: list[dict], *, clips: bool) -> int:
    """0 = pass, 1 = block. `clips=False` (stills-only preview) is report-only."""
    if not report:
        return 0
    pct = animated_pct(report)
    rc = real_clip_pct(report)
    dead = dead_beats(report)
    if not clips:
        if dead:
            print(f"[animated-gate] stills-only build, not gated — {pct}% "
                  f"(dead beats now: {dead})")
        return 0
    if rc == 0:
        print(f"\nANIMATED-GATE BLOCK: ZERO beats play a real clip in a --clips build — "
              f"the clips dir is empty, mis-pathed, or every slug is renamed. "
              f"(punch/slam energy alone reads {pct}% but those are $0 edit effects, "
              f"not animation.) Fix the clips dir — or --skip-animated-gate with user approval.")
        return 1
    if rc < REAL_FAIL_BELOW:
        print(f"\nANIMATED-GATE BLOCK: only {rc}% of beats play a real clip "
              f"(< {REAL_FAIL_BELOW}%, the shipped-corpus real-clip floor — minimum is "
              f"Isaiah 53 at 42%). Punch/slams don't substitute for animation.")
        return 1
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
