"""Comic Page Pipeline POC -- Rung 2 FINAL PHASE, Step 2: animate 14 panels.

Frozen-tableau discipline (per adhoc/SKILL_locked.md + CLAUDE.md comic-grid-cost-
tiered-animation lock): figures hold pose, camera locked, only named ambient
motion. Seedance 1.5 Pro for calm single/double-figure panels (~$0.36 real-
billed each per the ledger); Kling 3.0 pro sound-off for panels with more
figures/complexity/history-of-inventing-locomotion (~$1.13 each) -- reuses the
exact hardened FROZEN_*_V2-style "INVENT NOTHING" prompts validated in
poc_comic_page/rung1/_animate_bakeoff.py for panel_b/panel_d (same stills,
same failure mode to guard against).

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_animate_panels.py --job p1a
  .venv\\Scripts\\python.exe poc_comic_page/rung2/_animate_panels.py --job panel_d --reroll
"""
import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config  # noqa
from pipeline import cost  # noqa

HF = str(config.HF_CLI_PATH)
EPISODE = "CPP_Rung2_InNoWise"
HERE = Path(__file__).resolve().parent
R2_STILLS = HERE / "stills"
R1_STILLS = HERE.parent / "rung1" / "stills"
OUT = HERE / "clips"
OUT.mkdir(parents=True, exist_ok=True)

# ---- hardened Kling prompts (reusing rung1's validated FROZEN_*_V2 language
# for panel_b/panel_d -- same stills, same documented Kling locomotion-
# invention failure mode) --------------------------------------------------
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
    "The camera does not move at all. Both men stay perfectly frozen for the "
    "entire clip in this exact wide shot -- absolutely no walking, no steps, "
    "no leg movement, no foot lifting or placing, no weight shifting, no head "
    "turning, no facial movement, no arm movement, no clothing repositioning, "
    "and no new figures or objects appear. INVENT NOTHING NEW -- both figures "
    "remain pixel-for-pixel identical to the source image the entire time, "
    "frozen mid-stride like statues. Only these named things may move: the "
    "radiant light behind Jesus in the doorway pulses gently brighter and "
    "dimmer, a few dust motes drift through that light, and the very bottom "
    "hem-edges of their garments flutter by no more than 1-2 pixels. "
    "Everything else -- every limb, every fold of cloth above the hem, every "
    "facial feature -- must remain completely static throughout."
)
FROZEN_P5A = (
    "The camera does not move. Both figures stay perfectly frozen the entire "
    "time -- no limbs move, no legs move, no steps are taken, no feet lift off "
    "the ground, no heads turn, no faces change, no arms change position, no "
    "clothing shifts position, and no new figures, marks, or objects appear. "
    "INVENT NOTHING -- both figures stay pixel-for-pixel identical to this "
    "exact image throughout, holding their exact poses like statues. Only "
    "these named things may move: the radiant doorway light pulses softly, "
    "dust motes drift in the doorway light. Nothing else in the frame changes."
)

