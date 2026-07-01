#!/usr/bin/env python
"""Animate the 12 inked motion-comic panels via HF Kling 3.0 pro (9:16, 5s).

Why a piece-local driver (not the root _hf_animate_short.py):
  1. STYLE — these are INKED graphic-novel panels, not Baroque oil. The root driver's
     prompt says "Baroque oil painting on flat canvas", which makes Kling REPAINT the ink.
     Here the motion prompt is honest about the medium so the ink stays flat + un-redrawn.
  2. FILENAMES — lettered stems (01b/06c...) collide in the root driver's int(stem[:2]) index.
     This reads visual/scene_plan.json, which maps each scene to its exact png by the `png` field.
  3. MOTION — a motion comic wants ONE gentle per-panel move (push/pull/hold/dolly) that leaves
     room for the PIL furniture composited on top later, not the busy 5-hard-cut gallery tour.

Reuses the proven HF call (hf_animate) from the root shorts animator. Idempotent: an existing
.mp4 is moved to nbp/_old_kling/ and re-rendered; run --only for the test gate first.

  # TEST GATE (2 panels, ~$3.75) — a push-in figure + a macro:
  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/animate_stills.py --only 4,7
  # BATCH the rest (~$18.75):
  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/animate_stills.py --all
  # dry-run: lint every motion prompt, spend nothing:
  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/animate_stills.py --lint-only
"""
import argparse, importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from _hf_animate_short import hf_animate          # reuse the proven HF Kling call

# render-quality loop: lint each motion prompt before spending
_ls = importlib.util.spec_from_file_location("rl_lint", ROOT / "render_lint" / "lint.py")
rl = importlib.util.module_from_spec(_ls); _ls.loader.exec_module(rl)

NBP = HERE / "visual" / "nbp"
PLAN = json.load(open(HERE / "visual" / "scene_plan.json", encoding="utf-8"))["plan"]

# INKED motion prompt — mirrors the proven "invent nothing / frozen image" cut-discipline of the
# root shorts prompt, but declares the medium as a printed inked comic panel so Kling keeps the ink
# flat instead of repainting it into oil. ONE continuous camera move (motion-comic), no hard cuts.
INK_BASE = ("A finished inked graphic-novel comic panel — flat printed art with bold black ink "
            "outlines, cel-flat color and cross-hatching. Animate it as {move}. The drawing itself "
            "never moves, redraws, repaints, breathes or changes; the ink lines and flat colors stay "
            "exactly as printed; only the camera moves. No hard cuts, no dissolves, no morphing, no "
            "subject motion, no limbs moving, no new lines drawn. INVENT NOTHING: show ONLY what is "
            "already inked in this exact panel; do not add or generate any hand, finger, limb, face, "
            "halo, nail, wound, object or detail that is not literally drawn. Keep the subject whole in frame.")

def _move(scene: dict) -> str:
    f = scene["focus"]
    m = scene.get("motion", "pushin")
    return {
        "pushin":  f"ONE slow, steady, continuous push-in toward {f}",
        "pullback": f"ONE slow, steady, continuous pull-back that starts on {f} and reveals the whole panel",
        "dolly":   f"ONE slow, steady, continuous dolly forward toward {f}",
        "hold":    f"an almost-still hold on {f}, with only the faintest slow settling of light",
    }.get(m, f"ONE slow, steady, continuous push-in toward {f}")

def ink_prompt(scene: dict) -> str:
    return INK_BASE.format(move=_move(scene))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="comma scene indices to animate (test gate)")
    ap.add_argument("--all", action="store_true", help="animate every scene")
    ap.add_argument("--lint-only", action="store_true", help="lint prompts, spend nothing")
    ap.add_argument("--duration", type=int, default=5)
    a = ap.parse_args()
    only = {int(x) for x in a.only.split(",") if x.strip()}
    if not (only or a.all or a.lint_only):
        ap.error("pass --only N,M (test gate), --all (batch), or --lint-only")

    bak = NBP / "_old_kling"; bak.mkdir(exist_ok=True)
    scenes = [s for s in PLAN["scenes"] if a.lint_only or a.all or s["index"] in only]
    print(f"== animate {len(scenes)} inked panels via HF Kling pro 9:16 {a.duration}s "
          f"{'(LINT ONLY)' if a.lint_only else ''} ==")
    for s in scenes:
        prompt = ink_prompt(s)
        findings = rl.lint(prompt, stage="animation")
        flag = f"  ⚠ {len(findings)} lint" if findings else "  ✓ clean"
        print(f"-- scene {s['index']:>2} {s['png']:26} [{s.get('motion')}]{flag}")
        for fi in findings:
            print(f"     • [{fi['severity']}] {fi['id']}: {fi['message'][:80]}")
        if a.lint_only:
            continue
        png = NBP / f"{s['png']}.png"
        if not png.exists():
            print(f"     [skip-missing] {png.name}"); continue
        out = png.with_suffix(".mp4")
        if out.exists():
            old = bak / out.name
            out.replace(old) if not old.exists() else out.unlink()
        ok = hf_animate(png, out, prompt, a.duration)
        print(f"     SAVED {out}" if ok else f"     [FAILED] {png.name} — no mp4 (NSFW/credit?)")
    print("== DONE ==")


if __name__ == "__main__":
    main()
