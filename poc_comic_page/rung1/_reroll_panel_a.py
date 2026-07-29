"""One-shot reroll of panel_a_jesus.png (Rung 1 Phase 1): the first render fused
TWO scenes into one image (an internal panel divider appeared -- Jesus/door on
top, a duplicate ledger-hands scene below), violating the "exactly ONE
coherent scene per still" QC gate. Per the brief: reroll once, then escalate
if it recurs. Chained BACKWARD off panel_d_threshold.png (already-settled,
clean Jesus likeness) per the comic-strip-native spec sec1.3 backward-chain fix,
to lock character identity while re-rolling the composition.

  .venv\\Scripts\\python.exe poc_comic_page/rung1/_reroll_panel_a.py
"""
import re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "CPP_Rung1_InNoWise"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"

from _render_panel_stills import PANEL_A, CHAIN_LINE, run  # reuse validated prompt + run()

REF = OUT / "panel_d_threshold.png"
OUT_FILE = OUT / "panel_a_jesus.png"
BACKUP = OUT / "panel_a_jesus.reroll0_FAILED.png"

PROMPT = PANEL_A.replace(
    "SINGLE PANEL COMPOSITION:",
    CHAIN_LINE.strip() + "\n\nSINGLE PANEL COMPOSITION:",
    1,
)


def main():
    if OUT_FILE.exists():
        OUT_FILE.rename(BACKUP)
        print(f"[keep] original fused render backed up -> {BACKUP}")
    print("[img ] panel_a_jesus RE-ROLL (chained backward off panel_d_threshold.png) ...", flush=True)
    t = time.time()
    ok = run(PROMPT, OUT_FILE, [REF])
    if ok:
        try:
            row = cost.record_hf(EPISODE, "short", "stills", MODEL, note="[rung1-phase1] panel_a_jesus REROLL-1")
            print(f"   ok ({time.time()-t:.0f}s)  +${row.get('est_usd')}")
        except Exception as e:
            print(f"   ok ({time.time()-t:.0f}s)  (ledger record skipped: {e})")
    else:
        print("   FAILED -- restoring original fused render, escalate.")
        if BACKUP.exists():
            BACKUP.rename(OUT_FILE)


if __name__ == "__main__":
    main()
