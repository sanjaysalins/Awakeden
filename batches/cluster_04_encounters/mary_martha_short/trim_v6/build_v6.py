"""$0 v6 TRIM of Mary & Martha (cut-only, 72.97 s -> 60.08 s). Same voices, same picture, same paid score.
Cuts (blind panel, 2026-11-20): S03, S06 (end of Martha's KJV line), S14-S16. Voice = preview_F_final.mp3 (voice + 3 s hold).
Picture: the locked v7 film (visual/mary_martha_final.mp4) with the SAME LENGTHS removed, each picture cut snapped to a
shot change (CUTS in _remotion/src/MaryMarthaV4.tsx) so no shot is chopped mid-way.
Score: the v4 recipe (poc_warm_storybook_style/fit_score_v4.py + mix_score_v4.py) with every time mapped through the
voice cut map; end fade 2.5 s (owner rule 2026-11-16).
  .venv\\Scripts\\python.exe <this>"""
import json, subprocess
from pathlib import Path

H = Path(__file__).resolve().parent
P = H.parent
WS = P.parents[2] / "poc_warm_storybook_style"
S = json.load(open(H / "sentences.json", encoding="utf-8"))
VOICE = H / "preview_G_final.mp3"
SRC = P / "visual" / "mary_martha_final.mp4"
OUT = P / "visual" / "mary_martha_final_v6trim.mp4"
T1, P2 = WS / "_score_rejected" / "part1_try1_dead16s.mp3", WS / "score_piano_part2_raw.mp3"


def mid(a, b): return (a + b) / 2


def acut(i, j=None):
    j = i if j is None else j
    return (mid(S[i - 1]["end"], S[i]["start"]), mid(S[j]["end"], S[j + 1]["start"]))


# v6 r2 (guardrail, 4/4 seats): S14-S15 RESTORED ("Mary had chosen the one thing needed: to listen to Him");
# 3/4 seats: the word "Later," cut (John 11:5 gives no timing).
ACUTS = [acut(3), acut(6), acut(16), (53.55, 54.12)]
# picture cuts: same length as each voice cut, ending (or starting) on a shot change
VCUTS = []
for (a, b), anchor in zip(ACUTS, [("start", 8.72), ("end", 22.27), ("end", 50.77), ("end", 55.27)]):
    L = b - a
    VCUTS.append((anchor[1], anchor[1] + L) if anchor[0] == "start" else (anchor[1] - L, anchor[1]))


def f(t):
    sh = 0.0
    for a, b in ACUTS:
        if t >= b:
            sh += b - a
        elif t > a:
            return a - sh
    return t - sh


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout.strip())


def main():
    total = dur(VOICE)
    # 1. picture: keep everything outside VCUTS
    keep, t = [], 0.0
    for a, b in VCUTS:
        keep.append((t, a)); t = b
    keep.append((t, 72.97))
    fc = "".join(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{i}];" for i, (a, b) in enumerate(keep))
    fc += "".join(f"[v{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=1:a=0,trim=0:{total:.3f}[v]"
    pic = H / "_picture.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(SRC), "-filter_complex", fc, "-map", "[v]",
                    "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30", str(pic)], check=True)
    # 2. score: fit_score_v4 recipe, times mapped
    p2_at = f(53.49)
    score = H / "_score.mp3"
    fc = (f"[0:a]atrim=16.2:{16.2 + p2_at:.2f},asetpts=PTS-STARTPTS[a];"
          f"[1:a]atrim=0:{total - p2_at:.2f},asetpts=PTS-STARTPTS,adelay={int(p2_at * 1000)}:all=1[b];"
          f"[a][b]amix=inputs=2:duration=longest:normalize=0,afade=t=in:st=0:d=1.0,afade=t=out:st={total - 2.5:.2f}:d=2.5[o]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(T1), "-i", str(P2), "-filter_complex", fc,
                    "-map", "[o]", "-t", f"{total:.2f}", str(score)], check=True)
    # 3. mix: mix_score_v4 recipe, times mapped
    A, B, C, D, DIP = f(53.49), f(58.49), f(63.4), f(67.4), f(63.15)
    vol = (f"volume='pow(10,(if(lt(t,{A:.2f}),-11,if(lt(t,{B:.2f}),-11+3*(t-{A:.2f})/{B - A:.2f},"
           f"if(lt(t,{C:.2f}),-8,if(lt(t,{D:.2f}),-8+8*(t-{C:.2f})/{D - C:.2f},0)))))/20)':eval=frame")
    dip = f"volume='pow(10,-6*max(0,1-abs(t-{DIP:.2f})/0.7)/20)':eval=frame"
    fc = ("[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[v][sc];"
          f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,{vol},{dip}[m];"
          "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md];"
          "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(VOICE), "-i", str(score), "-i", str(pic),
                    "-filter_complex", fc, "-map", "2:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", str(OUT)], check=True)
    # 4. word timings for captions (publish reads <video>.words.json)
    a = json.load(open(P / "visual" / "mary_martha_final.words.json", encoding="utf-8"))
    words = a.get("words", a) if isinstance(a, dict) else a
    keep_w = [dict(w, start=round(f(w["start"]), 3), end=round(f(w["end"]), 3)) for w in words
              if not any(x <= mid(w["start"], w["end"]) <= y for x, y in ACUTS)]
    for i, w in enumerate(keep_w):  # "the Bible says" now starts the sentence
        if w["w"] == "the" and i + 1 < len(keep_w) and keep_w[i + 1]["w"] == "Bible":
            w["w"] = "The"
    json.dump(keep_w if not isinstance(a, dict) else dict(a, words=keep_w),
              open(OUT.with_suffix(".words.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("ACUTS", [(round(x, 2), round(y, 2)) for x, y in ACUTS], "VCUTS", [(round(x, 2), round(y, 2)) for x, y in VCUTS])
    print("OUT", OUT, dur(OUT), "words", len(keep_w))


if __name__ == "__main__":
    main()
