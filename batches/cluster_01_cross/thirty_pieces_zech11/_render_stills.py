#!/usr/bin/env python
"""Thirty Pieces (Zech 11) — 8 new 9:16 stills via BytePlus Seedream (lean prompts, ~$0.40).
Lint-gated ($0) before any call. Idempotent: skips existing PNGs unless --force.
JUDAS identity locked via ref_library; coins via THIRTY_PIECES_SILVER ref."""
import argparse, importlib.util, json, sys, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
FFT = HERE.parent / "father_forgive_them"
ROOT = HERE.parents[2]
OUT = HERE / "visual"
MODEL = "seedream-4-5-251128"; SIZE = "1440x2560"
BASE = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"
REF_JUDAS = ROOT / "ref_library" / "characters" / "JUDAS.png"
REF_COINS = ROOT / "ref_library" / "objects" / "THIRTY_PIECES_SILVER.png"

bp_spec = importlib.util.spec_from_file_location("bp", FFT / "byteplus_seedream.py")
bp = importlib.util.module_from_spec(bp_spec); bp_spec.loader.exec_module(bp)
sys.path.insert(0, str(ROOT))
from render_lint import lint as _lint

JOBS = {
 "thirty_coins_scatter": ("silver coins scattering and bouncing across a worn stone temple floor, low close angle, torchlight glinting on the metal, vertical, 1st-century Judea", REF_COINS),
 "coin_on_scroll": ("a single silver coin resting on an unrolled ancient scroll of faded illegible marks, warm oil-lamp light, close, vertical, ancient Judea", None),
 "weighing_scales_silver": ("aged hands steadying a bronze balance scale heavy with silver pieces, dim stone chamber, torchlight, vertical, 1st-century Judea", REF_COINS),
 "potter_at_wheel": ("an old potter's clay-covered hands shaping a vessel on a spinning stone wheel, dusty workshop shafts of light, close, vertical, ancient Judea", None),
 "judas_bag_priests": ("a weary bearded man in an olive robe clutching a small cloth money bag to his chest, head bowed, richly robed priests watching from the shadows behind him, torchlit stone chamber, vertical, 1st-century Judea", REF_JUDAS),
 "judas_casting_coins": ("a gaunt man in an olive robe hurling a handful of silver coins across a grand temple hall, the coins caught in mid-air, robed priests recoiling, vertical, 1st-century Judea", REF_JUDAS),
 "zechariah_casting": ("an aged prophet in a simple robe flinging a handful of silver coins across a torchlit temple court toward a potter's stall, the coins caught mid-air, night, vertical, ancient Judea", None),
 "potters_field": ("a bleak empty clay field scattered with broken pottery shards under a heavy grey sky, low ridge on the horizon, wide, vertical, ancient Judea", None),
 "silver_and_blood": ("worn silver coins lying flat, scattered wide across pale stone slabs, a dark red stream running across the stone between the coins, hard side light, low close angle, vertical", REF_COINS),
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
    print("\n$0 dry-run. --render to spend (~$0.40)."); sys.exit(0)

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
