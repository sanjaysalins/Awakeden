"""Deterministic KJV-verbatim check (calibration proposal #1).

The LLM review is supposed to verify quoted scripture is KJV-verbatim, but it
misses things a string compare never would — e.g. Matthew 8:27 ends with '!' and a
draft quoted it with '?', and all of self-review + independent audit rated G1 PASS
while 5 external LLMs caught it.

This runs a normalize-and-substring check of every DOUBLE-QUOTED span in the draft
against the cached KJV pericope:
  - exact (case-insensitive, whitespace-normalized) substring  -> OK
  - body matches but terminal punctuation differs              -> 'punctuation' (high confidence error)
  - >=70% content-word overlap but not verbatim                -> 'wording' (likely a near-miss)
  - low overlap                                                -> ignored (paraphrase, or a cross-ref
                                                                  quote not in the primary pericope —
                                                                  we can't verify those here, so we
                                                                  do NOT false-flag them)

Quotes shorter than 3 words are skipped (too short to judge). Only the PRIMARY
pericope is the source of truth; NT cross-references (1 Peter, etc.) are not in it
and fall through to 'ignored', which is the safe default.
"""
from __future__ import annotations

import re

_PUNCT = "!?.,;:—-"


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def find_quoted_spans(text: str) -> list[str]:
    return re.findall(r'"([^"]+)"', text)


def _content_overlap(chunk: str, passage_low: str) -> float:
    words = [w for w in re.findall(r"[a-z']+", chunk.lower()) if len(w) > 2]
    if not words:
        return 0.0
    hits = sum(1 for w in words if w in passage_low)
    return hits / len(words)


def verbatim_mismatches(full_text: str, passage: str | None) -> list[dict]:
    """Return a list of {quote, kind, detail} for quoted spans that look like they
    were meant to be KJV but are not verbatim against the pericope."""
    if not passage:
        return []
    kjv = _norm(passage)
    kjv_low = kjv.lower()
    issues: list[dict] = []
    seen: set[str] = set()
    for span in find_quoted_spans(full_text):
        for chunk in re.split(r"\s*(?:\.\.\.|…)\s*", span):
            c = _norm(chunk)
            key = c.lower()
            if len(c.split()) < 3 or key in seen:
                continue
            if key in kjv_low:
                seen.add(key)
                continue  # exact verbatim
            stripped = c.strip(_PUNCT).strip()
            if stripped and stripped.lower() in kjv_low:
                seen.add(key)
                # The wording is in the KJV. A punctuation DEFECT only exists when the
                # quote ends exactly where a KJV SENTENCE ends but uses a different
                # sentence-ender (the Matt 8:27 '!'-vs-'?' case). If the KJV continues
                # with a comma/colon/more words, the quote merely TRUNCATED mid-verse and
                # any closing '.' is fine — not an error.
                idx = kjv_low.find(stripped.lower())
                after = kjv_low[idx + len(stripped):].lstrip()
                kjv_next = after[:1]
                q_end = c.rstrip()[-1:] if c.rstrip()[-1:] in ".!?" else ""
                if kjv_next in "!?." and q_end and q_end != kjv_next:
                    issues.append({
                        "quote": c, "kind": "punctuation",
                        "detail": f"KJV ends this sentence with '{kjv_next}' but the quote used '{q_end}'",
                    })
                continue  # truncation or matching terminal punctuation -> fine
            ov = _content_overlap(stripped or c, kjv_low)
            if ov >= 0.70:
                seen.add(key)
                issues.append({
                    "quote": c, "kind": "wording",
                    "detail": f"~{int(ov * 100)}% word overlap with the pericope but NOT verbatim — check against the KJV",
                })
            # else: low overlap -> not a primary-pericope quote (paraphrase or cross-ref); skip
    return issues


def summarize(issues: list[dict]) -> str:
    return "; ".join(f'[{i["kind"]}] "{i["quote"]}" — {i["detail"]}' for i in issues)
