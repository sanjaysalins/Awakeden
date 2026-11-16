r"""Isaiah, angel, Jesus lines with eleven_v3 emotion cues, 2 takes each (owner yes ~$0.40 cap $0.60, 2026-11-15).
Cues are performance tags, not spoken; KJV text unchanged.  PythonProject1\.venv\Scripts\python.exe emotion_takes.py"""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
P.STABILITY = 0.3
OUT = Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\02_immanuel\audio\_takes"); OUT.mkdir(exist_ok=True)
V = {"prophet": "UzI1NsMEV3ni5JRkRSls", "angel": "puDRtQWF8NtQiPMJygTb", "jesus": "tlETan7Okc4pzjD0z62P"}
LINES = [
 ("02", "prophet", "[solemn][slowly][with quiet wonder] Behold, a virgin shall conceive, and bear a son, and shall call his name Immanuel."),
 ("05", "angel", "[gentle][reassuring][warm] thou shalt call his name JESUS: for he shall save his people from their sins."),
 ("08", "jesus", "[warm][tender][steady] I am with you alway."),
]
key = os.getenv("ELEVENLABS_API_KEY")
for n, who, text in LINES:
    for take in ("a", "b"):
        f = OUT / f"{n}_{who}_{take}.mp3"
        if f.exists(): continue
        f.write_bytes(P.render_turn(key, V[who], text)); print("ok", f.name, flush=True)
