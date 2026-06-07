"""Acceptance + regression fixtures for the parser + cluster gate (Phase A).

THE gate for the whole hardening effort: it must catch, on the templated Psalm 22
shorts, the exact repetition that per-artifact review could never see — and it must
NOT fire on legitimate variety or push a writer to alter Scripture.

Positive fixtures are SNAPSHOTTED inline (not read from the live narration.md) so
that de-templating the real shorts — the gate's own goal — does not break this test.
A separate live-file test only asserts the parser still extracts non-empty content.

Run: .venv\\Scripts\\python.exe -m pipeline.test_cluster_gate
"""
from __future__ import annotations

from pathlib import Path

from pipeline import cluster_gate as CG
from pipeline import narration_parse as NP

_REPO = Path(__file__).resolve().parent.parent
_SHORTS = _REPO / "longform" / "02_Psalm_22_Song_From_The_Cross" / "v1" / "shorts"


def _short(hook: str, cta: str, *, ref: str = "Psalm 22:18", quote: str = "the verse text here and more") -> str:
    return (f"# T\n- **Series:** x\n---\n\n**[narrator]**\n{hook}\n\n"
            f"**[narrator — KJV, {ref}]**\n\"{quote}\"\n\n**[narrator]**\n{cta}\n\n"
            f"---\n## DEPTH & SOURCING\nledger not spoken\n")


# Snapshot of the 8 shipped closers (7 identical + #02's lowercase em-dash variant)
# and the "thousand years" hook family.
_TEMPLATED = [
    ("01", _short("A thousand years before a Roman cross, a king wrote a song.", "Come to Him.")),
    ("02", _short("A thousand years before the cross, David wrote down the words.", "That's Jesus — come to him.")),
    ("03", _short("The most desolate words Jesus ever spoke, a thousand years before.", "Come to Him.")),
    ("04", _short("Psalm twenty-two is the psalm Jesus quoted from the cross.", "Come to Him.")),
    ("05", _short("The last line of Psalm twenty-two, a thousand years apart.", "Come to Him.")),
    ("06", _short("The psalm Jesus cried from the cross begins in agony.", "Come to Him.")),
    ("07", _short("A king once wrote a death, a thousand years before Rome.", "Come to Him.")),
    ("08", _short("A thousand years before the cross, a song wrote the thirst.", "He went dry, so come to Him and drink.")),
]


def test_parser_fail_closed_on_empty():
    # truly empty (only a heading + rule + a DEPTH ledger; no spoken prose) must raise.
    # NOTE: plain prose IS now valid (engine format) — only a no-spoken-text doc fails.
    try:
        NP.parse("# Title\n\n---\n\n## DEPTH & SOURCING\nledger line not spoken\n")
    except NP.EmptyNarrationError:
        return
    raise AssertionError("parser did not fail-closed on a no-spoken-text narration")


def test_live_shorts_parse_nonempty():
    paths = sorted(_SHORTS.glob("0*/narration.md"))
    assert len(paths) == 8
    for p in paths:
        nar = NP.parse(p.read_text(encoding="utf-8"))
        assert nar.spoken_text and nar.cta and nar.hook, f"{p.parent.name}: empty extraction"


def test_cta_repetition_flagged_8_of_8():
    rep = CG.cluster_check(_TEMPLATED, within_cluster=True)
    come = [f for f in rep.findings if f.kind == "cta_repetition" and "come to him" in f.phrase]
    assert come, "the 'come to him' CTA shape was NOT flagged"
    assert len(come[0].members) == 8, f"expected 8/8, got {len(come[0].members)}: {come[0].members}"
    assert come[0].blocking


def test_opener_family_flagged():
    rep = CG.cluster_check(_TEMPLATED, within_cluster=True)
    ty = [f for f in rep.findings if f.kind == "opener_repetition" and "thousand years" in f.phrase]
    assert ty and len(ty[0].members) >= 4, f"'thousand years' family not flagged: {ty}"


def test_real_cluster_is_blocked():
    assert not CG.cluster_check(_TEMPLATED, within_cluster=True).passed


