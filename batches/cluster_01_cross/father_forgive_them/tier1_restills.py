#!/usr/bin/env python
"""Tier-1 review fixes: re-render 2 stills + 1 NEW epic wide on BytePlus Seedream 4.5.

  intercession  -> risen wound now a HEALED FLAT SCAR (matches the beat-13 hero; kills the
                   black-hole vs red-slash continuity break the art-director flagged). Risen face ref.
  golgotha_wide -> a NEW cinematic-epic wide (three crosses, dwarfing scale, small 'us' at the foot)
                   to REBUILD beat 9 — replaces the 100%-recycled 4-up quad. No Christ ref.
(The Psalm-22 scroll is re-rendered via render_depth_stills.py from its updated plan prompt_seed.)

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/tier1_restills.py           # list
  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/tier1_restills.py --render   # ~$0.10
"""
import argparse, importlib.util, json, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN = json.loads((HERE / "visual" / "scene_plan_v2.json").read_text(encoding="utf-8"))["final_plan"]["scenes"]
OUT = HERE / "visual" / "_byteplus" / "reshoot"; OUT.mkdir(parents=True, exist_ok=True)
REF_RISEN = HERE / "visual" / "_byteplus" / "bakeoff" / "_ref_small.png"
MODEL = "seedream-4-5-251128"; SIZE = "1440x2560"
BASE = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"

bp_spec = importlib.util.spec_from_file_location("bp", HERE / "byteplus_seedream.py")
bp = importlib.util.module_from_spec(bp_spec); bp_spec.loader.exec_module(bp)

INTERCESSION = next(s["prompt_seed"] for s in PLAN if s["slug"] == "risen_interceding_christ")
GOLGOTHA_WIDE = (
    "inked biblical graphic-novel, a vast cinematic WIDE of Golgotha hill at the ninth hour: THREE tall "
    "rough wooden crosses silhouetted on a bare rocky summit against a vast bruised storm-dark sky, dwarfing "
    "scale, the hill falling away below; at the very foot, tiny and small against the towering crosses, a "
    "scattered huddle of ordinary bowed onlookers in coarse earth-toned robes seen from behind (US, the "
    "watching sinners), their faces unseen; a single pale shaft of light breaking the black clouds onto the "
    "central cross. Bold black ink, deep cel-flat shadow, muted earth tones, epic, reverent, awe, vertical, "
    "the crowd kept small and featureless so the crosses and the sky dominate, 1st-century Judea")

JOBS = [
    ("risen_interceding_christ", INTERCESSION, REF_RISEN),   # matched wound, risen ref
    ("golgotha_hill_wide",       GOLGOTHA_WIDE, None),        # NEW epic wide, no ref
]


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
        return f"HTTP {e.code}: {e.read().decode()[:300]}"
    url = resp.get("data", [{}])[0].get("url")
    if not url:
        return "no-url: " + json.dumps(resp)[:300]
    with urllib.request.urlopen(url, timeout=240) as im:
        dest.write_bytes(im.read())
    return "ok"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--render", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = {s.strip() for s in a.only.split(",") if s.strip()}
    for slug, prompt, ref in JOBS:
        if only and slug not in only:
            continue
        print(f"\n--- {slug} (ref={ref.name if ref else 'NONE'}) ---\n  {prompt[:150]}...")
        if a.render:
            print(f"  -> {call(prompt, OUT / f'{slug}.png', ref)}", flush=True)
    if not a.render:
        print("\n[list only] add --render (~$0.10)")


if __name__ == "__main__":
    main()
