"""Zacchaeus scratchy-ink film: 14 clips TRIMMED ONLY (owner rule: no freeze / boomerang / zoom / slow-mo), 1 s pause after
"Jesus went anyway.", pills (Barabbas/Jesus Wept style), soft ducked score, 3 s landing hold, loudness -14. $0. Gentle: -threads 3.
  ..\..\.venv\Scripts\python.exe build_film.py"""
import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "poc_comic_page" / "_ELEVATE"))
import build_tp as T  # noqa: E402
import build_w3 as W  # noqa: E402
CL = HERE/"clips"; NAR = HERE/"audio"/"narration.mp3"; SL = T.ROOT/"sound_library"/"clips"
WORK = HERE/"_work"; WORK.mkdir(exist_ok=True); OUT = HERE/"ZACCHAEUS_POC.mp4"
PAUSE_AT, PAUSE = 39.15, 1.0          # original-narration time of the inserted pause (after "anyway.", word end 39.09)
NAR_LEN = 81.22
TOTAL = NAR_LEN + PAUSE + 3.0          # 3 s landing hold after "third day." (ends 81.16)
def sh(t): return t + PAUSE if t >= PAUSE_AT else t   # original -> film time
# (clip, start, end) in ORIGINAL narration time (alignment.json); c07 end includes the pause, c14 the hold
B = [0.0, 5.70, 12.30, 17.30, 21.30, 27.33, 33.15, 39.15, 43.50, 47.82, 54.00, 61.33, 69.95, 75.90]
CLIPS = [f"c{i:02d}" for i in range(1, 15)]
def slots():
    out = []
    for i, k in enumerate(CLIPS):
        a = sh(B[i]); b = sh(B[i+1]) if i+1 < len(B) else TOTAL
        if k == "c07": b = sh(B[i+1])            # = 39.15 + 1.0 (pause belongs to c07)
        out.append((k, a, b))
    return out
# (t0, t1 ORIGINAL time, text, who, ref, jesus_pill, pos)
PL = [(0.10, 3.40, "A man climbed a tree to see Jesus.", None, None, False, "bot"),
      (3.45, 5.65, "But Jesus was looking for him.", None, None, True, "bot"),
      (5.75, 8.30, "Zacchaeus was a chief tax collector at Jericho.", None, "LUKE 19:2", False, "top"),
      (8.80, 12.10, "Tax men often took extra money from their own people.", None, None, False, "top"),
      (12.15, 17.25, "He was rich, and called a sinner. He was too short to see over the crowd.", None, "LUKE 19:3", False, "top"),
      (17.30, 20.90, "Jesus came by, looked up, and called him by name.", None, None, False, "bot"),
      (21.30, 27.30, "Zacchaeus, make haste, and come down; for to day I must abide at thy house.", "JESUS", "LUKE 19:5", True, "bot"),
      (27.35, 29.45, "Jesus must stay at his house today!", None, None, False, "bot"),
      (31.10, 33.10, "Zacchaeus hurried down, full of joy.", None, "LUKE 19:6", False, "bot"),
      (33.15, 36.50, "The crowd grumbled: Jesus is going to a sinner's house!", None, "LUKE 19:7", False, "bot"),
      (37.95, 39.12, "Jesus went anyway.", None, None, False, "bot"),
      (39.20, 40.60, "Jesus came to him first.", None, None, True, "top"),
      (41.65, 43.30, "Then Zacchaeus stood up and said:", None, None, False, "top"),
      (43.55, 47.80, "Behold, Lord, the half of my goods I give to the poor.", "ZACCHAEUS", "LUKE 19:8", False, "top"),
      (47.85, 49.05, "Half of all he had.", None, None, False, "bot"),
      (49.10, 53.60, "And if he had cheated anyone, he would pay back four times.", None, "LUKE 19:8", False, "bot"),
      (54.05, 57.45, "This day is salvation come to this house.", "JESUS", "LUKE 19:9", True, "bot"),
      (57.80, 61.30, "Salvation means God rescues you and brings you back to Him.", None, None, False, "bot"),
      (61.35, 64.55, "Jesus, the Son of man, said why He came:", None, None, False, "bot"),
      (64.95, 69.95, "For the Son of man is come to seek and to save that which was lost.", "JESUS", "LUKE 19:10", True, "bot"),
      (70.00, 73.40, "Zacchaeus came to look. Jesus came to find him.", None, None, True, "bot"),
      (74.35, 75.80, "He still looks for the lost.", None, None, True, "bot"),
      (76.20, NAR_LEN + 2.8, "To save them, He later died for our sins, and rose again on the third day.", None, "1 COR 15:3-4", True, "top")]
