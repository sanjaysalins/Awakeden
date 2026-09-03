"""Ambient/SFX bed for episode 10, "She Loved Much" (Luke 7:36-50) -- reuses
the shared sfxlib.py mix pattern, $0, reuse-only from sound_library.

Layer map keyed to the locked unit timeline (from the real assembled final's
own held durations logged by swirls_assemble.py's own [plan] output): front
0-4.033 (she stands at the lit threshold), f01 4.033-14.800 (she walks in),
f02 14.800-24.700 (she stands weeping), f03 24.700-32.467 (the kiss, the
ointment), f04 32.467-42.800 (Simon's unspoken judgment), f05 42.800-54.000
(the parable), f06 54.000-61.766 (Simon's hedge), f07 61.766-69.966 ("Seest
thou this woman?"), f08 69.966-82.899 (the declaration, hero), f09
82.899-92.799 (the sending), back 92.799-106.291 (dawn, the empty room,
including the +3.0s INV-26 hold).

Design: honestly sparse, on purpose. Unlike ep7 (a funeral procession, a
touch, a village praise-crowd -- genuinely different outdoor soundscapes
across its own scenes), this whole episode is ONE continuous interior --
Simon's dining room, start to finish, until the dawn cut on the back cover.
No library asset actually fits "quiet reclining dinner guests" (the closest,
crowd_murmur_distant, is built as an outdoor "jeering... far away" bed --
wrong tone for guests who are merely watching, not hostile) -- so rather than
force a mismatched asset in at low volume and hope nobody notices, the
interior stretch (front through f09) stays genuinely dry: her own footsteps
mark her entrance, then nothing but the felt-piano score and the narration
carry the whole scene, same "the words carry it" call ep8 already made on
its own dry sneer/first-meeting stretch. The only new sound in the whole
piece is the dawn ambience under the back cover -- the one real location/time
change the story actually has (the room, the next morning, empty).

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_10_she_loved_much\\build_sfx.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "sfx_pilots"))
import sfxlib  # noqa: E402
from sfxlib import layer  # noqa: E402

CUT = HERE / "swirls_episode_10_she_loved_much_final_piano.mp4"
OUT = HERE / "swirls_episode_10_she_loved_much_final_piano_sfx.mp4"

LAYERS = [
    layer("arrival_steps", "footsteps_stone",   "oneshot", 0.4,  3.2, -40.0, fin=0.0, fout=1.0),
    layer("dawn_landing",  "dawn_morning_warm",  "loop",   92.8, 13.5, -44.0, fin=3.0, fout=3.0),
]

if __name__ == "__main__":
    sfxlib.show_plan("Episode 10 -- She Loved Much", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT, regions=[
        ("front the threshold", 0.0, 4.033), ("f01 she walks in", 4.033, 14.800),
        ("f02 weeping", 14.800, 24.700), ("f03 the kiss", 24.700, 32.467),
        ("f04 Simon's thought", 32.467, 42.800), ("f05 the parable", 42.800, 54.000),
        ("f06 the hedge", 54.000, 61.766), ("f07 Seest thou", 61.766, 69.966),
        ("f08 forgiven (hero)", 69.966, 82.899), ("f09 the sending", 82.899, 92.799),
        ("back dawn+hold", 92.799, 106.291),
    ])
