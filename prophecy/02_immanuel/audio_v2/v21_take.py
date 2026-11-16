r"""Words v2.1 (owner 'go with your pick', ~$0.05, 2026-11-16): film-check fix (3 seats: 'refused, and begged' implied an
order the Bible does not give). Re-record narrator line 01 only, same voice + stability 0.65 as the other v2 lines."""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
P.STABILITY = 0.65
OUT = Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\02_immanuel\audio_v2\_takes\01_narrator_v21.mp3")
TEXT = "King Ahaz, from King David's family, was afraid of war. God said, \"fear not,\" and offered any sign, as proof. Ahaz refused. In that same war, he begged a foreign king: \"save me.\" God chose the sign:"
if not OUT.exists(): OUT.write_bytes(P.render_turn(os.getenv("ELEVENLABS_API_KEY"), "LSi9zNCeliLuhIGGS0By", TEXT)); print("ok", OUT.name)
