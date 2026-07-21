"""Ambient/SFX bed for Isaiah 53 ("The Suffering Servant"), same reverent
choir-free ambient-under-the-score approach as Bronze Serpent's
_sfx_bronze_inked.py and Psalm 22's _sfx_psalm22_lf.py (feedback-no-choir-
pad-under-score) -- ambience/accents only, layered UNDER the Suno score,
never a musical/choir pad.

Cue sheet only — the engine is pipeline/sfx_bed.py (ONE shared copy). Reuse-
only from sound_library ($0).

No prior sfx cue-sheet script was found for this piece in the repo (the
2026-07-15 shipped LivingPage_Isaiah53_16x9_scored_sfx.mp4 predates a saved,
reusable script -- clip-QC rebuild session, 2026-07-20) -- this is a fresh
cue sheet, authored from the piece's own beat captions
(v1/visual_16x9_inked/livingpage_full.spec.json).

Arc: the prophet writing, the question hanging (desolate) -> "Behold my
servant" builds, then "the picture breaks" (tension) -> marred, despised,
rejected (crowd, distant) -> the transaction: wounded, bruised, stripes,
laid on him all (weight, one nail-strike accent) -> all we like sheep, led
as a lamb (flock) -> silent before his accusers, into the honest objection
/ Israel-as-servant reading / the rich man's tomb (quiet, contemplative) ->
the Ethiopian eunuch's chariot, Philip preaches Christ (chariot wheels) ->
back to the cross, "it pleased the LORD to bruise him," poured out his soul
(storm weight) -> quietly the chapter turns toward morning, satisfied,
resurrection implied (warmth rising) -> "His name is Jesus" (one landing
impact) -> through the extended landing hold.

Output: LivingPage_Isaiah53_16x9_scored_sfx.mp4
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.sfx_bed import build  # noqa: E402

VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked"
SCORED = VIS / "LivingPage_Isaiah53_16x9_scored.mp4"
OUT = VIS / "LivingPage_Isaiah53_16x9_scored_sfx.mp4"
TOTAL = 408.28  # 405.28s narration + 3.0s outro (matches EPISODES recipe in _add_score_lf.py, INV-26)

CUES = [
    ("wind_desert_bleak",     0.0,   TOTAL, -37),   # continuous base
    ("air_hollow_desolate",   0.0,    51.7, -34),   # the prophet writing, the question hanging
    ("rumble_deep_sub",       45.0,   79.6, -30),   # "the picture breaks" through "looks away"
    ("crowd_murmur_distant",  64.7,   89.7, -36),   # despised and rejected, the world looks away
    ("nail_strike_single",    99.1,  100.1, -22),   # "wounded for our transgressions"
    ("rumble_deep_sub",       99.1,  137.2, -30),   # bruised, stripes, laid on him all
    ("flock_sheep_field",    128.4,  153.8, -32),   # all we like sheep, a lamb to the slaughter
    ("air_hollow_desolate",  159.3,  234.0, -35),   # silent; the honest objection; the tomb
    ("chariot_wheels_road",  234.0,  264.9, -30),   # the NT moment; the eunuch's chariot
    ("thunder_low_roll",     282.2,  305.7, -27),   # "it pleased the LORD to bruise him"
    ("rumble_deep_sub",      282.2,  305.7, -30),   # weight under the storm
    ("dawn_morning_warm",    305.7,  TOTAL, -30),   # the chapter turns toward morning, satisfied,
                                                      # through the landing hold
    ("impact_low_boom",      400.4,  401.4, -18),   # "His name is Jesus"
]


if __name__ == "__main__":
    build(SCORED, OUT, CUES, TOTAL)
