"""Graphic-novel FONT demo for the EW01 trailer captions (2026-07-22).

The B&W->colour world is locked; the last gap is the LETTERFORM — Impact/Arial
Black read as poster/corporate, not inked comic lettering. This renders the same
"TWO GOATS" slam over the B&W grid in the real graphic-novel faces already on the
box, so we can pick the letterform:
  Bangers          — classic comic-book caption (bold, inky, punchy)
  PermanentMarker  — hand-inked marker (indie graphic-novel)
  BarlowBlack      — bold condensed (modern movie-trailer control)

White fill + heavy black ink outline = the standard comic caption that reads on
any inked background. Transparent Chromium/CSS render, composited over B&W footage.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_comic_font_demo.py
"""
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked"
CLIPS = OUT / "clips"
DEMO = OUT / "_trailer" / "_font_demo"
DEMO.mkdir(parents=True, exist_ok=True)

W, H, FPS, DUR = 1920, 1080, 30, 3.0
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS), "-pix_fmt", "yuv420p"]

FONTS = [
    ("Bangers",         "file:///C:/Windows/Fonts/Bangers-Regular.ttf",         200),
    ("PermanentMarker", "file:///C:/Windows/Fonts/PermanentMarker-Regular.ttf", 172),
    ("BarlowBlack",     "file:///C:/Windows/Fonts/BarlowCondensed-Black.ttf",   224),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{' '.join(str(c) for c in cmd[:8])}...\n{r.stderr[-1400:]}")


def clip_for(cid):
    return sorted(CLIPS.glob(f"{cid:02d}_*.mp4"))[0]


def build_bw_grid(dst):
    """The TWO GOATS grid, graded to inky graphic-novel B&W."""
    ids = [7, 8, 9, 10]
    ins = []
    for cid in ids:
        ins += ["-stream_loop", "-1", "-t", f"{DUR}", "-i", str(clip_for(cid))]
    pre = "".join(
        f"[{i}:v]scale=957:537:force_original_aspect_ratio=increase,crop=957:537,"
        f"pad=960:540:(ow-iw)/2:(oh-ih)/2:color=0x0a0806,setsar=1[c{i}];"
        for i in range(4))
    grid = (f"[c0][c1][c2][c3]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0,"
            f"hue=s=0,eq=contrast=1.13:brightness=-0.015,fps={FPS},format=yuv420p[v]")
    run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", pre + grid,
         "-map", "[v]", "-t", f"{DUR}", "-an", *ENC, str(dst)])


def html_caption(font_family, font_uri, size, words):
    word_html = ""
    for wi, w in enumerate(words):
        delay = 0.12 + wi * 0.26
        word_html += f'\n      <div class="word" style="animation-delay:{delay:.2f}s">{w}</div>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
  @font-face {{ font-family:'GN'; src:url('{font_uri}'); }}
  html,body {{ margin:0; width:{W}px; height:{H}px; background:transparent; overflow:hidden; }}
  .stage {{ position:absolute; inset:0; display:flex; flex-direction:column;
            align-items:center; justify-content:center; gap:4px; top:170px; }}
  .word {{ font-family:'GN',sans-serif; font-size:{size}px; line-height:1.0; letter-spacing:2px;
           color:#f7f2e6; -webkit-text-stroke:11px #100d09; paint-order:stroke fill;
           text-shadow:0 9px 0 rgba(0,0,0,.4), 0 0 30px rgba(0,0,0,.5);
           opacity:0; transform-origin:50% 60%;
           animation:slam .52s cubic-bezier(.2,1.7,.32,1) both; }}
  @keyframes slam {{
     0%   {{ opacity:0; transform:scale(2.6) translateY(-64px) rotate(-7deg); }}
     55%  {{ opacity:1; transform:scale(.85) translateY(0) rotate(2deg); }}
     74%  {{ transform:scale(1.08) rotate(-1deg); }}
     100% {{ opacity:1; transform:scale(1) rotate(0); }} }}
</style></head><body>
  <div class="stage">{word_html}
  </div>
</body></html>"""


def render_transparent(html, frames_dir):
    if frames_dir.exists():
        for f in frames_dir.glob("*.png"):
            f.unlink()
    frames_dir.mkdir(parents=True, exist_ok=True)
    hp = frames_dir.parent / (frames_dir.name + ".html")
    hp.write_text(html, encoding="utf-8")
    n = int(DUR * FPS)
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--force-color-profile=srgb"])
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto(hp.resolve().as_uri())
        pg.wait_for_timeout(200)
        pg.evaluate("document.getAnimations().forEach(a=>a.pause())")
        for i in range(n):
            pg.evaluate("(t)=>document.getAnimations().forEach(a=>a.currentTime=t)", i * 1000.0 / FPS)
            pg.screenshot(path=str(frames_dir / f"f{i:05d}.png"), omit_background=True)
        b.close()
    hp.unlink()


def composite(bg, frames_dir, dst):
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(bg),
         "-framerate", str(FPS), "-i", str(frames_dir / "f%05d.png"),
         "-filter_complex", "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v]",
         "-map", "[v]", "-t", f"{DUR}", "-an", *ENC, str(dst)])


def main():
    words = ["TWO", "GOATS"]
    bg = DEMO / "_bw_grid.mp4"
    print("[bg] B&W grid ...")
    build_bw_grid(bg)
    for name, uri, size in FONTS:
        print(f"[render] {name} ...")
        fdir = DEMO / f"_frames_{name}"
        render_transparent(html_caption(name, uri, size, words), fdir)
        out = DEMO / f"demo_font_{name}.mp4"
        composite(bg, fdir, out)
        print(f"  -> {out}")
    print("\n[done]", DEMO)


if __name__ == "__main__":
    main()
