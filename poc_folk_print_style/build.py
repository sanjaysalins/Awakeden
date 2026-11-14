"""Build the Second Fire preview: 17 clips trimmed to their slots (1.0x, hard cuts, trim only),
voice B, 3.0 s landing hold, tail fade, faststart. $0. Gentle: ffmpeg -threads 3."""
import subprocess, json
from pathlib import Path

EP = Path(__file__).resolve().parent
VOICE = EP / "narration.mp3"
voice_len = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                           "-of", "csv=p=0", str(VOICE)]).decode().strip())
END = round(voice_len + 3.0, 3)
STARTS = [0.0, 3.3, 8.0, 13.2, 15.7, 18.9, 23.7, 28.9, 34.1, 36.7, 40.2, 47.8, 53.2, 60.2, 67.8, 75.2, 80.3]
bounds = STARTS + [END]
OUT = EP / "SECOND_FIRE_PREVIEW_v3.mp4"

inputs, filt = [], []
for i in range(17):
    clip = EP / "clips" / f"s{i + 1:02d}.mp4"
    dur = round(bounds[i + 1] - bounds[i], 3)
    clen = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(clip)]).decode().strip())
    assert clen >= dur, f"s{i+1:02d} clip {clen:.2f}s shorter than slot {dur:.2f}s"
    inputs += ["-i", str(clip)]
    filt.append(f"[{i}:v]trim=0:{dur},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,"
                f"crop=1080:1920,fps=30,format=yuv420p[v{i}]")
filt.append("".join(f"[v{i}]" for i in range(17)) + "concat=n=17:v=1:a=0[v]")
inputs += ["-i", str(VOICE)]
filt.append(f"[17:a]apad=whole_dur={END},atrim=0:{END},afade=t=out:st={END - 0.5}:d=0.5[a]")
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-threads", "3"] + inputs + [
    "-filter_complex", ";".join(filt), "-map", "[v]", "-map", "[a]",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-threads", "3",
    "-c:a", "aac", "-b:a", "192k", "-t", str(END), "-movflags", "+faststart", str(OUT)]
subprocess.run(cmd, check=True)
info = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration",
                                           "-of", "json", str(OUT)]))
print(OUT.name, "target", END, [(s["codec_type"], s.get("duration")) for s in info["streams"]])
