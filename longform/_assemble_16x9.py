"""Assemble the 16:9 long-form film: sequence each veo clip into its narration time
window, mux the balanced immersive audio. Each scene = the 8s veo motion, then a slow
continued ken-burns push on the frozen last frame to fill the window (no dead freeze).
Output: 1920x1080 30fps + narration.immersive.mp3 -> Isaiah53_16x9.mp4. ffmpeg only ($0)."""
import sys, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V1 = ROOT / "longform" / "01_Isaiah_53_Suffering_Servant" / "v1"
OUT = V1 / "visual_16x9"
WORK = OUT / "_assembly"
WORK.mkdir(exist_ok=True)
AUDIO = V1 / "narration.immersive.mp3"
W, H, FPS = 1920, 1080, 30

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{' '.join(str(c) for c in cmd[:6])}...\n{r.stderr[-1200:]}")

def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1",str(p)], capture_output=True, text=True).stdout.strip())

def slugof(t): return re.sub(r"[^a-z0-9]+","_",t.lower()).strip("_")[:40]

audio_dur = dur(AUDIO)
scenes = json.loads((OUT/"scene_plan.json").read_text(encoding="utf-8"))["scenes"]
print(f"audio {audio_dur:.1f}s · {len(scenes)} scenes")

seg_list = WORK / "segments.txt"
seg_paths = []
for i, s in enumerate(scenes):
    start, end = s["t"]
    D = (audio_dur - start) if i == len(scenes)-1 else (end - start)
    clip = OUT / f"{s['id']:02d}_{slugof(s['title'])}.mp4"
    if not clip.exists():
        raise SystemExit(f"missing clip: {clip}")
    cdur = dur(clip)
    motion = min(cdur, D)
    scene_mp4 = WORK / f"scene_{s['id']:02d}.mp4"

    # A: the veo motion, scaled/padded to 1920x1080 30fps, trimmed to `motion`
    A = WORK / f"a_{s['id']:02d}.mp4"
    run(["ffmpeg","-y","-i",str(clip),"-t",f"{motion:.3f}",
         "-vf",f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p",
         "-an","-c:v","libx264","-preset","medium","-crf","19","-r",str(FPS),str(A)])

    hold = D - motion
    if hold > 0.2:
        last = WORK / f"last_{s['id']:02d}.png"
        run(["ffmpeg","-y","-sseof","-0.15","-i",str(clip),"-frames:v","1",str(last)])
        hf = max(1, round(hold*FPS))
        B = WORK / f"b_{s['id']:02d}.mp4"
        # slow continued push-in on the frozen frame (ken-burns)
        run(["ffmpeg","-y","-loop","1","-i",str(last),"-t",f"{hold:.3f}",
             "-vf",(f"scale={W*2}:{H*2},zoompan=z='min(1.0+0.0009*on,1.18)':"
                    f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={hf}:s={W}x{H}:fps={FPS},"
                    f"format=yuv420p"),
             "-an","-c:v","libx264","-preset","medium","-crf","19","-r",str(FPS),str(B)])
        cat = WORK / f"cat_{s['id']:02d}.txt"
        cat.write_text(f"file '{A.as_posix()}'\nfile '{B.as_posix()}'\n", encoding="utf-8")
        run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cat),"-c","copy",str(scene_mp4)])
    else:
        scene_mp4 = A
    seg_paths.append(scene_mp4)
    print(f"  scene {s['id']:02d}  win={D:5.1f}s  motion={motion:.1f}+hold={max(0,hold):.1f}  {s['title'][:34]}")

seg_list.write_text("".join(f"file '{p.as_posix()}'\n" for p in seg_paths), encoding="utf-8")
video_only = WORK / "video_only.mp4"
run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(seg_list),"-c","copy",str(video_only)])
print(f"video_only {dur(video_only):.1f}s")

final = OUT / "Isaiah53_16x9.mp4"
run(["ffmpeg","-y","-i",str(video_only),"-i",str(AUDIO),
     "-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest",str(final)])
print(f"\n[done] {final}  ({dur(final):.1f}s)")
