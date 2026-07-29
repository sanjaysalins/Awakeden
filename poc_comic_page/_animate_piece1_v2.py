"""Piece 1 period-correction pass: animate all 15 corrected stills (stills_v2/).
Same cost tier, same proven frozen-tableau + steady-seam prompts as the first
pass (p2b/p5c -> Kling, everything else -> Seedance). p5c uses 9:16 for Kling
(3:4 isn't a supported Kling aspect ratio -- the bug hit and fixed last time).

  .venv\\Scripts\\python.exe poc_comic_page/_animate_piece1_v2.py
"""
import re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
EPISODE = "CPP_InNoWise_GoldSeam"
HERE = Path(__file__).resolve().parent
STILLS = HERE / "_piece1" / "stills_v2"
OUT = HERE / "_piece1" / "clips_v2"
OUT.mkdir(parents=True, exist_ok=True)

STEADY_SEAM = (
    "the gold seam stays a steady, unbroken line exactly where it already is -- "
    "it does not sparkle, flicker into particles, or scatter into glitter -- "
)

# (name, provider, still, ar, prompt)
JOBS = [
    ("p1a", "seedance", STILLS / "p1a_night_door.png", "1:1",
     "The composition and figure hold their exact positions and pose, perfectly "
     "still, seen from this exact high angle. INVENT NOTHING new. Only these "
     "named things may move: the warm lamplight under the door and from the "
     "wall niche breathes gently brighter and dimmer, faint dust drifts in the "
     "courtyard air, a few drifted leaves stir faintly on the stones. Nothing "
     "else in the frame changes."),

    ("p1b", "seedance", STILLS / "p1b_hesitant_hand.png", "1:1",
     "The hands hold their positions exactly, not touching the door. INVENT "
     "NOTHING new. Only: the warm glow under the door edge breathes gently, "
     "the scroll's hanging cord sways slightly. Nothing else changes."),

    ("p2a", "seedance", STILLS / "p2a_rehearsing.png", "9:16",
     "The figure and composition hold their exact positions, perfectly still. "
     "INVENT NOTHING new. Only: the warm lamplight rimming his edge breathes "
     "gently brighter and dimmer -- " + STEADY_SEAM +
     "faint dust drifts through the light. Nothing else changes."),

    ("p2b", "kling", STILLS / "p2b_jesus_speaks.png", "9:16",
     "The figure holds his exact expression, mouth, and head position "
     "unchanged -- INVENT NOTHING new, no new mouth movement, no change to "
     "his expression. Only: the warm light on his face and the gold seam "
     "along his edge breathe gently brighter and softer -- " + STEADY_SEAM +
     "faint dust motes drift through the light. Nothing else changes."),

    ("p2c", "seedance", STILLS / "p2c_the_record.png", "9:16",
     "The hand holds its exact grip on the scroll, perfectly still. INVENT "
     "NOTHING new. Only: the warm light on the parchment and wax seal "
     "breathes gently, faint dust drifts in the background light. Nothing "
     "else changes."),

    ("panel_b", "seedance", STILLS / "panel_b_door.png", "1:1",
     "The composition holds its exact framing, perfectly still. INVENT "
     "NOTHING new -- no figures or people ever appear. Only: the warm "
     "lamplight under the door and from the wall-niche lamp breathes gently "
     "brighter and dimmer, faint dust drifts in the night air, distant "
     "clouds drift very slowly in the night sky. Nothing else changes."),

    ("panel_a", "seedance", STILLS / "panel_a_jesus.png", "1:1",
     "The figure holds his exact pose and expression, perfectly still. "
     "INVENT NOTHING new. Only: the warm doorway light and the gold seam "
     "along his edge breathe gently -- " + STEADY_SEAM +
     "faint dust motes drift in the light. Nothing else changes."),

    ("panel_c", "seedance", STILLS / "panel_c_scroll.png", "1:1",
     "The hands hold their exact grip on the scroll, perfectly still. INVENT "
     "NOTHING new. Only: the light catching the hands' edge breathes gently "
     "-- " + STEADY_SEAM + "faint dust drifts in the background depth. "
     "Nothing else changes."),

    ("panel_d", "seedance", STILLS / "panel_d_threshold.png", "1:1",
     "The figure holds his exact mid-stride pose perfectly frozen -- INVENT "
     "NOTHING new, no additional steps, no new figures, no doorway change, "
     "no camera movement or zoom. Only: the warm light flooding past him "
     "breathes gently, faint dust drifts in the light. Nothing else "
     "changes, the whole frame otherwise stays pixel-identical throughout."),

    ("p4a", "seedance", STILLS / "p4a_the_exception_fear.png", "9:16",
     "The figure holds his exact pose, turned away, perfectly still. INVENT "
     "NOTHING new. Only: the door's warm light-line behind him breathes "
     "gently, faint dust drifts. Nothing else changes."),

    ("p4b", "seedance", STILLS / "p4b_the_record_nailed.png", "9:16",
     "The scroll and the wood hold their exact positions and shapes, "
     "perfectly still -- the nail and the parchment never move, no strike, "
     "no impact, nothing is driven or moves into place. INVENT NOTHING new, "
     "no figures ever appear. Only: a very slow, gentle camera drift may "
     "occur, and the darkening sky beyond breathes almost imperceptibly. "
     "Nothing else changes."),

    ("p4c", "seedance", STILLS / "p4c_empty_threshold.png", "9:16",
     "The figure holds his exact standing pose, perfectly still, viewed from "
     "behind. The camera does not move, zoom, or change angle at all. The "
     "door's exact size, shape, width, and position never change. INVENT "
     "NOTHING new. Only: the radiant light from the empty doorway pulses "
     "gently brighter and dimmer in brightness only, faint dust drifts in "
     "the light. Nothing else changes."),

    ("p5a", "kling", STILLS / "p5a_the_welcome.png", "1:1",
     "The camera does not move. Both figures stay perfectly frozen the "
     "entire time -- no limbs move, no legs move, no steps are taken, no "
     "feet lift off the ground, no heads turn, no faces change, no arms "
     "change position, no clothing shifts position, and no new figures, "
     "marks, or objects appear. INVENT NOTHING -- both figures stay "
     "pixel-for-pixel identical to this exact image throughout, holding "
     "their exact poses like statues. The gold rim-light along their edges "
     "stays a soft, steady, unbroken line -- it does not sparkle, flicker "
     "into particles, or scatter into glitter. Only these named things may "
     "move: the radiant doorway light pulses softly and evenly like a "
     "steady flame, a few dust motes drift slowly through that light. "
     "Nothing else in the frame changes.", 10),

    ("p5b", "seedance", STILLS / "p5b_record_left_behind.png", "3:4",
     "The scroll and the visible foot hold their exact positions, perfectly "
     "still. INVENT NOTHING new, no one enters or moves in this frame. Only: "
     "the warm light pooling over the parchment breathes gently. Nothing "
     "else changes."),

    ("p5c", "kling", STILLS / "p5c_jesus_face_open_door.png", "9:16",
     "The figure holds his exact pose and expression, standing in the "
     "doorway, perfectly still -- INVENT NOTHING new. The radiant gold seam "
     "along his whole edge stays a steady, unbroken, glowing line exactly "
     "where it already is -- it does not sparkle, flicker into particles, or "
     "scatter into glitter. Only these named things may move: the radiant "
     "light filling the doorway and sky behind him pulses softly and evenly "
     "like a steady flame, faint dust motes drift slowly through the light. "
     "Nothing else in the frame changes."),
]


