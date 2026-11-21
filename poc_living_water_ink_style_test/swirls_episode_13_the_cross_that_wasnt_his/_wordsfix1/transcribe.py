from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
segs,_=m.transcribe("_final_16k.wav",language="en",vad_filter=False)
txt=" ".join(s.text.strip() for s in segs)
open("transcript_final.txt","w",encoding="utf-8").write(txt); print(txt)
