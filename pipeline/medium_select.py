"""Stage 1 of the medium selection mechanism (MEDIUM_SELECTION.md sec.4) --
builds the propose-prompt an LLM receives to pick which spreads in a
living-sketchbook episode should be rendered as a TIPPED-IN PAPER MEDIUM
(Survey Plate / Archive Catalogue / Scribe's Ledger / Ancient Scroll / Night
Threshold) instead of the baseline sketchbook page. Sibling to
`pipeline/style_select.py` -- same shape, a different axis (what OBJECT the
page pretends to be, not what ENERGY the same object is drawn with).

This module does NOT call an LLM itself -- it only builds the prompt and
parses/validates the shape of a response, same division of labour as
style_select.py. `pipeline/medium_variety.py` then validates whatever comes
back; stage 3 is the existing human eye-gate.
"""
from __future__ import annotations

import json

from pipeline import medium_variety as MV


def format_manifest_for_prompt(manifest: dict) -> str:
    """Only production_approved, non-home mediums are ever offered to the
    proposer -- caution/rejected never appear as an option, and the home
    medium is never itself a proposal target (absence = home, by design)."""
    lines = []
    for mid, entry in sorted(manifest.items()):
        if mid == MV.HOME or entry["status"] != "production_approved":
            continue
        lines.append(
            f"- {mid} | {entry['name']} | figure_mode={entry['figure_mode']} | "
            f"beat_signal={entry['beat_signal']} | avoid_on={entry['avoid_on']} | "
            f"right_tool_for={entry.get('right_tool_for', '')}"
        )
    return "\n".join(lines)


def format_spread_table(spreads: list[dict]) -> str:
    """`spreads`: ordered list of {'slug':..., 'beat':..., 'text':...,
    optionally 'type':..., 'device':..., 'figures': [...]}. Renders one
    line per spread; `figures` is surfaced explicitly because the hard
    rules (no artifact_only medium on a figure spread, Jesus stays home)
    depend on the proposer actually seeing who's on the page."""
    lines = []
    for s in spreads:
        extra = f" | type={s['type']}" if "type" in s else ""
        extra += f" | device={s['device']}" if s.get("device") else ""
        figs = s.get("figures") or []
        extra += f" | figures={figs}" if figs else " | figures=none"
        lines.append(f"[{s['slug']}] beat {s.get('beat', '?')}: {s['text']}{extra}")
    return "\n".join(lines)


def build_propose_prompt(spreads: list[dict], manifest: dict, *,
                          max_mediums: int | None = None,
                          min_gap: int | None = None) -> str:
    episode_len = len(spreads)
    if max_mediums is None or min_gap is None:
        default_max, default_gap = MV.medium_budget(episode_len)
        max_mediums = max_mediums or default_max
        min_gap = min_gap or default_gap

    return f"""You are choosing which spreads in a living-sketchbook episode should be
rendered as a TIPPED-IN PAPER MEDIUM instead of the baseline sketchbook
page. A medium changes what physical object the page pretends to be (a
survey plate, an archive card, a ledger leaf, a scroll fragment, a night
sheet). Mediums are EVIDENCE moments -- the Keeper pasting a document into
the journal -- not decoration. Most spreads stay baseline.

EPISODE SPREAD TABLE (in page order, {episode_len} spreads):
{format_spread_table(spreads)}

AVAILABLE MEDIUMS (production_approved only -- do not propose anything not
on this list, do not invent new ones):
{format_manifest_for_prompt(manifest)}

HARD RULES you must respect in what you propose:
- An artifact_only medium may NEVER go on a spread listing a named figure.
- The landing spread and the two spreads before it are ALWAYS baseline.
- A spread with a JESUS appearance stays baseline (distant_marks survey is
  the only exception, and only with an explicit human OK -- flag it, do
  not assume it).
- If the beat needs night MOOD on a normal page, that is a technique
  variant (see STYLE_SELECTION.md), not the Night Threshold medium;
  propose the medium only when the page itself should become a flat
  threshold/emblem sheet.

BUDGET for this episode: at most {max_mediums} medium-spreads total, no two
within {min_gap} spreads of each other, no medium above its own
max_per_episode.

For each spread that EARNS a medium (the narration itself goes
documentary: a measurement, a record, a written thing, a reckoning, an
exhibit -- not "this could look cool"), propose ONE medium id + a one-line
reason tied to the beat's own content. Proposing nothing for most spreads
is the expected answer.

Output ONLY valid JSON, no other text: {{"slug": {{"medium": "id", "reason": "..."}}, ...}}
-- omit any spread you're not proposing a medium for."""


def parse_proposal(raw_json: str, spreads: list[dict]) -> dict:
    """Parses an LLM's raw JSON response into the flat {slug: medium_id_or_
    None} shape medium_variety.lint() expects, preserving spread ORDER
    (required for the spacing/landing-runway checks). Raises ValueError on
    malformed JSON or a slug the LLM invented that isn't in the real spread
    list."""
    valid_slugs = {s["slug"] for s in spreads}
    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"proposal is not valid JSON: {e}") from e

    proposal = {s["slug"]: None for s in spreads}
    for slug, detail in parsed.items():
        if slug not in valid_slugs:
            raise ValueError(f"proposal references unknown spread slug '{slug}'")
        if not isinstance(detail, dict) or "medium" not in detail:
            raise ValueError(f"'{slug}' entry must be {{'medium': ..., 'reason': ...}}")
        proposal[slug] = detail["medium"]
    return proposal
