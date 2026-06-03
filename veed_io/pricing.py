"""Cost estimation for ``veed/subtitles``.

Base rate is $0.10 per minute of source video. Dynamic presets apply a 2x
multiplier; basic presets are 1x. This is a client-side estimate only — the
authoritative charge comes from fal.ai.
"""

from __future__ import annotations

from dataclasses import dataclass

from .presets import is_dynamic_preset

BASE_RATE_PER_MINUTE = 0.10
DYNAMIC_MULTIPLIER = 2.0
BASIC_MULTIPLIER = 1.0


@dataclass
class CostEstimate:
    duration_seconds: float
    preset: str
    multiplier: float
    usd: float

    def __str__(self) -> str:
        mins = self.duration_seconds / 60.0
        return (
            f"~${self.usd:.2f} "
            f"({mins:.2f} min x ${BASE_RATE_PER_MINUTE:.2f}/min x {self.multiplier:g}, "
            f"preset={self.preset})"
        )


def estimate_cost(duration_seconds: float, preset: str) -> CostEstimate:
    """Estimate USD cost for subtitling ``duration_seconds`` with ``preset``."""
    if duration_seconds < 0:
        raise ValueError("duration_seconds must be >= 0")
    multiplier = DYNAMIC_MULTIPLIER if is_dynamic_preset(preset) else BASIC_MULTIPLIER
    minutes = duration_seconds / 60.0
    usd = minutes * BASE_RATE_PER_MINUTE * multiplier
    return CostEstimate(
        duration_seconds=duration_seconds,
        preset=preset,
        multiplier=multiplier,
        usd=round(usd, 4),
    )
