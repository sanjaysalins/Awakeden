#!/usr/bin/env python
"""release_check.py — the $0 fail-closed SYNC gate: website x publish x upload x tracking.

Runs SYNC-G1..G7 (v2/RELEASE_SYNC.md) over every catalogue item in
`_website/manifest.yaml`, hard-joined to its piece folder — no fuzzy matching.
Exit 0 = GREEN (warns allowed), exit 1 = drift somewhere (each line says the
one command that fixes it). Run before any _website deploy and after any
posting batch.

  .venv\\Scripts\\python.exe release_check.py               # everything
  .venv\\Scripts\\python.exe release_check.py --slug X      # one piece (substring ok)
  .venv\\Scripts\\python.exe release_check.py --strict      # WARNs count as FAILs
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from pipeline import release_state  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", default="", help="only items whose slug contains this")
    ap.add_argument("--strict", action="store_true", help="WARNs count as FAILs")
    args = ap.parse_args()

    try:
        states, orphans, orphan_pages = release_state.gather()
    except Exception as e:  # malformed manifest/ledger must fail CLOSED, by name
        print(f"RED - could not read the release state: {type(e).__name__}: {e}")
        print("(check _website/manifest.yaml and data/release_ledger.json)")
        return 1
    # gates ALWAYS run over the FULL catalogue (a --slug-filtered gate run lied:
    # G7 couldn't see the parent long and cried wolf — red-team M2); the filter
    # only narrows what is PRINTED.
    findings = release_state.run_gates(states, orphans, orphan_pages)
    if args.slug:
        shown = [s for s in states if args.slug in s.slug]
        if not shown:
            print(f"no catalogue item matches --slug '{args.slug}'")
            return 2
        keep = {s.slug for s in shown}
        findings = [f for f in findings if f[2] in keep]
        states = shown

    fails = [f for f in findings if f[1] == "FAIL"]
    warns = [f for f in findings if f[1] == "WARN"]
    if args.strict:
        fails, warns = fails + warns, []

    for gate, lvl, slug, msg in sorted(findings, key=lambda x: (x[1] != "FAIL", x[0], x[2])):
        print(f"  {lvl:4} {gate:8} {slug:34} {msg}")

    queue = release_state.to_post(states)
    if queue:
        print(f"\nTO POST ({len(queue)} piece(s)):")
        for s, missing in queue:
            idx = (s.source_dir / "publish" / "PUBLISH_INDEX.html") if s.source_dir else None
            link = f"  file:///{str(idx).replace(chr(92), '/')}" if idx and idx.is_file() else ""
            print(f"  {s.slug:34} {'+'.join(missing):34}{link}")

    n_ok = len(states) - len({f[2] for f in fails})
    print(f"\n{len(states)} items · {n_ok} clean · {len(fails)} FAIL · {len(warns)} WARN")
    if fails:
        print("RED — the release desk is out of sync; fix the FAIL lines above.")
        return 1
    print("GREEN — website, packs, thumbs and ledger agree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
