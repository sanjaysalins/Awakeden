"""Retime Bronze Serpent scene windows: warp old->new word times (panel-fix re-synth).

Matches old/new word sequences with difflib, uses matched words as piecewise-linear
control points, maps every scene ["t"] through the warp, rewrites scene_plan.json
(backup kept). Mirrors longform/_retime.py's approach, control points derived
automatically instead of hand-pasted.
"""
import difflib, json, shutil
from pathlib import Path

ROOT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible")
S = Path(r"C:\Users\sanjay\AppData\Local\Temp\claude\C--Users-sanjay-PycharmProjects-JesusInTheBible\06f4a00b-76bc-463a-8309-987820393bec\scratchpad")
PLAN = ROOT / "longform/04_The_Bronze_Serpent/v1/visual_16x9/scene_plan.json"

old = json.loads((S / "old_align_04.json").read_text(encoding="utf-8"))["words"]
new = json.loads((ROOT / "longform/04_The_Bronze_Serpent/v1/narration.alignment.json").read_text(encoding="utf-8"))["words"]

def toks(ws):
    return ["".join(c for c in w["text"].lower() if c.isalpha()) for w in ws]

sm = difflib.SequenceMatcher(a=toks(old), b=toks(new), autojunk=False)
ctrl = [(0.0, 0.0)]
for a, b, n in sm.get_matching_blocks():
    for k in range(0, n, 8):  # a control point every ~8 matched words
        ot, nt = old[a + k]["start"], new[b + k]["start"]
        if ot and nt and ot > ctrl[-1][0] and nt > ctrl[-1][1]:
            ctrl.append((float(ot), float(nt)))
old_end, new_end = 460.87, 474.23  # prior/new narration.mp3 durations
ctrl.append((old_end, new_end))

def warp(t):
    if t <= ctrl[0][0]:
        return ctrl[0][1]
    for (o1, n1), (o2, n2) in zip(ctrl, ctrl[1:]):
        if t <= o2:
            return n1 + (t - o1) * (n2 - n1) / (o2 - o1 or 1e-9)
    return ctrl[-1][1] + (t - ctrl[-1][0])

shutil.copy(PLAN, PLAN.with_suffix(".json.pre_retime_20260703"))
plan = json.loads(PLAN.read_text(encoding="utf-8"))
prev_end = 0.0
print(f"{len(ctrl)} control points; max drift "
      f"{max(abs(n - o) for o, n in ctrl):.1f}s")
for s in plan["scenes"]:
    o0, o1 = s["t"]
    n0, n1 = warp(o0), warp(o1)
    n0 = max(n0, prev_end)              # keep windows contiguous, non-overlapping
    n1 = max(n1, n0 + 2.0)
    drift = n0 - o0
    print(f"  scene {s['id']:02d}  {o0:6.1f}-{o1:6.1f}  ->  {n0:6.1f}-{n1:6.1f}  (drift {drift:+5.1f}s)")
    s["t"] = [round(n0, 2), round(n1, 2)]
    prev_end = n1
PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
print("scene_plan.json rewritten (backup: .json.pre_retime_20260703)")
