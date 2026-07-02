#!/usr/bin/env python
"""Redo the RISEN-scar panels 07 + 06c (user 2026-07-01). Old PNGs DELETED. 05 kept (good).

v-prev failed: 'healed nail scar' drew a tiny NAIL stuck in the scar (07); 'nail scar' + 'puckered'
scattered MULTIPLE pink dots + X-stitches across the fingers (06c). Learned fix (now in rules.json):
ONE single round healed scar at the CENTRE of the palm, smooth closed pale skin — never the word
'nail', never 'puckered'.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/redo_risen_scars.py [--render]
"""
import argparse, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]

def _load(n, rel):
    s = importlib.util.spec_from_file_location(n, ROOT / rel); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m

ber = _load("ber", "longform/_base_elements_refs.py")
rl = _load("rll", "render_lint/lint.py")

NBP = HERE / "visual" / "nbp"
CHRIST = ("the SAME man throughout: a dark-haired bearded man in his early thirties with a calm "
          "Near-Eastern face")
STYLE_NO_TEXT = ber.STYLE.split(" ABSOLUTELY NO text")[0]
# CORRECT risen scar: one, centred, smooth, closed — no 'nail', no 'puckered'
SCAR = ("one single round healed scar at the very centre of the palm — a small patch of smooth, "
        "closed, pale skin, flat and level with the palm, the only mark on an otherwise clean hand")

JOBS = [
    ("07_risen_hero",
     "LANDING hero 49-57s: mercy held out",
     f"The risen Christ standing in warm golden morning light ({CHRIST}, in clean flowing robes), "
     "alive and serene, his glorified face healed and at peace, reaching one open hand gently toward "
     f"the viewer in welcome; at the very centre of that open palm, {SCAR}. Soft deep shadow behind "
     "him. The tender gospel hero image.",
     STYLE_NO_TEXT),
    ("06c_intercession_lives",
     "CONVICTION 39.4-42.8s: the living Christ interceding",
     f"The living risen Christ standing in warm golden light ({CHRIST}), both hands lifted open in "
     f"intercession; on each open palm, at its very centre, {SCAR}. His glorified face calm and at "
     "peace. Soft deep shadow behind him. Reverent, alive.",
     STYLE_NO_TEXT),
]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--render", action="store_true")
    a = ap.parse_args()
    for slug, ctx, subj, style in JOBS:
        print(f"\n########## {slug} ##########\n{ctx}")
        rl.report(subj, stage="still", context=ctx)
        if a.render:
            dest = NBP / f"{slug}.png"
            ber.lint_canonical(slug, subj)
            print("  ->", ber.render(subj + style + ber.ONE, dest, refs=None))
    if not a.render:
        print("\n[lint-only] add --render to spend ~2 cr")


if __name__ == "__main__":
    main()
