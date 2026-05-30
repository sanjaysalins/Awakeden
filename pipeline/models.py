"""Lightweight data structures passed between engine stages."""
from __future__ import annotations

import re
from dataclasses import dataclass, field


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


@dataclass
class Beat:
    id: str        # structure beat id, e.g. "hook", "point", "proof", "conviction", "landing"
    text: str      # the plain-prose text for this beat


@dataclass
class Draft:
    title: str
    hook_type: str
    beats: list[Beat]
    scripture_reference: str
    scripture_quoted: str     # the exact words quoted inside the narration
    speakers: list[str] = field(default_factory=list)  # non-narrator voices, lowercase

    @property
    def narration(self) -> str:
        """The canonical plain-prose script: beats joined, blank line between."""
        return "\n\n".join(b.text.strip() for b in self.beats if b.text.strip())

    @property
    def hook(self) -> str:
        return self.beats[0].text.strip() if self.beats else ""

    @property
    def cta(self) -> str:
        return self.beats[-1].text.strip() if self.beats else ""

    @property
    def beat_ids(self) -> list[str]:
        return [b.id for b in self.beats]

    @property
    def word_count(self) -> int:
        return count_words(self.narration)

    @property
    def char_count(self) -> int:
        return len(self.narration)

    @classmethod
    def from_json(cls, d: dict) -> "Draft":
        speakers = [str(s).strip().lower() for s in d.get("speakers", []) if str(s).strip()]
        beats = [
            Beat(id=str(b.get("id", "")).strip(), text=str(b.get("text", "")).strip())
            for b in d.get("beats", [])
            if str(b.get("text", "")).strip()
        ]
        return cls(
            title=str(d.get("title", "")).strip(),
            hook_type=str(d.get("hook_type", "")).strip(),
            beats=beats,
            scripture_reference=str(d.get("scripture_reference", "")).strip(),
            scripture_quoted=str(d.get("scripture_quoted", "")).strip(),
            speakers=speakers,
        )


@dataclass
class ThreadCandidate:
    """One proposed thread, before selection. Pinned to a specific true detail
    in a specific verse so the choice can be checked for exegetical honesty."""
    thread: str          # the image/tension — short, evocative phrase
    lever: str           # overlooked-detail | original-language | nt-confirmed-ot-echo | cultural-historical
    anchor_ref: str      # verse the thread is pinned to, e.g. "Luke 15:20"
    anchor_detail: str   # the specific true detail being surfaced
    why_fresh: str       # why this is not the generic auto-complete take
    gospel_landing: str  # how the thread carries through to a clean gospel landing


@dataclass
class Thread:
    """The chosen thread that runs through hook -> middle -> CTA, plus all
    candidates considered (kept for traceability and the review report).

    Top-level fields mirror the chosen candidate so downstream stages can read
    `thread.thread` etc. without indexing into `candidates`."""
    thread: str
    lever: str
    anchor_ref: str
    anchor_detail: str
    why_fresh: str
    gospel_landing: str
    rationale: str                                  # why this candidate was chosen
    candidates: list[ThreadCandidate] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not self.thread.strip()

    @classmethod
    def from_json(cls, d: dict) -> "Thread":
        candidates = [
            ThreadCandidate(
                thread=str(c.get("thread", "")).strip(),
                lever=str(c.get("lever", "")).strip(),
                anchor_ref=str(c.get("anchor_ref", "")).strip(),
                anchor_detail=str(c.get("anchor_detail", "")).strip(),
                why_fresh=str(c.get("why_fresh", "")).strip(),
                gospel_landing=str(c.get("gospel_landing", "")).strip(),
            )
            for c in (d.get("candidates", []) or [])
            if str(c.get("thread", "")).strip()
        ]

        chosen_index = d.get("chosen_index")
        chosen: ThreadCandidate | None = None
        if isinstance(chosen_index, int) and 0 <= chosen_index < len(candidates):
            chosen = candidates[chosen_index]
        elif candidates:
            chosen = candidates[0]  # tolerate missing/invalid index

        if chosen is None:
            chosen = ThreadCandidate(
                thread="", lever="", anchor_ref="", anchor_detail="",
                why_fresh="", gospel_landing="",
            )

        return cls(
            thread=chosen.thread,
            lever=chosen.lever,
            anchor_ref=chosen.anchor_ref,
            anchor_detail=chosen.anchor_detail,
            why_fresh=chosen.why_fresh,
            gospel_landing=chosen.gospel_landing,
            rationale=str(d.get("chosen_rationale", "")).strip(),
            candidates=candidates,
        )


@dataclass
class GateResult:
    gate: str
    verdict: str   # PASS | CONDITIONAL | FAIL
    evidence: str
    fix: str = ""


@dataclass
class AgentVerdict:
    agent: str
    verdict: str   # STRONG | CAUTION | REVISION NEEDED
    note: str


@dataclass
class Review:
    panel: list[AgentVerdict]
    gates: list[GateResult]
    overall: str            # LOCKED | REVISE | REWORK
    priority_fixes: list[str]

    @property
    def is_locked(self) -> bool:
        return self.overall.upper().strip() == "LOCKED"

    @property
    def failed_gates(self) -> list[GateResult]:
        return [g for g in self.gates if g.verdict.upper().strip() == "FAIL"]

    @property
    def is_acceptable(self) -> bool:
        """Publishable when no gate hard-FAILs. CONDITIONAL/CAUTION are advisory —
        this is the terminal signal for the revise loops (a deliberately hostile
        auditor rarely awards a clean LOCKED, but zero FAILs means ship it)."""
        return len(self.failed_gates) == 0

    @classmethod
    def from_json(cls, d: dict) -> "Review":
        panel = [
            AgentVerdict(
                agent=str(p.get("agent", "")).strip(),
                verdict=str(p.get("verdict", "")).strip(),
                note=str(p.get("note", "")).strip(),
            )
            for p in d.get("panel", [])
        ]
        gates = [
            GateResult(
                gate=str(g.get("gate", "")).strip(),
                verdict=str(g.get("verdict", "")).strip(),
                evidence=str(g.get("evidence", "")).strip(),
                fix=str(g.get("fix", "")).strip(),
            )
            for g in d.get("gates", [])
        ]
        return cls(
            panel=panel,
            gates=gates,
            overall=str(d.get("overall", "")).strip(),
            priority_fixes=[str(x).strip() for x in d.get("priority_fixes", []) if str(x).strip()],
        )
