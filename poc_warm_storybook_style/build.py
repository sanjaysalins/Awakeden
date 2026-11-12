"""Mary and Martha (Warm Storybook POC) - voice-only preview cut, $0 assembly.

Copied from ep16 build_v3.py. Owner rule: no ping-pong/freeze/zoom fill. 15 Kling v3 pro clips,
each LONGER than its slot, played at 1.0x from frame 0, hard cuts on the PICTURE_PLAN slots
(whisperx word times). Fails loudly if any clip is shorter than its slot.
Voice = locked narration.mp3 (82.13 s) + 0.3 s tail fade (ep12 click lesson). 3.0 s landing hold.
Low priority, 3 threads (gentle mode). Music comes later (separate quote).
"""
import json, subprocess, sys
from pathlib import Path

EP = Path(__file__).resolve().parent
C, TMP = EP / "clips", EP / "_build"
VOICE_IN, OUT_VOICE = EP / "narration.mp3", TMP / "voice.wav"
OUT = EP / "MARY_MARTHA_PREVIEW_v1.mp4"
THREADS, HOLD, FADE = "3", 3.0, 0.3
LOW = 0x00004000 if sys.platform == "win32" else 0

# (clip, start, end) on the final timeline; end None = to the end of the hold
SHOTS = [
    ("s01.mp4", 0.0, 5.4),    # You do everything... Does anyone even care?
    ("s02.mp4", 5.4, 10.0),   # A tired woman once asked Jesus that. Her name was Martha.
    ("s03.mp4", 10.0, 14.4),  # She had opened her home to Him.
    ("s04.mp4", 14.4, 18.2),  # her sister Mary sat at His feet and listened.
    ("s05.mp4", 18.2, 25.8),  # MARTHA: Lord, dost thou not care... help me.
    ("s06.mp4", 25.8, 30.8),  # His first words? Her name.
    ("s07.mp4", 30.8, 36.8),  # JESUS: Martha, Martha... Twice.
    ("s08.mp4", 36.8, 42.2),  # careful and troubled about many things... one thing is needful
    ("s09.mp4", 42.2, 46.6),  # Mary hath chosen that good part...
    ("s10.mp4", 46.6, 52.4),  # "Careful" means full of worry. Not another job.
    ("s11.mp4", 52.4, 59.6),  # It was Him. Mary chose to stay close...
    ("s12.mp4", 59.6, 64.4),  # He never called Martha's work wrong. He named her worry.
    ("s13.mp4", 64.4, 69.2),  # So, did He care? Later, the Bible says it plainly,
    ("s14.mp4", 69.2, 76.6),  # "Now Jesus loved Martha, and her sister, and Lazarus."
    ("s15.mp4", 76.6, None),  # She felt left to serve alone. But Jesus was right there... (+ hold)
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
    d = dur(VOICE_IN)
    af = (f"aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,"
          f"afade=t=out:st={d - FADE:.3f}:d={FADE}")
    run(["ffmpeg", "-y", "-hide_banner", "-i", str(VOICE_IN), "-af", af, str(OUT_VOICE)])
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
