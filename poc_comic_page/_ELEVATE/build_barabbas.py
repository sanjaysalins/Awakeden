"""Barabbas A/B POC. Locked words 2026-11-09; recorded audio (37.24s) + 3.06s landing hold.
A = 4 animated 3-panel grid clips (10s each).  B = same 4 grid stills with a $0 slow top-to-bottom pan.
Same Mockers-look lettering + same sound mix on both. Gentle: -threads 2, one ffmpeg at a time.
  .venv\\Scripts\\python.exe poc_comic_page/_ELEVATE/build_barabbas.py [A|B|both]"""
import subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_tp as T
import build_w3 as W

PIECE = T.ROOT / "batches/cluster_01_cross/barabbas_short"
G = PIECE / "visual/grids"; SL = T.ROOT / "sound_library/clips"
NAR = PIECE / "audio/narration.mp3"
TOTAL = 41.6; FADE = 0.04
WORK = T.HERE / "work" / "barabbas"; WORK.mkdir(parents=True, exist_ok=True)

# turn times from real segment durations (+0.4s pre-quote silences)
# (t0, t1, text, who, ref, jesus)
PL = [(3.55, 5.15, "He was a robber in prison.", None, None, False),
      (5.2, 10.9, "Pilate, the governor, offered to free one man. Pilate knew the leaders were jealous of Jesus.", None, None, False),
      (11.35, 14.95, "Barabbas, or Jesus which is called Christ?", "PILATE", "MATTHEW 27:17", False),
      (15.35, 16.7, "Barabbas.", "THE CROWD", "MATTHEW 27:21", False),
      (17.0, 19.0, "Why, what evil hath he done?", "PILATE", "MATTHEW 27:23", False),
      (19.3, 20.8, "Let him be crucified.", "THE CROWD", "MATTHEW 27:23", False),
      (20.85, 23.7, "Listen: Bar-ABBA.", None, None, False),
      (23.75, 28.8, "Jesus called God “Abba.” It means Father.", None, "MARK 14:36", True),
      (28.9, 33.4, "So the robber went free. The true Son of the Father did not.", None, None, False),
      (33.45, 38.55, "Barabbas only had the name. Jesus died so we could call God Father too.", None, "GALATIANS 4:5-6", False)]


def run(cmd): subprocess.run([str(c) for c in cmd], check=True)


def base_A(out):
    segs = [G / ("a%d.mp4" % i) for i in (1, 2, 3, 4)]
    ins = []; fc = ""
    for i, s in enumerate(segs):
        ins += ["-i", s]; fc += "[%d:v]scale=1080:1920:flags=lanczos,fps=30,setsar=1[v%d];" % (i, i)
    fc += "".join("[v%d]" % i for i in range(4)) + "concat=n=4:v=1:a=0,tpad=stop_mode=clone:stop_duration=0.6[o]"
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", *ins, "-filter_complex", fc, "-map", "[o]", "-t", "%.2f" % TOTAL,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", out])


def base_A2(out):
    """A with 3 slideshow stretches replaced by their own animated moment clips (same durations, same sync)."""
    M = G.parent / "moments"; a = lambda i: G / ("a%d.mp4" % i)
    segs = [(a(1), 0, 2.8, 1.0), (M / "c1.mp4", 0, 3.1, 0.97), (a(1), 5.9, 10.03, 1.0), (a(2), 0, 10.03, 1.0),
            (a(3), 0, 3.3, 1.0), (M / "c2.mp4", 0, 3.4, 1.0), (a(3), 6.7, 10.03, 1.0), (a(4), 0, 5.0, 1.0), (M / "c3.mp4", 0, 5.03, 1.0)]
    ins = []; fc = ""
    for i, (f, t0, t1, crop) in enumerate(segs):
        ins += ["-i", f]
        c = "" if crop == 1.0 else "crop=iw*%.3f:ih*%.3f," % (crop, crop)
        fc += "[%d:v]trim=%.3f:%.3f,setpts=PTS-STARTPTS,%sscale=1080:1920:flags=lanczos,fps=30,setsar=1[v%d];" % (i, t0, t1, c, i)
    fc += "".join("[v%d]" % i for i in range(len(segs))) + "concat=n=%d:v=1:a=0,tpad=stop_mode=clone:stop_duration=0.6[o]" % len(segs)
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", *ins, "-filter_complex", fc, "-map", "[o]", "-t", "%.2f" % TOTAL,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", out])


