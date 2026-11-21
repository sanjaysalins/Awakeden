"""Captions (film's own _short_captions.burn, words = new alignment; no watermark, like the shipped v5hook) then the 0-2.0 s hook card, audio copied."""
import json, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; ROOT = H.parents[2]
sys.path.insert(0, str(ROOT/"poc_living_sketchbook"))
import _short_captions as C
words = [{"w": x["w"], "start": x["start"], "end": x["end"]} for x in json.load(open(H/"alignment_linefix1.json"))]
(H/"jericho_linefix2.words.json").write_text(json.dumps(words, indent=0), encoding="utf-8")
cc = H/"jericho_linefix2_cc.mp4"
C.burn(H/"jericho_linefix2_pre.mp4", cc, words, [], H/"_cc2")
out = H/"jericho_linefix2_cc_v5hook.mp4"
subprocess.run(["ffmpeg","-y","-v","error","-i",str(cc),"-i",str(H/"hook_card.png"),"-filter_complex","[0:v][1:v]overlay=0:0:enable='between(t,0,2.0)'[v]","-map","[v]","-map","0:a","-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart","-threads","3",str(out)],check=True)
print("ok", out)
