#!/usr/bin/env python
"""EW02 60s POC — stills-gate assembler ($0 ffmpeg Ken Burns push-ins).

Takes the 6 GN 16:9 stills + the 60s audio slice and builds a 1080p look-gate
cut: a gentle reverent slow push-in per still (10s each), concat, muxed with
narration. NO veo spend — this is the look/consistency/sync gate. Score +
captions come after the look is approved.

  .venv\\Scripts\\python.exe longform\\_poc_ew02_assemble.py
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POC = ROOT / "longform" / "EW02_Abraham" / "v1" / "_poc60"
STILLS = POC / "stills"
TMP = POC / "_clips"; TMP.mkdir(parents=True, exist_ok=True)
AUDIO = POC / "poc_60s.mp3"
OUT = POC / "poc_60s_lookgate.mp4"

SECS, FPS = 10, 30
FRAMES = SECS * FPS
ORDER = ["01_abraham_dawn", "02_journey", "03_promise_sky",
         "04_the_command", "05_moriah_afar", "06_heavy_heart"]
# gentle end-zooms; hero (Moriah) gets a touch more
ZMAX = {"05_moriah_afar": 1.16, "06_heavy_heart": 1.14}


def kenburns(still, dest, zmax):
    rate = (zmax - 1.0) / FRAMES
    vf = (f"scale=-2:2160:flags=lanczos,"
          f"zoompan=z='min(1+{rate:.6f}*on,{zmax})':d={FRAMES}:"
          f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={FPS},setsar=1")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(still),
                    "-t", str(SECS), "-r", str(FPS), "-vf", vf,
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium",
                    str(dest)], check=True)


def main():
    clips = []
    for name in ORDER:
        still = STILLS / f"{name}.png"
        if not still.exists():
            raise SystemExit(f"missing still: {still}")
        dest = TMP / f"{name}.mp4"
        kenburns(still, dest, ZMAX.get(name, 1.12))
        clips.append(dest)
        print(f"[clip] {name}")

    lst = TMP / "concat.txt"
    lst.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips), encoding="utf-8")
    silent = POC / "_silent.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(silent)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(AUDIO),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(OUT)], check=True)
    print(f"\nlook-gate cut -> {OUT}")


if __name__ == "__main__":
    main()
