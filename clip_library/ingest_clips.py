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

# Shorts (9:16) sources — clips live in <visual>/nbp/*.mp4 (skip the zechariah consumer,
# it's made of reused copies).
SOURCES = (
    "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/*/visual",
    "v2/pilot/isaiah_53_5_with_his_stripes/v1/visual",
    "v2/pilot/mockers_words_ps22/v1/visual",
)
# Long-form (16:9) sources — clips live DIRECTLY in <visual_16x9>/[0-9][0-9]_*.mp4 next to
# scene_plan.json (no nbp/ subdir). These feed cross-episode reuse into OTHER long-forms;
# aspect is tracked so a 9:16 short clip is never offered into a 16:9 film (and vice versa).
LONGFORM_SOURCES = (
    "longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9",
    "longform/02_Psalm_22_Song_From_The_Cross/v1/visual_16x9",
    "longform/03_The_Passover_Lamb/v1/visual_16x9",
    "longform/04_The_Bronze_Serpent/v1/visual_16x9",
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


# Human spot-review override (the topical-fit human check the auto-tagger can't make).
# slug -> tags. These long-form clips are eye-verified as GENERIC Christ/passion (not tied to
# their episode's story), so they are safe to reuse into OTHER 16:9 long-forms. Forced neutral.
REVIEWED_REUSABLE = {
    # #04 Bronze Serpent — own-world episode, but these 5 are generic enough to seed the bank:
    "23_not_a_preacher_s_picture_jesus_himself":     ["christ-face", "ministry-living"],   # fills the no-living-Christ gap
    "17_made_a_curse_for_us_on_the_tree":            ["cross", "crucified"],
    "21_look_to_the_one_lifted_up_hero_close":       ["christ-face", "risen-hero"],
    "13_lifted_up_signifying_what_death_he_shoul":   ["cross", "wide-cross"],
    "14_for_god_so_loved_the_world":                 ["cross", "wide-world-light"],
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
    # shorts use s["index"]; long-form (16:9) builders use s["id"]
    return {(s.get("index") if s.get("index") is not None else s.get("id")): s
            for s in (scenes or [])}


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


def _ingest(clips, patterns, clip_dir, aspect):
    """Append clips for a set of glob patterns. clip_dir='nbp' (shorts) or '' (long-form,
    clips sit directly in the visual dir). aspect tags the clip so reuse can filter by format."""
    for pat in patterns:
        for vis in glob.glob(str(ROOT / pat)):
            vis = Path(vis)
            scenes = _scenes(vis)
            episode = vis.parent.name if vis.parent.name != "v1" else vis.parents[1].name
            search = (vis / clip_dir) if clip_dir else vis
            for mp4 in sorted(search.glob("[0-9][0-9]_*.mp4")):
                idx = int(mp4.stem[:2])
                scene = scenes.get(idx, {})
                tags, scope = _tags_scope(scene)
                if mp4.stem in REVIEWED_REUSABLE:        # human spot-review override
                    tags, scope = REVIEWED_REUSABLE[mp4.stem], "neutral"
                clips.append({
                    "slug": mp4.stem,
                    "source": str(mp4.relative_to(ROOT)).replace("\\", "/"),
                    "title": scene.get("title", mp4.stem[3:].replace("-", " ").title()),
                    "episode": episode,
                    "aspect": aspect,
                    "duration": _probe(mp4),
                    "tags": tags,
                    "scope": scope,
                    "jesus_variant": scene.get("jesus_variant"),
                })


def main():
    clips = []
    _ingest(clips, SOURCES, "nbp", "9:16")
    _ingest(clips, LONGFORM_SOURCES, "", "16:9")
    OUT.write_text(json.dumps({"_doc": "Central clip library (by reference). Build via ingest_clips.py. "
                               "Spot-review the 'neutral' set before trusting cross-episode auto-reuse. "
                               "Reuse must match aspect (9:16 shorts vs 16:9 long-form).",
                               "version": 2, "clips": clips}, ensure_ascii=False, indent=2), encoding="utf-8")
    from collections import Counter
    for asp in ("9:16", "16:9"):
        sub = [c for c in clips if c["aspect"] == asp]
        neutral = [c for c in sub if c["scope"] == "neutral"]
        tagc = Counter(t for c in neutral for t in c["tags"])
        print(f"[{asp}] indexed {len(sub)} clips ({len(neutral)} neutral / {len(sub)-len(neutral)} specific)")
        print(f"       neutral reusable by tag: {dict(tagc)}")


if __name__ == "__main__":
    main()
