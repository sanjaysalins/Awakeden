#!/usr/bin/env python
"""watch_one_hour_matt2640 stills via BytePlus (~$0.25). Lint-gated. Idempotent."""
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
REF_PRAY = HERE.parent / "it_is_finished_john1930" / "visual" / "jesus_prays_night.png"

bp_spec = importlib.util.spec_from_file_location("bp", FFT / "byteplus_seedream.py")
bp = importlib.util.module_from_spec(bp_spec); bp_spec.loader.exec_module(bp)
sys.path.insert(0, str(ROOT))
from render_lint import lint as _lint, guard_prompt, arm_audit

JOBS = {
 "gethsemane_olives_night": ("a moonlit olive grove on a hillside at night, gnarled ancient trees casting long shadows, a distant city wall below, deep blue night, wide, vertical, 1st-century Judea", None),
 "disciples_sleeping": ("three robed men slumped asleep against the roots of an ancient olive tree at night, cloaks pulled around them, moonlight, vertical, 1st-century Judea", None),
 "jesus_stands_over_sleepers": ("Jesus standing quietly over three sleeping robed men beneath an olive tree at night, looking down at them with sorrowful tenderness, moonlight, vertical, 1st-century Judea", REF_JESUS),
 "cup_moonlight": ("a plain stone cup standing on a flat rock in cold moonlight, olive branches shadowing the ground around it, night, close, vertical, ancient Judea", None),
 "jesus_praying_close": ("the face of a man in anguished prayer kneeling in an olive garden at night, eyes shut tight, brow knotted, sweat on his brow, clasped hands under his chin, moonlight rim light, close, vertical, 1st-century Judea", REF_PRAY),
 "jesus_leads_three": ("a robed man leading three companions up a moonlit path into an olive garden at night, seen from behind, gnarled trees ahead, deep blue night, wide, vertical, 1st-century Judea", None),
 "sleeping_peter_close": ("an older bearded fisherman fast asleep against an olive trunk at night, cloak wrapped tight, mouth slack, moonlight on his weathered face, close, vertical, 1st-century Judea", None),
 "kneeling_lamp_prayer": ("a robed figure kneeling in prayer beside a small clay oil lamp in a dark stone room at night, head bowed, warm lamp glow on his hands, vertical, 1st-century Judea", None),
 "same_prayer_again": ("a robed man kneeling among olive trees with his forehead bowed low toward the ground in prayer, deep night, moonlight through the branches, seen from the side, vertical, 1st-century Judea", None),
 "weak_flesh_hands": ("two rough weathered hands clasped tight and trembling against a dark woollen cloak, knuckles pale, night shadow, close, vertical, ancient Judea", None),
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
