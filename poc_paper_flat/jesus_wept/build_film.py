"""Jesus Wept paper-flat POC film: 13 clips timed to the recorded narration, Barabbas-style pills, soft ducked score,
3 s landing hold, loudness -14. $0. Gentle: ffmpeg -threads 2.
  .venv\\Scripts\\python.exe poc_paper_flat/jesus_wept/build_film.py"""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "poc_comic_page" / "_ELEVATE"))
import build_tp as T  # noqa: E402
import build_w3 as W  # noqa: E402

CL = HERE / "clips"; NAR = HERE / "audio" / "narration.mp3"
SL = T.ROOT / "sound_library" / "clips"
WORK = HERE / "_work"; WORK.mkdir(exist_ok=True)
OUT = HERE / "JESUS_WEPT_POC.mp4"
TOTAL = 69.0  # 65.96 s narration + ~3 s landing hold

# (clip, slot_start, slot_end) — slot edges from the whisper word alignment (audio/narration.alignment.json)
SLOTS = [("s01", 0.0, 6.25), ("s02", 6.25, 13.6), ("s03", 13.6, 18.1), ("s04", 18.1, 25.3), ("s05", 25.3, 32.5),
         ("s06", 32.5, 39.3), ("s07", 39.3, 42.3), ("s08", 42.3, 44.7), ("s09", 44.7, 48.6), ("s10", 48.6, 54.05),
         ("s11", 54.05, 58.1), ("s12", 58.1, 61.5), ("s13", 61.5, TOTAL)]

# (t0, t1, text, who, ref, jesus_pill, pos)  pos: top/bot — chosen per shot so the box never covers a face or hands (owner 2026-11-10)
PL = [(0.0, 6.2, 'You said it to God, alone: "If You had been here, they would not have died."', None, None, False, "bot"),
      (6.3, 8.8, "Two sisters said that same sentence to Jesus.", None, None, False, "top"),
      (9.0, 13.5, "Their brother Lazarus, Jesus's friend, had been in the grave four days.", None, None, False, "top"),
      (13.8, 18.0, "Lord, if thou hadst been here, my brother had not died.", "MARTHA", "JOHN 11:21", False, "bot"),
      (18.3, 21.7, "Her sister Mary stayed in the house, until Martha whispered:", None, None, False, "bot"),
      (21.9, 25.2, "The Master is come, and calleth for thee.", "MARTHA", "JOHN 11:28", False, "bot"),
      (25.4, 27.9, "He was asking for the one who stayed behind.", None, None, False, "top"),
      (28.1, 32.4, "Lord, if thou hadst been here, my brother had not died.", "MARY", "JOHN 11:32", False, "top"),
      (32.7, 35.2, "He did not argue. He asked:", None, None, False, "top"),
      (35.4, 37.3, "Where have ye laid him?", "JESUS", "JOHN 11:34", True, "top"),
      (37.5, 39.2, "Lord, come and see.", "MOURNERS", "JOHN 11:34", False, "top"),
      (39.4, 42.2, "Jesus wept.", None, "JOHN 11:35", False, "bot"),
      (42.3, 44.7, "Behold how he loved him!", "MOURNERS", "JOHN 11:36", False, "bot"),
      (44.9, 48.4, "Then He called Lazarus out of the grave, alive.", None, None, False, "top"),
      (49.4, 54.0, "He gave a dead man life, so the leaders planned to kill Him.", None, "JOHN 11:53", False, "bot"),
      (54.1, 56.0, "He did not only cry at a grave.", None, None, False, "bot"),
      (56.2, 60.4, "He died on a cross for us, was laid in a grave, and rose.", None, None, False, "bot"),
      (61.6, 63.9, "The Jesus who wept is alive.", None, None, True, "bot"),
      (64.7, 68.0, "Say it to Him.", None, None, True, "bot")]


def run(cmd): subprocess.run([str(c) for c in cmd], check=True)


def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode())


