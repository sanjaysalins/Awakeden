"""payoff_ledger.py -- the hook-loop payoff gate, adapted for this project's
TIMED-LINE narration format.

Sister-project origin: ArkAIology's /payoff-ledger skill
(C:\\Users\\sanjay\\PycharmProjects\\ArkAIology\\.claude\\skills\\payoff-ledger\\SKILL.md,
implementation at episode-pipeline/scripts/payoff_ledger.py). Same judgment:
the hook opens curiosity loops; the body must pay each one off in words the
narration ACTUALLY says, and the ending must land a real verdict, not just
stop.

ArkAIology keys everything to numbered "shots" in a script.json. This
project's narrations (poc_living_sketchbook/<slug>/audio/timing.json) are a
flat sequence of TIMED LINES -- each line has a `name` ("l1", "l2", ...), a
`start`/`end` in seconds, and a `text` -- there is no shot numbering. So the
ledger and validator below are re-keyed to LINE NAMES, and "comes after" is
defined by a line's `start` TIME rather than an integer index. Re-implemented
from scratch for that reason, not copy-pasted -- the two schemas don't overlay
cleanly (there's no "hook_shots max" concept here, just named lines).

PAYOFF_LEDGER.json schema (hand-authored, the judgment pass):
{
  "slug": "<episode slug>",
  "hook_lines": ["l1", "l2", "l3"],
  "loops": [
    {"id": "L1", "opened_line": "l1",
     "loop": "<the curiosity gap, in plain words>",
     "payoff_line": "l9",
     "payoff_phrase": "<VERBATIM substring of payoff_line's text>",
     "status": "PAID | PARTIAL | UNPAID",
     "note": "<required for PARTIAL: what's missing + the creator call>"}
  ],
  "ending": {"verdict_line": "l9", "verdict_phrase": "<verbatim substring>"}
}

What the validator enforces (deterministic, fail-closed):
  1. payoff_phrase is a VERBATIM substring of the claimed payoff_line's text
     (whitespace-squeezed, case-sensitive -- "verbatim" means verbatim).
  2. payoff_line comes chronologically AFTER opened_line (by start time) --
     a loop "paid" before it's even opened isn't a payoff.
  3. no loop is UNPAID (fail); PARTIAL is allowed only with a non-empty note.
  4. the ending verdict_phrase is a verbatim substring of verdict_line's text,
     AND at least one loop pays off in the narration's last 3 lines (the
     ending calls back, it doesn't just stop -- ports ArkAIology's
     anti-abrupt-ending check to line-space).

Usage:
    python payoff_ledger.py <timing.json> <PAYOFF_LEDGER.json>
    python payoff_ledger.py --selftest <timing.json>

Exit codes: 0 = PASS, 1 = FAIL (a claim didn't hold up / selftest caught a
bug), 2 = usage error / missing file.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path


def squeeze(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def load_lines(timing_path: Path) -> dict:
    data = json.loads(timing_path.read_text(encoding="utf-8-sig"))
    lines = {ln["name"]: ln for ln in data["lines"]}
    if not lines:
        raise ValueError(f"{timing_path}: no lines found")
    return lines


def check_ledger(lines: dict, ledger: dict):
    """Pure function: (lines-by-name, ledger dict) -> (rows, fails, warns, ending_info).
    No file I/O -- kept separate from run() so the self-test can call it
    directly on planted-bad data without writing temp files."""
    fails: list[str] = []
    warns: list[str] = []
    rows: list[dict] = []

    names_by_time = sorted(lines, key=lambda n: lines[n]["start"])
    last3 = names_by_time[-3:] if len(names_by_time) >= 3 else names_by_time[:]

    for lp in ledger.get("loops", []):
        lid = lp.get("id", "?")
        opened = lp.get("opened_line")
        payoff = lp.get("payoff_line")
        phrase = lp.get("payoff_phrase", "")
        status = lp.get("status")

        if opened not in lines:
            fails.append(f"{lid}: opened_line {opened!r} not found in timing.json")
            rows.append({**lp, "ok": False})
            continue
        if payoff not in lines:
            fails.append(f"{lid}: payoff_line {payoff!r} not found in timing.json")
            rows.append({**lp, "ok": False})
            continue

        payoff_text = lines[payoff]["text"]
        ok_phrase = squeeze(phrase) in squeeze(payoff_text)
        ok_after = lines[payoff]["start"] > lines[opened]["start"]
        ok_status = status in ("PAID", "PARTIAL")  # UNPAID (or missing) fails
        ok_note = status != "PARTIAL" or bool(str(lp.get("note", "")).strip())

        if not ok_phrase:
            fails.append(
                f"{lid}: payoff_phrase not verbatim in {payoff} "
                f"(text={payoff_text!r}): claimed {phrase!r}"
            )
        if not ok_after:
            fails.append(
                f"{lid}: payoff_line {payoff} (start={lines[payoff]['start']}) does not "
                f"come after opened_line {opened} (start={lines[opened]['start']})"
            )
        if not ok_status:
            fails.append(f"{lid}: status={status!r} (UNPAID or missing) -- loop not paid: {lp.get('loop', '')!r}")
        if status == "PARTIAL":
            if ok_note:
                warns.append(f"{lid}: PARTIAL -- {lp.get('note')}")
            else:
                fails.append(f"{lid}: status PARTIAL but no note explaining what's missing / the creator call")

        rows.append({**lp, "ok": ok_phrase and ok_after and ok_status and ok_note})

    ending = ledger.get("ending", {})
    v_line = ending.get("verdict_line")
    v_phrase = ending.get("verdict_phrase", "")
    if v_line not in lines:
        fails.append(f"ending: verdict_line {v_line!r} not found in timing.json")
        verdict_ok = False
    else:
        verdict_ok = squeeze(v_phrase) in squeeze(lines[v_line]["text"])
        if not verdict_ok:
            fails.append(
                f"ending: verdict_phrase not verbatim in {v_line} "
                f"(text={lines[v_line]['text']!r}): claimed {v_phrase!r}"
            )

    callback_ok = any(lp.get("payoff_line") in last3 for lp in ledger.get("loops", []))
    if not callback_ok:
        fails.append(
            f"ending: no loop pays off in the last lines {last3} -- "
            f"the ending doesn't call back, it just stops"
        )

    einfo = {
        "last3": last3, "callback_ok": callback_ok, "verdict_ok": verdict_ok,
        "verdict_line": v_line, "verdict_phrase": v_phrase,
    }
    return rows, fails, warns, einfo


def run(timing_path: Path, ledger_path: Path) -> int:
    if not timing_path.is_file():
        print(f"[FAIL] no timing.json at {timing_path}", file=sys.stderr)
        return 2
    if not ledger_path.is_file():
        print(
            f"[FAIL] no ledger at {ledger_path} -- author it (the judgment pass: "
            f"walk the hook lines, list every curiosity loop, find where the "
            f"narration actually pays each off) before this gate can run",
            file=sys.stderr,
        )
        return 2

    lines = load_lines(timing_path)
    ledger = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    rows, fails, warns, e = check_ledger(lines, ledger)

    n_paid = sum(1 for r in rows if r["ok"] and r.get("status") == "PAID")
    n_partial = sum(1 for r in rows if r["ok"] and r.get("status") == "PARTIAL")
    verdict = "GATE FAIL" if fails else "GATE PASS"

    print(
        f"\n=== {ledger.get('slug', ledger_path.stem)}: {verdict} -- "
        f"{n_paid}/{len(rows)} PAID"
        + (f", {n_partial} PARTIAL" if n_partial else "")
        + " ==="
    )
    for r in rows:
        badge = "OK" if r["ok"] else "FAIL"
        print(
            f"  [{badge}] {r.get('id')}: {r.get('opened_line')} -> {r.get('payoff_line')} "
            f"({r.get('status')}) -- {r.get('loop')}"
        )
    print(
        f"  ending: callback in last lines {e['last3']}: "
        f"{'OK' if e['callback_ok'] else 'NO'}; "
        f"verdict spoken in {e['verdict_line']}: {'OK' if e['verdict_ok'] else 'NO'} "
        f"-- {e['verdict_phrase']!r}"
    )
    for f in fails:
        print(f"  X {f}")
    for w in warns:
        print(f"  ! {w}")

    if fails:
        print(f"\n[FAIL] {len(fails)} claim(s) failed -- see X lines above.")
        return 1
    print(
        "\n[PASS] every payoff_phrase verbatim + chronological, no UNPAID loops, "
        "ending calls back and speaks its verdict."
    )
    return 0


def selftest(timing_path: Path) -> int:
    """Proves fail-closed behavior against REAL narration text (no fixtures):
    builds a minimal ledger from timing.json that should legitimately PASS,
    then plants ONE fake payoff_phrase that is NOT actually spoken anywhere,
    and confirms the validator rejects it (naming the exact claim). If the
    good ledger doesn't pass, or the bad one isn't caught, this reports
    SELFTEST FAIL and returns 1 -- proof, not assertion."""
    if not timing_path.is_file():
        print(f"[FAIL] no timing.json at {timing_path}", file=sys.stderr)
        return 2

    lines = load_lines(timing_path)
    names_by_time = sorted(lines, key=lambda n: lines[n]["start"])
    first, last = names_by_time[0], names_by_time[-1]
    real_closing_words = squeeze(lines[last]["text"])[:20]

    good_ledger = {
        "slug": "selftest-good",
        "hook_lines": [first],
        "loops": [
            {
                "id": "T1", "opened_line": first,
                "loop": "self-test loop built from real text",
                "payoff_line": last,
                "payoff_phrase": real_closing_words,
                "status": "PAID",
            }
        ],
        "ending": {"verdict_line": last, "verdict_phrase": real_closing_words},
    }
    bad_ledger = copy.deepcopy(good_ledger)
    PLANTED_FAKE = "Apollo 11 lands on the Moon"
    bad_ledger["loops"][0]["payoff_phrase"] = PLANTED_FAKE

    print(f"--- selftest against real file: {timing_path} ---")
    print("[1] GOOD ledger (payoff_phrase copied verbatim from the real last line) should PASS:")
    _, fails_g, _, _ = check_ledger(lines, good_ledger)
    good_passed = not fails_g
    print("    PASS" if good_passed else f"    UNEXPECTED FAIL: {fails_g}")

    print(f"\n[2] BAD ledger (payoff_phrase planted as {PLANTED_FAKE!r}, never spoken) should FAIL:")
    _, fails_b, _, _ = check_ledger(lines, bad_ledger)
    caught = any(PLANTED_FAKE in f for f in fails_b)
    for f in fails_b:
        print(f"    X {f}")
    print("    CAUGHT the planted error" if caught else "    DID NOT CATCH the planted error -- validator is broken")

    ok = good_passed and caught
    print(
        f"\n[SELFTEST {'PASS' if ok else 'FAIL'}] fail-closed behavior "
        f"{'confirmed' if ok else 'BROKEN'}: real ledger passed={good_passed}, "
        f"planted fake payoff caught={caught}"
    )
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("timing_json", type=Path, help="path to a timing.json (name/start/end/text lines)")
    ap.add_argument("ledger_json", type=Path, nargs="?", help="path to PAYOFF_LEDGER.json")
    ap.add_argument(
        "--selftest", action="store_true",
        help="prove fail-closed behavior with a planted fake payoff against the given timing.json; ledger_json not required",
    )
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.timing_json)
    if args.ledger_json is None:
        print("usage: payoff_ledger.py <timing.json> <PAYOFF_LEDGER.json>", file=sys.stderr)
        return 2
    return run(args.timing_json, args.ledger_json)


if __name__ == "__main__":
    sys.exit(main())
