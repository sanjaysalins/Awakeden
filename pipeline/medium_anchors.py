"""Style-anchor prompt templates for the Stationer -- THE ONLY legal source
of prompt text for a "tipped-in paper medium" spread in the living-sketchbook
pipeline (see .claude/skills/living-sketchbook/MEDIUM_SELECTION.md). Never
hand-type a raw prompt string at a call site -- always go through
`build_prompt()` below or `pipeline/medium_registry.py`'s `Medium.prompt()`.

Promoted 2026-08-11 from the retired Drawing Office POC pipeline
(`drawing_office/prompts/style_anchors.py`) -- the prompt text is unchanged,
only its home moved.

Every anchor is illustration-mode by construction (positively asserts
"illustration"/"hand-drawn"/"ink" and never contains banned photoreal-drift
words). Every GUARDRAIL suffix bans legible text -- all real lettering is a
code overlay applied after render (Scribed Ink / marginalia / typography_panel),
per this project's standing LAW 1.

Proven this week, not invented today:
- SKETCH  -> living-sketchbook family (Sightline, Third Line: zero drift, most
  authentic "sketchbook" feel of the whole project).
- SURVEY_PLATE -> Far Corner / Sounding Line family (archaeological/technical
  cutaway register).
- ARCHIVE -> Closed File family (museum-catalogue *illustration*, never
  "museum photograph" -- the anchor explicitly forbids the photo drift that
  word combination caused elsewhere).
- LEDGER -> Double-Entry Page family (scribe's ledger, ruled paper).
- SCROLL -> One-Take Scroll family (rewritten post-drift: the original
  "photographed museum artifact" framing is exactly what broke it).
- NIGHT_INK -> The Token family (flat night ink-wash; explicitly bans
  "torchlight glow" and lens/cinema vocabulary, the specific phrase that
  caused drift there, use "pale wash reserve" instead).
"""
from __future__ import annotations

GUARDRAIL = (
    ", absolutely no legible text, no legible lettering, no readable words or "
    "numerals anywhere in the image, no modern objects or clothing, reverent "
    "and dignified tone, ancient Near-Eastern or period-appropriate setting "
    "only, fully and modestly clothed, no gore, no nsfw"
)

SKETCH = (
    "Hand-drawn editorial sketch illustration, ink linework with muted "
    "watercolor wash on aged sketchbook paper, journal-style, restrained "
    "earth and sepia palette, warm and painterly, not photographic, not a "
    "photograph, drawn and inked by hand"
)

SURVEY_PLATE = (
    "Detailed archaeological/scientific cutaway engraving, cutaway diagram "
    "style, muted mineral ink-wash palette of slate blue-grey and faded "
    "sienna, fine technical linework, aged parchment ground, restrained and "
    "scholarly like a 19th-century survey plate, hand-drawn illustration, "
    "not a photograph"
)

ARCHIVE = (
    "Antiquarian archive illustration, ink and muted wash on aged card "
    "stock, warm low lamplight, meticulous cross-hatched linework, "
    "restrained scholarly palette of sepia, slate and faded ochre, like a "
    "19th-century accession-catalogue engraving -- a DRAWN illustration in "
    "this style, never an actual photograph of an archive or a physical prop"
)

LEDGER = (
    "Scribe's ledger page illustration, aged cream paper, fine hand-ruled "
    "ink lines, restrained sepia and rubric-red palette, like an old "
    "accounting book rendered as hand-drawn illustration -- flat, drawn, "
    "not a photograph of a physical book"
)

SCROLL = (
    "Ancient scroll illustration, aged papyrus-toned ground, fine sepia ink "
    "linework, restrained scholarly palette, hand-drawn flat illustration "
    "of a scroll -- explicitly NOT a photograph, not a museum artifact "
    "photo, not under glass, not a display case; render as a drawn/painted "
    "surface the way an illuminated-manuscript illustration would be drawn"
)

NIGHT_INK = (
    "Flat hand-drawn ink-wash illustration on aged paper, editorial sketch "
    "style, restrained muted night palette of deep blue-grey and warm ochre "
    "pale wash reserve for light, paper tooth visible, not photographic, not "
    "a photograph, drawn and inked by hand"
)

# Registry-name -> anchor, so pipeline code can look up the right anchor from
# a device card without hardcoding strings at call sites.
ANCHOR_BY_SHAPE_FAMILY = {
    "geography": SURVEY_PLATE,
    "depth": SURVEY_PLATE,
    "elevation": SKETCH,
    "convergence": SKETCH,
    "taxonomy": ARCHIVE,
    "correspondence": LEDGER,
    "grammar": LEDGER,
    "reading-in-motion": SCROLL,
    "threshold": NIGHT_INK,
    "echo": SKETCH,
    "interruption": SKETCH,
    "attention": SKETCH,
    "trace": SKETCH,
    "scrutiny": SKETCH,
    "sequence": SKETCH,
}


def build_prompt(anchor: str, subject: str, guardrails: bool = True) -> str:
    """anchor: one of the module-level constants above (or a custom string).
    subject: the per-plate subject/mood description. guardrails=False only
    for debugging -- pipeline code must never disable this for a real render."""
    prompt = f"{anchor}. {subject.strip()}"
    if guardrails:
        prompt += GUARDRAIL
    return prompt
