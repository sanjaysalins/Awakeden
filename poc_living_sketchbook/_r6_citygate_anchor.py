"""living-sketchbook -- city-gate world anchor for the Day of Atonement episode.

Extends world/TABERNACLE_WORLD.md (item 9) -- a DIFFERENT era from the
wilderness-tabernacle anchors (1-8): Hebrews 13:12 "suffered without the
gate" places this at 1st-century Jerusalem (Second Temple period), not the
wilderness camp. Needed for spreads 57/58 (Christ led out of the city gate,
paired MV with the sin-offering's body carried outside the camp).

  .venv\\Scripts\\python.exe poc_living_sketchbook/_r6_citygate_anchor.py
"""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline import cost

spec = importlib.util.spec_from_file_location(
    "_e1", ROOT / "poc_castbible_look" / "episode_door" / "_e1_anchors.py")
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)

WORLD = Path(__file__).resolve().parent / "world"
WORLD.mkdir(parents=True, exist_ok=True)
EPISODE = "LS_DayOfAtonement"

CITYGATE_CANON = (
    "A massive ancient city gate built of huge dressed limestone blocks "
    "with drafted margins (Herodian-era ashlar masonry), set into a thick "
    "sun-baked stone city wall, a tall arched gateway opening onto a rough "
    "dirt road leading out into hilly Judean wilderness beyond -- "
    "weathered, sun-bleached stone, harsh midday light, no ornament, no "
    "modern hardware, no medieval towers or crenellations -- plain "
    "functional 1st-century Near Eastern construction, wide establishing "
    "view, the gateway and the road leading away from it both visible."
)


def run(prompt, out, ar):
    cmd = [E.HF, "generate", "create", E.MODEL, "--prompt", prompt,
           "--aspect_ratio", ar, "--resolution", "2k", "--wait"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    out = WORLD / "citygate_ref.png"
    if out.exists():
        print("[skip] citygate_ref")
        return
    prompt = E.STYLE + "\n\nSCENE: " + CITYGATE_CANON
    print("[ref] citygate_ref ...", flush=True)
    ok = run(prompt, out, "16:9")
    if not ok:
        ok = run(prompt, out, "16:9")
    if ok:
        cost.record_hf(EPISODE, "long", "world_anchor", E.MODEL, note="[dayofatonement] citygate_ref")
        print("   ok")
    else:
        print("   FAILED")


if __name__ == "__main__":
    main()
