"""Load and query the greenlit series library (data/series.json)."""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache

import config


@dataclass
class Episode:
    title: str
    primary_ref: str
    refs: list[str]
    theme: str


@dataclass
class Series:
    id: str
    name: str
    brand: str
    concept: str
    hook_pattern: str
    cta_pattern: str
    guardrails: str
    episodes: list[Episode]


@lru_cache(maxsize=1)
def load_series() -> list[Series]:
    raw = json.loads(config.SERIES_PATH.read_text(encoding="utf-8"))
    out: list[Series] = []
    for s in raw["series"]:
        episodes = [
            Episode(
                title=e["title"],
                primary_ref=e["primary_ref"],
                refs=e.get("refs", [e["primary_ref"]]),
                theme=e.get("theme", ""),
            )
            for e in s["episodes"]
        ]
        out.append(
            Series(
                id=s["id"],
                name=s["name"],
                brand=s.get("brand", ""),
                concept=s.get("concept", ""),
                hook_pattern=s.get("hook_pattern", ""),
                cta_pattern=s.get("cta_pattern", ""),
                guardrails=s.get("guardrails", ""),
                episodes=episodes,
            )
        )
    return out


def get_series(series_id: str) -> Series:
    for s in load_series():
        if s.id == series_id:
            return s
    raise KeyError(f"Unknown series id: {series_id}")


def render_series_library() -> str:
    """Compact text rendering of the full slate for the cached system prompt.

    Gives the model the hook/CTA patterns and guardrails for every series so it
    has cross-series context, not just the one episode being written.
    """
    lines: list[str] = ["# SERIES LIBRARY (greenlit slate)\n"]
    for s in load_series():
        lines.append(f"## {s.name}  [id: {s.id} · brand: {s.brand}]")
        lines.append(f"- Concept: {s.concept}")
        lines.append(f"- Hook pattern: {s.hook_pattern}")
        lines.append(f"- CTA pattern: {s.cta_pattern}")
        lines.append(f"- Guardrails: {s.guardrails}")
        eps = "; ".join(f"{e.title} ({e.primary_ref})" for e in s.episodes)
        lines.append(f"- Episodes: {eps}")
        lines.append("")
    return "\n".join(lines)
