"""POC ($0, no renders): deterministic text-only shot-family classifier.

Question this pair of POCs is testing: can a spread's PLANNED description
text (the "Shows"/"Shot" prose a planner already writes before any still is
rendered) predict a rough (pose_family, framing_family) bucket well enough
to flag composition-collision risk BEFORE spend, the same way
`pipeline/spread_variety.py` already flags it AFTER rendering (from a human-
authored `visual_tags.json`)? If yes, this could run at planning time on
every future episode's beat table, not just as a post-render lint.

Deliberately dumb: first-match keyword rules, no LLM call, no images. This
is meant to be a FLOOR (same caveat as spread_variety.py/panel_variety.py)
that flags candidates for a human/planner to look at — not an auto-decider.
"""
from __future__ import annotations

import re

FRAMING_RULES = [
    ("extreme close", "extreme-close"),
    ("extreme-close", "extreme-close"),
    ("close-up", "close"),
    ("close on", "close"),
    ("close,", "close"),
    ("intimate close", "close"),
    ("intimate", "close"),
    (" close", "close"),
    ("wide/mid", "wide"),
    ("wide", "wide"),
    ("establishing", "wide"),
    (" mid:", "mid"),
    (" mid,", "mid"),
]

POSE_RULES = [
    ("kneel", "kneeling"),
    ("pray", "kneeling"),
    ("interced", "kneeling"),
    ("forg", "hands-action"),
    ("hammer", "hands-action"),
    ("hands finishing", "hands-action"),
    ("close-up hands", "hands-action"),
    ("face", "face-only"),
    ("eyes", "face-only"),
    ("walk", "walking"),
    ("sleepless", "reclining"),
    ("lying", "reclining"),
    ("looking at", "gazing-at-object"),
    ("staring at", "gazing-at-object"),
    ("holding", "gazing-at-object"),
    ("turns to address", "standing-address"),
    ("turning the question", "standing-address"),
    ("direct-address", "standing-address"),
    ("address", "standing-address"),
    ("turn", "standing-address"),
    ("reflect", "interior-reflection"),
    ("resolve", "interior-reflection"),
    ("realiz", "interior-reflection"),
    ("processing", "interior-reflection"),
    ("surprise", "interior-reflection"),
]


def _first_match(text: str, rules: list[tuple[str, str]], default: str) -> str:
    low = text.lower()
    for keyword, bucket in rules:
        if keyword in low:
            return bucket
    return default


def classify(text: str) -> dict:
    """Pure function: description text -> {'pose': ..., 'framing': ...}.
    `default` framing is 'mid' (this project's own default shot when a plan
    doesn't state otherwise) — deliberately NOT hidden, see the POC reports:
    how often the default fires is itself a finding.
    """
    text = text or ""
    return {
        "pose": _first_match(text, POSE_RULES, "generic-standing"),
        "framing": _first_match(text, FRAMING_RULES, "mid"),
    }


def normalize_assets(assets: str) -> str:
    """Assets column -> a coarse subject-family key (sorted, lowercased,
    comma-free) so 'Moses' and 'moses' and 'Moses ' collapse together, and
    'Moses, bronze-serpent' != 'Moses' alone (a second subject element is
    exactly what rescued s01/s03 in the short episode, per spread_variety.py)."""
    parts = [p.strip().lower() for p in re.split(r",|\(", assets) if p.strip()]
    parts = [p for p in parts if p and not p.startswith("reuse") and not p.startswith("new")]
    return "+".join(sorted(set(parts))) or "none"
