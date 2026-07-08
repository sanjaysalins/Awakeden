#!/usr/bin/env python
"""The Forsaken Cry (Ps 22:1 / Matt 27:46) — 1 new 9:16 still via BytePlus (~$0.05). Lint-gated. Idempotent."""
import argparse, importlib.util, json, sys, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
FFT = HERE.parent / "father_forgive_them"
ROOT = HERE.parents[2]
OUT = HERE / "visual"
MODEL = "seedream-4-5-251128"; SIZE = "1440x2560"
BASE = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"

bp_spec = importlib.util.spec_from_file_location("bp", FFT / "byteplus_seedream.py")
bp = importlib.util.module_from_spec(bp_spec); bp_spec.loader.exec_module(bp)
sys.path.insert(0, str(ROOT))
from render_lint import lint as _lint, guard_prompt, arm_audit

JOBS = {
 "ninth_hour_darkness": ("three distant crosses on a hilltop under a sky gone almost black, a pale dim sun swallowed by heavy darkness, the land in shadow, wide, vertical, 1st-century Judea", None),
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
    print("\n$0 dry-run. --render to spend (~$0.05)."); sys.exit(0)

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
