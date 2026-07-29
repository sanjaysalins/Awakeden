"""Comic Page Pipeline POC -- Rung 2 v2.1: extend the NEW p5a embrace clip
(10.04s, 241 frames @24fps) to the page5 dwell (13.9167s, 334 frames @24fps,
matching sibling p5b/p5c extended clips) WITHOUT boomerang -- the embrace is
directional (approach -> hug -> hold), so reversing it would un-hug them.

Method: play the full embrace forward once, then hold the last frame with a
slow Ken Burns push-in (1.00 -> 1.06 zoom) for the remaining ~3.88s -- reads
as the camera lingering on the completed embrace, not a freeze-frame.

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_extend_p5a_holdzoom.py
"""
from __future__ import annotations
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "clips" / "p5a.mp4"
OUT = HERE / "clips" / "extended" / "p5a.mp4"
BACKUP = HERE / "clips" / "extended" / "p5a.v1_calmhold_extended.mp4"

TARGET_FRAMES = 334  # matches p5b/p5c extended (13.9167s @ 24fps)
FPS = 24
ZOOM_END = 1.06


def probe(path: Path, entry: str) -> str:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                         "-show_entries", f"stream={entry}", "-of", "csv=p=0", str(path)],
                        capture_output=True, text=True)
    return r.stdout.strip()


def main():
    if OUT.exists() and not BACKUP.exists():
        OUT.rename(BACKUP)
        print(f"[backup] old extended p5a -> {BACKUP.name}")

    w, h = probe(SRC, "width"), probe(SRC, "height")
    src_frames = int(probe(SRC, "nb_frames"))
    tail_frames = TARGET_FRAMES - src_frames
    print(f"[info] src {SRC.name}: {w}x{h}, {src_frames} frames @ {FPS}fps; "
          f"tail needed: {tail_frames} frames ({tail_frames / FPS:.3f}s)")
    assert tail_frames > 0, "source already >= target length"

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        norm = td / "norm.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(SRC), "-an",
                        "-r", str(FPS), "-pix_fmt", "yuv420p",
                        "-c:v", "libx264", "-crf", "18", str(norm)], check=True)

        last_png = td / "last.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.08", "-i", str(SRC),
                        "-vframes", "1", str(last_png)], check=True)

        tail = td / "tail.mp4"
        zoom_expr = f"min(zoom+{(ZOOM_END - 1.0) / tail_frames:.6f},{ZOOM_END})"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(last_png),
                        "-vf", f"scale={w}:{h},zoompan=z='{zoom_expr}':d=1:s={w}x{h}:fps={FPS}",
                        "-frames:v", str(tail_frames), "-an", "-pix_fmt", "yuv420p",
                        "-c:v", "libx264", "-crf", "18", str(tail)], check=True)

        listfile = td / "list.txt"
        listfile.write_text(f"file '{norm.as_posix()}'\nfile '{tail.as_posix()}'\n")
        OUT.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                        "-i", str(listfile), "-c", "copy", str(OUT)], check=True)

    out_frames = int(probe(OUT, "nb_frames"))
    out_dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                     "format=duration", "-of", "csv=p=0", str(OUT)],
                                    capture_output=True, text=True).stdout.strip())
    print(f"[ok] {OUT} -> {out_frames} frames, {out_dur:.4f}s "
          f"(target {TARGET_FRAMES} frames, {TARGET_FRAMES / FPS:.4f}s)")


if __name__ == "__main__":
    main()
