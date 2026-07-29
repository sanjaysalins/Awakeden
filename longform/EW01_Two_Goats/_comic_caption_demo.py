"""Comic-movie caption STYLE DEMO for the EW01 trailer (2026-07-22).

Proves we can do graphic comic-book animated text WITHOUT Remotion — using the
repo's own frame-exact Chromium/CSS engine (the same technique Remotion wraps).
Renders each caption as a TRANSPARENT layer (Playwright omit_background, per-frame
currentTime) and composites it over the real "TWO GOATS" grid footage.

Two contrasting directions on the same beat:
  A "ink-slam"  — hand-inked comic impact lettering: cream ink outline, per-word
                  slam with overshoot + rotate, white flash + speed-line burst.
  B "chromatic" — modern comic-movie title: cream caps, red/cyan chromatic split,
                  benday halftone dot burst, scale-slam + glow.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_comic_caption_demo.py
"""
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked"
CLIPS = OUT / "clips"
DEMO = OUT / "_trailer" / "_caption_demo"
DEMO.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1920, 1080, 30
DUR = 3.0
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS), "-pix_fmt", "yuv420p"]
IMPACT = "file:///C:/Windows/Fonts/impact.ttf"
ARIALBLK = "file:///C:/Windows/Fonts/ariblk.ttf"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{' '.join(str(c) for c in cmd[:8])}...\n{r.stderr[-1400:]}")


def clip_for(cid):
    return sorted(CLIPS.glob(f"{cid:02d}_*.mp4"))[0]


def build_grid_bg(dst):
    ids = [7, 8, 9, 10]
    ins = []
    for cid in ids:
        ins += ["-stream_loop", "-1", "-t", f"{DUR}", "-i", str(clip_for(cid))]
    pre = "".join(
        f"[{i}:v]scale=957:537:force_original_aspect_ratio=increase,crop=957:537,"
        f"pad=960:540:(ow-iw)/2:(oh-ih)/2:color=0x0a0806,setsar=1[c{i}];"
        for i in range(4))
    grid = f"[c0][c1][c2][c3]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0,fps={FPS},format=yuv420p[v]"
    run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", pre + grid,
         "-map", "[v]", "-t", f"{DUR}", "-an", *ENC, str(dst)])


