#!/usr/bin/env python
"""PROBE #2 — the FRAMING / zoom sweet spot. Same subject (the crucified Christ, wound recipe so
the hand detail doesn't confound), same style; vary ONLY the framing from extreme macro to epic
wide, plus one deliberately BUSY scene. Reveals where seedream_v4_5 (inked) holds together vs
breaks — so we design 1000 stills to its strengths. _probe/framing/, NOT indexed. ~6 cr (~$0.90).

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/probe_framing.py
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]

def _load(n, rel):
    s = importlib.util.spec_from_file_location(n, ROOT / rel); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m

ber = _load("ber", "longform/_base_elements_refs.py")
probe = _load("probe", "render_lint/probe.py")

OUT = HERE / "visual" / "_probe" / "framing"
CHRIST = "a dark-haired bearded man in his early thirties with a calm Near-Eastern face"
WOUND = ("a dark ragged pierced hole in the centre of the palm with dark red blood running down")  # proven recipe

VARIANTS = [
    ("1_macro_wound",
     f"EXTREME MACRO close-up filling the whole frame of the crucified Christ's open hand ({CHRIST}) "
     f"against the wooden cross-beam: {WOUND}. Only the hand and the wood, nothing else. Dramatic ink."),
    ("2_close_hand_and_face",
     f"CLOSE shot: the crucified Christ's face and one outstretched arm ({CHRIST}), the open hand at "
     f"the beam showing {WOUND}, his head lifted; dark storm sky, one shaft of warm light."),
    ("3_medium_waist_up",
     f"MEDIUM shot, waist up: the crucified Christ on the cross ({CHRIST}, robed at the waist), exactly "
     "two arms out along the crossbeam, head lifted, dark storm sky, one shaft of warm light."),
    ("4_wide_full_cross",
     f"WIDE shot: the whole cross with the crucified Christ upon it ({CHRIST}, robed at the waist), the "
     "upright planted in the rocky hilltop, a few small soldiers below, black storm sky, shaft of light."),
    ("5_epic_vista",
     f"EPIC WIDE VISTA: three crosses small on the dark hill of Golgotha against a vast torn storm sky "
     "with one break of gold light, tiny distant figures and a far city skyline below. Awe and scale."),
    ("6_busy_scene",
     f"A BUSY crowded scene at the foot of the cross ({CHRIST} above): a dense throng of many soldiers "
     "and mourners, scattered spears, helmets, dice, garments, torches, banners — packed with detail."),
]


def render_fn(prompt, dest):
    return ber.render(prompt + ber.STYLE + ber.ONE, dest, refs=None)


def main():
    probe.run_matrix(OUT, VARIANTS, render_fn)


if __name__ == "__main__":
    main()
