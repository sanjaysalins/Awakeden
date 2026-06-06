"""Test-gate for the long-form batch drivers (stills + animation).

WHY: the Isaiah 53 pilot wasted ~$18-20 re-rendering stills and re-animating
scenes because the FULL batch was paid for BEFORE the look/motion was locked
(contact-sheet QC missed anachronisms; the frozen-painting motion made calm
scenes read dead). The rule that recovers that money:

    render 1-2 TEST scenes -> QC them FULL-RES + get user approval -> THEN
    batch the remaining ~19.

A single test still + test clip (~$1) gates a ~$25 batch.

Usage in a driver:

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _test_gate import apply_test_gate
    gate_ids, gate_stop, gate_banner = apply_test_gate(
        sys.argv, OUT, stage="stills",
        all_ids=[s["id"] for s in plan["scenes"]],
        default_test=[1, 6],
        qc_hint="Open each PNG full-size (never a contact sheet).",
    )
    for s in plan["scenes"]:
        if s["id"] not in gate_ids:
            continue
        ...  # render
    if gate_stop:
        print(gate_banner); sys.exit(0)

Flags (read from argv):
  --test a,b   override which scene ids are the test scenes
  --approved   the look IS approved -> render the full pool (persists a marker)
  --no-gate    skip the gate entirely (full pool, no test stop) — escape hatch
"""
from pathlib import Path


def _parse_ids(s):
    return [int(x) for x in str(s).replace(" ", "").split(",") if x.strip()]


def _flag_val(argv, name):
    if name in argv:
        i = argv.index(name)
        if i + 1 < len(argv):
            return argv[i + 1]
    return None


def apply_test_gate(argv, out_dir, *, stage, all_ids, default_test, qc_hint=""):
    """Return (ids_to_process: set[int], stop_after: bool, banner: str).

    - stop_after True  -> driver rendered ONLY the test scenes; print banner + exit.
    - stop_after False -> driver renders the full pool (idempotent skips test ones).
    """
    out_dir = Path(out_dir)
    all_set = set(all_ids)
    marker = out_dir / f".{stage}_look_approved"

    if "--no-gate" in argv:
        return all_set, False, ""

    test_ids = [i for i in (_parse_ids(_flag_val(argv, "--test") or "")) if i in all_set]
    if not test_ids:
        test_ids = [i for i in default_test if i in all_set] or list(default_test)

    approved = ("--approved" in argv) or marker.exists()
    if approved:
        if "--approved" in argv and not marker.exists():
            marker.write_text(f"{stage} look approved\n", encoding="utf-8")
        return all_set, False, ""

    banner = (
        "\n" + "=" * 72 + "\n"
        f"  TEST GATE [{stage}] — look NOT yet approved.\n"
        f"  Rendered ONLY test scene(s): {test_ids}.\n"
        + (f"  {qc_hint}\n" if qc_hint else "")
        + f"  QC them FULL-RES in:\n    {out_dir}\n"
        f"  If the look is right, re-run with  --approved  to render the rest.\n"
        f"  (Override the test scenes: --test a,b  |  skip the gate: --no-gate)\n"
        + "=" * 72
    )
    return set(test_ids), True, banner
