#!/usr/bin/env python
"""Frame-exact DOM/CSS animation renderer (Playwright + ffmpeg), $0, no API.

Loads an HTML file with CSS @keyframes / Web Animations, pauses every
animation on load, then for each output frame sets every animation's
currentTime explicitly (deterministic — independent of real-time playback
jitter) and screenshots. This is how professional motion-design tools get
buttery smooth spring/easing curves without hand-rolled frame math.

Usage:
    python render_dom_clip.py clone_typography.html out.mp4 --duration 3.2
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

FPS = 30
W, H = 1920, 1080  # default 16:9 canvas; pass width/height to render() for 9:16 (1080x1920)


def render(html_path: Path, out_mp4: Path, duration_s: float, has_counter: bool = False,
           width: int = W, height: int = H):
    frames_dir = out_mp4.parent / (out_mp4.stem + "_frames")
    if frames_dir.exists():
        shutil.rmtree(frames_dir)
    frames_dir.mkdir(parents=True)

    n_frames = int(duration_s * FPS)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        page.goto(html_path.resolve().as_uri())
        page.wait_for_timeout(150)
        page.evaluate("document.getAnimations().forEach(a => a.pause())")

        for i in range(n_frames):
            t_ms = (i / FPS) * 1000
            page.evaluate(f"document.getAnimations().forEach(a => {{ a.currentTime = {t_ms}; }})")
            if has_counter:
                page.evaluate(f"window.setCounterTime && window.setCounterTime({t_ms})")
            page.screenshot(path=str(frames_dir / f"f{i:05d}.png"))
            if i % 30 == 0:
                print(f"  frame {i}/{n_frames}", flush=True)

        browser.close()

    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
         "-i", str(frames_dir / "f%05d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), str(out_mp4)],
        check=True,
    )
    shutil.rmtree(frames_dir)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("out")
    ap.add_argument("--duration", type=float, default=3.0)
    ap.add_argument("--counter", action="store_true", help="page exposes window.setCounterTime(ms)")
    ap.add_argument("--width", type=int, default=W)
    ap.add_argument("--height", type=int, default=H)
    a = ap.parse_args()
    render(Path(a.html), Path(a.out), a.duration, has_counter=a.counter, width=a.width, height=a.height)
