"""Captions (film's _short_captions.burn, new alignment, skip the verse-card window) then 0-2.0 s hook card; audio copied."""
import json, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; ST = H.parent
sys.path.insert(0, str(ST.parent))
import _short_captions as C
words = [{"w": x["w"], "start": x["start"], "end": x["end"]} for x in json.load(open(H/"alignment_wordsfix1.json")) if any(c.isalnum() for c in x["w"])]
(ST/"STORM_wordsfix1.words.json").write_text(json.dumps(words, indent=0), encoding="utf-8")
cc = H/"wordsfix1_cc.mp4"
C.burn(H/"wordsfix1_pre.mp4", cc, words, [(16.93, 20.48)], H/"_cc")
out = ST/"STORM_living_sketchbook_cc_v5hook_wordsfix1.mp4"
subprocess.run(["ffmpeg","-y","-v","error","-i",str(cc),"-i",str(H/"hook_card.png"),"-filter_complex","[0:v][1:v]overlay=0:0:enable='between(t,0,2.0)'[v]","-map","[v]","-map","0:a","-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(out)],check=True)
print("ok", out)
