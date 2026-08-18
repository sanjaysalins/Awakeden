"""Morph mechanic test -- blend the modern/biblical pair at 25/50/75% ($0, local
PIL work) to preview whether the composition match is tight enough for a real
morph to read cleanly, before spending on actual video-morph animation.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_morph_test/_blend.py
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
A = HERE / "a_modern.png"
B = HERE / "b_biblical.png"


def main() -> None:
    if not A.exists() or not B.exists():
        raise SystemExit(f"missing source(s): {A.exists()=} {B.exists()=}")

    img_a = Image.open(A).convert("RGB")
    img_b = Image.open(B).convert("RGB")
    if img_a.size != img_b.size:
        img_b = img_b.resize(img_a.size)

    for pct in (25, 50, 75):
        blended = Image.blend(img_a, img_b, pct / 100)
        out = HERE / f"c_blend_{pct}.png"
        blended.save(out)
        print(f"[ok] {out}")


if __name__ == "__main__":
    main()
