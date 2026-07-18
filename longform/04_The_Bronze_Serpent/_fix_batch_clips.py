"""One-off: re-render 7 clips after the user's media-review pass (2026-07-19).
6 are still+clip redos (12,16,18,25,31,two_thieves_foreground -- the T-dagger
nail artifact + scene 25's floating cross + scene 18's gore, all fixed at the
still level already). 1 is a clip-only redo (13 -- the still is fine, the
Kling-rendered clip invented blood spreading down the garment during
animation; re-animate with an explicit no-growth motion prompt, Seedance
instead of Kling per the locked "Kling invents blood" lesson).
Seedance 1.5 Pro for all seven -- none of these are action/crowd panels.
"""
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked"
SLUG_EP = "04_The_Bronze_Serpent"
MODEL = "seedance1_5"

BASE = ("Graphic novel inked illustration, painted tableau, a frozen moment. {content} "
        "The camera holds nearly still, an almost imperceptible settle, resting on the "
        "scene. Nothing moves -- every figure and element stays fixed as drawn, no "
        "blood grows, no blood drips, no blood spreads beyond what is painted at the "
        "wound. No invented motion, no morphing, no new elements, no camera shake. "
        "Painted tableau stays still; only the camera moves.")

JOBS = {
    "12_even_so_must_the_son_of_man_be_lifted_up": BASE.format(content=(
        "A gleaming bronze serpent coiled on a wooden pole on one side, and on the "
        "other Christ crucified on a wooden cross, arms outstretched, a small flat "
        "nail flush at each wrist with a thin trickle of blood, head bowed, wearing a "
        "simple robe.")),
    "16_the_likeness_of_the_curse_lifted_up": BASE.format(content=(
        "A gleaming bronze serpent coiled on a wooden pole in shadow on one side, and "
        "lit on the other Christ crucified on a wooden cross, arms outstretched, a "
        "small flat nail flush at each wrist with a thin trickle of blood, head bowed, "
        "wearing a simple robe.")),
    "18_curse": BASE.format(content=(
        "In the foreground a dying man on the desert ground reaching one hand upward, "
        "a small dark bite mark on the back of his hand. Far behind and above him, "
        "luminous against the dark, Christ crucified on a wooden cross, a small flat "
        "nail flush at each wrist with a thin trickle of blood, wearing a simple robe.")),
    "25_we_are_all_bitten__the_cure_outside_us": BASE.format(content=(
        "In the foreground a dying man lying on the desert ground, his snake-bitten "
        "hand resting on the sand with two small red puncture marks. Far off on the "
        "horizon, small and luminous, Christ crucified on a wooden cross planted in a "
        "small rise of ground, a small flat nail flush at each wrist with a thin "
        "trickle of blood.")),
    "31_his_own_self_bare_our_sins_in_his_own_body_on_the_tree": BASE.format(content=(
        "Christ crucified on a wooden cross against a darkened storm sky, head bowed "
        "low, arms outstretched, a small flat nail flush at each wrist with a thin "
        "trickle of blood, wearing a simple cream-white robe covering his torso.")),
    "two_thieves_foreground": BASE.format(content=(
        "Two condemned thieves crucified on wooden crosses in the foreground, an "
        "older bald heavy-set man on the left and a younger curly-haired lean man on "
        "the right, each with a small flat nail flush at the wrist, Christ crucified "
        "on the taller central cross rising behind and between them, wearing a simple "
        "robe, head bowed.")),
    "13_lifted_up__signifying_what_death_he_should_die": BASE.format(content=(
        "Christ crucified on a wooden cross, stripped to a simple loincloth, arms "
        "bound and nailed to the crossbeam, head bowed, a small dry blood mark at the "
        "side wound and at each wrist -- these marks are fixed exactly as painted and "
        "stay completely unchanged, a walled city visible below in stormy evening "
        "light.")),
}

cli = str(config.HF_CLI_PATH)
ok = fail = 0
for slug, prompt in JOBS.items():
    png = OUT / f"{slug}.png"
    clip = OUT / "clips" / f"{slug}.mp4"
    if not png.exists():
        print(f"[skip] {slug}: no still at {png}")
        fail += 1
        continue
    print(f"[clip] {slug} ({MODEL}) ...", flush=True)
    cmd = [
        cli, "generate", "create", MODEL,
        "--start-image", str(png),
        "--prompt", prompt,
        "--duration", "4",
        "--aspect_ratio", "16:9",
        "--wait",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=600)
    blob = (result.stdout or "") + "\n" + (result.stderr or "")
    if "nsfw" in blob.lower():
        print(f"       FAIL (NSFW): {blob[-300:]}")
        fail += 1
        continue
    if result.returncode != 0:
        print(f"       FAIL ({result.returncode}): {blob[-300:]}")
        fail += 1
        continue
    m = re.search(r"https://\S+?\.mp4", result.stdout, re.IGNORECASE)
    if not m:
        print(f"       FAIL: no mp4 URL: {blob[-300:]}")
        fail += 1
        continue
    url = m.group(0)
    clip.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "JesusInTheBible/1.0"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        clip.write_bytes(resp.read())
    print(f"       ok -> {clip.name}")
    try:
        cost.record_hf(SLUG_EP, "long", "clip", MODEL, note=f"{slug} (media-review fix)")
    except Exception as e:
        print(f"       [cost] ledger row failed (non-fatal): {e}")
    ok += 1

print(f"\n[done] {ok} ok, {fail} failed")
