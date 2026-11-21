r"""god_hung_up_a_snake linefix1: re-record ONLY the new first two sentences as one narrator turn.
Film's own voice: eleven_v3 text-to-dialogue, narrator LSi9zNCeliLuhIGGS0By, stability 0.65 (narration.meta.json). No audio tags. Cap $0.30."""
import os, sys
from pathlib import Path
NAR = r"F:\slk\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
OUT = Path(__file__).resolve().parent
NV = "LSi9zNCeliLuhIGGS0By"
TEXT = "People were dying of snake bites. God's cure was a snake on a pole."
key = os.getenv("ELEVENLABS_API_KEY"); assert key, "no key"
P.STABILITY = 0.65
for take in sys.argv[1:] or ["a"]:
    f = OUT / f"first_narrator_{take}.mp3"
    if f.exists(): print("exists", f.name); continue
    f.write_bytes(P.render_turn(key, NV, TEXT)); print("ok", f.name, len(TEXT), "chars", flush=True)
