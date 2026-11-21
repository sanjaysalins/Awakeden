import sys
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
for f in sys.argv[1:]:
    seg,_=m.transcribe(f,language="en",word_timestamps=True,vad_filter=False)
    print(f)
    for s in seg: print(" ",round(s.start,2),round(s.end,2),s.text, "| nospeech %.2f"%s.no_speech_prob)
