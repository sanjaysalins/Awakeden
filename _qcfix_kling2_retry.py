"""Second Kling pass on the 2 clips that still failed after the first Kling
round (nail_through_hand, lots_dice_closeup). Uses the project's OWN proven
precedent phrasing from longform/04_The_Bronze_Serpent/_animate_hero_clips.py:
- "21_look_to_the_one_lifted_up_hero_close" held a wound dry on Kling via
  EXPLICIT "no blood flows, drips, spreads, brightens, pools or grows".
- "15_hezekiah_breaks_the_brazen_serpent" held a mid-strike action frozen on
  Kling via EXPLICIT "the maul NEVER move or swing, no new motion of the
  strike itself" -- extending that same template to the lots' bones.
Cheaper first try than a still-level redesign; only escalate to a Gemini
still-edit if this explicit-language recipe doesn't hold.
"""
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

FROZEN = ("Every figure stays perfectly frozen the entire time -- no limbs move, no heads "
          "turn, no faces change, no morphing, no new figures, hands or objects appear. "
          "INVENT NOTHING: show only what is already painted in this exact image.")

JOBS = [
    dict(slug="nail_through_hand", lane="isaiah53", aspect="9:16",
         still=(ROOT / "longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked"
                "/clips/_qcfix_test/nail_through_hand_dry.png"),
         out=(ROOT / "longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked"
              "/clips/_qcfix_test/nail_through_hand_kling2.mp4"),
         prompt=(
             "A still finished inked graphic-novel illustration on flat canvas, filmed as "
             "ONE very slow, gentle push toward the outstretched fingertips at the lower "
             "right of the frame. The nail stays driven EXACTLY where painted, never lifts "
             "or shifts. The small wound mark at the nail stays EXACTLY as painted, dry and "
             "still -- no blood flows, drips, spreads, brightens, pools, or grows, not even "
             "slightly, for the entire clip. " + FROZEN + " ONLY the light is alive: the "
             "dim glow across the wood grain breathes gently, holding its exact painted "
             "tone from first frame to last.")),
    dict(slug="lots_dice_closeup", lane="psalm22", aspect="16:9",
         still=(ROOT / "longform/02_Psalm_22_Song_From_The_Cross/v1/visual_16x9_inked"
                "/lots_dice_closeup.png"),
         out=(ROOT / "longform/02_Psalm_22_Song_From_The_Cross/v1/visual_16x9_inked"
              "/clips/_qcfix_test/lots_dice_closeup_kling2.mp4"),
         prompt=(
             "A still finished inked graphic-novel illustration on flat canvas, filmed as "
             "ONE very slow push down toward the folds of the white garment at the lower "
             "right of frame. The knucklebones stay held EXACTLY where painted -- the ones "
             "already resting on the cloth NEVER move again, and the ones shown suspended "
             "in the air NEVER fall, drop, land, or move further, for the entire clip; the "
             "soldiers' hands and arms NEVER move, release, or open further. " + FROZEN +
             " ONLY the light is alive: the warm dusty light across the cloth breathes "
             "gently, holding its exact painted tone from first frame to last.")),
]

cli = str(config.HF_CLI_PATH)
ok = fail = 0
for j in JOBS:
    print(f"[roll] {j['slug']} (kling3_0 pro) ...", flush=True)
    cmd = [cli, "generate", "create", "kling3_0",
           "--start-image", str(j["still"]), "--prompt", j["prompt"],
           "--duration", "5", "--aspect_ratio", j["aspect"],
           "--mode", "pro", "--sound", "off", "--wait"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=900)
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    m = re.search(r"https://\S+?\.mp4", r.stdout or "", re.IGNORECASE)
    if "nsfw" in blob.lower() or r.returncode != 0 or not m:
        print(f"       FAIL ({r.returncode}): {blob[-300:]}")
        fail += 1
        continue
    j["out"].parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(m.group(0), headers={"User-Agent": "JesusInTheBible/1.0"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        j["out"].write_bytes(resp.read())
    try:
        cost.record_hf(j["lane"] if j["lane"] != "isaiah53" else "01_Isaiah_53",
                       "long", "clip", "kling3_0", note=f"{j['slug']} (qcfix Kling retry 2)")
    except Exception as e:
        print(f"       [cost] ledger row failed (non-fatal): {e}")
    print(f"       ok -> {j['out']}")
    ok += 1

print(f"\n[done] {ok} ok, {fail} failed")
