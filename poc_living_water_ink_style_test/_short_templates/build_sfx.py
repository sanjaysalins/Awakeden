"""Ambient / SFX bed for a Swirls SHORT episode (copy of ep13's build_sfx.py, parameterised: design v3.2
step 9). $0, reuse-only from sound_library.

The cut to put sound on is read from `assembly_receipt_scored.json` (`output`, `total`) -- no hard-coded
file name -- and every cue is placed from `unit_timing.json` by UNIT TAG, so the script names no other
episode's file or time. Edit CUES for the film (the starter bed is one quiet wind loop under the whole
film). `--dry-run` prints the plan and stops.

Cue = (label, library slug, kind, first unit, last unit, target dBFS, fade in, fade out). `oneshot` cues
play from the start of the first unit. A unit left out of every cue is bare (words + score alone).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ["JITB_ROOT"]) if os.environ.get("JITB_ROOT") else next(
    p for p in HERE.parents if (p / "sfx_pilots").is_dir())
sys.path.insert(0, str(ROOT / "sfx_pilots"))
import sfxlib  # noqa: E402

CUES = [
    ("wind", "wind_desert_bleak", "loop", "front", "back", -46.0, 2.0, 3.0),
]


def read_inputs() -> dict:
    rec = json.loads((HERE / "assembly_receipt_scored.json").read_text(encoding="utf-8"))
    timing = json.loads((HERE / "unit_timing.json").read_text(encoding="utf-8"))["units"]
    return {"cut": Path(rec["output"]), "total": float(rec["total"]), "timing": timing}


def layers(inp: dict) -> list[dict]:
    out = []
    for label, slug, kind, first, last, tgt, fin, fout in CUES:
        start = float(inp["timing"][first]["start_s"])
        end = float(inp["timing"][last]["end_s"]) if kind == "loop" else start + 4.0
        out.append(sfxlib.layer(label, slug, kind, start, end - start, tgt, fin=fin, fout=fout))
    return out


if __name__ == "__main__":
    inp = read_inputs()
    lay = layers(inp)
    out = HERE / f"{HERE.name}_final_piano_sfx.mp4"
    sfxlib.show_plan(HERE.name, lay)
    if "--dry-run" in sys.argv:
        print(json.dumps({"cut": str(inp["cut"]), "out": str(out), "total": inp["total"]}, indent=2))
        sys.exit(0)
    sfxlib.build(inp["cut"], out, lay)
    print(f"[ok] {out}")