def _find_job(model, started_after_iso):
    try:
        r = subprocess.run([HF, "generate", "list", "--video", "--size", "15", "--json"],
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


def run_job(name, provider, still, ar, prompt, duration=None):
    if not still.exists():
        print(f"   missing still: {still}")
        return False
    out = OUT / f"{name}.mp4"
    if provider == "seedance":
        model = "seedance1_5"
        extra = ["--duration", str(duration or 4), "--resolution", "720p", "--aspect_ratio", ar,
                 "--generate_audio", "false"]
    else:
        model = "kling3_0"
        extra = ["--mode", "pro", "--sound", "off", "--duration", str(duration or 5), "--aspect_ratio", ar]
    cmd = [HF, "generate", "create", model, "--start-image", str(still), "--prompt", prompt,
           "--wait"] + extra
    print(f"[clip] {name} ({model}) ...", flush=True)
    t = time.time()
    started = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED"); return False
    m = re.search(r'https?://\S+?\.mp4', blob)
    url = m.group(0) if m else None
    if not url and re.search(r"time(d)?\s*out|timeout", blob, re.IGNORECASE):
        print("   --wait timed out; polling `hf generate list` ...")
        for _ in range(20):
            time.sleep(15)
            u = _find_job(model, started)
            if u:
                url = u
                print("   recovered job via `hf generate list`")
                break
    if not url:
        print(f"   no mp4 url: {blob.strip()[-400:]}"); return False
    subprocess.run(["curl", "-s", "-L", url, "-o", str(out)], check=True)
    if out.exists() and out.stat().st_size > 0:
        try:
            cost.record_hf(EPISODE, "short", "animate", model, image=still,
                            note=f"[piece1-v2] {name}",
                            params={k.lstrip("-"): v for k, v in zip(extra[::2], extra[1::2])})
        except Exception as e:
            print(f"   (ledger skipped: {e})")
        print(f"   ok ({time.time()-t:.0f}s) -> {out}")
        return True
    print("   FAILED")
    return False


def main():
    results = []
    for job in JOBS:
        name, provider, still, ar, prompt = job[:5]
        duration = job[5] if len(job) > 5 else None
        ok = run_job(name, provider, still, ar, prompt, duration)
        if not ok:
            print("   retrying once ...")
            time.sleep(5)
            ok = run_job(name, provider, still, ar, prompt, duration)
        results.append((name, "clean" if ok else "FAILED"))
    print("\n=== summary ===")
    for name, status in results:
        print(f"  {name}: {status}")


if __name__ == "__main__":
    main()
