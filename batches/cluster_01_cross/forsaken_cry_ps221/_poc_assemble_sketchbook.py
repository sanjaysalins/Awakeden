"""POC -- assemble the 2 new sketchbook stills with their EXACT matching real
narration audio windows + real word alignment, then burn Noah's exact hand-ink
caption style on top (_short_captions.py, unchanged). A compact, honest pairing:
each still gets only the real narration seconds it was drawn for, nothing
invented or padded.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/forsaken_cry_ps221/_poc_assemble_sketchbook.py
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.resolve().parents[2]
sys.path.insert(0, str(ROOT / "poc_living_sketchbook"))
sys.path.insert(0, str(ROOT / "poc_castbible_look"))
from _short_captions import burn  # noqa: E402
from _polite import be_polite  # noqa: E402

AUD = HERE / "audio" / "narration.mp3"
STILLS = HERE / "_poc_sketchbook_stills"
WORK = HERE / "_poc2_work"
SILENT = HERE / "_poc2_silent.mp4"
MUXED = HERE / "_poc2_muxed.mp4"
OUT = HERE / "_POC2_sketchbook_art_and_captions.mp4"

W, H = 1080, 1920

# (still, window_start, window_end)
SEGMENTS = [
    ("s_golgotha_sketchbook.png", 9.8, 15.05),
    ("s_bowedhead_sketchbook.png", 27.15, 31.9),
]


def main():
    be_polite()
    WORK.mkdir(exist_ok=True)

    # 1) build each still-hold video clip at its real beat duration
    clip_files = []
    for i, (name, t0, t1) in enumerate(SEGMENTS):
        out = WORK / f"seg_{i}.mp4"
        dur = t1 - t0
        cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(STILLS / name),
               "-t", f"{dur:.3f}",
               "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
               "-an", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out)]
        subprocess.run(cmd, check=True)
        clip_files.append(out)

    concat_list = WORK / "_concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in clip_files) + "\n", encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                     "-i", str(concat_list), "-c", "copy", str(SILENT)], check=True)
    print(f"[ok] {SILENT}")

    # 2) extract + concat the exact matching real narration windows
    aud_segs = []
    for i, (name, t0, t1) in enumerate(SEGMENTS):
        out = WORK / f"aud_{i}.aac"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(AUD),
                         "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}",
                         "-c:a", "aac", "-b:a", "192k", str(out)], check=True)
        aud_segs.append(out)
    aud_concat_list = WORK / "_aud_concat.txt"
    aud_concat_list.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in aud_segs) + "\n", encoding="utf-8")
    aud_out = WORK / "_aud_full.aac"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                     "-i", str(aud_concat_list), "-c", "copy", str(aud_out)], check=True)

    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(SILENT), "-i", str(aud_out),
                     "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", str(MUXED)], check=True)
    print(f"[ok] {MUXED}")

    # 3) shift real alignment words into the new compact timeline
    all_words = json.loads((HERE / "audio" / "alignment.json").read_text(encoding="utf-8"))
    words = []
    running = 0.0
    for (name, t0, t1) in SEGMENTS:
        dur = t1 - t0
        for w in all_words:
            if w["start"] >= t0 and w["end"] <= t1:
                words.append({"w": w["w"], "start": w["start"] - t0 + running,
                              "end": w["end"] - t0 + running})
        running += dur

    burn(MUXED, OUT, words, skip_windows=[], work_dir=HERE / "_poc2_caption_frames")


if __name__ == "__main__":
    main()
