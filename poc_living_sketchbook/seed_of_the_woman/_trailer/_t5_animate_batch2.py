"""Trailer batch 2 animation: S1, S2, S4, S5, S9, S10. Applies the user's
own lesson from S3's rejected v1: any shot with a legible human face gets
its motion LOCKED (camera-only, matching this project's own frozen-tableau
convention) rather than asked to hold continuous character animation.
Real invented motion is reserved for content with no face at risk (S2's
object drop) or where the face is too small/distant to matter (S5, S9 --
locked anyway, as a defensive floor, not because it was strictly needed).

  .venv\\Scripts\\python.exe poc_living_sketchbook/seed_of_the_woman/_trailer/_t5_animate_batch2.py
"""
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
STILLS = HERE / "stills"
OUT = HERE / "clips"
OUT.mkdir(parents=True, exist_ok=True)

LOCK_FACE = (
    "Every figure holds their EXACT position, pose, and facial expression, "
    "perfectly still -- INVENT NOTHING new in the body or face, no new "
    "gesture, no head turn, no expression change. Only the camera itself "
    "and the named light may move. "
)

JOBS = [
    ("t_s1_eden_wide", "seedance", STILLS / "t_s1_eden_wide.png", "16:9", 4,
     "No figures present. The trees and canopy hold their exact shapes, "
     "perfectly still. Only: the camera slowly, steadily pushes forward "
     "through the garden toward the bright gap between the two central "
     "trees, a smooth continuous push that gently accelerates; the mist "
     "drifts and the gold light shafts breathe very gently as the camera "
     "moves. Nothing else invented."),
    ("t_s2_fruit_falling", "kling", STILLS / "t_s2_fruit_falling.png", "16:9", 5,
     "The hand at the top of frame holds its exact position, it does not "
     "move or grip further. Only the fruit itself: it continues falling "
     "from where it is shown, drops down out of frame at the bottom, "
     "then the camera holds on the bare blurred earth for a beat as a "
     "single soft impact and a small puff of dust rise from just below "
     "frame, and the warm golden light in the scene fades down to a "
     "cooler ink-blue tone as the moment lands. No new object, no second "
     "fruit, nothing else invented."),
    ("t_s4_hiding_light", "seedance", STILLS / "t_s4_hiding_light.png", "16:9", 4,
     LOCK_FACE +
     "Only: the warm gold light shaft on the right slowly, steadily "
     "grows nearer and brighter, advancing across the ground toward the "
     "two figures without quite reaching them by the end. Nothing else "
     "changes."),
    ("t_s5_sentencing_wide", "kling", STILLS / "t_s5_sentencing_wide.png", "16:9", 5,
     LOCK_FACE +
     "The two small distant figures do not move at all. Only: the camera "
     "performs a real continuous crane movement, rising and pulling back "
     "slightly, revealing more of the towering column of light and the "
     "vast dark sky above -- a smooth single camera move, no cuts. "
     "Nothing else invented."),
    ("t_s9_cross_wide", "kling", STILLS / "t_s9_cross_wide.png", "16:9", 5,
     LOCK_FACE +
     "The figure on the cross does not move at all, holding the exact "
     "bowed pose shown. Only: the camera performs a real continuous rise, "
     "craning upward from ground level toward the cross against the dark "
     "sky, a smooth single unhurried move, no cuts, ending closer to the "
     "cross than it started. Nothing else invented."),
    ("t_s10_tomb_wide", "seedance", STILLS / "t_s10_tomb_wide.png", "16:9", 4,
     "No figure present. The stone, doorway, and folded linen hold their "
     "exact positions, perfectly still. Only: the camera slowly pushes "
     "forward into the tomb's doorway, the warm gold light growing "
     "steadily brighter and beginning to bloom toward the frame's edges "
     "as the camera nears it. Nothing else invented."),
]


def run_job(name, provider, still, ar, prompt, duration):
    out = OUT / f"{name}.mp4"
    if provider == "seedance":
        model = "seedance1_5"
        extra = ["--duration", str(duration), "--resolution", "720p", "--aspect_ratio", ar, "--generate_audio", "false"]
    else:
        model = "kling3_0"
        extra = ["--mode", "pro", "--sound", "off", "--duration", str(duration), "--aspect_ratio", ar]
    cmd = [HF, "generate", "create", model, "--start-image", str(still), "--prompt", prompt,
           "--wait"] + extra
    print(f"[clip] {name} ({model}) ...", flush=True)
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED")
        return False
    m = re.search(r'https?://\S+?\.mp4', blob)
    url = m.group(0) if m else None
    if not url:
        print(f"   no mp4 url: {blob.strip()[-400:]}")
        return False
    subprocess.run(["curl", "-s", "-L", url, "-o", str(out)], check=True)
    if out.exists() and out.stat().st_size > 0:
        try:
            cost.record_hf(EPISODE, "long", "trailer_batch2_animate", model, image=still,
                            note=f"[trailer] {name}")
        except Exception as e:
            print(f"   (ledger skipped: {e})")
        print(f"   ok ({time.time()-t:.0f}s) -> {out}")
        return True
    print("   FAILED")
    return False


_OTHER_PROVIDER = {"kling": "seedance", "seedance": "kling"}


def main():
    for name, provider, still, ar, duration, prompt in JOBS:
        out = OUT / f"{name}.mp4"
        if out.exists():
            print(f"[skip] {name}")
            continue
        ok = run_job(name, provider, still, ar, prompt, duration)
        if not ok:
            fallback = _OTHER_PROVIDER[provider]
            print(f"   retrying with {fallback} instead of {provider} ...")
            ok = run_job(name, fallback, still, ar, prompt, duration)
        print(f"  -> {'ok' if ok else 'FAILED'}")


if __name__ == "__main__":
    main()
