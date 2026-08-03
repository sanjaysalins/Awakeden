"""Tests for the style-variant selection guardrail (pipeline/style_variety.py,
2026-08-01 -- the deterministic cap stage of STYLE_SELECTION.md's 3-stage
propose/guardrail/eye-gate mechanism). Uses small synthetic manifests, not
the real style_manifest.json, so these stay stable if the real bake-off
data changes."""
from __future__ import annotations

from pipeline import style_variety as SV


def _manifest(**overrides):
    base = {
        "good_a": {"status": "production_approved", "avoid_on": [], "max_per_episode": 1, "gold_leaf_conflict": False},
        "good_b": {"status": "production_approved", "avoid_on": [], "max_per_episode": 1, "gold_leaf_conflict": False},
        "caution_a": {"status": "caution", "avoid_on": [], "max_per_episode": 1, "gold_leaf_conflict": False},
        "gold_a": {"status": "production_approved", "avoid_on": [], "max_per_episode": 1, "gold_leaf_conflict": True},
        "avoid_landing": {"status": "production_approved", "avoid_on": ["landing"], "max_per_episode": 1, "gold_leaf_conflict": False},
    }
    base.update(overrides)
    return base


def _proposal(n, **assignments):
    p = {f"s{i:02d}": None for i in range(1, n + 1)}
    p.update(assignments)
    return p


def test_clean_proposal_passes():
    p = _proposal(20, s03="good_a", s15="good_b")
    r = SV.lint(p, _manifest())
    assert r["fails"] == []
    assert r["variant_count"] == 2


def test_unknown_variant_id_fails():
    p = _proposal(20, s03="nonexistent")
    r = SV.lint(p, _manifest())
    assert any("unknown variant id" in f for f in r["fails"])


def test_non_approved_status_fails():
    p = _proposal(20, s03="caution_a")
    r = SV.lint(p, _manifest())
    assert any("not production_approved" in f for f in r["fails"])


def test_spacing_violation_fails():
    p = _proposal(20, s10="good_a", s12="good_b")  # 2 apart, default gap for 20 spreads is 4
    r = SV.lint(p, _manifest())
    assert any("apart, minimum gap" in f for f in r["fails"])


def test_adequate_spacing_passes():
    p = _proposal(20, s10="good_a", s16="good_b")  # 6 apart, clears the gap
    r = SV.lint(p, _manifest())
    assert r["fails"] == []


def test_budget_exceeded_fails():
    # 14-spread episode -> budget (3, gap 4). 4 variant-spreads, each >=4 apart
    # (clears spacing) but exceeds the 3-spread budget.
    m = _manifest(good_a={"status": "production_approved", "avoid_on": [], "max_per_episode": 4, "gold_leaf_conflict": False})
    p = _proposal(14, s01="good_a", s05="good_a", s09="good_a", s13="good_a")
    r = SV.lint(p, m)
    assert any("budget is" in f for f in r["fails"])


def test_max_per_episode_cap_fails():
    m = _manifest()
    m["good_a"]["max_per_episode"] = 1
    p = _proposal(30, s01="good_a", s15="good_a")
    r = SV.lint(p, m)
    assert any("used 2x, cap is 1" in f for f in r["fails"])


def test_avoid_on_beat_type_fails():
    p = _proposal(20, s20="avoid_landing")
    r = SV.lint(p, _manifest(), beat_types={"s20": "landing"})
    assert any("avoid_on" in f for f in r["fails"])


def test_gold_leaf_conflict_on_non_glory_fails():
    p = _proposal(20, s05="gold_a")
    r = SV.lint(p, _manifest(), beat_types={"s05": "ordinary-narrative"})
    assert any("gold-leaf-conflict-flagged" in f for f in r["fails"])


def test_gold_leaf_on_glory_beat_passes():
    p = _proposal(20, s05="gold_a")
    r = SV.lint(p, _manifest(), beat_types={"s05": "glory"})
    assert r["fails"] == []


def test_no_beat_types_skips_theology_checks():
    """Without beat_types, avoid_on/gold_leaf checks degrade gracefully
    (same grandfathering philosophy as spread_variety.py's untagged pools)."""
    p = _proposal(20, s05="gold_a")
    r = SV.lint(p, _manifest())
    assert r["fails"] == []


def test_all_baseline_warns_not_fails():
    p = _proposal(14)
    r = SV.lint(p, _manifest())
    assert r["fails"] == []
    assert any("no variant-spreads proposed" in w for w in r["warns"])


def test_default_budget_scales_with_length():
    assert SV.default_budget(14) == (3, 4)
    assert SV.default_budget(68) == (10, 8)
    short, long_ = SV.default_budget(14), SV.default_budget(68)
    mid = SV.default_budget(41)  # midpoint
    assert short[0] < mid[0] < long_[0]


def test_lint_to_exit_code_contract():
    """check() just wraps lint() and returns 1 if fails else 0 -- verify
    the contract directly against lint() rather than hitting the real
    style_manifest.json (which check()'s own default path points at)."""
    p = _proposal(20, s03="good_a")
    r = SV.lint(p, _manifest())
    assert (1 if r["fails"] else 0) == 0
    p2 = _proposal(20, s03="caution_a")
    r2 = SV.lint(p2, _manifest())
    assert (1 if r2["fails"] else 0) == 1
