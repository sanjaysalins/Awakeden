"""Episode 12 v3 (retro style) - preview film, $0 assembly.

Voice: words v2 turns (_turns/), with a 0.5 s pause after the Jesus line and a
0.15 s fade on the last word (the raw take ends with 'towel' still sounding).
Pictures: 11 Kling clips (clips/c01..c11), cut on the real word timings
(whisper, +0.5 s after the Jesus turn). Slow-down capped at 1.35x, any remainder
ping-ponged from the clip's own tail (never a held still). 3.0 s landing hold.
Score: the episode's own felt-piano score (score_piano.mp3), ducked under the voice.
Low priority, 3 threads (gentle mode).
"""
import subprocess, sys, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
T = EP / "_turns"
TMP = HERE / "_build"
OUT_VOICE = TMP / "voice_v3.wav"
OUT_NOSCORE = TMP / "preview_noscore.mp4"
OUT = HERE / "EP12_RETRO_PREVIEW.mp4"
SCORE = EP / "score_arpeggiated_ostinato.mp3"  # owner-supplied 2026-11-10, used from its start
THREADS = "3"
MAX_SLOW = 1.35
PAUSE_AFTER_JESUS = 0.5
HOLD = 3.0
LOW = 0x00004000 if sys.platform == "win32" else 0

# (clip, start, end) on the final timeline (seconds)
SEGMENTS = [
    ("c01.mp4", 0.0, 5.6),     # If people really knew me...
    ("c02.mp4", 5.6, 11.0),    # Jesus at supper. He knew them.
    ("c03.mp4", 11.0, 19.6),   # Judas ... Peter ...
    ("c04.mp4", 19.6, 27.1),   # So what does He do ... ties a towel
    ("c05.mp4", 27.1, 33.7),   # pours water, washes their feet
    ("c06.mp4", 33.7, 38.6),   # Judas is still in the room / Know ye...
    ("c07.mp4", 38.6, 48.3),   # loved them unto the end ... the cross
    ("c08.mp4", 48.3, 56.2),   # Judas walks out ... and it was night
    ("c09.mp4", 56.2, 63.2),   # Maybe it is night where you are ...
    ("c10.mp4", 63.2, 66.3),   # Jesus knows. All of it.
    ("c11.mp4", 66.3, None),   # The one who knew ... holding the towel (+ hold)
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, creationflags=LOW)
    if r.returncode:
        print(r.stderr[-2000:])
        raise SystemExit(f"failed: {' '.join(map(str, cmd[:6]))}")


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def build_voice():
    n0, j1, n2 = T / "00_narrator__atempo.mp3", T / "01_jesus.mp3", T / "02_narrator__atempo.mp3"
    d2 = dur(n2)
    fmt = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
    fc = (f"[0:a]{fmt}[a0];[1:a]{fmt},volume=-7dB[a1];"  # Jesus take was 8 dB hotter than narrator
          f"[2:a]{fmt},afade=t=out:st={d2 - 0.15:.3f}:d=0.15[a2];"
          f"anullsrc=r=44100:cl=stereo,atrim=0:{PAUSE_AFTER_JESUS}[p];"
          f"[a0][a1][p][a2]concat=n=4:v=0:a=1[v]")
    run(["ffmpeg", "-y", "-hide_banner", "-i", str(n0), "-i", str(j1), "-i", str(n2),
         "-filter_complex", fc, "-map", "[v]", str(OUT_VOICE)])
    return dur(OUT_VOICE)


def build_segment(i, clip, start, end):
    src = HERE / "clips" / clip
    L = dur(src) - 0.05
    D = end - start
    out = TMP / f"seg{i:02d}.mp4"
    norm = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p"
    if D <= L:
        fc = f"[0:v]trim=0:{D:.3f},setpts=PTS-STARTPTS,{norm}[v]"
        info = "1.00x"
    else:
        f = min(MAX_SLOW, D / L)
        rem = D - L * f
        if rem <= 0.02:
            fc = f"[0:v]trim=0:{L:.3f},setpts={f:.4f}*(PTS-STARTPTS),{norm},trim=0:{D:.3f}[v]"
            info = f"{f:.2f}x"
        else:
            tail = rem / f
            fc = (f"[0:v]split[a0][b0];"
                  f"[a0]trim=0:{L:.3f},setpts={f:.4f}*(PTS-STARTPTS),{norm}[a];"
                  f"[b0]trim={L - tail:.3f}:{L:.3f},setpts=PTS-STARTPTS,reverse,setpts={f:.4f}*PTS,{norm}[b];"
                  f"[a][b]concat=n=2:v=1:a=0,trim=0:{D:.3f}[v]")
            info = f"{f:.2f}x + {rem:.2f}s ping-pong"
    run(["ffmpeg", "-y", "-hide_banner", "-threads", THREADS, "-i", str(src), "-filter_complex", fc,
         "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-threads", THREADS, str(out)])
    print(f"seg{i:02d} {clip} {start:6.2f}-{end:6.2f} ({D:.2f}s) {info}")
    return out


def main():
    TMP.mkdir(exist_ok=True)
    vlen = build_voice()
    total = max(vlen + HOLD, dur(SCORE) - 0.05)  # let the owner's score finish on its own ending
    segs = [build_segment(i, c, s, e if e is not None else total) for i, (c, s, e) in enumerate(SEGMENTS)]
    lst = TMP / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
    run(["ffmpeg", "-y", "-hide_banner", "-threads", THREADS, "-f", "concat", "-safe", "0", "-i", str(lst),
         "-i", str(OUT_VOICE), "-filter_complex", f"[1:a]apad=whole_dur={total:.3f}[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(OUT_NOSCORE)])
    afmt = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
    fc = (f"[1:a]{afmt},atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume=-10dB,"
          f"afade=t=out:st={total - 1.5:.3f}:d=1.5,apad=whole_dur={total:.3f}[mus];"
          f"[0:a]{afmt},asplit=2[main][key];"
          f"[mus][key]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[musd];"
          f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]")
    run(["ffmpeg", "-y", "-hide_banner", "-threads", THREADS, "-i", str(OUT_NOSCORE), "-i", str(SCORE),
         "-filter_complex", fc, "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(OUT)])
    print(json.dumps({"out": str(OUT), "voice_s": vlen, "total_s": total, "result_s": dur(OUT)}))


if __name__ == "__main__":
    main()
