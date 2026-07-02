#!/usr/bin/env python
"""Redo 01b_nailed_hands (user 2026-07-01) — old PNG DELETED. v1 rendered ornamental ARROWHEADS +
a hallucinated wire looped round the fingers (predicted by render_lint 'nail-renders-as-stud').

Applying the just-learned fix: say NAIL (not 'spike'), a flat SQUARE head hammered flush (no
protruding shaft), hands 'side by side' (drop 'fingers open/relaxed' which triggered the wire).
Judgement call: the rule now says 'prefer ONE hand', but the two-hands symmetry is the stronger
hook — trying two-hands ONCE with corrected wording (advise + human decides). Lint runs first.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/redo_01b.py [--render]
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
SUBJ = (
    "A stark close macro of the crucified Christ's two hands held side by side against the dark "
    "grained wood of the cross-beam, each hand pierced through the centre of the palm by a single "
    "thick plain dark iron nail with a flat square head hammered flush into the timber, dark blood "
    "running from each wound down toward the wrist. The hands rest still against the wood. A black "
    "storm sky beyond, only the two nailed hands and the beam in frame."
)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--render", action="store_true")
    a = ap.parse_args()
    ctx = "HOOK 0-3.4s: 'Nails through his hands.' — punchy macro open (v2, plain flat-head nails)"
    rl.report(SUBJ, stage="still", context=ctx)
    if a.render:
        dest = NBP / "01b_nailed_hands.png"
        ber.lint_canonical("01b_nailed_hands", SUBJ)
        print("  ->", ber.render(SUBJ + ber.STYLE + ber.ONE, dest, refs=None))
    else:
        print("[lint-only] add --render to spend ~1 cr")


if __name__ == "__main__":
    main()
