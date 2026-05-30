"""Exact King James Version verse lookup.

Scripture accuracy is a core differentiator for this ministry, so we fetch the
verbatim KJV text and hand it to the model rather than trusting recall. Results
are cached on disk. If the network is unavailable, we degrade gracefully: the
engine still runs, but the verse is flagged as unverified for the review gate.
"""
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request

import config

_SINGLE_VERSE = re.compile(r"^(.+?)\s+(\d+):(\d+)$")


def _load_cache() -> dict[str, str]:
    if config.SCRIPTURE_CACHE_PATH.exists():
        try:
            return json.loads(config.SCRIPTURE_CACHE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def _save_cache(cache: dict[str, str]) -> None:
    config.SCRIPTURE_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    config.SCRIPTURE_CACHE_PATH.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def fetch_kjv(reference: str, timeout: float = 10.0) -> str | None:
    """Return the exact KJV text for a reference, or None if it can't be fetched.

    Uses bible-api.com (public, no key, KJV translation). Cached on disk so a
    reference is fetched at most once.
    """
    reference = reference.strip()
    if not reference:
        return None

    cache = _load_cache()
    if reference in cache:
        return cache[reference]

    url = (
        "https://bible-api.com/"
        + urllib.parse.quote(reference)
        + "?translation=kjv"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "JesusInTheBible/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None  # offline / lookup failed — caller treats verse as unverified

    text = (data.get("text") or "").strip()
    # Collapse the API's internal newlines into clean single spaces.
    text = " ".join(text.split())
    if not text:
        return None

    cache[reference] = text
    _save_cache(cache)
    return text


def _context_reference(reference: str, window: int = 2) -> str:
    """Expand a single-verse ref to a small range for context.

    'John 10:9' -> 'John 10:7-11'. References that are already ranges or lists
    (contain '-' or ',') are returned unchanged.
    """
    reference = reference.strip()
    if "-" in reference or "," in reference:
        return reference
    m = _SINGLE_VERSE.match(reference)
    if not m:
        return reference
    book, chap, verse = m.group(1), int(m.group(2)), int(m.group(3))
    start = max(1, verse - window)
    end = verse + window
    return f"{book} {chap}:{start}-{end}"


def fetch_kjv_context(reference: str, window: int = 2, timeout: float = 10.0) -> str | None:
    """Fetch the verse plus a few neighbours, so the reviewer can judge whether the
    narration uses the verse in context (not proof-texting). Best-effort/cached.
    """
    return fetch_kjv(_context_reference(reference, window), timeout=timeout)


def fetch_kjv_passage(reference: str, window: int = 8, timeout: float = 10.0) -> str | None:
    """Fetch a wider pericope with verse markers preserved.

    Used by thread discovery (and by reviewers, in place of the narrower ±2
    context) so the model can mine the surrounding text for an overlooked
    detail, original-language reveal, NT-confirmed OT echo, or cultural-
    historical hook — and pin its chosen thread to a specific verse.

    Returns numbered lines like:
        [4:7] There cometh a woman of Samaria to draw water: ...
        [4:8] (For his disciples were gone away unto the city ...)
    Best-effort/cached. Returns None on lookup failure.
    """
    expanded = _context_reference(reference, window)
    if not expanded:
        return None

    cache = _load_cache()
    cache_key = f"passage:{expanded}"
    if cache_key in cache:
        return cache[cache_key]

    url = (
        "https://bible-api.com/"
        + urllib.parse.quote(expanded)
        + "?translation=kjv"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "JesusInTheBible/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None  # offline / lookup failed — caller treats passage as missing

    verses = data.get("verses") or []
    lines: list[str] = []
    for v in verses:
        chap = v.get("chapter")
        num = v.get("verse")
        text = (v.get("text") or "").strip()
        text = " ".join(text.split())
        if not text or chap is None or num is None:
            continue
        lines.append(f"[{chap}:{num}] {text}")
    if not lines:
        return None

    passage = "\n".join(lines)
    cache[cache_key] = passage
    _save_cache(cache)
    return passage
