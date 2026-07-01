#!/usr/bin/env python
"""PROBE #3 — CHARACTER-FACE CONSISTENCY (the #1 corpus risk). seedream ref-lock is broken, so we
render no-ref with a shared text descriptor. Question: how consistent does the SAME Christ face stay
across different scenes / framings / moods? Render the same descriptor in 6 varied contexts and
compare the FACES. Tells us whether a text descriptor is enough, or we need a richer locked descriptor.
_probe/face/, NOT indexed. ~6 cr (~$0.90).

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/probe_face.py
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

OUT = HERE / "visual" / "_probe" / "face"
# the SAME shared descriptor used everywhere (as in the real pipeline)
CHRIST = ("a man in his early thirties with a calm Near-Eastern face, warm olive skin, deep brown "
          "eyes, a straight nose, a short dark full beard and long dark wavy hair parted in the middle")

VARIANTS = [
    ("1_teaching_day",  f"A medium portrait of {CHRIST}, teaching outdoors in bright daylight, calm and warm."),
    ("2_sorrow_night",  f"A close portrait of {CHRIST}, sorrowful, praying at night by torchlight."),
    ("3_three_quarter", f"A three-quarter view of {CHRIST}, looking to the side, soft overcast light."),
    ("4_profile",       f"A profile side view of {CHRIST}, calm, warm morning light."),
    ("5_joyful_wide",   f"A wider shot of {CHRIST} standing among people, a faint warm smile, golden light."),
    ("6_glory_lit",     f"A close portrait of {CHRIST}, glorified and radiant, bright light on his face."),
]


def render_fn(prompt, dest):
    return ber.render(prompt + ber.STYLE + ber.ONE, dest, refs=None)


def main():
    probe.run_matrix(OUT, VARIANTS, render_fn)


if __name__ == "__main__":
    main()
