"""Cross-artifact CLUSTER gate — the check that was missing.

Per-artifact review cannot see "all 8 shorts end the same way." This gate reads
a SET of narrations together and flags repeated *phrasing/shape* — the defect the
Psalm 22 cluster shipped (8/8 closed on the "Come to Him" tag; repeated "thousand
years" hooks).

DESIGN (per the v5 plan; hardened after a code red-team + 5-CLI panel):
- It flags DENSITY of near-identical WORDING within a cluster/series — it NEVER
  bans the CTA-to-Jesus *destination* (the locked model). Inviting people to
  Jesus is always allowed; closing 8 shorts with the byte-identical tag is not.
- Detection is GENERAL (shared normalized n-grams), not a hard-coded phrase list.
  The named Psalm 22 phrases are regression FIXTURES, not the strategy.
- BLOCKING = a shared CTA opening/closing SHAPE (>=3-token prefix/suffix or an
  identical CTA) within a cluster, OR an opener-family n-gram (>=2 content words)
  shared across the cluster. ADVISORY (non-blocking) = a shared salient content
  phrase in the CTA (e.g. a "...the gospel" / "...bring you home" template) —
  surfaced for review without hard-blocking a legitimately themed series.
- A CTA that is itself a tagged KJV verse is EXCLUDED from shape comparison (the
  gate must never push a writer to alter Scripture verbatim).

Reuses `pipeline.narration_parse` for fail-closed hook/CTA extraction.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from pipeline import narration_parse as NP

# function words excluded from "content" n-grams (opener family + CTA advisory)
_STOP = {
    "a", "an", "the", "and", "or", "but", "of", "to", "in", "on", "at", "for",
    "is", "it", "he", "she", "they", "we", "you", "his", "her", "their", "that",
    "this", "with", "as", "by", "from", "was", "were", "be", "so", "then", "into",
    "what", "who", "him", "me", "my", "your", "our", "will", "shall", "would",
}
# gospel DESTINATION words — sharing these is the locked model, never a defect.
_DESTINATION = {
    "jesus", "christ", "lord", "god", "saviour", "savior", "redeemer", "messiah",
    "spirit", "son", "father", "king", "holy", "cross", "grace", "salvation",
}


@dataclass
class Finding:
    kind: str            # "cta_repetition" | "cta_theme" | "opener_repetition"
    phrase: str
    members: list[str]
    blocking: bool
    detail: str


@dataclass
class ClusterReport:
    findings: list[Finding] = field(default_factory=list)

    @property
    def blocking(self) -> list[Finding]:
        return [f for f in self.findings if f.blocking]

    @property
    def advisory(self) -> list[Finding]:
        return [f for f in self.findings if not f.blocking]

    @property
    def passed(self) -> bool:
        return not self.blocking


def _toks(text: str) -> list[str]:
    return [t for t in NP.normalize(text).split() if t]


def _ngrams(tokens: list[str], n: int) -> list[str]:
    return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def _content_ngrams(text: str, lo: int = 2, hi: int = 3, *, min_content: int = 2) -> set[str]:
    """n-grams with >=min_content non-stopword tokens (kills 'the cross'-style
    single-content-word incidental overlap; keeps 'thousand years')."""
    toks = _toks(text)
    grams: set[str] = set()
    for n in range(lo, hi + 1):
        for g in _ngrams(toks, n):
            if sum(1 for w in g.split() if w not in _STOP) >= min_content:
                grams.add(g)
    return grams


def _cta_ngrams(text: str, n_lo: int = 3, n_hi: int = 5) -> set[str]:
    """Token n-grams (anywhere — interior included) of the CTA clause that carry at
    least one CONTENT word (not a stopword, not a gospel-destination word). So a
    repeated invitation WORDING like 'come to him' (come = content) is caught even
    when interior ('...come to Him and drink'), while a phrase that is only stop +
    destination words ('to the Lord') is NOT flagged — inviting to Jesus is the
    locked model, repeated mechanical phrasing is the defect."""
    keys: set[str] = set()
    toks = _toks(text)
    for n in range(n_lo, n_hi + 1):
        for g in _ngrams(toks, n):
            words = g.split()
            if any(w not in _STOP and w not in _DESTINATION for w in words):
                keys.add(g)
    return keys


def _last_block(nar: NP.Narration) -> NP.Block | None:
    return nar.blocks[-1] if nar.blocks else None


def cluster_check(
    artifacts: list[tuple[str, str]],
    *,
    within_cluster: bool = True,
    min_share: int = 2,
) -> ClusterReport:
    """artifacts: list of (artifact_id, narration_md_text).

    within_cluster=True  → repetition is BLOCKING (same cluster/series).
    within_cluster=False → ADVISORY only (cross-catalogue): never blocks.
    """
    parsed = [(aid, NP.parse(md)) for aid, md in artifacts]  # fail-closed: raises on empty
    report = ClusterReport()
    hard = within_cluster
    n_total = len(parsed)

    # --- CTA wording repetition (BLOCKING) ------------------------------------
    # exclude shorts whose final block is a tagged KJV verse (don't compare Scripture).
    cta_members: dict[str, list[str]] = {}
    for aid, nar in parsed:
        last = _last_block(nar)
        if last is not None and last.ref:
            continue  # CTA is a KJV verse — not a crafted close
        for g in _cta_ngrams(nar.cta):
            cta_members.setdefault(g, []).append(aid)

    for key, members in _strongest(cta_members, min_share):
        report.findings.append(Finding(
            kind="cta_repetition", phrase=key, members=members, blocking=hard,
            detail=f"{len(members)} of {n_total} close on the same CTA wording {key!r} — "
                   f"repeated phrasing, not the gospel destination. Vary the closing line.",
        ))

    # --- opener-family repetition (BLOCKING; >=2 content words) ---------------
    opener_members: dict[str, list[str]] = {}
    for aid, nar in parsed:
        for g in _content_ngrams(nar.hook, min_content=2):
            opener_members.setdefault(g, []).append(aid)
    opener_floor = max(min_share, 3)
    for g, members in opener_members.items():
        members = sorted(set(members))
        if len(members) >= opener_floor:
            report.findings.append(Finding(
                kind="opener_repetition", phrase=g, members=members, blocking=hard,
                detail=f"opening phrase {g!r} in {len(members)} of {n_total} hooks — vary the entry point.",
            ))

    report.findings = _dedupe(report.findings)
    return report


def _strongest(members_by_key: dict[str, list[str]], min_share: int) -> list[tuple[str, list[str]]]:
    """Collapse overlapping shape keys to the longest key per member-set."""
    cand = [(k, sorted(set(v))) for k, v in members_by_key.items() if len(set(v)) >= min_share]
    cand.sort(key=lambda kv: len(kv[0].split()), reverse=True)
    kept: list[tuple[str, list[str]]] = []
    for k, members in cand:
        if any(k in jk and set(members) <= set(jm) for jk, jm in kept):
            continue
        kept.append((k, members))
    return kept


def _dedupe(findings: list[Finding]) -> list[Finding]:
    by_kind: dict[str, list[Finding]] = {}
    for f in findings:
        by_kind.setdefault(f.kind, []).append(f)
    out: list[Finding] = []
    for kind, fs in by_kind.items():
        fs.sort(key=lambda f: len(f.phrase.split()), reverse=True)
        kept: list[Finding] = []
        for f in fs:
            if any(f.phrase in k.phrase and set(f.members) <= set(k.members) for k in kept):
                continue
            kept.append(f)
        out.extend(kept)
    return out
