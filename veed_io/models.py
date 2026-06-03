"""Typed request/response objects for the ``veed/subtitles`` model.

These dataclasses mirror the fal.ai input/output schema. ``to_arguments()`` emits
exactly the JSON the model expects, omitting any field left as ``None`` so the
preset's own defaults win.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .presets import POSITIONS, SHADOWS, is_valid_preset


@dataclass
class TextCustomization:
    """Per-tier text styling override (baseline or highlighted words)."""

    font: Optional[str] = None      # must be a supported Google Font
    weight: Optional[int] = None    # 100-900; >=700 renders bold
    color: Optional[str] = None     # hex, e.g. "#FFCC00"

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        if self.font is not None:
            out["font"] = self.font
        if self.weight is not None:
            if not 100 <= self.weight <= 900:
                raise ValueError(f"weight must be 100-900, got {self.weight}")
            out["weight"] = self.weight
        if self.color is not None:
            out["color"] = self.color
        return out


@dataclass
class PresetCustomization:
    """Optional overrides layered on top of a preset's defaults."""

    position: Optional[str] = None  # top | center | bottom
    shadow: Optional[str] = None    # none | min | mid | max
    baseline: Optional[TextCustomization] = None
    highlighted: Optional[TextCustomization] = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        if self.position is not None:
            if self.position not in POSITIONS:
                raise ValueError(f"position must be one of {POSITIONS}")
            out["position"] = self.position
        if self.shadow is not None:
            if self.shadow not in SHADOWS:
                raise ValueError(f"shadow must be one of {SHADOWS}")
            out["shadow"] = self.shadow

        text: dict[str, Any] = {}
        if self.baseline is not None:
            text["baseline"] = self.baseline.to_dict()
        if self.highlighted is not None:
            text["highlighted"] = self.highlighted.to_dict()
        if text:
            out["text_customizations"] = text
        return out


@dataclass
class SubtitleRequest:
    """A single subtitling job.

    Provide exactly one transcription source:
      * ``video_url`` alone   -> VEED auto-transcribes the audio
      * ``srt_file_url`` or ``srt_content`` -> transcription is skipped

    ``video_url`` is always required (it is the footage that gets captioned).
    """

    video_url: str
    preset: str = "glass"
    language: Optional[str] = None
    srt_file_url: Optional[str] = None
    srt_content: Optional[str] = None
    customization: Optional[PresetCustomization] = None

    def validate(self) -> None:
        if not self.video_url:
            raise ValueError("video_url is required")
        if not is_valid_preset(self.preset):
            raise ValueError(
                f"unknown preset {self.preset!r}; see veed_io.presets.PRESETS"
            )
        if self.srt_file_url and self.srt_content:
            raise ValueError(
                "provide only one of srt_file_url / srt_content, not both"
            )

    def to_arguments(self) -> dict[str, Any]:
        """Build the fal.ai ``arguments`` payload (None fields omitted)."""
        self.validate()
        args: dict[str, Any] = {
            "video_url": self.video_url,
            "preset": self.preset,
        }
        if self.language is not None:
            args["language"] = self.language
        if self.srt_file_url is not None:
            args["srt_file_url"] = self.srt_file_url
        if self.srt_content is not None:
            args["srt_content"] = self.srt_content
        if self.customization is not None:
            cust = self.customization.to_dict()
            if cust:
                args["customization"] = cust
        return args


@dataclass
class SubtitleResult:
    """Parsed output of a completed job."""

    video_url: str
    content_type: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    request_id: Optional[str] = None
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_response(
        cls, response: dict[str, Any], request_id: Optional[str] = None
    ) -> "SubtitleResult":
        video = (response or {}).get("video") or {}
        url = video.get("url")
        if not url:
            raise VeedResponseError(
                f"response had no video.url; got keys {list((response or {}).keys())}"
            )
        return cls(
            video_url=url,
            content_type=video.get("content_type"),
            file_name=video.get("file_name"),
            file_size=video.get("file_size"),
            request_id=request_id,
            raw=response or {},
        )


class VeedResponseError(RuntimeError):
    """Raised when a completed job's payload is missing the expected video."""
