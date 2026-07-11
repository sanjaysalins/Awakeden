"""Calibration loop — the engine learns to PREDICT the external panel.

Each episode logs, in `data/learning/calibration.jsonl`, the real defects the
external LLM panel (or the user) caught that the self-review + independent audit
rated PASS/STRONG. Those are the self-review's BLIND SPOTS. The reporter aggregates
them by defect class and flags every class that keeps slipping past the internal
review while it is NOT yet a hard gate (or not reliably self-review-covered).

Workflow (propose-I-approve): run `_calibrate.py` -> read the proposals -> approve
the ones you want -> the agent strengthens the self-review prompt / adds a gate ->
the blind spot closes. When a class stops appearing in panel_misses for K episodes,
the engine has learned it; once the WHOLE panel_misses stream runs dry for K
episodes, you can SAMPLE the external panel instead of running it every time.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

_DATA = Path(__file__).resolve().parent.parent / "data" / "learning"
LEDGER = _DATA / "calibration.jsonl"
TAXONOMY = _DATA / "defect_classes.json"

# A class that has slipped past the internal review this many times (or more) and
# is not yet a reliably-covered hard gate is surfaced as a proposal.
PROMOTE_THRESHOLD = 1


def load_ledger() -> list[dict]:
    if not LEDGER.exists():
        return []
    out = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def load_taxonomy() -> dict:
    return json.loads(TAXONOMY.read_text(encoding="utf-8")).get("classes", {})


def append_record(record: dict) -> None:
    """Append one episode's calibration record (caller builds the dict)."""
    _DATA.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def validate_record(record: dict, tax: dict) -> tuple[list[str], list[str]]:
    """-> (blocking problems, warnings). A record needs an episode name and a
    panel_misses list (empty = a clean panel run, still worth logging); each miss
    needs defect_class + detail. An unknown class is a WARNING, not a block — a new
    class is exactly what the loop exists to capture (then add it to the taxonomy)."""
    problems, warnings = [], []
    if not str(record.get("episode", "")).strip():
        problems.append("record needs a non-empty 'episode'")
    misses = record.get("panel_misses")
    if not isinstance(misses, list):
        problems.append("record needs 'panel_misses' (a list; [] for a clean run)")
        misses = []
    for i, m in enumerate(misses):
        for key in ("defect_class", "detail"):
            if not str(m.get(key, "")).strip():
                problems.append(f"panel_misses[{i}] needs '{key}'")
        cls = m.get("defect_class", "")
        if cls and cls not in tax:
            warnings.append(f"'{cls}' is not in defect_classes.json — add it "
                            f"(description + status + self_review_covered)")
    return problems, warnings


def aggregate_misses(ledger: list[dict]) -> dict[str, list[dict]]:
    """defect_class -> list of {episode, beat, detail, caught_by, deterministic}."""
    by_class: dict[str, list[dict]] = defaultdict(list)
    for rec in ledger:
        for m in rec.get("panel_misses", []):
            by_class[m.get("defect_class", "?")].append({
                "episode": rec.get("episode", "?"),
                "beat": m.get("beat", ""),
                "detail": m.get("detail", ""),
                "caught_by": m.get("caught_by", ""),
                "deterministic": m.get("deterministic", False),
            })
    return by_class


def report() -> str:
    ledger = load_ledger()
    tax = load_taxonomy()
    by_class = aggregate_misses(ledger)

    n_eps = len(ledger)
    n_paneled = sum(1 for r in ledger if r.get("user_verdict") != "panel-pending")
    lines: list[str] = []
    lines.append(f"CALIBRATION REPORT — {n_eps} episodes logged, {n_paneled} with panel/user verdicts in.")
    lines.append("=" * 70)

    proposals: list[tuple[str, list[dict], dict]] = []
    for cls, misses in sorted(by_class.items(), key=lambda kv: -len(kv[1])):
        meta = tax.get(cls, {})
        status = meta.get("status", "unknown")
        covered = meta.get("self_review_covered", "unknown")
        flag = (status != "hard-gate") or (covered != "true")
        marker = "  >>> PROPOSAL CANDIDATE" if (flag and len(misses) >= PROMOTE_THRESHOLD) else ""
        lines.append(f"\n[{cls}]  misses={len(misses)}  status={status}  self_review={covered}{marker}")
        lines.append(f"    {meta.get('description', '(not in taxonomy)')}")
        for m in misses:
            det = "deterministic" if m["deterministic"] else "judgement"
            lines.append(f"    - {m['episode']} / {m['beat']} [{det}] (caught by {m['caught_by']}): {m['detail']}")
        if flag and len(misses) >= PROMOTE_THRESHOLD:
            proposals.append((cls, misses, meta))

    lines.append("\n" + "=" * 70)
    if proposals:
        lines.append(f"{len(proposals)} PROPOSAL CANDIDATE(S) — the self-review keeps missing these:")
        for cls, misses, meta in proposals:
            kind = ("DETERMINISTIC GATE" if meta.get("deterministic")
                    else "STRENGTHEN SELF-REVIEW PROMPT")
            lines.append(f"  - {cls}: {kind}  (seen {len(misses)}x)")
        lines.append("\nNext: review these, approve the ones to apply; the agent then edits the")
        lines.append("self-review role / adds the gate / updates the constitution (propose-I-approve).")
    else:
        lines.append("No proposal candidates — internal review is keeping up with the panel.")
    return "\n".join(lines)


def main(argv=None) -> int:
    """`report` (default) prints the calibration report; `record <file.json>` is the
    ledger's ONE writer — the /learn skill builds the record file after each panel
    run and appends it through the validation above."""
    import argparse
    import datetime
    import sys

    ap = argparse.ArgumentParser(description="calibration loop: report / record")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("report", help="aggregate the ledger + proposal candidates")
    rec = sub.add_parser("record", help="append one episode's record from a JSON file")
    rec.add_argument("json_file", help="record: {episode, ref?, stage?, panel_misses:[...], user_verdict?}")
    a = ap.parse_args(argv)
    if a.cmd in (None, "report"):
        print(report())
        return 0
    record = json.loads(Path(a.json_file).read_text(encoding="utf-8"))
    problems, warnings = validate_record(record, load_taxonomy())
    for w in warnings:
        print(f"WARN: {w}")
    if problems:
        for p in problems:
            print(f"BLOCK: {p}", file=sys.stderr)
        return 2
    record.setdefault("date", datetime.date.today().isoformat())
    append_record(record)
    print(f"logged '{record['episode']}': {len(record['panel_misses'])} panel miss(es) -> {LEDGER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
