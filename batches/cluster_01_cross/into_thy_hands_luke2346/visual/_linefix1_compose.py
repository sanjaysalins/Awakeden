r"""into_thy_hands linefix1 compose: NEW head (engine beat 0 + new hook card, 125 frames) + OLD v5hook frames 125..278 re-encoded once
+ OLD v5hook from 9.3 s (keyframe) STREAM-COPIED, then mux audio/_linefix1/narration_linefix1_mix.wav.
Output: into_thy_hands_luke2346_sfx_v5hook_linefix1.mp4. JesusInTheBible .venv python (for json) not needed; plain script."""
import subprocess, sys
from pathlib import Path
V = Path(__file__).resolve().parent
POOL = V / "_linefix1_pool"
OLD = V / "into_thy_hands_luke2346_sfx_v5hook.mp4"
HEAD = POOL / "livingpage_short.linefix1.spec_preview.mp4"
CARD = POOL / "hookcard_new.png"
AUD = V.parent / "audio" / "_linefix1" / "narration_linefix1_mix.wav"
W = POOL / "_compose"; W.mkdir(exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-profile:v", "high", "-level", "4.0", "-pix_fmt", "yuv420p", "-r", "30", "-an"]
def run(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: sys.exit("FAIL " + " ".join(map(str, c))[:200] + "\n" + r.stderr[-1500:])
# 1 head with hook card 0.55..2.05 (fade 0.12)
fc = ("[1:v]format=rgba,fade=t=in:st=0.55:d=0.12:alpha=1,fade=t=out:st=1.93:d=0.12:alpha=1[c];"
      "[0:v][c]overlay=0:0:enable='between(t,0.55,2.05)',trim=start_frame=0:end_frame=125,setpts=PTS-STARTPTS[v]")
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(HEAD), "-loop", "1", "-t", "5", "-i", str(CARD), "-filter_complex", fc, "-map", "[v]"] + ENC + [str(W / "head.mp4")])
# 2 mid: old frames 125..278 (4.1667 .. 9.2667); keyframe at 9.3 = frame 279
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(OLD), "-vf", "trim=start_frame=125:end_frame=279,setpts=PTS-STARTPTS"] + ENC + [str(W / "mid.mp4")])
# 3 tail: stream copy from keyframe 9.3
run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "9.3", "-i", str(OLD), "-an", "-c:v", "copy", "-avoid_negative_ts", "make_zero", str(W / "tail.mp4")])
(W / "list.txt").write_text("".join(f"file '{n}.mp4'\n" for n in ("head", "mid", "tail")))
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(W / "list.txt"), "-c", "copy", str(W / "video_only.mp4")])
out = V / "into_thy_hands_luke2346_sfx_v5hook_linefix1.mp4"
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(W / "video_only.mp4"), "-i", str(AUD), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
     "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", str(out)])
print("ok", out)
