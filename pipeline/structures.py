"""Load and render narration structures (data/structures.json)."""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache

import config


@dataclass
class Beat:
    id: str
    name: str
    start: int
    end: int
    pace: str
    word_guide: str
    intent: str


@dataclass
class Structure:
    id: str
    name: str
    description: str
    total_seconds: int
    beats: list[Beat]

    @property
    def beat_ids(self) -> list[str]:
        return [b.id for b in self.beats]

    def name_for(self, beat_id: str) -> str:
        for b in self.beats:
            if b.id == beat_id:
                return b.name
        return beat_id


@lru_cache(maxsize=1)
def _raw() -> dict:
    return json.loads(config.STRUCTURES_PATH.read_text(encoding="utf-8"))


def get_structure(structure_id: str | None = None) -> Structure:
    raw = _raw()
    sid = structure_id or config.DEFAULT_STRUCTURE or raw.get("default")
    s = raw["structures"][sid]
    beats = [
        Beat(
            id=b["id"],
            name=b["name"],
            start=b["start"],
            end=b["end"],
            pace=b.get("pace", ""),
            word_guide=b.get("word_guide", ""),
            intent=b["intent"],
        )
        for b in s["beats"]
    ]
    return Structure(
        id=sid,
        name=s["name"],
        description=s.get("description", ""),
        total_seconds=s.get("total_seconds", 60),
        beats=beats,
    )


def render(structure: Structure) -> str:
    """Human/LLM-readable rendering of a structure for the prompt."""
    lines = [
        f"STRUCTURE: {structure.name} ({structure.total_seconds}s total)",
        structure.description,
        "",
        "BEATS (write exactly one text block per beat, in this order):",
    ]
    for b in structure.beats:
        lines.append(
            f"- [{b.id}] {b.name}  ({b.start}-{b.end}s · ~{b.word_guide} words · {b.pace})\n"
            f"    {b.intent}"
        )
    return "\n".join(lines)
