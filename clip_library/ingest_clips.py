"""Ingest already-animated clips into clip_library/index.json (BY REFERENCE, no copies).

Scans each episode's visual/nbp/*.mp4 + its scene_plan.json, auto-derives tags, a
topical-fit scope (neutral|specific), and jesus_variant. Conservative: a clip with any
STORY-SPECIFIC marker is tagged 'specific' (won't be offered for cross-episode reuse);
only clean passion/Christ plates become 'neutral'. The index is a STARTING point — spot-
review the 'neutral' set before trusting auto-reuse (topical-fit stays the human check).

Run: .venv\\Scripts\\python.exe clip_library\\ingest_clips.py
"""
from __future__ import annotations
import glob
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "index.json"

# Source episodes to ingest (skip the zechariah consumer — it's made of reused copies).
SOURCES = (
    "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/*/visual",
    "v2/pilot/isaiah_53_5_with_his_stripes/v1/visual",
    "v2/pilot/mockers_words_ps22/v1/visual",
)

# tag -> substrings (searched in subject_block + title, lowercased)
NEUTRAL = {
    "cross":        ["crucified", "on the cross", "wooden cross", "the cross", "cross beam"],
    "christ-face":  ["christ's face", "thorn-crowned head", "thorn-marked brow", "eyes lowered", "the living face"],
    "pierced-side": ["pierced side", "spear", "blood and water", "wound below the ribs", "the pierced"],
    "wounds":       ["welt", "stripe", "scourg", "marked shoulder", "marked back", "flogging", "wounded"],
    "nailed-hand":  ["nailed hand", "nail through", "nailed open hand", "marks of one"],
    "dawn-cross":   ["widening dawn", "gold dawn", "light breaking", "finished at the cross"],
    "lamb":         ["a lamb", "young lamb"],
    "wounded-body": ["bound by the wrists", "short rough", "poured out like water", "drained"],
}
SPECIFIC = {
    "mockers":      ["jeer", "mock", "scorn", "wagging", "shake the head", "shoot out the lip", "sneer", "curled lip"],
    "rulers":       ["religious rulers", "chief priest", "scribe", "prayer fringe"],
    "dice-garments":["dice", "cast lots", "garment", "seamless", "vesture", "stripped"],
    "sheep":        ["sheep", "shepherd", "flock", "strayed lamb"],
    "tomb":         ["tomb", "stone rolled", "grave-linen", "empty tomb"],
    "risen":        ["risen christ", "resurrection", "scarred hand"],
    "thirst-water": ["potsherd", "tongue cleav", "dust of death", "living water", "well", "spring", "every river"],
    "prophet":      ["prophet", "psalmist", "isaiah", "zechariah"],
    "soldier":      ["soldier", "roman"],
    "mourners":     ["upturned", "mourn", "softening", "bowed and ashamed"],
    "apostle":      ["apostle", "peter", "matthew"],
}


def _probe(p: Path) -> float:
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", str(p)], capture_output=True, text=True, timeout=20)
        return round(float(r.stdout.strip()), 2)
    except Exception:
        return 0.0


def _scenes(visual_dir: Path) -> dict[int, dict]:
    sp = visual_dir / "scene_plan.json"
    if not sp.is_file():
        return {}
    d = json.loads(sp.read_text(encoding="utf-8"))
    scenes = d.get("plan", {}).get("scenes") if "plan" in d else d.get("scenes")
    return {s["index"]: s for s in (scenes or [])}


def _tags_scope(scene: dict) -> tuple[list[str], str]:
    text = (str(scene.get("subject_block", "")) + " " + str(scene.get("title", ""))).lower()
    tags, spec = [], False
    for t, kws in NEUTRAL.items():
        if any(k in text for k in kws):
            tags.append(t)
    for t, kws in SPECIFIC.items():
        if any(k in text for k in kws):
            tags.append(t); spec = True
    scope = "specific" if spec or not tags else "neutral"
    return tags, scope


def main():
    clips = []
    for pat in SOURCES:
        for vis in glob.glob(str(ROOT / pat)):
            vis = Path(vis)
            scenes = _scenes(vis)
            episode = vis.parent.name if vis.parent.name != "v1" else vis.parents[1].name
            for mp4 in sorted((vis / "nbp").glob("[0-9][0-9]_*.mp4")):
                idx = int(mp4.stem[:2])
                scene = scenes.get(idx, {})
                tags, scope = _tags_scope(scene)
                clips.append({
                    "slug": mp4.stem,
                    "source": str(mp4.relative_to(ROOT)).replace("\\", "/"),
                    "title": scene.get("title", mp4.stem[3:].replace("-", " ").title()),
                    "episode": episode,
                    "duration": _probe(mp4),
                    "tags": tags,
                    "scope": scope,
                    "jesus_variant": scene.get("jesus_variant"),
                })
    OUT.write_text(json.dumps({"_doc": "Central clip library (by reference). Build via ingest_clips.py. "
                               "Spot-review the 'neutral' set before trusting cross-episode auto-reuse.",
                               "version": 1, "clips": clips}, ensure_ascii=False, indent=2), encoding="utf-8")
    neutral = [c for c in clips if c["scope"] == "neutral"]
    from collections import Counter
    tagc = Counter(t for c in neutral for t in c["tags"])
    print(f"indexed {len(clips)} clips ({len(neutral)} neutral / {len(clips)-len(neutral)} specific)")
    print("neutral reusable by tag:", dict(tagc))


if __name__ == "__main__":
    main()
