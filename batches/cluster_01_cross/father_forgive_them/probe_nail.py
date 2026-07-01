#!/usr/bin/env python
"""PROBE #1 — the crucifixion NAIL. Hold the hand/cross/style constant, vary ONLY the nail clause,
to learn empirically what wording seedream_v4_5 (inked) renders as a believable nail vs a weird
proud object / cube / arrowhead. Renders to _probe/nail/, NOT indexed. ~8 cr (~$1.20).

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/probe_nail.py
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

OUT = HERE / "visual" / "_probe" / "nail"
CHRIST = "a dark-haired bearded man in his early thirties with a calm Near-Eastern face"
# constant base — one open hand palm-forward against the cross-beam; ONLY {nail} changes
BASE = (f"A close reverent study of the crucified Christ's open right hand ({CHRIST}) held "
        "palm-forward flat against the dark wooden beam of the cross, the bare forearm leading back "
        "toward his robed shoulder at the frame edge, one shaft of warm light across the palm. {nail}")

VARIANTS = [
    ("flush_round_head",
     "Through the centre of the palm a single dark iron nail is driven into the wood behind; only its "
     "plain round head shows, flush against the skin, dark blood around it running down."),
    ("flat_head_pressed",
     "Through the centre of the palm a single dark iron nail is hammered into the wood, its flat head "
     "pressed flat against the skin, dark blood running down."),
    ("wound_first_flush",
     "In the centre of the palm a dark bleeding nail-wound; the head of the nail is just visible flush "
     "within the wound, blood running down."),
    ("dark_disc_flush",
     "Through the centre of the palm the head of a crucifixion nail shows as a single dark iron disc "
     "flush with the skin, blood running from beneath it."),
    ("wound_only_no_metal",
     "In the centre of the palm a dark pierced wound with fresh and dried blood, the nail sunk so deep "
     "that no metal stands out from the skin."),
    ("blacksmith_broad_head",
     "Through the centre of the palm a thick blacksmith's nail is driven flush; only its broad round "
     "head shows against the skin, dark blood pooling."),
    ("control_spike",
     "Through the centre of the palm a large iron spike."),
    ("control_square_head",
     "Through the centre of the palm a thick iron nail with a flat square head."),
    ("wound_no_nail_word",
     "In the centre of the palm a dark ragged pierced hole, torn and bleeding, dark red blood running "
     "down toward the wrist."),
    ("wound_puncture",
     "A deep round puncture wound in the centre of the palm, rimmed with torn skin and dark clotted "
     "blood, a thin trickle of blood running down to the wrist."),
]


def render_fn(prompt, dest):
    return ber.render(prompt + ber.STYLE + ber.ONE, dest, refs=None)


def main():
    jobs = [(label, BASE.format(nail=nail)) for label, nail in VARIANTS]
    probe.run_matrix(OUT, jobs, render_fn)


if __name__ == "__main__":
    main()