def test_synthetic_ninth_come_to_him_regression():
    arts = _TEMPLATED + [("09", _short("A brand new and totally different hook.", "A fresh closing thought. Come to Him."))]
    rep = CG.cluster_check(arts, within_cluster=True)
    come = [f for f in rep.findings if f.kind == "cta_repetition" and "come to him" in f.phrase]
    assert come and "09" in come[0].members, "synthetic 9th 'Come to Him' short not caught"


def test_does_not_ban_distinct_gospel_ctas():
    a = _short("Hook one is unique.", "So run to the Saviour today.")
    b = _short("Hook two is also unique.", "Will you kneel before the risen Lord?")
    rep = CG.cluster_check([("a", a), ("b", b)], within_cluster=True)
    assert not rep.blocking, f"falsely blocked distinct gospel CTAs: {[f.phrase for f in rep.blocking]}"


def test_fp3_varied_tail_template_caught_at_least_advisory():
    """Closers that share a template word but vary the tail ('...the gospel') must
    at least be SURFACED (advisory), not silently passed."""
    arts = [
        ("a", _short("Hook a unique.", "And that is the gospel.")),
        ("b", _short("Hook b unique.", "This is the gospel today.")),
        ("c", _short("Hook c unique.", "Here is the gospel, friend.")),
    ]
    rep = CG.cluster_check(arts, within_cluster=True)
    gospel = [f for f in rep.findings if "gospel" in f.phrase]
    assert gospel, "varied-tail 'gospel' template was not surfaced at all"


def test_fb1_themed_series_sharing_the_cross_not_blocked():
    """A crucifixion-themed series whose hooks all say 'the cross' must NOT be
    blocked for sharing the gospel subject (locked rule)."""
    arts = [
        ("a", _short("At the cross, the sky went black.", "Trust the risen Lord.")),
        ("b", _short("Near the cross, the soldiers gambled.", "Believe and live today.")),
        ("c", _short("Beneath the cross, His mother wept.", "Will you turn and follow?")),
    ]
    rep = CG.cluster_check(arts, within_cluster=True)
    cross = [f for f in rep.blocking if "cross" in f.phrase]
    assert not cross, f"falsely BLOCKED a themed series for sharing 'the cross': {[f.phrase for f in cross]}"


def test_short_inline_kjv_not_skipped():
    """FP-1: short KJV sayings must NOT be blanket-exempted from verification."""
    md = ("# T\n---\n**[narrator]**\nHe cried out.\n\n**[narrator]**\n\"It is finished.\"\n\n---\n## DEPTH\nx\n")
    spans = NP.quoted_spans_with_refs(md)
    fin = [s for s in spans if "finished" in s["text"].lower()]
    assert fin and fin[0]["klass"] != "rhetoric", f"short KJV wrongly skipped: {fin}"


def test_tagged_kjv_block_without_quotes_not_skipped():
    """FP-2: a KJV-tagged block with no quote marks must still be verified."""
    md = ("# T\n---\n**[narrator — KJV, Psalm 2:7]**\nThou art my Son.\n\n"
          "**[narrator]**\nClose.\n\n---\n## DEPTH\nx\n")
    spans = NP.quoted_spans_with_refs(md)
    tagged = [s for s in spans if s["klass"] == "tagged_kjv"]
    assert tagged and "son" in tagged[0]["text"].lower(), f"tagged KJV block silently skipped: {spans}"


def test_hyphen_header_ref_not_lost():
    """LS-1: a header using '-' or '--' instead of em-dash must still map the ref."""
    for dash in ("-", "--", "–", "—"):
        md = f"# T\n---\n**[narrator {dash} KJV, John 3:16]**\n\"For God so loved the world\"\n---\n## DEPTH\nx\n"
        spans = NP.quoted_spans_with_refs(md)
        assert spans and spans[0]["ref"] == "John 3:16", f"ref lost with dash {dash!r}: {spans}"


def test_sentence_split_handles_closing_quote():
    """FP-4: a sentence ending inside a closing quote must not swallow the next."""
    s = NP.sentences('He said: "It is finished." Then He died.')
    assert len(s) == 2, f"closing-quote sentence split failed: {s}"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"[PASS] {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}")
        except Exception as e:  # noqa
            print(f"[ERROR] {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
    raise SystemExit(0 if passed == len(tests) else 1)
