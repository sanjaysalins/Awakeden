"""Piece 1 Gate 3: animate the 14 remaining final stills (p5a already done and
proven glitter-free). Cost tier per v2/PRODUCTION_PLAN_400CR.md: Seedance default,
Kling for p2b (Christ face) + p5c (the earned hero shot). Every prompt uses the
project's proven frozen-tableau "INVENT NOTHING" discipline, extended with
explicit steady-seam wording (proven clean on p5a) wherever a gold seam is visible
on a figure.

  .venv\\Scripts\\python.exe poc_comic_page/_animate_piece1_final.py
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
STILLS = HERE / "_piece1" / "stills"
ROUND2 = HERE / "_piece1" / "round2"
OUT = HERE / "_piece1" / "clips"
OUT.mkdir(parents=True, exist_ok=True)

STEADY_SEAM = (
    "the gold seam stays a steady, unbroken line exactly where it already is -- "
    "it does not sparkle, flicker into particles, or scatter into glitter -- "
)

# (name, provider, still, ar, prompt)
JOBS = [
    ("p1a", "seedance", ROUND2 / "R4_p1a_dense_burden_view.png", "1:1",
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

    ("p2a", "seedance", ROUND2 / "R5_p2a_doorframe_eye.png", "9:16",
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

    ("panel_b", "seedance", ROUND2 / "R1_panel_b_door_fix.png", "1:1",
     "The composition holds its exact framing, perfectly still. INVENT "
     "NOTHING new -- no figures or people ever appear. Only: the warm "
     "lamplight under the door and from the wall-niche lamp breathes gently "
     "brighter and dimmer, the moth circles the flame slowly, faint dust "
     "drifts in the night air, distant clouds drift very slowly in the night "
     "sky. Nothing else changes."),

    ("panel_a", "seedance", STILLS / "panel_a_jesus.png", "1:1",
     "The figure holds his exact pose and expression, perfectly still. "
     "INVENT NOTHING new. Only: the warm doorway light and the gold seam "
     "along his edge breathe gently -- " + STEADY_SEAM +
     "faint dust motes drift in the light. Nothing else changes."),

    ("panel_c", "seedance", ROUND2 / "R2_panel_c_scroll_fix.png", "1:1",
     "The hands hold their exact grip on the scroll, perfectly still. INVENT "
     "NOTHING new. Only: the light catching the hands' edge breathes gently "
     "-- " + STEADY_SEAM + "faint dust drifts in the background depth. "
     "Nothing else changes."),

    ("panel_d", "seedance", ROUND2 / "R3_panel_d_threshold_fix.png", "1:1",
     "The figure holds his exact mid-stride pose perfectly frozen -- INVENT "
     "NOTHING new, no additional steps, no new figures, no doorway change. "
     "Only: the warm light flooding past him breathes gently, faint dust "
     "drifts in the light. Nothing else changes, the whole frame otherwise "
     "stays pixel-identical throughout."),

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
     "behind. INVENT NOTHING new. Only: the radiant light from the empty "
     "doorway breathes gently, faint dust drifts in the light. Nothing else "
     "changes."),

    ("p5b", "seedance", STILLS / "p5b_record_left_behind.png", "3:4",
     "The scroll and the visible foot hold their exact positions, perfectly "
     "still. INVENT NOTHING new, no one enters or moves in this frame. Only: "
     "the warm light pooling over the parchment breathes gently. Nothing "
     "else changes."),

    ("p5c", "kling", STILLS / "p5c_jesus_face_open_door.png", "3:4",
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


def run_job(name, provider, still, ar, prompt):
    if not still.exists():
        print(f"   missing still: {still}")
        return False
    out = OUT / f"{name}.mp4"
    if provider == "seedance":
        model = "seedance1_5"
        extra = ["--duration", "4", "--resolution", "720p", "--aspect_ratio", ar,
                 "--generate_audio", "false"]
    else:
        model = "kling3_0"
        extra = ["--mode", "pro", "--sound", "off", "--duration", "5", "--aspect_ratio", ar]
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
                            note=f"[piece1-final] {name}",
                            params={k.lstrip("-"): v for k, v in zip(extra[::2], extra[1::2])})
        except Exception as e:
            print(f"   (ledger skipped: {e})")
        print(f"   ok ({time.time()-t:.0f}s) -> {out}")
        return True
    print("   FAILED")
    return False


def main():
    results = []
    for name, provider, still, ar, prompt in JOBS:
        ok = run_job(name, provider, still, ar, prompt)
        if not ok:
            print("   retrying once ...")
            time.sleep(5)
            ok = run_job(name, provider, still, ar, prompt)
        results.append((name, "clean" if ok else "FAILED"))
    print("\n=== summary ===")
    for name, status in results:
        print(f"  {name}: {status}")


if __name__ == "__main__":
    main()
