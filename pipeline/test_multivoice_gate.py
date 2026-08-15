"""G9 Multi-voice gate tests.

Locked 2026-08-14 after a confirmed project-wide regression: God's own
Exodus 12:5 words shipped as plain narrator prose in
`39_The_Longer_They_Looked` while sibling pieces in the same batch
correctly split a voice, and the review pipeline had NO gate catching it.
Cases below are the real narrations that motivated the fix, not
synthetic examples.

Run: .venv\\Scripts\\python.exe -m pytest pipeline/test_multivoice_gate.py -q
"""
from __future__ import annotations

from pipeline.engine import _apply_multivoice_gate
from pipeline.models import Beat, Draft, Review


def _rev() -> Review:
    return Review(panel=[], gates=[], overall="LOCKED", priority_fixes=[])


def _gate(rev: Review) -> tuple[str, str] | None:
    hits = [g for g in rev.gates if g.gate.upper().startswith("G9")]
    return (hits[0].gate, hits[0].verdict) if hits else None


def test_no_quote_is_silent():
    draft = Draft(title="t", hook_type="x", beats=[Beat("hook", "no quote here")],
                  scripture_reference="John 3:16", scripture_quoted="", speakers=[])
    out = _apply_multivoice_gate(_rev(), draft)
    assert _gate(out) is None
    assert out.overall == "LOCKED"


def test_voice_already_present_is_silent():
    draft = Draft(
        title="t", hook_type="x",
        beats=[Beat("proof", 'To the serpent God says, "And I will put enmity between thee and the woman."')],
        scripture_reference="Genesis 3:15", scripture_quoted="And I will put enmity...",
        speakers=["god"])
    out = _apply_multivoice_gate(_rev(), draft)
    assert _gate(out) is None
    assert out.overall == "LOCKED"


def test_real_regression_case_flags_conditional():
    # 39_The_Longer_They_Looked: no attribution phrase in the text at all --
    # a divine-speech-pattern regex would miss this; the coarse "any quote,
    # zero voices" check is what actually catches it.
    draft = Draft(
        title="t", hook_type="x",
        beats=[
            Beat("hook", "You'd think the safest way to pick a sacrifice is fast, before "
                          "anyone looks closely. God did the opposite."),
            Beat("point", "He made Israel watch their lamb four straight days - the longer "
                           "they looked, the more certain they were."),
            Beat("proof", '"Your lamb shall be without blemish, a male of the first year... '
                           'ye shall keep it up until the fourteenth day of the same month." '
                           "Call it overkill."),
        ],
        scripture_reference="Exodus 12:5",
        scripture_quoted="Your lamb shall be without blemish...", speakers=[])
    out = _apply_multivoice_gate(_rev(), draft)
    assert _gate(out) == ("G9 Multi-voice", "CONDITIONAL")
    assert out.overall == "LOCKED"  # advisory, does not force REVISE


def test_pauline_epistle_exemption_stays_conditional_not_fail():
    # Her Seed's own Galatians 4:4 quote -- an unvoiced epistle line is a
    # real gap now (2026-08-15: the constitution says it should get the
    # `scripture` voice, not stay narrator-only), but the deterministic gate
    # still can't reliably auto-classify dramatized-vs-citation from text
    # alone, so this stays CONDITIONAL (a human call), not a hard FAIL.
    draft = Draft(
        title="t", hook_type="x",
        beats=[Beat("proof",
            "Paul writes: 'But when the fulness of the time was come, God sent forth his "
            "Son, made of a woman, made under the law.' Paul could have written son of "
            "David, son of Abraham.")],
        scripture_reference="Galatians 4:4",
        scripture_quoted="But when the fulness of the time was come...", speakers=[])
    out = _apply_multivoice_gate(_rev(), draft)
    assert _gate(out) == ("G9 Multi-voice", "CONDITIONAL")
    assert out.overall == "LOCKED"


def test_explicit_spoken_attribution_hard_fails():
    # the narration's OWN words frame this as spoken dialogue -- unambiguous.
    draft = Draft(
        title="t", hook_type="x",
        beats=[Beat("proof",
            'To the serpent God says, "And I will put enmity between thee and the woman, '
            'and between thy seed and her seed." Only then does He turn to Eve.')],
        scripture_reference="Genesis 3:15",
        scripture_quoted="And I will put enmity...", speakers=[])
    out = _apply_multivoice_gate(_rev(), draft)
    assert _gate(out) == ("G9 Multi-voice", "FAIL")
    assert out.overall == "REVISE"


def test_fail_does_not_downgrade_non_locked_overall():
    draft = Draft(
        title="t", hook_type="x",
        beats=[Beat("proof", 'The LORD said, "Let there be light."')],
        scripture_reference="Genesis 1:3", scripture_quoted="Let there be light",
        speakers=[])
    rev = Review(panel=[], gates=[], overall="REVISE", priority_fixes=["some other fix"])
    out = _apply_multivoice_gate(rev, draft)
    assert _gate(out) == ("G9 Multi-voice", "FAIL")
    assert out.overall == "REVISE"
    assert "some other fix" in out.priority_fixes
