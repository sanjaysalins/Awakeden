"""Night Threshold cast mini bake-off (MEDIUM_SELECTION.md sec.7, item 5 --
the one real spend in the Stationer plan). Tests whether a named cast anchor
(jesus_ref.png / moses_ref.png) survives identity-lock under the NIGHT_INK
medium anchor, at two framings: a distant/silhouette threshold shot (the
scale medium_manifest.json currently allows for this medium) and a closer
mid-shot with the face turned toward camera (the scale that would be needed
to ever raise Night Threshold's face_scale above "silhouette-only").

Reuses the real character canon text + FULLBLEED framing note from
_run_bakeoff.py (no retyped copies) and the same run()/ledger pattern.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_identity_bakeoff/_run_night_threshold_bakeoff.py --list
  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_identity_bakeoff/_run_night_threshold_bakeoff.py
"""
import re
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
from pipeline.medium_registry import MEDIUMS

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _run_bakeoff import MOSES, JESUS, FULLBLEED, MOSES_REF, JESUS_REF  # noqa: E402

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "LS_NightThresholdBakeoff"
HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "stills_night_threshold"

NIGHT = MEDIUMS["md_night_ink"]

SILHOUETTE_SCENE = (
    "A wide, distant shot at a doorway at midnight: {subject} standing at "
    "the threshold, seen mostly in silhouette against a pale wash of light "
    "beyond the doorframe, face in shadow, not readable in detail. "
    + FULLBLEED
)
CLOSE_SCENE = (
    "A close, intimate mid-shot at night: {subject}'s face turned directly "
    "toward the viewer, lit only by a pale wash of light from one side, "
    "expression calm and watchful. " + FULLBLEED
)

JOBS = [
    ("moses_silhouette", MOSES_REF, SILHOUETTE_SCENE.format(subject=MOSES)),
    ("moses_close", MOSES_REF, CLOSE_SCENE.format(subject=MOSES)),
    ("jesus_silhouette", JESUS_REF, SILHOUETTE_SCENE.format(subject=JESUS)),
    ("jesus_close", JESUS_REF, CLOSE_SCENE.format(subject=JESUS)),
]


def run(prompt, out, ref):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--resolution", "2k", "--wait",
           "--image", str(ref)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    if "--list" in sys.argv[1:]:
        print(f"{len(JOBS)} jobs (model={MODEL}, ~2cr each, ~{len(JOBS)*2}cr total):\n")
        for slug, ref, prompt in JOBS:
            print(f"[{slug}] ref={ref.name}")
            print(f"    {NIGHT.prompt(prompt)[:160]}...")
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for ref in (MOSES_REF, JESUS_REF):
        if not ref.exists():
            print(f"FAILED -- missing {ref}")
            return

    for slug, ref, scene in JOBS:
        out = OUT_DIR / f"{slug}.png"
        if out.exists():
            print(f"[skip] {slug}")
            continue
        prompt = NIGHT.prompt(scene)
        print(f"[img] {slug} ...", flush=True)
        ok = run(prompt, out, ref)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, ref)
        if ok:
            try:
                cost.record_hf(EPISODE, "poc", "stills", MODEL, note=f"[nightthreshold] {slug}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT_DIR}")


if __name__ == "__main__":
    main()
