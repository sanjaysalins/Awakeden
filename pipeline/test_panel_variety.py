"""Tests for the shared panel-variety + reuse-aspect gate (pipeline/panel_variety.py,
generalized 2026-07-19 from Bronze Serpent's per-episode script and wired into
the livingpage build)."""
from __future__ import annotations

import json

from pipeline import panel_variety as PV


def _pool(tmp_path, tags):
    if tags is not None:
        (tmp_path / "visual_tags.json").write_text(json.dumps(tags), encoding="utf-8")
    return tmp_path


def _spec(beats):
    return {"beats": beats}


def test_grandfathered_pool_skips(tmp_path):
    """A pool with no visual_tags.json (legacy piece) must skip with exit 0 —
    father_forgive_them / Psalm 22 rebuilds cannot be broken by the new wiring."""
    pool = _pool(tmp_path, None)
    spec = _spec([{"tpl": "two_v", "clips": [{"slug": "a"}, {"slug": "b"}]}])
    assert PV.lint(pool, spec)["skipped"] is True
    assert PV.check(pool, spec, log=lambda *a: None) == 0


def test_redundant_grid_fails(tmp_path):
    pool = _pool(tmp_path, {"a": "christ-face", "b": "christ-face", "c": "crowd"})
    spec = _spec([{"tpl": "triptych_v",
                   "clips": [{"slug": "a"}, {"slug": "b"}, {"slug": "c"}]}])
    r = PV.lint(pool, spec)
    assert len(r["fails"]) == 1 and "share tag 'christ-face'" in r["fails"][0]
    assert PV.check(pool, spec, log=lambda *a: None) == 1


def test_distinct_grid_passes(tmp_path):
    pool = _pool(tmp_path, {"a": "christ-face", "b": "crowd"})
    spec = _spec([{"tpl": "two_v", "clips": [{"slug": "a"}, {"slug": "b"}]}])
    assert PV.check(pool, spec, log=lambda *a: None) == 0


def test_untagged_slug_in_grid_blocks(tmp_path):
    """Once a pool HAS visual_tags.json, an untagged slug in a multi-panel grid
    blocks (tag before it enters a grid — the Bronze Serpent discipline)."""
    pool = _pool(tmp_path, {"a": "christ-face"})
    spec = _spec([{"tpl": "two_v", "clips": [{"slug": "a"}, {"slug": "mystery"}]}])
    r = PV.lint(pool, spec)
    assert r["untagged"] == ["mystery"]
    assert PV.check(pool, spec, log=lambda *a: None) == 1


def test_reuse_aspect_violations(tmp_path):
    """A reuse_* 9:16 asset full-bleed (single-clip beat) or zoomed past 1.05 fails."""
    pool = _pool(tmp_path, {"reuse_x": "cross-wide", "a": "crowd"})
    spec = _spec([
        {"tpl": "full", "clips": [{"slug": "reuse_x"}]},                       # full-bleed
        {"tpl": "two_v", "clips": [{"slug": "reuse_x", "zoom": 1.2}, {"slug": "a"}]},  # over-zoom
    ])
    r = PV.lint(pool, spec)
    assert len(r["aspect_fails"]) == 2, r["aspect_fails"]
    assert "full-bleed hero panel" in r["aspect_fails"][0]
    assert "zoomed to 1.2" in r["aspect_fails"][1]
