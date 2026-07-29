"""Sin City / 300 noir GRADE demo — 3 spot-colour options (2026-07-22).

Grades two showcase clips (the two-goats altar FIRE = red, the mercy-seat GLOW =
gold) three ways so we can compare the spot-colour intensity in motion:
  1_bold        — full crimson/gold flood on the warm regions (as first tested)
  2_restrained  — only the flame / light source itself keeps colour (the red dress)
  3_purenoir    — stark B&W, no spot colour at all
All share the same stark noir base: crushed blacks, blown highlights, film grain.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_noir_grade_demo.py
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked"
CLIPS = OUT / "clips"
DEMO = OUT / "_trailer" / "_noir_grade_demo"
DEMO.mkdir(parents=True, exist_ok=True)

W, H, FPS, SEG = 1920, 1080, 30, 2.6
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS), "-pix_fmt", "yuv420p"]

SHOWCASE = [11, 8]   # 11 = altar fire (red), 8 = mercy-seat glow (gold)

# stark noir base applied AFTER the spot/gray stage
NOIR_TAIL = ("curves=all='0/0 0.28/0.10 0.72/0.94 1/1',"
             "eq=contrast=1.42:brightness=-0.03,noise=alls=10:allf=t+u")

OPTIONS = {
    "1_bold":       "colorhold=color=0xD9922E:similarity=0.30:blend=0.14",
    "2_restrained": "colorhold=color=0xE8791A:similarity=0.15:blend=0.04,eq=saturation=0.85",
    "3_purenoir":   "format=gray",
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{' '.join(str(c) for c in cmd[:8])}...\n{r.stderr[-1400:]}")


def clip_for(cid):
    return sorted(CLIPS.glob(f"{cid:02d}_*.mp4"))[0]


def main():
    for opt, grade in OPTIONS.items():
        segs = []
        for cid in SHOWCASE:
            seg = DEMO / f"_seg_{opt}_{cid:02d}.mp4"
            vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                  f"{grade},{NOIR_TAIL},fps={FPS},format=yuv420p")
            run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0", "-t", f"{SEG}",
                 "-i", str(clip_for(cid)), "-vf", vf, "-an", *ENC, str(seg)])
            segs.append(seg)
        lst = DEMO / f"_list_{opt}.txt"
        lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
        out = DEMO / f"demo_noir_{opt}.mp4"
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", str(lst), "-c", "copy", str(out)])
        # a still for quick verification
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.2", "-i", str(out),
             "-vframes", "1", str(DEMO / f"chk_{opt}.jpg")])
        print(f"  -> {out}")
    print("[done]", DEMO)


if __name__ == "__main__":
    main()
