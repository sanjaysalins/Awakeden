"""Trailer test batch (2 shots): S6 (serpent sinking) + S3 (Adam+Eve running).
Reuses the episode's own STYLE/ADAM/EVE/SERPENT/EDEN/FULLBLEED constants and
render pipeline -- same nano_banana_pro HF call as _s2_stills.py, just a
separate output dir since this is trailer-specific, not a numbered spread.

  .venv\\Scripts\\python.exe poc_living_sketchbook/seed_of_the_woman/_trailer/_t1_stills_test.py
"""
import importlib.util
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "SeedOfTheWoman"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

EP_DIR = HERE.parent
CAST = EP_DIR.parent / "cast"
WORLD = EP_DIR.parent / "world"
SPREADS_STILLS = EP_DIR / "stills"

# import the episode's own constants/refs so the trailer matches the film's
# exact style block, not a re-typed copy
spec = importlib.util.spec_from_file_location("_ep_stills", EP_DIR / "_s2_stills.py")
ep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ep)

REF_MAP = {
    "adam": CAST / "adam_ref.png",
    "eve": CAST / "eve_ref.png",
    "serpent": WORLD / "serpent_ref.png",
    "s18": SPREADS_STILLS / "s18_turns_to_serpent.png",
}

SHOTS = [
    # S6: serpent sinking belly-flat as the God-light edge reaches it.
    # High angle looking DOWN (SERPENT.md rule 2, never violated even in
    # the trailer's more kinetic register); ink-blue only, never warm;
    # no face close-up, no eye contact (rule 5). Real invented creature
    # motion is the ONE freedom granted here (user-approved, trailer-only).
    ("t_s6_serpent_sinking", "serpent,s18",
     f"STEEP HIGH-ANGLE view, the camera looking sharply DOWN (per world/"
     f"SERPENT.md's locked camera rule -- the lens never kneels to the "
     f"enemy): {ep.SERPENT} Coiled among a tree's exposed roots in the "
     f"dust, head turned aside in profile, NOT facing the camera, no eye "
     f"contact with the viewer, no face close-up. A hard-edged band of "
     f"warm golden light is sweeping across the ground from one side of "
     f"the frame, having not yet reached the serpent -- clear dark "
     f"ground still separates the light's leading edge from the "
     f"creature. Ink-blue-toned scales throughout, cool judgment "
     f"coloring, never gold, never warm. {ep.FULLBLEED}"),
    # S3: Adam and Eve actually RUNNING -- real locomotion, the one thing
    # the film's own body never shows. Lateral tracking framing, mid-
    # distance (identity-drift guard: not a close face shot), foreground
    # foliage for whip-past blur potential at animate time.
    ("t_s3_running", "adam,eve",
     f"WIDE lateral tracking shot, eye-level, camera moving alongside "
     f"the runners: {ep.ADAM} and {ep.EVE}, both captured mid-stride in "
     f"a genuine dead run through the garden, real forward-leaning "
     f"running posture, arms driving, both figures at mid-distance from "
     f"camera (not a close face shot), out-of-focus leaves and ferns "
     f"filling the near foreground as if the camera runs alongside them "
     f"through the undergrowth. The garden's warm gold light streaks "
     f"past behind them. Genuine motion-forward body mechanics, not a "
     f"static standing pose. {ep.FULLBLEED}"),
]


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "16:9", "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def resolve_refs(tag):
    refs = []
    for t in tag.split(","):
        t = t.strip()
        if t and REF_MAP.get(t) and REF_MAP[t].exists():
            refs.append(REF_MAP[t])
    return refs


def main():
    for name, tag, scene in SHOTS:
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        refs = resolve_refs(tag)
        prompt = ep.STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(refs)}) ...", flush=True)
        ok = run(prompt, out, refs)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, refs)
        if ok:
            try:
                cost.record_hf(EPISODE, "long", "trailer_test", MODEL, note=f"[trailer] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")


if __name__ == "__main__":
    main()