def base_A3(out):
    """A2 + 3 more moment clips: Pilate/priests without ghost Jesus, calm Jesus in the crowd, Jesus carrying the cross."""
    M = G.parent / "moments"; a = lambda i: G / ("a%d.mp4" % i)
    segs = [(a(1), 0, 2.8, 1.0), (M / "c1.mp4", 0, 3.1, 0.97), (M / "d3.mp4", 0, 4.13, 1.0), (a(2), 0, 6.7, 1.0),
            (M / "d1.mp4", 0, 3.35, 1.0), (a(3), 0, 3.3, 1.0), (M / "c2.mp4", 0, 3.4, 1.0), (a(3), 6.7, 10.03, 1.0),
            (a(4), 0, 2.9, 1.0), (M / "d2.mp4", 0, 3.73, 1.0), (M / "c3.mp4", 0, 3.6, 1.0)]
    ins = []; fc = ""
    for i, (f, t0, t1, crop) in enumerate(segs):
        ins += ["-i", f]
        c = "" if crop == 1.0 else "crop=iw*%.3f:ih*%.3f," % (crop, crop)
        fc += "[%d:v]trim=%.3f:%.3f,setpts=PTS-STARTPTS,%sscale=1080:1920:flags=lanczos,fps=30,setsar=1[v%d];" % (i, t0, t1, c, i)
    fc += "".join("[v%d]" % i for i in range(len(segs))) + "concat=n=%d:v=1:a=0,tpad=stop_mode=clone:stop_duration=0.6[o]" % len(segs)
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", *ins, "-filter_complex", fc, "-map", "[o]", "-t", "%.2f" % TOTAL,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", out])


def base_A4(out):
    """A3 + red-team fixes: sky marks cut out (a2 3.0-4.7s), burst lands on 'the robber went free', film ends on Jesus with the cross."""
    M = G.parent / "moments"; a = lambda i: G / ("a%d.mp4" % i)
    # (file, t0, t1, crop, speed_factor, hold_after_s)
    segs = [(a(1), 0, 2.8, 1.0, 1, 0), (M / "c1.mp4", 0, 3.1, 0.97, 1, 0), (M / "d3.mp4", 0, 4.13, 1.0, 1, 0),
            (a(2), 0, 1.4, 1.0, 2.0, 0.89), (a(2), 4.9, 5.9, 1.0, 1, 0), (M / "d1.mp4", 0, 4.03, 1.0, 1.30, 0),
            (a(3), 0, 3.3, 1.0, 1, 0), (M / "c2.mp4", 0, 4.03, 1.0, 1, 0.62), (a(3), 6.7, 10.03, 1.0, 1, 0),
            (a(4), 1.26, 2.9, 1.0, 1, 0), (M / "c3.mp4", 0, 3.6, 1.0, 1, 0), (M / "d2.mp4", 0, 3.73, 1.0, 1, 0)]
    ins = []; fc = ""
    for i, (f, t0, t1, crop, sp, hold) in enumerate(segs):
        ins += ["-i", f]
        c = "" if crop == 1.0 else "crop=iw*%.3f:ih*%.3f," % (crop, crop)
        sl = "" if sp == 1 else "setpts=PTS*%.3f," % sp
        hd = "" if not hold else "tpad=stop_mode=clone:stop_duration=%.2f," % hold
        fc += "[%d:v]trim=%.3f:%.3f,setpts=PTS-STARTPTS,%s%s%sscale=1080:1920:flags=lanczos,fps=30,setsar=1[v%d];" % (i, t0, t1, sl, hd, c, i)
    fc += "".join("[v%d]" % i for i in range(len(segs))) + "concat=n=%d:v=1:a=0,tpad=stop_mode=clone:stop_duration=0.6[o]" % len(segs)
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", *ins, "-filter_complex", fc, "-map", "[o]", "-t", "%.2f" % TOTAL,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", out])


