"""Punctuation-STRICT KJV verbatim verification (Phase B).

Closes two root causes:
  1. `data/kjv_cache.json` (bible-api) is corrupt — it dropped the Ps 22:7 comma
     (`"shake the head saying"` vs the 1769 `"shake the head, saying"`).
  2. `short_gate.kjv` compares against a CORRECT corpus but its `norm()` STRIPS
     punctuation, so its verbatim check is punctuation-BLIND and misses the comma.

This module verifies against a PINNED local copy of the proven HF-POC 1769 corpus
(`data/kjv_corpus.json`, provenance in `data/kjv_corpus.provenance.json`) with a
punctuation-PRESERVING, ORDER-PRESERVING comparison. The corpus is the reused asset;
ref-parsing/verse-lookup are owned here (robust against malformed refs + multi-word
book names — the sibling `short_gate.kjv` crashes on `22:6-` and can't parse
"Song of Solomon").

Rules (hardened after a code red-team + 5-CLI panel):
  - tagged-KJV span → verified strict against its verse; mismatch / unresolvable
    ref → BLOCKING. Empty/punctuation-only span → UNRESOLVED (never OK).
  - ellipsis `…`/`...` fragments must match IN ORDER and NON-OVERLAPPING (a
    scrambled or clause-omitted quote is NOT verbatim).
  - interior punctuation MUST match (catches the comma); a trailing terminal
    `.!?`/quote on a fragment is allowed (honest truncation at the boundary).
  - translator-note braces (`{...: ...}`, `{...; or, ...}`, Heb./Gr. glosses) are
    removed; supplied-word italics (`{saying}`) are KEPT.
  - inline (untagged) echoes → best-effort resolved per-VERSE within the chapters
    the narration cites, with a min-length floor; not-confirmable → advisory WARN,
    never blocking.
"""
from __future__ import annotations

import json
import os
import re
from functools import lru_cache
from pathlib import Path

from pipeline import narration_parse as NP

_REPO = Path(__file__).resolve().parent.parent
_PINNED = _REPO / "data" / "kjv_corpus.json"
_FALLBACK = Path(r"C:\Users\sanjay\PycharmProjects\HF-POC\series\03_furgiven\tools\data\kjv.json")

_ALIASES = {
    "psalm": "psalms", "ps": "psalms", "song of songs": "song of solomon",
    "songofsongs": "song of solomon", "matt": "matthew", "mt": "matthew",
    "mk": "mark", "lk": "luke", "jn": "john", "rom": "romans", "deut": "deuteronomy",
    "isa": "isaiah", "jer": "jeremiah", "ezek": "ezekiel", "dan": "daniel",
    "heb": "hebrews", "rev": "revelation", "gen": "genesis", "ex": "exodus", "exod": "exodus",
    "lev": "leviticus", "num": "numbers", "phil": "philippians", "cor": "corinthians",
}


def _corpus_path() -> Path | None:
    env = os.getenv("JESUS_KJV_CORPUS")
    for p in (Path(env) if env else None, _PINNED, _FALLBACK):
        if p and p.is_file():
            return p
    return None


@lru_cache(maxsize=1)
def _by_name() -> dict[str, dict]:
    """Lazy-load the pinned corpus into {book_name_lower: book}. Fail-closed."""
    path = _corpus_path()
    if path is None:
        raise FileNotFoundError(
            "KJV corpus not found (data/kjv_corpus.json or $JESUS_KJV_CORPUS). "
            "KJV verification cannot run without it (fail-closed)."
        )
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return {b["name"].lower(): b for b in data}


def corpus_provenance() -> dict:
    path = _corpus_path()
    prov_file = _REPO / "data" / "kjv_corpus.provenance.json"
    prov = json.loads(prov_file.read_text(encoding="utf-8")) if prov_file.is_file() else {}
    return {"resolved_path": str(path) if path else None,
            "exists": bool(path), **prov}


# ---- reference parsing (robust; multi-word books; never crashes) -------------
_REF_RX = re.compile(r"^\s*((?:[1-3]\s*)?[A-Za-z][A-Za-z ]*?)\s+(\d+)\s*:\s*([\d,\-–—\s]+?)\s*$")


def _resolve_book(token: str) -> dict | None:
    by = _by_name()
    key = re.sub(r"[\s.]", "", token).lower()
    key = re.sub(r"[\s.]", "", _ALIASES.get(token.strip().lower(), key)).lower()
    alias = _ALIASES.get(token.strip().lower())
    if alias and alias in by:
        return by[alias]
    if key in by:
        return by[key]
    # collapse spaces for multi-word match ("song of solomon")
    for nm, book in by.items():
        if nm.replace(" ", "") == key or nm.replace(" ", "").startswith(key):
            return book
    return None


def _verse_numbers(spec: str) -> list[int] | None:
    """Parse '6-7' / '1,3' / '14' into [ints]; None on any malformed part."""
    nums: list[int] = []
    for part in spec.replace("–", "-").replace("—", "-").split(","):
        part = part.strip()
        if not part:
            continue
        try:
            if "-" in part:
                a, b = part.split("-", 1)
                a, b = int(a), int(b)
                if a > b or a < 1:
                    return None
                nums.extend(range(a, b + 1))
            else:
                nums.append(int(part))
        except ValueError:
            return None
    return nums or None


