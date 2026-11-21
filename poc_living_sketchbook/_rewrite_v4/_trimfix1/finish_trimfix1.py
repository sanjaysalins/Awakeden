import json, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; V4 = H.parent; ROOT = V4.parents[1]
sys.path.insert(0, str(ROOT/"poc_living_sketchbook"))
import _short_captions as C
words = [{"w": x["w"], "start": x["start"], "end": x["end"]} for x in json.load(open(V4/"audio"/"bronze_serpent"/"alignment.json"))]
(H/"bronze_serpent_trimfix1.words.json").write_text(json.dumps(words, indent=0), encoding="utf-8")
cc = H/"bronze_serpent_trimfix1_cc.mp4"
C.burn(H/"bronze_serpent_trimfix1_pre.mp4", cc, words, [], H/"_cc")
out = V4/"video"/"bronze_serpent_trimfix1_cc_v5hook.mp4"
subprocess.run(["ffmpeg","-y","-v","error","-i",str(cc),"-i",str(H/"hook_card.png"),"-filter_complex","[0:v][1:v]overlay=0:0:enable='between(t,0,2.0)'[v]","-map","[v]","-map","0:a","-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart","-threads","3",str(out)],check=True)
(V4/"video"/"bronze_serpent_trimfix1_cc_v5hook.words.json").write_text(json.dumps(words, indent=0), encoding="utf-8")
print("ok", out)
