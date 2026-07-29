"""Comic Page Pipeline POC -- Rung 2 FINAL PHASE, Step 6: assemble the
finished comic-page short. $0, deterministic ffmpeg.

  concat page1..page5 (with-text versions where they exist, else the plain
  composite) hard-cut, no transitions
  -> mux full narration.mp3 with apad to the video's exact duration
     (INV-26: audio track duration == video track duration)
  -> add_watermark.py (top-left, 9:16 portrait position)

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_assemble_final.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NARR_MP3 = (ROOT.parent / "PythonProject1" / "jesus" / "narration" /
            "36_In_No_Wise_Cast_Out" / "v1" / "narration.mp3")

# with-text version if the page has one, else the plain composite
PAGE_SOURCES = {
    "page1": HERE / "page1_composite.mp4",
    "page2": HERE / "page2_with_text.mp4",
    "page3": HERE / "page3_with_text.mp4",
    "page4": HERE / "page4_composite.mp4",
    "page5": HERE / "page5_with_text.mp4",
}

CONCAT_MP4 = HERE / "_concat_silent.mp4"
MUXED_MP4 = HERE / "IN_NO_WISE_comic_v1.mp4"


def probe_duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    for name, p in PAGE_SOURCES.items():
        if not p.exists():
            raise SystemExit(f"missing {name} source: {p}")
    if not NARR_MP3.exists():
        raise SystemExit(f"missing narration mp3: {NARR_MP3}")

    listfile = HERE / "_concat_list.txt"
    listfile.write_text("".join(f"file '{PAGE_SOURCES[k].resolve().as_posix()}'\n"
                                 for k in ["page1", "page2", "page3", "page4", "page5"]))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(listfile), "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-r", "24", str(CONCAT_MP4)], check=True)
    vdur = probe_duration(CONCAT_MP4)
    print(f"[concat] {CONCAT_MP4} -> {vdur:.3f}s")

    adur = probe_duration(NARR_MP3)
    print(f"[narration] {NARR_MP3} -> {adur:.3f}s")

    # apad the narration to EXACTLY match the video's duration (INV-26: audio
    # track duration must equal video track duration, never a shortest-cutoff)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(CONCAT_MP4), "-i", str(NARR_MP3),
                    "-filter_complex", f"[1:a]apad=whole_dur={vdur:.3f}[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", str(MUXED_MP4)], check=True)
    v2, = [probe_duration(MUXED_MP4)]
    print(f"[mux] {MUXED_MP4} -> {v2:.3f}s")

    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration",
                        "-of", "csv=p=0", str(MUXED_MP4)], capture_output=True, text=True)
    print(f"[streams] {r.stdout.strip()}")


if __name__ == "__main__":
    main()
