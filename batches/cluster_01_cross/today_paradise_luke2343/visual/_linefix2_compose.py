r"""today_paradise linefix2 compose (video): linefix1 video with 3 rebuilt spans (engine, stock) + stream-copied rest.
 A 23.6333..28.8667 confession caption = spoken words; B 33.2333..43.2 Jesus beat without 'VERILY = TRULY' card + 'He asked for someday...' caption;
 C 53.9667..end Paradise beat at the clip's real length (5.03 s) = landing hold. Audio: audio/_linefix2/narration_linefix2_mix.wav"""
import subprocess, sys
from pathlib import Path
V=Path(__file__).resolve().parent; POOL=V/"_linefix1_pool"; W=POOL/"_compose2"; W.mkdir(exist_ok=True)
L1=V/"today_paradise_luke2343_sfx_v5hook_linefix1.mp4"
ENC=["-c:v","libx264","-crf","18","-preset","medium","-profile:v","high","-level","4.0","-pix_fmt","yuv420p","-r","30","-an"]
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode: sys.exit("FAIL "+" ".join(map(str,c))[:200]+"\n"+r.stderr[-1500:])
def cp(name,a,b,n):
    run(["ffmpeg","-y","-loglevel","error","-ss",f"{a+0.01:.3f}","-i",str(L1),"-frames:v",str(n),"-an","-c:v","copy","-avoid_negative_ts","make_zero",str(W/f"{name}.mp4")])
def re(name,src,n):
    run(["ffmpeg","-y","-loglevel","error","-i",str(src),"-vf",f"trim=start_frame=0:end_frame={n},setpts=PTS-STARTPTS"]+ENC+[str(W/f"{name}.mp4")])
cp("s1",0,23.63333,709); re("A",POOL/"linefix2_A.spec_preview.mp4",157); cp("s3",28.86667,33.23333,131)
re("B",POOL/"linefix2_B.spec_preview.mp4",299); cp("s5",43.2,53.96667,323); re("C",POOL/"linefix2_C.spec_preview.mp4",151)
names=["s1","A","s3","B","s5","C"]
(W/"list.txt").write_text("".join(f"file '{n}.mp4'\n" for n in names))
run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(W/"list.txt"),"-c","copy",str(W/"video_only.mp4")])
print("ok")