def base_A5(out):
    """A4 re-timed to the re-recorded narration (38.52s): hook slowed to 3.5s, more Pilate/priests, hand shortened, cross walk slowed, ends on Jesus."""
    M = G.parent / "moments"; a = lambda i: G / ("a%d.mp4" % i)
    segs = [(a(1), 0, 2.8, 1.0, 1.254, 0), (M / "c1.mp4", 0, 3.1, 0.97, 1, 0), (M / "d3.mp4", 0, 4.214, 1.0, 1, 0),
            (a(2), 0, 1.4, 1.0, 2.0, 0.89), (a(2), 4.9, 5.9, 1.0, 1, 0), (M / "d1.mp4", 0, 4.03, 1.0, 1.30, 0),
            (a(3), 0, 3.3, 1.0, 1, 0), (M / "c2.mp4", 0, 4.03, 1.0, 1, 0.62), (a(3), 6.7, 10.03, 1.0, 1, 0),
            (a(4), 1.26, 2.9, 1.0, 1, 0), (M / "c3.mp4", 0, 2.3, 1.0, 1, 0), (M / "d2.mp4", 0, 4.03, 1.0, 1.30, 0.1)]
    ins = []; fc = ""
    for i, (f, t0, t1, crop, sp, hold) in enumerate(segs):
        ins += ["-i", f]
        c = "" if crop == 1.0 else "crop=iw*%.3f:ih*%.3f," % (crop, crop)
        sl = "" if sp == 1 else "setpts=PTS*%.3f," % sp
        hd = "" if not hold else "tpad=stop_mode=clone:stop_duration=%.2f," % hold
        fc += "[%d:v]trim=%.3f:%.3f,setpts=PTS-STARTPTS,%s%s%sscale=1080:1920:flags=lanczos,fps=30,setsar=1[v%d];" % (i, t0, t1, sl, hd, c, i)
    fc += "".join("[v%d]" % i for i in range(len(segs))) + "concat=n=%d:v=1:a=0,tpad=stop_mode=clone:stop_duration=0.6[o]" % len(segs)
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", *ins, "-filter_complex", fc, "-map", "[o]", "-t", "%.2f" % TOTAL,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", out])


def base_A6(out):
    """A5 with the c1 'ragged trousers' clip (not era-correct) swapped for e1: a new still (bare legs under a
    knee-length tunic, ankle shackles; nano_banana_2) animated 4s with gemini_omni_flash_1_2 (owner OK, ~$0.55)."""
    M = G.parent / "moments"; a = lambda i: G / ("a%d.mp4" % i)
    segs = [(a(1), 0, 2.8, 1.0, 1.254, 0), (M / "e1.mp4", 0, 3.1, 1.0, 1, 0), (M / "d3.mp4", 0, 4.214, 1.0, 1, 0),
            (a(2), 0, 1.4, 1.0, 2.0, 0.89), (a(2), 4.9, 5.9, 1.0, 1, 0), (M / "d1.mp4", 0, 4.03, 1.0, 1.30, 0),
            (a(3), 0, 3.3, 1.0, 1, 0), (M / "c2.mp4", 0, 4.03, 1.0, 1, 0.62), (a(3), 6.7, 10.03, 1.0, 1, 0),
            (a(4), 1.26, 2.9, 1.0, 1, 0), (M / "c3.mp4", 0, 2.3, 1.0, 1, 0), (M / "d2.mp4", 0, 4.03, 1.0, 1.30, 0.1)]
    ins = []; fc = ""
    for i, (f, t0, t1, crop, sp, hold) in enumerate(segs):
        ins += ["-i", f]
        c = "" if crop == 1.0 else "crop=iw*%.3f:ih*%.3f," % (crop, crop)
        sl = "" if sp == 1 else "setpts=PTS*%.3f," % sp
        hd = "" if not hold else "tpad=stop_mode=clone:stop_duration=%.2f," % hold
        fc += "[%d:v]trim=%.3f:%.3f,setpts=PTS-STARTPTS,%s%s%sscale=1080:1920:flags=lanczos,fps=30,setsar=1[v%d];" % (i, t0, t1, sl, hd, c, i)
    fc += "".join("[v%d]" % i for i in range(len(segs))) + "concat=n=%d:v=1:a=0,tpad=stop_mode=clone:stop_duration=0.6[o]" % len(segs)
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", *ins, "-filter_complex", fc, "-map", "[o]", "-t", "%.2f" % TOTAL,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", out])


