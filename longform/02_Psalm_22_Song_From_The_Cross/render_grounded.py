#!/usr/bin/env python
"""Render stills from the GROUNDED, validated prompts in still_specs.json (the fix for lazy prompting).

Every prompt here has passed still_validate.py (cited verse + distinct shot + pinned pose + dedup +
poison lint). Prepends the shared INK style, expands {CH}, uses the same BytePlus client + ref-lock as
render_fresh_16x9. Deletes the target PNG first so it re-renders (call() is otherwise idempotent).

  ...python .../render_grounded.py --only poured_out_bones,pierced_feet   # reroll a subset
  ...python .../render_grounded.py --all                                  # every grounded spec
"""
import argparse, importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


rf = _load("render_fresh_16x9")
rn = _load("render_new16_16x9")
SPECS = json.loads((HERE / "still_specs.json").read_text(encoding="utf-8"))["specs"]
REFK = {slug: refk for slug, (p, refk) in {**rf.PROMPTS, **rn.PROMPTS}.items()}  # crux|risen|None per slug


def full_prompt(slug):
    return f"{rf.INK}: " + SPECS[slug]["prompt"].replace("{CH}", rf.CH)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=""); ap.add_argument("--all", action="store_true")
    ap.add_argument("--render", action="store_true")
    a = ap.parse_args()
    only = {s.strip() for s in a.only.split(",") if s.strip()}
    targets = [s for s in SPECS if a.all or s in only]
    if not targets:
        ap.error("pass --only <slugs> or --all")
    for slug in targets:
        refk = REFK.get(slug)
        ref = rf.REFMAP.get(refk)
        png = rf.OUT / f"{slug}.png"
        print(f"\n{slug:24} shot={SPECS[slug]['shot']:14} ref={refk or 'NONE'}")
        if a.render:
            if png.exists():
                png.unlink()                    # force reroll
            print(f"   -> {rf.call(full_prompt(slug), png, ref)}", flush=True)
    if not a.render:
        print(f"\n[list only] {len(targets)} grounded stills. add --render (~${len(targets)*0.05:.2f})")


if __name__ == "__main__":
    main()
