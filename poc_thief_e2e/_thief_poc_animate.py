"""Animate the 3 Thief POC pages with Kling 3.0 direct (2026-07-25), the
top pick from today's bake-off. Same simple prompt that performed best
there -- no heavy FROZEN engineering, accepting the known invention/drift
risk per the user's explicit choice.

  .venv\\Scripts\\python.exe poc_thief_e2e/_thief_poc_animate.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills" / "_thief_poc"
OUT = HERE / "clips" / "_thief_poc"
OUT.mkdir(parents=True, exist_ok=True)

PROMPT = (
    "Animate this comic book page. Bring all four panels to life with subtle, natural motion "
    "in each one, while keeping every character exactly as drawn."
)

PAGES = ["page1", "page2", "page3"]


def main():
    for name in PAGES:
        png = STILLS / f"{name}.png"
        out = OUT / f"{name}.mp4"
        cmd = [HF, "generate", "create", "kling3_0", "--start-image", str(png), "--prompt", PROMPT,
               "--duration", "5", "--aspect_ratio", "9:16", "--mode", "pro", "--sound", "off", "--wait"]
        print(f"[clip] {name} kling3_0 5s -> {out.name} ...", flush=True)
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
                cost.record_hf("EW_Thief_POC", "short", "animate", "kling3_0", note=f"[poc-animate] {name}",
                                params={"mode": "pro", "sound": "off", "duration": 5})
            except Exception as e:
                print(f"   (ledger record skipped: {e})")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
