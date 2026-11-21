import json, subprocess, whisperx
from pathlib import Path
H=Path(__file__).resolve().parent
T={"first":"Ten sick men begged Jesus for mercy. He sent them off, still sick.",
   "last":"Nine went on clean. One, face down at His feet, went on whole."}
m,meta=whisperx.load_align_model(language_code="en",device="cpu")
res={}
for which,spoken in T.items():
  for take in "ab":
    src=H/f"{which}_narrator_{take}.mp3"; wav=H/f"_{which}_{take}_16k.wav"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(src),"-ac","1","-ar","16000",str(wav)],check=True)
    audio=whisperx.load_audio(str(wav)); dur=len(audio)/16000
    r=whisperx.align([{"start":0.0,"end":dur,"text":spoken}],m,meta,audio,"cpu")
    w=[{"w":x["word"],"start":round(x["start"],3),"end":round(x["end"],3)} for x in r["word_segments"] if "start" in x]
    res[f"{which}_{take}"]={"dur":dur,"words":w}
    print(which,take,dur,[(x["w"],x["start"],x["end"]) for x in w])
(H/"new_lines_words_rel.json").write_text(json.dumps(res,indent=1),encoding="utf-8")
