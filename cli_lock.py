"""cli_lock.py — the fail-closed lock chokepoint.

Every narration folder must pass this before it is locked or its audio rendered.
Runs KJV-strict (Phase B) + Rule-8 (short) + the cross-artifact cluster check
(Phase A) vs its siblings; on 0 blocking findings it writes <folder>/.locked
(bound to the spoken text) and registers the artifact. Exits non-zero on any
blocking finding.

  .venv\\Scripts\\python.exe cli_lock.py "<narration-folder>"
  .venv\\Scripts\\python.exe cli_lock.py "<folder>" --form long
  .venv\\Scripts\\python.exe cli_lock.py "<folder>" --no-cluster
  .venv\\Scripts\\python.exe cli_lock.py "<folder>" --status     # just report lock state
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pipeline import lock as L


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folder")
    ap.add_argument("--form", choices=["short", "long"], default="short")
    ap.add_argument("--no-cluster", action="store_true", help="skip the cross-artifact cluster check")
    ap.add_argument("--status", action="store_true", help="report lock state only; make no changes")
    args = ap.parse_args(argv)

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        print(f"not a folder: {folder}", file=sys.stderr)
        return 2

    if args.status:
        ok, why = L.is_locked(folder)
        print(f"[{'LOCKED' if ok else 'UNLOCKED'}] {folder.name} — {why}")
        return 0 if ok else 1

    rep = L.run_lock(folder, form=args.form, check_cluster=not args.no_cluster)
    for d in rep.get("doctrine", []):
        print(f"  [DOCTRINE WARN] {d['landmine']}: '{d['matched']}' — {d['note']}")
    if rep["ok"]:
        msg = "all checks passed; wrote .locked + registered."
        if rep.get("doctrine"):
            msg += f" ({len(rep['doctrine'])} doctrine WARNING(s) above — human review advised, not blocking)"
        print(f"[LOCKED] {rep['folder']} — {msg}")
        return 0
    print(f"[BLOCKED] {rep['folder']} — {len(rep['blocking'])} blocking finding(s):")
    for b in rep["blocking"]:
        print(f"  - {b}")
    print("\nFix the findings (de-template / correct the KJV) and re-run cli_lock.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
