#!/usr/bin/env python
"""batch_advance.py — walk every living-page piece in a batch through its $0 steps.

The night-shift runner: for each piece folder under the batch dir it re-detects the
position (cli_livingpage.detect, artifact-driven) and runs the next step while it is
auto=True ($0, no human gate). PAID steps (BytePlus stills, Kling) and HUMAN gates
(stills approval, audio by ear) are NEVER run — the piece is parked with its exact
next command, per INV-20 (ask before spending). A crashed step is retried once, then
the piece is marked BLOCKED and the runner moves to the next piece. A step that
returns 0 but doesn't advance the board is marked STUCK (no infinite loops).

  .venv\\Scripts\\python.exe batch_advance.py batches\\cluster_01_cross
  .venv\\Scripts\\python.exe batch_advance.py batches\\cluster_01_cross --pieces pierced,i_thirst
  .venv\\Scripts\\python.exe batch_advance.py batches\\cluster_01_cross --dry-run
  .venv\\Scripts\\python.exe batch_advance.py batches\\cluster_01_cross --json

Exit code: 0 = every piece COMPLETE or parked at a gate; 1 = any BLOCKED/STUCK piece.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import cli_livingpage as LP

STEP_TIMEOUT_S = 3600          # a single build/score/sfx step must finish within an hour
MAX_STEPS_PER_PIECE = 12       # backstop far above the real chain length


def find_pieces(batch: Path, only: set[str]) -> list[Path]:
    out = []
    for d in sorted(batch.iterdir()):
        if not d.is_dir() or d.name.startswith(("_", ".")):
            continue
        if not ((d / "piece.json").is_file() or (d / "narration.md").is_file()):
            continue
        if only and not any(o in d.name for o in only):
            continue
        out.append(d)
    return out


def run_step(cmd: str) -> tuple[bool, str]:
    """Run one $0 step, retrying once on failure. -> (ok, tail of output on failure)."""
    for attempt in (1, 2):
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                               timeout=STEP_TIMEOUT_S)
        except subprocess.TimeoutExpired:
            if attempt == 1:
                continue
            return False, f"timed out after {STEP_TIMEOUT_S}s"
        if r.returncode == 0:
            return True, ""
        if attempt == 1:
            print(f"      retrying (exit {r.returncode})...")
    tail = "\n".join(((r.stdout or "") + "\n" + (r.stderr or "")).strip().splitlines()[-12:])
    return False, tail


def advance_piece(piece: Path, dry: bool) -> dict:
    """Advance one piece until COMPLETE or the first non-auto step. Never spends."""
    ran: list[str] = []
    last = None
    for _ in range(MAX_STEPS_PER_PIECE):
        steps = LP.detect(piece)
        nxt = next((s for s in steps if not s.done), None)
        if nxt is None:
            return {"piece": piece.name, "state": "COMPLETE", "ran": ran}
        if not nxt.auto:
            kind = "PAID" if "[PAID" in nxt.next_cmd else "GATE"
            return {"piece": piece.name, "state": f"{kind}:{nxt.name}", "ran": ran,
                    "detail": nxt.detail, "cmd": nxt.next_cmd}
        if nxt.name == last:
            return {"piece": piece.name, "state": f"STUCK:{nxt.name}", "ran": ran,
                    "detail": f"step returned 0 but board still shows it pending — {nxt.detail}",
                    "cmd": nxt.next_cmd}
        if dry:
            return {"piece": piece.name, "state": f"WOULD-RUN:{nxt.name}", "ran": ran,
                    "cmd": nxt.next_cmd}
        print(f"   -> {nxt.name}: {nxt.next_cmd}")
        ok, tail = run_step(nxt.next_cmd)
        if not ok:
            return {"piece": piece.name, "state": f"BLOCKED:{nxt.name}", "ran": ran,
                    "detail": tail, "cmd": nxt.next_cmd}
        ran.append(nxt.name)
        last = nxt.name
    return {"piece": piece.name, "state": "MAXED", "ran": ran,
            "detail": f"gave up after {MAX_STEPS_PER_PIECE} steps"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="advance every piece in a batch through its $0 steps")
    ap.add_argument("batch", help="batch folder (e.g. batches\\cluster_01_cross)")
    ap.add_argument("--pieces", default="", help="comma substrings — limit which pieces")
    ap.add_argument("--dry-run", action="store_true", help="report what WOULD run, run nothing")
    ap.add_argument("--json", action="store_true", help="machine-readable board")
    a = ap.parse_args(argv)
    batch = Path(a.batch).resolve()
    if not batch.is_dir():
        print(f"not a folder: {batch}", file=sys.stderr)
        return 2
    only = {s.strip() for s in a.pieces.split(",") if s.strip()}
    pieces = find_pieces(batch, only)
    if not pieces:
        print("no pieces found", file=sys.stderr)
        return 2

    results = []
    for piece in pieces:
        if not a.json:
            print(f"\n== {piece.name} ==")
        results.append(advance_piece(piece, a.dry_run))

    if a.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"\n==== batch board - {batch.name} ====")
        for r in results:
            ran = f"  (ran: {', '.join(r['ran'])})" if r["ran"] else ""
            print(f"  [{r['state']:>18}] {r['piece']}{ran}")
            if r.get("cmd") and not r["state"].startswith("COMPLETE"):
                print(f"  {'':>20}  next: {r['cmd']}")
            if r.get("detail") and r["state"].split(":")[0] in ("BLOCKED", "STUCK", "MAXED"):
                for line in r["detail"].splitlines():
                    print(f"  {'':>20}  ! {line}")
        n_done = sum(r["state"] == "COMPLETE" for r in results)
        n_bad = sum(r["state"].split(":")[0] in ("BLOCKED", "STUCK", "MAXED") for r in results)
        print(f"\n  {n_done} complete | {len(results) - n_done - n_bad} at a gate/paid step | "
              f"{n_bad} blocked | $0 spent")
    return 1 if any(r["state"].split(":")[0] in ("BLOCKED", "STUCK", "MAXED") for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
