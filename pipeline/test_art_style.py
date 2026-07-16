"""Tests for pipeline/art_style.py — the Baroque-legacy detection signal
behind SYNC-G8 (memory `graphic-novel-style-migration`, hardened 2026-07-15)."""
from __future__ import annotations

import json

from pipeline import art_style


def test_unknown_when_nothing_present(tmp_path):
    assert art_style.detect_art_style(tmp_path) == art_style.UNKNOWN


def test_longform_baroque_scene_plan_detected(tmp_path):
    d = tmp_path / "visual_16x9"
    d.mkdir()
    (d / "scene_plan.json").write_text(
        json.dumps({"style_base": "Baroque oil painting, dramatic chiaroscuro"}),
        encoding="utf-8",
    )
    assert art_style.detect_art_style(tmp_path) == art_style.BAROQUE


def test_longform_graphic_novel_scene_plan_detected(tmp_path):
    d = tmp_path / "visual_16x9"
    d.mkdir()
    (d / "scene_plan.json").write_text(
        json.dumps({"style_base": "inked biblical graphic-novel style"}),
        encoding="utf-8",
    )
    assert art_style.detect_art_style(tmp_path) == art_style.GRAPHIC_NOVEL


def test_inked_dir_wins_over_legacy_dir(tmp_path):
    # matches finality.py's own inked-first precedence: if a piece has BOTH
    # an old Baroque visual_16x9 and a rebuilt visual_16x9_inked, the inked
    # pool is what's actually shipping.
    (tmp_path / "visual_16x9").mkdir()
    (tmp_path / "visual_16x9" / "scene_plan.json").write_text(
        json.dumps({"style_base": "Baroque oil painting"}), encoding="utf-8")
    (tmp_path / "visual_16x9_inked").mkdir()
    (tmp_path / "visual_16x9_inked" / "scene_plan.json").write_text(
        json.dumps({"style_base": "inked graphic-novel"}), encoding="utf-8")
    assert art_style.detect_art_style(tmp_path) == art_style.GRAPHIC_NOVEL


def test_panel_scene_plan_md_fallback(tmp_path):
    (tmp_path / "_panel_scene_plan.md").write_text(
        "Each scene below is a Baroque-oil still tiled to its narration window.",
        encoding="utf-8",
    )
    assert art_style.detect_art_style(tmp_path) == art_style.BAROQUE


def test_batches_piece_json_detected(tmp_path):
    (tmp_path / "piece.json").write_text(
        json.dumps({"stills": {"jobs": {"01": {"prompt": "inked biblical graphic-novel close-up"}}}}),
        encoding="utf-8",
    )
    assert art_style.detect_art_style(tmp_path) == art_style.GRAPHIC_NOVEL


def test_livingpage_inked_rebuild_wins_over_stale_baroque_sibling(tmp_path):
    # the Isaiah 53 false-positive this module was built to catch: an inked
    # rebuild that ships from *_inked but uses the livingpage format (no
    # scene_plan.json at all) sitting next to a STALE Baroque visual_16x9
    # that still has its old scene_plan.json on disk.
    old = tmp_path / "visual_16x9"
    old.mkdir()
    (old / "scene_plan.json").write_text(
        json.dumps({"style_base": "Baroque oil painting"}), encoding="utf-8")
    inked = tmp_path / "visual_16x9_inked"
    inked.mkdir()
    (inked / "LivingPage_Foo_16x9_scored_sfx.mp4").write_bytes(b"\x00")
    assert art_style.detect_art_style(tmp_path) == art_style.GRAPHIC_NOVEL


def test_negated_baroque_mention_is_not_a_baroque_hit(tmp_path):
    # real false positive caught on father_forgive_them: its migrated
    # scene_plan.json doc-comment reads "STYLE = inked graphic-novel (NOT
    # Baroque oil)" — a naive substring scan must not read the negated
    # mention as a Baroque hit.
    d = tmp_path / "visual"
    d.mkdir()
    (d / "scene_plan.json").write_text(
        json.dumps({"_doc": "STYLE = inked graphic-novel (NOT Baroque oil) - the "
                             "animate driver builds an inked motion prompt"}),
        encoding="utf-8",
    )
    assert art_style.detect_art_style(tmp_path) == art_style.GRAPHIC_NOVEL


def test_livingpage_filename_wins_even_in_a_non_inked_dir(tmp_path):
    # real false positive caught on psalm-22-from-the-cross: FINAL_VIDEO.txt
    # pins visual_16x9/LivingPage_Psalm22_16x9_scored_sfx.mp4 (verified by eye:
    # genuinely inked graphic-novel) sitting next to a STALE pre-migration
    # visual_16x9/scene_plan.json that still says Baroque.
    d = tmp_path / "visual_16x9"
    d.mkdir()
    (d / "scene_plan.json").write_text(
        json.dumps({"style_base": "Baroque oil painting"}), encoding="utf-8")
    (d / "LivingPage_Foo_16x9_scored_sfx.mp4").write_bytes(b"\x00")
    (tmp_path / "FINAL_VIDEO.txt").write_text(
        "visual_16x9/LivingPage_Foo_16x9_scored_sfx.mp4", encoding="utf-8")
    assert art_style.detect_art_style(tmp_path) == art_style.GRAPHIC_NOVEL


def test_malformed_json_does_not_crash(tmp_path):
    d = tmp_path / "visual_16x9"
    d.mkdir()
    (d / "scene_plan.json").write_text("{not valid json", encoding="utf-8")
    assert art_style.detect_art_style(tmp_path) == art_style.UNKNOWN


if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
