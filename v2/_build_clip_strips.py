"""Build a per-clip filmstrip review page so the user can flag clips to delete.

Usage: python v2/_build_clip_strips.py "<clips_dir>" "<out_html>" "<title>"
Extracts N evenly-spaced frames per .mp4 and lays them out one row per clip,
with the clip filename + a delete-checkbox note. $0, ffmpeg only.
"""
import sys, subprocess, json
from pathlib import Path

clips_dir = Path(sys.argv[1])
out_html = Path(sys.argv[2])
title = sys.argv[3] if len(sys.argv) > 3 else "Clip strips"
N = 8

slices_dir = out_html.parent / (out_html.stem + "_slices")
slices_dir.mkdir(parents=True, exist_ok=True)

mp4s = sorted(clips_dir.glob("*.mp4"))
rows = []
for mp4 in mp4s:
    # duration
    try:
        dur = float(subprocess.run(
            ["ffprobe","-v","error","-show_entries","format=duration","-of","json",str(mp4)],
            capture_output=True, text=True).stdout and
            json.loads(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","json",str(mp4)],capture_output=True,text=True).stdout)["format"]["duration"])
    except Exception:
        dur = 5.0
    stem = mp4.stem
    frames = []
    for i in range(N):
        t = dur * (i + 0.5) / N
        outp = slices_dir / f"{stem}_{i:02d}.jpg"
        subprocess.run(["ffmpeg","-y","-ss",f"{t:.2f}","-i",str(mp4),
                        "-frames:v","1","-vf","scale=240:-1","-q:v","4",str(outp)],
                       capture_output=True)
        if outp.exists():
            frames.append(outp.name)
    rows.append((stem, dur, frames))

rel = slices_dir.name
cards = []
for stem, dur, frames in rows:
    imgs = "".join(f'<img src="{rel}/{f}" loading="lazy">' for f in frames)
    cards.append(f"""
    <div class="clip">
      <div class="hd"><span class="name">{stem}</span><span class="dur">{dur:.1f}s</span>
        <label class="del"><input type="checkbox"> mark to DELETE</label></div>
      <div class="strip">{imgs}</div>
    </div>""")

html = f"""<!doctype html><meta charset="utf-8"><title>{title}</title>
<style>
 body{{background:#15110c;color:#eee;font-family:system-ui,Arial;margin:0;padding:24px}}
 h1{{font-weight:600;font-size:20px}}
 .sub{{color:#b59;color:#caa37a;margin-bottom:18px}}
 .clip{{background:#211a12;border:1px solid #3a2e1f;border-radius:10px;padding:12px 14px;margin:14px 0}}
 .hd{{display:flex;align-items:center;gap:16px;margin-bottom:8px}}
 .name{{font-weight:600;color:#f0d9a8}}
 .dur{{color:#9a8}}
 .del{{margin-left:auto;color:#e88;font-size:13px;cursor:pointer}}
 .strip{{display:flex;gap:4px;overflow-x:auto}}
 .strip img{{height:200px;border-radius:4px;border:1px solid #000}}
</style>
<h1>{title}</h1>
<div class="sub">{len(rows)} clips · {N} frames each (left→right = clip start→end). Tick a clip to mark it for deletion, then tell me the names.</div>
{''.join(cards)}
"""
out_html.write_text(html, encoding="utf-8")
print(f"wrote {out_html}  ({len(rows)} clips, {len(rows)*N} frames)")
