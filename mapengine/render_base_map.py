#!/usr/bin/env python
"""Render an inked antique-parchment base map via HF seedream_v4_5 ($0.30, 16:9).

The style spine (ink cartography, NO legible text) is baked in; you supply the
SUBJECT (which region + features) via --prompt. Text is deliberately kept OFF the
image — labels are added deterministically by mapengine.py so nothing can be
garbled by a downstream model.

    <venv>\\python.exe mapengine\\render_base_map.py --out base_map.png \\
        --prompt "Egypt & the Nile delta lower-left, the Sinai triangle & the two
                  Red-Sea arms centre, Canaan & the Jordan upper-right, desert dunes"
"""
from __future__ import annotations
import argparse, re, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)

STYLE = (
    " Flat top-down cartographic bird's-eye view. Small hand-drawn inked mountain "
    "peaks, rolling desert dunes, stylised inked sea waves, a decorative compass rose "
    "in one corner. Drawn in INKED BIBLICAL GRAPHIC-NOVEL / antique-cartography style: "
    "bold clean black ink linework and outlines, fine cross-hatching, flat muted sepia, "
    "ochre and faded teal wash on weathered burnt-edged parchment, hand-drawn 2D artwork. "
    "NOT a photograph, NOT photorealistic, NOT a glossy 3D render. Reverent, timeless, "
    "ancient. ABSOLUTELY NO text, letters, words, numbers, captions, labels, place names, "
    "inscriptions or writing anywhere in the image — every surface blank. --ar 16:9"
)
DEFAULT_SUBJECT = (
    "An aged antique parchment map of the ancient Near East. Egypt and the green Nile "
    "river delta fan out in the lower-left corner; the triangular Sinai peninsula sits in "
    "the centre flanked by two arms of the Red Sea; the Mediterranean sea runs along the "
    "top edge; the land of Canaan with the winding Jordan river and the Dead Sea lies on "
    "the right."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--prompt", default=DEFAULT_SUBJECT, help="the SUBJECT (region + features)")
    a = ap.parse_args()
    dest = Path(a.out)
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {dest}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    args = [HF, "generate", "create", "seedream_v4_5", "--prompt", a.prompt + STYLE,
            "--aspect_ratio", "16:9", "--quality", "high", "--wait"]
    for attempt in (1, 2, 3):
        r = subprocess.run(args, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=600)
        blob = (r.stdout or "") + (r.stderr or "")
        m = URL_RE.search(blob)
        if m:
            req = urllib.request.Request(m.group(0), headers={"User-Agent": "awakeden-map/1.0"})
            with urllib.request.urlopen(req, timeout=180) as resp:
                dest.write_bytes(resp.read())
            print(f"[ok] {dest}  ({dest.stat().st_size} bytes)")
            return
        low = blob.lower()
        if not any(t in low for t in ("concurrent_jobs_limit", "rate_limit", "timeout", "502")):
            print(f"[FAIL] {blob[-300:].strip()}")
            return
        print(f"[retry {attempt}] transient error")
    print("[FAIL] no image after retries")


if __name__ == "__main__":
    main()
