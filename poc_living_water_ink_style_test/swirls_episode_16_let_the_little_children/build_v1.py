"""Episode 16 "Let the Little Children" - preview film, $0 assembly (ep12 build_v3 pattern).

Voice: words X5 turns (_turns/), 0.4 s pauses around the Jesus line (same timing as
narration.mp3, so narration.alignment.json times hold), Jesus -5.5 dB (take was hotter),
0.15 s fade on the last word. Pictures: 9 Kling clips, cut on whisperx word times.
Slow-down capped at 1.35x, remainder ping-ponged from the clip's own tail. Some clips are
reused as a tighter crop (a different "shot" of the same clip). 3.0 s landing hold.
No score yet (owner to choose). Low priority, 3 threads (gentle mode).
"""
import json, subprocess, sys
from pathlib import Path

EP = Path(__file__).resolve().parent
T, C, TMP = EP / "_turns", EP / "clips", EP / "_build"
OUT_VOICE = TMP / "voice_v1.wav"
OUT = EP / "EP16_PREVIEW_v1.mp4"
THREADS, MAX_SLOW, HOLD, PAUSE = "3", 1.35, 3.0, 0.4
LOW = 0x00004000 if sys.platform == "win32" else 0

# (clip, start, end, clip_in, crop) ; crop = (x, y, w, h) as fractions of the frame, or None
SEGMENTS = [
    ("c01.mp4", 0.0, 7.6, 0.0, None),    # Has someone pushed you away? ... This story is for you.
    ("c02.mp4", 7.6, 15.0, 0.0, None),   # People were bringing young children ... touch them
    ("c03.mp4", 15.0, 20.8, 0.0, None),  # close followers rebuked ... tried to stop them
    ("c04.mp4", 20.8, 27.9, 0.0, None),  # Jesus saw it ... much displeased ... Angry.
    ("c03.mp4", 27.9, 32.5, 1.0, (0.15, 0.08, 0.75, 0.55)),  # With the ones who tried to stop them (tight on the men)
    ("c05.mp4", 32.5, 41.9, 0.0, None),  # JESUS: Suffer the little children ... let them come
    ("c08.mp4", 41.9, 48.0, 0.0, None),  # Do not stop them. God's kingdom belongs to people like these children
    ("c06.mp4", 48.0, 54.0, 0.0, None),  # grown-ups must receive it ... like a little child
    ("c07.mp4", 54.0, 58.3, 0.0, None),  # And here is what He did. "He took them up in his arms,
    ("c08.mp4", 58.3, 62.6, 1.5, (0.10, 0.10, 0.70, 0.55)),  # put his hands upon them, and blessed them (tight)
    ("c02.mp4", 62.6, 65.0, 2.5, (0.0, 0.25, 0.75, 0.6)),   # The people came for a touch.
    ("c07.mp4", 65.0, 68.0, 2.0, (0.10, 0.08, 0.80, 0.6)),  # He gave the children His arms.
    ("c09.mp4", 68.0, None, 0.0, None),  # Someone told you "not now." Look at who Jesus picked up. (+ hold)
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, creationflags=LOW)
    if r.returncode:
        print(r.stderr[-2000:])
        raise SystemExit(f"failed: {' '.join(map(str, cmd[:6]))}")


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def build_voice():
    n0, j1, n2 = T / "00_narrator__atempo.mp3", T / "01_jesus.mp3", T / "02_narrator__atempo.mp3"
    d2 = dur(n2)
    fmt = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
    fc = (f"[0:a]{fmt}[a0];[1:a]{fmt},volume=-5.5dB[a1];"
          f"[2:a]{fmt},afade=t=out:st={d2 - 0.15:.3f}:d=0.15[a2];"
          f"anullsrc=r=44100:cl=stereo,atrim=0:{PAUSE}[p1];anullsrc=r=44100:cl=stereo,atrim=0:{PAUSE}[p2];"
          f"[a0][p1][a1][p2][a2]concat=n=5:v=0:a=1[v]")
    run(["ffmpeg", "-y", "-hide_banner", "-i", str(n0), "-i", str(j1), "-i", str(n2),
         "-filter_complex", fc, "-map", "[v]", str(OUT_VOICE)])
    return dur(OUT_VOICE)


def build_segment(i, clip, start, end, cin, crop):
    src = C / clip
    L = dur(src) - 0.05 - cin
    D = end - start
    out = TMP / f"seg{i:02d}.mp4"
    cr = f"crop=iw*{crop[2]}:ih*{crop[3]}:iw*{crop[0]}:ih*{crop[1]}," if crop else ""
    norm = f"{cr}scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p"
    if D <= L:
        fc, info = f"[0:v]trim=0:{D:.3f},setpts=PTS-STARTPTS,{norm}[v]", "1.00x"
    else:
        f = min(MAX_SLOW, D / L)
        rem = D - L * f
        if rem <= 0.02:
            fc, info = f"[0:v]trim=0:{L:.3f},setpts={f:.4f}*(PTS-STARTPTS),{norm},trim=0:{D:.3f}[v]", f"{f:.2f}x"
        else:
            tail = min(rem / f, L)
            fc = (f"[0:v]split[a0][b0];"
                  f"[a0]trim=0:{L:.3f},setpts={f:.4f}*(PTS-STARTPTS),{norm}[a];"
                  f"[b0]trim={L - tail:.3f}:{L:.3f},setpts=PTS-STARTPTS,reverse,setpts={f:.4f}*PTS,{norm}[b];"
                  f"[a][b]concat=n=2:v=1:a=0,trim=0:{D:.3f}[v]")
            info = f"{f:.2f}x + {rem:.2f}s ping-pong"
    run(["ffmpeg", "-y", "-hide_banner", "-threads", THREADS, "-ss", f"{cin:.3f}", "-i", str(src), "-filter_complex", fc,
         "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-threads", THREADS, str(out)])
    print(f"seg{i:02d} {clip} {start:6.2f}-{end:6.2f} ({D:.2f}s) {info}{' crop' if crop else ''}")
    return out


def main():
    TMP.mkdir(exist_ok=True)
    vlen = build_voice()
    total = vlen + HOLD
    segs = [build_segment(i, c, s, e if e is not None else total, ci, cr) for i, (c, s, e, ci, cr) in enumerate(SEGMENTS)]
    lst = TMP / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
    run(["ffmpeg", "-y", "-hide_banner", "-threads", THREADS, "-f", "concat", "-safe", "0", "-i", str(lst),
         "-i", str(OUT_VOICE), "-filter_complex", f"[1:a]apad=whole_dur={total:.3f}[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(OUT)])
    print(json.dumps({"out": str(OUT), "voice_s": vlen, "total_s": total, "result_s": dur(OUT)}))


if __name__ == "__main__":
    main()
