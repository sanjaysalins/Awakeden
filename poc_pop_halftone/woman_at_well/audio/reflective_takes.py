r"""Re-record the woman's line 12 quieter and reflective, 2 takes (owner yes 2026-11-13). Reuses per_turn_synth.render_turn."""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
P.STABILITY = 0.3
OUT = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_pop_halftone\woman_at_well\audio\_takes")
key = os.getenv("ELEVENLABS_API_KEY")
TXT = "[quietly][in awe][slowly, with wonder] Come, see a man, which told me all things that ever I did: is not this the Christ?"
for take in ("c", "d"):
    f = OUT/f"12_woman_{take}.mp3"
    if not f.exists(): f.write_bytes(P.render_turn(key, "NbkKnEAZ7Bqw4EAkVEaz", TXT)); print("ok", f.name, flush=True)
