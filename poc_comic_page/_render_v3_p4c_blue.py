"""v3.1 adversarial fix 6: re-render p4c (empty threshold) STORM-BLUE dominant.
Pages 4-5 are hue-monotone gold at the art level; this panel becomes the one
cold frame the DNA palette promises -- deep storm blue-black night, the empty
doorway's gold the ONLY warmth. Same scene, same period rules.
NOTE: still re-roll INVALIDATES its clip chain -- _animate_v3_p4c.py must run
after this passes the eye check (locked rule).

  .venv\\Scripts\\python.exe poc_comic_page/_render_v3_p4c_blue.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline import cost  # noqa

spec = importlib.util.spec_from_file_location(
    "_stills_v2", Path(__file__).resolve().parent / "_render_piece1_stills_v2.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

OUT = S.OUT / "p4c_empty_threshold.png"

SCENE = (
    "SCENE: A great open arched gateway in a massive ancient stone wall at "
    "night, the passage standing open -- pure weathered hand-cut stone, an "
    "open way of stone and light. A long beam of warm golden light pours "
    "through the open arch and spills across bare worn flagstones toward the "
    "camera, the stones inside the beam glowing warm gold. Beyond and around "
    "it, deep storm blue-black night dominates everything -- the cold blue "
    "night sky, the blue-shadowed stone wall receding, the blue-dark bare "
    "flagstone street, utterly still and silent, stone and shadow only. The "
    "warm gold beam from the open arch is the ONLY warmth anywhere in the "
    "image, a single candle of color in a cold blue world. Seen level, a "
    "quiet mid-distance."
)


def main():
    prompt = (S.PASSION_STYLE + "\n\n" + SCENE + "\n\n" + S.PASSION_CLOSING +
              "\n\n" + S.CONSTRAINT)
    if OUT.exists():
        bak = OUT.with_name("p4c_empty_threshold.v1_warm.png")
        if not bak.exists():
            OUT.rename(bak)
            print(f"[keep] old warm still -> {bak.name}")
    print("[img] p4c blue re-render (9:16, no refs) ...", flush=True)
    ok = S.run(prompt, OUT, [], "9:16")
    if not ok:
        print("   retrying once ...")
        ok = S.run(prompt, OUT, [], "9:16")
    if ok:
        try:
            cost.record_hf(S.EPISODE, "short", "stills_v31_blue", S.MODEL,
                           note="[piece1-v3.1] p4c blue")
        except Exception as e:
            print(f"   (ledger record skipped: {e})")
        print(f"[ok] {OUT}")
    else:
        raise SystemExit("FAILED")


if __name__ == "__main__":
    main()
