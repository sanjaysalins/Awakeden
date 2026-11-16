"""Gate 5: python gate.py <topic_dir> [--driver 1]     (default Driver 2: GROWTH is also required)
Per card, ALL must hold - the gate never waives anything:
  ANCHOR rules (see _rules.card_problems) - real KJV quotes, 2 different books, WHY-VERSE, honest LABEL
  5+ distinct judge files, each with a parsed row (every score, SOUND, COMMON) for every card
  medians: FRESH 7, TRUE 8, CLEAR 7, JESUS 8, GROWTH 7 (Driver 2), DEPTH 7; no SOUND flag from any judge
  one non-Claude judge (codex/gemini/grok) at or above the FRESH and DEPTH bars
  COMMON: fewer than 2 judges say yes/partly
  CONTEXT PASS from both context_codex.md and context_gemini.md (context_check.py)
  every judge/context file newer than CARDS.md (else "stale")
A card with a SOUND flag is reworded and RE-JUDGED with new judge files. Writes GATE.md; no PASS -> exit 1."""
import hashlib, sys
from statistics import median
from pathlib import Path
from _rules import need, card_text, card_problems, judge_rows, context_rows

BARS = {"FRESH": 7, "TRUE": 8, "CLEAR": 7, "JESUS": 8, "GROWTH": 7, "DEPTH": 7}
NONCLAUDE = ("codex", "gemini", "grok")
CTX_SEATS = ("codex", "gemini")


def evaluate(T, d1=False):
    """-> dict(rows=[...], judges=[names], bars={}, texts={}). Does not write anything."""
    bars = {k: v for k, v in BARS.items() if not (d1 and k == "GROWTH")}
    texts = card_text(T)
    # judgments go stale if ANY prompt input changed after them
    cards_m = max((T / f).stat().st_mtime for f in ("CARDS.md", "SUNDAY_SCHOOL.md", "KJV_PACK.md", "JUDGE_BRIEF.md") if (T / f).exists())
    files = sorted(f for f in T.glob("judge_*.md") if f.name.startswith("judge_"))
    names = [f.stem[6:] for f in files]
    glob = []
    distinct = len({hashlib.md5(f.read_bytes()).hexdigest() for f in files})
    if distinct < 5:
        glob.append(f"need 5+ distinct judge files (have {distinct})")
    glob += [f"stale ({f.name} older than CARDS.md)" for f in files if f.stat().st_mtime <= cards_m]
    judged = {n: judge_rows(f) for n, f in zip(names, files)}
    ctx, ctx_files = {}, {}
    for s in CTX_SEATS:
        f = T / f"context_{s}.md"
        ctx_files[s] = f
        if f.exists():
            ctx[s] = context_rows(f)
            if f.stat().st_mtime <= cards_m:
                glob.append(f"stale ({f.name} older than CARDS.md)")
    need_keys = list(bars) + ["SOUND", "COMMON"]
    rows = []
    for cid in sorted(texts):
        why = list(glob)
        pw, got = card_problems(texts[cid], T)
        why += pw
        vals = {n: judged[n].get(cid, {}) for n in names}
        for n in names:
            if any(k not in vals[n] for k in need_keys):
                why.append(f"unparsed ({n})")
        med = {k: median(v[k] for v in vals.values() if k in v) for k in bars if any(k in v for v in vals.values())}
        why += [f"{k} {med[k]:g}<{b}" for k, b in bars.items() if k in med and med[k] < b]
        flags = [n for n in names if vals[n].get("SOUND") == "FLAG"]
        if flags:
            why.append(f"SOUND flag from {', '.join(flags)} (no waiver: reword and re-judge)")
        com = sum(v.get("COMMON") in ("yes", "partly") for v in vals.values())
        if com >= 2:
            why.append(f"COMMON yes/partly from {com} judges")
        if not any(any(x in n.lower() for x in NONCLAUDE) and vals[n].get("FRESH", 0) >= bars["FRESH"]
                   and vals[n].get("DEPTH", 0) >= bars["DEPTH"] for n in names):
            why.append("no non-Claude judge (codex/gemini/grok) at the FRESH and DEPTH bars")
        for s in CTX_SEATS:
            r = ctx.get(s, {}).get(cid)
            if r != "PASS":
                why.append(f"CONTEXT {s} " + ("missing" if r is None else "FAIL"))
        rows.append(dict(cid=cid, med=med, why=list(dict.fromkeys(why)), com=com, flags=flags, anchors=got))
    return dict(rows=rows, judges=names, bars=bars, texts=texts)


def main():
    T = Path(sys.argv[1]).resolve()
    need(T, "gate")
    if not (T / "CARDS.md").exists():
        sys.exit(f"gate: REFUSED - {T / 'CARDS.md'} missing")
    d1 = "--driver" in sys.argv and sys.argv[sys.argv.index("--driver") + 1] == "1"
    r = evaluate(T, d1)
    out = [f"# GATE - {T.name}", "", f"Judges read: {len(r['judges'])} ({', '.join(r['judges'])}). Driver {1 if d1 else 2}. "
           "Bars: " + ", ".join(f"{k} {v}" for k, v in r["bars"].items()) +
           ", SOUND no flags, COMMON under 2, 1 non-Claude judge, CONTEXT PASS x2, anchors valid.", "",
           "| Card | FRESH | TRUE | CLEAR | JESUS | GROWTH | DEPTH | COMMON yes/partly | Result |", "|---|---|---|---|---|---|---|---|---|"]
    for x in r["rows"]:
        g = lambda k: f"{x['med'][k]:g}" if k in x["med"] else "-"
        out.append(f"| {x['cid']} | {g('FRESH')} | {g('TRUE')} | {g('CLEAR')} | {g('JESUS')} | {g('GROWTH')} | {g('DEPTH')} | {x['com']} | "
                   + ("PASS" if not x["why"] else "FAIL: " + "; ".join(x["why"])) + " |")
    passed = [x["cid"] for x in r["rows"] if not x["why"]]
    out += ["", f"PASS cards: {', '.join(passed) or 'none'}"]
    if not passed:
        out += ["", "NO PASS - NO FILM: reword + re-judge, or pick another topic"]
    (T / "GATE.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
