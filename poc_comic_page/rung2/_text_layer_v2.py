"""Text overlays for the v2 (living-comic) composites -- same boxes, same
timings, same drawing code as _text_layer_rung2.py, just pointed at the
*_composite_v2.mp4 files. The timings stay valid because v2 keeps every
page's dwell identical to v1.

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_text_layer_v2.py [page2 page3 page5]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _text_layer_rung2 as T  # noqa

for pk, cfg in T.PAGES.items():
    cfg["src"] = HERE / f"{pk}_composite_v2.mp4"
    cfg["out"] = HERE / f"{pk}_with_text_v2.mp4"

if __name__ == "__main__":
    pages = sys.argv[1:] or list(T.PAGES.keys())
    for p in pages:
        T.build_page(p)