def verse_texts(ref: str) -> list[str] | None:
    """Raw verse strings for a ref (incl. ranges). None if unresolvable."""
    m = _REF_RX.match(ref.strip())
    if not m:
        return None
    try:
        book = _resolve_book(m.group(1))
        chap = int(m.group(2))
    except (ValueError, FileNotFoundError):
        raise
    except Exception:
        return None
    if book is None:
        return None
    nums = _verse_numbers(m.group(3))
    if not nums:
        return None
    chapters = book.get("chapters", [])
    if not (1 <= chap <= len(chapters)):
        return None
    verses = chapters[chap - 1]
    out = [verses[n - 1] for n in nums if 1 <= n <= len(verses)]
    return out or None


# ---- canonicalization (punctuation-preserving) -------------------------------
_UNI_SPACE = re.compile(r"[  -   　]")
_NOTE_RX = re.compile(r"\{[^{}]*(?::|;|\bor,|\bHeb\.|\bGr\.|\bChal\.|\bcalled\b)[^{}]*\}")


def _strip_markers(verse: str) -> str:
    verse = _NOTE_RX.sub(" ", verse)          # translator notes / glosses
    return verse.replace("{", "").replace("}", "")  # keep supplied-word italics


def _canon(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-")
    s = re.sub(r"[*_`]", "", s)
    s = _UNI_SPACE.sub(" ", s)
    s = s.lower()
    s = re.sub(r"\s+", " ", s)
    return s.strip()


_TERMINAL = ' .!?"\''


def _ordered_in(span: str, text: str) -> bool:
    """Every ellipsis fragment of `span` occurs in `text`, IN ORDER and
    non-overlapping (moving cursor). Trailing terminal punctuation on a fragment
    is allowed (truncation); interior punctuation must match."""
    cursor = 0
    for frag in re.split(r"…|\.\.\.", span):
        f = _canon(frag).strip(_TERMINAL)
        if not f:
            continue
        idx = text.find(f, cursor)
        if idx < 0:
            return False
        cursor = idx + len(f)
    return True


def _verse_haystack(ref: str) -> str | None:
    vts = verse_texts(ref)
    if vts is None:
        return None
    return _canon(_strip_markers(" ".join(vts)))


def verify_span(ref: str | None, span: str) -> tuple[str, str]:
    """Verify a TAGGED span against its verse, punctuation+order strict.
    status ∈ {OK, MISQUOTE, UNRESOLVED}."""
    if not ref:
        return ("UNRESOLVED", "no scripture reference for this quoted span")
    if not _canon(span).strip(_TERMINAL):
        return ("UNRESOLVED", "empty / punctuation-only quoted span")
    hay = _verse_haystack(ref)
    if hay is None:
        return ("UNRESOLVED", f"ref {ref!r} not found in the witnessed KJV corpus")
    if _ordered_in(span, hay):
        return ("OK", f"verbatim against {ref}")
    return ("MISQUOTE",
            f"not verbatim against {ref}: {span.strip()[:70]!r} "
            f"(wording / interior punctuation / order differs from the KJV)")


def resolve_inline(span: str, candidate_refs: list[str], *, min_chars: int = 20) -> tuple[str, str]:
    """Best-effort verify an UNTAGGED inline echo against the cited chapters,
    matched per-VERSE (not a chapter-join, so a coincidental cross-verse hit can't
    pass). Short spans can't be confirmed → WARN. Never blocking."""
    canon = _canon(span).strip(_TERMINAL)
    if len(canon) < min_chars:
        return ("WARN", f"inline echo {span.strip()[:40]!r} too short to confirm verbatim (advisory)")
    seen_chapters: set[tuple[str, int]] = set()
    for ref in candidate_refs:
        m = _REF_RX.match(ref.strip())
        if not m:
            continue
        try:
            book = _resolve_book(m.group(1))
            chap = int(m.group(2))
        except Exception:
            continue
        if book is None or (book["name"], chap) in seen_chapters:
            continue
        seen_chapters.add((book["name"], chap))
        chapters = book.get("chapters", [])
        if not (1 <= chap <= len(chapters)):
            continue
        for verse in chapters[chap - 1]:
            if _ordered_in(span, _canon(_strip_markers(verse))):
                return ("OK", f"inline echo located verbatim in {book['name']} {chap} (cited chapter)")
    return ("WARN",
            f"inline echo {span.strip()[:50]!r} not located verbatim in the cited "
            f"chapters — confirm it is KJV or an intentional paraphrase (advisory)")


# ---- narration-level + audit -------------------------------------------------
def verify_narration(md: str) -> list[dict]:
    """status ∈ {OK, MISQUOTE(block), UNRESOLVED(block), WARN(advisory)}."""
    spans = NP.quoted_spans_with_refs(md)
    candidate_refs = [s["ref"] for s in spans if s["klass"] == "tagged_kjv" and s["ref"]]
    findings: list[dict] = []
    for s in spans:
        if s["klass"] == "rhetoric":
            continue
        if s["klass"] == "tagged_kjv":
            status, detail = verify_span(s["ref"], s["text"])
        else:
            status, detail = resolve_inline(s["text"], candidate_refs)
        findings.append({**s, "status": status, "detail": detail,
                         "blocking": status in ("MISQUOTE", "UNRESOLVED")})
    return findings


def audit_paths(paths: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for p in paths:
        try:
            for f in verify_narration(p.read_text(encoding="utf-8")):
                rows.append({"file": str(p), **f})
        except NP.EmptyNarrationError as e:
            rows.append({"file": str(p), "text": "", "ref": None, "klass": "parse",
                         "status": "UNRESOLVED", "blocking": True, "detail": f"parse: {e}"})
    return rows
