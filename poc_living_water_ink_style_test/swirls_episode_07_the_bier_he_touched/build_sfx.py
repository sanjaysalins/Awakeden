"""Ambient/SFX bed for episode 7, "The Bier He Touched" (Luke 7:11-17, the
widow of Nain) -- reuses the shared sfxlib.py mix pattern, $0, reuse-only
from sound_library.

Layer map keyed to the locked unit timeline (from the real assembled final's
own held durations logged by swirls_assemble.py's own [plan] output): front
0-8.633 (the procession carrying the bier out through the gate), f01
8.633-16.500 (the law of distance -- "and you were unclean"), f02
16.500-25.500 (Jesus walks toward her -- "Weep not"), f03 25.500-34.133 (he
touches the bier, the bearers stand still -- the held-breath beat), f04
34.133-44.666 (the gospel turn -- "Arise"), f05 44.666-51.432 (the boy sits
up, given back), f06 51.432-57.465 (the reversal named -- "Life spread from
Jesus to the boy," the crowd streaming home), back 57.465-72.025 (dawn, the
empty bier, "It became a homecoming," including the +3.0s INV-26 hold).

Design: a bleak desert wind carries the whole funeral throughline (front
through f03), receding to near-silence at the touch itself -- the "held
breath" the narration's own bearers keep, no new layer added at F03 at all.
A warmer, closer crowd murmur returns at F06 as the villagers praise and the
procession turns homeward, distinct from the earlier distant, wary murmur of
people keeping away at F01. Dawn birdsong carries the whole back-cover
landing, matching the caption's own "homecoming."

REMOVED 2026-09-02 (user, after hearing the finished mix): a "gospel_choir"
layer (heavenly_choir_soft) was originally placed at F04's "Arise" (34-51s,
the middle of the cut), following this project's usual pattern of timing a
choir swell to the gospel claim. On this piece it read as a second,
competing piece of music playing alongside the felt-piano score rather than
an ambience layer -- the sound library's choir clip has its own melodic
movement, and stacked against a real score (unlike the plain instrumental
ambience beds used everywhere else) it clashed instead of supporting. The
score's own strings already gather at this exact point in its own
composition, so the layer was redundant as well as clashing. Dropped
entirely rather than just turned down -- if a future episode wants a choir
moment under a real score again, treat it as a genuine risk to A/B test
before locking, not a safe default.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "sfx_pilots"))
import sfxlib  # noqa: E402
from sfxlib import layer  # noqa: E402

CUT = HERE / "swirls_episode_07_the_bier_he_touched_final_piano.mp4"
OUT = HERE / "swirls_episode_07_the_bier_he_touched_final_piano_sfx.mp4"

LAYERS = [
    layer("funeral_wind",    "wind_desert_bleak",     "loop",     0.0,  34.5, -44.0, fin=2.0, fout=4.0),
    layer("wary_villagers",  "crowd_murmur_distant",  "loop",     0.5,  15.0, -50.0, filt="lowpass=f=2000", fin=2.0, fout=3.0),
    layer("homecoming_crowd","crowd_murmur_distant",  "loop",    51.0,   8.0, -46.0, fin=2.0, fout=2.5),
    layer("dawn_landing",    "dawn_morning_warm",     "loop",    57.0,  15.5, -44.0, fin=2.5, fout=3.0),
]

if __name__ == "__main__":
    sfxlib.show_plan("Episode 7 -- The Bier He Touched", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT, regions=[
        ("front the procession", 0.0, 8.633), ("f01 the law", 8.633, 16.500),
        ("f02 Weep not", 16.500, 25.500), ("f03 the touch (held breath)", 25.500, 34.133),
        ("f04 Arise", 34.133, 44.666), ("f05 sat up", 44.666, 51.432),
        ("f06 life spread", 51.432, 57.465), ("back landing+hold", 57.465, 72.025),
    ])
