"""Jonah line fix: 3 takes of the new S03+S04 line, witness voice, eleven_v3 (as the original). Owner 'spend' 2026-11-21, cap $0.10."""
import sys, os, requests
from pathlib import Path
from dotenv import load_dotenv
H = Path(__file__).resolve().parent
sys.path.insert(0, r"F:\slk\PycharmProjects\PythonProject1\jesus\narration")
load_dotenv(r"F:\slk\PycharmProjects\PythonProject1\.env")
import per_turn_synth as P
KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE = "UzI1NsMEV3ni5JRkRSls"
TEXT = "He sent me to Nineveh, that great city, but I fled toward Tarshish."
def chars():
    return requests.get("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": KEY}, timeout=30).json().get("character_count")
c0 = chars(); (H / "_takes").mkdir(exist_ok=True)
P.STABILITY = 0.6  # matches narration.meta.json
for t in "abc":
    f = H / "_takes" / f"line_{t}.mp3"
    if f.exists(): continue
    f.write_bytes(P.render_turn(KEY, VOICE, TEXT)); print("ok", f.name, flush=True)
c1 = chars(); print("characters used:", c1 - c0 if c0 is not None and c1 is not None else "unknown")
