"""Animate a short's scenes via HF Kling 3.0 with VIRAL MOTION prompts (the winner,
2026-06-15). Per the higgsfield-generate skill: --start-image + MOTION-only prompt,
concise, positive phrasing, one-shot --wait. Subject frozen, only the camera moves.

- Writing scenes (--skip) are NOT animated (see memory feedback-never-animate-writing).
- If HF NSFW-blocks a clip (no mp4 URL), auto-fall-back to deterministic ffmpeg crop-cuts
  (memory feedback-shorts-generative-not-ffmpeg: ffmpeg is the NSFW-only exception).
- Old direct-Kling clips are moved to visual/nbp/_old_kling/ (not deleted).

Usage:
  python _hf_animate_short.py 06_The_Ends_Of_The_Earth --skip 2,6 --duration 5
  python _hf_animate_short.py 06_The_Ends_Of_The_Earth --only 1,4 --duration 5   # subset
"""
import argparse, json, re, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).parent
HF = Path.home() / "bin" / "hf.exe"
SHORTS = ROOT / "longform" / "02_Psalm_22_Song_From_The_Cross" / "v1" / "shorts"

# HARD-CUT CUT-PLAN prompt (2026-06-15, the WINNER): drives Kling pro to JUMP-CUT between
# crops of ONE frozen painting (the viral edit), using each scene's macro_elements as the
# crop targets. Validated on #06 cross+tomb: 5 hard cuts in 5s, frozen between, faithful crops.
# A plain "push-in/zoom" prompt was too basic (user: regression); ffmpeg jump-cuts were jittery
# + lifeless; Kling pro + this prompt is smooth with subtle life. See memory
# feedback-shorts-generative-not-ffmpeg. ffmpeg is fallback/NSFW-only.
CUT_BASE = ("A still finished Baroque oil painting on flat canvas, filmed as a HARD-CUT video "
            "edit — like an editor jump-cutting between different crops of ONE frozen painting. "
            "The painting itself never moves, breathes, brightens or changes; only the FRAMING "
            "jumps. Sequence of HARD CUTS (instant jumps to a new static crop, NOT a smooth zoom, "
            "no dissolves): ")
CUT_TAIL = (" Between cuts the image holds perfectly still. No subject motion, no limbs moving, "
            "no morphing, no smooth zoom, no dissolve — every crop is the same frozen painting. "
            "CRITICAL — INVENT NOTHING: show ONLY what is already painted in this exact image. Do "
            "NOT add or generate any new hand, finger, limb, nail, wound, face, figure, halo, object, "
            "or detail that is not literally present in the still. Each crop is a plain rectangular "
            "section of the existing painting — nothing outside the original is created. If a tighter "
            "crop would reveal an area that is not clearly painted (e.g. a hand or edge), do NOT "
            "invent it — stay on the full wide instead.")
_CUT_VERBS = ["CUT to a tight close-up of {}.", "CUT to a macro crop of {}.",
              "CUT to a detail of {}.", "CUT to {}."]

def viral_prompt(scene: dict) -> str:
    macros = [m for m in scene.get("macro_elements", []) if m][:4]
    cuts = ["Open on the full painting wide."]
    for i, m in enumerate(macros):
        cuts.append(_CUT_VERBS[i % len(_CUT_VERBS)].format(m))
    cuts.append("CUT back to the full wide.")
    return CUT_BASE + " ".join(cuts) + CUT_TAIL

def hf_animate(png: Path, out: Path, prompt: str, duration: int) -> bool:
    cmd = [str(HF), "generate", "create", "kling3_0", "--start-image", str(png),
           "--prompt", prompt, "--duration", str(duration), "--mode", "pro",
           "--sound", "off", "--aspect_ratio", "9:16", "--wait"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    blob = (r.stdout or "") + (r.stderr or "")
    m = re.search(r'https?://[^\s"]+\.mp4', blob)
    if not m:
        print(f"   [HF no-url] {png.name}: {blob.strip()[-200:]}")
        return False
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 0

def ffmpeg_fallback(png: Path, out: Path):
    sys.path.insert(0, str(ROOT))
    from _ffmpeg_viralcut_test import build
    build(png, out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("short")
    ap.add_argument("--skip", default="", help="comma scene indices NOT to animate (writing)")
    ap.add_argument("--only", default="", help="comma scene indices to animate (subset)")
    ap.add_argument("--duration", type=int, default=5)
    a = ap.parse_args()
    short_dir = Path(a.short)
    if not short_dir.is_dir():
        short_dir = SHORTS / a.short            # bare name -> Psalm-22 shorts dir (back-compat)
    nbp = short_dir / "visual" / "nbp"
    plan = json.load(open(short_dir / "visual" / "scene_plan.json", encoding="utf-8"))
    scenes = plan["plan"]["scenes"] if "plan" in plan else plan["scenes"]
    by_idx = {s["index"]: s for s in scenes}
    role = {s["index"]: s.get("viral_role", "") for s in scenes}
    skip = {int(x) for x in a.skip.split(",") if x.strip()}
    only = {int(x) for x in a.only.split(",") if x.strip()}
    bak = nbp / "_old_kling"; bak.mkdir(exist_ok=True)

    pngs = sorted(nbp.glob("[0-9][0-9]_*.png"))
    todo = []
    for png in pngs:
        idx = int(png.stem[:2])
        if idx in skip: continue
        if only and idx not in only: continue
        todo.append((idx, png))
    print(f"== {a.short}: animating {len(todo)} scenes via HF Kling viral "
          f"(skip writing {sorted(skip) or '-'}), {a.duration}s ==")
    for idx, png in todo:
        out = png.with_suffix(".mp4")
        if out.exists():
            old = bak / out.name
            if not old.exists(): out.replace(old)
            else: out.unlink()
        pr = viral_prompt(by_idx.get(idx, {}))
        print(f"-- scene {idx:>2} {png.stem[3:]:34} [{role.get(idx,'build')}]")
        ok = hf_animate(png, out, pr, a.duration)
        if not ok:
            print(f"   -> HF blocked/failed; ffmpeg fallback (NSFW-only path)")
            ffmpeg_fallback(png, out)
        print(f"   SAVED {out}")
    print("== DONE ==")

if __name__ == "__main__":
    main()
