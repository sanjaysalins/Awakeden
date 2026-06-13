"""Data models for the Upload Kit stage (Stage 5).

One finished video -> one UploadKit. The kit holds ready-to-paste metadata for
every platform (YouTube short/long, TikTok, Facebook, Instagram), plus the
verification trail (gates + red-team + panel) that proves it is safe to publish.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SourceFacts:
    """Everything harvested from a finished media folder that the metadata is built from."""
    media_dir: str
    video_path: str
    format: str                 # "short" | "long"
    series_name: str
    brand: str
    episode_title: str
    anchor_ref: str             # e.g. "Psalm 22:27"
    anchor_kjv: str             # exact KJV text of the anchor verse (verified)
    kjv_verified: bool
    thread: str                 # the one-thread spine
    thread_lever: str
    hook_line: str              # the opening spoken line (scroll-stopper)
    spoken_script: str          # full narration text (for keyword grounding)
    beats: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass
class PlatformMeta:
    """The ready-to-paste metadata for ONE platform."""
    platform: str               # key into platform_specs.json
    label: str
    title: str                  # "" for platforms with no title field
    description: str            # full body INCLUDING the stamped footer
    tags: list[str] = field(default_factory=list)        # keyword tags ("" where unsupported)
    hashtags: list[str] = field(default_factory=list)    # ordered; first ones matter most

    def to_dict(self) -> dict[str, Any]:
        return {
            "platform": self.platform,
            "label": self.label,
            "title": self.title,
            "description": self.description,
            "tags": self.tags,
            "hashtags": self.hashtags,
        }


@dataclass
class GateResult:
    gate: str                   # "UK-G1" ...
    name: str
    passed: bool
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass
class TitleCandidate:
    """One divergent title option (we generate several and pick the best)."""
    text: str
    angle: str                  # what hook strategy it uses
    chosen: bool = False
    reason: str = ""            # why chosen / rejected

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass
class UploadKit:
    source: SourceFacts
    platforms: list[PlatformMeta] = field(default_factory=list)
    title_candidates: list[TitleCandidate] = field(default_factory=list)
    gates: list[GateResult] = field(default_factory=list)
    redteam: str = ""           # in-engine hostile-auditor verdict + notes
    panel_verdict: str = ""     # merged external-panel verdict (filled after panel run)
    status: str = "DRAFT"       # DRAFT -> RED-TEAMED -> PANELED -> READY
    created_at: str = ""
    notes: list[str] = field(default_factory=list)

    @property
    def all_gates_pass(self) -> bool:
        return all(g.passed for g in self.gates)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "created_at": self.created_at,
            "source": self.source.to_dict(),
            "platforms": [p.to_dict() for p in self.platforms],
            "title_candidates": [c.to_dict() for c in self.title_candidates],
            "gates": [g.to_dict() for g in self.gates],
            "all_gates_pass": self.all_gates_pass,
            "redteam": self.redteam,
            "panel_verdict": self.panel_verdict,
            "notes": self.notes,
        }
