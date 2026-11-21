r"""Storm wordsfix1: re-record ONLY the new narrator lines. Film's own voice: eleven_v3 text-to-dialogue,
narrator LSi9zNCeliLuhIGGS0By, stability 0.65 (narration.meta.json). Emotion tags as in the film's narration-tagged.md. Cap $0.30."""
import os, sys, json
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
from dotenv import load_dotenv
load_dotenv(r"C:\Users\sanjay\PycharmProjects\PythonProject1\.env")
import per_turn_synth as P
OUT = Path(__file__).resolve().parent
NV = "LSi9zNCeliLuhIGGS0By"
T = {
 "l1": ("[serious]", "The ship is covered with the waves."),
 "l3": ("[quietly][reflective]", "The Bible does not say why He sleeps."),
 "l4a": ("[serious]", "They wake Him:"),
 "l4b": ("[serious]", "Lord, save us: we perish."),
 "l9": ("[reflective]", "Maybe your own storm is loud right now. You can pray their short prayer: Lord, save us."),
 "l11": ("[quietly][reflective]", "Their faith was little, and He still stood up for them."),
}
key = os.getenv("ELEVENLABS_API_KEY"); assert key
P.STABILITY = 0.65
tot = 0
for k, (tag, text) in T.items():
    f = OUT / f"{k}_raw.mp3"
    if f.exists(): print("exists", f.name); continue
    full = f"{tag} {text}"
    f.write_bytes(P.render_turn(key, NV, full)); tot += len(full); print("ok", f.name, len(full), "chars", flush=True)
print("chars billed", tot)
