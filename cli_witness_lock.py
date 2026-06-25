"""cli_witness_lock.py — the fail-closed LOCK chokepoint for the Awakeden eyewitness format.

Every eyewitness narration folder must pass this before it is locked or its audio rendered.
Runs the deterministic EW-G1..EW-G6 gates (v2/EYEWITNESS_SPEC.md §4, §9) over the folder's
narration.md; on 0 blocking findings it writes <folder>/.locked (bound to the spoken text)
and prints LOCKED. Exits non-zero on any blocking finding. Mirrors cli_lock.py.

  .venv\\Scripts\\python.exe cli_witness_lock.py "<folder>" --form short
  .venv\\Scripts\\python.exe cli_witness_lock.py "<folder>" --form long
  .venv\\Scripts\\python.exe cli_witness_lock.py "<folder>" --form short --status   # report lock state only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import re

from pipeline import eyewitness_gates as EW


def _spoken_hash(md: str) -> str:
    """Hash the canonical SPOKEN text + the ordered SPEAKER tags (so an edit OR a voice-swap —
    e.g. re-tagging an invented line from a human to the_LORD — busts the lock)."""
    p = EW.parse_witness(md)
    canon = p.spoken_text.lower() + " || " + "|".join(s.lower() for s in p.speaker_tags)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- cross-episode cluster check
def _content_ngrams(spoken: str, n: int, skeleton: list[str]) -> set:
    low = spoken.lower()
    for sk in skeleton:                       # remove the intentional shared skeleton
        low = low.replace(sk, " ")
    toks = re.findall(r"[a-z']+", low)
    return {" ".join(toks[i:i + n]) for i in range(len(toks) - n + 1)}


def cluster_findings(folder: Path, rules: dict) -> list[str]:
    """Block a slate of near-identical episodes: compare this folder's spoken n-grams against
    every SIBLING eyewitness narration.md (same parent dir). cli_lock.py has this guard; the
    eyewitness lock was missing it — and this format is the most template-heavy in the repo."""
    cfg = rules.get("cluster", {})
    n = cfg.get("ngram", 5)
    cap = cfg.get("max_shared_ngrams", 6)
    skeleton = cfg.get("skeleton_phrases", [])
    md_path = folder / "narration.md"
    if not md_path.is_file():
        return []
    mine = _content_ngrams(EW.parse_witness(md_path.read_text(encoding="utf-8")).spoken_text, n, skeleton)
    if not mine:
        return []
    out: list[str] = []
    for sib in sorted((folder.parent).iterdir()):
        if not sib.is_dir() or sib.resolve() == folder.resolve():
            continue
        sib_md = sib / "narration.md"
        if not sib_md.is_file():
            continue
        theirs = _content_ngrams(EW.parse_witness(sib_md.read_text(encoding="utf-8")).spoken_text, n, skeleton)
        shared = mine & theirs
        if len(shared) > cap:
            ex = list(sorted(shared))[:2]
            out.append(f"shares {len(shared)} content {n}-grams with sibling '{sib.name}' "
                       f"(> {cap}) — too similar; e.g. \"{ex[0] if ex else ''}\"")
    return out


def _is_locked(folder: Path) -> tuple[bool, str]:
    lk = folder / ".locked"
    if not lk.is_file():
        return (False, "no .locked token")
    md_path = folder / "narration.md"
    if not md_path.is_file():
        return (False, "no narration.md")
    try:
        data = json.loads(lk.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return (False, ".locked is unreadable")
    cur = _spoken_hash(md_path.read_text(encoding="utf-8"))
    if data.get("spoken_sha256") != cur:
        return (False, "stale: spoken text changed since lock — re-run cli_witness_lock")
    return (True, "locked")


def require_lock(folder: Path, form: str) -> None:
    """Enforcement guard — call this at the TOP of the witness-voice / witness-cut build steps
    so audio/video can NEVER render an unlocked or stale eyewitness narration (a standalone CLI
    nobody is required to run is not enforcement — the red-team's point). Raises on failure."""
    folder = Path(folder)
    ok, why = _is_locked(folder)
    if not ok:
        raise SystemExit(
            f"[BLOCKED] {folder.name} is not locked ({why}). Run "
            f'cli_witness_lock.py "{folder}" --form {form} and pass the panel before rendering.')


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folder")
    ap.add_argument("--form", choices=["short", "long"], required=True)
    ap.add_argument("--status", action="store_true", help="report lock state only; make no changes")
    args = ap.parse_args(argv)

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        print(f"not a folder: {folder}", file=sys.stderr)
        return 2

    if args.status:
        ok, why = _is_locked(folder)
        print(f"[{'LOCKED' if ok else 'UNLOCKED'}] {folder.name} — {why}")
        return 0 if ok else 1

    md_path = folder / "narration.md"
    if not md_path.is_file():
        print(f"[BLOCKED] {folder.name} — no narration.md", file=sys.stderr)
        return 1
    md = md_path.read_text(encoding="utf-8")
    passage = EW.load_passage(folder)

    results = EW.run_gates(md, form=args.form, passage=passage)
    for r in results:
        print(f"  {r}")
        for f in r.findings:
            print(f"      - {f}")

    blocking = [r for r in results if not r.ok and r.blocking]

    # cross-episode cluster check (block a slate of near-identical episodes)
    cluster = cluster_findings(folder, EW.load_rules())
    for c in cluster:
        print(f"  [FAIL] EW-CLUSTER cross-episode: {c}")

    if blocking or cluster:
        print(f"\n[BLOCKED] {folder.name} — {len(blocking)} gate + {len(cluster)} cluster "
              "blocking finding(s). Fix the above and re-run cli_witness_lock.")
        return 1

    (folder / ".locked").write_text(
        json.dumps({
            "version": 1, "format": "eyewitness", "form": args.form,
            "spoken_sha256": _spoken_hash(md),
            "gates_run": [r.gate for r in results],
        }, indent=2),
        encoding="utf-8",
    )
    print(f"\n[LOCKED] {folder} — all EW-G1..EW-G6 passed; wrote .locked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
