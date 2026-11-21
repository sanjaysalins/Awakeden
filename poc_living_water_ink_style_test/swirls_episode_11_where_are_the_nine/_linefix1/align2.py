import json, subprocess, whisperx
from pathlib import Path
H=Path(__file__).resolve().parent
spoken="Nine went on clean. One came back whole: at His feet, not on the road."
m,meta=whisperx.load_align_model(language_code="en",device="cpu")
res={}
for take in "ab":
    src=H/f"last2_narrator_{take}.mp3"; wav=H/f"_last2_{take}_16k.wav"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(src),"-ac","1","-ar","16000",str(wav)],check=True)
    audio=whisperx.load_audio(str(wav)); dur=len(audio)/16000
    r=whisperx.align([{"start":0.0,"end":dur,"text":spoken}],m,meta,audio,"cpu")
    w=[{"w":x["word"],"start":round(float(x["start"]),3),"end":round(float(x["end"]),3)} for x in r["word_segments"] if "start" in x]
    res["last2_"+take]={"dur":dur,"words":w}; print(take,dur,[(x["w"],x["start"],x["end"]) for x in w])
(H/"new_last2_words_rel.json").write_text(json.dumps(res,indent=1),encoding="utf-8")
