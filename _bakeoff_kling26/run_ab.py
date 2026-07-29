"""kling2_6 vs kling3_0-pro A/B (user-approved 2026-07-21, ~$1.50).

Renders ONLY the kling2_6 side (5cr/clip, boolean --sound false, --image flag) with the
byte-identical production prompt, and pairs each clip against the EXISTING production
kling3_0 pro clip (8.75cr) already in visual/nbp/. Scenes chosen to stress both anim
modes: #08 gallery hard-cut over a multi-figure crowd, #19 push-in on the Christ landing.
Output: _bakeoff_kling26/compare.html
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import _hf_animate_short as sh  # viral_prompt / pushin_prompt (the production prompts)
from pipeline.clip_anim_qc import choose_anim_mode
from pipeline import cost

HF = Path.home() / "bin" / "hf.exe"
SHORT = ROOT / "longform" / "02_Psalm_22_Song_From_The_Cross" / "v1" / "shorts" / "06_The_Ends_Of_The_Earth"
OUT = Path(__file__).resolve().parent
SCENES = [8, 19]
PARAMS = {"duration": 5, "sound": "false", "aspect_ratio": "9:16"}

plan = json.load(open(SHORT / "visual" / "scene_plan.json", encoding="utf-8"))
scenes = plan["plan"]["scenes"] if "plan" in plan else plan["scenes"]
by_idx = {s["index"]: s for s in scenes}
nbp = SHORT / "visual" / "nbp"

pairs = []
for idx in SCENES:
    png = next(nbp.glob(f"{idx:02d}_*.png"))
    prod = png.with_suffix(".mp4")
    sc = by_idx[idx]
    mode = choose_anim_mode(sc)
    prompt = sh.pushin_prompt(sc) if mode == "pushin" else sh.viral_prompt(sc)
    new = OUT / f"{png.stem}__kling2_6.mp4"
    old = OUT / f"{png.stem}__kling3_0_pro.mp4"
    if not old.exists():
        shutil.copy2(prod, old)
    if new.exists():
        print(f"[skip] {new.name} exists")
        pairs.append((idx, sc["title"], mode, old.name, new.name)); continue
    print(f"[k2.6] scene {idx:02d} mode={mode} ...", flush=True)
    cmd = [str(HF), "generate", "create", "kling2_6", "--image", str(png),
           "--prompt", prompt, "--duration", "5", "--sound", "false",
           "--aspect_ratio", "9:16", "--wait"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + (r.stderr or "")
    m = re.search(r'https?://[^\s"]+\.mp4', blob)
    if not m:
        print(f"   FAILED: {blob.strip()[-300:]}"); continue
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(new)], check=True)
    cost.record_hf("bakeoff_kling26", "clip", "animate", "kling2_6",
                   note=f"{png.stem} A/B vs kling3_0 pro", params=PARAMS)
    print(f"   ok {new.name} ({new.stat().st_size:,} b)")
    pairs.append((idx, sc["title"], mode, old.name, new.name))

rows = "".join(f"""
<section><h2>#{idx:02d} {title} <span class="mode">{mode}</span></h2>
<div class="pair">
  <figure><video src="{a}" autoplay loop muted playsinline></video>
    <figcaption>kling3_0 <b>pro</b> — 8.75cr (production)</figcaption></figure>
  <figure><video src="{b}" autoplay loop muted playsinline></video>
    <figcaption>kling2_6 — <b>5cr</b> (challenger, same prompt)</figcaption></figure>
</div></section>""" for idx, title, mode, a, b in pairs)

(OUT / "compare.html").write_text(f"""<!doctype html><meta charset="utf-8">
<title>kling2_6 vs kling3_0-pro A/B</title>
<style>body{{background:#111;color:#eee;font-family:system-ui;margin:2rem}}
h1{{font-size:1.3rem}} h2{{font-size:1.05rem;margin:1.6rem 0 .5rem}}
.mode{{color:#f9b234;font-size:.85rem;margin-left:.5rem}}
.pair{{display:flex;gap:1rem}} figure{{margin:0}}
video{{width:330px;border-radius:8px;display:block}}
figcaption{{margin-top:.4rem;font-size:.9rem;color:#bbb}}</style>
<h1>kling2_6 (5cr) vs kling3_0 pro (8.75cr) — same still, byte-identical prompt, 5s 9:16, sound off</h1>
{rows}""", encoding="utf-8")
print(f"\n[done] {OUT / 'compare.html'}")
