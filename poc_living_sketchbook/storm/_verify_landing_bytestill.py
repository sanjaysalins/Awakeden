"""One-off verification: confirm s13's landing frames are pixel-identical
between v5 (STORM_living_sketchbook.mp4, already shipped/watermarked) and
v6's PRE-watermark output (STORM_living_sketchbook_v6.prewm.bak.mp4, written
by add_watermark.py) -- the HARD RULE is "the landing is untouchable", and
s13_landing gets zero paper devices in apply_paper_devices_v6 (falls through
to S4.apply_paper_devices unchanged). Compares a center crop (avoiding the
top-left watermark corner both files carry) at several timestamps well
inside the landing hold. Deleted after use; not part of the deliverable.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
V5 = HERE / "STORM_living_sketchbook.mp4"
V6 = HERE / "STORM_living_sketchbook_v6.prewm.bak.mp4"


def grab(src, t, out):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t}", "-i", str(src),
                     "-frames:v", "1", str(out)], check=True)


def main():
    if not V6.exists():
        print(f"[skip] {V6} not found yet")
        return 1
    tmp = HERE / "_bytestill_tmp"
    tmp.mkdir(exist_ok=True)
    times = [51.0, 55.0, 58.0, 61.0]
    max_diffs = []
    for t in times:
        a = tmp / f"v5_{t}.png"
        b = tmp / f"v6_{t}.png"
        grab(V5, t, a)
        grab(V6, t, b)
        ia = np.asarray(Image.open(a).convert("RGB"), np.int16)
        ib = np.asarray(Image.open(b).convert("RGB"), np.int16)
        # center crop, well clear of the top-left watermark corner (x<240,y<160)
        crop_a = ia[300:1700, 300:900]
        crop_b = ib[300:1700, 300:900]
        diff = np.abs(crop_a - crop_b)
        max_diffs.append((t, int(diff.max()), float(diff.mean())))
    for t, mx, mean in max_diffs:
        status = "BYTE-STILL" if mx == 0 else f"DIFFERS (max={mx}, mean={mean:.3f})"
        print(f"  t={t:5.1f}s  {status}")
    ok = all(mx == 0 for (_, mx, _) in max_diffs)
    print("RESULT:", "PASS -- landing untouched, byte-identical to v5" if ok
          else "FAIL -- landing pixels differ from v5, investigate")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
