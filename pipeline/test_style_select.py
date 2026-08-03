"""Tests for pipeline/style_select.py -- the propose-prompt builder + the
response parser feeding into style_variety.lint()."""
from __future__ import annotations

import json

import pytest

from pipeline import style_select as SS


def _manifest():
    return {
        "good_a": {"name": "Good A", "family": "linework", "beat_signal": ["calm"],
                   "avoid_on": [], "status": "production_approved", "gold_leaf_conflict": False},
        "caution_a": {"name": "Caution A", "family": "texture", "beat_signal": ["hardship"],
                      "avoid_on": [], "status": "caution", "gold_leaf_conflict": False},
    }


def _spreads(n=5):
    return [{"slug": f"s{i:02d}", "beat": 1, "text": f"narration text {i}"} for i in range(1, n + 1)]


def test_manifest_format_excludes_non_approved():
    text = SS.format_manifest_for_prompt(_manifest())
    assert "good_a" in text
    assert "caution_a" not in text


def test_prompt_includes_budget_and_spreads():
    prompt = SS.build_propose_prompt(_spreads(14), _manifest())
    assert "s01" in prompt and "s14" in prompt
    assert "good_a" in prompt
    assert "at most 3 variant-spreads" in prompt  # default_budget(14) == (3, 4)
    assert "4 spreads of each other" in prompt


def test_parse_proposal_happy_path():
    spreads = _spreads(5)
    raw = json.dumps({"s03": {"variant": "good_a", "reason": "fits the beat"}})
    proposal = SS.parse_proposal(raw, spreads)
    assert proposal == {"s01": None, "s02": None, "s03": "good_a", "s04": None, "s05": None}


def test_parse_proposal_rejects_unknown_slug():
    with pytest.raises(ValueError, match="unknown spread slug"):
        SS.parse_proposal(json.dumps({"s99": {"variant": "good_a"}}), _spreads(5))


def test_parse_proposal_rejects_malformed_json():
    with pytest.raises(ValueError, match="not valid JSON"):
        SS.parse_proposal("not json at all", _spreads(5))


def test_parse_proposal_rejects_missing_variant_key():
    with pytest.raises(ValueError, match="must be"):
        SS.parse_proposal(json.dumps({"s01": {"reason": "no variant key"}}), _spreads(5))


def test_end_to_end_propose_then_guardrail():
    """The real pipeline: build a prompt (not executed here, no LLM call),
    simulate a plausible LLM response, parse it, then run it through the
    REAL style_variety guardrail -- proves the two modules' data shapes
    actually connect."""
    from pipeline import style_variety as SV
    spreads = _spreads(20)
    raw = json.dumps({"s10": {"variant": "good_a", "reason": "calm beat"}})
    proposal = SS.parse_proposal(raw, spreads)
    r = SV.lint(proposal, _manifest())
    assert r["fails"] == []
    assert r["variant_count"] == 1
