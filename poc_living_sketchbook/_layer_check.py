#!/usr/bin/env python
"""_layer_check.py -- the $0 layer-completeness gate. Born from the Day of
Atonement retrospective: all 14 verse-card spreads sat as blank paper margins
for most of the build ("REAL SCOPE DISCOVERY: none of the 14 verse-card
spreads have any real lettering yet") -- discovered only well after the
visual + animation passes were already done, forcing a whole separate
late-game rollout. This gate reads the episode's own PLAN and device table
and FAILs any verse-card spread that has no real lettering entry, so the gap
is caught the moment a spread is planned, not after the film is assembled
(memory `day-of-atonement-retro-learnings` fix #4).

Reads:
  <episode-dir>/_PLAN.md          -- section-2 spread table (# | ... | Type | ...)
  <episode-dir>/_spread_table.py  -- SPREADS list, gives the # -> name mapping
                                      (the PLAN only has row numbers; _devices.py
                                      keys are the real spread names)
  <episode-dir>/_devices.py       -- VERSE_CARDS, SPECIAL_CARDS, and the optional
                                      EXTERNAL_LETTERING set (spreads whose real
                                      lettering is built by a standalone script
                                      outside the normal card dispatch -- e.g.
                                      Day of Atonement's spread55_isaiah536, built
                                      by _s3_thread_leaf_54_55.py, not a card dict)

A VC-typed spread passes if:
  - its name is in EXTERNAL_LETTERING, or
  - its name is in VERSE_CARDS with a non-empty "lines" list, or
  - its name is in SPECIAL_CARDS with a "kind" key present
An entry carrying "deferred": True downgrades a missing/empty entry to WARN
(an explicit, logged decision -- not a silent gap).

Usage:
    python _layer_check.py --episode-dir <dir>

Exit code 1 on any FAIL.
"""
from __future__ import annotations
import argparse
import importlib.util
import re
import sys
from pathlib import Path


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(mod)
    return mod


def parse_plan_table(plan_path: Path) -> list[dict]:
    """Section-2 spread table: '| # | Start-End (s) | Dur | Beat | Type | Shows | Assets | Device |'.
    Returns [{"num": int, "type": str}, ...] for every real data row."""
    lines = plan_path.read_text(encoding="utf-8").splitlines()
    header_idx = None
    cols = []
    for i, ln in enumerate(lines):
        if ln.strip().startswith("|") and "Type" in ln and "#" in ln:
            cols = [c.strip() for c in ln.strip().strip("|").split("|")]
            if "Type" in cols:
                header_idx = i
                break
    if header_idx is None:
        sys.exit(f"[FATAL] no spread table found in {plan_path} (looked for a header row with '#' and 'Type')")
    type_col = cols.index("Type")
    num_col = cols.index("#")

    rows = []
    for ln in lines[header_idx + 2:]:  # skip header + the '|---|---|' separator
        if not ln.strip().startswith("|"):
            break
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) <= max(type_col, num_col):
            continue
        m = re.match(r"\d+", cells[num_col])
        if not m:
            continue
        rows.append({"num": int(m.group()), "type": cells[type_col].strip("*")})
    return rows


def card_status(name: str, devices_mod) -> tuple[str, str]:
    """Returns (status, detail): status in {"ok", "deferred", "missing"}."""
    external = getattr(devices_mod, "EXTERNAL_LETTERING", set())
    if name in external:
        return "ok", "built via a standalone script (EXTERNAL_LETTERING)"

    vc = getattr(devices_mod, "VERSE_CARDS", {})
    if name in vc:
        entry = vc[name]
        if entry.get("deferred"):
            return "deferred", "VERSE_CARDS entry present but marked deferred:True"
        if entry.get("lines"):
            return "ok", f"VERSE_CARDS combo={entry.get('combo', '?')}, {len(entry['lines'])} line(s)"
        return "missing", "VERSE_CARDS entry present but 'lines' is empty/absent"

    sc = getattr(devices_mod, "SPECIAL_CARDS", {})
    if name in sc:
        entry = sc[name]
        if entry.get("deferred"):
            return "deferred", "SPECIAL_CARDS entry present but marked deferred:True"
        if entry.get("kind"):
            return "ok", f"SPECIAL_CARDS kind={entry['kind']}"
        return "missing", "SPECIAL_CARDS entry present but 'kind' is absent"

    return "missing", "no VERSE_CARDS/SPECIAL_CARDS/EXTERNAL_LETTERING entry at all"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode-dir", required=True, type=Path)
    args = ap.parse_args()
    ep = args.episode_dir

    plan_path = ep / "_PLAN.md"
    spread_table_path = ep / "_spread_table.py"
    devices_path = ep / "_devices.py"
    for p in (plan_path, spread_table_path, devices_path):
        if not p.exists():
            sys.exit(f"[FATAL] missing {p}")

    spread_mod = load_module(spread_table_path)
    devices_mod = load_module(devices_path)
    by_num = spread_mod.by_num  # num -> (name, beat, start, end)

    rows = parse_plan_table(plan_path)
    vc_rows = [r for r in rows if r["type"] == "VC"]
    print(f"[layer_check] {len(rows)} plan rows, {len(vc_rows)} Type=VC")

    fails, warns = [], []
    for r in vc_rows:
        num = r["num"]
        if num not in by_num:
            fails.append((num, "?", f"row #{num} has no matching entry in _spread_table.py"))
            continue
        name = by_num[num][0]
        status, detail = card_status(name, devices_mod)
        if status == "missing":
            fails.append((num, name, detail))
        elif status == "deferred":
            warns.append((num, name, detail))

    for num, name, detail in fails:
        print(f"  [FAIL] #{num:<3} {name:<32} {detail}")
    for num, name, detail in warns:
        print(f"  [WARN] #{num:<3} {name:<32} {detail}")

    print(f"[layer_check] {len(fails)} FAIL, {len(warns)} WARN "
          f"({len(vc_rows) - len(fails) - len(warns)}/{len(vc_rows)} VC spreads have real lettering)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
