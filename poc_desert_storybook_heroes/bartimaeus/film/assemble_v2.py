"""Draft v2 (words+voice v4, SHOT_PLAN v2): 17 clips, 1.0x hard cuts, trim only (head of each clip), narration + 3 s landing hold. No music/SFX yet."""
import re, subprocess
from pathlib import Path
H = Path(__file__).resolve().parent; P = H.parent
rows = [l for l in (P / "SHOT_PLAN.md").read_text(encoding="utf-8").splitlines() if re.match(r"\| s\d\d", l)]
slots = []
for r in rows:
    c = [x.strip() for x in r.strip("|").split("|")]
    a, b = map(float, c[1].split("-")); slots.append((c[0], a, b))
END = slots[-1][2]  # 79.17 = 76.17 narration + 3.0 hold
FPS = 30
args, f = ["ffmpeg", "-y", "-v", "error"], []
for i, (sid, a, b) in enumerate(slots):
    # frame-exact slot lengths from cumulative boundaries (no drift)
    n = round(b * FPS) - round(a * FPS)
    args += ["-i", str(P / "clips" / f"{sid}.mp4")]
    f.append(f"[{i}:v]fps={FPS},scale=1080:1920,setsar=1,trim=end_frame={n},setpts=PTS-STARTPTS[v{i}]")
k = len(slots)
args += ["-i", str(P / "audio" / "narration.mp3")]
f.append("".join(f"[v{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0[v]")
f.append(f"[{k}:a]apad=whole_dur={END}[a]")
out = H / "bartimaeus_draft_v2.mp4"
args += ["-filter_complex", ";".join(f), "-map", "[v]", "-map", "[a]", "-t", f"{END}",
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)]
subprocess.run(args, check=True)
for s in ("v", "a"):
    d = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", f"{s}:0", "-show_entries", "stream=duration", "-of", "csv=p=0", str(out)]).decode().strip()
    print(s, d)
