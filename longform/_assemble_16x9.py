"""Assemble the 16:9 long-form film: sequence each veo clip into its narration time
window, mux the balanced immersive audio. Two fill modes (no frozen ken-burns hold):
  - camera-only / static scenes -> seamless BOOMERANG (forward + reverse, looped).
  - DIRECTIONAL scenes (walking/riding; reverse looks comical) -> FORWARD-only concat of
    the original clip + chained continuation clips (<stem>_contN.mp4), trimmed to window.
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
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", str(FPS)]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{' '.join(str(c) for c in cmd[:6])}...\n{r.stderr[-1200:]}")

def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1",str(p)], capture_output=True, text=True).stdout.strip())

def slugof(t): return re.sub(r"[^a-z0-9]+","_",t.lower()).strip("_")[:40]

def scaled(src, dst):
    """scale/pad any clip to 1920x1080 30fps yuv420p, no audio."""
    run(["ffmpeg","-y","-i",str(src),
         "-vf",f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p",
         "-an",*ENC,str(dst)])

# scenes with genuine onward locomotion (walking/riding): NEVER boomerang (reverse
# looks comical). Filled with forward-chained continuation clips (<stem>_contN.mp4).
DIRECTIONAL = {8, 9, 11, 13, 14, 20}

audio_dur = dur(AUDIO)
scenes = json.loads((OUT/"scene_plan.json").read_text(encoding="utf-8"))["scenes"]
print(f"audio {audio_dur:.1f}s · {len(scenes)} scenes · boomerang + directional-chain")

seg_paths = []
for i, s in enumerate(scenes):
    start, end = s["t"]
    D = (audio_dur - start) if i == len(scenes)-1 else (end - start)
    stem = f"{s['id']:02d}_{slugof(s['title'])}"
    clip = OUT / f"{stem}.mp4"
    if not clip.exists():
        raise SystemExit(f"missing clip: {clip}")
    scene_mp4 = WORK / f"scene_{s['id']:02d}.mp4"

    if s["id"] in DIRECTIONAL:
        # forward-only: original + chained continuation clips, concat, trim/pad to window
        parts = [clip] + sorted(OUT.glob(f"{stem}_cont*.mp4"))
        scaled_parts = []
        for k, p in enumerate(parts):
            sp = WORK / f"f_{s['id']:02d}_{k}.mp4"
            scaled(p, sp)
            scaled_parts.append(sp)
        fwd = WORK / f"fwd_{s['id']:02d}.mp4"
        cat = WORK / f"catf_{s['id']:02d}.txt"
        cat.write_text("".join(f"file '{p.as_posix()}'\n" for p in scaled_parts), encoding="utf-8")
        run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cat),"-c","copy",str(fwd)])
        fdur = dur(fwd)
        if fdur >= D - 0.05:
            run(["ffmpeg","-y","-i",str(fwd),"-t",f"{D:.3f}","-an",*ENC,str(scene_mp4)])
        else:
            # tiny shortfall: clone the last frame for the remainder (sub-second)
            run(["ffmpeg","-y","-i",str(fwd),
                 "-vf",f"tpad=stop_mode=clone:stop_duration={D-fdur+0.1:.3f}",
                 "-t",f"{D:.3f}","-an",*ENC,str(scene_mp4)])
        print(f"  scene {s['id']:02d}  win={D:5.1f}s  FORWARD {len(parts)} clip(s) ({fdur:.0f}s)  {s['title'][:30]}")
    else:
        # camera-only / static: seamless boomerang (forward + reverse, looped)
        A = WORK / f"a_{s['id']:02d}.mp4"
        scaled(clip, A)
        cdur = dur(A)
        if D <= cdur + 0.05:
            run(["ffmpeg","-y","-i",str(A),"-t",f"{D:.3f}","-an",*ENC,str(scene_mp4)])
            loops = 0
        else:
            B = WORK / f"b_{s['id']:02d}.mp4"
            run(["ffmpeg","-y","-i",str(A),"-vf","reverse","-an",*ENC,str(B)])
            unit = WORK / f"unit_{s['id']:02d}.mp4"
            cat = WORK / f"cat_{s['id']:02d}.txt"
            cat.write_text(f"file '{A.as_posix()}'\nfile '{B.as_posix()}'\n", encoding="utf-8")
            run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cat),"-c","copy",str(unit)])
            run(["ffmpeg","-y","-stream_loop","-1","-i",str(unit),"-t",f"{D:.3f}","-an",*ENC,str(scene_mp4)])
            loops = D / (2*cdur)
        print(f"  scene {s['id']:02d}  win={D:5.1f}s  pingpong x{loops:4.1f}  {s['title'][:30]}")
    seg_paths.append(scene_mp4)

seg_list = WORK / "segments.txt"
seg_list.write_text("".join(f"file '{p.as_posix()}'\n" for p in seg_paths), encoding="utf-8")
video_only = WORK / "video_only.mp4"
run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(seg_list),"-c","copy",str(video_only)])
print(f"video_only {dur(video_only):.1f}s")

# concat frame-rounding leaves the video a touch short of the audio; clone the last
# frame (the hero "settle/hold" close on Christ) up to the audio length so the close
# isn't clipped, then -shortest trims to exact audio duration.
vdur = dur(video_only)
gap = max(0.0, audio_dur - vdur) + 0.5
final = OUT / "Isaiah53_16x9.mp4"
run(["ffmpeg","-y","-i",str(video_only),"-i",str(AUDIO),
     "-filter_complex",f"[0:v]tpad=stop_mode=clone:stop_duration={gap:.3f}[v]",
     "-map","[v]","-map","1:a",*ENC,"-c:a","aac","-b:a","192k","-shortest",str(final)])
print(f"\n[done] {final}  video_only={vdur:.1f}s + {gap:.1f}s hold -> ({dur(final):.1f}s)")
