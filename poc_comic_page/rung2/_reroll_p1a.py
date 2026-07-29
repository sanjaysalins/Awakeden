"""Rung 2 Phase A -- single reroll of p1a_night_door (job failed on first
attempt, no image produced, no spend). Reuses the exact same prompt/ref/AR
from _render_panel_stills.py.

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_reroll_p1a.py
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

name, ar, ref_name, comp = R.PANELS[0]
assert name == "p1a_night_door"
out = OUT / f"{name}.png"
ref = R.REF_DIR / ref_name
prompt = R.PREFIX + R.CHAIN_LINE + f"SINGLE PANEL COMPOSITION: {comp}\n\n" + R.STYLE_TAIL

print(f"[reroll] {name} (AR {ar}, ref {ref_name}) ...")
ok = R.run(prompt, out, [ref], ar)
if ok:
    row = cost.record_hf(EPISODE, "short", "stills", R.MODEL, note=f"[rung2-phase-a] {name} REROLL-1")
    print(f"   ok -> {out}  (+${float(row.get('est_usd') or 0):.2f})")
else:
    print("   FAILED again -- escalate")
