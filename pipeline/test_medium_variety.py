"""Tests for the medium-selection guardrail (pipeline/medium_variety.py --
MEDIUM_SELECTION.md sec.4 stage 2, the Stationer's guardrail). Uses small
synthetic manifests, not the real medium_manifest.json, so these stay stable
if the real Stationer's case changes. Mirrors pipeline/test_style_variety.py
in shape; adds cases for the six medium-specific checks that axis never
needed."""
from __future__ import annotations

from pipeline import medium_variety as MV


def _manifest(**overrides):
    base = {
        "md_sketch": {"status": "production_approved", "avoid_on": [], "max_per_episode": 0,
                     "gold_leaf_conflict": False, "figure_mode": "figure_forward",
                     "text_drift_risk": "low"},
        "md_survey": {"status": "production_approved", "avoid_on": [], "max_per_episode": 2,
                      "gold_leaf_conflict": True, "figure_mode": "distant_marks",
                      "text_drift_risk": "medium"},
        "md_ledger": {"status": "production_approved", "avoid_on": [], "max_per_episode": 1,
                     "gold_leaf_conflict": True, "figure_mode": "artifact_only",
                     "text_drift_risk": "high"},
        "md_night": {"status": "production_approved", "avoid_on": [], "max_per_episode": 1,
                    "gold_leaf_conflict": True, "figure_mode": "figure_forward",
                    "text_drift_risk": "low"},
        "md_caution": {"status": "caution", "avoid_on": [], "max_per_episode": 1,
                       "gold_leaf_conflict": False, "figure_mode": "artifact_only",
                       "text_drift_risk": "low"},
    }
    base.update(overrides)
    return base


def _proposal(n, **assignments):
    p = {f"s{i:02d}": None for i in range(1, n + 1)}
    p.update(assignments)
    return p


def test_clean_proposal_passes():
    p = _proposal(30, s03="md_survey", s20="md_ledger")
    r = MV.lint(p, _manifest())
    assert r["fails"] == []
    assert r["medium_count"] == 2


def test_shared_checks_reused_unknown_id_fails():
    p = _proposal(30, s03="nonexistent")
    r = MV.lint(p, _manifest())
    assert any("unknown variant id" in f for f in r["fails"])


def test_shared_checks_reused_caution_status_fails():
    p = _proposal(30, s03="md_caution")
    r = MV.lint(p, _manifest())
    assert any("not production_approved" in f for f in r["fails"])


def test_figure_clash_artifact_only_fails():
    p = _proposal(30, s10="md_ledger")
    r = MV.lint(p, _manifest(), figures={"s10": ["priest"]})
    assert any("artifact_only medium" in f and "priest" in f for f in r["fails"])


def test_artifact_only_without_figures_passes():
    p = _proposal(30, s10="md_ledger")
    r = MV.lint(p, _manifest(), figures={"s10": []})
    assert r["fails"] == []


def test_jesus_spread_fails_without_override():
    p = _proposal(30, s10="md_survey")
    r = MV.lint(p, _manifest(), figures={"s10": ["jesus"]})
    assert any("Jesus spread" in f for f in r["fails"])


def test_jesus_spread_passes_with_explicit_override():
    p = _proposal(30, s10="md_survey")
    r = MV.lint(p, _manifest(), figures={"s10": ["jesus"]}, allow_jesus_distant={"s10"})
    assert r["fails"] == []


def test_landing_runway_blocks_landing_spread():
    p = _proposal(20, s20="md_survey")
    r = MV.lint(p, _manifest(), landing_slug="s20")
    assert any("landing runway" in f for f in r["fails"])


def test_landing_runway_blocks_two_spreads_before():
    p = _proposal(20, s18="md_survey")
    r = MV.lint(p, _manifest(), landing_slug="s20")
    assert any("landing runway" in f for f in r["fails"])


def test_landing_runway_allows_further_back():
    p = _proposal(20, s10="md_survey")
    r = MV.lint(p, _manifest(), landing_slug="s20")
    assert r["fails"] == []


def test_cross_axis_exclusivity_fails():
    mp = _proposal(30, s05="md_survey")
    vp = _proposal(30, s05="sv02_chiaroscuro")
    r = MV.lint(mp, _manifest(), variant_proposal=vp)
    assert any("BOTH the medium and technique-variant axes" in f for f in r["fails"])


