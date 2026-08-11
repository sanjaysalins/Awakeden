"""Pure-code commission-plan guards — no LLM call.

Encodes failure modes #2 and the cost-discipline rule from this week's POC
work:

  - `assert_no_alignment_risk` — a device concept that asked the image model
    to generate TWO SEPARATE images meant to spatially align with each other
    (e.g. two vignettes on two different "pages" landing on the same spot)
    never once worked across 3 real attempts. The fix that DID work (proven:
    `same_fire`'s night/dawn relight, see
    `drawing_office/primitives/relight.py`) was always ONE generation,
    manipulated by code, never two generations hoping to match. This function
    is defense in depth: (a) a hard check that any registry card describing
    itself declares `generation_alignment == "forbidden"` (mirrors the check
    the registry module itself should also make), and (b) a heuristic scan of
    a commission's own `plate_bill` for language that smells like the banned
    pattern.

  - `assert_motion_budget_ok` — "motion only where it's the meaning": a
    commission must not request more paid animated inserts than the chosen
    device's registry card allows.

Field names below (`chosen_device.registry_name`, `plate_bill`,
`derived_views`, `paid_inserts`) are taken from the real commission at
`drawing_office/episodes/two_goats/commission.json`.
"""
from __future__ import annotations

import re

# Loose heuristic: "same/matching/aligned/identical" followed within a short
# span by "position/spot/place/location". Natural language is fuzzy, so this
# is a WARN-only heuristic, not a hard block.
_ALIGNMENT_RISK_RE = re.compile(
    r"\b(same|matching|aligned|identical)\b[^.]{0,40}\b(position|spot|place|location)\b",
    re.IGNORECASE,
)


def assert_no_alignment_risk(commission: dict, registry_card: dict | None = None) -> dict:
    """Two checks against the proven "two generations must align" failure:

    1. HARD BLOCK (raises ValueError): if `registry_card` is provided, its
       `generation_alignment` field must literally equal the string
       "forbidden". This mirrors the check the registry module itself should
       make — a device card that doesn't explicitly forbid the alignment
       pattern is not safe to commission from.
    2. SOFT WARNING (returned, not raised): scans `commission["plate_bill"]`
       for 2+ plates whose `must_contain`/`label` text describes needing the
       "same"/"matching"/"aligned"/"identical" position/spot as another plate,
       with no intervening `derived_views` step (i.e. no code-only step
       reducing them back to one generation). This is a heuristic catch, not
       a hard block, since natural language is fuzzy.

    Returns {"ok": bool, "warnings": [...]}. Despite the `assert_` name (kept
    for symmetry with `assert_prompt_ok`/`assert_motion_budget_ok`), only
    condition 1 raises; condition 2 is advisory."""
    warnings: list[str] = []

    if registry_card is not None:
        alignment = registry_card.get("generation_alignment")
        if alignment != "forbidden":
            raise ValueError(
                "registry_card.generation_alignment must be the literal string "
                "'forbidden' -- the two-separate-generations-must-spatially-"
                f"align pattern failed across 3 real attempts this week; got "
                f"{alignment!r} for device "
                f"{commission.get('chosen_device', {}).get('registry_name', '?')!r}. "
                "Fix the registry card before this device can be commissioned."
            )

    plate_bill = commission.get("plate_bill", []) or []
    risky_plate_ids: list[str] = []
    for plate in plate_bill:
        text = f"{plate.get('must_contain', '')} {plate.get('label', '')}".lower()
        if _ALIGNMENT_RISK_RE.search(text):
            risky_plate_ids.append(plate.get("id", "?"))

    if len(risky_plate_ids) >= 2:
        derived_from = {dv.get("from") for dv in (commission.get("derived_views", []) or [])}
        # An intervening derived_view/primitive step defuses the risk when it
        # re-derives one of the flagged plates by CODE rather than asking a
        # second independent generation to line up with it.
        has_intervening_step = any(pid in derived_from for pid in risky_plate_ids)
        if not has_intervening_step:
            warnings.append(
                f"plates {risky_plate_ids} are each described with 'same/matching/"
                "aligned/identical position' language and no derived_view/primitive "
                "step reduces them to one generation -- this is the exact pattern "
                "that failed across 3 real attempts (two separate generations "
                "hoping to spatially align). Consider one generation + a code-only "
                "split (see primitives/relight.py's relight_split, proven on "
                "same_fire) instead."
            )

    return {"ok": len(warnings) == 0, "warnings": warnings}


def assert_motion_budget_ok(commission: dict, registry_card: dict) -> None:
    """Cost discipline, structurally enforced: raise ValueError if the
    commission requests more paid animated inserts (`commission["paid_inserts"]`)
    than the chosen device's registry card allows
    (`registry_card["motion_slots"]["max"]`)."""
    paid_inserts = commission.get("paid_inserts", []) or []
    requested = len(paid_inserts)

    motion_slots = (registry_card or {}).get("motion_slots", {}) or {}
    max_allowed = motion_slots.get("max")
    if max_allowed is None:
        raise ValueError(
            "registry_card has no motion_slots.max -- cannot verify the motion "
            "budget for device "
            f"{commission.get('chosen_device', {}).get('registry_name', '?')!r}; "
            "fix the registry card before commissioning."
        )

    if requested > max_allowed:
        raise ValueError(
            f"commission requests {requested} paid animated insert(s) "
            f"({[pi.get('id', '?') for pi in paid_inserts]}) but device "
            f"{commission.get('chosen_device', {}).get('registry_name', '?')!r}'s "
            f"registry card allows a max of {max_allowed} motion_slots -- "
            "motion only where it's the meaning."
        )


