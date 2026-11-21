r"""he_hath_done_this holdfix1 compose: frames 0..1093 of the CURRENT final stream-copied (keyframe-aligned, untouched), then the two
engine-rebuilt beats (beat 12 at 4.1833 s; last beat at the clip's real 5.0333 s => film ends 45.667 s = last word 42.637 + 3.03 s),
audio = audio/_holdfix1/narration_holdfix1_mix.wav (AAC 192k).  Output he_hath_done_this_ps2231_sfx_holdfix1.mp4 (nothing overwritten)."""
import subprocess, sys
from pathlib import Path
V=Path(__file__).resolve().parent; POOL=V/"_holdfix1_pool"; W=POOL/"_compose"; W.mkdir(exist_ok=True)
SRC=V/"he_hath_done_this_ps2231_sfx.mp4"; TAIL=POOL/"holdfix1_tail.spec_preview.mp4"
AUD=V.parent/"audio/_holdfix1/narration_holdfix1_mix.wav"; OUT=V/"he_hath_done_this_ps2231_sfx_holdfix1.mp4"
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode: sys.exit("FAIL "+" ".join(map(str,c))[:200]+"\n"+r.stderr[-1500:])
run(["ffmpeg","-y","-loglevel","error","-ss","0","-i",str(SRC),"-frames:v","1094","-an","-c:v","copy","-avoid_negative_ts","make_zero",str(W/"s1.mp4")])
run(["ffmpeg","-y","-loglevel","error","-threads","3","-i",str(TAIL),"-vf","trim=start_frame=0:end_frame=276,setpts=PTS-STARTPTS",
     "-c:v","libx264","-crf","18","-preset","medium","-profile:v","high","-level","4.0","-pix_fmt","yuv420p","-r","30","-an",str(W/"tail.mp4")])
(W/"list.txt").write_text("file 's1.mp4'\nfile 'tail.mp4'\n")
run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(W/"list.txt"),"-c","copy",str(W/"video_only.mp4")])
run(["ffmpeg","-y","-loglevel","error","-threads","3","-i",str(W/"video_only.mp4"),"-i",str(AUD),"-map","0:v","-map","1:a","-c:v","copy",
     "-c:a","aac","-b:a","192k","-ar","44100","-ac","2","-movflags","+faststart","-shortest",str(OUT)])
print("ok",OUT)
