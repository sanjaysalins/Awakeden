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

A SECOND, separate check lives below: `census()` / `check_census()`. Added
2026-08-16 after Serpent-Crusher Promised (Romans 16:20) shipped 4
serpent-centered spreads with zero exact-triple collisions between any of
them -- `lint()` above correctly found nothing wrong, yet the piece still
read as "loads of feet and snake stills" on real playback (the user's own
words). Distinct treatment does not fix monotonous VOLUME; that is a
dominance problem, not a collision problem, so it needs a different check
(see memory `living-sketchbook-subject-variety-gap`).
"""
from __future__ import annotations

import json
from pathlib import Path

DEFAULT_OBJECT_THRESHOLD = 2


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


def census(pool: Path, spreads: list[str], *, threshold: int = DEFAULT_OBJECT_THRESHOLD) -> dict:
    """Tally each spread's central OBJECT/PROP tags (visual_tags.json's per-slug
    `objects` list, e.g. ["serpent", "garden"]) across the WHOLE episode and
    flag any object anchoring the frame in more than `threshold` spreads.
    Deliberately count-based, not collision-based -- this is the check that
    catches "the same motif everywhere" even when `lint()` above finds zero
    exact subject+pose+framing duplicates (see module docstring).

    A top-level `_mandated` map ({slug: [object, ...]}) exempts specific
    occurrences the KJV text itself names (e.g. Romans 16:20's own "under
    your feet") from the tally -- the occurrence is still recorded in `tally`
    for visibility, it just never counts toward `over_threshold`.

    Untagged spreads (no `objects` key) are reported the same as `lint()`'s
    untagged check -- forcing the object to be named is the actual
    discipline, independent of whether any count trips the threshold.

    Returns {'skipped': bool, 'over_threshold': [(obj, [slugs]), ...],
    'untagged': [...], 'tally': {obj: [slugs]}}. `skipped` means no
    visual_tags.json (grandfathered pool)."""
    tags_path = pool / "visual_tags.json"
    if not tags_path.is_file():
        return {"skipped": True, "over_threshold": [], "untagged": [], "tally": {}}
    data = json.loads(tags_path.read_text(encoding="utf-8"))
    mandated = data.get("_mandated", {})

    tally: dict[str, list[str]] = {}
    untagged: list[str] = []
    for slug in spreads:
        tag = data.get(slug)
        if tag is None or "objects" not in tag:
            untagged.append(slug)
            continue
        exempt = set(mandated.get(slug, []))
        for obj in tag["objects"]:
            if obj in exempt:
                continue
            tally.setdefault(obj, []).append(slug)

    over_threshold = [(obj, slugs) for obj, slugs in tally.items() if len(slugs) > threshold]
    over_threshold.sort(key=lambda kv: -len(kv[1]))
    return {"skipped": False, "over_threshold": over_threshold, "untagged": untagged, "tally": tally}


def check_census(pool: Path, spreads: list[str], *, threshold: int = DEFAULT_OBJECT_THRESHOLD,
                  log=print) -> int:
    """Print the object-census report; return 0 clean / 1 only on untagged
    spreads. A dominance finding is printed as WARN and never blocks the exit
    code on its own -- a recurring object can be the RIGHT call (e.g. this
    piece's own crushed serpent, staged 4 genuinely distinct ways) as easily
    as it can be the lazy default this gate exists to surface; the point is
    making a human look and decide, not auto-rejecting repetition outright."""
    r = census(pool, spreads, threshold=threshold)
    if r["skipped"]:
        log(f"[object-census] no visual_tags.json in {pool.name} -- grandfathered "
            f"legacy pool, gate SKIPPED (new episodes should tag every slug's "
            f"central objects, at planning time, before rendering)")
        return 0
    log(f"[object-census] {len(spreads)} spreads scanned, threshold={threshold}")
    if r["untagged"]:
        log("[object-census] UNTAGGED slugs (add an 'objects' list before rendering):")
        for s in r["untagged"]:
            log(f"    {s}")
    if r["over_threshold"]:
        log(f"[object-census] {len(r['over_threshold'])} object(s) over the dominance "
            f"threshold (WARN, not blocking):")
        for obj, slugs in r["over_threshold"]:
            log(f"  WARN  '{obj}' is the central object in {len(slugs)} spreads "
                f"(> {threshold}): {', '.join(slugs)}")
        log("        before rendering: diversify HOW it reads (angle/distance/company/"
            "absence) or confirm each occurrence is genuinely distinct, per "
            "living-sketchbook SKILL.md sec.3 'textual refrain != visual refrain'")
    else:
        log("[object-census] no object dominates the piece -- subject volume looks healthy.")
    return 1 if r["untagged"] else 0
