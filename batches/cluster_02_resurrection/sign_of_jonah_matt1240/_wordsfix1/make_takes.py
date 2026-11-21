"""Jonah wordsfix1: 2 takes each of the 3 locked replacement sentences, witness voice, eleven_v3, stability 0.6 (as the film).
Owner-approved spend 2026-11-21, cap $0.25."""
import sys, os, requests
from pathlib import Path
from dotenv import load_dotenv
H = Path(__file__).resolve().parent
sys.path.insert(0, r"F:\slk\PycharmProjects\PythonProject1\jesus\narration")
load_dotenv(r"F:\slk\PycharmProjects\PythonProject1\.env")
import per_turn_synth as P
KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE = "UzI1NsMEV3ni5JRkRSls"
LINES = {
 "n1": "He sent me to Nineveh, and I fled. I knew He is gracious, and would spare her.",
 "n2": "Then, centuries later, scribes demanded a sign \u2014 Jesus gave them only my name:",
 "n3": "The One who went down into your dark and rose again is Jesus. He can bring you up.",
}
def chars():
    return requests.get("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": KEY}, timeout=30).json().get("character_count")
c0 = chars(); P.STABILITY = 0.6
for k, t in LINES.items():
    for take in "ab":
        f = H / f"{k}_{take}.mp3"
        if f.exists(): continue
        f.write_bytes(P.render_turn(KEY, VOICE, t)); print("ok", f.name, len(t), flush=True)
c1 = chars(); print("characters used:", c1 - c0 if c0 is not None and c1 is not None else "unknown")
