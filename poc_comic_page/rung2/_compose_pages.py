"""Comic Page Pipeline POC -- Rung 2 FINAL PHASE, Step 4: compose the 5 pages
via panel_animator/grid_choreography.py ($0, deterministic virtual page
camera). 1080x1920, uniform spotlight (equal per-panel dwell, no favoured
panel), total_duration = page dwell (page5 gets its dwell PLUS the 3.24s
INV-26 landing hold as a bonus partial sweep back onto the hero cell).

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_compose_pages.py            # all 5
  .venv\\Scripts\\python.exe poc_comic_page/rung2/_compose_pages.py page3      # just one
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GC = ROOT / "panel_animator" / "grid_choreography.py"
EXT = HERE / "clips" / "extended"
R1_EXT = HERE.parent / "rung1" / "clips" / "extended"

PAGES = {
    "page1": dict(clips=[EXT / "p1a.mp4", EXT / "p1b.mp4"],
                  layout="2v", per_panel=10.08 / 2, total=10.08),
    "page2": dict(clips=[EXT / "p2a.mp4", EXT / "p2b.mp4", EXT / "p2c.mp4"],
                  layout="3-big-left", per_panel=10.96 / 3, total=10.96),
    "page3": dict(clips=[EXT / "panel_b.mp4", R1_EXT / "panel_a.mp4", EXT / "panel_c.mp4", EXT / "panel_d.mp4"],
                  layout="2x2", per_panel=12.10 / 4, total=12.10),
    "page4": dict(clips=[EXT / "p4a.mp4", EXT / "p4b.mp4", EXT / "p4c.mp4"],
                  layout="3-big-left", per_panel=10.64 / 3, total=10.64),
    "page5": dict(clips=[EXT / "p5a.mp4", EXT / "p5b.mp4", EXT / "p5c.mp4"],
                  layout="3-big-top", per_panel=10.66 / 3, total=13.90),
}


def build(page_key):
    cfg = PAGES[page_key]
    out = HERE / f"{page_key}_composite.mp4"
    for c in cfg["clips"]:
        if not c.exists():
            raise SystemExit(f"[{page_key}] missing clip: {c}")
    cmd = [sys.executable, str(GC), "--clips"] + [str(c) for c in cfg["clips"]] + [
        "--out", str(out), "--layout", cfg["layout"],
        "--per-panel", f"{cfg['per_panel']:.4f}", "--total-duration", f"{cfg['total']:.2f}",
        "--w", "1080", "--h", "1920",
    ]
    print(f"[compose] {page_key} ({cfg['layout']}, {len(cfg['clips'])} clips, "
          f"per_panel={cfg['per_panel']:.3f}s, total={cfg['total']:.2f}s)")
    subprocess.run(cmd, check=True)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0", str(out)],
                       capture_output=True, text=True)
    print(f"   -> {out}  probe: {r.stdout.strip()}")


if __name__ == "__main__":
    pages = sys.argv[1:] or list(PAGES.keys())
    for p in pages:
        build(p)
