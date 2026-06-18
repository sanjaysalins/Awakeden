"""Deterministic VIRAL crop-cut clip from ONE still — hard cuts + punch-ins on the
REAL pixels (zero hallucination, $0). Test vs direct-Kling / HF-Kling.

Each framing = a crop window (zoom Z, center cx,cy in [0,1]) on a 1080x1920 base
canvas, with a subtle continuous push within the framing; HARD cuts between framings
= the viral edit feel. No model ever repaints anything, so a hand can never grow a
sixth finger — worst case is a slightly soft crop, always faithful."""
import subprocess, sys, tempfile, os
from pathlib import Path

W, H, FPS = 1080, 1920, 30

# (label, Z_start, Z_end, cx, cy, dur_s) — full->mid->detail->detail->side->full
FRAMINGS = [
    ("full",   1.02, 1.08, 0.50, 0.45, 0.80),
    ("mid",    1.26, 1.34, 0.50, 0.42, 0.70),
    ("upper",  1.70, 1.80, 0.50, 0.30, 0.60),
    ("lower",  1.92, 2.00, 0.55, 0.62, 0.60),
    ("side",   1.48, 1.56, 0.35, 0.50, 0.60),
    ("back",   1.16, 1.00, 0.50, 0.45, 0.95),
]

def seg(png, fr, out):
    label, z0, z1, cx, cy, dur = fr
    d = max(2, int(round(dur * FPS)))
    base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
    zexpr = f"{z0}+({z1}-{z0})*on/{d-1}"
    zp = (f"zoompan=z='{zexpr}'"
          f":x='(iw-iw/zoom)*{cx}':y='(ih-ih/zoom)*{cy}'"
          f":d={d}:s={W}x{H}:fps={FPS}")
    vf = f"{base},{zp},format=yuv420p"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(png),
                    "-vf", vf, "-t", f"{dur}", "-r", str(FPS),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)], check=True)

def build(png, out_mp4):
    png = Path(png)
    tmp = Path(tempfile.mkdtemp())
    parts = []
    for i, fr in enumerate(FRAMINGS):
        p = tmp / f"s{i}.mp4"
        seg(png, fr, p)
        parts.append(p)
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-r", str(FPS), str(out_mp4)], check=True)
    for p in parts: os.remove(p)
    os.remove(lst); os.rmdir(tmp)
    print("SAVED", out_mp4)

if __name__ == "__main__":
    OUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\_hf_test")
    OUT.mkdir(exist_ok=True)
    B = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross\v1\shorts")
    jobs = [
        (B / "04_Declared_To_The_Brethren/visual/nbp/09_the-wounded-hand-on-the-shoulder.png", OUT / "04_09_hand_FFMPEG.mp4"),
        (B / "06_The_Ends_Of_The_Earth/visual/nbp/01_one-man-alone.png", OUT / "06_01_face_FFMPEG.mp4"),
    ]
    for png, out in jobs:
        build(png, out)
