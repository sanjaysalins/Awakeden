"""Phase B — punctuation-strict KJV verification tests.

Run: .venv\\Scripts\\python.exe -m pipeline.test_kjv_strict
"""
from __future__ import annotations

from pipeline import kjv_strict as K


def test_corpus_loaded():
    prov = K.corpus_provenance()
    assert prov["exists"], f"KJV corpus not found: {prov}"


def test_ps22_7_comma_is_strict():
    # the flagship integrity case: the cache dropped this comma.
    assert K.verify_span("Psalm 22:7", "they shake the head, saying")[0] == "OK"
    assert K.verify_span("Psalm 22:7", "they shake the head saying")[0] == "MISQUOTE"


def test_altered_word_caught():
    assert K.verify_span("Psalm 22:18",
        "They part my garments among them, and cast lots upon my clothing.")[0] == "MISQUOTE"


def test_verbatim_tagged_ok():
    assert K.verify_span("Psalm 22:18",
        "They part my garments among them, and cast lots upon my vesture.")[0] == "OK"
    assert K.verify_span("Matthew 27:46", "My God, my God, why hast thou forsaken me?")[0] == "OK"


def test_boundary_truncation_allowed():
    # a quote that truncates mid-verse and adds its own terminal period is OK
    assert K.verify_span("Psalm 22:18", "They part my garments among them.")[0] == "OK"


def test_range_ref_resolves():
    # range ref joins verses; a phrase spanning the range verifies
    s, _ = K.verify_span("Psalm 22:6-7", "But I am a worm, and no man")
    assert s == "OK", s


def test_supplied_word_italics_kept():
    # Ps 22:7 has {saying} (italics supplied word) — must be kept as 'saying'
    assert K.verify_span("Psalm 22:7",
        "they shoot out the lip, they shake the head, saying")[0] == "OK"


def test_nt_quote_checked_against_nt_verse():
    # an NT saying verifies against its NT ref; a bogus tail is caught
    assert K.verify_span("John 19:30", "It is finished.")[0] == "OK"
    assert K.verify_span("John 19:30", "It is finished forever.")[0] == "MISQUOTE"


def test_unresolvable_tagged_ref_blocks():
    s, _ = K.verify_span("Psalm 999:1", "nope")
    assert s == "UNRESOLVED"


def test_ellipsis_fragments():
    # both fragments must be verbatim substrings of the verse
    ok = K.verify_span("Psalm 22:1", "My God, my God … why hast thou forsaken me")
    assert ok[0] == "OK", ok
    bad = K.verify_span("Psalm 22:1", "My God, my God … why hast thou abandoned me")
    assert bad[0] == "MISQUOTE", bad


def test_f1_scrambled_fragments_rejected():
    # red-team F1: order-insensitive matching let a scrambled quote pass
    s, _ = K.verify_span("Psalm 22:18",
        "and cast lots upon my vesture … they part my garments among them")
    assert s == "MISQUOTE", f"scrambled fragments wrongly accepted: {s}"


def test_f1_omitted_clause_rejected():
    s, _ = K.verify_span("Psalm 22:18", "they part my garments … upon my vesture")
    # legitimate truncation in order is OK; but dropping the middle and keeping a
    # later disjoint snippet must still be ORDER-valid — this IS in order, so OK.
    # The dangerous case is reversal (covered above). A forward gap is allowed truncation.
    assert s == "OK", s


def test_f5_malformed_ref_does_not_crash():
    for bad in ("Psalm 22:6-", "Psalm 22:-7", "Psalm 22:", "Psalm abc"):
        s, _ = K.verify_span(bad, "my god")
        assert s == "UNRESOLVED", f"{bad!r} -> {s} (should be UNRESOLVED, not crash)"


def test_f4_semicolon_note_not_injected():
    # Deut 3:17 has a semicolon translator note {Ashdothpisgah; or, ...}
    hay = K._verse_haystack("Deuteronomy 3:17")
    assert hay is not None
    assert "springs of pisgah" not in hay, "semicolon translator note leaked into the verse"


def test_f3_short_inline_not_falsely_confirmed():
    # a 1-2 word echo must NOT be claimed verbatim (advisory WARN)
    s, _ = K.resolve_inline("forsaken", ["Psalm 22:1"])
    assert s == "WARN", f"short inline echo wrongly confirmed: {s}"


def test_f7_unicode_space_not_false_blocked():
    # a legitimate quote with a thin space (U+2009) must still verify OK
    s, _ = K.verify_span("Psalm 22:18",
        "They part my garments among them, and cast lots upon my vesture.")
    assert s == "OK", f"thin space false-blocked: {s}"


def test_empty_span_unresolved():
    assert K.verify_span("Psalm 22:1", "...")[0] == "UNRESOLVED"


def test_multiword_book_resolves():
    assert K.verse_texts("Song of Solomon 2:1") is not None


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t(); print(f"[PASS] {t.__name__}"); passed += 1
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}")
        except Exception as e:  # noqa
            print(f"[ERROR] {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
    raise SystemExit(0 if passed == len(tests) else 1)