def base_A7(out):
    """A6 + red-team r2 free fixes: chain-burst sparks cut (a3 starts 7.7s, after the burst), sky-hand clip c3 dropped
    (cross walk d2 starts at 33.68 and runs slower, last frame held into the landing hold)."""
    M = G.parent / "moments"; a = lambda i: G / ("a%d.mp4" % i)
    segs = [(a(1), 0, 2.8, 1.0, 1.254, 0), (M / "e1.mp4", 0, 3.1, 1.0, 1, 0), (M / "d3.mp4", 0, 4.214, 1.0, 1, 0),
            (a(2), 0, 1.4, 1.0, 2.0, 0.89), (a(2), 4.9, 5.9, 1.0, 1, 0), (M / "d1.mp4", 0, 4.03, 1.0, 1.30, 0),
            (a(3), 0, 3.3, 1.0, 1, 0), (M / "c2.mp4", 0, 4.03, 1.0, 1, 0.62), (a(3), 7.7, 10.03, 1.0, 1.43, 0),
            (a(4), 1.26, 2.9, 1.0, 1, 0), (M / "d2.mp4", 0, 4.03, 1.0, 1.5, 1.3)]
    ins = []; fc = ""
    for i, (f, t0, t1, crop, sp, hold) in enumerate(segs):
        ins += ["-i", f]
        c = "" if crop == 1.0 else "crop=iw*%.3f:ih*%.3f," % (crop, crop)
        sl = "" if sp == 1 else "setpts=PTS*%.3f," % sp
        hd = "" if not hold else "tpad=stop_mode=clone:stop_duration=%.2f," % hold
        fc += "[%d:v]trim=%.3f:%.3f,setpts=PTS-STARTPTS,%s%s%sscale=1080:1920:flags=lanczos,fps=30,setsar=1[v%d];" % (i, t0, t1, sl, hd, c, i)
    fc += "".join("[v%d]" % i for i in range(len(segs))) + "concat=n=%d:v=1:a=0,tpad=stop_mode=clone:stop_duration=0.6[o]" % len(segs)
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", *ins, "-filter_complex", fc, "-map", "[o]", "-t", "%.2f" % TOTAL,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", out])


def base_A8(out):
    """A7 + red-team r2 paid redraws (owner yes ~USD 2.33): f2 Pilate + plain dignified elders replaces d3 hooded leaders;
    f1 Jesus praying alone (8s) replaces a3 overview + c2 invented Barabbas/Jesus meeting on the Abba line;
    f3b upright cross walk, empty hill, soft light replaces a4 tearful look-back + d2 X-cross walk."""
    M = G.parent / "moments"; a = lambda i: G / ("a%d.mp4" % i)
    segs = [(a(1), 0, 2.8, 1.0, 1.254, 0), (M / "e1.mp4", 0, 3.1, 1.0, 1, 0), (M / "f2.mp4", 0, 4.0, 1.0, 1.0535, 0),
            (a(2), 0, 1.4, 1.0, 2.0, 0.89), (a(2), 4.9, 5.9, 1.0, 1, 0), (M / "d1.mp4", 0, 4.03, 1.0, 1.30, 0),
            (M / "f1.mp4", 0, 7.95, 1.0, 1, 0), (a(3), 7.7, 10.03, 1.0, 1.43, 0),
            (M / "f3b.mp4", 0, 6.03, 1.0, 1.3, 1.3)]
    ins = []; fc = ""
    for i, (f, t0, t1, crop, sp, hold) in enumerate(segs):
        ins += ["-i", f]
        c = "" if crop == 1.0 else "crop=iw*%.3f:ih*%.3f," % (crop, crop)
        sl = "" if sp == 1 else "setpts=PTS*%.3f," % sp
        hd = "" if not hold else "tpad=stop_mode=clone:stop_duration=%.2f," % hold
        fc += "[%d:v]trim=%.3f:%.3f,setpts=PTS-STARTPTS,%s%s%sscale=1080:1920:flags=lanczos,fps=30,setsar=1[v%d];" % (i, t0, t1, sl, hd, c, i)
    fc += "".join("[v%d]" % i for i in range(len(segs))) + "concat=n=%d:v=1:a=0,tpad=stop_mode=clone:stop_duration=0.6[o]" % len(segs)
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", *ins, "-filter_complex", fc, "-map", "[o]", "-t", "%.2f" % TOTAL,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", out])


def base_B(out):
    parts = []
    for i in (1, 2, 3, 4):
        o = WORK / ("b%d.mp4" % i); parts.append(o)
        # zoom 1.6 then ease a 1080x1920 window from the top of the grid to the bottom over 10.03s
        vf = ("scale=1728:-1:flags=lanczos,crop=1080:1920:'(iw-1080)/2':"
              "'(ih-1920)*(3*pow(min(t/10.03,1),2)-2*pow(min(t/10.03,1),3))',setsar=1,fps=30")
        run(["ffmpeg", "-y", "-v", "error", "-threads", "2", "-loop", "1", "-framerate", "30", "-t", "10.03",
             "-i", G / ("g%d.png" % i), "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", o])
    (WORK / "bl.txt").write_text("".join("file '%s'\n" % p.as_posix() for p in parts))
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", "-f", "concat", "-safe", "0", "-i", WORK / "bl.txt",
         "-vf", "tpad=stop_mode=clone:stop_duration=0.6", "-t", "%.2f" % TOTAL, "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", out])


