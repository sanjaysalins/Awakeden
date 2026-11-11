"""Episode 16 "Let the Little Children" - v2 high-production cut, $0 assembly.

Owner (2026-11-11): no backwards/ping-pong, no freeze, no crop-zoom reuse. So: 17 shots,
each a Kling v3 PRO clip rendered LONGER than its slot, played at 1.0x from its first frame,
hard cuts on whisperx word times. Fails loudly if any clip is shorter than its slot.
Voice as v1 (Jesus -5.5 dB, 0.4 s pauses, last-word fade). 3.0 s landing hold.
Low priority, 3 threads (gentle mode).
"""
import json, subprocess, sys
from pathlib import Path

EP = Path(__file__).resolve().parent
T, C, TMP = EP / "_turns", EP / "v2" / "clips", EP / "_build_v2"
OUT_VOICE = TMP / "voice.wav"
OUT = EP / "EP16_PREVIEW_v2.mp4"
THREADS, HOLD, PAUSE = "3", 3.0, 0.4
LOW = 0x00004000 if sys.platform == "win32" else 0

# (clip, start, end) on the final timeline; end None = to the end of the hold
SHOTS = [
    ("sA.mp4", 0.0, 2.6),    # Has someone pushed you away?
    ("p01.mp4", 2.6, 7.6),   # Told you "not now"? This story is for you.
    ("p02.mp4", 7.6, 10.5),  # People were bringing young children to Jesus.
    ("sB.mp4", 10.5, 15.0),  # They wanted one thing: "that he should touch them."
    ("p03.mp4", 15.0, 20.8), # close followers "rebuked ..." They tried to stop them.
    ("sC.mp4", 20.8, 23.6),  # Then Jesus saw it. And the Bible says
    ("p04.mp4", 23.6, 27.9), # He was "much displeased." Angry.
    ("sD.mp4", 27.9, 32.5),  # Not with the children. With the ones who tried to stop them.
    ("p05.mp4", 32.5, 38.6), # JESUS: Suffer the little children ...
    ("sE.mp4", 38.6, 43.5),  # In plain words: let them come. Do not stop them.
    ("sF.mp4", 43.5, 47.9),  # God's kingdom belongs to people like these children.
    ("p06.mp4", 47.9, 53.8), # grown-ups must receive it the same way: like a little child.
    ("p07.mp4", 53.8, 58.2), # And here is what He did. "He took them up in his arms,
    ("p08.mp4", 58.2, 62.6), # put his hands upon them, and blessed them."
    ("sG.mp4", 62.6, 65.0),  # The people came for a touch.
    ("sH.mp4", 65.0, 68.0),  # He gave the children His arms.
    ("p09.mp4", 68.0, None), # Someone told you "not now." Look at who Jesus picked up. (+ hold)
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


def main():
    TMP.mkdir(exist_ok=True)
    vlen = build_voice()
    total = vlen + HOLD
    short = [(c, round(dur(C / c), 2), round((e or total) - s, 2)) for c, s, e in SHOTS if dur(C / c) - 0.02 < (e or total) - s]
    if short:
        raise SystemExit(f"clip shorter than its slot (no ping-pong allowed): {short}")
    segs = []
    for i, (c, s, e) in enumerate(SHOTS):
        D = (e or total) - s
        out = TMP / f"seg{i:02d}.mp4"
        vf = f"trim=0:{D:.3f},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p"
        run(["ffmpeg", "-y", "-hide_banner", "-threads", THREADS, "-i", str(C / c), "-vf", vf, "-an",
             "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-threads", THREADS, str(out)])
        print(f"seg{i:02d} {c:8s} {s:6.2f}-{s + D:6.2f} ({D:.2f}s of {dur(C / c):.2f}s) 1.00x")
        segs.append(out)
    lst = TMP / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
    run(["ffmpeg", "-y", "-hide_banner", "-threads", THREADS, "-f", "concat", "-safe", "0", "-i", str(lst),
         "-i", str(OUT_VOICE), "-filter_complex", f"[1:a]apad=whole_dur={total:.3f}[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(OUT)])
    print(json.dumps({"out": str(OUT), "voice_s": vlen, "total_s": total, "result_s": dur(OUT)}))


if __name__ == "__main__":
    main()
