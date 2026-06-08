"""Print exact word/phrase times from the aligned words.json files, for plan design.
Usage: python sfx_pilots/anchors.py <safe_stem> word1 word2 ...
       python sfx_pilots/anchors.py --all     # dump every clip duration + last word
"""
import json
import re
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parent / "work"


def words_of(stem):
    return json.loads((WORK / f"{stem}.words.json").read_text(encoding="utf-8"))


def main():
    if sys.argv[1] == "--all":
        for f in sorted(WORK.glob("*.words.json")):
            w = json.loads(f.read_text(encoding="utf-8"))
            print(f"{f.stem.replace('.words',''):<40} {len(w):>3}w  last '{w[-1]['w']}' end {w[-1]['end']:.2f}s")
        return
    stem = sys.argv[1]
    needles = [re.sub(r"[^a-z]", "", a.lower()) for a in sys.argv[2:]]
    w = words_of(stem)
    for i, wd in enumerate(w):
        tok = re.sub(r"[^a-z]", "", wd["w"].lower())
        if tok in needles:
            ctx = " ".join(x["w"] for x in w[max(0, i-2):i+3])
            print(f"  {tok:<12} {wd['start']:.2f}-{wd['end']:.2f}s   …{ctx}…")


if __name__ == "__main__":
    main()
