r"""Empty Tomb endfix1: record ONLY the new closing line. Same voice/model/settings as the original (eleven_v3, stability 0.5,
narrator LSi9zNCeliLuhIGGS0By). Cap $0.30 (owner). Takes a, b.  Run with PythonProject1 venv."""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
OUT = Path(r"F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_02_resurrection\empty_tomb_john208\audio\_endfix1")
NV = "LSi9zNCeliLuhIGGS0By"
TEXT = "You were not there. He spoke about you anyway, and called you blessed."
key = os.getenv("ELEVENLABS_API_KEY")
assert P.STABILITY == 0.5 and P.MODEL_ID == "eleven_v3"
for take in sys.argv[1:] or ["a"]:
    f = OUT / f"28_narrator_{take}.mp3"
    if not f.exists():
        f.write_bytes(P.render_turn(key, NV, TEXT)); print("ok", f.name, len(TEXT), "chars", flush=True)
