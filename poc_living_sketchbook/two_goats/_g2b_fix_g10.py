"""Two Goats — patch: g10_finished's Jesus drifted from g08's Jesus (user
catch: different hair color/length, thinner beard) -- the Door-episode
anchor alone isn't locking identity tightly enough across poses within a
NEW episode. Fix: chain the Door anchor AND this episode's own approved
g08 render together as TWO references, so the model has two consistent
views of THIS episode's Jesus to match, not one cross-episode anchor.

  .venv\\Scripts\\python.exe poc_living_sketchbook/two_goats/_g2b_fix_g10.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline import cost

spec = importlib.util.spec_from_file_location(
    "_g2", Path(__file__).resolve().parent / "_g2_stills.py")
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)

OUT = G.OUT / "g10_finished.png"
G08 = G.OUT / "g08_jesuspivot.png"
assert G08.exists(), f"missing approved g08: {G08}"

SCENE = (
    f"{G.JESUS} He matches BOTH reference images exactly, with no drift "
    f"at all: the SAME full dark near-black wavy/curly shoulder-length "
    f"hair (not lighter brown, not shorter), the SAME full dark beard "
    f"covering his whole jaw (not thinner, not patchy), the SAME warm "
    f"olive skin tone. Seen from behind and to the side, He sits at rest "
    f"on a plain stone ledge within a radiant doorway of warm gold light, "
    f"His posture utterly at peace, head slightly bowed; deep blue-wash "
    f"shadow beyond the light."
)


def main():
    prompt = G.STYLE + "\n\nSCENE: " + SCENE
    print("[img] g10_finished v2 (refs=2: door anchor + approved g08) ...", flush=True)
    ok = G.run(prompt, OUT, [G.JESUS_REF, G08])
    if not ok:
        ok = G.run(prompt, OUT, [G.JESUS_REF, G08])
    if ok:
        cost.record_hf(G.EPISODE, "short", "stills", G.MODEL,
                       note="[two-goats] g10 refix vs g08")
        print("   ok")
    else:
        raise SystemExit("FAILED")


if __name__ == "__main__":
    main()