if __name__ == "__main__":
    import json
    from pathlib import Path

    all_ok = True

    # --- alignment: hard-block case (should PASS: generation_alignment == "forbidden") ---
    good_registry_card = {"generation_alignment": "forbidden", "motion_slots": {"max": 2}}
    commission_simple = {
        "chosen_device": {"registry_name": "the_undivided"},
        "plate_bill": [{"id": "P1", "label": "veil"}, {"id": "P2", "label": "two_goats"}],
        "derived_views": [],
        "paid_inserts": [{"id": "InsertA"}, {"id": "InsertB"}],
    }
    try:
        result = assert_no_alignment_risk(commission_simple, good_registry_card)
        ok = result["ok"] is True
        print(f"[{'PASS' if ok else 'FAIL'}] alignment hard-check, registry_card forbidden -> no raise, ok={result['ok']}")
        all_ok &= ok
    except ValueError as e:
        print(f"[FAIL] alignment hard-check unexpectedly raised: {e}")
        all_ok = False

    # --- alignment: hard-block case (should FAIL: generation_alignment NOT "forbidden") ---
    bad_registry_card = {"generation_alignment": "allowed", "motion_slots": {"max": 2}}
    try:
        assert_no_alignment_risk(commission_simple, bad_registry_card)
        print("[FAIL] alignment hard-check did NOT raise for generation_alignment='allowed' -- BUG")
        all_ok = False
    except ValueError as e:
        print(f"[PASS] alignment hard-check raised as expected: {e}")

    # --- alignment: heuristic warning case (should WARN: two plates, same-position language, no derived_view) ---
    commission_risky = {
        "chosen_device": {"registry_name": "fake_two_page_device"},
        "plate_bill": [
            {"id": "PA", "label": "left vignette", "must_contain": "must land in the same spot as PB"},
            {"id": "PB", "label": "right vignette", "must_contain": "must occupy the identical position as PA"},
        ],
        "derived_views": [],
        "paid_inserts": [],
    }
    result = assert_no_alignment_risk(commission_risky, None)
    ok = result["ok"] is False and len(result["warnings"]) >= 1
    print(f"[{'PASS' if ok else 'FAIL'}] alignment heuristic scan flags risky plate pair: ok={result['ok']}, warnings={result['warnings']}")
    all_ok &= ok

    # --- alignment: heuristic case that should NOT warn (single plate, no risky language) ---
    commission_safe = {
        "chosen_device": {"registry_name": "fine_device"},
        "plate_bill": [{"id": "P1", "label": "a shepherd under a tree"}],
        "derived_views": [],
        "paid_inserts": [],
    }
    result = assert_no_alignment_risk(commission_safe, None)
    ok = result["ok"] is True and result["warnings"] == []
    print(f"[{'PASS' if ok else 'FAIL'}] alignment heuristic scan silent on safe commission: ok={result['ok']}")
    all_ok &= ok

    # --- motion budget: should PASS (2 requested, max 2) ---
    try:
        assert_motion_budget_ok(commission_simple, good_registry_card)
        print("[PASS] motion budget ok (2 requested <= max 2), no raise")
    except ValueError as e:
        print(f"[FAIL] motion budget unexpectedly raised: {e}")
        all_ok = False

    # --- motion budget: should FAIL (2 requested, max 1) ---
    tight_registry_card = {"generation_alignment": "forbidden", "motion_slots": {"max": 1}}
    try:
        assert_motion_budget_ok(commission_simple, tight_registry_card)
        print("[FAIL] motion budget did NOT raise for 2 requested > max 1 -- BUG")
        all_ok = False
    except ValueError as e:
        print(f"[PASS] motion budget raised as expected: {e}")

    # --- real commission.json integration check ---
    real_path = Path(__file__).resolve().parents[1] / "episodes" / "two_goats" / "commission.json"
    if real_path.exists():
        real_commission = json.loads(real_path.read_text(encoding="utf-8"))
        # Simulated registry card for "the_undivided" -- the real card doesn't
        # exist yet (registry/ is empty), but its own commission.json declares
        # this exact policy in risk_reconciliation.generation_alignment prose,
        # so a matching real card is exactly what's expected to be authored.
        the_undivided_card = {"generation_alignment": "forbidden", "motion_slots": {"max": 2}}
        result = assert_no_alignment_risk(real_commission, the_undivided_card)
        print(f"[REAL] two_goats commission.json alignment check: ok={result['ok']}, warnings={result['warnings']}")
        try:
            assert_motion_budget_ok(real_commission, the_undivided_card)
            print(f"[REAL] two_goats commission.json motion budget: {len(real_commission.get('paid_inserts', []))} requested <= 2 max -- no raise (correct)")
        except ValueError as e:
            print(f"[REAL] two_goats commission.json motion budget raised: {e}")
    else:
        print(f"[SKIP] real commission.json not found at {real_path}")

    print()
    print("ALL TEST CASES PASSED" if all_ok else "SOME TEST CASES FAILED")
