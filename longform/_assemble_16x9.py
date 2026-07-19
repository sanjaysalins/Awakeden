"""Assemble the 16:9 long-form film: sequence each veo clip into its narration time
window, mux the immersive (or plain) narration audio. EPISODE-GENERIC: pass an episode
slug/dir as the first arg (bare = Isaiah). Two fill modes (no frozen ken-burns hold):
  - camera-only / static scenes -> SLOW seamless BOOMERANG: the clip is slowed so a single
    forward+reverse drift fills the whole window (reverent, no brisk repeated loops).
  - DIRECTIONAL scenes (per-scene `directional:true`; reverse looks comical) -> FORWARD-only
    concat of the original clip + chained continuation clips (<stem>_contN.mp4).
Output: 1920x1080 30fps + the episode's audio -> <film_name>. ffmpeg only ($0)."""
import sys, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _episode import resolve  # noqa: E402

ep = resolve(sys.argv)
OUT = ep.out
WORK = OUT / "_assembly"
WORK.mkdir(exist_ok=True)
AUDIO = ep.audio(prefer_immersive=True)
if not AUDIO.exists():
    raise SystemExit(f"missing audio: {AUDIO} (render narration.mp3 first)")
W, H, FPS = 1920, 1080, 30
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", str(FPS)]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{' '.join(str(c) for c in cmd[:6])}...\n{r.stderr[-1200:]}")

def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1",str(p)], capture_output=True, text=True).stdout.strip())

def scaled(src, dst):
    """scale/pad any clip to 1920x1080 30fps yuv420p, no audio."""
    run(["ffmpeg","-y","-i",str(src),
         "-vf",f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p",
         "-an",*ENC,str(dst)])

KB_RANGE = 0.07   # subtle Ken Burns: 7% slow zoom over the window (push-in or pull-out)

def ken_burns(src, dst, D, push_in):
    """Layer a SUBTLE Ken Burns camera move over a finished scene clip — on TOP of the veo
    atmospherics + boomerang — so even quiet scenes carry continuous motion (user-approved).
    Alternated push-in / pull-out per scene so the film never feels like one monotonous push."""
    frames = max(2, int(round(D * FPS)))
    inc = KB_RANGE / frames
    hi = 1.0 + KB_RANGE
    if push_in:
        z = f"z='min(zoom+{inc:.6f},{hi:.4f})'"
    else:  # start zoomed, ease out to 1.0
        z = f"z='if(lte(on,1),{hi:.4f},max(zoom-{inc:.6f},1.0))'"
    vf = (f"scale={W*2}:{H*2},zoompan={z}:d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
          f"fps={FPS}:s={W}x{H}")
    run(["ffmpeg","-y","-i",str(src),"-vf",vf,"-an",*ENC,str(dst)])

audio_dur = dur(AUDIO)
scenes = ep.scenes
print(f"{ep.slug}: audio {audio_dur:.1f}s · {len(scenes)} scenes · boomerang + directional-chain")

# LF-AS deterministic gate (validators.lf_assembly, 2026-07-19): window tiling,
# movement coverage, gospel frame, hero window — BLOCKING (all 4 window-lane
# episodes sweep clean, so a failure here is a real authoring defect).
sys.path.insert(0, str(ROOT))
from pipeline import validators as _validators, clip_qc as _clip_qc  # noqa: E402
_blk, _warns = _validators.lf_assembly({"scenes": scenes}, audio_dur=audio_dur)
for _w in _warns:
    print(f"  [lf-as] warn: {_w}")
if _blk:
    for _b in _blk:
        print(f"  [lf-as] BLOCK: {_b}")
    raise SystemExit("LF-AS gate failed — fix the scene windows/plan before assembling")

# Fail-closed CLIP QC chokepoint (INV-23/24 discipline for the long lane).
# ROLLOUT-GATED: existing episodes' clips predate the sidecar discipline, so
# the default is report-only; set JITB_REQUIRE_CLIPQC=1 to enforce once an
# episode's clips are backfilled (`python -m pipeline.clip_qc <dir> --dir`).
import os as _os  # noqa: E402
_unverified = [ep.stem(s) for s in scenes
               if not _clip_qc.is_verified(OUT / f"{ep.stem(s)}.mp4")]
