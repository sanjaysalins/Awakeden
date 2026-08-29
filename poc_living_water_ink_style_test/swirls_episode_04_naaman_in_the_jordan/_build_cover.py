import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "test_the_cross"))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

side = sys.argv[1]

from swirls_cover import render_cover_still, render_cover_animation  # noqa: E402
from episode import COVERS  # noqa: E402

spec = COVERS[side]
png = HERE / f"{side}_cover_9x16.png"
mp4 = HERE / f"{side}_cover.mp4"

mode = sys.argv[2] if len(sys.argv) > 2 else "still"
if mode == "still":
    ok = render_cover_still(spec, png)
else:
    ok = render_cover_animation(spec, png, mp4)
sys.exit(0 if ok else 1)
