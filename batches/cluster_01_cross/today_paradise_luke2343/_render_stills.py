#!/usr/bin/env python
"""Today in Paradise (Luke 23:43) — 6 new 9:16 stills via BytePlus Seedream (~$0.30).
Lint-gated ($0). Idempotent. Jesus identity via the pierced crucified ref (same cluster)."""
import argparse, importlib.util, json, sys, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
FFT = HERE.parent / "father_forgive_them"
PZ = HERE.parent / "pierced_zech1210"
ROOT = HERE.parents[2]
OUT = HERE / "visual"
MODEL = "seedream-4-5-251128"; SIZE = "1440x2560"
BASE = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"
REF_JESUS_CROSS = PZ / "visual" / "face_on_cross.png"

bp_spec = importlib.util.spec_from_file_location("bp", FFT / "byteplus_seedream.py")
bp = importlib.util.module_from_spec(bp_spec); bp_spec.loader.exec_module(bp)
sys.path.insert(0, str(ROOT))
from render_lint import lint as _lint, guard_prompt, arm_audit

JOBS = {
 "mocker_thief_face": ("a lean criminal on a cross, face twisted in a snarl as he shouts sideways, his wrists pierced to the beam, a dark ragged pierced wound at each wrist with dark red blood, storm sky behind, low angle, vertical, 1st-century Judea", None),
 "penitent_thief_face": ("a CLOSE upper-body portrait of a gaunt weather-beaten OLDER criminal with a broad heavy face, a balding head with short-cropped grey hair, a heavy lined weathered face and a coarse grey stubble beard, crucified on a single rough wooden cross, one bare arm stretched out and roped at the wrist to the horizontal crossbeam, the wrist bound with coils of rope, no wound, at the edge of the frame, head bowed low, tears cutting through the grime on his cheeks, spent and humble, storm light, vertical, 1st-century Judea", None),
 "thief_looks_to_jesus": ("a penitent criminal crucified on his own single wooden cross on a barren dusty Golgotha hilltop, a bald weather-beaten older man, his arms stretched out and roped at the wrists to his crossbeam and his feet bound to the post with rope, no wounds, his body sagging, the bare clean dusty ground at the foot of the cross empty, his head LIFTED and clearly turned to the side to gaze across toward the thorn-crowned Christ crucified on a separate single cross a short distance away, dry blowing dust and dark storm sky, a medium shot from the side so BOTH crosses stand clear on the hill, vertical, 1st-century Judea", None),
 "jesus_turns_to_thief": ("a CLOSE portrait of the thorn-crowned crucified Christ against a plain dark empty storm sky, one single plain vertical wooden post directly behind his back and one horizontal crossbeam behind his shoulders, his arms stretched out and nailed along that one crossbeam, his head turned gently to one side, eyes open and steady with quiet compassion, vertical, 1st-century Judea", REF_JESUS_CROSS),
 "thief_nailed_hand": ("a weathered hand nailed through the palm to a rough wooden crossbeam, rope wound around the wrist, fingers curled, storm light, close, vertical, 1st-century", None),
 "two_thieves_wide": ("three men crucified high on three rough wooden crosses on a barren hilltop, arms outstretched on the crossbeams, the middle cross taller, seen from a low angle, heavy storm sky, wide, vertical, 1st-century Judea", None),
 "confession_face_hands": ("an OLDER criminal's weathered face — short-cropped grey hair, grey stubble — pressed near his hand held flat to the wooden beam, a small dark wound and a little dark blood on the back of the hand, eyes shut, jaw tight, storm light, close, vertical, 1st-century", None),
 "kingdom_light_clouds": ("a single shaft of pale light opening through heavy dark storm clouds over distant Judean hills, the light is the subject, vertical, ancient", None),
 "answer_light_profile": ("the thorn-crowned head in quiet profile against a break of warm light in the storm clouds, calm and steady, close, vertical, 1st-century Judea", REF_JESUS_CROSS),
 "paradise_dawn": ("warm golden dawn light flooding over a ridge of cypress and olive trees into a still garden valley, soft mist catching the light, seen from below, vertical, ancient Judea", None),
}

ap = argparse.ArgumentParser(); ap.add_argument("--render", action="store_true"); ap.add_argument("--force", action="store_true")
ap.add_argument("--only", default="")
a = ap.parse_args()
only = {s for s in a.only.split(",") if s.strip()}
block = False
for slug, (prompt, ref) in JOBS.items():
    finds = _lint(prompt, stage="still")
    bad = [f for f in finds if str(f.get("level", f.get("severity", "warn"))).lower() == "block"]
    print(f"{slug:24} lint: {len(finds)} finding(s){' BLOCK' if bad else ''}")
    for f in finds:
        print("   !", json.dumps(f)[:110])
    block |= bool(bad)
if block:
    sys.exit("BLOCKED by lint")
if not a.render:
    print("\n$0 dry-run. --render to spend (~$0.30)."); sys.exit(0)

def call(prompt, dest, ref):
    prompt = guard_prompt(prompt)  # fail-closed: auto-fix poison tokens before the paid call
    body = {"model": MODEL, "prompt": prompt + bp.STYLE + bp.ONE, "size": SIZE,
            "response_format": "url", "watermark": False}
    if ref is not None:
        body["image"] = bp._ref_to_field(str(ref)); body["sequential_image_generation"] = "disabled"
    req = urllib.request.Request(BASE, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {bp._load_key()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=240) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode()[:200]}"
    url = resp.get("data", [{}])[0].get("url")
    if not url:
        return "no-url"
    with urllib.request.urlopen(url, timeout=240) as im:
        dest.write_bytes(im.read())
    arm_audit(dest)  # fail-closed: pending-FAIL sidecar until a real PASS is recorded
    return "ok"

for slug, (prompt, ref) in JOBS.items():
    if only and slug not in only:
        continue
    dest = OUT / f"{slug}.png"
    if dest.exists() and not a.force:
        print(f"[skip] {slug}"); continue
    print(f"{slug:24} -> {call(prompt, dest, ref)}")
print("DONE")
