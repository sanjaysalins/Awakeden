"""Generate the Zacchaeus thumbnail, reusing pipeline/thumbnails.py's real
functions directly (grab_frame with blank-avoidance, compose, brand assets)
rather than its manifest-driven batch wrapper, since this POC piece isn't
registered in _website/manifest.yaml.

  .venv\\Scripts\\python.exe poc_thief_e2e/_thumbnail_zacchaeus.py
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pipeline.thumbnails import grab_frame, compose, _duration

VIDEO = ROOT / "poc_thief_e2e" / "clips" / "_zacchaeus" / "ZACCHAEUS_CAPTIONED.mp4"
OUT = ROOT / "poc_thief_e2e" / "clips" / "_zacchaeus" / "thumbs"
OUT.mkdir(parents=True, exist_ok=True)

TITLE = ["HE CALLED HIM", "BY NAME"]
REF = "Luke 19:1-10"
HERO_T = 20.0  # Jesus's close-up call -- the gospel-pivot moment (AS-G6)


def main():
    dur = _duration(VIDEO)
    raw_png = OUT / "_raw_frame.png"
    frame = grab_frame(VIDEO, HERO_T, raw_png, duration=dur, piece_label="Zacchaeus")

    for size_key, fname in [("9x16", "thumb_9x16.jpg"), ("16x9", "thumb_16x9.jpg"),
                              ("1x1", "thumb_1x1.jpg")]:
        img = compose(frame, size_key, TITLE, REF)
        img.convert("RGB").save(OUT / fname, quality=92)
        print(f"[thumb] {fname} ({img.size[0]}x{img.size[1]})")

    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
