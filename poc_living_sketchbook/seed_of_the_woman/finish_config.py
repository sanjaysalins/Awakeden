"""Seed of the Woman LONG's finish_config.py -- the only per-episode
content _finish_long.py needs. Score/SFX/caption choices below cover
spreads 1-5 (promoted from the POC30 validation test); revisit SCORE's
outro_s (currently a short test tail) and SFX_CUES once the full spread
table exists, and re-point CAPTIONS.skip_spreads at the full set of
verse-card spreads."""

STEM = "SEEDOFTHEWOMAN_LONG_living_sketchbook"

SCORE = {
    "segments": ["lonely_searching_a"],
    "xfade_s": 0.0,
    "gain_db": -13.0,
    "outro_s": 1.0,
}

SFX_CUES = [
    ("dawn_morning_warm", "ALL", -24),
]

CAPTIONS = {
    "skip_spreads": ["s03_verse_card"],
    "segment_seconds": 60.0,
}

WATERMARK = True
