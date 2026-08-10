"""Final trailer assembly: 12 beats trimmed to fit the real narration's
own measured segment boundaries (via ffmpeg silencedetect on the actual
narration.mp3, not estimates), muxed with that real audio.

Segment 1 (narrator, 0.00-13.83s): S1 eden -> S2 fruit -> S3 running ->
  S4 hiding -> S5 sentencing -> S6 serpent
Segment 2 (GOD quote + pauses, 13.83-19.05s): S7 shadow (tail portion,
  already advancing -> arrives) -> S8 heel (arrested)
Segment 3 (narrator, 19.05-29.10s) + title hold: S9 cross -> S10 tomb ->
  S11 montage -> S12 title (extends slightly past the last word for the hold)
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLIPS = HERE / "clips"
NARR = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\05_The_Seed_Of_The_Woman\v1\_trailer\narration.mp3")
OUT = HERE / "SEED_OF_THE_WOMAN_TRAILER.mp4"

# (source_file, in_point, duration)
PLAN = [
    ("t_s1_eden_wide.mp4", 0.0, 1.6),
    ("t_s2_fruit_falling.mp4", 0.0, 1.5),
    ("t_s3_running_camerafix.mp4", 0.0, 1.5),
    ("t_s4_hiding_light_camerafix.mp4", 0.0, 2.9),
    ("t_s5_sentencing_wide.mp4", 0.0, 3.0),
    ("t_s6_serpent_sinking.mp4", 0.0, 3.33),
    ("t_s7_shadow_sweep.mp4", 2.6, 2.61),   # tail portion: already advancing -> arrives+holds
    ("t_s8_heel_strike.mp4", 0.0, 2.61),
    ("t_s9_cross_wide.mp4", 0.0, 2.3),
    ("t_s10_tomb_wide.mp4", 0.0, 0.5),   # trimmed from 2.2s: cuts away before a real AI
                                          # motion wobble in the doorway right jamb
                                          # (confirmed onset ~0.55-0.7s clip-local)
    ("t_s11_montage.mp4", 0.0, 5.167),   # extended by the 1.7s removed from S10 above
                                          # (free $0 recut, safe to lengthen)
    ("t_s12_title.mp4", 0.0, 2.6),
]

def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                           "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                          check=True, capture_output=True, text=True)
    return float(out.stdout.strip())


work = HERE / "_final_work"
work.mkdir(exist_ok=True)
trimmed = []
for i, (fname, ss, dur) in enumerate(PLAN):
    src = CLIPS / fname
    dst = work / f"seg{i:02d}.mp4"
    available = probe_duration(src) - ss
    vf = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"
    trim_t = dur
    if dur > available + 0.01:
        # requested duration exceeds this source's real footage (e.g. S11's
        # montage extended to cover the time trimmed off S10's wobble) --
        # hold the clip's own last frame for the shortfall instead of
        # inventing new content.
        vf += f",tpad=stop_mode=clone:stop_duration={dur - available:.3f}"
        trim_t = available
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{trim_t:.3f}",
                     "-i", str(src), "-an", "-vf", vf, "-t", f"{dur:.3f}",
                     "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", str(dst)], check=True)
    trimmed.append(dst)

concat_list = work / "_list.txt"
concat_list.write_text("\n".join(f"file '{p.resolve().as_posix()}'" for p in trimmed) + "\n", encoding="utf-8")
silent = work / "_silent.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_list),
                 "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", str(silent)], check=True)

video_dur = sum(d for _, _, d in PLAN)
print(f"[info] total video duration: {video_dur:.3f}s")

subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(NARR),
                 "-map", "0:v", "-map", "1:a", "-t", f"{video_dur:.3f}",
                 "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(OUT)], check=True)
print(f"[done] {OUT}")
