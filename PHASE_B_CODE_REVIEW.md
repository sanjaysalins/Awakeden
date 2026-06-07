# Phase B — KJV punctuation-strict verification (code for review)

Context: Scripture was trusted from a corrupt cache (data/kjv_cache.json dropped the Ps 22:7
comma); and short_gate's existing verbatim check uses a punctuation-BLIND norm() so it would
miss the comma even against the correct HF-POC corpus. Phase B REUSES short_gate/kjv.py (corpus
load + ref parse + verse lookup, via real import — not a copy) and adds a punctuation-PRESERVING
comparison. Tagged-KJV refs are verified strict (mismatch/unresolvable = BLOCKING); untagged
inline echoes are best-effort resolved against the chapters the narration cites (not-located =
advisory WARN, never block). REVIEW for: false-PASS (a real misquote slips through), false-BLOCK
(a correct quote flagged), marker/italics handling, range refs, NT-vs-OT, ellipsis, robustness.

B1 audit result on the real 10 narrations: 55 KJV-claimed spans, 54 OK, 0 blocking, 1 advisory
WARN (a long-form inline echo wrote 'my brethren,' where KJV Ps 22:22 has 'my brethren:').

## pipeline/kjv_strict.py
```python
"""Punctuation-STRICT KJV verbatim verification (Phase B).

Two root causes this closes:
  1. `data/kjv_cache.json` (bible-api) is corrupt — it dropped the Ps 22:7 comma
     (`"shake the head saying"` vs the 1769 `"shake the head, saying"`). The engine
     trusts it blindly.
  2. The existing `short_gate.kjv.check_quote` compares against a CORRECT corpus
     (HF-POC `kjv.json` HAS the comma) but its `norm()` STRIPS punctuation, so the
     verbatim check is punctuation-BLIND and would miss the comma anyway.

This module REUSES `short_gate/kjv.py` (corpus loader + ref parsing + verse lookup
— real import, not a copy) and adds a punctuation-PRESERVING comparison on top:
  - interior punctuation MUST match (catches the dropped/added comma);
  - a trailing terminal `.`/`!`/`?` on a quote fragment is allowed (honest
    truncation / added sentence-ender at the quote boundary);
  - `…`/`...` splits a quote into fragments, each verified as a contiguous
    substring of its OWN tagged verse (so an NT quote is checked against the NT
    verse, never the Masoretic OT verse it alludes to — no LXX false-fail);
  - translator-note markers `{shoot...: Heb. open}` are removed; supplied-word
    italics `{saying}` are KEPT as `saying` (so Ps 22:7's comma case is exact).

Fail-closed: an unresolvable / unwitnessed ref is a BLOCKING finding, never a
silent pass.
"""
from __future__ import annotations

import importlib.util
import os
import re
from pathlib import Path

from pipeline import narration_parse as NP

# ---- locate + import short_gate/kjv.py (reuse, don't fork) --------------------
_KNOWN = [
    os.getenv("JITB_SHORT_GATE_KJV", ""),
    r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\short_gate\kjv.py",
]


def _load_sg_kjv():
    here = Path(__file__).resolve()
    # also try a sibling-repo relative path so this isn't machine-pinned
    rel = here.parents[2] / "PythonProject1" / "jesus" / "narration" / "short_gate" / "kjv.py"
    for cand in [*_KNOWN, str(rel)]:
        if cand and Path(cand).is_file():
            spec = importlib.util.spec_from_file_location("sg_kjv", cand)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  # type: ignore[union-attr]
            return mod, Path(cand)
    raise FileNotFoundError(
        "short_gate/kjv.py not found — set JITB_SHORT_GATE_KJV to its path. "
        "KJV verification cannot run without the corpus (fail-closed)."
    )


_SG, _SG_PATH = _load_sg_kjv()


def corpus_provenance() -> dict:
    """Where the corpus + verifier came from (drift/provenance record)."""
    corpus = _SG.resolve_kjv_path()
    return {
        "verifier": str(_SG_PATH),
        "corpus": str(corpus) if corpus else None,
        "corpus_exists": bool(corpus and Path(corpus).is_file()),
    }


# ---- punctuation-preserving canonicalization ---------------------------------
def _strip_markers(verse: str) -> str:
    """Remove translator-note braces `{...: ...}`; KEEP supplied-word italics
    `{saying}` as `saying` (mirrors short_gate.kjv.norm's brace handling)."""
    verse = re.sub(r"\{[^{}]*:[^{}]*\}", " ", verse)   # notes
    return verse.replace("{", "").replace("}", "")      # keep italic words


def _canon(s: str) -> str:
    """Lowercase, fold smart quotes/dashes, collapse whitespace — but KEEP interior
    punctuation (the whole point of strict mode)."""
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-")
    s = re.sub(r"[*_`]", "", s)
    s = s.lower()
    s = re.sub(r"\s+", " ", s)
    return s.strip()


_TERMINAL = ' .!?"\'’”'


def _verse_text(ref: str) -> str | None:
    """Resolve a ref (incl. ranges like 'Psalm 22:6-7') to its canonical verse text."""
    by_name = _SG.load_kjv_by_name()
    m = _SG.REF_RX.match(ref.strip())
    if not m:
        return None
    book = _SG.resolve_book((m.group(1) or "").strip(), by_name)
    if book is None:
        return None
    try:
        chap = int(m.group(2))
    except (TypeError, ValueError):
        return None
    verses = _SG.verses_for(book, chap, m.group(3).strip())
    if not verses:
        return None
    return _canon(_strip_markers(" ".join(verses)))


