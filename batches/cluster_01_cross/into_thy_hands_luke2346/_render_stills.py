#!/usr/bin/env python
"""into_thy_hands_luke2346 stills via BytePlus (~$0.25). Lint-gated. Idempotent."""
import argparse, importlib.util, json, sys, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
FFT = HERE.parent / "father_forgive_them"
PZ = HERE.parent / "pierced_zech1210"
ROOT = HERE.parents[2]
OUT = HERE / "visual"
MODEL = "seedream-4-5-251128"; SIZE = "1440x2560"
BASE = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"
REF_JESUS = PZ / "visual" / "face_on_cross.png"

bp_spec = importlib.util.spec_from_file_location("bp", FFT / "byteplus_seedream.py")
bp = importlib.util.module_from_spec(bp_spec); bp_spec.loader.exec_module(bp)
sys.path.insert(0, str(ROOT))
from render_lint import lint as _lint, guard_prompt, arm_audit

JOBS = {
 "child_sleeping_lamp": ("a small child asleep on a woven mat under a wool blanket, a clay oil lamp burning low beside, a mother's silhouette in the doorway, warm night interior, vertical, ancient Judea", None),
 "psalm_scroll_night": ("an open scroll of faded illegible script beside a burning clay oil lamp on a rough table at night, warm lamplight, close, vertical, ancient Judea", None),
 "father_holds_sleeping_child": ("a bearded father cradling his sleeping child against his shoulder by lamplight, the child's face at peace, warm night interior, close, vertical, ancient Judea", None),
 "hands_of_light_open": ("two vast gentle hands formed of warm golden light opening downward through parted storm clouds, rays spilling from the palms, vertical", None),
 "child_waking_dawn": ("a child stirring awake on a mat as warm dawn light pours through a small window, eyes just opening, hopeful morning interior, vertical, ancient Judea", None),
 "father_hand_childs_hand": ("a small child's hand resting inside a large weathered father's hand, a small clay oil lamp burning beside them, dark wool cloth behind, close, vertical, ancient Judea", None),
 "father_lamp_doorway": ("a robed father holding a small clay oil lamp in the doorway of a stone house at night, warm light spilling across the threshold, seen from inside the dark room, vertical, 1st-century Judea", None),
 "child_eyes_closing": ("a small child's peaceful face with eyes gently closed, tucked under a wool blanket, a large weathered hand resting on the blanket, a small clay oil lamp burning low nearby, close, vertical, ancient Judea", None),
 "cross_at_dawn": ("an empty wooden cross standing on a rocky hilltop against a golden sunrise, warm light flooding the sky, wide, vertical, 1st-century Judea", None),
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
    print("\n$0 dry-run. --render to spend (~$0.25)."); sys.exit(0)

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

