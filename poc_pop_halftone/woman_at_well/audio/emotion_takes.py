r"""Re-record the 5 dialogue lines with eleven_v3 emotion cues, 2 takes each (owner yes ~$0.20, 2026-11-13).
Reuses per_turn_synth.render_turn (no duplicate pipeline). Cues are performance tags, not spoken; KJV text unchanged.
  PythonProject1\.venv\Scripts\python.exe emotion_takes.py"""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
P.STABILITY = 0.3   # v3: lower = more expressive ("creative" side of natural)
HERE = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_pop_halftone\woman_at_well\audio"); OUT = HERE/"_takes"; OUT.mkdir(exist_ok=True)
V = {"jesus": "tlETan7Okc4pzjD0z62P", "woman": "NbkKnEAZ7Bqw4EAkVEaz"}
LINES = [
 ("02", "jesus", "[tired][gently] Give me to drink."),
 ("03", "woman", "[surprised][a little wary] How is it that thou, being a Jew, askest drink of me?"),
 ("05", "jesus", "[warmly] Whosoever drinketh of this water shall thirst again."),
 ("09", "jesus", "[softly][tenderly] I that speak unto thee am he."),
 ("12", "woman", "[breathless][joyful][half-laughing] Come, see a man, which told me all things that ever I did: is not this the Christ?"),
]
key = os.getenv("ELEVENLABS_API_KEY")
for n, who, text in LINES:
    for take in ("a", "b"):
        f = OUT/f"{n}_{who}_{take}.mp3"
        if f.exists(): continue
        f.write_bytes(P.render_turn(key, V[who], text)); print("ok", f.name, flush=True)
