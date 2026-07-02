#!/usr/bin/env python
"""Redo 04_cast_lots (user 2026-07-01) — old PNG DELETED (redo rule: never keep/index it).

Defect: a small free-standing Latin cross was rendered planted in the ground behind the robe
pile (an anachronistic devotional crucifix). Fix: this beat is the gambling at GROUND LEVEL —
drop any cross from the frame entirely (seedream has no negative channel, so the fix is to not
mention a cross at all, not to forbid one). Just hands + lots + the seamless robe + torchlight.

~1 credit (~$0.15). seedream_v4_5 inked.
  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/redo_04.py
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("ber", ROOT / "longform" / "_base_elements_refs.py")
ber = importlib.util.module_from_spec(spec); spec.loader.exec_module(ber)

NBP = HERE / "visual" / "nbp"

SUBJ = (
    "Framed low on the dusty ground among the sandalled feet of Roman soldiers in first-century "
    "legionary dress: their weathered hands casting small carved lots and knucklebones in the dirt, "
    "a folded cream seamless robe heaped on the ground beside them, one low guttering candle-flame "
    "to the side casting warm torchlight against deep shadow. The rough soldiers' hands and the "
    "scattered carved lots fill the foreground. Ground-level, gritty, cold and indifferent."
)


def main():
    dest = NBP / "04_cast_lots.png"
    ber.lint_canonical("04_cast_lots", SUBJ)
    status = ber.render(SUBJ + ber.STYLE + ber.ONE, dest, refs=None)
    print(f"  -> 04_cast_lots: {status}")


if __name__ == "__main__":
    main()
