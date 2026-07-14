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


def test_today_summary_only_counts_todays_rows(tmp_ledger):
    C.record("ep_a", "clip", "animate", "hf", "kling3_0", est_usd=0.65, est_credits=4.3)
    C.record("ep_a", "still", "stills", "nbp", "gemini", est_usd="~1")  # legacy string usd
    # yesterday's row must be excluded
    tmp_ledger.open("a", encoding="utf-8").write(
        '{"ts": "2020-01-01T00:00:00+00:00", "episode": "old", "provider": "hf", "est_usd": 99.0}\n')
    line = C.today_summary(line=True)
    assert line.startswith("TODAY $1.65") and "hf $0.65" in line and "nbp $1.00" in line
    table = C.today_summary()
    assert "99" not in table and "TOTAL" in table and "$   1.65" in table


def test_today_summary_empty_ledger(tmp_ledger):
    assert C.today_summary(line=True) == "TODAY $0.00 (0.0cr)"


def test_hook_adhoc_detector_matches_only_direct_hf_calls():
    import cost_status as W
    trigger = "hf generate " + "create"  # keep the literal out of shell/command surfaces
    assert W.adhoc_models("~/bin/hf.exe generate create kling3_0 --mode pro") == ["kling3_0"]
    assert W.adhoc_models("hf generate create nano_banana_2 --prompt 'a cross'") == ["nano_banana_2"]
    assert W.adhoc_models("cd /tmp && hf generate create kling3_0 --image x.png") == ["kling3_0"]
    # chained spends -> one row EACH (red-team M1)
    assert W.adhoc_models("hf generate create kling3_0 -p a; hf generate create kling3_0 -p b") \
        == ["kling3_0", "kling3_0"]
    # mere MENTIONS must never log phantom spend (red-team H1)
    assert W.adhoc_models(f'git commit -m "fix: {trigger} kling3_0 phantom"') == []
    assert W.adhoc_models(f'echo "{trigger} nano_banana_2"') == []
    assert W.adhoc_models(f"grep -rn '{trigger}' pipeline/") == []
    assert W.adhoc_models(f"python -c \"print('{trigger} kling3_0')\"") == []
    # pipeline runs (hf called INSIDE python) / non-spend hf commands never match
    assert W.adhoc_models(".venv/Scripts/python.exe cli_visual.py folder --provider hf") == []
    assert W.adhoc_models("hf account transactions --json") == []
    assert W.adhoc_models("hf generate cost kling3_0 --json") == []


def test_hook_adhoc_kling_price_scales_with_duration():
    import cost_status as W
    assert W._adhoc_usd("kling3_0", "hf generate create kling3_0 --duration 10")[0] == 1.3
    assert W._adhoc_usd("kling3_0", "hf generate create kling3_0 --mode pro")[0] == 0.65
    assert W._adhoc_usd("nano_banana_2", "hf generate create nano_banana_2")[0] == 0.30


def test_today_skips_reconcile_and_garbage_lines(tmp_ledger, monkeypatch):
    C.record("ep_a", "clip", "animate", "hf", "kling3_0", est_usd=0.65)
    C.record("ep_a", "", "reconcile", "hf", "", actual_credits=4.3, est_usd=0.65)  # true-up
    with tmp_ledger.open("a", encoding="utf-8") as f:
        f.write("null\n{not json\n")  # torn/garbage lines must not brick anything
    assert C.today_summary(line=True).startswith("TODAY $0.65")
    import cost_status as W
    monkeypatch.setattr(W, "LEDGER", tmp_ledger)
    by_p = W.today_by_provider()
    assert round(sum(d["usd"] for d in by_p.values()), 2) == 0.65


def test_usd_coerces_legacy_string_rows():
    assert C._usd(1.5) == 1.5
    assert C._usd("20-35") == 20.0   # range -> low bound
    assert C._usd("~1") == 1.0
    assert C._usd("<1") == 1.0
    assert C._usd(None) == 0.0
