#!/usr/bin/env python
"""Pierced (Zech 12:10) — 7 new 9:16 stills via BytePlus Seedream (lean prompts, ~$0.35).
Lint-gated ($0) before any call. Idempotent: skips existing PNGs unless --force."""
import argparse, importlib.util, json, sys, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
FFT = HERE.parent / "father_forgive_them"
ROOT = HERE.parents[2]
OUT = HERE / "visual"
MODEL = "seedream-4-5-251128"; SIZE = "1440x2560"
BASE = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"
REF_CRUX = FFT / "visual" / "_byteplus" / "nail_wide_45.png"

bp_spec = importlib.util.spec_from_file_location("bp", FFT / "byteplus_seedream.py")
bp = importlib.util.module_from_spec(bp_spec); bp_spec.loader.exec_module(bp)
sys.path.insert(0, str(ROOT))
from render_lint import lint as _lint

JOBS = {
 "spear_thrust_up": ("a Roman soldier seen from behind and below, thrusting a long spear steeply upward toward the crucified figure high against a dark storm sky, the moment of Zechariah's word arriving, vertical, 1st-century Judea", REF_CRUX),
 "zechariah_night_scroll": ("an aged prophet standing on a flat rooftop at night, face lifted to a sky of stars, a rolled scroll held loosely at his side, moonlit ancient Judean city below, vertical, 1st-millennium-BC", None),
 "mourners_only_son": ("a father and mother collapsed together in grief beside a shrouded form on a low bier, torchlit stone courtyard at night, their faces buried in each other's shoulders, vertical, ancient Judea", None),
 "john_watching": ("a young disciple at the foot of the cross flinching as he watches upward, one hand gripping the cloak at his chest, hard storm light on his face, vertical, 1st-century", None),
 "blood_water_wood": ("a macro of the base of a rough wooden cross, a thin stream of water and dark blood running down the grain and pooling on the stone, storm light, vertical, 1st-century", None),
 "grace_poured_sky": ("warm golden light pouring down like a waterfall from a single break in heavy dark clouds onto the small stone city below, the pouring is the subject, vertical, ancient Judea", None),
 "look_up_faces": ("three different upturned 1st-century faces close together in half-light, eyes lifted toward a warm light above, tears catching the light, hope breaking on the faces, vertical", None),
}

ap = argparse.ArgumentParser(); ap.add_argument("--render", action="store_true"); ap.add_argument("--force", action="store_true")
a = ap.parse_args()
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
    print("\n$0 dry-run. --render to spend (~$0.35)."); sys.exit(0)

def call(prompt, dest, ref):
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
    return "ok"

for slug, (prompt, ref) in JOBS.items():
    dest = OUT / f"{slug}.png"
    if dest.exists() and not a.force:
        print(f"[skip] {slug}"); continue
    print(f"{slug:24} -> {call(prompt, dest, ref)}")
print("DONE")
