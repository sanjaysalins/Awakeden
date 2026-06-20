#!/usr/bin/env python3
"""Cut a few study figures out of their background so the narration text wraps the
subject's silhouette (CSS shape-outside). Impressive, magazine-style.

LOCAL tool — needs rembg + the source paintings, so it is NOT run by Netlify. Run
it BEFORE build_catalog.py, then commit the results:

  python _website/make_cutouts.py
  python _website/build_catalog.py
  git add _website/assets/study

The cut-outs are committed; the cloud build renders them from the committed webps.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import yaml
from PIL import Image
from rembg import new_session, remove
from scipy import ndimage

import build_catalog as bc

SITE = Path(__file__).resolve().parent
# slugs that read as a single person/figure -> clean cut-out subjects
FIGURE_HINTS = {
    "christ", "jesus", "risen", "king", "servant", "bearing", "silent", "looking",
    "forsaking", "wounded", "hung", "poured", "pierced", "lamb", "shepherd", "david",
    "man", "face", "body", "suffering", "scourged", "crucified", "proclaiming",
    "brethren", "stricken", "prophet", "come", "thirst",
}
SKIP_HINTS = {
    "nations", "earth", "world", "tomb", "scroll", "lamp", "darkness", "dust", "crowd",
    "leaders", "hands", "whole", "ends", "kindreds", "light", "gentiles", "empty",
    # multi-figure / group scenes leave stray people in the cut-out -> avoid
    "among", "brethren", "proclaiming", "rejoicing", "family", "congregation",
    "welcomed", "shaking", "jeer", "twelve", "legions", "declared", "apostle",
    "peter", "john", "stare", "look", "shoulder", "calling",
}
MAX_PER_PAGE = 2


def isolate(rgba: Image.Image):
    """Keep only the single largest subject; drop stray blobs + faint halo.

    Returns (cleaned_image, dominance) where dominance is the largest subject's
    share of all foreground -- low means a multi-figure/crowd scene (reject).
    """
    arr = np.array(rgba)
    a = arr[..., 3]
    mask = a > 50
    lbl, n = ndimage.label(mask)
    if n == 0:
        return rgba, 0.0
    sizes = ndimage.sum(mask, lbl, range(1, n + 1))
    keep = int(np.argmax(sizes)) + 1
    dominance = float(sizes[keep - 1] / max(mask.sum(), 1))
    kept = lbl == keep
    kept = ndimage.binary_fill_holes(kept)
    new_a = np.where(kept, a, 0)
    new_a = np.where(new_a < 70, 0, new_a)  # cut the translucent haze
    arr[..., 3] = new_a
    return Image.fromarray(arr, "RGBA"), dominance


def good_subject(rgba: Image.Image) -> bool:
    a = np.array(rgba.split()[-1])
    cov = float((a > 25).mean())
    if not (0.12 <= cov <= 0.80):
        return False
    bbox = rgba.getbbox()
    if not bbox:
        return False
    h = bbox[3] - bbox[1]
    w = bbox[2] - bbox[0]
    return h >= 0.45 * rgba.height and w >= 0.2 * rgba.width


def main() -> int:
    manifest = yaml.safe_load((SITE / "manifest.yaml").read_text(encoding="utf-8"))
    sess = new_session("u2net")
    total = 0
    for item in manifest.get("items", []):
        ss = bc.study_source_for(item)
        study = bc.load_study(ss)
        if not study:
            continue
        slug = item["slug"]
        pm = re.search(r"\d+_([a-z0-9-]+)\.png", item.get("preview_source") or "")
        poster = pm.group(1) if pm else ""
        placement = bc.select_study_figures(ss, slug, study["reading"], study["is_long"], poster)
        cands = [
            c for c in placement.values()
            if c.get("png")
            and (set(c["slug"].split("-")) & FIGURE_HINTS)
            and not (set(c["slug"].split("-")) & SKIP_HINTS)
        ]
        cut_dir = SITE / "assets" / "study" / slug / "cut"
        made = 0
        for c in cands:
            if made >= MAX_PER_PAGE:
                break
            out = cut_dir / f"{c['slug']}.webp"
            plate = SITE / "assets" / "study" / slug / f"{c['slug']}.webp"
            if out.is_file():
                made += 1
                continue
            try:
                res = remove(Image.open(c["png"]).convert("RGBA"), session=sess)
                res, dominance = isolate(res)
            except Exception as ex:  # noqa: BLE001
                print(f"  skip {slug}/{c['slug']} ({ex})")
                continue
            if dominance < 0.82:
                print(f"  skip {slug}/{c['slug']} (multi-figure, dominance {dominance:.2f})")
                continue
            if not good_subject(res):
                print(f"  skip {slug}/{c['slug']} (subject not clean enough)")
                continue
            res = res.crop(res.getbbox())
            res.thumbnail((560, 940), Image.LANCZOS)
            cut_dir.mkdir(parents=True, exist_ok=True)
            res.save(out, "WEBP", quality=86, method=6)
            if plate.is_file():
                plate.unlink()  # the cut-out replaces the framed plate
            made += 1
            total += 1
            print(f"  cut {slug}/{c['slug']}")
    print(f"Wrote {total} cut-outs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
