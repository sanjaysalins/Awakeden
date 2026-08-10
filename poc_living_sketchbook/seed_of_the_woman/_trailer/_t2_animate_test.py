"""Trailer test batch animation (2 shots): S6 (serpent sinking) + S3 (running
couple), both on Kling with REAL INVENTED MOTION -- the one deliberate,
user-approved exception to this project's own frozen-tableau discipline,
scoped to the trailer only. No same-provider-fallback for the serpent shot
(memory living-light-no-fresh-blood + SERPENT.md: Seedance has a track
record of hallucinating extra content on this episode's own serpent
stills); the running-couple shot may fall back to Seedance if Kling fails.

  .venv\\Scripts\\python.exe poc_living_sketchbook/seed_of_the_woman/_trailer/_t2_animate_test.py
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

JOBS = [
    ("t_s6_serpent_sinking", "kling", STILLS / "t_s6_serpent_sinking.png", "16:9", False,
     "The coiled serpent begins exactly as shown, ink-blue-toned, holding its "
     "coiled position at first. As the moment passes, the advancing warm "
     "light-band visible at the frame's edge sweeps forward and reaches the "
     "coils; as the light touches it, the serpent's raised coils lower and "
     "flatten belly-down into the dust, sinking low and going still by the "
     "end -- a real, deliberate defensive lowering away from the light, NOT "
     "an attack, NOT rearing up, NOT opening its jaws, no aggression, no "
     "striking motion of any kind. The head stays in profile throughout, "
     "never turning to face the camera, never close enough to read as a "
     "face shot. No second creature ever appears. Ink-blue coloring "
     "throughout, never gold, never warm on the creature itself. Nothing "
     "else invented."),
    ("t_s3_running", "kling", STILLS / "t_s3_running.png", "16:9", True,
     "Both figures continue their exact running motion shown in the still -- "
     "real forward-driving locomotion, arms and legs continuing to pump "
     "naturally stride after stride, genuine sustained running through the "
     "undergrowth, the camera continuing to track alongside them at the "
     "same distance and framing. Their faces keep the same fearful "
     "expression throughout, no new gesture, no change of direction, no "
     "stumbling, no falling, no turning to face the camera. The garden's "
     "foliage and golden light continue streaming past in the foreground "
     "blur. Nothing else invented."),
]

_OTHER_PROVIDER = {"kling": "seedance", "seedance": "kling"}


def run_job(name, provider, still, ar, prompt):
    out = OUT / f"{name}.mp4"
    if provider == "seedance":
        model = "seedance1_5"
        extra = ["--duration", "4", "--resolution", "720p", "--aspect_ratio", ar, "--generate_audio", "false"]
    else:
        model = "kling3_0"
        extra = ["--mode", "pro", "--sound", "off", "--duration", "5", "--aspect_ratio", ar]
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
            cost.record_hf(EPISODE, "long", "trailer_test_animate", model, image=still,
                            note=f"[trailer] {name}")
        except Exception as e:
            print(f"   (ledger skipped: {e})")
        print(f"   ok ({time.time()-t:.0f}s) -> {out}")
        return True
    print("   FAILED")
    return False


def main():
    for name, provider, still, ar, allow_fallback, prompt in JOBS:
        out = OUT / f"{name}.mp4"
        if out.exists():
            print(f"[skip] {name}")
            continue
        ok = run_job(name, provider, still, ar, prompt)
        if not ok and allow_fallback:
            fallback = _OTHER_PROVIDER[provider]
            print(f"   retrying with {fallback} instead of {provider} ...")
            ok = run_job(name, fallback, still, ar, prompt)
        print(f"  -> {'ok' if ok else 'FAILED'}")


if __name__ == "__main__":
    main()