def base(out):
    ins, fc = [], ""
    for i, (k, a, b) in enumerate(SLOTS):
        f = CL / f"{k}.mp4"; d = dur(f) - 0.05; slot = b - a
        if slot <= d:
            t1, sp = slot, 1.0
        else:
            t1, sp = d, slot / d
        ins += ["-i", f]
        fc += (f"[{i}:v]trim=0:{t1:.3f},setpts=PTS-STARTPTS,setpts=PTS*{sp:.4f},scale=1080:1920:flags=lanczos,fps=30,"
               f"trim=0:{slot:.3f},setsar=1[v{i}];")
    fc += "".join(f"[v{i}]" for i in range(len(SLOTS))) + f"concat=n={len(SLOTS)}:v=1:a=0,tpad=stop_mode=clone:stop_duration=1[o]"
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", *ins, "-filter_complex", fc, "-map", "[o]", "-t", f"{TOTAL:.2f}",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", out])


def mix(out):
    fc = f"""
[0:a]apad=whole_dur={TOTAL},asplit=2[nar][key];
[1:a]atrim=0:{TOTAL},afade=t=in:st=0:d=1.5,afade=t=out:st={TOTAL-4.5}:d=4.5,volume=-13dB,apad=whole_dur={TOTAL}[sc];
[2:a]afade=t=in:st=0:d=2,volume=2dB,adelay=60300|60300,afade=t=out:st={TOTAL-3.5}:d=3.5,apad=whole_dur={TOTAL},atrim=0:{TOTAL}[ch];
[sc][ch]amix=inputs=2:normalize=0:duration=longest[bed];
[bed][key]sidechaincompress=threshold=0.02:ratio=5:attack=40:release=600[duck];
[nar][duck]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.85:level=disabled,atrim=0:{TOTAL}[a]"""
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", "-i", NAR, "-i", SL / "score_reverent_grace.mp3",
         "-i", SL / "heavenly_choir_soft.mp3", "-filter_complex", fc, "-map", "[a]", "-c:a", "pcm_s16le", out])


YOFF = {"top": -780, "bot": 330}  # pill drawn at y=1000; top -> y220 (below Shorts top icons), bot -> y1330 (above the Shorts title/buttons zone)


def letter(basev, audio, out):
    d = WORK / "pills"; d.mkdir(exist_ok=True); ov = []
    for i, (a, b, text, who, ref, j, pos) in enumerate(PL):
        p = d / f"p{i:02d}.png"; W.pill_tabs(p, text, who, ref, jesus=j); ov.append((str(p), a, b, YOFF[pos]))
    h = d / "hook.png"; T.light_text(h, "IF YOU HAD BEEN HERE...", 330, size=104, maxw=900); ov.append((str(h), 0.0, 3.2, 0))
    ins = ["-i", basev]; fc = ""; prev = "[0:v]"; loop = ["-loop", "1", "-framerate", "30", "-t", f"{TOTAL:.2f}"]
    for i, (png, t0, t1, yo) in enumerate(ov):
        ins += loop + ["-i", png]; n = i + 1
        fc += (f"[{n}:v]format=rgba,fade=in:st={t0:.2f}:d=0.12:alpha=1,fade=out:st={max(t0, t1-0.12):.2f}:d=0.12:alpha=1[o{i}];"
               f"{prev}[o{i}]overlay=0:{yo}:eof_action=pass:enable='between(t,{t0:.2f},{t1:.2f})'[p{i}];")
        prev = f"[p{i}]"
    fc += prev + "null[out]"
    na = len(ov) + 1
    # loudness: one-pass-measured gain is done after; here encode AAC at the mix level
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", *ins, "-i", audio, "-filter_complex", fc, "-map", "[out]", "-map", f"{na}:a",
         "-t", f"{TOTAL:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out])


if __name__ == "__main__":
    b = WORK / "base.mp4"; a = WORK / "mix.wav"
    base(b); mix(a); letter(b, a, OUT); print("built", OUT)
