import json, subprocess
from pathlib import Path
H=Path(__file__).resolve().parent; A=H.parent
LEAD=0.25; B1=4.7
w=json.loads((H/"new_first_words_rel.json").read_text())["a"]["words"]
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(H/"first_a.wav"),"-i",str(A/"narration.mp3"),"-filter_complex",
 f"[0:a]aresample=44100,aformat=channel_layouts=mono,adelay={int(LEAD*1000)},apad=whole_dur={B1}[a];"
 f"[1:a]atrim=7.8333:12.0333,asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=mono[b];[a][b]concat=n=2:v=0:a=1[o]",
 "-map","[o]","-ar","44100","-ac","1",str(H/"head_narr_new.wav")],check=True)
print([round(x["start"]+LEAD,3) for x in w]); print(len(w))
