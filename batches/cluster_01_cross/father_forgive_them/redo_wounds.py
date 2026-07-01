#!/usr/bin/env python
"""Redo the WOUND panels so the wounds look correct + CONSISTENT (user 2026-07-01).
Old PNGs DELETED (redo rule). Lint pre-flight runs first.

  05_pierced_hand (passion) -> replace the ornamental twisted spike with the plain flat-head iron
                               nail that worked on 01b; keep the arm connected to the body.
  07_risen_hero (risen)     -> the healed scar looked wrong -> a small round patch of closed,
                               slightly-puckered pale-pink skin, flat and level (a real healed wound).
  06c_intercession_lives    -> same risen-scar fix (its scars rendered as bright white dots).

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/redo_wounds.py [--render]
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
# reusable "correct healed scar" phrasing (matches the learned fix; no bright white dot)
HEALED = ("one healed nail scar — a small round patch of closed, slightly puckered pale-pink skin, "
          "flat and level with the palm, plainly an old wound now healed over, not a bright dot and "
          "not an open hole")

JOBS = [
    ("05_pierced_hand",
     "INTERCESSION 26.8-32.4s: the nailed hand — mercy, not a fist",
     "A tight low-angle view along the crucified Christ's outstretched arm laid against the dark "
     f"grained wood of the cross-beam ({CHRIST}): through the centre of the open palm a single thick "
     "plain dark iron nail with a flat square head is hammered flush into the timber, dark blood "
     "running from the wound down toward the wrist. The bare forearm continues unbroken up to His "
     "shoulder and robed torso and calm face at the edge of the frame, so the nailed hand plainly "
     "belongs to the living man on the cross. One shaft of warm light falls across the pierced open "
     "hand. Reverent, merciful — an open hand, not a clenched fist.",
     ber.STYLE),
    ("07_risen_hero",
     "LANDING hero 49-57s: mercy held out",
     f"The risen Christ standing in warm golden morning light ({CHRIST}, in clean flowing robes), "
     "alive and serene, his glorified face healed and at peace, reaching one open hand gently toward "
     f"the viewer in welcome; at the centre of that open palm {HEALED}. Soft deep shadow behind him. "
     "The tender gospel hero image.",
     STYLE_NO_TEXT),
    ("06c_intercession_lives",
     "CONVICTION 39.4-42.8s: the living Christ interceding",
     f"The living risen Christ standing in warm golden light ({CHRIST}), both hands lifted in "
     f"intercession, each open palm bearing {HEALED}; his glorified face calm and at peace. Soft deep "
     "shadow behind him. Reverent, alive.",
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
        print("\n[lint-only] add --render to spend ~3 cr")


if __name__ == "__main__":
    main()
