"""Translation-ready SRT from a words.json (list of {w, start, end}). $0, deterministic.
Rules: one cue per sentence; a short cue (<1.2 s) or a line split mid-phrase is merged into its
neighbour while the cue stays <= MAXC chars; each cue is shown >= 1.2 s where the gap allows.
  python srt_from_words.py <words.json> <out.srt>"""
import json
import sys

MIN, MAXC, GAP = 1.2, 46, 0.05


def sentences(words):
    cues, cur = [], []
    for w in words:
        cur.append(w)
        if w["w"].rstrip('"\'').endswith((".", "?", "!")):
            cues.append(cur); cur = []
    if cur: cues.append(cur)
    return [dict(t=" ".join(x["w"] for x in c), a=c[0]["start"], b=c[-1]["end"]) for c in cues]


def merge(cues):
    out = []
    for c in cues:
        p = out[-1] if out else None
        if p and not p.get("m") and ((c["b"] - c["a"]) < MIN or (p["b"] - p["a"]) < MIN) and len(p["t"]) + 1 + len(c["t"]) <= MAXC:
            p["t"] += " " + c["t"]; p["b"] = c["b"]; p["m"] = 1  # one merge per cue keeps echo pairs together
        else:
            out.append(dict(c))
    return out


def stretch(cues):
    for i, c in enumerate(cues):
        nxt = cues[i + 1]["a"] - GAP if i + 1 < len(cues) else c["a"] + 99
        c["b"] = min(max(c["b"], c["a"] + MIN), nxt) if c["b"] - c["a"] < MIN else c["b"]
    return cues


def ts(s):
    ms = int(round(s * 1000)); return "%02d:%02d:%02d,%03d" % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)


def main(src, dst):
    cues = stretch(merge(sentences(json.load(open(src, encoding="utf-8")))))
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        for i, c in enumerate(cues, 1):
            f.write("%d\n%s --> %s\n%s\n\n" % (i, ts(c["a"]), ts(c["b"]), c["t"]))
    short = [c["t"] for c in cues if c["b"] - c["a"] < MIN - 1e-6]
    print("%d cues -> %s | under %.1fs: %s" % (len(cues), dst, MIN, short or "none"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
