"""word_boxes.py (uplift T6): caption boxes from the engine's own caption layer PNGs ($0).

Kinetic captions: _kc16_<beat>_<n>.png = the caption as it looks when word n is lit. The box of word n is the
set of pixels that are in state n but not in state n-1. Quote (redletter) captions: _red16_<beat>.png is one
layer; its union box is the caption zone (per-word split is only needed for ring/strike/underline marks).
Output: word_boxes.json  { "<beat>": {"kind": "kinetic"|"quote", "zone": [x,y,w,h], "words": [[x,y,w,h]...]} }
Usage: python word_boxes.py <pool>/_livingpage_work <out.json>
"""
import json, re, sys
from pathlib import Path
import numpy as np
from PIL import Image


def bbox(mask):
    ys, xs = np.where(mask)
    if not len(xs):
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


def main(work, out):
    work = Path(work)
    res = {}
    kc = {}
    for p in work.glob("_kc16_*_*.png"):
        m = re.match(r"_kc16_(\d+)_(\d+)\.png", p.name)
        if m:
            kc.setdefault(int(m.group(1)), {})[int(m.group(2))] = p
    for beat, states in sorted(kc.items()):
        prev = None
        words, zone = [], None
        for n in sorted(states):
            a = np.array(Image.open(states[n]).convert("RGBA"))[:, :, 3] > 24
            diff = a if prev is None else (a & ~prev)
            b = bbox(diff)
            words.append(b)
            zone = bbox(a) if zone is None else bbox(a | (np.zeros_like(a) if zone is None else a))
            prev = a if prev is None else (prev | a)
        res[str(beat)] = {"kind": "kinetic", "zone": bbox(prev), "words": words}
    for p in sorted(work.glob("_red16_*.png")):
        m = re.match(r"_red16_(\d+)\.png", p.name)
        a = np.array(Image.open(p).convert("RGBA"))[:, :, 3] > 24
        res[str(int(m.group(1)))] = {"kind": "quote", "zone": bbox(a), "words": []}
    Path(out).write_text(json.dumps(res, indent=1), encoding="utf-8")
    for k, v in res.items():
        print(k, v["kind"], v["zone"], len(v["words"]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
