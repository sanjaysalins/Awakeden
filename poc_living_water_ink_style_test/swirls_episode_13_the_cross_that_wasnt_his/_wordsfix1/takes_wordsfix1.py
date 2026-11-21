r"""Ep13 wordsfix1: re-record ONLY the two replaced passages. Same voice/model/settings as the film (eleven_v3, stability 0.65,
narrator LSi9zNCeliLuhIGGS0By). Cap $0.25 (owner). Usage: takes_wordsfix1.py mid|end a [b]"""
import os, sys
from pathlib import Path
NAR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
sys.path.insert(0, NAR); os.chdir(NAR)
import per_turn_synth as P
OUT = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_13_the_cross_that_wasnt_his\_wordsfix1")
NV = "LSi9zNCeliLuhIGGS0By"
LINES = {
 "mid": "[reflective][deliberate] Long before, in God's law, the animal offered for sin was burned outside the camp.",
 "end": "[reflective][emphasized] Reproach means shame. Simon was forced out there. You are invited. If shame has put you outside, Jesus is already there. The dying, the finishing, was His alone. You only come to Him.",
}
key = os.getenv("ELEVENLABS_API_KEY")
assert key, "no key"
P.STABILITY = 0.65
which = sys.argv[1]
for take in sys.argv[2:]:
    f = OUT / f"{which}_narrator_{take}.mp3"
    if f.exists(): print("exists", f.name); continue
    f.write_bytes(P.render_turn(key, NV, LINES[which])); print("ok", f.name, len(LINES[which]), "chars", flush=True)
