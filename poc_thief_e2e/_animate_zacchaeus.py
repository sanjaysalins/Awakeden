"""Animate the 3 Zacchaeus panels, cost-tiered (2026-07-25): Kling for the
crowd/complex wide shot (panel A, per locked comic-grid-cost-tiered-animation
rule), cheaper Minimax Hailuo for the two calm single-figure close-ups
(panels B, C) -- the real tiered mix, not yet tested in isolation.

  .venv\\Scripts\\python.exe poc_thief_e2e/_animate_zacchaeus.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills" / "_zacchaeus"
OUT = HERE / "clips" / "_zacchaeus"
OUT.mkdir(parents=True, exist_ok=True)

FROZEN = (
    "Every figure stays perfectly frozen the entire time -- no limbs move, no heads turn, no "
    "faces change, no expressions change, no skin changes, no hair moves, no clothing moves, "
    "no held objects move, and no new figures, marks, or objects appear. INVENT NOTHING -- "
    "every figure stays pixel-for-pixel identical to this exact image throughout. "
)

JOBS = [
    ("panel_a_wide", "kling3_0", "16:9",
     "A single comic panel, wide shot of a crowd, a man in a tree, and a teacher looking up "
     "at him. The camera does not move. " + FROZEN +
     "Only the environment is alive: leaves on the tree rustle faintly, dust motes drift in "
     "the sunbeams, distant background figures hold still."),
    ("panel_b_jesus", "minimax_hailuo", "1:1",
     "A single comic panel, close-up on a man's face looking up, mid-speech. The camera does "
     "not move. " + FROZEN +
     "Only the background is alive: leaves on the branch above sway faintly in a breeze."),
    ("panel_c_zacchaeus", "minimax_hailuo", "1:1",
     "A single comic panel, close-up on a man's face among tree branches, an expression of "
     "joyful disbelief. The camera does not move. " + FROZEN +
     "Only the leaves around him are alive: they rustle faintly in a breeze, sunlight flickers "
     "through them."),
]


def main():
    for name, model, ar, prompt in JOBS:
        png = STILLS / f"{name}.png"
        out = OUT / f"{name}.mp4"
        if model == "kling3_0":
            cmd = [HF, "generate", "create", model, "--start-image", str(png), "--prompt", prompt,
                   "--duration", "5", "--aspect_ratio", ar, "--mode", "pro", "--sound", "off", "--wait"]
            params = {"mode": "pro", "sound": "off", "duration": 5}
        else:
            cmd = [HF, "generate", "create", model, "--start-image", str(png), "--prompt", prompt,
                   "--duration", "6", "--wait"]
            params = {"duration": 6}
        print(f"[clip] {name} ({model}) ...", flush=True)
        t = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        blob = (r.stdout or "") + "\n" + (r.stderr or "")
        if re.search(r"nsfw", blob, re.IGNORECASE):
            print("   NSFW-REJECTED"); continue
        m = re.search(r'https?://\S+?\.mp4', blob)
        if not m:
            print(f"   no mp4 url: {blob.strip()[-300:]}"); continue
        subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
        if out.exists() and out.stat().st_size > 0:
            try:
                cost.record_hf("Zacchaeus_Luke19", "short", "animate", model, note=f"[zacchaeus] {name}", params=params)
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
