#!/usr/bin/env python
"""Render the INKED 16:9 gravitas-test SLICE for the Psalm-22 long pilot (3 scenes).

Reuses the LOCKED short pilot's BytePlus Seedream 4.5 client (INV-15, no re-implementation),
at 16:9 (2560x1440). christ_ref scenes lock to the short pilot's risen-face ref; the wound
detail renders with no ref. Idempotent. List-only until --render (ASK-before-spend, INV-20).

  .venv\\Scripts\\python.exe longform/02_Psalm_22_Song_From_The_Cross/pilot_inked_slice.py            # list + cost
  .venv\\Scripts\\python.exe longform/02_Psalm_22_Song_From_The_Cross/pilot_inked_slice.py --render   # ~$0.12 (3 stills)
"""
import argparse, importlib.util, json, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PLAN = HERE / "v1" / "visual_16x9_inked" / "scene_plan_slice.json"
OUT = HERE / "v1" / "visual_16x9_inked"; OUT.mkdir(parents=True, exist_ok=True)
PILOT = ROOT / "batches" / "cluster_01_cross" / "father_forgive_them"
REF_RISEN = PILOT / "visual" / "_byteplus" / "bakeoff" / "_ref_small.png"
MODEL = "seedream-4-5-251128"
SIZE = "2560x1440"   # 16:9 landscape (>= 3,686,400 px)
BASE = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"

bp_spec = importlib.util.spec_from_file_location("bp", PILOT / "byteplus_seedream.py")
bp = importlib.util.module_from_spec(bp_spec); bp_spec.loader.exec_module(bp)

REFS = {"risen_face": REF_RISEN}


def call(prompt, dest, ref):
    if dest.exists() and dest.stat().st_size > 0:
        return "skip"
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
    scenes = json.loads(PLAN.read_text(encoding="utf-8"))["scenes"]
    if not REF_RISEN.exists():
        print(f"  ! risen ref missing: {REF_RISEN}")
    for s in scenes:
        slug = s["slug"]
        if only and slug not in only:
            continue
        ref = REFS.get(s.get("ref")) if s.get("christ_ref") else None
        print(f"\n#{s['index']:2} {slug:20} [{s['subject_type']}] ref={s.get('ref') or 'NONE'}")
        print(f"   {s['prompt_seed'][:160]}...")
        if a.render:
            print(f"   -> {call(s['prompt_seed'], OUT / f'{slug}.png', ref)}", flush=True)
    if not a.render:
        print(f"\n[list only] {len(scenes)} inked 16:9 stills @ {SIZE}. Add --render (~$0.12). "
              f"Then Kling-16:9 animate (~$2) for the A/B vs the Baroque clips.")


if __name__ == "__main__":
    main()
