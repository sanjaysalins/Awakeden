import json, subprocess, sys, whisperx
from pathlib import Path
H=Path(__file__).resolve().parent
spoken="Afraid God is angry with you? Watch where Jesus stopped reading."
m,meta=whisperx.load_align_model(language_code="en",device="cpu")
for t in sys.argv[1:]:
    wav=H/f"_{t}16k.wav"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(H/f"00_narrator_{t}.mp3"),"-ac","1","-ar","16000",str(wav)],check=True)
    audio=whisperx.load_audio(str(wav)); dur=len(audio)/16000
    r=whisperx.align([{"start":0.0,"end":dur,"text":spoken}],m,meta,audio,"cpu")
    w=[{"w":x["word"],"start":round(x["start"],3),"end":round(x["end"],3)} for x in r["word_segments"] if "start" in x]
    (H/f"words_{t}.json").write_text(json.dumps(w),encoding="utf-8"); print(t,dur,[(x['w'],x['start'],x['end']) for x in w])
