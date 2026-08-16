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


# -- census() / check_census() ------------------------------------------------
# The real Serpent-Crusher Promised (Romans 16:20) defect: `lint()` above would
# find ZERO collisions here (every spread has a distinct subject+pose+framing
# triple) yet the piece still read as monotonous on real playback -- proving
# the two checks catch genuinely different failure modes.

_SCP_BEFORE_FIX = {  # round-1 draft: 7 of 9 spreads centered on feet/serpent,
    # each at a distinct subject+pose+framing so lint() finds zero collisions
    "s01": {"subject": "recap", "pose": "wide-establish", "framing": "wide", "objects": ["serpent"]},
    "s02": {"subject": "insert-1", "pose": "device", "framing": "insert", "objects": ["footprint"]},
    "s03": {"subject": "insert-2", "pose": "device", "framing": "close", "objects": ["footprint"]},
    "s04": {"subject": "hands", "pose": "writing", "framing": "wide", "objects": ["footprint"]},
    "s05": {"subject": "hero", "pose": "kjv-quote", "framing": "close", "objects": ["serpent", "feet"]},
    "s06": {"subject": "cross", "pose": "shadow", "framing": "mid", "objects": ["serpent"]},
    "s07": {"subject": "split", "pose": "strain-vs-still", "framing": "split", "objects": ["footprint"]},
    "s08": {"subject": "bridge", "pose": "gold-light", "framing": "wide", "objects": ["gold-thread"]},
    "s09": {"subject": "landing", "pose": "standing-feet", "framing": "close", "objects": ["serpent", "feet"]},
}

_SCP_AFTER_FIX = {  # final LOCKED plan: serpent legitimately recurs 4x at
    # genuinely distinct framings (wide-recap/cross-shadow/split-inset/
    # landing-feet-only); feet appears twice, once on the KJV quote itself
    "_mandated": {"s05": ["feet"]},
    "s01": {"objects": ["serpent"]},
    "s02": {"objects": ["unfinished-page"]},
    "s03": {"objects": ["armor"]},
    "s04": {"objects": ["quill-and-parchment"]},
    "s05": {"objects": ["serpent", "feet"]},  # KJV: "bruise Satan under your feet"
    "s06": {"objects": ["serpent", "cross"]},
    "s07": {"objects": ["serpent", "straining-figure"]},
    "s08": {"objects": ["gold-thread"]},
    "s09": {"objects": ["serpent", "feet"]},
}


def test_census_grandfathered_pool_skips(tmp_path):
    pool = _pool(tmp_path, None)
    assert SV.census(pool, ["s01", "s02"])["skipped"] is True
    assert SV.check_census(pool, ["s01", "s02"], log=lambda *a: None) == 0


def test_census_flags_dominant_object_no_collision_needed(tmp_path):
    """Reproduces the real defect: zero subject+pose+framing collisions, but
    the census still correctly flags the dominant objects."""
    pool = _pool(tmp_path, _SCP_BEFORE_FIX)
    slugs = list(_SCP_BEFORE_FIX.keys())
    assert SV.lint(pool, slugs)["fails"] == []  # lint() sees nothing wrong

    r = SV.census(pool, slugs)
    flagged = {obj for obj, _ in r["over_threshold"]}
    assert flagged == {"footprint", "serpent"}
    footprint_slugs = dict(r["over_threshold"])["footprint"]
    assert footprint_slugs == ["s02", "s03", "s04", "s07"]
    # census WARNs (non-blocking) -- it doesn't reject a real plan outright
    assert SV.check_census(pool, slugs, log=lambda *a: None) == 0


def test_census_mandated_exemption_excludes_kjv_named_occurrence(tmp_path):
    """The final locked plan: serpent legitimately recurs 4x at distinct
    framings (still surfaces as a WARN for a human to judge), feet appears
    twice but s05's occurrence is KJV-mandated ('under your feet') so it's
    exempted from the tally -- confirms the exemption narrows the count
    without hiding the occurrence class entirely."""
    pool = _pool(tmp_path, _SCP_AFTER_FIX)
    slugs = [k for k in _SCP_AFTER_FIX.keys() if not k.startswith("_")]
    r = SV.census(pool, slugs)
    tally = dict(r["over_threshold"])
    assert tally["serpent"] == ["s01", "s05", "s06", "s07", "s09"]
    assert "feet" not in tally  # only 1 non-exempt occurrence (s09) left, under threshold


def test_census_untagged_slug_blocks(tmp_path):
    pool = _pool(tmp_path, {"s01": {"objects": ["a"]}})
    r = SV.census(pool, ["s01", "s02"])
    assert r["untagged"] == ["s02"]
    assert SV.check_census(pool, ["s01", "s02"], log=lambda *a: None) == 1


def test_census_exactly_at_threshold_does_not_warn(tmp_path):
    pool = _pool(tmp_path, {
        "s01": {"objects": ["serpent"]},
        "s02": {"objects": ["serpent"]},
        "s03": {"objects": ["cross"]},
    })
    r = SV.census(pool, ["s01", "s02", "s03"], threshold=2)
    assert r["over_threshold"] == []
