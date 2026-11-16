r"""Prophet + scribe lines with eleven_v3 emotion cues, 2 takes each (owner yes, part of ~$0.50 voice, 2026-11-14).
Reuses per_turn_synth.render_turn. Cues are performance tags, not spoken; KJV text unchanged.
  PythonProject1\.venv\Scripts\python.exe emotion_takes.py"""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
P.STABILITY = 0.3
HERE = Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\01_bethlehem\audio"); OUT = HERE/"_takes"; OUT.mkdir(exist_ok=True)
V = {"prophet": "UzI1NsMEV3ni5JRkRSls", "scribe": "SOYHLrjzK2X1ezoPC6cr"}
LINES = [
 ("02", "prophet", "[solemn][slowly][with quiet wonder] But thou, Bethlehem... out of thee shall he come forth unto me that is to be ruler in Israel."),
 ("04", "scribe", "[matter-of-fact][confident] In Bethlehem of Judaea."),
]
key = os.getenv("ELEVENLABS_API_KEY")
for n, who, text in LINES:
    for take in ("a", "b"):
        f = OUT/f"{n}_{who}_{take}.mp3"
        if f.exists(): continue
        f.write_bytes(P.render_turn(key, V[who], text)); print("ok", f.name, flush=True)
