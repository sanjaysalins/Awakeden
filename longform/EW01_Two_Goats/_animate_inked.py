"""Tiered animation for the EW01 Two Goats inked rebuild (2026-07-21).

Each of the 25 stills -> one 16:9 frozen-tableau clip. Tier per the locked
comic-grid cost rule (memory comic-grid-cost-tiered-animation):
  - Kling 3.0 pro (7.5cr, ~$1.13) for MULTI-FIGURE / crowd / complex scenes,
    where cheaper i2v invents motion (the 2026-07-17 bake-off finding).
  - Seedance 1.5 pro (4.8cr, ~$0.72) for calm single-figure tableaux.
Prompts are motion-only, camera + living-light, INVENT NOTHING (the proven
Bronze Serpent `_animate_hero_clips.py` FROZEN pattern + adhoc/SKILL_locked.md).

Budget teeth: this is the ink MIGRATION, a deliberate re-do the user approved at
~$35 (ceiling $40). The episode's lifetime ledger also holds the ARCHIVED OIL
production (~$102), so the global 'long' cap would false-trip; instead we gate on
migration spend only = EW01 rows since 2026-07-21. Refuse a clip if it would push
the migration total past MIGRATION_CEILING (override with --override).

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_animate_inked.py --only 1,18   # test-gate pair
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_animate_inked.py                # the rest
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_animate_inked.py --dry-run      # preflight only
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
from pipeline.video_render import _hf_duration

HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked"
CLIPS = OUT / "clips"
SLUG = "EW01_Two_Goats"
HF = str(config.HF_CLI_PATH)

MIGRATION_START = "2026-07-21"
MIGRATION_CEILING = 40.0
TARGET_DUR = 5

# Multi-figure / crowd / complex scenes -> Kling; everything else -> Seedance.
# 21 added after clip-QC (2026-07-21): its mid-stride still made Seedance WALK the
# figure (invented locomotion); Kling holds a frozen mid-action pose far better.
KLING_SCENES = {6, 11, 13, 14, 18, 20, 21, 24}

FROZEN = ("Every figure stays perfectly frozen the entire time -- no limbs move, no heads "
          "turn, no faces change, no morphing, and no new figures, hands or objects appear. "
          "INVENT NOTHING: show only what is already drawn in this exact image. ")
BASE = ("A still finished inked graphic-novel illustration on flat canvas, 16:9, filmed as "
        "{move}. " + FROZEN + "Only the light and the air are alive: {living}.")

# move + living-light per scene id (motion-only; nothing in the scene itself moves)
PUSH = "ONE slow, steady push-in toward the centre of the frame"
WIDE = "ONE slow, gentle push-in across the scene"
HERO = "ONE very slow, gentle push-in toward Christ's face and open hand"

MOTION = {
    1:  (WIDE, "dust motes drift in a shaft of temple light, faint incense smoke rises, robe hems stir almost imperceptibly"),
    2:  (PUSH, "a single shaft of light glints on the gold, fine dust drifts, the folded linen edge stirs faintly"),
    3:  (PUSH, "dust drifts in the corridor light, the plain linen robe stirs faintly, distant torch-glow breathes"),
    4:  (WIDE, "thin incense smoke curls upward, a shaft of light breathes brighter and dimmer, dust motes drift slowly"),
    5:  (WIDE, "the cloud of glory above the mercy seat glows and breathes gently, fine golden motes drift, the surrounding shadow deepens"),
    6:  (PUSH, "thin gray smoke drifts up from the scorched ground, fine ash motes settle slowly, the dim light breathes"),
    7:  (PUSH, "dust drifts in a shaft of light, the two goats' coats and the priest's linen stir faintly"),
    8:  (PUSH, "the faint golden glow of the mercy seat breathes gently, a thin thread of smoke curls, dust drifts -- the settled blood stays perfectly still"),
    9:  (PUSH, "dust drifts in the light, the live goat's coat and the priest's linen stir faintly, shadow breathes"),
    10: (WIDE, "heat-haze and fine dust rise off the desert, the far horizon shimmers, the departing goat's shape holds perfectly still"),
    11: (WIDE, "the altar fire glows and pulses warm, a thin thread of smoke curls upward, faint heat-haze drifts -- both goats stay perfectly still"),
    12: (PUSH, "the low flame flickers gently, thin smoke curls, dust drifts, the small distant sun holds still"),
    13: (WIDE, "dust drifts over the emptying court, a shaft of light breathes, the robes of the frozen people stir almost imperceptibly"),
    14: (PUSH, "the ghosted echoes hold perfectly still, thin smoke drifts, fine dust settles, the dim recurring light breathes"),
    15: (PUSH, "a shaft of light breathes brighter and dimmer, dust motes drift, the priest's linen stirs faintly"),
    16: (WIDE, "warm light breathes gently across the scene, heat-haze and fine dust drift, the cross-shadow holds perfectly still"),
    17: (PUSH, "the radiant light at the torn veil glows and breathes gently, fine motes drift, Christ's robe and hair stir almost imperceptibly"),
    18: (PUSH, "the cross of soft light above Christ glows and breathes, fine golden motes drift -- both goats and every figure hold perfectly still"),
    19: (WIDE, "warm evening haze drifts over the skyline, the golden radiance around Christ breathes gently, fine dust drifts, his robe stirs faintly"),
    20: (PUSH, "the shaft of light through the torn veil breathes, dust motes drift, the seated Christ's golden radiance glows gently -- the standing figures hold still"),
    21: (PUSH, "the priest's stride stays frozen exactly as drawn -- his legs, feet, arms and robe do "
               "NOT step, swing, walk forward or change position at all, he stays locked mid-step like "
               "a statue; the flock of goats stays perfectly still; only a shaft of light breathes and "
               "fine dust drifts"),
    22: (PUSH, "the golden radiance around Christ breathes brighter and dimmer, dust drifts across the road, the far speck on the horizon holds still"),
    23: (WIDE, "warm light pours and breathes through the opening, fine motes drift, robe hems stir faintly"),
    24: (PUSH, "Christ at the centre stays perfectly frozen -- his head, face, eyes, gaze and "
               "expression do NOT move, tilt, turn, rise or change at all; he stays locked exactly "
               "as drawn like a statue; every other figure holds perfectly still too; only the light "
               "through the open way glows and breathes and fine golden motes drift"),
    25: (HERO, "the warm golden radiance behind Christ glows and breathes gently brighter and dimmer, his robe and hair stir almost imperceptibly, his gentle expression never changes"),
}


def stem_for(s: dict) -> str:
    t = s["title"].lower()
    t = "".join(c if (c.isalnum() or c == " ") else "" for c in t)
    return f"{s['id']:02d}_{'_'.join(t.split())[:46]}"


def model_for(sid: int) -> str:
    return "kling3_0" if sid in KLING_SCENES else "seedance1_5"


def params_for(model: str) -> dict:
    dur = _hf_duration(model, TARGET_DUR)
    p = {"duration": dur, "aspect_ratio": "16:9"}
    if model == "kling3_0":
        p["mode"] = "pro"
        p["sound"] = "off"
    return p


def migration_spend() -> float:
    return round(sum(cost._usd(r.get("est_usd")) for r in cost.load()
                     if r.get("episode") == SLUG and r.get("ts", "") >= MIGRATION_START), 2)


def animate_one(png: Path, out: Path, model: str, prompt: str, params: dict) -> bool:
    cmd = [HF, "generate", "create", model, "--start-image", str(png), "--prompt", prompt]
    for k, v in params.items():
        cmd += [f"--{k}", str(v)]
    cmd += ["--wait"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print(f"       NSFW-REJECTED (would need direct-Kling fallback)")
        return False
    m = re.search(r'https?://\S+?\.mp4', blob)
    if not m:
        print(f"       no mp4 url: {blob.strip()[-200:]}")
        return False
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="comma-separated scene ids")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--override", action="store_true", help="bypass the migration ceiling")
    ap.add_argument("--dry-run", action="store_true", help="preflight cost only, render nothing")
    a = ap.parse_args()
    only = {int(x) for x in a.only.split(",") if x.strip()} if a.only else None

    CLIPS.mkdir(parents=True, exist_ok=True)
    plan = json.loads((OUT / "scene_plan.json").read_text(encoding="utf-8"))
    scenes = [s for s in plan["scenes"] if only is None or s["id"] in only]

    print(f"[budget] migration spent so far: ${migration_spend():.2f} / ${MIGRATION_CEILING:.0f} ceiling")
    print(f"[plan] {len(scenes)} scene(s):")
    batch_est = 0.0
    for s in scenes:
        model = model_for(s["id"])
        params = params_for(model)
        est = cost.hf_estimate(model, params=params) * cost.CREDITS_TO_USD
        batch_est += est
        print(f"   #{s['id']:02d} {model:<12} {params['duration']}s  ~${est:.2f}  {s['title'][:40]}")
    print(f"[plan] batch estimate ~${batch_est:.2f}  ->  projected migration total ~${migration_spend()+batch_est:.2f}")
    if a.dry_run:
        return

    ok = fail = skip = 0
    for s in scenes:
        stem = stem_for(s)
        png = OUT / f"{stem}.png"
        out = CLIPS / f"{stem}.mp4"
        if out.exists() and out.stat().st_size > 0 and not a.force:
            print(f"[skip] {out.name} (exists)")
            skip += 1
            continue
        if not png.exists():
            print(f"[FAIL] #{s['id']:02d}: missing still {png.name}")
            fail += 1
            continue
        model = model_for(s["id"])
        params = params_for(model)
        est = cost.hf_estimate(model, params=params) * cost.CREDITS_TO_USD
        proj = migration_spend() + est
        if proj > MIGRATION_CEILING and not a.override:
            print(f"[STOP] #{s['id']:02d} would push migration to ~${proj:.2f} > ${MIGRATION_CEILING:.0f} "
                  f"ceiling. Re-run with --override to proceed.")
            fail += 1
            break
        move, living = MOTION[s["id"]]
        prompt = BASE.format(move=move, living=living)
        print(f"[clip] #{s['id']:02d} {model} {params['duration']}s ~${est:.2f} -> {out.name} ...", flush=True)
        t = time.time()
        if animate_one(png, out, model, prompt, params):
            cost.record_hf(SLUG, "long", "animate", model, note=f"[ink-anim] #{s['id']:02d} {s['title'][:30]}",
                           params=params)
            print(f"       ok ({time.time()-t:.0f}s)")
            ok += 1
        else:
            print(f"       FAILED")
            fail += 1

    print(f"\n[done] animated {ok}, skipped {skip}, failed {fail}")
    print(f"[budget] migration total now ~${migration_spend():.2f} / ${MIGRATION_CEILING:.0f}")


if __name__ == "__main__":
    main()
