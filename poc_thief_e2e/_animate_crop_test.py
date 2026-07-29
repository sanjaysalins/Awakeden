"""Crop-and-recomposite test, step 2 (2026-07-25): animate each cropped panel
INDIVIDUALLY -- nothing else in frame for Kling to invent onto. Tests whether
this actually solves the invention problem the whole-page approach couldn't.
Page 1 only (test-gate slice, 4 panels) before committing to pages 2-3.

  .venv\\Scripts\\python.exe poc_thief_e2e/_animate_crop_test.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
HERE = Path(__file__).resolve().parent
PANELS = HERE / "stills" / "_crop_test" / "panels"
OUT = HERE / "clips" / "_crop_test"
OUT.mkdir(parents=True, exist_ok=True)

FROZEN = (
    "Every figure stays perfectly frozen the entire time -- no limbs move, no heads turn, no "
    "faces change, no expressions change, no skin changes, no hair moves, no clothing moves, "
    "no held objects move, and no new figures, marks, or objects appear. INVENT NOTHING -- the "
    "figure stays pixel-for-pixel identical to this exact image throughout. "
)

JOBS = [
    ("page1_panel1", "16:9", "A single comic panel, wide shot of three crucified figures "
     "against a stormy sky. The camera does not move. " + FROZEN +
     "Only the storm clouds are alive: they roll and churn slowly, and lightning flickers "
     "faintly in the far background sky, never touching any figure."),
    ("page1_panel2", "1:1", "A single comic panel, tight close-up on a man's angry, shouting face. "
     "The camera does not move. " + FROZEN +
     "Only the background is alive: the stormy sky visible at the edge of frame shifts and "
     "drifts faintly."),
    ("page1_panel3", "1:1", "A single comic panel, tight close-up on a man's face. The camera does "
     "not move. " + FROZEN +
     "Only the background is alive: faint atmospheric haze drifts slowly behind him."),
    ("page1_panel4", "16:9", "A single comic panel, medium-wide shot of a crucified man on a cross, "
     "soldiers and a crowd in the background. The camera does not move. " + FROZEN +
     "Only the environment is alive: the storm clouds behind him drift and shift slowly, and "
     "the light on the horizon flickers faintly. Nothing on his body or face changes."),
]


def main():
    for name, ar, prompt in JOBS:
        png = PANELS / f"{name}.png"
        out = OUT / f"{name}.mp4"
        cmd = [HF, "generate", "create", "kling3_0", "--start-image", str(png), "--prompt", prompt,
               "--duration", "5", "--aspect_ratio", ar, "--mode", "pro", "--sound", "off", "--wait"]
        print(f"[clip] {name} ...", flush=True)
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
                cost.record_hf("EW_Thief_POC", "short", "animate", "kling3_0", note=f"[crop-test] {name}",
                                params={"mode": "pro", "sound": "off", "duration": 5})
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
