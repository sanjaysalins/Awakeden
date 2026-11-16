r"""Nazareth voice v1 (owner yes ~$0.35, 2026-11-15). Locked words = ../words/FINAL_WORDS_v3.md (text unchanged; [cues] are performance tags, not spoken).
Narrator 1 take per turn (stability 0.5, natural speed); isaiah / jesus / townsman 2 takes each (stability 0.3). Reuses per_turn_synth.render_turn.
  C:\Users\sanjay\PycharmProjects\PythonProject1\.venv\Scripts\python.exe voice.py"""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
OUT = Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\02_nazareth\audio\_takes"); OUT.mkdir(exist_ok=True)
V = {"narrator": "LSi9zNCeliLuhIGGS0By", "isaiah": "UzI1NsMEV3ni5JRkRSls", "jesus": "tlETan7Okc4pzjD0z62P", "townsman": "SOYHLrjzK2X1ezoPC6cr"}
T = [
 ("00", "narrator", "Jesus stopped reading in the middle of a sentence."),
 ("01", "narrator", "In Nazareth, His home town, He stood to read from the prophet Isaiah, written long before. He read God's promise of someone sent with good news for the poor, freedom for prisoners, and a time of God's welcome. Then He rolled up the scroll. Isaiah's sentence goes on:"),
 ("02", "isaiah", "[solemn][slowly] and the day of vengeance of our God."),
 ("03", "narrator", "He left the day of vengeance unread, and sat down. Every eye was on Him."),
 ("04", "jesus", "[calm][gentle][quiet authority] This day is this scripture fulfilled in your ears."),
 ("05", "narrator", "The people were amazed at His kind words. They knew Him as a local boy."),
 ("06", "townsman", "[puzzled][half amazed, half doubting] Is not this Joseph's son?"),
 ("07", "narrator", "That local boy was saying Isaiah's promise was about Him. He stopped reading at God's welcome, and said: \"This day.\""),
 ("08", "narrator", "His welcome is still open, for you, today."),
]
key = os.getenv("ELEVENLABS_API_KEY")
assert key, "no ELEVENLABS_API_KEY"
for n, who, text in T:
    P.STABILITY = 0.5 if who == "narrator" else 0.3
    for take in (("a",) if who == "narrator" else ("a", "b")):
        f = OUT / f"{n}_{who}_{take}.mp3"
        if f.exists(): continue
        f.write_bytes(P.render_turn(key, V[who], text)); print("ok", f.name, flush=True)
