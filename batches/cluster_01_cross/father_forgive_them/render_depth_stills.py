#!/usr/bin/env python
"""Render the NEW context/depth stills of the v2 scene plan on BytePlus Seedream 4.5.

These are the scenes with reuse=="new" (crowd, David's Psalm-22 scroll, executioner, torn veil).
They carry NO Christ figure, so they render WITHOUT the Christ face ref (christ_ref==false) — this
is the face-bleed fix the craft red-team flagged (a Christ ref would bleed his face onto the
executioner / crowd). Output lands beside the reshoot stills so the comic can find all 13.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/render_depth_stills.py            # list
  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/render_depth_stills.py --render   # spend ~$0.15
  ...  --render --only crowd_mocking
"""
import argparse, importlib.util, json, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN = HERE / "visual" / "scene_plan_v2.json"
OUT = HERE / "visual" / "_byteplus" / "reshoot"; OUT.mkdir(parents=True, exist_ok=True)
MODEL = "seedream-4-5-251128"
SIZE = "1440x2560"
BASE = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"

bp_spec = importlib.util.spec_from_file_location("bp", HERE / "byteplus_seedream.py")
bp = importlib.util.module_from_spec(bp_spec); bp_spec.loader.exec_module(bp)
rl_spec = importlib.util.spec_from_file_location("rll", HERE.parents[2] / "render_lint" / "lint.py")
rl = importlib.util.module_from_spec(rl_spec); rl_spec.loader.exec_module(rl)


def call(prompt: str, dest: Path) -> str:
    if dest.exists() and dest.stat().st_size > 0:
        return "skip"
    body = {"model": MODEL, "prompt": prompt + bp.STYLE + bp.ONE, "size": SIZE,
            "response_format": "url", "watermark": False}   # NO ref image -> no face-bleed
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = {s.strip() for s in a.only.split(",") if s.strip()}
    scenes = json.loads(PLAN.read_text(encoding="utf-8"))["final_plan"]["scenes"]
    new = [s for s in scenes if s.get("reuse") == "new" and not s.get("christ_ref", False)]
    for s in new:
        slug = s["slug"]
        if only and slug not in only:
            continue
        print(f"\n--- #{s['index']} {slug} ({s['subject_type']}) ---")
        rl.report(s["prompt_seed"], stage="still", context=slug)   # pre-flight lint
        if a.render:
            print(f"  -> {call(s['prompt_seed'], OUT / f'{slug}.png')}", flush=True)
    if not a.render:
        print(f"\n[list/lint only] {len(new)} new depth stills, NO Christ ref. Add --render (~$0.15).")


if __name__ == "__main__":
    main()
