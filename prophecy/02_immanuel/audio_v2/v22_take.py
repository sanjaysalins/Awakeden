r"""Words v2.2 (owner yes, ~$0.05, 2026-11-16): film re-check fix (3 seats: film never says it came true). Was:
order the Bible does not give). Re-record narrator line 01 only, same voice + stability 0.65 as the other v2 lines."""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
P.STABILITY = 0.65
OUT = Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\02_immanuel\audio_v2\_takes\03_narrator_v22.mp3")
TEXT = "Seven hundred years later, it came true. Mary, a virgin, was pregnant by God's Holy Spirit."
if not OUT.exists(): OUT.write_bytes(P.render_turn(os.getenv("ELEVENLABS_API_KEY"), "LSi9zNCeliLuhIGGS0By", TEXT)); print("ok", OUT.name)
