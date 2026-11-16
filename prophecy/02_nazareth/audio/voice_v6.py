r"""Nazareth voice v6 (owner yes ~$1.60 total incl. pictures, cap $2.50, 2026-11-16). Locked words = ../words/FINAL_WORDS_v6.md.
New lines only; reused takes: 00_narrator_a, 02_isaiah_b, 03_narrator_a (trimmed before 'Every eye'), 04_jesus_b.
  C:\Users\sanjay\PycharmProjects\PythonProject1\.venv\Scripts\python.exe voice_v6.py"""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
OUT = Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\02_nazareth\audio\_takes"); OUT.mkdir(exist_ok=True)
V = {"narrator": "LSi9zNCeliLuhIGGS0By", "jesus": "tlETan7Okc4pzjD0z62P", "leader": "SOYHLrjzK2X1ezoPC6cr"}
T = [
 ("v6_01", "narrator", "In Nazareth, His home town, He read God's promise of someone sent with good news for the poor, freedom for prisoners, and a time of God's welcome."),
 ("v6_02", "narrator", "The prophet Isaiah's sentence goes on:"),
 ("v6_06", "narrator", "He knew what His town would say:"),
 ("v6_07", "jesus", "[calm][knowing][gentle] Physician, heal thyself."),
 ("v6_08", "narrator", "He reminded them God once sent help to foreigners, not to them. Furious, they led Him to a cliff to throw Him down. He walked right through them."),
 ("v6_09", "narrator", "Later, at the cross, leaders mocked:"),
 ("v6_10", "leader", "[mocking][scornful] He saved others; let him save himself."),
 ("v6_11", "narrator", "This time, He stayed, and gave His life."),
 ("v6_12", "narrator", "He stopped reading at the welcome. It is still open, for you, today."),
]
key = os.getenv("ELEVENLABS_API_KEY")
assert key, "no ELEVENLABS_API_KEY"
for n, who, text in T:
    P.STABILITY = 0.5 if who == "narrator" else 0.3
    for take in (("a",) if who == "narrator" else ("a", "b")):
        f = OUT / f"{n}_{who}_{take}.mp3"
        if f.exists(): continue
        f.write_bytes(P.render_turn(key, V[who], text)); print("ok", f.name, flush=True)
