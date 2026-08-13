"""Look and Live -- $0 Ken Burns fallback for s08_crowd_healing, replacing a
generative clip after 2 straight paid Seedance attempts both invented motion
in the serpent (try 1: the tongue whipped into a long lashing ribbon; try 2,
after explicitly locking the tongue too: the whole head/neck bent downward).
Per this project's own locked practice (a still-stuck/over-inventive shot is
a USER decision, never a silent fallback -- see feedback-static-ai-clips-
need-real-camera / the God Hung Up a Snake session, which used this same
dynamic_cam3d 'push' move on 4 of its own clips), user chose the $0 camera
push after seeing both failures.

panel_animator/dynamic_cam3d.py hard-codes 16:9 (1920x1080) output; this
project's shorts are 9:16. Patches OUT_W/OUT_H before calling render_move,
same as the (unsaved, inline) approach used for God Hung Up a Snake's own
s08/s11/s12a/s12b -- confirmed those clips are 1080x1920 on disk.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_s08_kenburns.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
import dynamic_cam3d as DC  # noqa: E402

DC.OUT_W, DC.OUT_H = 1080, 1920

HERE = Path(__file__).resolve().parent
STILL = HERE / "stills" / "s08_crowd_healing.png"
DEST = HERE / "clips" / "s08_crowd_healing.mp4"


def main():
    if not STILL.exists():
        raise SystemExit(f"missing still: {STILL}")
    DEST.parent.mkdir(exist_ok=True)
    out = DC.render_move(STILL, "push", duration=4.0, focus=(0.5, 0.55), dest=DEST)
    print(f"[ok] {out}")


if __name__ == "__main__":
    main()