def mix(out):
    if out.exists(): return
    fc = f"""
[1:a]apad=whole_dur={TOTAL},asplit=2[nar][key];
[2:a]atrim=0:{TOTAL},afade=t=in:st=0:d=0.8,afade=t=out:st=37.3:d=4.3,volume=-12dB[sc];
[3:a]atrim=0:11,afade=t=in:st=0:d=1,afade=t=out:st=8.5:d=2.5,volume=-3dB,apad=whole_dur={TOTAL}[air];
[4:a]atrim=0:10,afade=t=in:st=0:d=0.6,afade=t=out:st=8:d=2,volume=-9dB,adelay=11300|11300,apad=whole_dur={TOTAL}[mob];
[5:a]volume=-4dB,adelay=28600|28600,apad=whole_dur={TOTAL}[door];
[6:a]afade=t=in:st=0:d=1.5,volume=6dB,adelay=33400|33400,afade=t=out:st=37.5:d=4,apad=whole_dur={TOTAL},atrim=0:{TOTAL}[ch];
[sc][air][mob][door][ch]amix=inputs=5:normalize=0:duration=longest[bed];
[bed][key]sidechaincompress=threshold=0.02:ratio=6:attack=30:release=500[duck];
[nar][duck]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.85:level=disabled,atrim=0:{TOTAL}[a]"""
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", "-i", WORK / "silence_stub.wav", "-i", NAR,
         "-i", SL / "score_reverent_grace.mp3", "-i", SL / "air_hollow_desolate.mp3", "-i", SL / "crowd_shout_mob.mp3",
         "-i", SL / "door_gate_creak.mp3", "-i", SL / "heavenly_choir_soft.mp3",
         "-filter_complex", fc, "-map", "[a]", "-c:a", "aac", "-b:a", "192k", out])


def letter(base, audio, out, d):
    ov = []
    for i, (a, b, text, who, ref, j) in enumerate(PL):
        p = d / ("p%02d.png" % i); W.pill_tabs(p, text, who, ref, jesus=j); ov.append((str(p), a, b))
    h = d / "hook.png"; T.light_text(h, "IN ARAMAIC, BARABBAS = SON OF THE FATHER", 400, size=104, maxw=900); ov.append((str(h), 0.0, 3.5))
    ins = ["-i", base]; fc = ""; prev = "[0:v]"; n = 1; loop = ["-loop", "1", "-framerate", "30", "-t", "%.2f" % TOTAL]
    for i, (png, t0, t1) in enumerate(ov):
        ins += loop + ["-i", png]
        fc += "[%d:v]format=rgba,fade=in:st=%.2f:d=%.2f:alpha=1,fade=out:st=%.2f:d=%.2f:alpha=1[o%d];%s[o%d]overlay=x=0:y=0:eof_action=pass:enable='between(t,%.2f,%.2f)'[p%d];" % (n, t0, FADE, max(t0, t1 - FADE), FADE, i, prev, i, t0, t1, i)
        prev = "[p%d]" % i; n += 1
    fc += prev + "null[out]"
    run(["ffmpeg", "-y", "-v", "error", "-threads", "2", *ins, "-i", audio, "-filter_complex", fc, "-map", "[out]", "-map", "%d:a" % n,
         "-t", "%.2f" % TOTAL, "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", out])


def main(which):
    (WORK / "silence_stub.wav").exists() or run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "1", WORK / "silence_stub.wav"])
    aud = WORK / "mix_v2.m4a"; mix(aud)
    for v in ("A", "B", "A2", "A3", "A4", "A5", "A6", "A7", "A8"):
        if which not in (v, "both"): continue
        base = WORK / ("base_%s.mp4" % v)
        {"A": base_A, "B": base_B, "A2": base_A2, "A3": base_A3, "A4": base_A4, "A5": base_A5, "A6": base_A6, "A7": base_A7, "A8": base_A8}[v](base)
        d = WORK / ("lett_" + v); d.mkdir(exist_ok=True)
        out = PIECE / "visual" / ("barabbas_short_%s_%s.mp4" % (v, "pan" if v == "B" else "animated"))
        letter(base, aud, out, d); print("built", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "both")
