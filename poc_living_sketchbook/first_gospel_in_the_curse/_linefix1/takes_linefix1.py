r"""first_gospel_in_the_curse linefix1: re-record ONLY the two changed narrator passages.
Film's own voice: eleven_v3 text-to-dialogue, narrator LSi9zNCeliLuhIGGS0By, stability 0.65 (narration.meta.json), original performance tags kept
([serious][quietly] for the opening, [reflective][awe] for the ending, as in narration-tagged.md). Takes a,b per passage. Cap $0.30."""
import os, sys
from pathlib import Path
NAR = r"F:\slk\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
from dotenv import load_dotenv
load_dotenv(r"F:\slk\PycharmProjects\PythonProject1\.env")
OUT = Path(__file__).resolve().parent
NV = "LSi9zNCeliLuhIGGS0By"
T = {"first": "[serious][quietly] Adam and Eve hid among the trees, afraid.",
     "last": "[reflective][awe] That promise has a name now: Jesus. Before the sentence, grace spoke first."}
key = os.getenv("ELEVENLABS_API_KEY"); assert key, "no key"
P.STABILITY = 0.65
tot = 0
for name, text in T.items():
    for take in sys.argv[1:] or ["a", "b"]:
        f = OUT / f"{name}_narrator_{take}.mp3"
        if f.exists(): print("exists", f.name); continue
        f.write_bytes(P.render_turn(key, NV, text)); tot += len(text); print("ok", f.name, len(text), "chars", flush=True)
print("chars billed", tot)
