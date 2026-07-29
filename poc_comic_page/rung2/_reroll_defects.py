"""Rung 2 Phase A -- reroll of two panels that failed self-check:
  p1a_night_door: baked gibberish lettering on the pouch strap/buckle
  p4a_turning_away: content drift -- rendered TWO figures (Jesus + Seeker at
    a handle) instead of the specified single Seeker turning away, alone.
Same prompt/ref/AR as the original attempt (plain stochastic retry, the one
reroll the brief allows per panel).

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_reroll_defects.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
import poc_comic_page.rung2._render_panel_stills as R  # noqa

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
EPISODE = "CPP_Rung2_InNoWise"

TARGETS = {
    "p1a_night_door": "REROLL-2 (content reroll; REROLL-1 was the API-failure retry)",
    "p4a_turning_away": "REROLL-1 (content reroll: dropped Jesus/handle-reach, enforce single Seeker turning away)",
}

by_name = {name: (name, ar, ref_name, comp) for name, ar, ref_name, comp in R.PANELS}

for target, label in TARGETS.items():
    name, ar, ref_name, comp = by_name[target]
    out = OUT / f"{name}.png"
    ref = R.REF_DIR / ref_name
    prompt = R.PREFIX + R.CHAIN_LINE + f"SINGLE PANEL COMPOSITION: {comp}\n\n" + R.STYLE_TAIL
    print(f"[reroll] {name} (AR {ar}, ref {ref_name}) ...")
    ok = R.run(prompt, out, [ref], ar)
    if ok:
        row = cost.record_hf(EPISODE, "short", "stills", R.MODEL, note=f"[rung2-phase-a] {name} {label}")
        print(f"   ok -> {out}  (+${float(row.get('est_usd') or 0):.2f})")
    else:
        print("   FAILED again -- escalate")
