"""Shared rules for the hunt-kit challenge gates (prerequisites, quote validity, ANCHOR rules, card + judge parsing)."""
import json, re, sys
from functools import lru_cache
from pathlib import Path
from _kjv import check, K

GOSPELS = ("Matthew", "Mark", "Luke", "John")  # same list loom.py uses for its Gospel-parallel section
NT = set("Matthew Mark Luke John Acts Romans 1Corinthians 2Corinthians Galatians Ephesians Philippians Colossians "
         "1Thessalonians 2Thessalonians 1Timothy 2Timothy Titus Philemon Hebrews James 1Peter 2Peter 1John 2John 3John "
         "Jude Revelation".split())
STEMS = {p.stem.lower(): p.stem for p in K.glob("*.json") if p.stem != "Books"}
ALIAS = {"psalm": "psalms", "songofsongs": "songofsolomon", "canticles": "songofsolomon", "revelationofjohn": "revelation"}
PAT = re.compile(r'((?:[1-3] ?)?[A-Z][a-z]+(?: of [A-Z][a-z]+)? \d+:\d+(?:-\d+)?)[ \t*_:,—-]{1,6}"([^"\n]*)"')
REF = re.compile(r"((?:[1-3]\s*)?[A-Za-z][A-Za-z ]*?)\s+(\d+):(\d+)(?:\s*[-–]\s*(\d+))?")
ANYREF = re.compile(r"(?:[1-3] ?)?[A-Z][a-z]+(?: of [A-Z][a-z]+)? \d+:\d+(?:-\d+)?")
STOP = set("the and of to a in that he it is was for unto his thou thy them they with be i him me my not but as on by all ye "
           "shall from will said had have are which then there when this were thee thine hath their".split())


def need(T, who):
    """Prerequisites, checked at every entry point. Exits 1 with a clear REFUSED message."""
    miss = []
    loom, ss = T / "loom.md", T / "SUNDAY_SCHOOL.md"
    if not loom.exists():
        miss.append('loom.md missing -> loom.py <topic_dir> "Book C:V-V"')
    else:
        t = loom.read_text(encoding="utf-8")
        if not t.startswith("# LOOM - "):
            miss.append("loom.md does not start with the loom.py header '# LOOM - <passage>'")
        elif not re.search(r"^- .+", t, re.M):
            miss.append("loom.md has no match lines")
    if not ss.exists():
        miss.append('SUNDAY_SCHOOL.md missing -> sunday_school.py <topic_dir> "Book C:V-V"')
    elif len(re.findall(r"^\s*[-*] \S", ss.read_text(encoding="utf-8"), re.M)) < 5:
        miss.append("SUNDAY_SCHOOL.md has fewer than 5 bullet items")
    for f in ("BRIEF.md", "KJV_PACK.md"):
        if not (T / f).exists():
            miss.append(f"{f} missing")
    if miss:
        sys.exit(f"{who}: REFUSED - in {T}:\n  " + "\n  ".join(miss))


@lru_cache(None)
def _chapter(stem, ch):
    d = json.loads((K / f"{stem}.json").read_text(encoding="utf-8-sig"))
    c = next((x for x in d["chapters"] if str(x["chapter"]) == str(ch)), None)
    return {int(v["verse"]): v["text"] for v in c["verses"]} if c else {}


def parse_ref(ref):
    """'Psalm 23:1-3' -> ('Psalms', 23, 1, 3) if that book/chapter/verses exist in kjv_full, else None."""
    m = REF.fullmatch(ref.strip())
    if not m:
        return None
    k = re.sub(r"[^a-z0-9]", "", m.group(1).lower())
    stem = STEMS.get(ALIAS.get(k, k))
    if not stem:
        return None
    ch, v1 = int(m.group(2)), int(m.group(3))
    v2 = int(m.group(4) or v1)
    have = _chapter(stem, ch)
    if v2 < v1 or not all(v in have for v in range(v1, v2 + 1)):
        return None
    return stem, ch, v1, v2


