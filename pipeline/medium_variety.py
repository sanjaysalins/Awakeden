"""Deterministic guardrail for medium selection (MEDIUM_SELECTION.md sec.4
stage 2) -- the Stationer's guardrail. Same family as style_variety.py
(technique-variant caps), spread_variety.py, and panel_variety.py, applied to
a NEW axis: which spreads get rendered as a different physical paper OBJECT
(a survey plate, an archive card, a ledger leaf, a scroll fragment, a night
sheet) instead of the baseline sketchbook page.

Reuses `style_variety.lint()` for every check the two axes share (the
manifest field-name mirroring in medium_manifest.json makes this free: an
unknown id, a non-`production_approved` status, an over-budget or
under-spaced or over-capped or `avoid_on`/gold-leaf-conflict proposal are all
already caught). This module then adds six medium-specific checks the
technique-variant axis never needed, because a medium swap is a bigger
perceptual and doctrinal event than a technique shift:

  1. figure clash        -- an artifact_only medium on a spread with a named figure
  2. Jesus fail-closed    -- any non-home medium on a Jesus spread, without an explicit override
  3. landing runway       -- the landing spread + the 2 spreads before it stay home
  4. cross-axis exclusivity + a combined 30% ceiling with the technique-variant axis
  5. motion floor         -- every medium spread still needs a real generative clip planned
  6. text-overlay declaration (WARN) -- a high-text-risk medium needs a named overlay plan or an explicit "blank"

Fails CLOSED, same "floor, not ceiling" discipline as every other variety
gate in this repo. A human eye-gate still runs after (STYLE_SELECTION.md's
existing stage 3 -- nothing new needed there).
"""
from __future__ import annotations

from pathlib import Path

from pipeline import style_variety as SV
from pipeline.medium_registry import HOME, MANIFEST_PATH, load_manifest  # noqa: F401 -- re-exported

_HIGH_TEXT_RISK = ("high", "medium-high")


def medium_budget(episode_len: int) -> tuple[int, int]:
    """(max_medium_spreads, min_spread_gap). Stricter than
    style_variety.default_budget() (3/gap-4 at 14 spreads -> 10/gap-8 at 68)
    because a medium switch -- a different physical object on the page -- is
    a bigger perceptual event than a technique/mood shift. Episodes of 14
    spreads or fewer get a flat (2, 5); 68+ spreads get a flat (5, 10);
    anything between is linear-interpolated. (The interpolation formula's
    own floor never actually triggers below 14 spreads -- the flat branch
    always returns first -- so a 1-spread episode still gets (2, 5), not a
    smaller number.)"""
    if episode_len <= 14:
        return 2, 5
    if episode_len >= 68:
        return 5, 10
    frac = (episode_len - 14) / (68 - 14)
    max_v = round(2 + frac * (5 - 2))
    gap = round(5 + frac * (10 - 5))
    return max_v, gap


