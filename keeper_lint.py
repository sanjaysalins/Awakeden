#!/usr/bin/env python
"""keeper_lint.py -- the KEEPER LINT ($0, deterministic governor).

Round 6 (`poc_living_sketchbook/_FABLE_ROUND6_THE_KEEPER.md`, build order
step 2, claude's catch: "every content rule gets a fail-closed script" --
same house pattern as `margin_sentinel.py` and CLAUDE.md's
`panel_variety_lint.py`). This is that script for the five Keeper-Hand
engines (`panel_animator/keeper_hand.py`, `margin_study.py`,
`page_transitions.py`, `bleeding_word.py`, `candle_only.py`). It never
renders a frame -- it reads an episode's KEEPER-ENTRY MANIFEST (a plain JSON
description of every keeper-hand entry the episode's assembler is about to
composite: spread, origin, size, text, and the entry's own active time
window) and checks it against the Round 6 governors:

  FAIL  more than 1 keeper entry on the same spread (the "<=1 entry per
        spread" journal-not-subtitles rule)
  FAIL  more than 4 non-header entries + 1 header across the whole episode
  FAIL  any entry sized below the LAW 2 floor (54px @ 1080-width)
  FAIL  any entry's origin lands inside the logo safe-zone (x 40-240,
        y 70-160) or the bottom 18% UI caption band (y > 0.82 * canvas height)
  FAIL  an entry's active time window overlaps a verse-card window on the
        SAME spread (the Keeper's words must never compete with the Word)
  WARN  the entry's text contains a doctrine-adjacent keyword (list below)
        -- not a FAIL; every WARN is surfaced by name for the panel. The
        Keeper's words are a human voice (questions/observations), never a
        doctrine claim -- this is a human judgment call, not automatable, so
        the lint only FLAGS it.

Manifest schema (one JSON file per episode):
    {
      "episode": "<name>",
      "canvas": {"w": 1080, "h": 1920},
      "spreads": [
        {"id": "s01",
         "entries": [
           {"text": "...", "origin": [x, y], "size": 64, "is_header": false,
            "t_start": 0.6, "t_end": 3.2}
         ],
         "verse_cards": [{"t_start": 23.55, "t_end": 27.10}]
        }, ...
      ]
    }

Usage:
    .venv\\Scripts\\python.exe keeper_lint.py <manifest.json>
    .venv\\Scripts\\python.exe keeper_lint.py --selftest

Exit codes: 0 = clean (WARNs may still print). 1 = at least one FAIL.
            2 = manifest missing/unreadable/malformed, or no args given.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_W, DEFAULT_H = 1080, 1920
MIN_SIZE = 54                        # LAW 2 floor (keeper_hand.MIN_SIZE)
LOGO_ZONE = (40, 240, 70, 160)       # x0, x1, y0, y1 -- px @ 1080-width reference
BOTTOM_BAND_FRAC = 0.82              # y > this fraction of canvas height = UI caption band
MAX_ENTRIES_PER_SPREAD = 1
MAX_NON_HEADER_PER_EPISODE = 4       # + 1 header, checked separately
MAX_HEADERS_PER_EPISODE = 1

DOCTRINE_KEYWORDS = [
    "saved", "saves", "salvation", "sin", "sins", "repent", "believe",
    "faith", "lord", "christ", "messiah", "god", "spirit", "forgive",
]
_KEYWORD_RE = re.compile(r"\b(" + "|".join(DOCTRINE_KEYWORDS) + r")\b", re.IGNORECASE)


def _in_zone(x: float, y: float, zone: tuple[float, float, float, float]) -> bool:
    x0, x1, y0, y1 = zone
    return x0 <= x <= x1 and y0 <= y <= y1


def lint_manifest(manifest: dict) -> tuple[list[str], list[str]]:
    """Returns (fails, warns), each a list of human-readable messages. Pure
    function of the manifest dict -- no filesystem/network access, so this is
    trivially unit-testable (see run_selftest())."""
    fails: list[str] = []
    warns: list[str] = []

    canvas = manifest.get("canvas", {})
    w = canvas.get("w", DEFAULT_W)
    h = canvas.get("h", DEFAULT_H)
    bottom_y = BOTTOM_BAND_FRAC * h

    total_non_header = 0
    total_headers = 0

    for spread in manifest.get("spreads", []):
        sid = spread.get("id", "?")
        entries = spread.get("entries", [])
        verse_cards = spread.get("verse_cards", [])

        non_header_here = [e for e in entries if not e.get("is_header")]
        if len(non_header_here) > MAX_ENTRIES_PER_SPREAD:
            fails.append(
                f"{sid}: {len(non_header_here)} keeper entries on one spread "
                f"(limit {MAX_ENTRIES_PER_SPREAD}) -- a journal, not subtitles")

        for e in entries:
            text = e.get("text", "")
            if e.get("is_header"):
                total_headers += 1
            else:
                total_non_header += 1

            size = e.get("size", 0)
            if size < MIN_SIZE:
                fails.append(f"{sid}: entry {text!r} size={size} below the LAW 2 floor ({MIN_SIZE}px)")

            origin = e.get("origin", [0, 0])
            ox, oy = origin[0], origin[1]
            if _in_zone(ox, oy, LOGO_ZONE):
                fails.append(f"{sid}: entry {text!r} origin {(ox, oy)} lands inside "
                             f"the logo safe-zone {LOGO_ZONE}")
            if oy > bottom_y:
                fails.append(f"{sid}: entry {text!r} origin {(ox, oy)} lands inside "
                             f"the bottom {int(round((1 - BOTTOM_BAND_FRAC) * 100))}% UI band "
                             f"(y > {bottom_y:.0f})")

            hits = sorted(set(m.group(1).lower() for m in _KEYWORD_RE.finditer(text)))
            if hits:
                warns.append(f"{sid}: entry {text!r} contains doctrine-adjacent "
                              f"keyword(s) {hits} -- flagged for the panel, not auto-failed")

            t_start, t_end = e.get("t_start"), e.get("t_end")
            if t_start is not None and t_end is not None:
                for vc in verse_cards:
                    vs, ve = vc.get("t_start"), vc.get("t_end")
                    if vs is not None and ve is not None and t_start < ve and vs < t_end:
                        fails.append(f"{sid}: entry {text!r} window [{t_start},{t_end}] "
                                     f"overlaps verse-card window [{vs},{ve}] on the same spread")

    if total_non_header > MAX_NON_HEADER_PER_EPISODE:
        fails.append(f"episode: {total_non_header} non-header keeper entries "
                     f"(limit {MAX_NON_HEADER_PER_EPISODE} + 1 header)")
    if total_headers > MAX_HEADERS_PER_EPISODE:
        fails.append(f"episode: {total_headers} field headers (limit {MAX_HEADERS_PER_EPISODE})")

    return fails, warns


def lint_file(path: Path) -> int:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[error] could not read/parse {path}: {e}")
        return 2

    fails, warns = lint_manifest(manifest)
    print(f"=== KEEPER LINT -- {path} ===\n")
    if warns:
        print(f"{len(warns)} WARN(s) -- doctrine-adjacent keyword(s), for the panel:")
        for w in warns:
            print(f"  WARN  {w}")
        print()
    if fails:
        print(f"{len(fails)} FAIL(s):")
        for f in fails:
            print(f"  FAIL  {f}")
        return 1
    print("0 FAILs.")
    return 0


# ---------------------------------------------------------------------------
# self-test: one planted violation per rule, plus a clean control spread that
# must NOT be flagged
# ---------------------------------------------------------------------------

def _selftest_manifest() -> dict:
    return {
        "episode": "selftest",
        "canvas": {"w": 1080, "h": 1920},
        "spreads": [
            {   # violation: 2 entries on one spread
                "id": "s01_two_entries",
                "entries": [
                    {"text": "first entry.", "origin": [400, 1000], "size": 60,
                     "t_start": 1.0, "t_end": 2.0},
                    {"text": "second entry, same spread.", "origin": [400, 1100], "size": 60,
                     "t_start": 3.0, "t_end": 4.0},
                ],
                "verse_cards": [],
            },
            {   # violation: size < 54
                "id": "s02_too_small",
                "entries": [
                    {"text": "too small.", "origin": [400, 1000], "size": 40,
                     "t_start": 1.0, "t_end": 2.0},
                ],
                "verse_cards": [],
            },
            {   # violation: inside logo zone
                "id": "s03_logo_zone",
                "entries": [
                    {"text": "in the logo zone.", "origin": [120, 100], "size": 60,
                     "t_start": 1.0, "t_end": 2.0},
                ],
                "verse_cards": [],
            },
            {   # violation: inside bottom UI band
                "id": "s04_bottom_band",
                "entries": [
                    {"text": "in the caption band.", "origin": [400, 1800], "size": 60,
                     "t_start": 1.0, "t_end": 2.0},
                ],
                "verse_cards": [],
            },
            {   # violation: overlaps a verse card window
                "id": "s05_verse_overlap",
                "entries": [
                    {"text": "overlapping the verse card.", "origin": [400, 1000], "size": 60,
                     "t_start": 5.0, "t_end": 8.0},
                ],
                "verse_cards": [{"t_start": 7.0, "t_end": 10.0}],
            },
            {   # WARN only: doctrine-adjacent keyword, otherwise clean
                "id": "s06_doctrine_warn",
                "entries": [
                    {"text": "did he mean it -- saved, even us?", "origin": [400, 1000], "size": 60,
                     "t_start": 1.0, "t_end": 2.0},
                ],
                "verse_cards": [],
            },
            {   # clean control spread -- must NOT be flagged for anything
                "id": "s07_clean",
                "entries": [
                    {"text": "not a breath of wind.", "origin": [400, 1000], "size": 64,
                     "t_start": 1.0, "t_end": 2.0},
                ],
                "verse_cards": [{"t_start": 10.0, "t_end": 12.0}],
            },
        ],
    }


def run_selftest() -> int:
    manifest = _selftest_manifest()
    fails, warns = lint_manifest(manifest)
    fail_text = "\n".join(fails)
    warn_text = "\n".join(warns)

    checks = [
        (any(f.startswith("s01_two_entries:") and "spread" in f for f in fails),
         ">1 entry/spread caught (s01)"),
        (any(f.startswith("s02_too_small:") and "LAW 2" in f for f in fails),
         "size<54 caught (s02)"),
        (any(f.startswith("s03_logo_zone:") and "logo safe-zone" in f for f in fails),
         "logo-zone lane caught (s03)"),
        (any(f.startswith("s04_bottom_band:") and "UI band" in f for f in fails),
         "bottom-band lane caught (s04)"),
        (any(f.startswith("s05_verse_overlap:") and "verse-card window" in f for f in fails),
         "verse-card overlap caught (s05)"),
        (any(w.startswith("s06_doctrine_warn:") and "saved" in w for w in warns),
         "doctrine keyword WARN caught (s06)"),
        (not any(f.startswith("s06_doctrine_warn:") for f in fails),
         "doctrine keyword is a WARN, not a FAIL (s06)"),
        (not any(f.startswith("s07_clean:") for f in fails) and
         not any(w.startswith("s07_clean:") for w in warns),
         "clean control spread NOT falsely flagged (s07)"),
        (any("episode:" in f and "non-header keeper entries" in f for f in fails),
         "episode-wide entry-count ceiling caught (7 non-header entries > 4)"),
    ]

    print("=== KEEPER LINT SELFTEST (planted violations) ===\n")
    ok = True
    for passed, label in checks:
        print(f"  {'PASS' if passed else 'FAIL'}  {label}")
        ok = ok and passed
    print(f"\n{len(fails)} FAIL(s) / {len(warns)} WARN(s) total in the fixture.")
    print(f"\n{'ALL PASS' if ok else 'FAILURES ABOVE'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", nargs="?", help="path to a keeper-entry manifest JSON")
    ap.add_argument("--selftest", action="store_true", help="run the planted-violation selftest")
    a = ap.parse_args(argv)

    if a.selftest:
        return run_selftest()
    if not a.manifest:
        ap.print_help()
        return 2
    return lint_file(Path(a.manifest))


if __name__ == "__main__":
    raise SystemExit(main())
