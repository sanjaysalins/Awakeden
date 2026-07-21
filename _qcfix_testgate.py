"""Clip-QC fix TEST-GATE (user-approved ~$4, 2026-07-19): one re-roll per failure
class into _qcfix_test/ (originals untouched). Recipes under test:
  - blood class    : POSITIVE-ONLY wound language (the 2026-07-19 negative recipe
                     "no blood grows/drips" leaked on all 6 clips it touched — and
                     naming-the-noun-draws-it is the documented seedream failure mode)
  - EW01 snow      : particle/mote words stripped entirely (feedback-veo-no-glitter-glow)
  - EW01 invention : push-in ONLY (pull-backs out-paint past the painting's edge)
  - writing class  : scroll described as fixed-as-painted, camera led away from it
Verdict after render: extract QC frames, eyeball, pick winners, THEN batch.
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

LF = ROOT / "longform"

STILL_RULE = ("The entire painting holds perfectly still like a printed page — every "
              "figure, face, and mark stays fixed exactly as painted. Only the camera moves.")

JOBS = [
    # 1. BLOOD class — Seedance, positive-only (never names the fluid)
    dict(ep="04_The_Bronze_Serpent", model="seedance1_5", dur="4",
         png=LF / "04_The_Bronze_Serpent/v1/visual_16x9_inked/31_his_own_self_bare_our_sins_in_his_own_body_on_the_tree.png",
         out=LF / "04_The_Bronze_Serpent/v1/visual_16x9_inked/clips/_qcfix_test/31_his_own_self_bare_our_sins_in_his_own_body_on_the_tree.mp4",
         prompt=("Graphic novel inked illustration, a frozen painted tableau. Christ crucified "
                 "on a wooden cross against a darkened storm sky, head bowed low, arms "
                 "outstretched, wearing a simple cream-white robe, small dark marks at each "
                 "wrist fixed exactly as painted. " + STILL_RULE +
                 " The camera settles almost imperceptibly, resting on the scene. The storm "
                 "clouds hold their painted shapes.")),
    # 2. EW01 SNOW class — veo3, zero particle vocabulary
    dict(ep="EW01_Two_Goats", model="veo3_1_lite", dur="8",
         png=LF / "EW01_Two_Goats/v1/visual_16x9/07_they_brought_me_two_goats_and_i_cast_lot.png",
         out=LF / "EW01_Two_Goats/v1/visual_16x9/_qcfix_test/07_they_brought_me_two_goats_and_i_cast_lot.mp4",
         prompt=("Baroque oil painting, a frozen painted moment. An old high priest in white "
                 "robes holds two small stone lots above a bronze basin, two goats standing "
                 "beside him before the goat-hair tent. The one thin plume of incense smoke "
                 "already in the painting drifts slowly upward. " + STILL_RULE +
                 " The camera pushes in very slowly toward the priest's hands. Steady warm "
                 "afternoon light.")),
    # 3. EW01 INVENTION class — veo3, push-in only (the original pull-back fabricated a panorama)
    dict(ep="EW01_Two_Goats", model="veo3_1_lite", dur="8",
         png=LF / "EW01_Two_Goats/v1/visual_16x9/slice_13.png",
         out=LF / "EW01_Two_Goats/v1/visual_16x9/_qcfix_test/slice_13.mp4",
         prompt=("Baroque oil painting, a frozen painted moment. Israelites in earth-toned "
                 "robes gathered close outside a large goat-hair tent at sunset, warm "
                 "firelight glowing from the tent opening. " + STILL_RULE +
                 " The camera pushes in very slowly toward the glowing tent entrance, staying "
                 "inside the painting's own edges. Steady warm evening light.")),
    # 4. WRITING class — Seedance, scroll fixed-as-painted, camera led to the face
    dict(ep="02_Psalm_22", model="seedance1_5", dur="4",
         png=LF / "02_Psalm_22_Song_From_The_Cross/v1/visual_16x9_inked/david_psalmist.png",
         out=LF / "02_Psalm_22_Song_From_The_Cross/v1/visual_16x9_inked/clips/_qcfix_test/david_psalmist.mp4",
         prompt=("Graphic novel inked illustration, a frozen painted tableau. David seated "
                 "under a vast starry night sky, singing upward, holding a wooden lyre, a "
                 "rolled parchment scroll resting on the ground beside him fixed exactly as "
                 "painted. " + STILL_RULE +
                 " The camera pushes in slowly toward his upturned face. The stars hold "
                 "steady.")),
]

cli = str(config.HF_CLI_PATH)
ok = fail = 0
for j in JOBS:
    if not j["png"].exists():
        print(f"[skip] missing still: {j['png']}")
        fail += 1
        continue
    print(f"[test] {j['png'].stem} ({j['model']}) ...", flush=True)
    cmd = [cli, "generate", "create", j["model"],
           "--start-image", str(j["png"]),
           "--prompt", j["prompt"],
           "--duration", j["dur"],
           "--aspect_ratio", "16:9",
           "--wait"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=900)
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if "nsfw" in blob.lower():
        print(f"       FAIL (NSFW): {blob[-200:]}")
        fail += 1
        continue
    m = re.search(r"https://\S+?\.mp4", r.stdout or "", re.IGNORECASE)
    if r.returncode != 0 or not m:
        print(f"       FAIL ({r.returncode}): {blob[-300:]}")
        fail += 1
        continue
    j["out"].parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(m.group(0), headers={"User-Agent": "JesusInTheBible/1.0"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        j["out"].write_bytes(resp.read())
    print(f"       ok -> {j['out']}")
    try:
        cost.record_hf(j["ep"], "long", "clip", j["model"], note=f"{j['png'].stem} (qcfix test-gate)")
    except Exception as e:
        print(f"       [cost] ledger row failed (non-fatal): {e}")
    ok += 1

print(f"\n[done] {ok} ok, {fail} failed")