# (name, provider, still_path, prompt, extra_cli_args)
JOBS = {
    "p1a": dict(provider="seedance", still=R2_STILLS / "p1a_night_door.png", ar="1:1",
                prompt=("The figure holds his standing pose, expression unchanged. Only: "
                        "the thin light-line under the door flickers gently, faint cold "
                        "mist drifts low across the stone floor. No other movement.")),
    "p1b": dict(provider="seedance", still=R2_STILLS / "p1b_hesitant_hand.png", ar="1:1",
                prompt=("The hands hold their positions exactly, not touching the door. "
                        "Only: the warm glow under the door edge breathes gently, the "
                        "scroll's hanging cord sways slightly. No other movement.")),
    "p2a": dict(provider="seedance", still=R2_STILLS / "p2a_rehearsing.png", ar="9:16",
                prompt=("The figure holds his leaning pose, eyes closed, expression "
                        "unchanged. Only: the warm under-door light breathes gently, his "
                        "mantle hem stirs faintly. No other movement.")),
    "p2b": dict(provider="seedance", still=R2_STILLS / "p2b_jesus_speaks.png", ar="9:16",
                prompt=("The figure holds his exact expression, mouth, and head position "
                        "unchanged. Only: the warm light on his face breathes brighter and "
                        "softer, faint dust motes drift through the light. No other "
                        "movement.")),
    "p2c": dict(provider="seedance", still=R2_STILLS / "p2c_light_line.png", ar="9:16",
                prompt=("The composition and feet hold their exact positions, perfectly "
                        "still. Only: the light-line shimmers gently along the stone, "
                        "faint dust motes drift in the warm light. No other movement.")),
    "p4a": dict(provider="seedance", still=R2_STILLS / "p4a_turning_away.png", ar="9:16",
                # v2 hardened after the first re-roll moved Jesus' arms (raised hand ->
                # open-arms welcome) and morphed the seeker's floor shadow
                prompt=("The camera does not move. Both figures stay perfectly frozen "
                        "the entire time -- the man with the scroll holds his exact "
                        "turned-away pose, and Jesus in the doorway holds his exact "
                        "raised-hand gesture. No limbs move, no arms change position, "
                        "no heads turn, no faces change, no clothing shifts, and the "
                        "dark shadow on the floor keeps its exact same shape. INVENT "
                        "NOTHING -- both figures stay pixel-for-pixel identical to this "
                        "exact image throughout, like statues. Only these named things "
                        "may move: the doorway light behind Jesus pulses gently "
                        "brighter and dimmer, faint dust motes drift in that light. "
                        "Nothing else in the frame changes.")),
    "p4b": dict(provider="seedance", still=R2_STILLS / "p4b_open_hands.png", ar="9:16",
                prompt=("The hands hold their exact open position, fingers unmoving. "
                        "Only: the warm light pooled in the palms breathes brighter and "
                        "softer. No other movement.")),
    "p4c": dict(provider="seedance", still=R2_STILLS / "p4c_empty_doorway.png", ar="9:16",
                prompt=("The composition holds its exact framing. Only: the radiant light "
                        "from the empty doorway pulses gently, faint dust motes drift. No "
                        "other movement.")),
    "p5b": dict(provider="seedance", still=R2_STILLS / "p5b_record_received.png", ar="3:4",
                prompt=("The hands hold their exact positions, releasing and receiving the "
                        "scroll without moving. Only: the warm light on the scroll "
                        "breathes, the frayed cord sways slightly. No other movement.")),
    "p5c": dict(provider="seedance", still=R2_STILLS / "p5c_never_locked.png", ar="3:4",
                prompt=("The composition holds its exact framing. Only: the warm light "
                        "along the door edge breathes softly. No other movement.")),
    "panel_c": dict(provider="seedance", still=R1_STILLS / "panel_c_ledger.png", ar="9:16",
                    prompt=("The hands hold their grip on the scroll exactly. Only: the "
                            "scroll's cord tie sways gently, the light sliver on the "
                            "papyrus flickers. No other movement.")),
    "p5a": dict(provider="kling", still=R2_STILLS / "p5a_the_welcome.png", ar="1:1",
                prompt=FROZEN_P5A),
    "panel_b": dict(provider="kling", still=R1_STILLS / "panel_b_door.png", ar="9:16",
                    prompt=FROZEN_B_V2),
    "panel_d": dict(provider="kling", still=R1_STILLS / "panel_d_threshold.png", ar="9:16",
                    prompt=FROZEN_D_V2),
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


def run_job(name, reroll=False):
    j = JOBS[name]
    png = j["still"]
    if not png.exists():
        print(f"   missing still: {png}")
        return False
    out = OUT / f"{name}.mp4"
    if j["provider"] == "seedance":
        model = "seedance1_5"
        extra = ["--duration", "4", "--resolution", "720p", "--aspect_ratio", j["ar"],
                 "--generate_audio", "false"]
    else:
        model = "kling3_0"
        extra = ["--mode", "pro", "--sound", "off", "--duration", "5",
                 "--aspect_ratio", j["ar"]]
    cmd = [HF, "generate", "create", model, "--start-image", str(png), "--prompt", j["prompt"],
           "--wait"] + extra
    print(f"[clip] {name} ({model}{' RE-ROLL' if reroll else ''}) ...", flush=True)
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
            cost.record_hf(EPISODE, "short", "animate", model, image=png,
                            note=f"[rung2-final-phase] {name}{' REROLL' if reroll else ''}",
                            params=_params_from_extra(extra))
        except Exception as e:
            print(f"   (ledger skipped: {e})")
        print(f"   ok ({time.time()-t:.0f}s) -> {out}")
        return True
    print("   FAILED")
    return False


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True, choices=list(JOBS.keys()) + ["all"])
    ap.add_argument("--reroll", action="store_true")
    a = ap.parse_args()
    names = list(JOBS.keys()) if a.job == "all" else [a.job]
    ok_all = True
    for n in names:
        ok_all = run_job(n, a.reroll) and ok_all
    sys.exit(0 if ok_all else 1)
