"""Most-dynamic animation test (2026-07-24) for the 3 David & Goliath template
stills: one continuous camera move per page -- rack from panel to panel,
hold briefly on each, push in hard on the climax panel -- instead of a fixed
camera with only atmosphere alive. All figures stay frozen throughout
(reinforced no-invention wording); only camera, light, dust and air move.

  .venv\\Scripts\\python.exe poc_thief_e2e/_animate_david_goliath_dynamic.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
from pipeline.video_render import _hf_duration
HF = str(config.HF_CLI_PATH)
HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills" / "_comic_strip_template_test"
OUT = HERE / "clips" / "_comic_strip_template_test"
OUT.mkdir(parents=True, exist_ok=True)

FROZEN_V2 = (
    "Every figure in every panel stays perfectly frozen the entire time -- no limbs move, no "
    "heads turn, no faces change, no expressions change, no skin changes, no new marks or "
    "liquid appear anywhere on any body or face, and no new figures, hands or objects appear. "
    "INVENT NOTHING AT ALL on any face or body -- every face stays pixel-for-pixel identical to "
    "this exact image throughout, in every panel, the whole time. All caption text stays "
    "exactly as drawn, unchanged. "
)
LEAD = "A finished comic-strip page with four panels, 9:16, filmed with a single continuous camera move: {moves} "
TAIL = FROZEN_V2 + "Only the light, dust and air are alive: {living}"

JOBS = [
    ("david_goliath_dynamic", "david_goliath.png",
     "the camera opens holding on the top wide panel showing the valley of Elah, then racks "
     "down and left to the tight close-up panel on the Philistine's snarling face, holds "
     "briefly, then racks right to the close-up panel on the young shepherd's calm face, holds "
     "briefly, then racks down and pushes in firmly on the bottom wide panel at the moment of "
     "impact.",
     "lightning flickers over the valley in the top panel; dust drifts faintly across the "
     "close-up panels; in the bottom panel, dust bursts upward and the light rays intensify as "
     "the camera pushes in."),
    ("david_goliath_p1_dynamic", "david_goliath_p1.png",
     "the camera opens holding on the top wide panel showing the warrior striding into the "
     "valley, then racks down and left to the tight close-up panel on his snarling face, holds "
     "briefly, then racks right to the panel on the young shepherd's face among the soldiers, "
     "holds briefly, then racks down and pushes in on the bottom panel inside the tent.",
     "storm clouds churn slowly over the valley in the top panel; dust drifts faintly across "
     "the close-up panels; in the bottom panel, the torch flame flickers and casts a warm "
     "moving light as the camera pushes in."),
    ("david_goliath_p2_dynamic", "david_goliath_p2.png",
     "the camera opens holding on the top wide panel at the brook, then racks down and left to "
     "the tight close-up panel on the Philistine's snarling face, holds briefly, then racks "
     "right to the panel on the young shepherd mid-motion with his sling, holds briefly, then "
     "racks down and pushes in hard on the bottom panel at the instant of impact.",
     "the brook glimmers faintly and clouds drift in the top panel; dust motes drift across the "
     "close-up panels; in the bottom panel, dust bursts upward and light rays intensify sharply "
     "as the camera pushes in for the final beat."),
]


def main():
    dur = _hf_duration("kling3_0", 10)
    for name, src, moves, living in JOBS:
        png = STILLS / src
        out = OUT / f"{name}.mp4"
        prompt = LEAD.format(moves=moves) + TAIL.format(living=living)
        cmd = [HF, "generate", "create", "kling3_0", "--start-image", str(png), "--prompt", prompt,
               "--duration", str(dur), "--aspect_ratio", "9:16", "--mode", "pro", "--sound", "off", "--wait"]
        print(f"[clip] {name} kling3_0 {dur}s -> {out.name} ...", flush=True)
        t = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        blob = (r.stdout or "") + "\n" + (r.stderr or "")
        if re.search(r"nsfw", blob, re.IGNORECASE):
            print("   NSFW-REJECTED"); continue
        m = re.search(r'https?://\S+?\.mp4', blob)
        if not m:
            print(f"   no mp4 url: {blob.strip()[-300:]}"); continue
        subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
        if out.exists() and out.stat().st_size > 0:
            cost.record_hf("EW_Thief_POC", "short", "animate", "kling3_0", note=f"[david-goliath-dynamic] {name}", params={"duration": dur})
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
