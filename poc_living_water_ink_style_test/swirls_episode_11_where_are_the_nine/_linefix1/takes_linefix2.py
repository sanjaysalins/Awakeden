r"""Ep11 linefix1: re-record ONLY the two new lines. Same voice/model/settings as the film (eleven_v3, stability 0.5,
text-to-dialogue, narrator LSi9zNCeliLuhIGGS0By). Cap $0.40 (owner). Takes a, b per line. Usage: takes_linefix1.py first a b | last a b"""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
OUT = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_11_where_are_the_nine\_linefix1")
NV = "LSi9zNCeliLuhIGGS0By"
LINES = {
 "last2": "[reflective][deliberate] Nine went on clean. One came back whole: at His feet, not on the road.",
 "first": "[serious] Ten sick men begged Jesus for mercy. He sent them off, still sick.",
 "last":  "[reflective][deliberate] Nine went on clean. One, face down at His feet, went on whole.",
}
key = os.getenv("ELEVENLABS_API_KEY")
assert key, "no key"
P.STABILITY = 0.5
which = sys.argv[1]
for take in sys.argv[2:]:
    f = OUT / f"{which}_narrator_{take}.mp3"
    if f.exists(): print("exists", f.name); continue
    f.write_bytes(P.render_turn(key, NV, LINES[which])); print("ok", f.name, len(LINES[which]), "chars", flush=True)