def lint(
    proposal: dict,
    manifest: dict,
    *,
    beat_types: dict | None = None,
    figures: dict | None = None,
    landing_slug: str | None = None,
    variant_proposal: dict | None = None,
    motion_plan: dict | None = None,
    overlay_plan: dict | None = None,
    allow_jesus_distant: set | None = None,
    max_variants: int | None = None,
    min_gap: int | None = None,
) -> dict:
    """`proposal`: ORDERED {slug: medium_id_or_None}, same shape/order
    contract as style_variety.lint()'s proposal.

    `figures`: optional {slug: [figure_name, ...]} -- named figures present
        on that spread (the plan table already knows this; it drives
        REF_MAP chaining). Omit to skip the figure-clash / Jesus checks
        (degrades gracefully, same grandfathering philosophy as every other
        optional check in this repo).
    `landing_slug`: the landing spread's slug. That slug plus the two
        immediately before it (by proposal ORDER) form the landing runway.
    `variant_proposal`: the SIBLING technique-variant proposal
        (style_select.py's shape) for the cross-axis exclusivity + combined-
        ceiling check. Omit if this episode isn't also running the variant
        axis this pass.
    `motion_plan`: optional {slug: bool} -- True/False whether a real
        generative clip is planned for that spread. Only slugs present in
        this dict are checked (the motion floor).
    `overlay_plan`: optional {slug: "declared" | "blank"} -- whether the
        plan named a lettering-overlay device, or explicitly chose blank.
        A high-text-risk medium spread absent from this dict WARNs.
    `allow_jesus_distant`: optional set of slugs where a human has
        explicitly overridden the Jesus fail-closed check.

    Returns {'fails': [...], 'warns': [...], 'medium_count': int,
    'by_medium': {id: [slugs]}, 'budget_max': int, 'budget_gap': int}.
    """
    slugs = list(proposal.keys())
    episode_len = len(slugs)
    budget_max, budget_gap = medium_budget(episode_len)
    if max_variants is None:
        max_variants = budget_max
    if min_gap is None:
        min_gap = budget_gap

    # 0. HOME (md_sketch) can never be proposed as a tipped-in medium --
    # absence = home, by design. Strip it out BEFORE handing off to the
    # shared SV.lint() pass: HOME's own manifest entry carries no real caps
    # (it's never meant to be capped), so letting it reach the shared cap
    # arithmetic is a crash waiting to happen, not just a wrong answer.
    home_fails = [f"{slug}: '{HOME}' is the home medium and can never be "
                  f"proposed as a tipped-in medium (absence = home, by design)"
                  for slug, mid in proposal.items() if mid == HOME]
    sanitized = {s: (None if v == HOME else v) for s, v in proposal.items()}

    shared = SV.lint(sanitized, manifest, beat_types=beat_types,
                      max_variants=max_variants, min_gap=min_gap)
    fails: list[str] = home_fails + list(shared["fails"])
    warns: list[str] = list(shared["warns"])
    by_medium: dict[str, list[str]] = shared["by_variant"]

    figures = figures or {}
    motion_plan = motion_plan or {}
    overlay_plan = overlay_plan or {}
    allow_jesus_distant = allow_jesus_distant or set()
    variant_proposal = variant_proposal or {}

    landing_window: set[str] = set()
    if landing_slug and landing_slug in slugs:
        li = slugs.index(landing_slug)
        landing_window = set(slugs[max(0, li - 2): li + 1])

    for slug in slugs:
        mid = proposal[slug]
        if mid is None or mid == HOME:
            continue  # HOME already reported above; None is baseline
        entry = manifest.get(mid)
        if entry is None or entry.get("status") != "production_approved":
            continue  # already reported by the shared SV.lint() pass above

        figs = figures.get(slug) or []  # a present-but-null value must not crash
        figure_mode = entry.get("figure_mode")

        # 1. figure clash
        if figure_mode == "artifact_only" and figs:
            fails.append(f"{slug}: artifact_only medium '{mid}' proposed on a "
                         f"spread with named figure(s) {figs}")

        # 2. Jesus fail-closed -- substring match, not exact: real plan
        # tables annotate figures as e.g. "Jesus (small, teaching-by-night
        # register)", not a bare "Jesus". The override is legal ONLY for a
        # distant_marks medium (MEDIUM_SELECTION.md sec.1/sec.4) -- a
        # figure_forward medium can never be silently rescued, no matter
        # what's in allow_jesus_distant.
        has_jesus = any("jesus" in f.lower() for f in figs)
        override_ok = slug in allow_jesus_distant and figure_mode == "distant_marks"
        if has_jesus and not override_ok:
            fails.append(f"{slug}: non-home medium '{mid}' (figure_mode="
                         f"{figure_mode}) proposed on a Jesus spread -- needs "
                         f"an explicit allow_jesus_distant override on a "
                         f"distant_marks medium (human decision, never a "
                         f"default, and never on a readable-face medium)")

        # 3. landing runway
        if slug in landing_window:
            fails.append(f"{slug}: medium '{mid}' proposed inside the landing "
                         f"runway (the landing spread + the 2 before it must "
                         f"stay on the home medium)")

        # 5. motion floor
        if motion_plan.get(slug) is False:
            fails.append(f"{slug}: medium '{mid}' has no generative clip "
                         f"planned -- every medium spread needs real animated "
                         f"motion, never a static camera hold over the plate")

        # 6. text-overlay declaration (WARN only)
        if entry.get("text_drift_risk") in _HIGH_TEXT_RISK and slug not in overlay_plan:
            warns.append(f"{slug}: high-text-risk medium '{mid}' has no "
                         f"declared lettering-overlay plan (or an explicit "
                         f"'blank') -- silence is how baked text sneaks in")

    # 4. cross-axis exclusivity + combined ceiling
    medium_slugs = {s for s, v in sanitized.items() if v}
    variant_slugs = {s for s, v in variant_proposal.items() if v}
    for slug in sorted(medium_slugs & variant_slugs):
        fails.append(f"{slug}: proposed on BOTH the medium and technique-"
                     f"variant axes -- a spread may carry only one")
    combined = len(medium_slugs | variant_slugs)
    ceiling = max(1, round(0.30 * episode_len)) if episode_len else 0
    if combined > ceiling:
        fails.append(f"{combined} spread(s) carry a non-baseline medium or "
                     f"variant combined, ceiling is {ceiling} (30% of "
                     f"{episode_len} spreads) -- the book must still read as "
                     f"one book")

    return {
        "fails": fails,
        "warns": warns,
        "medium_count": len(medium_slugs),
        "by_medium": by_medium,
        "budget_max": max_variants,
        "budget_gap": min_gap,
    }


def check(proposal: dict, manifest_path: Path = MANIFEST_PATH, *, log=print, **kwargs) -> int:
    manifest = load_manifest(manifest_path)
    r = lint(proposal, manifest, **kwargs)
    log(f"[medium-variety] {r['medium_count']} medium-spread(s) proposed "
        f"(budget {r['budget_max']}, min gap {r['budget_gap']})")
    for w in r["warns"]:
        log(f"  WARN  {w}")
    if r["fails"]:
        log(f"[medium-variety] {len(r['fails'])} FAIL(s):")
        for f in r["fails"]:
            log(f"  FAIL  {f}")
    else:
        log("[medium-variety] 0 fails -- proposal within budget/spacing/"
            "figure/landing/motion guardrails.")
    return 1 if r["fails"] else 0