def fmt(p):
    return f"{p[0]} {p[1]}:{p[2]}" + (f"-{p[3]}" if p[3] != p[2] else "")


def vtext(p):
    return " ".join(_chapter(p[0], p[1])[v] for v in range(p[2], p[3] + 1))


def overlap(a, b):
    return a[0] == b[0] and a[1] == b[1] and a[2] <= b[3] and b[2] <= a[3]


def valid_quote(ref, quote):
    """(ok, reason, parsed_ref). Needs a real ref, >=4 real words, and every piece found in the KJV verse(s)."""
    p = parse_ref(ref)
    if not p:
        return False, f"bad reference '{ref}'", None
    pieces = [x for x in re.split(r"\.{3,}|…", quote) if re.search("[A-Za-z]", x)]
    if len(re.findall(r"[A-Za-z']+", " ".join(pieces))) < 4:
        return False, "quote has fewer than 4 real words", p
    if not all(check(fmt(p), x)[0] for x in pieces):
        return False, f"quote not in KJV {fmt(p)}", p
    return True, "", p


def card_text(T):
    parts = re.split(r"^##\s+ANGLE\s+(\w+)\b", (T / "CARDS.md").read_text(encoding="utf-8"), flags=re.M)
    return {parts[i].upper(): parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def _clean(t):
    return re.sub("[“”]", '"', t).replace("’", "'")


def field(txt, key):
    m = re.search(rf"^[\s*_`>#-]*{key}\s*:\s*(.+)$", _clean(txt), re.M | re.I)
    return re.sub(r"[*`]", "", m.group(1)).strip() if m else ""


def ref_quote(s):
    m = re.match(r'(.*?\d+:\d+(?:\s*[-–]\s*\d+)?)\s*[:,—-]?\s*"(.*)"', s)
    return (m.group(1).strip(), m.group(2).strip()) if m else None


def labels(txt):
    head = re.split(r"\(| - |—", field(txt, "LABEL"))[0].upper()
    return re.findall(r"PROPHECY|NT-STATED|ECHO|DETAIL", head)


def loom_info(T):
    """(episode passage, refs of the verbatim/thematic matches, refs of the Gospel parallels)"""
    t = (T / "loom.md").read_text(encoding="utf-8")
    pas = parse_ref(re.match(r"# LOOM - (.+)", t).group(1))
    body, _, par = t.partition("## Gospel parallels")
    refs = lambda s: [p for p in map(parse_ref, ANYREF.findall(s)) if p]
    return pas, refs(body.partition("##")[2]), refs(par)


def shared_phrase(a, b):
    w = lambda s: re.sub(r"[^a-z' ]", "", s.lower()).split()
    wa, wb = w(a), w(b)
    grams = lambda ws, n: {tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)}
    for n in range(8, 2, -1):
        for g in grams(wa, n) & grams(wb, n):
            if sum(x not in STOP for x in g) >= 3:
                return " ".join(g)
    return ""


