"""POC30 Seed's finish_config.py -- the only per-episode content
_finish_long.py needs (process-validation test, second real proof of fix
#6 beyond the Day of Atonement regression: applying the SAME shared runner
to genuinely new, different content, not just reproducing old output)."""

STEM = "POC30_SEED_living_sketchbook"

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