def _fragments_in(span: str, text: str) -> bool:
    """Every ellipsis-delimited fragment of `span` is a contiguous substring of
    `text` (punctuation-strict, boundary terminal punctuation allowed)."""
    for frag in re.split(r"…|\.\.\.", span):
        f = _canon(frag).strip(_TERMINAL)
        if f and f not in text:
            return False
    return True


def verify_span(ref: str | None, span: str) -> tuple[str, str]:
    """Verify a quoted span against its TAGGED verse, punctuation-strict.

    Returns (status, detail): status in {OK, MISQUOTE, UNRESOLVED}.
    """
    if not ref:
        return ("UNRESOLVED", "no scripture reference for this quoted span")
    verse = _verse_text(ref)
    if verse is None:
        return ("UNRESOLVED", f"ref {ref!r} not found in the witnessed KJV corpus")
    if _fragments_in(span, verse):
        return ("OK", f"verbatim against {ref}")
    return ("MISQUOTE",
            f"not verbatim against {ref}: {span.strip()[:70]!r} "
            f"(interior punctuation / wording differs from the KJV)")


def _chapter_text(ref: str) -> str | None:
    """Canonical text of the WHOLE chapter a ref points to (for inline resolution)."""
    by_name = _SG.load_kjv_by_name()
    m = _SG.REF_RX.match(ref.strip())
    if not m:
        return None
    book = _SG.resolve_book((m.group(1) or "").strip(), by_name)
    if book is None:
        return None
    try:
        chap = int(m.group(2))
    except (TypeError, ValueError):
        return None
    chapters = book.get("chapters", [])
    if not (1 <= chap <= len(chapters)):
        return None
    return _canon(_strip_markers(" ".join(chapters[chap - 1])))


def resolve_inline(span: str, candidate_refs: list[str]) -> tuple[str, str]:
    """Best-effort verify an UNTAGGED inline quote against the chapters the
    narration actually cites. OK if found verbatim in one; WARN (advisory) if it
    can't be located there (a paraphrase or out-of-scope cross-ref — not blocked)."""
    seen: set[str] = set()
    for ref in candidate_refs:
        m = _SG.REF_RX.match(ref.strip())
        key = f"{(m.group(1) if m else '')}|{(m.group(2) if m else '')}"
        if key in seen:
            continue
        seen.add(key)
        text = _chapter_text(ref)
        if text and _fragments_in(span, text):
            return ("OK", f"inline quote located verbatim in {ref.split(':')[0]} (cited chapter)")
    return ("WARN",
            f"inline quote {span.strip()[:60]!r} not located verbatim in the cited "
            f"chapters — confirm it is KJV or an intentional paraphrase")


# ---- narration-level + audit -------------------------------------------------
def verify_narration(md: str) -> list[dict]:
    """Verify every KJV-claimed quoted span in a narration.

    - 'rhetoric'   spans are skipped (explicit non-KJV frames).
    - 'tagged_kjv' spans are verified STRICT against their tagged verse; an
      unresolvable tagged ref or a mismatch is BLOCKING.
    - 'inline_kjv' spans are best-effort resolved against the chapters the
      narration cites; not-located is an advisory WARN, never a block.

    status ∈ {OK, MISQUOTE (block), UNRESOLVED (block), WARN (advisory)}.
    """
    spans = NP.quoted_spans_with_refs(md)
    candidate_refs = [s["ref"] for s in spans if s["klass"] == "tagged_kjv" and s["ref"]]
    findings: list[dict] = []
    for s in spans:
        if s["klass"] == "rhetoric":
            continue
        if s["klass"] == "tagged_kjv":
            status, detail = verify_span(s["ref"], s["text"])
        else:  # inline_kjv
            status, detail = resolve_inline(s["text"], candidate_refs)
        findings.append({**s, "status": status, "detail": detail,
                         "blocking": status in ("MISQUOTE", "UNRESOLVED")})
    return findings


def audit_paths(paths: list[Path]) -> list[dict]:
    """B1 audit: verify every quoted span across a set of narration.md files."""
    rows: list[dict] = []
    for p in paths:
        md = p.read_text(encoding="utf-8")
        for f in verify_narration(md):
            rows.append({"file": str(p), **f})
    return rows
```

## pipeline/test_kjv_strict.py
```python
"""Phase B — punctuation-strict KJV verification tests.

Run: .venv\\Scripts\\python.exe -m pipeline.test_kjv_strict
"""
from __future__ import annotations

from pipeline import kjv_strict as K


def test_corpus_loaded():
    prov = K.corpus_provenance()
    assert prov["corpus_exists"], f"KJV corpus not found: {prov}"


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
```

## Test output
```
[PASS] test_altered_word_caught
[PASS] test_boundary_truncation_allowed
[PASS] test_corpus_loaded
[PASS] test_ellipsis_fragments
[PASS] test_nt_quote_checked_against_nt_verse
[PASS] test_ps22_7_comma_is_strict
[PASS] test_range_ref_resolves
[PASS] test_supplied_word_italics_kept
[PASS] test_unresolvable_tagged_ref_blocks
[PASS] test_verbatim_tagged_ok

10/10 tests passed
```
