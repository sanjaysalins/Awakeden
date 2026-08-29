import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "test_the_cross"))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from swirls_page import render_still  # noqa: E402
from episode import PAGES  # noqa: E402

spec = PAGES["f04"]
png = HERE / f"{HERE.name}_f04_9x16.png"

ok = render_still(spec, png)
sys.exit(0 if ok else 1)
