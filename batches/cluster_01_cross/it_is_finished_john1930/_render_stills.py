#!/usr/bin/env python
"""It Is Finished (John 19:30) ??? 7 new 9:16 stills via BytePlus (~$0.35). Lint-gated. Idempotent.
jesus_prays_night + first_day_morning are cluster-shared (watch/hands reuse them)."""
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
from render_lint import lint as _lint

JOBS = {
 "eden_garden_finished": ("an empty pristine garden valley at golden dawn, rivers threading between flowering trees toward distant mountains, landscape only, vast and still, wide, vertical", None),
 "seventh_day_light": ("warm golden evening light resting over rolling young hills and still water, a great calm, no figures, wide, vertical", None),
 "jesus_prays_night": ("Jesus kneeling in prayer among gnarled olive trees at night, face lifted to the moonlit sky, hands clasped on a flat rock, deep blue night, vertical, 1st-century Judea", REF_JESUS),
 "vinegar_sponge_reed": ("a rough dark sea sponge bound to the tip of a long thin reed, lifted up toward a crucified figure high above, seen from below along the reed, storm light, vertical, 1st-century Judea", REF_JESUS),
 "bowed_head_finished": ("the thorn-crowned crucified Christ with head bowed in deep stillness, eyes closed, at peace, storm clouds parting behind, close, vertical, 1st-century Judea", REF_JESUS),
 "tomb_stone_sealed": ("a great round stone sealing a rock-cut tomb at dusk, the hillside quiet, two small robed figures walking away down the path, vertical, 1st-century Judea", None),
 "first_day_morning": ("dawn light bursting from the open rock-cut entrance of a garden tomb, the great round stone rolled to the side, warm gold spilling across a stone path, olive trees, vertical, 1st-century Judea", None),
 "hands_shaping_light": ("two strong open hands cupping a swirling sphere of warm golden light against deep starry darkness, rays between the fingers, close, vertical", None),
 "carpenter_bench_rest": ("a carpenter's wooden workbench with a finished three-legged wooden stool standing on it, tools laid down neatly, wood shavings, warm evening light through a small window, quiet stone workshop, vertical, 1st-century Judea", None),
 "man_lifting_face_dawn": ("a weathered man lifting his face upward into warm dawn light with eyes closed and peace on his face, dark robe, close, vertical, 1st-century Judea", None),
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
    if only and slug not in only:
        continue
    dest = OUT / f"{slug}.png"
    if dest.exists() and not a.force:
        print(f"[skip] {slug}"); continue
    print(f"{slug:24} -> {call(prompt, dest, ref)}")
print("DONE")

