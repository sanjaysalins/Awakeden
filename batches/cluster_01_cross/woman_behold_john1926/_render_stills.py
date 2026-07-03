#!/usr/bin/env python
"""Woman Behold Thy Son (John 19:25-27) — 6 new 9:16 stills via BytePlus (~$0.30).
Lint-gated ($0). Idempotent. Jesus identity via the pierced crucified ref."""
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
from render_lint import lint as _lint

JOBS = {
 "simeon_baby_temple": ("an aged man with a white beard lifting a swaddled infant in a shaft of temple light, a young mother in a veil watching close, stone columns, vertical, ancient Judea", None),
 "mary_infant_shadow": ("a young veiled mother clutching a swaddled infant to her chest, a long thin cold shadow falling diagonally across her robe, dark temple stone behind, vertical, ancient Judea", None),
 "mary_at_cross": ("a veiled grieving woman looking up from the foot of a tall cross where a crucified figure hangs high above her, seen from behind her shoulder, storm light, vertical, 1st-century Judea", REF_JESUS_CROSS),
 "jesus_looks_down": ("the thorn-crowned crucified Christ looking downward with steady compassion from the cross, storm sky behind, seen from below, close, vertical, 1st-century Judea", REF_JESUS_CROSS),
 "mary_and_john": ("a young bearded disciple wrapping his arm around a veiled grieving woman's shoulders, both looking up, at the foot of a cross, storm light, vertical, 1st-century Judea", None),
 "john_leads_home": ("a young disciple gently leading a veiled woman along a dusk road toward the gate of a walled town, a bare empty hill far behind them, warm evening light, wide, vertical, 1st-century Judea", None),
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
    if only and slug not in only:
        continue
    dest = OUT / f"{slug}.png"
    if dest.exists() and not a.force:
        print(f"[skip] {slug}"); continue
    print(f"{slug:24} -> {call(prompt, dest, ref)}")
print("DONE")
