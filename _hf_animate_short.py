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
            "CROP ONLY TO EXPRESSIVE FOCAL POINTS — the FACE, the EYES, the HANDS, and the key named "
            "object. NEVER crop to feet, a plain swath of robe or fabric folds, bare floor or pavement, "
            "a blank wall, empty background, or empty sky — those are wasted crops. Every crop must show "
            "the subject's face/hands or a meaningful named detail. "
            "CRITICAL — INVENT NOTHING: show ONLY what is already painted in this exact image. Do "
            "NOT add or generate any new hand, finger, limb, nail, wound, face, figure, halo, object, "
            "or detail that is not literally present in the still. Each crop is a plain rectangular "
            "section of the existing painting. If a tighter crop would reveal an area that is not clearly "
            "painted, do NOT invent it — stay on the full wide instead.")
_CUT_VERBS = ["CUT to a tight close-up of {}.", "CUT to a macro crop of {}.",
              "CUT to a detail of {}.", "CUT to {}."]

# anchor curation (2026-06-23): the gallery-tour is only as good as its crop
# targets. EXPRESSIVE anchors (a face, eyes, hands, a flame, a tear, a named
# object) make a punchy viral edit; GENERIC ones (robe/fabric/floor/pillar/sky/
# background) crop to nothing and make a full figure "dance" (caught on #31 #06,
# whose macros were face/hand/STONES/ROBE/PILLARS). Rank good anchors first, drop
# the wasted ones, so even a single full-figure portrait tours face->hand->full.
_GOOD_ANCHOR = ("face", "eyes", "eye", "hand", "hands", "finger", "fingertip", "tear",
                "flame", "lamp", "wound", "footprint", "chain", "box", "chest", "veil",
                "scroll", "stone", "lips", "mouth", "wrist", "feet of",
                # the human subject of the scene is always a focal point, not a wasted crop
                "woman", "child", "cowering", "kneeling", "the accused")
_WASTED_ANCHOR = ("robe", "fabric", "drapery", "linen", "pillar", "column", "floor",
                  "pavement", "background", "sky", "landscape", "horizon", "wall",
                  "shadow", "haze", "dust", "pool of light", "edge of light", "tiles")

def _curate_anchors(macros: list[str]) -> list[str]:
    good = [m for m in macros if any(g in m.lower() for g in _GOOD_ANCHOR)
            and not any(w in m.lower() for w in _WASTED_ANCHOR)]
    if good:
        return good[:3]
    # nothing expressive listed -> tour the face + hands generically rather than fabric
    return ["the subject's face", "the subject's hands"]

def viral_prompt(scene: dict) -> str:
    macros = _curate_anchors([m for m in scene.get("macro_elements", []) if m])
    cuts = ["Open on the full painting wide."]
    for i, m in enumerate(macros):
        cuts.append(_CUT_VERBS[i % len(_CUT_VERBS)].format(m))
    cuts.append("CUT back to the full wide.")
    return CUT_BASE + " ".join(cuts) + CUT_TAIL


# PUSH-IN prompt (2026-06-23): the WINNER for single full-figure subjects (a
# standing/seated person, a Christ portrait). The gallery-tour hard-cut crops
# such a frame into a foot / a swath of robe / an empty corner so the figure
# "dances" (caught on #31 scene 06). One slow continuous push-in holds the
# subject. Mode is chosen by pipeline.clip_anim_qc.choose_anim_mode.
PUSHIN_BASE = ("A still finished Baroque oil painting on flat canvas, filmed as ONE slow, steady, "
               "continuous push-in toward ")
PUSHIN_TAIL = (". The painting itself never moves, breathes, brightens or changes; only the camera "
               "slowly, smoothly zooms in, keeping the subject centred and whole the entire time. "
               "No hard cuts, no dissolves, no crop-jumps, no morphing, no subject motion, no limbs "
               "moving. INVENT NOTHING: show ONLY what is already painted in this exact image; do not "
               "add or generate any hand, finger, limb, face, halo, object or detail that is not "
               "literally present. The final frame still holds the whole subject.")

