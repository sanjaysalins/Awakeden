"""Comic Page Pipeline POC -- Rung 1 Phase 2: animate + bake-off render jobs.

Renders one clip per --job call (so the caller can fire jobs in parallel).
Frozen-tableau discipline: figures hold pose, camera locked, only named
ambient motion. Reuses the validated call/ledger pattern from
poc_thief_e2e/_animate_crop_test.py (Kling) and
poc_thief_e2e/_test_captionless_bakeoff.py (multi-model bake-off).

  .venv\\Scripts\\python.exe poc_comic_page/rung1/_animate_bakeoff.py --job panel_d_kling
"""
import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
EPISODE = "CPP_Rung1_InNoWise"
HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
OUT = HERE / "clips"
OUT.mkdir(parents=True, exist_ok=True)

FROZEN_B = ("The figure holds his walking pose. Only: the warm light through the door gap "
            "breathes gently brighter and dimmer like firelight, faint dust motes drift in the "
            "light, the hem of his cloak sways almost imperceptibly. No other movement.")
FROZEN_D = ("Both figures hold their poses. Only: the radiant light behind Jesus pulses softly, "
            "dust motes drift in the doorway light, the cloak hems sway almost imperceptibly. "
            "No other movement.")
FROZEN_A = ("The figure holds perfectly still, expression unchanged. Only: the warm light from "
            "the doorway behind him breathes gently, faint dust motes drift through the light "
            "shaft. No other movement.")
FROZEN_C = ("The hands hold their grip on the book. Only: the hanging frayed strap sways gently, "
            "the sliver of warm light on the book's edge flickers softly. No other movement.")

# NOTE (2026-07-25 pre-flight `hf model get`): seedance1_5 duration is an enum
# {4,8,12} and minimax_hailuo duration is an enum {6,10} -- neither supports
# the brief's literal "5s". Using the nearest legal value per model (4 for
# Seedance, 6 for Hailuo); Kling3_0's duration is a free integer and 5 is
# valid there, unchanged. minimax_hailuo also has no aspect_ratio param at
# all (only `resolution`, an enum of {512,768,1080} that must be passed via
# `hf model get`'s exact case, not overridden here -- default 768 used).
# RE-ROLL 2026-07-25: QC caught BOTH kling3_0 clips inventing real leg/gait
# locomotion (frames show the Seeker's feet lifting and striding) despite the
# brief's "holds his walking pose" instruction -- a documented Kling failure
# mode on action/multi-figure panels (see CLAUDE.md comic-grid-cost-tiered-
# animation bake-off notes). Hardened with the explicit no-limbs-move /
# INVENT NOTHING language validated in poc_thief_e2e/_animate_crop_test.py.
FROZEN_B_V2 = (
    "The camera does not move. Every figure stays perfectly frozen the entire "
    "time -- no limbs move, no legs move, no steps are taken, no feet lift off "
    "the ground, no heads turn, no faces change, no clothing shifts position, "
    "no held objects move position, and no new figures, marks, or objects "
    "appear. INVENT NOTHING -- the figure stays pixel-for-pixel identical to "
    "this exact image throughout, holding his exact walking pose like a "
    "statue. Only these named things may move: the warm light through the "
    "door gap breathes gently brighter and dimmer like firelight, faint dust "
    "motes drift in the light, and the very hem-edge of his cloak flutters by "
    "at most a few pixels. Nothing else in the frame changes."
)
FROZEN_D_V2 = (
    "The camera does not move. Every figure stays perfectly frozen the entire "
    "time -- no limbs move, no legs move, no steps are taken, no feet lift off "
    "the ground, no heads turn, no faces change, no arms change position, no "
    "clothing shifts position, and no new figures, marks, or objects appear. "
    "INVENT NOTHING -- both figures stay pixel-for-pixel identical to this "
    "exact image throughout, holding their exact poses like statues. Only "
    "these named things may move: the radiant light behind Jesus pulses "
    "softly, dust motes drift in the doorway light, and the very hem-edges of "
    "their cloaks flutter by at most a few pixels. Nothing else in the frame "
    "changes."
)

JOBS = {
    "panel_b_kling": dict(still="panel_b_door.png", model="kling3_0", prompt=FROZEN_B,
                           extra=["--mode", "pro", "--sound", "off", "--duration", "5",
                                  "--aspect_ratio", "9:16"]),
    "panel_d_kling": dict(still="panel_d_threshold.png", model="kling3_0", prompt=FROZEN_D,
                           extra=["--mode", "pro", "--sound", "off", "--duration", "5",
                                  "--aspect_ratio", "9:16"]),
    "panel_b_kling_v2": dict(still="panel_b_door.png", model="kling3_0", prompt=FROZEN_B_V2,
                              extra=["--mode", "pro", "--sound", "off", "--duration", "5",
                                     "--aspect_ratio", "9:16"]),
    "panel_d_kling_v2": dict(still="panel_d_threshold.png", model="kling3_0", prompt=FROZEN_D_V2,
                              extra=["--mode", "pro", "--sound", "off", "--duration", "5",
                                     "--aspect_ratio", "9:16"]),
    "panel_a_seedance": dict(still="panel_a_jesus.png", model="seedance1_5", prompt=FROZEN_A,
                              extra=["--duration", "4", "--resolution", "720p",
                                     "--aspect_ratio", "9:16", "--generate_audio", "false"]),
    "panel_a_hailuo": dict(still="panel_a_jesus.png", model="minimax_hailuo", prompt=FROZEN_A,
                            extra=["--duration", "6"]),
    "panel_c_seedance": dict(still="panel_c_ledger.png", model="seedance1_5", prompt=FROZEN_C,
                              extra=["--duration", "4", "--resolution", "720p",
                                     "--aspect_ratio", "9:16", "--generate_audio", "false"]),
    "panel_c_hailuo": dict(still="panel_c_ledger.png", model="minimax_hailuo", prompt=FROZEN_C,
                            extra=["--duration", "6"]),
}


def _params_from_extra(extra):
    params = {}
    it = iter(extra)
    for a in it:
        if a.startswith("--"):
            k = a[2:]
            v = next(it, True)
            params[k] = v
    return params


def run_job(name):
    j = JOBS[name]
    png = STILLS / j["still"]
    if not png.exists():
        print(f"   missing still: {png}")
        return False
    out = OUT / f"{name}.mp4"
    cmd = [HF, "generate", "create", j["model"], "--start-image", str(png), "--prompt", j["prompt"],
           "--wait"] + j["extra"]
    print(f"[clip] {name} ({j['model']}) ...", flush=True)
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED")
        return False
    m = re.search(r'https?://\S+?\.mp4', blob)
    if not m:
        print(f"   no mp4 url: {blob.strip()[-500:]}")
        return False
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
    if out.exists() and out.stat().st_size > 0:
        try:
            # NOTE (found 2026-07-25): minimax_hailuo's cost-estimate query
            # requires an image (start_image/end_image) to be present in the
            # SAME call, else `hf generate cost` 400s and record_hf's except
            # swallows it -- silently under-logging the ledger. Always pass
            # `image=png` here, not just the CLI `params`.
            cost.record_hf(EPISODE, "short", "animate", j["model"],
                            image=png, note=f"[rung1-phase2] {name}",
                            params=_params_from_extra(j["extra"]))
        except Exception as e:
            print(f"   (ledger skipped: {e})")
        print(f"   ok ({time.time()-t:.0f}s) -> {out}")
        return True
    print("   FAILED")
    return False


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True, choices=list(JOBS.keys()))
    a = ap.parse_args()
    ok = run_job(a.job)
    sys.exit(0 if ok else 1)
