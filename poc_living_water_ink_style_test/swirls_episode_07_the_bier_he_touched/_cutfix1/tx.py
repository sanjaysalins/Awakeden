import sys, subprocess
from faster_whisper import WhisperModel
subprocess.run(["ffmpeg","-y","-v","error","-i",sys.argv[1],"-vn","-ac","1","-ar","16000","_tx.wav"],check=True)
m=WhisperModel("small.en",device="cpu",compute_type="int8")
segs,_=m.transcribe("_tx.wav",word_timestamps=True)
for s in segs: print("%.2f-%.2f %s"%(s.start,s.end,s.text.strip()))
