#!/usr/bin/env python
"""Animate the 13 v2 stills via HF Kling 3.0 pro (9:16, 5s) — one gentle camera move each.

INKED motion prompt (invent nothing / camera-only) so Kling keeps the flat ink instead of repainting
it. Reads scene_plan_v2.json for each still's slug + motion + concept. Clips -> visual/_byteplus/clips/.
Idempotent (existing .mp4 skipped). Test-gate ONE clip before the full batch.

  ...\\python.exe batches/cluster_01_cross/father_forgive_them/animate_v2.py --lint-only        # free
  ...\\python.exe batches/cluster_01_cross/father_forgive_them/animate_v2.py --only nail_through_hand   # ~$0.65 test
  ...\\python.exe batches/cluster_01_cross/father_forgive_them/animate_v2.py --all               # ~$8.50
"""
import argparse, importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from _hf_animate_short import hf_animate

_ls = importlib.util.spec_from_file_location("rl_lint", ROOT / "render_lint" / "lint.py")
rl = importlib.util.module_from_spec(_ls); _ls.loader.exec_module(rl)
g_spec = importlib.util.spec_from_file_location("g", HERE / "build_gallery_v2.py")
g = importlib.util.module_from_spec(g_spec); g_spec.loader.exec_module(g)

BP = HERE / "visual" / "_byteplus"
CLIPS = BP / "clips"; CLIPS.mkdir(parents=True, exist_ok=True)
PLAN = json.loads((HERE / "visual" / "scene_plan_v2.json").read_text(encoding="utf-8"))["final_plan"]

INK_BASE = ("A finished inked graphic-novel comic panel — flat printed art with bold black ink "
            "outlines, cel-flat color and cross-hatching. Animate it as {move}. The drawing itself "
            "never moves, redraws, repaints, breathes or changes; the ink lines and flat colors stay "
            "exactly as printed; only the camera moves. No hard cuts, no dissolves, no morphing, no "
            "subject motion, no limbs moving, no new lines drawn. INVENT NOTHING: show ONLY what is "
            "already inked in this exact panel; do not add or generate any hand, finger, limb, face, "
            "halo, nail, wound, object or detail that is not literally drawn. Keep the subject whole in frame.")


def _move(motion, focus):
    return {
        "pushin":   f"ONE slow, steady, continuous push-in toward {focus}",
        "pullback": f"ONE slow, steady, continuous pull-back that starts on {focus} and reveals the whole panel",
        "dolly":    f"ONE slow, steady, continuous dolly forward toward {focus}",
        "static":   f"an almost-still hold on {focus}, with only the faintest slow settling of light",
        "hold":     f"an almost-still hold on {focus}, with only the faintest slow settling of light",
    }.get(motion, f"ONE slow, steady, continuous push-in toward {focus}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=""); ap.add_argument("--all", action="store_true")
    ap.add_argument("--lint-only", action="store_true"); ap.add_argument("--duration", type=int, default=5)
    a = ap.parse_args()
    only = {x.strip() for x in a.only.split(",") if x.strip()}
    if not (only or a.all or a.lint_only):
        ap.error("pass --only <slug>, --all, or --lint-only")
    scenes = [s for s in PLAN["scenes"] if a.lint_only or a.all or s["slug"] in only]
    print(f"== animate {len(scenes)} inked panels · HF Kling pro 9:16 {a.duration}s {'(LINT)' if a.lint_only else ''} ==")
    for s in scenes:
        slug = s["slug"]; focus = s["concept"].rstrip(".")
        prompt = INK_BASE.format(move=_move(s.get("motion"), focus))
        findings = rl.lint(prompt, stage="animation")
        print(f"-- {slug:28} [{s.get('motion')}] {'clean' if not findings else str(len(findings))+' lint'}")
        if a.lint_only:
            continue
        still = BP / g.IMG[slug]
        out = CLIPS / f"{slug}.mp4"
        if out.exists() and out.stat().st_size > 0:
            print(f"     [skip] {out.name}"); continue
        ok = hf_animate(still, out, prompt, a.duration)
        print(f"     SAVED {out}" if ok else f"     [FAILED] {slug} (NSFW/credit?)")
    print("== DONE ==")


if __name__ == "__main__":
    main()
