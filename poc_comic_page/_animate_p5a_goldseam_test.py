"""Real animation test: does the Gold Seam's glowing rim-light survive Kling animation
without turning into glitter/sparkle particles (the documented veo/Kling failure mode on
bright Christ-light scenes, see memory feedback-veo-no-glitter-glow)? Animates the NEW
Piece-1 p5a_the_welcome.png (the most gold-heavy still) with the project's proven frozen-
tableau "INVENT NOTHING" discipline (poc_comic_page/rung2/_animate_panels.py FROZEN_P5A),
extended with explicit steady-seam wording to proactively guard the new gold-rim element
the old ink style never had to. Kling3_0 pro, sound off, 5s, ~7.5cr ($1.13).

  .venv\\Scripts\\python.exe poc_comic_page/_animate_p5a_goldseam_test.py
"""
import re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "kling3_0"
EPISODE = "CPP_InNoWise_GoldSeam"
HERE = Path(__file__).resolve().parent
STILL = HERE / "_piece1" / "stills" / "p5a_the_welcome.png"
OUT = HERE / "_piece1" / "clips"
OUT.mkdir(parents=True, exist_ok=True)
AR = "1:1"

PROMPT = (
    "The camera does not move. Both figures stay perfectly frozen the entire "
    "time -- no limbs move, no legs move, no steps are taken, no feet lift off "
    "the ground, no heads turn, no faces change, no arms change position, no "
    "clothing shifts position, and no new figures, marks, or objects appear. "
    "INVENT NOTHING -- both figures stay pixel-for-pixel identical to this "
    "exact image throughout, holding their exact poses like statues. The thin "
    "gold rim-light along their edges stays a soft, steady, unbroken line of "
    "light exactly where it already is -- it does not sparkle, flicker into "
    "particles, scatter into glitter, or spread beyond its exact current "
    "shape. Only these named things may move: the radiant doorway light "
    "behind them pulses softly and evenly like a steady flame, a few dust "
    "motes drift slowly through that light. Nothing else in the frame "
    "changes."
)


def _find_job(model, started_after_iso):
    try:
        r = subprocess.run([HF, "generate", "list", "--video", "--size", "10", "--json"],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
        import json
        jobs = json.loads(r.stdout or "[]")
    except Exception as e:
        print(f"   (job lookup failed: {e})")
        return None
    for j in jobs:
        if j.get("job_type") == model and j.get("created_at", "") >= started_after_iso:
            if j.get("status") == "completed" and j.get("result_url"):
                return j["result_url"]
    return None


def main():
    assert STILL.exists(), f"missing {STILL}"
    out = OUT / "p5a_goldseam_test.mp4"
    started = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    cmd = [HF, "generate", "create", MODEL, "--start-image", str(STILL), "--prompt", PROMPT,
           "--mode", "pro", "--sound", "off", "--duration", "5", "--aspect_ratio", AR, "--wait"]
    print("[clip] p5a_goldseam_test (kling3_0 pro) ...", flush=True)
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED"); return
    m = re.search(r'https?://\S+?\.mp4', blob)
    if not m and re.search(r"time(d)?\s*out|timeout", blob, re.IGNORECASE):
        print("   --wait timed out; polling `hf generate list` ...")
        for _ in range(20):
            time.sleep(15)
            u = _find_job(MODEL, started)
            if u:
                m = re.search(r'https?://\S+?\.mp4', u) or type("x", (), {"group": lambda s, i: u})()
                break
    if not m:
        print(f"   no mp4 url: {blob.strip()[-500:]}"); return
    url = m.group(0) if hasattr(m, "group") else m
    subprocess.run(["curl", "-s", "-L", url, "-o", str(out)], check=True)
    if out.exists() and out.stat().st_size > 0:
        row = cost.record_hf(EPISODE, "short", "animate_test", MODEL, image=STILL,
                              note="[goldseam-glitter-test] p5a",
                              params={"mode": "pro", "sound": "off", "duration": "5", "aspect_ratio": AR})
        print(f"   ok ({time.time()-t:.0f}s) -> {out}  est ${row.get('est_usd')}")
    else:
        print("   FAILED")


if __name__ == "__main__":
    main()
