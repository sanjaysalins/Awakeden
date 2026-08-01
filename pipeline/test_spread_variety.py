"""Tests for the shared spread-variety gate (pipeline/spread_variety.py,
adapted 2026-07-31 from panel_variety.py for linear living-sketchbook spread
sequences instead of comic-grid panels)."""
from __future__ import annotations

import json

from pipeline import spread_variety as SV


def _pool(tmp_path, tags):
    if tags is not None:
        (tmp_path / "visual_tags.json").write_text(json.dumps(tags), encoding="utf-8")
    return tmp_path


def test_grandfathered_pool_skips(tmp_path):
    pool = _pool(tmp_path, None)
    assert SV.lint(pool, ["s01", "s02"])["skipped"] is True
    assert SV.check(pool, ["s01", "s02"], log=lambda *a: None) == 0


def test_exact_triple_match_fails(tmp_path):
    """The real Bronze Serpent defect: two spreads sharing subject+pose+framing."""
    pool = _pool(tmp_path, {
        "s07": {"subject": "moses-alone", "pose": "standing-staff-grip", "framing": "mid"},
        "s11": {"subject": "moses-alone", "pose": "standing-staff-grip", "framing": "mid"},
    })
    r = SV.lint(pool, ["s07", "s11"])
    assert len(r["fails"]) == 1 and "'s07' and 's11'" in r["fails"][0]
    assert SV.check(pool, ["s07", "s11"], log=lambda *a: None) == 1


def test_shared_pose_but_distinct_subject_passes(tmp_path):
    """s01/s03 share pose+framing with s07/s11 but carry a redeeming second
    subject element -- distinct subject tag means no collision."""
    pool = _pool(tmp_path, {
        "s01": {"subject": "moses+family", "pose": "standing-staff-grip", "framing": "wide"},
        "s03": {"subject": "moses+crowd", "pose": "standing-staff-grip", "framing": "wide"},
    })
    assert SV.check(pool, ["s01", "s03"], log=lambda *a: None) == 0


def test_untagged_slug_blocks(tmp_path):
    pool = _pool(tmp_path, {"s01": {"subject": "a", "pose": "b", "framing": "c"}})
    r = SV.lint(pool, ["s01", "s02"])
    assert r["untagged"] == ["s02"]
    assert SV.check(pool, ["s01", "s02"], log=lambda *a: None) == 1


def test_three_way_collision_reports_only_first_pair(tmp_path):
    """Three spreads sharing one triple report as one fail against the first
    seen slug -- documents current behavior (not a design requirement)."""
    tag = {"subject": "x", "pose": "y", "framing": "z"}
    pool = _pool(tmp_path, {"a": tag, "b": tag, "c": tag})
    r = SV.lint(pool, ["a", "b", "c"])
    assert len(r["fails"]) == 2
