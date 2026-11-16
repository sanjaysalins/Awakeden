r"""Turn 06 retake: raw take slurs "Jesus says" into "Jesus as". Same locked words; a TTS-only comma gives a clean break. 2 takes, within the ~$0.60 voice cap."""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
P.STABILITY = 0.65
OUT = Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\02_immanuel\audio\_takes")
TEXT = "Matthew's book about Jesus, says the promise came true. Jesus is that promised son, and His other name, Immanuel, means: God with us."
key = os.getenv("ELEVENLABS_API_KEY")
for take in ("a", "b"):
    f = OUT / f"06_narrator_{take}.mp3"
    if not f.exists(): f.write_bytes(P.render_turn(key, "LSi9zNCeliLuhIGGS0By", TEXT)); print("ok", f.name, flush=True)