def test_combined_ceiling_fails_when_over_30_percent():
    # 10-spread episode: ceiling = round(0.30*10) = 3. 2 medium + 2 variant,
    # all spaced/budgeted individually fine, but 4 > 3 combined.
    mp = _proposal(10, s01="md_survey", s02="md_night")
    vp = _proposal(10, s05="sv01", s06="sv02")
    r = MV.lint(mp, _manifest(), variant_proposal=vp,
                max_variants=99, min_gap=1)
    assert any("ceiling is" in f for f in r["fails"])


def test_motion_floor_fails_when_no_clip_planned():
    p = _proposal(30, s05="md_survey")
    r = MV.lint(p, _manifest(), motion_plan={"s05": False})
    assert any("no generative clip planned" in f for f in r["fails"])


def test_motion_floor_passes_when_clip_planned():
    p = _proposal(30, s05="md_survey")
    r = MV.lint(p, _manifest(), motion_plan={"s05": True})
    assert r["fails"] == []


def test_motion_floor_skipped_when_not_in_plan():
    p = _proposal(30, s05="md_survey")
    r = MV.lint(p, _manifest())
    assert r["fails"] == []


def test_high_text_risk_without_overlay_plan_warns():
    p = _proposal(30, s05="md_ledger")
    r = MV.lint(p, _manifest())
    assert any("no declared lettering-overlay plan" in w for w in r["warns"])


def test_high_text_risk_with_overlay_plan_no_warn():
    p = _proposal(30, s05="md_ledger")
    r = MV.lint(p, _manifest(), overlay_plan={"s05": "declared"})
    assert not any("lettering-overlay plan" in w for w in r["warns"])


def test_low_text_risk_never_warns():
    p = _proposal(30, s05="md_night")
    r = MV.lint(p, _manifest())
    assert not any("lettering-overlay plan" in w for w in r["warns"])


def test_medium_budget_scales_with_length():
    assert MV.medium_budget(14) == (2, 5)
    assert MV.medium_budget(68) == (5, 10)
    short, long_ = MV.medium_budget(14), MV.medium_budget(68)
    mid = MV.medium_budget(41)
    assert short[0] <= mid[0] <= long_[0]


def test_check_wraps_lint_exit_code():
    p = _proposal(30, s03="md_survey")
    r = MV.lint(p, _manifest())
    assert (1 if r["fails"] else 0) == 0
    p2 = _proposal(30, s03="md_caution")
    r2 = MV.lint(p2, _manifest())
    assert (1 if r2["fails"] else 0) == 1


def test_home_medium_proposal_fails_not_crashes():
    """Regression: proposing HOME (md_sketch) as a tipped-in medium used to
    crash with a TypeError (md_sketch's real max_per_episode is JSON null,
    and style_variety.lint()'s .get(key, 1) doesn't fall back on a
    present-but-null value). It must now fail closed instead."""
    p = _proposal(20, s10="md_sketch")
    r = MV.lint(p, _manifest())
    assert any("home medium" in f and "md_sketch" in f for f in r["fails"])
    assert r["medium_count"] == 0


def test_figures_none_value_does_not_crash():
    """Regression: figures={"s10": None} used to crash with
    'NoneType' object is not iterable."""
    p = _proposal(30, s10="md_ledger")
    r = MV.lint(p, _manifest(), figures={"s10": None})
    assert r["fails"] == []


def test_jesus_substring_matches_real_plan_table_format():
    """Regression: the check used to require an EXACT 'jesus' match, so it
    silently never fired against this repo's own real figure-annotation
    format, e.g. 'Jesus (small, teaching-by-night register)'."""
    p = _proposal(30, s10="md_survey")
    r = MV.lint(p, _manifest(), figures={"s10": ["Jesus (small, teaching-by-night register)"]})
    assert any("Jesus spread" in f for f in r["fails"])


def test_jesus_override_rejected_on_non_distant_marks_medium():
    """Regression: allow_jesus_distant used to rescue ANY non-home medium,
    not just distant_marks ones -- so a figure_forward medium (a readable
    face) could carry Jesus under an override meant only for distant marks."""
    p = _proposal(30, s10="md_night")  # figure_forward, not distant_marks
    r = MV.lint(p, _manifest(), figures={"s10": ["jesus"]}, allow_jesus_distant={"s10"})
    assert any("Jesus spread" in f for f in r["fails"])


def test_jesus_override_still_accepted_on_distant_marks_medium():
    """The override must still work for its one legal case."""
    p = _proposal(30, s10="md_survey")  # distant_marks
    r = MV.lint(p, _manifest(), figures={"s10": ["jesus"]}, allow_jesus_distant={"s10"})
    assert r["fails"] == []
