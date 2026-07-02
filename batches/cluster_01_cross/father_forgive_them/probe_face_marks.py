#!/usr/bin/env python
"""PROBE #4 — does adding UNIQUE MARKS (+ keeping the face NEUTRAL, mood carried by context/posture)
tighten the identity lock vs probe #3's generic descriptor? Same 6 scene contexts as probe #3 for an
apples-to-apples read. Check: (a) is the face more consistent scene-to-scene, (b) do the marks persist
and stay on the correct side. _probe/face_marks/, NOT indexed. ~6 cr (~$0.90).

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/probe_face_marks.py
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

OUT = HERE / "visual" / "_probe" / "face_marks"
# base descriptor + UNIQUE MARKS (distinct, drawable, anchoring)
MARKED = ("a man in his early thirties with a calm Near-Eastern face, warm olive skin, deep brown "
          "eyes, a lean face with high cheekbones, a slightly aquiline nose, a small dark mole on his "
          "LEFT cheek just below the eye, a short dark full beard and long dark wavy hair parted in the "
          "middle")

# mood carried by CONTEXT / POSTURE only — face kept neutral (per probe #3 finding)
SCENES = [
    ("1_teaching_day",  "teaching a crowd outdoors in bright midday daylight, one hand raised in gesture"),
    ("2_sorrow_night",  "kneeling at night by torchlight, his head slightly bowed, his shoulders heavy"),
    ("3_three_quarter", "a three-quarter view, turning to look to the side, soft overcast light"),
    ("4_profile",       "a clear profile side view, warm morning light"),
    ("5_among_people",  "standing among a group of people in a sunlit street, calm"),
    ("6_glory_lit",     "standing with bright radiant golden light blazing behind and around him"),
]


def render_fn(prompt, dest):
    return ber.render(prompt + ber.STYLE + ber.ONE, dest, refs=None)


def main():
    jobs = [(label, f"A portrait of {MARKED}, {scene}.") for label, scene in SCENES]
    probe.run_matrix(OUT, jobs, render_fn)


if __name__ == "__main__":
    main()
