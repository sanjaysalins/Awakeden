"""Standalone retry for S2 (fruit falling) after 2 transient API failures
in the main batch."""
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
EPISODE = "SeedOfTheWoman"
HERE = Path(__file__).resolve().parent
still = HERE / "stills" / "t_s2_fruit_falling.png"
dest = HERE / "clips" / "t_s2_fruit_falling.mp4"

prompt = (
    "The hand at the top of frame holds its exact position, it does not "
    "move or grip further. Only the fruit itself: it continues falling "
    "from where it is shown, drops down out of frame at the bottom, "
    "then the camera holds on the bare blurred earth for a beat as a "
    "single soft impact and a small puff of dust rise from just below "
    "frame, and the warm golden light in the scene fades down to a "
    "cooler ink-blue tone as the moment lands. No new object, no second "
    "fruit, nothing else invented."
)

cmd = [HF, "generate", "create", "kling3_0", "--start-image", str(still), "--prompt", prompt,
       "--wait", "--mode", "pro", "--sound", "off", "--duration", "5", "--aspect_ratio", "16:9"]

for attempt in range(3):
    print(f"[clip] t_s2_fruit_falling attempt {attempt+1} ...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED")
        break
    m = re.search(r'https?://\S+?\.mp4', blob)
    if m:
        subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(dest)], check=True)
        if dest.exists() and dest.stat().st_size > 0:
            try:
                cost.record_hf(EPISODE, "long", "trailer_batch2_animate", "kling3_0", image=still,
                                note="[trailer] t_s2_fruit_falling")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print(f"   ok -> {dest}")
            break
    print(f"   no mp4 url: {blob.strip()[-300:]}")
    time.sleep(15)
else:
    print("   FAILED after retries")
