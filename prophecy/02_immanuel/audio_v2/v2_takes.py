r"""Words v2 re-record (owner yes ~$0.25 cap $0.40, 2026-11-16): only the new lines. Same voices/model as v1.
Narrator stability 0.65 (v1 default), angel 0.3 with emotion cues (v1 emotion_takes). Cues are not spoken.
  C:\Users\sanjay\PycharmProjects\PythonProject1\.venv\Scripts\python.exe v2_takes.py"""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
OUT = Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\02_immanuel\audio_v2\_takes")
NV, AV = "LSi9zNCeliLuhIGGS0By", "puDRtQWF8NtQiPMJygTb"
NARR = [
 ("00", "A frightened king told God no. God answered anyway."),
 ("01", "King Ahaz, from King David's family, was afraid of war. God said, \"fear not,\" and offered any sign, as proof. Ahaz refused, and begged a foreign king: \"save me.\" God chose the sign:"),
 ("03", "Seven hundred years later, Mary, a virgin, was pregnant by God's Holy Spirit."),
 ("04", "An angel told Joseph:"),
 ("07", "Joseph obeyed. Ahaz begged a king to save him. This child saves. Immanuel means: God with us."),
 ("10", "That was God's answer."),
]
ANGEL = "[gentle][reassuring][warm] Joseph, thou son of David, fear not to take unto thee Mary thy wife:"
key = os.getenv("ELEVENLABS_API_KEY")
P.STABILITY = 0.65
for n, text in NARR:
    f = OUT / f"{n}_narrator_a.mp3"
    if not f.exists(): f.write_bytes(P.render_turn(key, NV, text)); print("ok", f.name, flush=True)
P.STABILITY = 0.3
for take in ("a", "b"):
    f = OUT / f"05_angel_{take}.mp3"
    if not f.exists(): f.write_bytes(P.render_turn(key, AV, ANGEL)); print("ok", f.name, flush=True)