def run(cmd): subprocess.run([str(c) for c in cmd], check=True)
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).decode())
def base(out):
    ins, fc, S = [], "", slots()
    for i, (k, a, b) in enumerate(S):
        f = CL/f"{k}.mp4"; slot = b - a; d = dur(f)
        if slot > d - 0.02: raise SystemExit(f"{k}: slot {slot:.2f}s > clip {d:.2f}s (owner rule: trim only)")
        ins += ["-i", f]
        fc += f"[{i}:v]trim=0:{slot:.3f},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30,setsar=1[v{i}];"
        print(f"{k} {a:6.2f}-{b:6.2f} slot {slot:.2f} / clip {d:.2f}")
    fc += "".join(f"[v{i}]" for i in range(len(S))) + f"concat=n={len(S)}:v=1:a=0[o]"
    run(["ffmpeg","-y","-v","error","-threads","3",*ins,"-filter_complex",fc,"-map","[o]","-t",f"{TOTAL:.2f}",
         "-c:v","libx264","-preset","veryfast","-crf","17","-pix_fmt","yuv420p",out])
def mix(out):
    land = sh(76.2)
    fc = f"""
[0:a]atrim=0:{PAUSE_AT},asetpts=PTS-STARTPTS[n1];[0:a]atrim={PAUSE_AT},asetpts=PTS-STARTPTS[n2];
anullsrc=r=44100:cl=mono,atrim=0:{PAUSE}[gap];[n1]aresample=44100,aformat=channel_layouts=mono[m1];[n2]aresample=44100,aformat=channel_layouts=mono[m2];
[m1][gap][m2]concat=n=3:v=0:a=1,apad=whole_dur={TOTAL},asplit=2[nar][key];
[1:a]atrim=0:{TOTAL},afade=t=in:st=0:d=1.5,afade=t=out:st={TOTAL-4.5}:d=4.5,volume=-13dB,apad=whole_dur={TOTAL}[sc];
[2:a]afade=t=in:st=0:d=2,volume=2dB,adelay={int(land*1000)}|{int(land*1000)},afade=t=out:st={TOTAL-3.5}:d=3.5,apad=whole_dur={TOTAL},atrim=0:{TOTAL}[ch];
[sc][ch]amix=inputs=2:normalize=0:duration=longest[bed];
[bed][key]sidechaincompress=threshold=0.02:ratio=5:attack=40:release=600[duck];
[nar][duck]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.85:level=disabled,atrim=0:{TOTAL}[a]"""
    run(["ffmpeg","-y","-v","error","-threads","3","-i",NAR,"-i",SL/"score_reverent_grace.mp3","-i",SL/"heavenly_choir_soft.mp3",
         "-filter_complex",fc,"-map","[a]","-c:a","pcm_s16le",out])
YOFF = {"top": -780, "bot": 330}
def letter(basev, audio, out):
    d = WORK/"pills"; d.mkdir(exist_ok=True); ov = []
    for i, (a, b, text, who, ref, j, pos) in enumerate(PL):
        p = d/f"p{i:02d}.png"; W.pill_tabs(p, text, who, ref, jesus=j); ov.append((str(p), sh(a), min(sh(b), TOTAL-0.05), YOFF[pos]))
    h = d/"hook.png"; T.light_text(h, "WHO WAS LOOKING FOR WHOM?", 700, size=96, maxw=900); ov.append((str(h), 0.0, 3.2, 0))
    ins = ["-i", basev]; fc = ""; prev = "[0:v]"; loop = ["-loop","1","-framerate","30","-t",f"{TOTAL:.2f}"]
    for i, (png, t0, t1, yo) in enumerate(ov):
        ins += loop + ["-i", png]; n = i + 1
        fc += (f"[{n}:v]format=rgba,fade=in:st={t0:.2f}:d=0.12:alpha=1,fade=out:st={max(t0, t1-0.12):.2f}:d=0.12:alpha=1[o{i}];"
               f"{prev}[o{i}]overlay=0:{yo}:eof_action=pass:enable='between(t,{t0:.2f},{t1:.2f})'[p{i}];")
        prev = f"[p{i}]"
    fc += prev + "null[out]"; na = len(ov) + 1
    run(["ffmpeg","-y","-v","error","-threads","3",*ins,"-i",audio,"-filter_complex",fc,"-map","[out]","-map",f"{na}:a",
         "-t",f"{TOTAL:.2f}","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p",
         "-af","loudnorm=I=-14:TP=-1.5:LRA=11","-ar","44100","-c:a","aac","-b:a","192k","-movflags","+faststart",out])
def loud2(src, out):
    """two-pass loudnorm to -14 LUFS / -1.5 TP; video copied."""
    import json, re
    r = subprocess.run(["ffmpeg","-hide_banner","-threads","3","-i",str(src),"-af","loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json","-f","null","-"],
                       capture_output=True, text=True)
    m = json.loads(re.findall(r"\{[^{}]*\}", r.stderr)[-1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(["ffmpeg","-y","-v","error","-threads","3","-i",src,"-c:v","copy","-af",af,"-ar","44100","-c:a","aac","-b:a","192k","-movflags","+faststart",out])
if __name__ == "__main__":
    b = WORK/"base.mp4"; a = WORK/"mix.wav"; pre = WORK/"pre_loud.mp4"
    base(b); mix(a); letter(b, a, pre); loud2(pre, OUT); print("built", OUT)
