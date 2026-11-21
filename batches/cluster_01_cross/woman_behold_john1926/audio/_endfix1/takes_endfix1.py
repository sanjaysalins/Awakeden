r"""Woman Behold endfix1: re-record ONLY the new closing line. Same voice/model/settings as v1 (eleven_v3, stability 0.65).
Cap $0.30 (owner). Takes a, b.  Run with PythonProject1 venv."""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
OUT = Path(__file__).resolve().parent if "__file__" in globals() else Path(".")
NV = "LSi9zNCeliLuhIGGS0By"
TEXT = "He was dying, and He made sure His mother did not go home alone."
key = os.getenv("ELEVENLABS_API_KEY")
P.STABILITY = 0.65
for take in sys.argv[1:] or ["a"]:
    f = OUT / f"15_narrator_{take}.mp3"
    if not f.exists():
        f.write_bytes(P.render_turn(key, NV, TEXT)); print("ok", f.name, len(TEXT), "chars", flush=True)
