"""Ambient/SFX bed for episode 8, "Can Any Good Thing" (John 1:45-51) --
retrofit pass, reuses the shared sfxlib.py mix pattern first built for
episode 1, $0, reuse-only from sound_library.

Layer map keyed to the locked unit timeline (from CAN_ANY_GOOD_THING_final
.mp4's own held durations, cross-checked against _assembly/concat.txt + the
+3.0s INV-26 landing hold): front 0-7.47 (dawn, Nathanael under the fig
tree, news breaking on the road), f01 7.47-14.53 (Philip arrives at a
run), f02 14.53-19.40 (the sneer -- "any good thing"), f03 19.40-23.50
(Nathanael meets Jesus -- "in whom is no guile"), f04 23.50-32.80 (heaven's
own memory: Nathanael alone in private prayer under the fig tree -- "under
the fig tree"), f05 32.80-45.10 (the confession -- "the Son of God"), f06
45.10-53.67 (heaven opens, the Jacob's-Ladder echo -- "ascending and
descending"), back 53.67-64.04 (dusk, the empty fig tree, the gospel
landing + CTA + the 3s landing hold).

Design: dawn birdsong opens on the fig tree and Philip's real running
footsteps land exactly on his arrival in F01. The whole dialogue-dense
middle (F02/F03, the sneer through the first meeting) is left DRY on
purpose -- this episode is built almost entirely out of quoted speech, so
the words carry it, the same "held breath" discipline used on the pilot's
own theophany page. F04's private prayer gets the SAME dawn warmth as the
front cover, much quieter -- heaven revisiting an earlier hidden moment,
acoustically rhymed with the opening. From there a single heavenly-choir
swell is built out of two overlapping takes (a quiet hint under the
confession, crossfading into the fuller swell) so it grows continuously
from F05's confession, through F06's own Jacob's-Ladder vision, into the
dusk landing and CTA -- one held arc, not a single hard cue, because unlike
the pilot/episode 2 (an OT scene reaching toward Christ), Jesus is already
speaking in his own voice for this whole back half.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "sfx_pilots"))
import sfxlib  # noqa: E402
from sfxlib import layer  # noqa: E402

CUT = HERE / "CAN_ANY_GOOD_THING_final.mp4"
OUT = HERE / "CAN_ANY_GOOD_THING_final_sfx.mp4"

LAYERS = [
    layer("dawn_village",     "dawn_morning_warm",    "loop",    0.0, 15.0, -35.0, fin=2.0, fout=2.5),
    layer("philip_footsteps", "footsteps_dirt_approach", "oneshot", 8.5, 4.0, -30.0, fin=0.3, fout=1.0),
    layer("fig_tree_prayer",  "dawn_morning_warm",    "loop",   23.0, 10.0, -42.0, fin=2.0, fout=2.0),
    layer("choir_confession", "heavenly_choir_soft",  "loop",   33.0, 13.0, -40.0, fin=3.0, fout=3.0),
    layer("choir_vision",     "heavenly_choir_soft",  "loop",   44.0, 20.0, -31.0, fin=3.0, fout=5.0),
]

if __name__ == "__main__":
    sfxlib.show_plan("Episode 8 -- Can Any Good Thing", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT, regions=[
        ("front dawn", 0.0, 7.47), ("f01 Philip arrives", 7.47, 14.53),
        ("f02/f03 sneer+meeting", 14.53, 23.5), ("f04 fig-tree prayer", 23.5, 32.8),
        ("f05 confession", 32.8, 45.1), ("f06 ladder vision", 45.1, 53.67),
        ("back landing+hold", 53.67, 64.04),
    ])