def card_problems(txt, T):
    """(list of reasons this card fails the ANCHOR gate, {key: parsed ref}). Empty list = card is well formed."""
    why, got = [], {}
    for key in ("ANCHOR-1", "ANCHOR-2", "WHY-VERSE"):
        raw = field(txt, key)
        if not raw:
            why.append(f"{key} missing")
            continue
        rq = ref_quote(raw)
        if not rq:
            why.append(f'{key} not in the form Book C:V "quote"')
            continue
        ok, reason, p = valid_quote(*rq)
        if ok:
            got[key] = p
        else:
            why.append(f"{key} {reason}")
    for ref, q in PAT.findall(_clean(txt)):  # every other counted-looking quote on the card must be real too
        if not valid_quote(ref, q)[0]:
            why.append(f"bad quote {ref}")
    lab = labels(txt)
    if not lab:
        why.append("LABEL missing or not PROPHECY/NT-STATED/ECHO/DETAIL")
    elif set(lab) == {"DETAIL"}:
        why.append("DETAIL-only card (two-book rule)")
    passage, matches, parallels = loom_info(T)
    a1, a2, wv = got.get("ANCHOR-1"), got.get("ANCHOR-2"), got.get("WHY-VERSE")
    if a1 and not (a1[0] == passage[0] and a1[1] == passage[1] and passage[2] <= a1[2] and a1[3] <= passage[3]):
        why.append(f"ANCHOR-1 {fmt(a1)} is outside the passage {fmt(passage)}")
    if a1 and a2:
        if a2[0] == a1[0]:
            why.append("ANCHOR-2 is the same book as ANCHOR-1 (two-book rule)")
        elif a1[0] in GOSPELS and a2[0] in GOSPELS:
            why.append("ANCHOR-2 is a Gospel parallel (another Gospel)")
        elif any(overlap(a2, q) for q in parallels):
            why.append("ANCHOR-2 is in loom.md's Gospel parallels")
    if wv and ("PROPHECY" in lab or "NT-STATED" in lab) and wv[0] not in NT:
        why.append("WHY-VERSE must be a New Testament verse for PROPHECY/NT-STATED")
    if a1 and a2 and "ECHO" in lab and not shared_phrase(vtext(a1), vtext(a2)) and not any(overlap(a2, q) for q in matches):
        why.append("ECHO: no shared 3-word phrase and ANCHOR-2 not in loom.md matches")
    return why, got


JKEYS = ["FRESH", "TRUE", "CLEAR", "JESUS", "GROWTH", "DEPTH"]
ROW = re.compile(r"^[\s#>\-•]*ANGLE\s+([A-Za-z0-9]+)\b(.*)$", re.M | re.I)
SEP = r"\s*(?:\([^)]*\))?\s*[:=|\-–]*\s*"


def judge_rows(path):
    """{card: {KEY: float, SOUND: PASS/FLAG, COMMON: yes/no/partly}}. Tolerates bold/italics and : | - separators.
    If a card has several lines, the one with the most parsed values wins."""
    text = re.sub(r"[*_`]", "", Path(path).read_text(encoding="utf-8", errors="replace"))
    out = {}
    for cid, rest in ROW.findall(text):
        r = {}
        for k in JKEYS:
            m = re.search(rf"\b{k}{SEP}(\d+(?:\.\d+)?)", rest, re.I)
            if m and 0 <= float(m.group(1)) <= 10:
                r[k] = float(m.group(1))
        m = re.search(rf"\bSOUND{SEP}(PASS|FLAG)", rest, re.I)
        if m:
            r["SOUND"] = m.group(1).upper()
        m = re.search(rf"\bCOMMON\s*\??{SEP}(yes|no|partly)", rest, re.I)
        if m:
            r["COMMON"] = m.group(1).lower()
        c = cid.upper(); prev = out.get(c, {})
        best = dict(r) if len(r) > len(prev) else dict(prev)
        # objections are never lost: any FLAG wins, the worst COMMON wins
        if "FLAG" in (r.get("SOUND"), prev.get("SOUND")):
            best["SOUND"] = "FLAG"
        rank = {"no": 0, "partly": 1, "yes": 2}
        cs = [x for x in (r.get("COMMON"), prev.get("COMMON")) if x]
        if cs:
            best["COMMON"] = max(cs, key=rank.get)
        out[c] = best
    return out


def context_rows(path):
    """{card: PASS|FAIL} from lines 'ANGLE A | PASS | why'. Any FAIL line for a card wins."""
    out = {}
    text = re.sub(r"[*_`]", "", Path(path).read_text(encoding="utf-8", errors="replace"))
    for cid, rest in ROW.findall(text):
        m = re.search(r"\b(PASS|FAIL)\b", rest, re.I)
        if m:
            c = cid.upper()
            out[c] = "FAIL" if "FAIL" in (m.group(1).upper(), out.get(c)) else "PASS"
    return out


def context_block(p):
    ch = _chapter(p[0], p[1])
    lo, hi = max(min(ch), p[2] - 10), min(max(ch), p[3] + 10)
    return "\n".join(f"{'>>' if p[2] <= v <= p[3] else '  '} {p[0]} {p[1]}:{v} {ch[v]}" for v in range(lo, hi + 1))
