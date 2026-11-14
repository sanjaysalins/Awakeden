r"""Re-record the 5 character lines (Bartimaeus) with eleven_v3 emotion cues, 2 takes each (owner yes, part of ~$0.50 voice, 2026-11-13).
Reuses per_turn_synth.render_turn (no duplicate pipeline). Cues are performance tags, not spoken; KJV text unchanged.
  PythonProject1\.venv\Scripts\python.exe emotion_takes.py"""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
P.STABILITY = 0.3   # v3: lower = more expressive ("creative" side of natural)
HERE = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_desert_storybook_heroes\bartimaeus\audio"); OUT = HERE/"_takes"; OUT.mkdir(exist_ok=True)
V = {"jesus": "tlETan7Okc4pzjD0z62P", "bartimaeus": "puDRtQWF8NtQiPMJygTb"}
LINES = [
 ("00", "bartimaeus", "[shouting][desperate] Jesus, thou Son of David, have mercy on me."),
 ("04", "bartimaeus", "[shouting louder][pleading] Thou Son of David, have mercy on me."),
 ("07", "jesus", "[gently][warmly] What wilt thou that I should do unto thee?"),
 ("08", "bartimaeus", "[hopeful][trembling] Lord, that I might receive my sight."),
 ("09", "jesus", "[warmly][tenderly] Go thy way; thy faith hath made thee whole."),
]
key = os.getenv("ELEVENLABS_API_KEY")
for n, who, text in LINES:
    for take in ("a", "b"):
        f = OUT/f"{n}_{who}_{take}.mp3"
        if f.exists(): continue
        f.write_bytes(P.render_turn(key, V[who], text)); print("ok", f.name, flush=True)
