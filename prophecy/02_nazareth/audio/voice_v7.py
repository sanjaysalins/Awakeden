r"""Nazareth voice v7 (owner "lock and yes" ~$0.25, 2026-11-16). Locked words = ../words/FINAL_WORDS_v7.md.
New lines only; reused: v6 takes + 04_jesus_b cut after 'fulfilled'. Townsman = same voice as the leader (heal/save echo).
  C:\Users\sanjay\PycharmProjects\PythonProject1\.venv\Scripts\python.exe voice_v6.py"""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
OUT = Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\02_nazareth\audio\_takes"); OUT.mkdir(exist_ok=True)
V = {"narrator": "LSi9zNCeliLuhIGGS0By", "townsman": "SOYHLrjzK2X1ezoPC6cr"}
T = [
 ("v7_01", "narrator", "In Nazareth, His home town, He read God's promise of someone sent with good news for the poor, and a time of God's welcome."),
 ("v7_06", "narrator", "It was about Him. They would want miracles, and say:"),
 ("v7_07", "townsman", "[scornful][challenging] Physician, heal thyself."),
 ("v7_08", "narrator", "He reminded them God once sent help to foreigners, not to their own. Furious, they took Him to a cliff to throw Him down. He walked right through them."),
 ("v7_09", "narrator", "Later, at the cross, the same dare:"),
 ("v7_11", "narrator", "This time, He stayed. He died, and rose again."),
]
key = os.getenv("ELEVENLABS_API_KEY")
assert key, "no ELEVENLABS_API_KEY"
for n, who, text in T:
    P.STABILITY = 0.5 if who == "narrator" else 0.3
    for take in (("a",) if who == "narrator" else ("a", "b")):
        f = OUT / f"{n}_{who}_{take}.mp3"
        if f.exists(): continue
        f.write_bytes(P.render_turn(key, V[who], text)); print("ok", f.name, flush=True)
