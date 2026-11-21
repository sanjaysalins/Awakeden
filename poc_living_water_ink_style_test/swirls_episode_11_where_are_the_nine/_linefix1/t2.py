import sys
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
for p,s,e in [(sys.argv[1],0,15),(sys.argv[1],68.5,83.6)]:
    import subprocess; subprocess.run(["ffmpeg","-y","-v","error","-ss",str(s),"-t",str(e-s),"-i",p,"-ac","1","-ar","16000","_seg.wav"])
    segs,_=m.transcribe("_seg.wav",language="en",word_timestamps=True)
    print("---",s,e)
    for g in segs:
        for w in g.words: print("%.2f-%.2f %s"%(w.start+s,w.end+s,w.word))
