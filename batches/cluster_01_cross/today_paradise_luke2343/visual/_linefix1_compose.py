r"""today_paradise linefix1 compose: new head (engine beats 0+3, 267 frames, hook card remade) + OLD v5hook from keyframe 12.0333 (frame 361) STREAM-COPIED + new audio mix."""
import subprocess, sys
from pathlib import Path
V=Path(__file__).resolve().parent; POOL=V/"_linefix1_pool"
OLD=V/"today_paradise_luke2343_sfx_v5hook.mp4"; HEAD=POOL/"livingpage_short.linefix1.spec_preview.mp4"
AUD=V.parent/"audio/_linefix1/narration_linefix1_mix.wav"; W=POOL/"_compose"; W.mkdir(exist_ok=True)
ENC=["-c:v","libx264","-crf","18","-preset","medium","-profile:v","high","-level","4.0","-pix_fmt","yuv420p","-r","30","-an"]
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode: sys.exit("FAIL "+" ".join(map(str,c))[:200]+"\n"+r.stderr[-1500:])
fc=("[1:v]format=rgba,fade=t=in:st=0.30:d=0.12:alpha=1,fade=t=out:st=3.58:d=0.12:alpha=1[c1];"
    "[2:v]format=rgba,fade=t=in:st=2.85:d=0.12:alpha=1,fade=t=out:st=3.68:d=0.12:alpha=1[c2];"
    "[0:v][c1]overlay=0:0:enable='between(t,0.30,3.70)'[m];[m][c2]overlay=0:0:enable='between(t,2.85,3.80)',trim=start_frame=0:end_frame=267,setpts=PTS-STARTPTS[v]")
run(["ffmpeg","-y","-loglevel","error","-i",str(HEAD),"-loop","1","-t","9","-i",str(POOL/"hook1.png"),"-loop","1","-t","9","-i",str(POOL/"hook2.png"),"-filter_complex",fc,"-map","[v]"]+ENC+[str(W/"head.mp4")])
run(["ffmpeg","-y","-loglevel","error","-ss","12.04","-i",str(OLD),"-an","-c:v","copy","-avoid_negative_ts","make_zero",str(W/"tail.mp4")])
(W/"list.txt").write_text("file 'head.mp4'\nfile 'tail.mp4'\n")
run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(W/"list.txt"),"-c","copy",str(W/"video_only.mp4")])
out=V/"today_paradise_luke2343_sfx_v5hook_linefix1.mp4"
run(["ffmpeg","-y","-loglevel","error","-i",str(W/"video_only.mp4"),"-i",str(AUD),"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-ar","44100","-t","55.9333","-movflags","+faststart",str(out)])
print("ok",out)
