"""Shared spread-variety lint for living-sketchbook (linear full-page spread) episodes.

Adapted 2026-07-31 from `pipeline/panel_variety.py` (which checks panel
redundancy WITHIN one multi-panel comic grid) for a structurally different
case: a living-sketchbook episode is a linear SEQUENCE of full-page spreads,
not grids, so the collision scope is the WHOLE episode's spread list, not a
sub-grid.

Real defect this caught (Bronze Serpent, 2026-07-31): the user's own eye
caught s01_wide / s03_complaint / s07_horizon / s11_hearme all rendering the
same "Moses standing, staff gripped in one hand, waist-up crop, three-quarter
view, looking off to one side" composition -- 4 of 14 spreads (~30%) on one
pose. s01 and s03 survive because they carry a redeeming SECOND SUBJECT
element (the tent camp + distant family; the complaining crowd) that changes
what the eye actually reads on the page -- s07 and s11 do not (Moses alone,
no second element), so they collide with each other and needed genuinely
different blocking, not just a new background.

Each spread's still is tagged in `visual_tags.json` with three short axes
(a dict per slug, not a single string like panel_variety.py's tags -- a
linear sequence needs finer resolution since EVERY spread in an episode is
in scope, not just the 2-4 panels of one grid):
  - subject: WHAT is actually in the frame, including secondary figures
    (e.g. "moses-alone", "moses+family", "moses+crowd", "jesus-alone") --
    deliberately NOT just "which named character," because a second subject
    element is exactly what rescues an otherwise-repeated pose (see above).
  - pose: standing-staff-grip / kneeling-praying / seated-direct-address /
    action-forging / crucified-head-bowed / etc.
  - framing: wide / mid / close / extreme-close

Flags any 2+ spreads in the SAME episode sharing subject+pose+framing all
three (an exact triple match). Because `subject` folds in secondary frame
content, s01 and s03 do not collide with s07/s11 or with each other even
though all four share the same pose+framing pair -- that's the mechanism
that correctly spares s01/s03 (redeeming second element) while catching the
genuine s07/s11 duplicate (Moses alone, nothing else, twice).

GRANDFATHERING: an episode pool with no `visual_tags.json` skips the gate
entirely (WARN) -- same rule as `panel_variety.py`, for episodes built
before this existed.

This is a FLOOR, not the ceiling -- same caveat as `panel_variety.py`: a
human eye pass over the actual composited full-res stills is still required
(see `feedback-audit-stills-fullres` / living-sketchbook SKILL.md sec.8a).
The tag values themselves are an authored judgment call, not derived from
pixels -- garbage tags in, garbage check out.
"""
from __future__ import annotations

import json
from pathlib import Path


def lint(pool: Path, spreads: list[str]) -> dict:
    """Pure check. `spreads` is the ordered list of spread slugs (e.g.
    ["s01_wide", "s02_grief", ...]) making up the episode's page sequence.
    Returns {'skipped': bool, 'fails': [...], 'untagged': [...]}.
    `skipped` means no visual_tags.json (grandfathered pool) -- nothing else
    is populated in that case."""
    tags_path = pool / "visual_tags.json"
    if not tags_path.is_file():
        return {"skipped": True, "fails": [], "untagged": []}
    tags = json.loads(tags_path.read_text(encoding="utf-8"))

    fails: list[str] = []
    untagged: list[str] = []
    seen: dict[tuple, str] = {}
    for slug in spreads:
        tag = tags.get(slug)
        if tag is None:
            untagged.append(slug)
            continue
        key = (tag.get("subject"), tag.get("pose"), tag.get("framing"))
        if key in seen:
            fails.append(f"'{seen[key]}' and '{slug}' share subject+pose+framing "
                         f"(subject='{key[0]}' pose='{key[1]}' framing='{key[2]}')")
        else:
            seen[key] = slug

    return {"skipped": False, "fails": fails, "untagged": untagged}


def check(pool: Path, spreads: list[str], *, log=print) -> int:
    """Print a report; return 0 clean / 1 violations / 0 with a WARN when the
    pool is grandfathered (no visual_tags.json)."""
    r = lint(pool, spreads)
    if r["skipped"]:
        log(f"[spread-variety] no visual_tags.json in {pool.name} -- grandfathered "
            f"legacy pool, gate SKIPPED (new living-sketchbook episodes should tag "
            f"their spreads)")
        return 0
    log(f"[spread-variety] {len(spreads)} spreads scanned")
    if r["untagged"]:
        log("[spread-variety] UNTAGGED slugs (add to visual_tags.json before calling done):")
        for s in r["untagged"]:
            log(f"    {s}")
    if r["fails"]:
        log(f"[spread-variety] {len(r['fails'])} REPEATED-COMPOSITION FAIL(s):")
        for f in r["fails"]:
            log(f"  FAIL  {f}")
    else:
        log("[spread-variety] 0 repeated compositions -- every spread reads distinct.")
    return 1 if (r["fails"] or r["untagged"]) else 0
