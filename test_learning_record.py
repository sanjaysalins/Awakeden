"""Tests for the calibration ledger's validated writer (pipeline/learning.py record)."""
import json

import pytest

from pipeline import learning


TAX = {"grace-trap": {"status": "hard-gate"}}


def _miss(**over):
    m = {"defect_class": "grace-trap", "beat": "conviction",
         "detail": "demand-to-produce phrasing", "caught_by": "external-panel",
         "deterministic": False}
    m.update(over)
    return m


def test_valid_record_passes():
    problems, warnings = learning.validate_record(
        {"episode": "30 Test", "panel_misses": [_miss()]}, TAX)
    assert problems == [] and warnings == []


def test_clean_panel_run_is_valid():
    problems, _ = learning.validate_record({"episode": "30 Test", "panel_misses": []}, TAX)
    assert problems == []


def test_missing_episode_and_misses_block():
    problems, _ = learning.validate_record({}, TAX)
    assert any("episode" in p for p in problems)
    assert any("panel_misses" in p for p in problems)


def test_miss_needs_class_and_detail():
    problems, _ = learning.validate_record(
        {"episode": "x", "panel_misses": [{"beat": "hook"}]}, TAX)
    assert any("defect_class" in p for p in problems)
    assert any("detail" in p for p in problems)


def test_unknown_class_warns_not_blocks():
    problems, warnings = learning.validate_record(
        {"episode": "x", "panel_misses": [_miss(defect_class="brand-new-class")]}, TAX)
    assert problems == []
    assert any("brand-new-class" in w for w in warnings)


def test_record_cli_appends_and_stamps_date(tmp_path, monkeypatch):
    monkeypatch.setattr(learning, "_DATA", tmp_path)
    monkeypatch.setattr(learning, "LEDGER", tmp_path / "calibration.jsonl")
    rec = tmp_path / "rec.json"
    rec.write_text(json.dumps({"episode": "30 Test", "panel_misses": [_miss()]}),
                   encoding="utf-8")
    assert learning.main(["record", str(rec)]) == 0
    rows = learning.load_ledger()
    assert len(rows) == 1 and rows[0]["episode"] == "30 Test" and rows[0]["date"]


def test_record_cli_blocks_invalid(tmp_path, monkeypatch):
    monkeypatch.setattr(learning, "_DATA", tmp_path)
    monkeypatch.setattr(learning, "LEDGER", tmp_path / "calibration.jsonl")
    rec = tmp_path / "rec.json"
    rec.write_text(json.dumps({"panel_misses": "not-a-list"}), encoding="utf-8")
    assert learning.main(["record", str(rec)]) == 2
    assert not (tmp_path / "calibration.jsonl").exists()


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