if _unverified:
    _msg = (f"  [clip-qc] {len(_unverified)}/{len(scenes)} clips lack a passing "
            f".clipqc.json sidecar (fail-closed discipline, pipeline/clip_qc.py)")
    if _os.environ.get("JITB_REQUIRE_CLIPQC") == "1":
        print(_msg)
        raise SystemExit("clip-qc gate failed — QC the clips (record_verdict) before assembling")
    print(_msg + " — REPORT-ONLY (set JITB_REQUIRE_CLIPQC=1 to enforce)")

seg_paths = []
for i, s in enumerate(scenes):
    start, end = s["t"]
    D = (audio_dur - start) if i == len(scenes)-1 else (end - start)
    stem = ep.stem(s)
    clip = OUT / f"{stem}.mp4"
    if not clip.exists():
        raise SystemExit(f"missing clip: {clip}")
    scene_mp4 = WORK / f"scene_{s['id']:02d}.mp4"

    if s.get("fill") == "forward_slow":
        # FORWARD-ONLY, time-stretched to fill the window (no reverse → no causal motion
        # running backwards like blood un-striking; no mid-motion freeze). For clips whose
        # motion is one-way: rising smoke, mist, a strike, or a camera push.
        A = WORK / f"a_{s['id']:02d}.mp4"
        scaled(clip, A)
        cdur = dur(A)
        factor = max(1.0, D / cdur)
        run(["ffmpeg","-y","-i",str(A),"-vf",f"setpts={factor:.4f}*PTS,fps={FPS}",
             "-t",f"{D:.3f}","-an",*ENC,str(scene_mp4)])
        print(f"  scene {s['id']:02d}  win={D:5.1f}s  SLOW-FWD x{factor:4.2f} (no reverse)  {s['title'][:30]}")
    elif s.get("directional"):
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
        # camera-only / static: SLOW seamless boomerang — slow the clip so ONE forward+reverse
        # ping-pong fills the whole window (a single reverent drift out and back; no brisk
        # repeated loops). factor = (D/2)/cdur, never below 1.0 (never speed the clip up).
        A = WORK / f"a_{s['id']:02d}.mp4"
        scaled(clip, A)
        cdur = dur(A)
        if D <= cdur + 0.05:
            run(["ffmpeg","-y","-i",str(A),"-t",f"{D:.3f}","-an",*ENC,str(scene_mp4)])
            label = "trim"
        else:
            factor = max(1.0, (D / 2.0) / cdur)   # slow each half to ~D/2; never speed up
            Aslow = A
            if factor > 1.001:
                Aslow = WORK / f"aslow_{s['id']:02d}.mp4"
                run(["ffmpeg","-y","-i",str(A),"-vf",f"setpts={factor:.4f}*PTS,fps={FPS}","-an",*ENC,str(Aslow)])
            B = WORK / f"b_{s['id']:02d}.mp4"
            run(["ffmpeg","-y","-i",str(Aslow),"-vf","reverse","-an",*ENC,str(B)])
            unit = WORK / f"unit_{s['id']:02d}.mp4"
            cat = WORK / f"cat_{s['id']:02d}.txt"
            cat.write_text(f"file '{Aslow.as_posix()}'\nfile '{B.as_posix()}'\n", encoding="utf-8")
            run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cat),"-c","copy",str(unit)])
            # slowed unit ≈ D; if factor capped at 1.0 (D<2·cdur) the unit is 2·cdur>D, trim to D
            run(["ffmpeg","-y","-stream_loop","-1","-i",str(unit),"-t",f"{D:.3f}","-an",*ENC,str(scene_mp4)])
            label = f"slow-boomerang x{factor:4.2f} (single drift)"
        print(f"  scene {s['id']:02d}  win={D:5.1f}s  {label}  {s['title'][:30]}")

    # layer a subtle Ken Burns over the finished scene clip (alternate push-in / pull-out)
    scene_kb = WORK / f"scenekb_{s['id']:02d}.mp4"
    push_in = (s["id"] % 2 == 1)
    ken_burns(scene_mp4, scene_kb, D, push_in)
    print(f"           + Ken Burns {'push-in' if push_in else 'pull-out'}")
    seg_paths.append(scene_kb)

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
final = ep.film_out
run(["ffmpeg","-y","-i",str(video_only),"-i",str(AUDIO),
     "-filter_complex",f"[0:v]tpad=stop_mode=clone:stop_duration={gap:.3f}[v]",
     "-map","[v]","-map","1:a",*ENC,"-c:a","aac","-b:a","192k","-shortest",str(final)])
print(f"\n[done] {final}  video_only={vdur:.1f}s + {gap:.1f}s hold -> ({dur(final):.1f}s)")
