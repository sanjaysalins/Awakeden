"""Per-SLICE clip QC — break every gallery clip into 1-second slices, tile them into one
filmstrip per clip (numbered), so each slice can be judged against the omit-rules. Builds
the filmstrips + an index; the vision verdict (auto-omit) runs on top of these.
Run:  _clip_slice_qc.py EW02_Abraham EW03_Joseph"""
import sys, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def dur(f):
    o = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of",
        "default=nk=1:nw=1",str(f)],capture_output=True,text=True).stdout.strip()
    return float(o) if o else 0.0

eps = sys.argv[1:] or ["EW02_Abraham","EW03_Joseph"]
cards = []
for ep in eps:
    gc = ROOT/"longform"/ep/"v1"/"short"/"gallery_clips"
    qc = gc/"_qc"; qc.mkdir(exist_ok=True)
    clips = sorted(gc.glob("[0-9][0-9]_*.mp4"))
    rows = []
    for clip in clips:
        d = dur(clip); n = max(1, int(round(d)))           # ~1 frame per second
        strip = qc/f"{clip.stem}.strip.jpg"
        # fps=1 -> one frame/sec; number each slice; tile into a single row
        vf = f"fps=1,scale=150:-1,tile={n}x1:padding=2:color=black"   # slices left->right, 0-indexed
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(clip),"-vf",vf,
                        "-frames:v","1",str(strip)], check=False)
        uri = "file:///" + str(strip).replace("\\","/")
        rows.append(f'<div class="clip"><div class="nm">{clip.stem} &middot; {d:.0f}s &middot; {n} slices</div>'
                    f'<img src="{uri}"></div>')
    cards.append(f'<section><h2>{ep}</h2>{"".join(rows)}</section>')
    print(f"{ep}: {len(clips)} clips sliced -> {qc}")

html = ("<!doctype html><meta charset=utf-8><title>Per-slice clip QC</title>"
 "<style>body{background:#141210;color:#e8e0d2;font-family:system-ui;margin:0;padding:20px}"
 "h2{color:#e7c98a}.clip{margin:0 0 14px}.nm{font-size:13px;color:#c8b48a;margin-bottom:3px}"
 "img{max-width:100%;border:1px solid #333;border-radius:4px}</style>"
 "<h1>Per-1s-slice clip QC — flag bad slices/clips</h1>" + "".join(cards))
out = ROOT/"longform/_clip_slice_qc.html"; out.write_text(html, encoding="utf-8")
print(f"\nindex -> {out}")
