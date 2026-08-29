import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "test_the_cross"))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from swirls_page import render_animation  # noqa: E402
from episode import PAGES  # noqa: E402

spec = PAGES["f03"]
png = HERE / f"{HERE.name}_f03_9x16.png"
mp4 = HERE / f"{HERE.name}_f03_9x16.mp4"

ok = render_animation(spec, png, mp4)
sys.exit(0 if ok else 1)
