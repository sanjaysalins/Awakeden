"""Talitha Cumi vector POC - preview v2 (freeze fix, 2026-11-10).

Every segment is a real moving clip: speed-slow capped at MAX_SLOW, any remainder
filled by ping-ponging the clip's own tail (never a held still frame).
Adds the 3.0 s landing hold (INV-26) with audio padded to the same length.
Runs ffmpeg at low priority with a capped thread count (gentle mode).
"""
import subprocess, sys, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
NARR = HERE.parent / "short_g5" / "narration.mp3"
OUT = HERE / "TALITHA_PREVIEW_G5_v2.mp4"
TMP = HERE / "_build_v2"
THREADS = "3"
MAX_SLOW = 1.35
HOLD = 3.0
NARR_END = 50.843

# (clip, start, end) - cut points on real pauses in short_g5/narration.mp3
SEGMENTS = [
    ("c1_plea.mp4", 0.0, 5.5),
    ("c2_news.mp4", 5.5, 13.6),
    ("c3_walk.mp4", 13.6, 20.2),
    ("c4_hand.mp4", 20.2, 25.3),
    ("c4c_arise.mp4", 25.3, 32.3),
    ("c5_rise.mp4", 32.3, 37.6),
    ("c6_family.mp4", 37.6, 43.1),
    ("c7_believe.mp4", 43.1, NARR_END + HOLD),
]

LOW = 0x00004000 if sys.platform == "win32" else 0  # BELOW_NORMAL_PRIORITY_CLASS


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, creationflags=LOW)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        raise SystemExit(f"ffmpeg failed: {' '.join(cmd[:6])}...")


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def build_segment(i, clip, start, end):
    src = HERE / "clips" / clip
    L = dur(src) - 0.05
    D = end - start
    out = TMP / f"seg{i:02d}.mp4"
    norm = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p"
    if D <= L:  # enough footage: play at 1x, trim
        fc = f"[0:v]trim=0:{D:.3f},setpts=PTS-STARTPTS,{norm}[v]"
        info = "1.00x"
    else:
        f = min(MAX_SLOW, D / L)
        played = L * f
        rem = D - played
        if rem <= 0.02:
            fc = f"[0:v]trim=0:{L:.3f},setpts={f:.4f}*(PTS-STARTPTS),{norm},trim=0:{D:.3f}[v]"
            info = f"{f:.2f}x"
        else:
            tail = rem / f
            fc = (f"[0:v]split[a0][b0];"
                  f"[a0]trim=0:{L:.3f},setpts={f:.4f}*(PTS-STARTPTS),{norm}[a];"
                  f"[b0]trim={L - tail:.3f}:{L:.3f},setpts=PTS-STARTPTS,reverse,"
                  f"setpts={f:.4f}*PTS,{norm}[b];"
                  f"[a][b]concat=n=2:v=1:a=0,trim=0:{D:.3f}[v]")
            info = f"{f:.2f}x + {rem:.2f}s ping-pong"
    run(["ffmpeg", "-y", "-hide_banner", "-threads", THREADS, "-i", str(src),
         "-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "medium",
         "-crf", "18", "-threads", THREADS, str(out)])
    print(f"seg{i:02d} {clip:16s} {start:6.2f}-{end:6.2f} ({D:.2f}s) {info}")
    return out


def main():
    TMP.mkdir(exist_ok=True)
    segs = [build_segment(i, *s) for i, s in enumerate(SEGMENTS)]
    lst = TMP / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
    total = SEGMENTS[-1][2]
    run(["ffmpeg", "-y", "-hide_banner", "-threads", THREADS,
         "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(NARR),
         "-filter_complex", f"[1:a]apad=whole_dur={total:.3f}[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(OUT)])
    print(json.dumps({"out": str(OUT), "video_s": dur(OUT), "target_s": total}))


if __name__ == "__main__":
    main()
