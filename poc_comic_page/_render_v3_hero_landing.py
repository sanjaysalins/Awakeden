"""v3 elevation: the ONE new metered still -- the landing hero splash.
The Bowed Camera grammar rations the low-angle hero shot for glory beats;
piece 1 never spent it (p5c reads level + has an iron door handle, a period
violation the small cell hid). This still is the payoff frame: true low
angle, wide radiant seam, bare plank door. Positive end-state wording only.

  .venv\\Scripts\\python.exe poc_comic_page/_render_v3_hero_landing.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline import cost  # noqa

sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util

spec = importlib.util.spec_from_file_location(
    "_stills_v2", Path(__file__).resolve().parent / "_render_piece1_stills_v2.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

OUT = S.OUT / "p6_hero_landing.png"

STYLE = S.GLORY_STYLE
CLOSING = (
    "Render with the gold-seam rule throughout: the seam is wide and radiant, "
    "fully earned, the camera a low earned hero angle looking up, triumphant."
)
SCENE = (
    "SCENE: Seen from very low, at the height of the worn threshold stones "
    "themselves, the camera looking steeply UP at Jesus standing tall beneath "
    "a great open gateway arch in a massive ancient stone wall, filling the "
    "frame with quiet majesty. The gateway is pure weathered stone -- rough "
    "hand-cut voussoirs converging dramatically overhead, worn flagstones "
    "below -- an open passage of stone, light, and the man alone. His arms "
    "are slightly open at his "
    "sides in welcome, palms turned outward. Radiant morning-gold light "
    "floods the archway around him and pours past him over the stones toward "
    "the camera, his edge burning in a wide radiant gold seam against the "
    "deep blue-black night sky above. His face is calm, glad, triumphant, "
    "looking down toward the camera with open welcome. He matches the "
    "reference image: long dark wavy hair, short dark beard, simple undyed "
    "homespun tunic with a woven cord sash, leather sandals."
)


def main():
    prompt = STYLE + "\n\n" + SCENE + "\n\n" + CLOSING + "\n\n" + S.CONSTRAINT
    print("[img] p6_hero_landing (9:16, JESUS ref) ...", flush=True)
    ok = S.run(prompt, OUT, [S.JESUS_REF], "9:16")
    if not ok:
        print("   retrying once ...")
        ok = S.run(prompt, OUT, [S.JESUS_REF], "9:16")
    if ok:
        try:
            cost.record_hf(S.EPISODE, "short", "stills_v3_hero", S.MODEL,
                           note="[piece1-v3] p6_hero_landing")
        except Exception as e:
            print(f"   (ledger record skipped: {e})")
        print(f"[ok] {OUT}")
    else:
        raise SystemExit("FAILED")


if __name__ == "__main__":
    main()
