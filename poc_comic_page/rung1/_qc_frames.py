"""Comic Page Pipeline POC -- Rung 1 Phase 2, Step 2: CSN-G5 clip QC frame
strips. For each clip, extracts 5 frames (start / quarter / mid /
three-quarter / end) into clips/_frames/<clip_stem>/ for eye-check.

  .venv\\Scripts\\python.exe poc_comic_page/rung1/_qc_frames.py <clip1.mp4> [<clip2.mp4> ...]
"""
import subprocess
import sys
from pathlib import Path


def probe_duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                         "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


def extract(clip: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    dur = probe_duration(clip)
    fracs = [0.0, 0.25, 0.5, 0.75, 0.98]  # 0.98 not 1.0 -- avoid EOF probe failure
    labels = ["start", "quarter", "mid", "three_quarter", "end"]
    paths = []
    for frac, label in zip(fracs, labels):
        t = max(0.0, dur * frac)
        out = out_dir / f"{label}_t{t:.2f}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(clip),
                        "-frames:v", "1", str(out)], check=True)
        paths.append(out)
    return paths


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    root = Path(__file__).resolve().parent / "clips" / "_frames"
    for a in sys.argv[1:]:
        clip = Path(a)
        out_dir = root / clip.stem
        paths = extract(clip, out_dir)
        print(f"[qc] {clip.name} -> {out_dir}  ({len(paths)} frames)")


if __name__ == "__main__":
    main()
