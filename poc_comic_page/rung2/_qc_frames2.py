"""Same as rung1/_qc_frames.py but writes into THIS dir's clips/_frames/ (the
rung1 version hardcodes its own directory as the frames root)."""
import subprocess
import sys
from pathlib import Path


def probe_duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


def extract(clip: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    dur = probe_duration(clip)
    fracs = [0.0, 0.25, 0.5, 0.75, 0.98]
    labels = ["start", "quarter", "mid", "three_quarter", "end"]
    for frac, label in zip(fracs, labels):
        t = max(0.0, dur * frac)
        out = out_dir / f"{label}_t{t:.2f}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(clip),
                        "-frames:v", "1", str(out)], check=True)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent / "clips" / "_frames"
    for a in sys.argv[1:]:
        clip = Path(a)
        out_dir = root / clip.stem
        extract(clip, out_dir)
        print(f"[qc] {clip.name} -> {out_dir}")
