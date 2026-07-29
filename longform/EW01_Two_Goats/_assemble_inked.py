"""Assemble the EW01 Two Goats INKED 16:9 film (2026-07-22).

A faithful fork of the shared `longform/_assemble_16x9.py` window-tiled assembler
(same boomerang / forward_slow / directional fill + subtle Ken Burns + audio mux),
specialised for the inked rebuild. Two things differ, both deliberate:

  1. Paths point at `v1/visual_16x9_inked/` (stills, clips/, scene_plan.json, film).
  2. Clips are matched by the `NN_` id-prefix (`clips/{id:02d}_*.mp4`), NOT by a
     re-derived stem. `_animate_inked.stem_for` truncates titles to 46 chars while
     `_episode.slugof` truncates to 40 — they DIFFER for scenes 5/8/18/22, so an
     assembler built on `_episode.stem` would silently fail to find those 4 clips.
     The id-prefix is unambiguous (zero-padded, one clip per scene) and sidesteps
     the whole truncation trap. (RESUME red-team, 2026-07-21 night #4.)

The inked scene_plan uses a slightly different schema than the oil window-lane
(`scene_type:"jesus_link"` instead of `jesus:true`; `audio_seconds` tiling target
584.5 while the real narration.mp3 is ~588.6s — the last scene stretches to cover
the tail). The LF-AS gate is calibrated for the oil schema, so we normalise a copy
before the (still blocking) check — see `_lf_gate` below.

Output: 1920x1080 30fps + narration.mp3 -> <film_name>. ffmpeg only ($0).

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_assemble_inked.py
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = HERE / "v1" / "visual_16x9_inked"
CLIPS = OUT / "clips"
WORK = OUT / "_assembly"
WORK.mkdir(parents=True, exist_ok=True)

plan = json.loads((OUT / "scene_plan.json").read_text(encoding="utf-8"))
scenes = plan["scenes"]

AUDIO = HERE / "v1" / "narration.immersive.mp3"
if not AUDIO.exists():
    AUDIO = HERE / "v1" / "narration.mp3"
if not AUDIO.exists():
    raise SystemExit(f"missing audio: {AUDIO} (render narration.mp3 first)")

FILM = OUT / plan["film_name"]

W, H, FPS = 1920, 1080, 30
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", str(FPS)]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{' '.join(str(c) for c in cmd[:6])}...\n{r.stderr[-1200:]}")


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(p)], capture_output=True, text=True).stdout.strip())


def scaled(src, dst):
    """scale/pad any clip to 1920x1080 30fps yuv420p, no audio."""
    run(["ffmpeg", "-y", "-i", str(src),
         "-vf", f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p",
         "-an", *ENC, str(dst)])


KB_RANGE = 0.07   # subtle Ken Burns: 7% slow zoom over the window (push-in or pull-out)


def ken_burns(src, dst, D, push_in):
    """Layer a SUBTLE Ken Burns move over the finished scene clip (alternated
    push-in / pull-out per scene) so even quiet scenes carry continuous motion."""
    frames = max(2, int(round(D * FPS)))
    inc = KB_RANGE / frames
    hi = 1.0 + KB_RANGE
    if push_in:
        z = f"z='min(zoom+{inc:.6f},{hi:.4f})'"
    else:  # start zoomed, ease out to 1.0
        z = f"z='if(lte(on,1),{hi:.4f},max(zoom-{inc:.6f},1.0))'"
    vf = (f"scale={W*2}:{H*2},zoompan={z}:d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
          f"fps={FPS}:s={W}x{H}")
    run(["ffmpeg", "-y", "-i", str(src), "-vf", vf, "-an", *ENC, str(dst)])


def clip_for(s):
    """The clip for scene N is the single `NN_*.mp4` in clips/ (id-prefix match)."""
    matches = sorted(CLIPS.glob(f"{s['id']:02d}_*.mp4"))
    if not matches:
        raise SystemExit(f"missing clip for scene {s['id']:02d}: no {s['id']:02d}_*.mp4 in {CLIPS}")
    return matches[0]


def _lf_gate(audio_dur):
    """LF-AS deterministic gate (BLOCKING), normalised for the inked schema:
      - jesus flag derived from scene_type == 'jesus_link' (the inked plan has no
        `jesus:true` field; scene 25 IS jesus_link, so the gospel-close check holds).
      - audio_dur = the plan's tiling target (audio_seconds), NOT the real ~588.6s
        narration: the windows tile to 584.5 and the assembler stretches the last
        scene to cover the real tail, so passing the real dur would false-block on
        LF-AS-G1 'tail uncovered' for a tail that is genuinely covered.
    Everything else (tiling, movement coverage + clip-on-disk, gospel open) is a
    real guard and stays blocking."""
    sys.path.insert(0, str(ROOT))
    from pipeline import validators as _validators  # noqa: E402
    norm = {"scenes": [{**s, "jesus": s.get("scene_type") == "jesus_link"} for s in scenes]}
    tiling_target = plan.get("audio_seconds", scenes[-1]["t"][1])
    blk, warns = _validators.lf_assembly(norm, audio_dur=tiling_target, clips_dir=CLIPS)
    for w in warns:
        print(f"  [lf-as] warn: {w}")
    if blk:
        for b in blk:
            print(f"  [lf-as] BLOCK: {b}")
        raise SystemExit("LF-AS gate failed — fix the scene windows/plan before assembling")


audio_dur = dur(AUDIO)
print(f"EW01_Two_Goats (inked): audio {audio_dur:.1f}s · {len(scenes)} scenes · boomerang + forward_slow")
_lf_gate(audio_dur)

seg_paths = []
for i, s in enumerate(scenes):
    start, end = s["t"]
    D = (audio_dur - start) if i == len(scenes) - 1 else (end - start)
    clip = clip_for(s)
    scene_mp4 = WORK / f"scene_{s['id']:02d}.mp4"

    if s.get("fill") == "forward_slow":
        # FORWARD-ONLY, time-stretched to fill the window (no reverse). For frozen
        # tableaux whose only motion is a one-way camera push / rising light.
        A = WORK / f"a_{s['id']:02d}.mp4"
        scaled(clip, A)
        cdur = dur(A)
        factor = max(1.0, D / cdur)
        run(["ffmpeg", "-y", "-i", str(A), "-vf", f"setpts={factor:.4f}*PTS,fps={FPS}",
             "-t", f"{D:.3f}", "-an", *ENC, str(scene_mp4)])
        print(f"  scene {s['id']:02d}  win={D:5.1f}s  SLOW-FWD x{factor:4.2f} (no reverse)  {s['title'][:30]}")
    elif s.get("directional"):
        # forward-only: original + chained continuation clips, concat, trim/pad to window
        parts = [clip] + sorted(CLIPS.glob(f"{s['id']:02d}_*_cont*.mp4"))
        scaled_parts = []
        for k, p in enumerate(parts):
            sp = WORK / f"f_{s['id']:02d}_{k}.mp4"
            scaled(p, sp)
            scaled_parts.append(sp)
        fwd = WORK / f"fwd_{s['id']:02d}.mp4"
        cat = WORK / f"catf_{s['id']:02d}.txt"
        cat.write_text("".join(f"file '{p.as_posix()}'\n" for p in scaled_parts), encoding="utf-8")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(cat), "-c", "copy", str(fwd)])
        fdur = dur(fwd)
        if fdur >= D - 0.05:
            run(["ffmpeg", "-y", "-i", str(fwd), "-t", f"{D:.3f}", "-an", *ENC, str(scene_mp4)])
        else:
            run(["ffmpeg", "-y", "-i", str(fwd),
                 "-vf", f"tpad=stop_mode=clone:stop_duration={D-fdur+0.1:.3f}",
                 "-t", f"{D:.3f}", "-an", *ENC, str(scene_mp4)])
        print(f"  scene {s['id']:02d}  win={D:5.1f}s  FORWARD {len(parts)} clip(s) ({fdur:.0f}s)  {s['title'][:30]}")
    else:
        # camera-only / static: SLOW seamless boomerang — slow the clip so ONE
        # forward+reverse ping-pong fills the whole window (a single reverent drift
        # out and back). factor = (D/2)/cdur, never below 1.0 (never speed up).
        A = WORK / f"a_{s['id']:02d}.mp4"
        scaled(clip, A)
        cdur = dur(A)
        if D <= cdur + 0.05:
            run(["ffmpeg", "-y", "-i", str(A), "-t", f"{D:.3f}", "-an", *ENC, str(scene_mp4)])
            label = "trim"
        else:
            factor = max(1.0, (D / 2.0) / cdur)   # slow each half to ~D/2; never speed up
            Aslow = A
            if factor > 1.001:
                Aslow = WORK / f"aslow_{s['id']:02d}.mp4"
                run(["ffmpeg", "-y", "-i", str(A), "-vf", f"setpts={factor:.4f}*PTS,fps={FPS}", "-an", *ENC, str(Aslow)])
            B = WORK / f"b_{s['id']:02d}.mp4"
            run(["ffmpeg", "-y", "-i", str(Aslow), "-vf", "reverse", "-an", *ENC, str(B)])
            unit = WORK / f"unit_{s['id']:02d}.mp4"
            cat = WORK / f"cat_{s['id']:02d}.txt"
            cat.write_text(f"file '{Aslow.as_posix()}'\nfile '{B.as_posix()}'\n", encoding="utf-8")
            run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(cat), "-c", "copy", str(unit)])
            run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(unit), "-t", f"{D:.3f}", "-an", *ENC, str(scene_mp4)])
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
run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(seg_list), "-c", "copy", str(video_only)])
print(f"video_only {dur(video_only):.1f}s")

# concat frame-rounding leaves the video a touch short of the audio; clone the last
# frame (the hero close on Christ) up to the audio length so the close isn't clipped,
# then -shortest trims to exact audio duration.
vdur = dur(video_only)
gap = max(0.0, audio_dur - vdur) + 0.5
run(["ffmpeg", "-y", "-i", str(video_only), "-i", str(AUDIO),
     "-filter_complex", f"[0:v]tpad=stop_mode=clone:stop_duration={gap:.3f}[v]",
     "-map", "[v]", "-map", "1:a", *ENC, "-c:a", "aac", "-b:a", "192k", "-shortest", str(FILM)])
print(f"\n[done] {FILM}  video_only={vdur:.1f}s + {gap:.1f}s hold -> ({dur(FILM):.1f}s)")
