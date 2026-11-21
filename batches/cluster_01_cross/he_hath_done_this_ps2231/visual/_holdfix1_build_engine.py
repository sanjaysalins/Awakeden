r"""holdfix1 (he_hath_done_this) engine wrapper: runs the stock livingpage engine on the 2-beat tail spec, with ONE seam patched:
cap["word_t"] (seconds from beat start, one per caption word) makes the kinetic caption reveal each word AT its
spoken time instead of an even cascade. Nothing else in the engine is touched.
  .venv\Scripts\python.exe visual\_holdfix1_build_engine.py"""
import sys, subprocess
from pathlib import Path
ENG = Path(r"F:\slk\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross")
sys.path.insert(0, str(ENG))
import build_livingpage_16x9 as E
base = E.base
_orig = base.apply_kinetic

def apply_kinetic(seg, cap, sol, dur, stem, delay=0.0):
    wt = cap.get("word_t")
    if not wt:
        return _orig(seg, cap, sol, dur, stem, delay)
    paths = base.cr.render_kinetic_states(cap.get("kw", ""), sol, base.PAGE, base.WORK, stem)
    n = len(paths)
    assert n == len(wt), f"caption words {n} != word_t {len(wt)}"
    bounds = wt[1:]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg)]
    for p in paths:
        cmd += ["-loop", "1", "-t", f"{dur}", "-i", str(p)]
    parts = [f"[1:v]format=rgba,fade=t=in:st={wt[0]:.3f}:d=0.12:alpha=1[k1]"]
    for j in range(2, n + 1):
        parts.append(f"[{j}:v]format=rgba[k{j}]")
    prev = "0:v"
    for idx in range(1, n + 1):
        a = wt[0] if idx == 1 else bounds[idx - 2]
        en = f"between(t,{a:.3f},{bounds[idx-1]:.3f})" if idx < n else f"gte(t,{a:.3f})"
        out = f"o{idx}" if idx < n else "outv"
        parts.append(f"[{prev}][k{idx}]overlay=0:0:enable='{en}'[{out}]"); prev = out
    tmp = seg.with_name(seg.stem + "_kc.mp4")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[outv]", "-r", "30",
            "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(tmp)]
    base.run(cmd, f"kinetic caption {stem}")
    tmp.replace(seg)

base.apply_kinetic = apply_kinetic
POOL = Path(__file__).resolve().parent / "_holdfix1_pool"
SPECNAME = sys.argv[1] if len(sys.argv)>1 else "holdfix1_tail.spec.json"
sys.argv = ["build_livingpage_16x9.py", "--pool", str(POOL), "--spec", SPECNAME,
            "--page", "1080x1920", "--clips"] + ([] if __import__("os").environ.get("LF1_SFX") else ["--no-sfx"])
E.main()
