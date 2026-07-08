"""Budget-teeth tests (P0-3, 2026-07-08): the ceiling must actually refuse a spend
(check_budget was dead code — defined, never called, never tested), and the ledger
math must survive the old hand-written string rows ('20-35', '~1', '<1').

Run: .venv\\Scripts\\python.exe -m pytest pipeline/test_cost.py
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from pipeline import cost as C


@pytest.fixture()
def tmp_ledger(monkeypatch):
    led = Path(tempfile.mkdtemp()) / "ledger.jsonl"
    monkeypatch.setattr(C, "LEDGER", led)
    return led


def test_check_budget_raises_on_ceiling_breach(tmp_ledger):
    C.record("ep_poc", "clip", "animate", "hf", "kling3_0", est_usd=24.0)
    with pytest.raises(SystemExit):
        C.check_budget("ep_poc", "short", projected_usd=2.0)  # 24 + 2 > 25 cap


def test_check_budget_allows_under_cap_and_override(tmp_ledger):
    C.record("ep_poc", "clip", "animate", "hf", "kling3_0", est_usd=10.0)
    assert C.check_budget("ep_poc", "short", projected_usd=2.0) == 12.0
    # override lets a deliberate breach through (returns the projected total)
    assert C.check_budget("ep_poc", "short", projected_usd=99.0, override=True) > 25


def test_record_appends_readable_row(tmp_ledger):
    C.record("ep_poc", "clip", "animate", "hf", "kling3_0", est_usd=0.65, note="x.png")
    rows = C.load()
    assert len(rows) == 1 and rows[0]["episode"] == "ep_poc" and rows[0]["est_usd"] == 0.65
    assert C.episode_total_usd("ep_poc") == 0.65


def test_usd_coerces_legacy_string_rows():
    assert C._usd(1.5) == 1.5
    assert C._usd("20-35") == 20.0   # range -> low bound
    assert C._usd("~1") == 1.0
    assert C._usd("<1") == 1.0
    assert C._usd(None) == 0.0
