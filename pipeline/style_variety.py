"""Deterministic guardrail for style-variant selection across a living-
sketchbook episode -- same family as spread_variety.py (pose/framing
collisions) and panel_variety.py (comic-grid redundancy), applied to a NEW
axis: which spreads get a named rendering-TECHNIQUE variant instead of the
plain baseline style (see .claude/skills/living-sketchbook/STYLE_SELECTION.md
sec.4 for the full design -- this is stage 2 of that 3-stage mechanism:
an LLM PROPOSES per-spread variants, THIS script caps them against the
evidence-backed manifest, then the existing human eye-gate confirms).

Reads `poc_living_sketchbook/_style_identity_bakeoff/style_manifest.json`
(the bake-off-scored catalog -- 35 variants, each with a real handmade/
identity_lock score, a status, and beat-fit metadata) and validates a
proposed per-spread assignment against it. Fails CLOSED: an unknown
variant id, a non-approved status, or a budget/spacing/theology violation
all reject the proposal outright -- same "floor, not ceiling" discipline
as every other variety gate in this repo. A human eye-gate still runs
after, same as every other gate here.
"""
from __future__ import annotations

import json
from pathlib import Path

MANIFEST_PATH = (Path(__file__).resolve().parents[1] / "poc_living_sketchbook"
                  / "_style_identity_bakeoff" / "style_manifest.json")


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def default_budget(episode_len: int) -> tuple[int, int]:
    """Returns (max_variant_spreads, min_spread_gap), scaled per
    STYLE_SELECTION.md sec.4's proposed table -- short episodes (~14
    spreads) get 3 variant-spreads/gap 4; long episodes (~68) get ~15-18%
    of spreads/gap 8. Linear-interpolated between those two anchors for
    anything in between; extrapolated (capped) beyond."""
    if episode_len <= 14:
        return 3, 4
    if episode_len >= 68:
        return max(10, round(episode_len * 0.15)), 8
    # linear interpolation between the two anchor points
    frac = (episode_len - 14) / (68 - 14)
    max_v = round(3 + frac * (10 - 3))
    gap = round(4 + frac * (8 - 4))
    return max_v, gap


def lint(proposal: dict, manifest: dict, *, beat_types: dict | None = None,
          max_variants: int | None = None, min_gap: int | None = None) -> dict:
    """`proposal`: ORDERED dict of spread_slug -> variant_id or None
    (baseline; the expected default for most spreads). Order must match
    story/page order -- spacing is checked by POSITION in this dict, not
    by any number embedded in the slug.
    `beat_types`: optional slug -> beat-type-tag dict (e.g. "glory",
    "landing", "dread") for the avoid_on / gold_leaf_conflict checks --
    omit to skip those two checks (degrades gracefully, same as
    spread_variety.py's grandfathering of untagged pools).
    Returns {'fails': [...], 'warns': [...], 'variant_count': int,
    'by_variant': {id: [slugs]}}.
    """
    fails: list[str] = []
    warns: list[str] = []
    slugs = list(proposal.keys())
    episode_len = len(slugs)
    budget_max, budget_gap = default_budget(episode_len)
    if max_variants is None:
        max_variants = budget_max
    if min_gap is None:
        min_gap = budget_gap

    used_positions: list[tuple[int, str, str]] = []  # (index, slug, variant_id)
    by_variant: dict[str, list[str]] = {}

    for i, slug in enumerate(slugs):
        vid = proposal[slug]
        if vid is None:
            continue
        if vid not in manifest:
            fails.append(f"{slug}: unknown variant id '{vid}' (not in style_manifest.json)")
            continue
        entry = manifest[vid]
        if entry["status"] != "production_approved":
            fails.append(f"{slug}: variant '{vid}' has status '{entry['status']}', "
                         f"not production_approved -- needs an explicit human override, "
                         f"not a silent proposal")
            continue
        used_positions.append((i, slug, vid))
        by_variant.setdefault(vid, []).append(slug)

        if beat_types and slug in beat_types:
            bt = beat_types[slug]
            if bt in entry.get("avoid_on", []) or "*" in entry.get("avoid_on", []):
                fails.append(f"{slug}: variant '{vid}' lists beat-type '{bt}' in its "
                             f"avoid_on -- wrong fit for this spread")
            if entry.get("gold_leaf_conflict") and bt != "glory":
                fails.append(f"{slug}: variant '{vid}' is gold-leaf-conflict-flagged "
                             f"(uses gold as a major element) on a non-glory beat "
                             f"('{bt}') -- violates the locked 'gold = His glory "
                             f"only' rule")

    # total budget
    if len(used_positions) > max_variants:
        fails.append(f"{len(used_positions)} variant-spreads proposed, budget is "
                     f"{max_variants} for a {episode_len}-spread episode -- baseline "
                     f"style must stay the default for the large majority of spreads")

    # per-variant max_per_episode cap
    for vid, used_slugs in by_variant.items():
        cap = manifest[vid].get("max_per_episode", 1)
        if len(used_slugs) > cap:
            fails.append(f"variant '{vid}' used {len(used_slugs)}x, cap is {cap}: {used_slugs}")

    # minimum spacing between ANY two variant-spreads, regardless of which variant
    used_positions.sort()
    for (i1, s1, v1), (i2, s2, v2) in zip(used_positions, used_positions[1:]):
        if i2 - i1 < min_gap:
            fails.append(f"'{s1}' ({v1}) and '{s2}' ({v2}) are only {i2 - i1} spreads "
                         f"apart, minimum gap is {min_gap}")

    if not used_positions:
        warns.append("no variant-spreads proposed -- entire episode on baseline style "
                     "(valid, just confirming this wasn't accidental)")

    return {"fails": fails, "warns": warns, "variant_count": len(used_positions),
            "by_variant": by_variant, "budget_max": max_variants, "budget_gap": min_gap}


def check(proposal: dict, manifest_path: Path = MANIFEST_PATH, *, beat_types=None,
          max_variants=None, min_gap=None, log=print) -> int:
    manifest = load_manifest(manifest_path)
    r = lint(proposal, manifest, beat_types=beat_types, max_variants=max_variants, min_gap=min_gap)
    log(f"[style-variety] {r['variant_count']} variant-spread(s) proposed "
        f"(budget {r['budget_max']}, min gap {r['budget_gap']})")
    for w in r["warns"]:
        log(f"  WARN  {w}")
    if r["fails"]:
        log(f"[style-variety] {len(r['fails'])} FAIL(s):")
        for f in r["fails"]:
            log(f"  FAIL  {f}")
    else:
        log("[style-variety] 0 fails -- proposal within budget/spacing/theology guardrails.")
    return 1 if r["fails"] else 0
