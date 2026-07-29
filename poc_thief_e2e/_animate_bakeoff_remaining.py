"""Retry the models the widened bake-off missed (2026-07-25): seedance_2_0_mini
timed out, and the ledger-recording crash on minimax_hailuo's cost query took
the script down before seedance_2_0/happy_horse_video/grok_video_v15 ran.
Same source page, same simple prompt. Ledger recording is now non-fatal so a
reconciliation hiccup can't stop the batch.

  .venv\\Scripts\\python.exe poc_thief_e2e/_animate_bakeoff_remaining.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills" / "_comic_strip_template_test"
OUT = HERE / "clips" / "_bakeoff_i2v"
OUT.mkdir(parents=True, exist_ok=True)
SRC = STILLS / "david_goliath.png"

PROMPT = (
    "Animate this comic book page. Bring all four panels to life with subtle, natural motion "
    "in each one, while keeping every character, face, and caption exactly as drawn."
)

JOBS = [
    ("seedance_2_0_mini", ["--duration", "5", "--aspect_ratio", "9:16"]),
    ("seedance_2_0", ["--duration", "5", "--aspect_ratio", "9:16"]),
    ("happy_horse_video", ["--duration", "5", "--aspect_ratio", "9:16"]),
    ("grok_video_v15", ["--duration", "5"]),
]


def main():
    for model, extra in JOBS:
        out = OUT / f"{model}.mp4"
        cmd = [HF, "generate", "create", model, "--start-image", str(SRC), "--prompt", PROMPT,
               "--wait"] + extra
        print(f"[clip] {model} -> {out.name} ...", flush=True)
        t = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=480)
        blob = (r.stdout or "") + "\n" + (r.stderr or "")
        if re.search(r"nsfw", blob, re.IGNORECASE):
            print("   NSFW-REJECTED"); continue
        m = re.search(r'https?://\S+?\.mp4', blob)
        if not m:
            print(f"   no mp4 url: {blob.strip()[-300:]}"); continue
        subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
        if out.exists() and out.stat().st_size > 0:
            print(f"   ok ({time.time()-t:.0f}s)")
            try:
                cost.record_hf("EW_Thief_POC", "short", "animate", model, note="[i2v-bakeoff] david_goliath")
            except Exception as e:
                print(f"   (ledger record skipped: {e})")
        else:
            print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
