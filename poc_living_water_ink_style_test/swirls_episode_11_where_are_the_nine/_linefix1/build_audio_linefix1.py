r"""Ep11 linefix1 audio. Zero-shift design: every word after the new first line stays at its OLD time (old 'They' = 6.18 s ... old 'faith.' = 72.74 s),
so the picture, score (score_piano.mp3), sfx layers (build_sfx.py LAYERS) and the marks are untouched.
 narration_linefix1: [new first line, take a, 0.40 s of its long pause removed, 'Ten' at 0.18 s]
                   + [old narration.mp3 5.80..73.60 s, kept at its OLD times]
                   + [new last line, take b, placed so 'face' lands at 77.55 s]
 then the film's own chain: narration -> aac -> score_mix.mix_tail (score -6 dB, duck 0.12/2.5/250) -> aac -> sfxlib.build(LAYERS).
Usage: build_audio_linefix1.py null|new   (null = old narration through the same chain, to prove the chain reproduces the shipped audio)"""
import subprocess, sys, json
from pathlib import Path
H = Path(__file__).resolve().parent
EP = H.parent
ROOT = EP.parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(EP))
from pipeline import score_mix
import build_sfx
import sfxlib
mode = sys.argv[1] if len(sys.argv) > 1 else "new"
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit("FAIL " + " ".join(map(str, cmd))[:300] + "\n" + r.stderr[-1500:])
FMT = "aformat=sample_fmts=fltp:channel_layouts=mono:sample_rates=44100"
OLD = EP / "narration.mp3"
NARR_LEN = 80.608866
TOTAL = NARR_LEN + 3.0
if mode == "null":
    narr = OLD
else:
    # first line: take a. cut 2.95..3.35 (inside the silence 2.85..3.72). file t -> abs t+0.08 (before cut).
    CUT0, CUT1, FOFF = 2.95, 3.35, 0.08
    KEEP0, KEEP1 = 5.80, 73.60            # old narration kept span (both ends inside old silences)
    LAST_OFF = 77.55 - 3.091              # last line take b: 'face' at 77.55
    fc = ";".join([
        f"[0:a]{FMT},atrim=0:{CUT0},asetpts=PTS-STARTPTS,afade=t=out:st={CUT0-0.03}:d=0.03[a1]",
        f"[0:a]{FMT},atrim={CUT1},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.03[a2]",
        "[a1][a2]concat=n=2:v=0:a=1,adelay=80,afade=t=out:st=5.3:d=0.15[first]",
        f"[1:a]{FMT},atrim={KEEP0}:{KEEP1},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.03,afade=t=out:st={KEEP1-KEEP0-0.05}:d=0.05,adelay={int(round(KEEP0*1000))}[mid]",
        f"[2:a]{FMT},afade=t=in:st=0:d=0.02,adelay={int(round(LAST_OFF*1000))}[last]",
        f"[first][mid][last]amix=inputs=3:normalize=0:duration=longest,apad=whole_dur={NARR_LEN:.6f},atrim=0:{NARR_LEN:.6f}[n]",
    ])
    narr = H / "narration_linefix1.wav"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(H / "first_narrator_a.mp3"), "-i", str(OLD),
         "-i", str(H / "last_narrator_b.mp3"), "-filter_complex", fc, "-map", "[n]", "-c:a", "pcm_s16le", str(narr)])
tag = mode
# stage 1: narration -> aac (like swirls_assemble with_narration), then the shared mix_tail
wn = H / f"_{tag}_with_narration.m4a"
run(["ffmpeg", "-y", "-v", "error", "-i", str(narr), "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL:.3f}", str(wn)])
filt = f"[1:a]{score_mix.AFMT},volume=-6dB[mus];" + "[0:a]" + score_mix.AFMT + f",apad=whole_dur={TOTAL},asplit=2[main][key];" \
    + "[mus][key]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[musd];[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
mix_aac = H / f"_{tag}_mix_stage1.m4a"
run(["ffmpeg", "-y", "-v", "error", "-i", str(wn), "-i", str(EP / "score_piano.mp3"), "-filter_complex", filt,
     "-map", "[mix]", "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL:.3f}", str(mix_aac)])
# stage-1 mp4 = picture (the pinned film's own video stream) + stage-1 audio, as sfxlib.build expects a video+audio src
VID = EP / "uplift" / "ep11_uplift_fix1.mp4"
s1 = H / f"_{tag}_stage1.mp4"
run(["ffmpeg", "-y", "-v", "error", "-i", str(VID), "-i", str(mix_aac), "-map", "0:v", "-map", "1:a", "-c", "copy", "-shortest", str(s1)])
out = H / f"_{tag}_sfx.mp4"
sfxlib.build(s1, out, build_sfx.LAYERS)
print("ok", out)
