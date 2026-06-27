"""Deterministically remove nano_banana's hallucinated corner signatures from an episode's
stills by cropping the bottom strip (where they always sit) and rescaling back to 16:9.
Guarded by a <stem>.sigcrop marker so it never double-crops. Episode-generic.
  python _sig_crop.py EW01_Two_Goats [--pct 6] [--force]
"""
import sys, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _episode import resolve

ep = resolve(sys.argv)
PCT = 6.0
if "--pct" in sys.argv:
    PCT = float(sys.argv[sys.argv.index("--pct") + 1])
FORCE = "--force" in sys.argv
keep = 1.0 - PCT / 100.0

def probe(p):
    out = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
        "stream=width,height","-of","csv=p=0:s=x",str(p)], capture_output=True, text=True).stdout.strip()
    w, h = out.split("x"); return int(w), int(h)

done = skipped = 0
for s in ep.scenes:
    png = ep.png(s)
    if not png.exists():
        continue
    marker = png.with_suffix(".sigcrop")
    if marker.exists() and not FORCE:
        skipped += 1; continue
    w, h = probe(png)
    tmp = png.with_suffix(".crop.png")
    # crop off the bottom PCT% (anchored at top), then scale back to the original W x H (16:9)
    subprocess.run(["ffmpeg","-y","-i",str(png),
        "-vf",f"crop={w}:{int(h*keep)}:0:0,scale={w}:{h}", str(tmp)],
        capture_output=True, text=True)
    if tmp.exists() and tmp.stat().st_size > 0:
        tmp.replace(png)
        marker.write_text(f"bottom {PCT}% cropped\n", encoding="utf-8")
        print(f"[crop] {png.name}  (bottom {PCT}%)"); done += 1
    else:
        print(f"[FAIL] {png.name}")
print(f"\n[done] cropped {done}, skipped {skipped}")
