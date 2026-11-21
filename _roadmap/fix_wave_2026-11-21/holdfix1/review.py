import subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); import holdfix1 as H
F = {"thy": dict(title="Father, into thy hands (Luke 23:46)", old_t=[13.0, 24.5, 58.5, 58.9], new_t=[13.0, 24.5, 59.5, 61.5],
        cap=["Gloss cards REDEEMED = BOUGHT BACK and COMMEND = ENTRUST removed", "Ending: hold 0.10 s -> 3.15 s: a closing 3.07 s beat of unseen frames of the morning clip (first_day_morning, from 1.78 s), real frames, no freeze/loop", "Score fades over the last 2.5 s to silence", "Kept: new first line + hook card"],
        nums="video 62.099 s = audio 62.100 s. Last word 58.949 s. Hold 3.150 s."),
     "forsaken": dict(title="Forsaken cry (ps22-03)", old_t=[1.0, 22.0, 57.0, 58.1], new_t=[1.0, 22.0, 57.0, 60.5],
        cap=["Hook card: 'WHY DID JESUS CRY THIS?' (not spoken) -> 'FROM THE CROSS, / IN HIS DARKEST HOUR' (spoken 0.1-2.0 s)", "Gloss card 'FORSAKEN = ABANDONED' removed", "Ending: hold 0.11 s -> 3.08 s, score fades over the last 2.5 s to silence"],
        nums="video 61.167 s = audio 61.166 s. Last word 58.084 s. Hold 3.083 s."),
     "fin": dict(title="It is finished (john 19:30)", old_t=[1.0, 39.5, 57.0, 58.9], new_t=[1.0, 39.5, 57.5, 60.5],
        cap=["Gloss card 'GAVE UP THE GHOST = DIED' removed", "Ending: hold 0.06 s -> 3.07 s, score fades over the last 2.5 s to silence", "Not changed (not in brief): hook card 'WHAT WAS FINISHED?'"],
        nums="video 62.100 s = audio 62.100 s. Last word 59.034 s. Hold 3.066 s.")}
for f, d in F.items():
    if len(sys.argv) > 1 and f not in sys.argv[1:]: continue
    c, V, P = H.paths(f); R = V / "_holdfix1_review"; R.mkdir(exist_ok=True)
    old = V / c["pinned"]; new = V / (c["new"] + ".mp4"); imgs = []
    for k, (src, ts) in enumerate(((old, d["old_t"]), (new, d["new_t"]))):
        for t in ts:
            n = f"{'old' if k == 0 else 'new'}_{t}.jpg"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(src), "-frames:v", "1", "-vf", "scale=360:-1", str(R / n)], check=True); imgs.append(n)
    row = lambda pre, ts: "".join(f'<a href="{pre}_{t}.jpg"><img src="{pre}_{t}.jpg"></a>' for t in ts)
    html = f"""<!doctype html><meta charset=utf-8><title>{d['title']} holdfix1</title><style>body{{font:22px Arial;margin:24px;background:#fafafa}}img{{height:420px;margin:4px;border:2px solid #333}}h2{{margin-top:28px}}li{{margin:8px 0}}</style>
<h1>{d['title']} - hold fix</h1><h2>What changed</h2><ul>{''.join('<li>'+x+'</li>' for x in d['cap'])}</ul><p><b>{d['nums']}</b></p>
<h2>OLD (times {d['old_t']} s)</h2>{row('old', d['old_t'])}<h2>NEW (times {d['new_t']} s)</h2>{row('new', d['new_t'])}
<p>New film: <a href="file:///{new.as_posix()}">{new}</a></p>"""
    (V.parent / f"_HOLDFIX1_REVIEW.html").write_text(html, encoding="utf-8"); print(V.parent / "_HOLDFIX1_REVIEW.html")
