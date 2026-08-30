"""Ambient/SFX bed for episode 4, "Naaman in the Jordan" (2 Kings 5 +
Luke 4:27) -- reuses the shared sfxlib.py mix pattern first built for
episode 1, $0, reuse-only from sound_library.

Layer map keyed to the locked unit timeline (ffprobed from each _assembly/
*__held.mp4 in swirls_episode_04_naaman_in_the_jordan_final_piano.mp4's own
concat order, cross-checked against the final mux's real 72.018s length =
the held units (69.032s) + the +3.0s INV-26 landing hold): front 0-7.47
(Nazareth cliff brow, the "tried to throw him off a cliff" hook), f01
7.47-13.17 (Damascus courtyard, Naaman alone with his leprosy), f02
13.17-18.50 (the chariot at Elisha's shut door), f03 18.50-28.47 (the fury
-- "Abana and Pharpar"), f04 28.47-41.63 (the servants' appeal, the turn),
f05 41.63-45.93 (the seventh wash -- new skin), f06 45.93-58.37 (Jesus
citing the story to his own hometown -- "saving Naaman the Syrian"), back
58.37-69.03 (the Jordan at dawn, healed, the gospel-losing-the-argument CTA
+ the 3s landing hold).

Design: one continuous "bleak wilderness" wind bed runs the whole dry-Syria
throughline (front through f04, matching episode 2's own single-bed
discipline for a piece that stays in one kind of country) -- Nazareth's
cliff, Damascus's courtyard, the shut door, the storming fury, and the
servants' appeal are all the same parched country until the water arrives.
A quiet, lowpass-filtered crowd murmur sits under the front cover only
(the mob that nearly threw him off the cliff -- the narration's own cold
open), then RETURNS under f06 at the same treatment -- the same hometown,
the same press, now hearing the very story that provoked them, closing the
loop the narration itself draws. A door-creak accent marks Elisha's
shut door in f02 (he sends one line and never opens it); an armored stride
bed carries Naaman's storming fury through f03, prominent, then cut loose
as he arrives and stills. River water enters at f05's seventh wash and
runs continuously through f06 and the back-cover landing + hold -- the
Jordan doesn't stop when the scene cuts away from it, same as the gold
frame doesn't stop caring what happened in it. The one heavenly-choir swell
is reserved for f06, the actual NT gospel-link page (Jesus speaking the
citation in his own voice), not the CTA cover -- matching episode 1's own
choice to time the swell to the gospel claim itself, not the emotional
beat either side of it.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "sfx_pilots"))
import sfxlib  # noqa: E402
from sfxlib import layer  # noqa: E402

CUT = HERE / "swirls_episode_04_naaman_in_the_jordan_final_piano.mp4"
OUT = HERE / "swirls_episode_04_naaman_in_the_jordan_final_piano_sfx.mp4"

LAYERS = [
    # 2026-08-30: two rounds of user ear-review, both "too loud" -- round 1 dropped
    # every target 2-6dB but the shared sidechain duck (ratio=5) only lets ~1/5 of
    # a pre-duck cut through while narration is speaking, so the change was real
    # but too subtle to hear. Round 2 (this one): a much bigger blanket cut (another
    # 5-6dB on every layer, on top of round 1's numbers) PLUS a deeper duck passed
    # to sfxlib.build() itself (ratio 5->9, threshold lowered) so the bed sits
    # further back under narration specifically, not just quieter in the gaps.
    layer("syria_dry",     "wind_desert_bleak",     "loop",     0.0, 42.0, -46.0, fin=2.0, fout=3.0),
    layer("cliff_crowd",   "crowd_murmur_distant",  "loop",     0.5,  6.5, -52.0, filt="lowpass=f=2200", fin=1.5, fout=1.5),
    layer("door_creak",    "door_gate_creak",       "oneshot", 14.5,  2.0, -39.0, fin=0.1, fout=0.8),
    layer("fury_stride",   "soldiers_march_armor",  "loop",    18.7,  9.5, -39.0, fin=0.8, fout=2.0),
    layer("jordan_river",  "river_well_water",      "loop",    41.5, 30.5, -40.0, fin=0.5, fout=3.5),
    layer("gospel_choir",  "heavenly_choir_soft",   "oneshot", 46.2, 10.5, -38.0, fin=2.0, fout=3.5),
    layer("hometown_crowd", "crowd_murmur_distant", "loop",    46.5, 11.5, -51.0, filt="lowpass=f=2200", fin=2.0, fout=2.5),
]

SCC = "threshold=0.02:ratio=9:attack=15:release=320"

if __name__ == "__main__":
    sfxlib.show_plan("Episode 4 -- Naaman in the Jordan", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS, scc=SCC)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT, regions=[
        ("front cliff", 0.0, 7.47), ("f01 courtyard", 7.47, 13.17),
        ("f02 shut door", 13.17, 18.50), ("f03 fury", 18.50, 28.47),
        ("f04 servants", 28.47, 41.63), ("f05 seventh wash", 41.63, 45.93),
        ("f06 hometown/choir", 45.93, 58.37), ("back landing+hold", 58.37, 72.02),
    ])