def pushin_prompt(scene: dict) -> str:
    # the dominant subject to keep centred (first macro is usually the face/centre)
    macros = [m for m in scene.get("macro_elements", []) if m]
    focus = macros[0] if macros else "the central figure"
    return (PUSHIN_BASE + f"the main subject of the painting, easing gently toward {focus}, "
            "keeping the whole figure in frame" + PUSHIN_TAIL)

def _episode_of(png: Path) -> str:
    """The owning piece folder (has narration.md / publish_meta.json), for the ledger."""
    for p in png.parents:
        if (p / "narration.md").is_file() or (p / "publish_meta.json").is_file():
            return p.name
    return png.parent.name


def hf_animate(png: Path, out: Path, prompt: str, duration: int, aspect_ratio: str = "9:16") -> bool:
    # aspect_ratio defaults to 9:16 (shorts); pass "16:9" for long-form motion-comic (MOTIONCOMIC_SPEC MC-R2)
    # STILL GATE (P0-4, 2026-07-08): never pay Kling for a production still that has no
    # PASS audit sidecar — the batch flow used to animate stills the gate never saw.
    # JITB_SKIP_STILL_GATE=1 overrides (discouraged).
    import os
    if os.getenv("JITB_SKIP_STILL_GATE", "0") in ("0", "false", "no"):
        try:
            sys.path.insert(0, str(ROOT))
            from render_lint.verify import _sidecar_verdict, is_production_png
            if is_production_png(png) and _sidecar_verdict(png) != "PASS":
                raise PermissionError(
                    f"REFUSING to animate {png.name}: no PASS audit sidecar "
                    f"(verdict={_sidecar_verdict(png)!r}). Record a PASS via render_lint "
                    f"verify --record first, or set JITB_SKIP_STILL_GATE=1 (discouraged).")
        except ImportError as e:
            print(f"   [gate] render_lint unavailable ({e}) — proceeding ungated")
    # BUDGET TEETH (2026-07-08): this is the one chokepoint every Kling clip passes
    # (batch _animate.py scripts + this CLI), so the episode ceiling is enforced and a
    # ledger row written HERE — the engine audit found the batch flow spent unmetered.
    _cost, ep = None, ""
    try:
        sys.path.insert(0, str(ROOT))
        from pipeline import cost as _cost_mod
        _cost, ep = _cost_mod, _episode_of(png)
        _cost.check_budget(ep, "short", _cost.KLING_USD_PER_CLIP)
    except SystemExit:
        raise                     # ceiling breach — refuse the spend
    except Exception as e:  # noqa - a broken ledger must not block animation
        print(f"   [cost] ledger unavailable ({e}) — proceeding unmetered")
        _cost = None
    cmd = [str(HF), "generate", "create", "kling3_0", "--start-image", str(png),
           "--prompt", prompt, "--duration", str(duration), "--mode", "pro",
           "--sound", "off", "--aspect_ratio", aspect_ratio, "--wait"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    blob = (r.stdout or "") + (r.stderr or "")
    m = re.search(r'https?://[^\s"]+\.mp4', blob)
    if not m:
        print(f"   [HF no-url] {png.name}: {blob.strip()[-200:]}")
        return False
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
    ok = out.exists() and out.stat().st_size > 0
    if ok and _cost:
        try:
            _cost.record(ep, "clip", "animate", "hf", "kling3_0", 1,
                         est_usd=_cost.KLING_USD_PER_CLIP, est_only=True, note=png.name)
        except Exception:  # noqa - never fail a finished clip on a logging error
            pass
    return ok

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
        sc = by_idx.get(idx, {})
        try:
            from pipeline.clip_anim_qc import choose_anim_mode
            mode = choose_anim_mode(sc)
        except Exception:
            mode = "gallery"
        pr = pushin_prompt(sc) if mode == "pushin" else viral_prompt(sc)
        print(f"-- scene {idx:>2} {png.stem[3:]:34} [{role.get(idx,'build')}] mode={mode}")
        ok = hf_animate(png, out, pr, a.duration)
        if not ok:
            print(f"   -> HF blocked/failed; ffmpeg fallback (NSFW-only path)")
            ffmpeg_fallback(png, out)
        print(f"   SAVED {out}")
    print("== DONE ==")

if __name__ == "__main__":
    main()