# ---------------------------------------------------------------- style A: ink-slam
def html_inkslam(words):
    word_html = ""
    for wi, w in enumerate(words):
        delay = 0.10 + wi * 0.30
        word_html += f"""
      <div class="wrap">
        <div class="burst" style="animation-delay:{delay+0.14:.2f}s"></div>
        <div class="word" style="animation-delay:{delay:.2f}s">{w}</div>
      </div>"""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
  @font-face {{ font-family:'ImpactC'; src:url('{IMPACT}'); }}
  html,body {{ margin:0; width:{W}px; height:{H}px; background:transparent; overflow:hidden; }}
  .stage {{ position:absolute; inset:0; display:flex; flex-direction:column;
            align-items:center; justify-content:center; gap:6px; top:180px; }}
  .wrap {{ position:relative; display:flex; align-items:center; justify-content:center; }}
  .word {{ font-family:'ImpactC',sans-serif; font-size:230px; line-height:0.98; letter-spacing:4px;
           color:#14110b; -webkit-text-stroke:12px #f3e8cc; paint-order:stroke fill;
           text-shadow:0 10px 0 rgba(0,0,0,.34), 0 0 34px rgba(0,0,0,.45);
           opacity:0; transform-origin:50% 60%;
           animation:slam .52s cubic-bezier(.2,1.7,.32,1) both; }}
  @keyframes slam {{
     0%   {{ opacity:0; transform:scale(2.7) translateY(-70px) rotate(-9deg); }}
     55%  {{ opacity:1; transform:scale(.84) translateY(0) rotate(2.5deg); }}
     74%  {{ transform:scale(1.09) rotate(-1.5deg); }}
     100% {{ opacity:1; transform:scale(1) rotate(0); }} }}
  .burst {{ position:absolute; width:1100px; height:1100px; left:50%; top:50%;
            margin:-550px 0 0 -550px; opacity:0;
            background:
              radial-gradient(circle, rgba(255,255,255,.9) 0%, rgba(255,255,255,0) 26%),
              repeating-conic-gradient(from 0deg, rgba(20,17,11,.0) 0deg 7deg,
                 rgba(20,17,11,.42) 7deg 9deg);
            -webkit-mask:radial-gradient(circle, #000 34%, transparent 62%);
            animation:pop .42s ease-out both; }}
  @keyframes pop {{
     0%   {{ opacity:0; transform:scale(.35) rotate(0deg); }}
     35%  {{ opacity:.95; }}
     100% {{ opacity:0; transform:scale(1.5) rotate(14deg); }} }}
</style></head><body>
  <div class="stage">{word_html}</div>
</body></html>"""


# ------------------------------------------------------------ style B: chromatic halftone
def html_chromatic(words):
    lines = ""
    for wi, w in enumerate(words):
        d = 0.06 + wi * 0.16
        lines += f"""
      <div class="capline" style="--d:{d:.2f}s">
        <span class="rd">{w}</span><span class="cy">{w}</span><span class="base">{w}</span>
      </div>"""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
  @font-face {{ font-family:'ABlackC'; src:url('{ARIALBLK}'); }}
  html,body {{ margin:0; width:{W}px; height:{H}px; background:transparent; overflow:hidden; }}
  .stage {{ position:absolute; inset:0; display:flex; flex-direction:column;
            align-items:center; justify-content:center; gap:2px; top:150px; }}
  .halftone {{ position:absolute; left:50%; top:50%; width:1250px; height:720px;
               margin:-360px 0 0 -625px; opacity:0; z-index:-3;
               background:radial-gradient(circle, #12100c 30%, transparent 32%) 0 0/26px 26px;
               -webkit-mask:radial-gradient(ellipse 55% 55% at 50% 50%, #000 28%, transparent 70%);
               animation:htin .5s ease-out both; animation-delay:.04s; }}
  @keyframes htin {{ 0%{{opacity:0; transform:scale(.6);}} 45%{{opacity:.5;}} 100%{{opacity:.34; transform:scale(1);}} }}
  .capline {{ position:relative; display:inline-flex; justify-content:center;
              font-family:'ABlackC',sans-serif; font-size:196px; line-height:1.02; letter-spacing:3px;
              text-transform:uppercase; white-space:nowrap; }}
  .capline span {{ display:inline-block; }}
  .rd, .cy {{ position:absolute; left:0; right:0; text-align:center; }}
  .base {{ position:relative; color:#f6e7c1; -webkit-text-stroke:9px #14110b; paint-order:stroke fill;
           text-shadow:0 0 40px rgba(246,231,193,.35), 0 10px 0 rgba(0,0,0,.3);
           animation:slam .5s cubic-bezier(.2,1.55,.32,1) both; animation-delay:var(--d); }}
  .cy {{ color:#12d7ff; z-index:-1; animation:cy .55s cubic-bezier(.2,1.4,.3,1) both; animation-delay:var(--d); }}
  .rd {{ color:#ff2f57; z-index:-2; animation:rd .55s cubic-bezier(.2,1.4,.3,1) both; animation-delay:var(--d); }}
  @keyframes slam {{ 0%{{opacity:0; transform:scale(1.5);}} 60%{{opacity:1; transform:scale(.97);}} 100%{{transform:scale(1);}} }}
  @keyframes cy {{ 0%{{opacity:0; transform:translate(38px,24px) scale(1.5);}} 100%{{opacity:.9; transform:translate(-9px,-6px) scale(1);}} }}
  @keyframes rd {{ 0%{{opacity:0; transform:translate(-38px,-24px) scale(1.5);}} 100%{{opacity:.9; transform:translate(9px,6px) scale(1);}} }}
</style></head><body>
  <div class="stage">
    <div class="halftone"></div>{lines}
  </div>
</body></html>"""


def render_transparent(html, dur, frames_dir):
    if frames_dir.exists():
        for f in frames_dir.glob("*.png"):
            f.unlink()
    frames_dir.mkdir(parents=True, exist_ok=True)
    hp = frames_dir.parent / (frames_dir.name + ".html")
    hp.write_text(html, encoding="utf-8")
    n = int(dur * FPS)
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--force-color-profile=srgb"])
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto(hp.resolve().as_uri())
        pg.wait_for_timeout(200)
        pg.evaluate("document.getAnimations().forEach(a=>a.pause())")
        for i in range(n):
            ms = i * 1000.0 / FPS
            pg.evaluate("(t)=>document.getAnimations().forEach(a=>a.currentTime=t)", ms)
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
    bg = DEMO / "_grid_bg.mp4"
    print("[bg] building TWO GOATS grid ...")
    build_grid_bg(bg)
    for name, htmlfn in [("A_inkslam", html_inkslam), ("B_chromatic", html_chromatic)]:
        print(f"[render] style {name} (transparent CSS -> frames) ...")
        fdir = DEMO / f"_frames_{name}"
        render_transparent(htmlfn(words), DUR, fdir)
        out = DEMO / f"demo_caption_{name}.mp4"
        composite(bg, fdir, out)
        print(f"  -> {out}")
    print("\n[done] demos in", DEMO)


if __name__ == "__main__":
    main()
