"""veed_io — a small, typed Python wrapper around VEED's subtitle model on fal.ai.

This package is intentionally self-contained and independent of the gospel-shorts
engine in the rest of this repo. It talks to the ``veed/subtitles`` fal.ai model
to burn styled captions into a video.

Quick start::

    from veed_io import VeedSubtitlesClient, SubtitleRequest

    client = VeedSubtitlesClient()                 # reads FAL_KEY from env
    result = client.subtitle(SubtitleRequest(
        video_url="https://example.com/clip.mp4",
        preset="glass",
    ))
    print(result.video_url)
"""

from .models import (
    PresetCustomization,
    SubtitleRequest,
    SubtitleResult,
    TextCustomization,
)
from .presets import (
    BASIC_PRESETS,
    DYNAMIC_PRESETS,
    PRESETS,
    is_dynamic_preset,
)
from .pricing import estimate_cost
from .client import VeedSubtitlesClient, VeedError

__all__ = [
    "VeedSubtitlesClient",
    "VeedError",
    "SubtitleRequest",
    "SubtitleResult",
    "PresetCustomization",
    "TextCustomization",
    "PRESETS",
    "DYNAMIC_PRESETS",
    "BASIC_PRESETS",
    "is_dynamic_preset",
    "estimate_cost",
]

__version__ = "0.1.0"
