"""corpus_diversity.py — the CROSS-PIECE staleness gate the per-piece panel can't see.

The 5-CLI panel and the EW-G* gates judge ONE narration at a time, so they are blind to
repetition ACROSS a set (every short ending "Come to Jesus", every hook "I was there…",
the same KJV quote, the same closing verb). This deterministic check looks at a WHOLE set
and flags sameness — run it before a batch/series is declared done.

Usage:
  .venv\\Scripts\\python.exe corpus_diversity.py longform\\EW0*\\v1\\short   --form short
  .venv\\Scripts\\python.exe corpus_diversity.py longform\\EW0*\\v1          --form long
  (pass any folders/globs that contain narration.md; --warn-exit makes it exit 1 on WARN)
"""
import argparse, glob, json, re, sys
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from pipeline.eyewitness_gates import parse_witness  # noqa: E402

RULES = json.loads((ROOT / "data" / "eyewitness_rules.json").read_text(encoding="utf-8"))
INV_VERBS = RULES["invitation_verbs"]
STOP = set("the a an and or but of to in on at for with from is was are be he his him her "
           "you your they them it its i me my we us our that this these those as so not no "
           "who whom which what when where why how all any one two his their s t".split())


def words(text):
    return re.findall(r"[a-z']+", text.lower())


def content_words(text):
    return [w for w in words(text) if w not in STOP and len(w) > 2]


def ngrams(ws, n):
    return {" ".join(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / max(1, len(a | b))


def last_sentence(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return parts[-1] if parts else text


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+", help="folders/globs containing narration.md")
    ap.add_argument("--form", choices=["short", "long"], default="short")
    ap.add_argument("--warn-exit", action="store_true", help="exit 1 if any WARN fires")
    args = ap.parse_args()

    folders = []
    for p in args.paths:
        folders += [Path(x) for x in glob.glob(p)] if any(c in p for c in "*?[") else [Path(p)]
    pieces = []
    for f in sorted(folders):
        md = f / "narration.md"
        if not md.is_file():
            continue
        pw = parse_witness(md.read_text(encoding="utf-8"))
        if not pw.beats:
            continue
        hook, cta = pw.beats[0].spoken, pw.beats[-1].spoken
        close = last_sentence(cta)
        # the operative verb is the one in the CLOSING sentence (what actually lands),
        # not the first invitation verb buried in a long contemplative beat.
        cverbs = [v for v in INV_VERBS if re.search(rf"\b{re.escape(v)}\b", close.lower())]
        pieces.append({"name": f.parts[-3] if f.name == "short" else f.parts[-2],
                       "hook": hook, "cta": cta, "close": close, "verbs": cverbs})
    n = len(pieces)
    if n < 3:
        print(f"[corpus] only {n} piece(s) — need >=3 to judge diversity."); return 0

    warns = []
    print(f"[corpus] {n} pieces · form={args.form}\n")

    # 1) closing-verb spread — a dominant verb = the "stamp"
    primary = Counter(p["verbs"][0] if p["verbs"] else "(none)" for p in pieces)
    print("CLOSING VERB SPREAD:", dict(primary))
    top_v, top_c = primary.most_common(1)[0]
    if top_c > max(2, round(0.40 * n)):
        warns.append(f"verb '{top_v}' closes {top_c}/{n} pieces (>40%) — widen the ending palette")

    # 2) near-duplicate CLOSES (the actual last sentence)
    dupes = []
    for a, b in combinations(pieces, 2):
        sim = jaccard(content_words(a["close"]), content_words(b["close"]))
        if sim >= 0.45:
            dupes.append((a["name"], b["name"], round(sim, 2)))
    if dupes:
        warns.append(f"{len(dupes)} near-duplicate closing line pair(s)")
    print("\nNEAR-DUP CLOSING PAIRS (>=0.45):", dupes or "none")

    # 3) phrases shared across many closes (the repeated stamp, e.g. 'come to jesus')
    shared = Counter()
    for p in pieces:
        for g in ngrams(words(p["close"]), 3):
            shared[g] += 1
    repeated = [(g, c) for g, c in shared.most_common(8) if c >= max(3, round(0.33 * n))]
    if repeated:
        warns.append(f"closing phrase(s) repeated across >=1/3 of pieces: {[g for g, _ in repeated]}")
    print("REPEATED CLOSING 3-GRAMS (>=1/3):", repeated or "none")

    # 4) hook sameness (same opening shape)
    hdupes = [(a["name"], b["name"]) for a, b in combinations(pieces, 2)
              if jaccard(content_words(a["hook"]), content_words(b["hook"])) >= 0.5]
    if hdupes:
        warns.append(f"{len(hdupes)} near-duplicate hook pair(s)")
    print("NEAR-DUP HOOK PAIRS (>=0.5):", hdupes or "none")

    print("\nPER-PIECE CLOSE:")
    for p in pieces:
        print(f"  {p['name']:22} [{','.join(p['verbs']) or '-'}]  …{p['close'][-70:]}")

    print("\n" + ("=" * 60))
    if warns:
        print("VERDICT: WARN — cross-piece sameness:")
        for w in warns:
            print("  •", w)
        return 1 if args.warn_exit else 0
    print("VERDICT: PASS — endings/hooks are diverse across the set.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
