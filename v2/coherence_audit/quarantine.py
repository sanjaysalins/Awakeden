"""Quarantine user-confirmed bad stills (move, don't hard-delete — keep as gate fixtures).

Moves each still + its sibling clip + ALL verdict sidecars/votes/cut-hints into
_rejected_coherence/<original-relative-path>, preserving structure, and writes a manifest.
Reversible. Also reports any clip_library/index.json references that become dangling.

Run: .venv\\Scripts\\python.exe v2\\coherence_audit\\quarantine.py          # dry-run (lists)
     .venv\\Scripts\\python.exe v2\\coherence_audit\\quarantine.py --apply   # actually move
"""
from __future__ import annotations
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
QUAR = ROOT / "_rejected_coherence"

STILLS = [
    "image_library/stills/exiled_nation_column_grey.png",
    "image_library/stills/glory_exalted_light_figure.png",
    "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/01_The_Crucifixion_Foretold/visual/nbp/11_a-thousand-years-apart.png",
    "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/02_The_Mockers_Words/visual/nbp/07_the-jabbing-hands.png",
    "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/02_The_Mockers_Words/visual/nbp/09_twelve-legions-restrained.png",
    "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/02_The_Mockers_Words/visual/nbp/13_the-silent-king.png",
    "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/03_The_Forsaken_Cry/visual/nbp/14_he-opened-it-from-the-dark.png",
    "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/05_He_Hath_Done_This/visual/nbp/05_the-greek-word.png",
    "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/07_The_Body_Foretold/visual/nbp/11_the-marks-of-one.png",
    "v2/pilot/isaiah_53_5_with_his_stripes/v1/visual/nbp/11_aimed-at-you.png",
    "v2/pilot/mockers_words_ps22/v1/visual/nbp/01_the-shaking-heads.png",
    "v2/pilot/mockers_words_ps22/v1/visual/nbp/03_they-shoot-out-the-lip.png",
    "v2/pilot/mockers_words_ps22/v1/visual/nbp/09_if-thou-be-the-son-of-god.png",
    "v2/pilot/mockers_words_ps22/v1/visual/nbp/14_come-to-the-one-who-would-not-come-down.png",
    "v2/pilot/zechariah_12_10_pierced/v1/visual/nbp/03_gods-staggering-word.png",
    "v2/pilot/zechariah_12_10_pierced/v1/visual/nbp/07_john-saw-it.png",
    "v2/pilot/zechariah_12_10_pierced/v1/visual/nbp/10_look-at-him.png",
]


def _associated(png: Path) -> list[Path]:
    """The still + every sibling artifact that should travel with it."""
    stem = png.with_suffix("")            # strips .png
    out = [png]
    out += list(png.parent.glob(png.name + ".*"))          # .png.audit.json/.png.coherence.json/.png.vote.*.json
    out += list(png.parent.glob(stem.name + ".mp4"))        # the clip
    out += list(png.parent.glob(stem.name + ".mp4.*"))      # .mp4.clipqc.json
    out += list(png.parent.glob(stem.name + ".cut_hint.json"))
    # de-dup, keep existing only
    seen, uniq = set(), []
    for p in out:
        if p.exists() and p not in seen:
            seen.add(p); uniq.append(p)
    return uniq


def _index_refs() -> dict:
    """clip_library/index.json entries whose source points at one of the quarantined stills."""
    idx = ROOT / "clip_library" / "index.json"
    if not idx.exists():
        return {}
    try:
        clips = json.loads(idx.read_text(encoding="utf-8")).get("clips", [])
    except (OSError, ValueError):
        return {}
    targets = {s.rsplit(".", 1)[0] for s in STILLS}   # stem rel paths
    hits = {}
    for c in clips:
        src = (c.get("source") or "").replace("\\", "/").rsplit(".", 1)[0]
        if src in targets:
            hits[c.get("slug", "?")] = c.get("source")
    return hits


def main(apply: bool) -> None:
    manifest = []
    n_files = 0
    for rel in STILLS:
        png = ROOT / rel
        if not png.exists():
            print(f"  [missing] {rel}")
            continue
        files = _associated(png)
        n_files += len(files)
        print(f"  {rel}  (+{len(files)-1} sidecar/clip)")
        if apply:
            for f in files:
                dest = QUAR / f.relative_to(ROOT)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(f), str(dest))
            manifest.append({"still": rel, "moved": [str(f.relative_to(ROOT)).replace("\\", "/") for f in files]})
    refs = _index_refs()
    if refs:
        print(f"\n  ! {len(refs)} clip_library/index.json entries reference a quarantined still (dangling):")
        for slug, src in refs.items():
            print(f"      {slug}  <-  {src}")
        print("    -> remove these from the index (reuse would otherwise fail to find the source).")
    if apply:
        (QUAR / "_manifest.json").parent.mkdir(parents=True, exist_ok=True)
        (QUAR / "_manifest.json").write_text(json.dumps(
            {"_README": "Quarantined bad stills (reversible). Kept as gate fixtures.",
             "dangling_index_refs": refs, "items": manifest}, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n  MOVED {n_files} files -> {QUAR}\n  manifest: {QUAR / '_manifest.json'}")
    else:
        print(f"\n  DRY-RUN: would move {n_files} files for {len(STILLS)} stills. Re-run with --apply.")


if __name__ == "__main__":
    main("--apply" in sys.argv)
