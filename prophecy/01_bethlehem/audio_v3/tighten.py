"""$0: cap internal pauses in the NEW narrator turns (01, 03, 07) at CAP s, then atempo ATEMPO (3%, inaudible).
Writes _turns/NN_narrator__atempo.mp3 (raw NN_narrator.mp3 untouched). Old turns keep their approved audio."""
import re, subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
CAP, ATEMPO = 0.45, 1.03
def run(*a): return subprocess.run(a, capture_output=True, text=True)
for t in ("01", "03", "07"):
    src = H / "_turns" / f"{t}_narrator.mp3"
    d = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)).stdout)
    e = run("ffmpeg", "-hide_banner", "-i", str(src), "-af", "silencedetect=n=-38dB:d=0.25", "-f", "null", "-").stderr
    ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", e)]; se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", e)]
    keep, cur = [], 0.0
    for a, b in zip(ss, se):
        if b - a > CAP and b < d - 0.05:
            cut0, cut1 = a + CAP / 2, b - CAP / 2
            keep.append((cur, cut0)); cur = cut1
    keep.append((cur, d))
    sel = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in keep)
    out = H / "_turns" / f"{t}_narrator__atempo.mp3"
    r = run("ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", f"aselect='{sel}',asetpts=N/SR/TB,atempo={ATEMPO}",
            "-c:a", "libmp3lame", "-b:a", "128k", str(out))
    assert r.returncode == 0, r.stderr
    nd = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)).stdout)
    print(t, f"{d:.2f} -> {nd:.2f}")
