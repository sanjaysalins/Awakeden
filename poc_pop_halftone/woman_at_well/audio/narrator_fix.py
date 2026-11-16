r"""Film-panel fixes (owner yes ~$0.20, 2026-11-13): re-record 3 narrator lines, 2 takes each, default narrator
settings (same as per_turn_synth run). Reuses per_turn_synth.render_turn.
  C:\Users\sanjay\PycharmProjects\PythonProject1\.venv\Scripts\python.exe narrator_fix.py"""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
HERE = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_pop_halftone\woman_at_well\audio"); OUT = HERE/"_takes"
VN = "LSi9zNCeliLuhIGGS0By"
LINES = [
 ("07", "Then He tells her the truth about her life: five husbands, and the man she has now is not her husband. He knew it all, and stayed."),
 ("14", "The jar stayed. She came for water, and found the One who gives better water: Jesus, who knew her whole story and offered her life."),
 ("15", "To give that life, He died for our sins and rose the third day."),
]
key = os.getenv("ELEVENLABS_API_KEY")
print("stability", P.STABILITY)
for n, text in LINES:
    for take in ("a", "b"):
        f = OUT/f"{n}_narrator_fix_{take}.mp3"
        if f.exists(): continue
        f.write_bytes(P.render_turn(key, VN, text)); print("ok", f.name, flush=True)
