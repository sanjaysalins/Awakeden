"""Crop-and-recomposite test, step 2b (2026-07-25): animate pages 2 and 3's
panels individually, same as page 1 which came back clean. Completes the
3-page/12-panel test.

  .venv\\Scripts\\python.exe poc_thief_e2e/_animate_crop_test_p23.py
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
    ("page2_panel1", "16:9", "A single comic panel, medium shot of two men on crosses, one "
     "turning his head toward the other. The camera does not move. " + FROZEN +
     "Only the storm clouds behind them are alive: they roll and shift slowly."),
    ("page2_panel2", "1:1", "A single comic panel, close-up on a man's humbled face, eyes "
     "lowered. The camera does not move. " + FROZEN +
     "Only the background is alive: faint atmospheric haze drifts slowly."),
    ("page2_panel3", "1:1", "A single comic panel, close-up on a man's pleading, tearful face. "
     "The camera does not move. " + FROZEN +
     "Only the light behind him is alive: it shifts faintly and warmly."),
    ("page2_panel4", "16:9", "A single comic panel, medium shot of a crucified man turning his "
     "head slightly, listening. The camera does not move. " + FROZEN +
     "Only the environment is alive: the warm light behind him shifts faintly against the dark "
     "sky."),
    ("page3_panel1", "16:9", "A single comic panel, close-up on a crucified man's face, "
     "speaking. The camera does not move. " + FROZEN +
     "Only the light is alive: warm light behind him breaks faintly through the dark clouds."),
    ("page3_panel2", "1:1", "A single comic panel, close-up on a man's face receiving news, "
     "relief in his eyes. The camera does not move. " + FROZEN +
     "Only the light on his face is alive: it shifts faintly, warm and gentle."),
    ("page3_panel3", "16:9", "A single comic panel, symbolic wide shot of light breaking "
     "through storm clouds above three crosses. The camera does not move. " + FROZEN +
     "The clouds and light rays are alive: the clouds drift and the light shafts shift and "
     "intensify slowly."),
    ("page3_panel4", "16:9", "A single comic panel, wide landing shot of three crosses "
     "silhouetted against a darkening sky with light breaking through. The camera does not "
     "move. " + FROZEN +
     "The clouds and light are alive: they drift and shift slowly, the light growing subtly "
     "brighter above the center cross."),
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
