"""Tests for pipeline/medium_select.py -- the propose-prompt builder + the
response parser feeding into medium_variety.lint(). Mirrors
pipeline/test_style_select.py in shape."""
from __future__ import annotations

import json

import pytest

from pipeline import medium_select as MS


def _manifest():
    return {
        "md_sketch": {"name": "Sketchbook Ink", "figure_mode": "figure_forward",
                      "beat_signal": ["human"], "avoid_on": [],
                      "status": "production_approved", "right_tool_for": "the default"},
        "md_survey": {"name": "Survey Plate", "figure_mode": "distant_marks",
                     "beat_signal": ["geography"], "avoid_on": ["landing"],
                     "status": "production_approved", "right_tool_for": "geography beats"},
        "md_caution": {"name": "Archive Catalogue", "figure_mode": "artifact_only",
                       "beat_signal": ["exhibit"], "avoid_on": [],
                       "status": "caution", "right_tool_for": "exhibit beats"},
    }


def _spreads(n=5):
    return [{"slug": f"s{i:02d}", "beat": 1, "text": f"narration text {i}",
              "figures": []} for i in range(1, n + 1)]


def test_manifest_format_excludes_home_and_non_approved():
    text = MS.format_manifest_for_prompt(_manifest())
    assert "md_survey" in text
    assert "md_sketch" not in text  # home medium never itself a proposal target
    assert "md_caution" not in text  # caution status never offered


def test_prompt_includes_budget_and_spreads():
    prompt = MS.build_propose_prompt(_spreads(14), _manifest())
    assert "s01" in prompt and "s14" in prompt
    assert "md_survey" in prompt
    assert "at most 2 medium-spreads" in prompt  # medium_budget(14) == (2, 5)
    assert "5 spreads of each other" in prompt


def test_spread_table_surfaces_figures():
    spreads = _spreads(2)
    spreads[0]["figures"] = ["jesus"]
    table = MS.format_spread_table(spreads)
    assert "figures=['jesus']" in table
    assert "figures=none" in table


def test_parse_proposal_happy_path():
    spreads = _spreads(5)
    raw = json.dumps({"s03": {"medium": "md_survey", "reason": "a measurement beat"}})
    proposal = MS.parse_proposal(raw, spreads)
    assert proposal == {"s01": None, "s02": None, "s03": "md_survey", "s04": None, "s05": None}


def test_parse_proposal_rejects_unknown_slug():
    with pytest.raises(ValueError, match="unknown spread slug"):
        MS.parse_proposal(json.dumps({"s99": {"medium": "md_survey"}}), _spreads(5))


def test_parse_proposal_rejects_malformed_json():
    with pytest.raises(ValueError, match="not valid JSON"):
        MS.parse_proposal("not json at all", _spreads(5))


def test_parse_proposal_rejects_missing_medium_key():
    with pytest.raises(ValueError, match="must be"):
        MS.parse_proposal(json.dumps({"s01": {"reason": "no medium key"}}), _spreads(5))


def test_end_to_end_propose_then_guardrail():
    """Build a prompt (not executed here, no LLM call), simulate a plausible
    LLM response, parse it, then run it through the REAL medium_variety
    guardrail -- proves the two modules' data shapes actually connect."""
    from pipeline import medium_variety as MV
    spreads = _spreads(20)
    raw = json.dumps({"s10": {"medium": "md_survey", "reason": "a scale beat"}})
    proposal = MS.parse_proposal(raw, spreads)
    r = MV.lint(proposal, _manifest())
    assert r["fails"] == []
    assert r["medium_count"] == 1
