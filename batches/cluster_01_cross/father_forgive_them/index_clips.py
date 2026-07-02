#!/usr/bin/env python
"""Register the 12 animated motion-comic clips into the global asset index (root asset_index.json).

Each clip clones its source still's rich metadata (the still is already indexed as fft_<slug>),
then overrides type/media/path + adds motion + duration. Clip id = fft_<slug>_clip. Idempotent.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/index_clips.py
"""
import importlib.util, json, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("ax", ROOT / "asset_index.py")
ax = importlib.util.module_from_spec(spec); spec.loader.exec_module(ax)

NBP = HERE / "visual" / "nbp"
SCENES = json.load(open(HERE / "visual" / "scene_plan.json", encoding="utf-8"))["plan"]["scenes"]


def _dur(mp4: Path) -> float:
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", str(mp4)], capture_output=True, text=True)
        return round(float(out.stdout.strip()), 2)
    except Exception:
        return 0.0


def main():
    stills = {a["id"]: a for a in ax.load()["assets"]}
    n = 0
    for s in SCENES:
        slug = s["png"]
        mp4 = NBP / f"{slug}.mp4"
        if not (mp4.exists() and mp4.stat().st_size > 0):
            print(f"  [skip-missing] {slug}.mp4"); continue
        still = stills.get(f"fft_{slug}")
        if not still:
            print(f"  [no-still-meta] fft_{slug} — clip indexed with minimal meta")
            still = {"cluster": "01_cross", "piece": "father_forgive_them",
                     "piece_title": "Father, forgive them", "verse": "Luke 23:34",
                     "style": "inked-graphic-novel", "aspect": "9:16"}
        entry = {k: v for k, v in still.items() if k not in ("id", "path", "type", "media", "source")}
        entry.update({
            "id": f"fft_{slug}_clip", "type": "clip", "media": "video",
            "path": str(mp4), "source": "kling3_0-pro",
            "motion": s.get("motion"), "duration_s": _dur(mp4),
            "created": "2026-07-01", "still_id": f"fft_{slug}",
        })
        # merge motion into tags for discoverability
        tags = list(entry.get("tags", []))
        for t in ("clip", "motion-comic", s.get("motion", "")):
            if t and t not in tags:
                tags.append(t)
        entry["tags"] = tags
        ax.register(entry)
        print(f"  [indexed] fft_{slug}_clip  [{s.get('motion')}] {entry['duration_s']}s")
        n += 1
    print(f"\nregistered {n} clips. asset_index.json now holds {len(ax.load()['assets'])} assets.")


if __name__ == "__main__":
    main()
