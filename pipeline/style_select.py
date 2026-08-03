"""Stage 1 of the style-variant selection mechanism (STYLE_SELECTION.md
sec.4) -- turns the documented propose-prompt template into a real,
callable function. Builds the actual prompt an LLM (Agent-mode, per this
project's locked LLM-access pattern -- no direct API call from here) would
receive to propose per-spread style variants for a living-sketchbook
episode. Stage 2 (`pipeline/style_variety.py`) then validates whatever
comes back; stage 3 is the existing human eye-gate.

This module does NOT call an LLM itself -- it only builds the prompt and
parses/validates the shape of a response. The actual LLM call happens
wherever this episode's planning is happening (an Agent call, an in-chat
turn, or a future scripted call once this project's LLM-access story for
this pipeline is settled) -- keeping this module a pure, testable text
transform, not a network client.
"""
from __future__ import annotations

import json

from pipeline import style_variety as SV


def format_manifest_for_prompt(manifest: dict) -> str:
    """Only production_approved variants are ever offered to the proposer
    -- caution/rejected never even appear as an option, so there's no way
    for the LLM to propose something a human has to override."""
    lines = []
    for vid, entry in sorted(manifest.items()):
        if entry["status"] != "production_approved":
            continue
        lines.append(
            f"- {vid} | {entry['name']} | family={entry['family']} | "
            f"beat_signal={entry['beat_signal']} | avoid_on={entry['avoid_on']}"
            + (" | GOLD-LEAF: glory beats only" if entry.get("gold_leaf_conflict") else "")
        )
    return "\n".join(lines)


def format_spread_table(spreads: list[dict]) -> str:
    """`spreads`: ordered list of {'slug':..., 'beat':..., 'text':...,
    optionally 'type':..., 'device':...}. Renders one line per spread."""
    lines = []
    for s in spreads:
        extra = f" | type={s['type']}" if "type" in s else ""
        extra += f" | device={s['device']}" if s.get("device") else ""
        lines.append(f"[{s['slug']}] beat {s.get('beat', '?')}: {s['text']}{extra}")
    return "\n".join(lines)


def build_propose_prompt(spreads: list[dict], manifest: dict, *,
                          max_variants: int | None = None,
                          min_gap: int | None = None) -> str:
    episode_len = len(spreads)
    if max_variants is None or min_gap is None:
        default_max, default_gap = SV.default_budget(episode_len)
        max_variants = max_variants or default_max
        min_gap = min_gap or default_gap

    return f"""You are choosing which spreads in a living-sketchbook episode should use a
named rendering-technique variant instead of the plain baseline style.
Named variants exist to make specific beats hit harder -- they are NOT
decoration, and most spreads should stay on baseline.

EPISODE SPREAD TABLE (in page order, {episode_len} spreads):
{format_spread_table(spreads)}

AVAILABLE VARIANTS (production_approved only -- do not propose anything
not on this list, do not invent new ones):
{format_manifest_for_prompt(manifest)}

BUDGET for this episode: at most {max_variants} variant-spreads total, no
two within {min_gap} spreads of each other, no variant used more than
once unless the manifest says otherwise.

For each spread you think EARNS a variant (a beat whose energy the
baseline style would flatten -- judgment, dread, memory, a hook, a
glory beat, NOT just "this spread could look cool"), propose ONE variant
id and a one-line reason tying it to the beat's own content, not just
vibes. Stay well under budget if the episode doesn't have that many
genuinely earning beats -- proposing nothing is a valid, expected answer
for most spreads.

Output ONLY valid JSON, no other text: {{"slug": {{"variant": "id", "reason": "..."}}, ...}}
-- omit any spread you're not proposing a variant for."""


def parse_proposal(raw_json: str, spreads: list[dict]) -> dict:
    """Parses an LLM's raw JSON response into the flat {slug: variant_id
    or None} shape style_variety.lint() expects, preserving spread ORDER
    (required for the spacing check). Raises ValueError on malformed JSON
    or a slug the LLM invented that isn't in the real spread list."""
    valid_slugs = {s["slug"] for s in spreads}
    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"proposal is not valid JSON: {e}") from e

    proposal = {s["slug"]: None for s in spreads}
    for slug, detail in parsed.items():
        if slug not in valid_slugs:
            raise ValueError(f"proposal references unknown spread slug '{slug}'")
        if not isinstance(detail, dict) or "variant" not in detail:
            raise ValueError(f"'{slug}' entry must be {{'variant': ..., 'reason': ...}}")
        proposal[slug] = detail["variant"]
    return proposal
