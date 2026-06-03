"""Preset and language tables for the ``veed/subtitles`` model.

The two preset tiers differ in price: dynamic presets carry a 2x multiplier over
the base rate, basic presets are 1x. See :mod:`veed_io.pricing`.
"""

from __future__ import annotations

# Richer, context-aware rendering. 2x price multiplier.
DYNAMIC_PRESETS: tuple[str, ...] = (
    "glass",
    "whisper",
    "glide2",
    "fusion",
    "glide",
    "terminal",
    "handwritten",
)

# Fixed, lightweight styling. 1x price multiplier.
BASIC_PRESETS: tuple[str, ...] = (
    "simple",
    "plain",
    "beans",
    "corpo",
    "boo",
    "shadeplay",
    "casper",
    "capri",
    "lowkey",
    "vinta",
    "diego",
    "ali",
    "slay",
    "kitty",
    "hustle",
    "karl",
    "sprout",
    "flex",
    "mint",
    "rizz",
    "vegas",
)

PRESETS: tuple[str, ...] = DYNAMIC_PRESETS + BASIC_PRESETS

# customization.position
POSITIONS: tuple[str, ...] = ("top", "center", "bottom")

# customization.shadow
SHADOWS: tuple[str, ...] = ("none", "min", "mid", "max")

# A trimmed, commonly-used slice of the ~150 supported BCP-47 source-audio codes.
# The full list is accepted by the API; we only validate against COMMON_LANGUAGES
# when the caller opts into strict validation.
COMMON_LANGUAGES: tuple[str, ...] = (
    "en-US", "en-GB", "en-AU", "en-IN",
    "es-ES", "es-MX", "es-US",
    "fr-FR", "fr-CA",
    "de-DE", "it-IT", "pt-BR", "pt-PT",
    "nl-NL", "pl-PL", "ru-RU", "uk-UA",
    "ar-SA", "he-IL", "tr-TR",
    "ja-JP", "ko-KR", "zh", "zh-TW", "zh-HK",
    "id-ID", "ms-MY", "th-TH", "vi-VN",
)
# Note: COMMON_LANGUAGES is a convenience subset for autocompletion/help text.
# The API itself accepts the full enum; we do not block uncommon codes by default.

FONTS_REFERENCE_URL = "https://www.veed.io/api/v1/subtitle-renders/fonts"


def is_dynamic_preset(preset: str) -> bool:
    """True if ``preset`` is a dynamic (2x price) preset."""
    return preset in DYNAMIC_PRESETS


def is_valid_preset(preset: str) -> bool:
    return preset in PRESETS
