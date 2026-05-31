"""PANEL GATE — external multi-LLM review of a narration BEFORE it is finalized.

The text stage produces a LOCKED draft, then STOPS here. This module writes
`panel_request.md` into the v1 folder: (1) the engine's own assessment of where
the draft is weakest (pulled from the review's CAUTION panel notes + CONDITIONAL
gate fixes), and (2) a ready-to-paste prompt for 2-4 external LLMs to critique and
beat the draft. The audio is NOT rendered until the user panels it and the draft
is finalized (see `_finalize.py`). This makes the panel a hard gate, not a step
someone has to remember.
"""
from __future__ import annotations

from pathlib import Path

from pipeline.models import Draft, Review, Thread
from pipeline.series import Episode, Series


# The binding rules every landing/whole-narration panel must enforce. Kept in sync
# with data/constitution.md (clarity / grace-tuned / scene-scope / landing-not-tired
# / pacing). One source so the prompt never drifts from the engine's own gates.
BINDING_RULES = [
    "KJV verbatim inside quotation marks (including terminal punctuation); paraphrase only as narrator prose outside quotes.",
    "Clarity beats cleverness — a tired stranger with zero Bible background must get every beat on ONE hearing. No geography/word-study/wordplay as the POINT; no logic-tricks.",
    "Land on WHO CHRIST IS, never 'your problem solved' — the ache is the doorway, Christ is the room. Name the episode's specific self-help trap and kill it.",
    "Grace, not self-effort — the conviction pierces as grace (He acts first), never 'try harder / be braver / want it more'. Do NOT shame the person in the text.",
    "Grace-tuned question — if the close turns the verse's question onto the viewer, the ANSWER must be something God GIVES (revealed / put on your lips), never something the viewer must PRODUCE.",
    "Scene-scope only — every claim airtight to THIS scene and pericope; do not import later doctrine the text hasn't reached (e.g. pre-resurrection 'He is risen', or 'He made it' where the scene only shows authority).",
    "No tired closers ('will you trust Him', 'the choice is yours', 'He's waiting'); the last line does NEW work and is UN-PORTABLE (could not close a different episode).",
    "Pacing: <= 2 short spoken quotes (KJV quotes render at natural pace and cannot be sped up; more than two rushes the narrator).",
]


def _engine_assessment(review: Review) -> list[str]:
    """The engine's own weak-spot list = every CAUTION/REVISION panel note and every
    CONDITIONAL/FAIL gate fix. These are exactly the soft spots the panel should attack."""
    out: list[str] = []
    for p in review.panel:
        v = p.verdict.upper()
        if "CAUTION" in v or "REVISION" in v:
            out.append(f"[{p.agent}] {p.note}")
    for g in review.gates:
        v = g.verdict.upper()
        if v in ("CONDITIONAL", "FAIL"):
            fix = f" -> fix: {g.fix}" if g.fix else ""
            out.append(f"[{g.gate} {g.verdict}] {g.evidence}{fix}")
    for pf in review.priority_fixes:
        out.append(f"[priority] {pf}")
    return out


def _beats_block(draft: Draft) -> str:
    label = {
        "hook": "Hook", "point": "Point", "proof": "Proof",
        "conviction": "Conviction", "landing": "Landing",
    }
    lines = []
    for b in draft.beats:
        lines.append(f"- **{label.get(b.id, b.id.title())}** — {b.text.strip()}")
    return "\n".join(lines)


def build_panel_request(
    series: Series, episode: Episode, draft: Draft,
    kjv: str | None, review: Review, thread: Thread | None = None,
) -> str:
    assessment = _engine_assessment(review)
    assess_md = (
        "\n".join(f"- {a}" for a in assessment)
        if assessment else
        "- No weak spots flagged by the engine review — panel for polish and a stronger landing."
    )
    rules_md = "\n".join(f"{i+1}. {r}" for i, r in enumerate(BINDING_RULES))
    thread_md = (f"\n**Thread (spine):** {thread.thread}" if thread and thread.thread else "")
    kjv_md = f'\n**Verified KJV ({episode.primary_ref}):** "{kjv}"' if kjv else ""

    return f"""# PANEL REQUEST — {draft.title or episode.title} ({episode.primary_ref})

> **This is a GATE.** Paste the PROMPT block below into 2-4 other LLMs. Bring their
> replies back here; the engine/agent judges them, folds in the winners, and only
> THEN finalizes + renders audio. Do not proceed to audio until finalized.

## Engine self-assessment — where this draft is weakest
{assess_md}

## Current draft
{_beats_block(draft)}

---
## PROMPT — copy everything below into your other LLMs
---

You are a sharp script editor red-teaming a 60-second gospel YouTube Short. Be a critic first, a reviser second. Quote the line you critique.

**Format:** Series *{series.name}* — opens in a Bible scene, surfaces a question/claim, turns it onto the viewer, and ends on a response **to Jesus by grace** (never self-improvement). Warm authority; a skeptic should be able to stay in the room. Five beats, ~150-160 words total: Hook (~22w) - Point (~24w) - Proof (~50w, carries the KJV quotes) - Conviction (~30w) - Landing (~24w).

**Episode — {episode.primary_ref}: {episode.title}.** Theme: {episode.theme}{kjv_md}{thread_md}

**My current draft:**
{_beats_block(draft)}

**Binding rules — flag any violation, then beat it:**
{rules_md}

**Deliver:**
(a) a short critique of EACH beat against the rules — where is it weakest?
(b) for each beat you'd improve, a stronger version at the same word budget;
(c) if you see a better *spine* entirely, one full 5-beat alternative;
(d) your single best **conviction** and best **landing**, and why.
"""


def write_panel_request(
    folder: Path, series: Series, episode: Episode, draft: Draft,
    kjv: str | None, review: Review, thread: Thread | None = None,
) -> Path:
    md = build_panel_request(series, episode, draft, kjv, review, thread)
    out = folder / "panel_request.md"
    out.write_text(md, encoding="utf-8")
    return out
