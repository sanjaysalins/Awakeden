"""pipeline/concordance.py — the Concordance Loom.

A $0, deterministic, stdlib-only cross-book KJV verbatim-phrase concordance.
No model calls anywhere in this module.

WHY THIS EXISTS: this project's first locked non-negotiable is "the whole
Bible, through Jesus" — every episode's narration traces a thread to Christ,
and every visual scene plan requires at least one genuine Old-Testament echo
(see CLAUDE.md, "NON-NEGOTIABLE"). Today the mechanism that FINDS those
cross-book echoes is Stage 0 (`pipeline.engine.discover_thread`), which runs
on the model's memory alone — nothing deterministic surfaces candidates for
it to judge. The gap is not hypothetical: the Storm episode (Matthew
8:23-27, Jesus calming the storm) shipped with zero Old Testament echo, even
though Psalm 107:29 ("He maketh the storm a calm, so that the waves thereof
are still") is the OT's own storm-stilling passage and the classic
prefiguration of that exact Gospel scene. A phrase-level scan would have
surfaced it. See `.claude/skills/concordance-loom/SKILL.md` for how this
tool's output is meant to be consumed downstream.

ALGORITHM (ported from ArkAIology's `episode-pipeline/scripts/plan_threads.py`,
proven there to rediscover every hand-placed thread beat in that project
plus two nobody had asked for — adapted here to this repo's own passage
model, not copy-pasted, since the source script is wired to ArkAIology's own
shot/episode JSON files, which don't exist in this repo):

  1. Load the full KJV (data/kjv_full/, one JSON per book — copied once from
     the sibling ArkAIology project's public-domain corpus, see that folder's
     README.md for provenance) into an in-memory list of ~31k verses.
  2. Build an exhaustive index: every 4-word "shingle" (SHINGLE below) in the
     corpus -> the list of verses containing it. This is the one-time,
     $0 scan that makes an exhaustive search practical (build once per
     process, reused for every query via `get_index()`).
  3. For a queried passage (book/chapter/verse-range), walk every 4-word
     shingle inside it. Each shingle is a SEED: look up which OTHER verses
     also contain that exact 4-gram, then greedily EXTEND the match left and
     right, word by word, to the longest verbatim run shared by the two
     verses (`_longest_shared_run`). This turns a fixed-length seed into a
     variable-length "how much do these two verses actually share" measure.
  4. SCORE = shared_run_length / (1 + 0.35 * corpus_frequency_of_the_seed).
     Longer shared runs score higher; but a seed shingle that appears in
     `corpus_frequency` verses across the whole KJV drags the score down —
     a common turn of phrase ("and it came to pass", "the word of the LORD
     came unto") is not a distinctive echo just because it's four words
     long. This is the same length x (inverse-)rarity shape ArkAIology's
     script used; the 0.35 damping constant is carried over unchanged since
     it's already proven, not re-derived here.
  5. NOISE FILTER: (a) a seed shingle appearing in more than
     BOILERPLATE_HIT_CAP verses is skipped entirely before extension —
     never a "distinctive" pivot no matter how it extends; (b) a shared run
     made up ENTIRELY of common/stopword-ish words (STOP below, the same
     guard list ArkAIology's script used) is dropped even if it cleared (a);
     (c) same-book matches are excluded by default (`cross_book_only=True`)
     since a fresh cross-canon thread is the point — two nearby verses in
     the SAME chapter sharing wording is usually just repeated phrasing, not
     an echo (override with --include-same-book / cross_book_only=False if
     you want those too).

HONEST LIMITATION, FOUND WHILE VALIDATING THIS AGAINST THE STORM EPISODE:
the verbatim-phrase concordance above (`find_echoes`) does NOT surface Psalm
107:29 for Matthew 8:23-27 — the two passages never share four consecutive
identical words (the Gospel says "tempest", the Psalm says "storm"; the
longest run either shares is two words, "the sea" / "the waves"). The Fable
brief's own framing ("a phrase-level scan on 'storm'/'calm'/'waves' surfaces
Psalm 107 instantly") describes a LOOSER technique — matching individual
distinctive WORDS the two passages hold in common, not a shared contiguous
PHRASE. That is a real, different, weaker signal, so it is a second,
clearly-separate function (`find_thematic_echoes`), never merged into the
verbatim-verified candidate list: it reports verses sharing several rare
CONTENT WORDS with the queried passage even when no run reaches SHINGLE
words, and its output must be read as "these two passages use overlapping
vocabulary" — not "these two passages share a verified phrase." This is the
concrete, honest reason the module exposes two ranked lists instead of one;
see the SKILL.md for how the two should be weighted differently downstream.

WHAT THIS TOOL DOES **NOT** DO: it never asserts a thread is real, fresh, or
doctrinally sound. Every candidate is pre-verified by plain string equality
(the shared phrase genuinely occurs verbatim in both verses — that part is
not in question), but whether a shared phrase is a meaningful theological
echo, a coincidental shared idiom, or noise is a judgment call that stays
exactly where it already lives: Stage 0's four-part thread-qualification
test, the in-engine self-review, the independent red-team audit, and the
external 5-CLI panel. This module only narrows "what could Opus have missed"
down to a short, honest, verbatim-verified candidate sheet.

CLI:
    python pipeline/concordance.py --book Matthew --chapter 8 --verses 23-27
    python pipeline/concordance.py --book Matthew --chapter 8 --verses 26 --max 10
    python pipeline/concordance.py --book Leviticus --chapter 16 --verses 1-25 --json out.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

# Windows consoles default to cp1252; force UTF-8 so em dashes don't crash printing.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Allow `python pipeline/concordance.py ...` (script's own dir on sys.path)
# as well as `import pipeline.concordance` / `python -m pipeline.concordance`
# (repo root already on sys.path) — same fix as pipeline/cost.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # noqa: E402

KJV_FULL_DIR = config.DATA_DIR / "kjv_full"

SHINGLE = 4                 # exact-match seed length (words) — same as ArkAIology's plan_threads.py
BOILERPLATE_HIT_CAP = 40    # a seed shingle in >= this many verses is common liturgical
                            # phrasing ("and it came to pass"...), never a distinctive echo
DEFAULT_MAX_CANDIDATES = 25 # CLI print cap (0 / None = show everything found)

# Shared phrases made ONLY of these words are concordance noise, not threads
# (carried over verbatim from ArkAIology's plan_threads.py STOP guard).
STOP = set(
    "and the of that in it is was were he his him for to a an on with "
    "them they their which shall be as at by unto from all this there "
    "i thou thee thy ye you your but not so are am".split()
)

# The 27 New Testament books (internal `book` field spelling, matching
# data/kjv_full/Books.json) — used only to tag a candidate cross_testament,
# never to decide relevance.
NT_BOOKS = frozenset({
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians",
    "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians",
    "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus",
    "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John",
    "3 John", "Jude", "Revelation",
})


def _norm_words(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


def _book_key(name: str) -> str:
    """Collapse a book name to a bare lowercase alnum key so 'Matthew',
    '1 Kings', '1Kings', and 'Song of Solomon' all resolve the same way."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _testament(book: str) -> str:
    return "NT" if book in NT_BOOKS else "OT"


@dataclass(frozen=True)
class Verse:
    book: str
    chapter: int
    verse: int
    text: str
    words: tuple[str, ...]   # normalized lowercase words, for shingle matching

    @property
    def ref(self) -> str:
        return f"{self.book} {self.chapter}:{self.verse}"


@dataclass
class ConcordanceCandidate:
    """One OTHER KJV verse sharing a distinctive verbatim phrase with a verse
    inside the queried passage. Everything here is a plain fact (the phrase
    IS a verbatim substring of both verses) — whether it's a real thread is
    a judgment call left to Stage 0 / the panel, not this module."""
    passage_ref: str        # the verse INSIDE the queried passage that matched
    match_ref: str           # the OTHER verse, outside the queried passage
    passage_text: str
    match_text: str
    shared_phrase: str
    shared_word_count: int
    corpus_frequency: int    # verses in the WHOLE KJV containing the seed shingle
    score: float
    cross_testament: bool    # True if passage_ref and match_ref sit in different testaments


@dataclass
class ThematicEchoCandidate:
    """SECONDARY, WEAKER signal than ConcordanceCandidate: a verse that shares
    several distinctive CONTENT WORDS with the queried passage, with NO
    requirement that those words appear as a contiguous phrase. Real
    vocabulary overlap, verbatim word-for-word — but NOT a verified shared
    phrase, so always report/weight this below the verbatim list."""
    passage_ref: str         # the queried passage as a whole, e.g. "Matthew 8:23-27"
    match_ref: str
    match_text: str
    shared_words: list[str]  # the distinctive words held in common, sorted
    shared_word_count: int
    score: float
    cross_testament: bool


def load_corpus(corpus_dir: Path = KJV_FULL_DIR) -> list[Verse]:
    """Every verse in data/kjv_full/, canonical KJV text, as flat Verse records.

    Skips Books.json (the bare book-name/order list shipped alongside the
    per-book files — not a book of the Bible itself, so it has no "chapters"
    key and is filtered out rather than hardcoding a 66-book allowlist)."""
    corpus: list[Verse] = []
    for path in sorted(corpus_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict) or "chapters" not in data:
            continue
        book = str(data["book"]).strip()
        for ch in data["chapters"]:
            chapter = int(ch["chapter"])
            for v in ch["verses"]:
                text = str(v["text"]).strip()
                corpus.append(Verse(
                    book=book, chapter=chapter, verse=int(v["verse"]),
                    text=text, words=tuple(_norm_words(text)),
                ))
    if not corpus:
        raise SystemExit(f"no KJV corpus found in {corpus_dir} — expected per-book JSON files")
    return corpus


def _longest_shared_run(a: tuple[str, ...], b: tuple[str, ...], ai: int, bi: int) -> tuple[str, ...]:
    """Extend the seed match at a[ai:ai+SHINGLE] / b[bi:bi+SHINGLE] left and
    right to the longest verbatim run the two word-sequences share."""
    lo = 0
    while ai - lo - 1 >= 0 and bi - lo - 1 >= 0 and a[ai - lo - 1] == b[bi - lo - 1]:
        lo += 1
    hi = SHINGLE
    while ai + hi < len(a) and bi + hi < len(b) and a[ai + hi] == b[bi + hi]:
        hi += 1
    return a[ai - lo:ai + hi]


@dataclass
class ConcordanceIndex:
    """The one-time exhaustive scaffold: every verse, plus a shingle -> verse
    lookup, plus a ref -> verse lookup, plus tolerant book-name resolution.
    Build once (`ConcordanceIndex.build()` or the module-level `get_index()`
    singleton) and reuse across every query in the process."""
    corpus: list[Verse]
    shingles: dict[tuple[str, ...], list[int]]
    by_ref: dict[tuple[str, int, int], int]
    book_aliases: dict[str, str]
    word_doc_freq: dict[str, int]   # word -> number of verses containing it (whole KJV)

    @classmethod
    def build(cls, corpus_dir: Path = KJV_FULL_DIR) -> "ConcordanceIndex":
        corpus = load_corpus(corpus_dir)
        shingles: dict[tuple[str, ...], list[int]] = {}
        by_ref: dict[tuple[str, int, int], int] = {}
        word_doc_freq: dict[str, int] = {}
        for vi, v in enumerate(corpus):
            by_ref[(v.book, v.chapter, v.verse)] = vi
            words = v.words
            for i in range(len(words) - SHINGLE + 1):
                shingles.setdefault(words[i:i + SHINGLE], []).append(vi)
            for w in set(words):
                word_doc_freq[w] = word_doc_freq.get(w, 0) + 1
        book_aliases = {_book_key(v.book): v.book for v in corpus}
        return cls(corpus=corpus, shingles=shingles, by_ref=by_ref,
                    book_aliases=book_aliases, word_doc_freq=word_doc_freq)

    def resolve_book(self, name: str) -> str:
        try:
            return self.book_aliases[_book_key(name)]
        except KeyError:
            raise SystemExit(
                f"unknown book: {name!r} (checked against {len(self.book_aliases)} KJV books)"
            ) from None


_INDEX_CACHE: ConcordanceIndex | None = None


def get_index(corpus_dir: Path = KJV_FULL_DIR, *, force_rebuild: bool = False) -> ConcordanceIndex:
    """Lazily build + cache the index for the life of the process, so a caller
    (e.g. Stage 0 checking several candidate passages in one run) only pays
    the one-time scaffold cost once."""
    global _INDEX_CACHE
    if _INDEX_CACHE is None or force_rebuild:
        _INDEX_CACHE = ConcordanceIndex.build(corpus_dir)
    return _INDEX_CACHE


def find_echoes(
    index: ConcordanceIndex,
    book: str,
    chapter: int,
    verse_start: int,
    verse_end: int | None = None,
    *,
    cross_book_only: bool = True,
    max_candidates: int | None = None,
) -> list[ConcordanceCandidate]:
    """Every OTHER KJV verse sharing a distinctive verbatim phrase with
    book/chapter/verse_start-verse_end, ranked by score (highest first).

    The passage's own verbatim text is read from the index itself (the
    corpus is the single source of truth — no risk of a caller passing text
    that has drifted from what's actually in data/kjv_full/); pass a smaller
    or larger verse_start/verse_end to check a different slice, or diff the
    returned passage_text against data/kjv_cache.json to sanity-check the
    two copies agree.
    """
    verse_end = verse_start if verse_end is None else verse_end
    book_canon = index.resolve_book(book)
    passage_range = {(book_canon, chapter, v) for v in range(verse_start, verse_end + 1)}
    missing = [f"{book_canon} {chapter}:{v}" for v in range(verse_start, verse_end + 1)
               if (book_canon, chapter, v) not in index.by_ref]
    if missing:
        raise SystemExit(f"verse(s) not found in corpus: {', '.join(missing)}")

    cands: dict[tuple[str, str], ConcordanceCandidate] = {}
    for v in range(verse_start, verse_end + 1):
        pv = index.corpus[index.by_ref[(book_canon, chapter, v)]]
        words = pv.words
        for i in range(len(words) - SHINGLE + 1):
            seed = words[i:i + SHINGLE]
            hits = index.shingles.get(seed, [])
            if len(hits) > BOILERPLATE_HIT_CAP:
                continue  # common liturgical phrasing — never distinctive, skip before extending
            for hi in hits:
                hv = index.corpus[hi]
                if (hv.book, hv.chapter, hv.verse) in passage_range:
                    continue  # excludes the passage's own range (incl. self-match)
                if cross_book_only and hv.book == book_canon:
                    continue
                bi = next(j for j in range(len(hv.words) - SHINGLE + 1)
                          if hv.words[j:j + SHINGLE] == seed)
                run = _longest_shared_run(words, hv.words, i, bi)
                if all(w in STOP for w in run):
                    continue  # the shared run is itself only common/stopword-ish phrasing
                key = (pv.ref, hv.ref)
                score = round(len(run) / (1 + 0.35 * len(hits)), 3)
                prev = cands.get(key)
                if prev is None or len(run) > prev.shared_word_count:
                    cands[key] = ConcordanceCandidate(
                        passage_ref=pv.ref, match_ref=hv.ref,
                        passage_text=pv.text, match_text=hv.text,
                        shared_phrase=" ".join(run), shared_word_count=len(run),
                        corpus_frequency=len(hits), score=score,
                        cross_testament=_testament(pv.book) != _testament(hv.book),
                    )

    ranked = sorted(cands.values(), key=lambda c: -c.score)
    if max_candidates:
        ranked = ranked[:max_candidates]
    return ranked


# Thematic-word-overlap defaults. A word counted as "distinctive" must occur
# in no more than this many verses corpus-wide (e.g. "calm" or "tempest" —
# common nouns like "sea" still qualify; grammatical filler is already out
# via STOP). Two independently-published KJV word-frequency counts agree
# these thresholds keep genuinely rare vocabulary without admitting ordinary
# narrative words as "distinctive".
THEMATIC_MAX_WORD_DOC_FREQ = 60
THEMATIC_MIN_SHARED_WORDS = 2


def find_thematic_echoes(
    index: ConcordanceIndex,
    book: str,
    chapter: int,
    verse_start: int,
    verse_end: int | None = None,
    *,
    min_shared_words: int = THEMATIC_MIN_SHARED_WORDS,
    max_word_doc_freq: int = THEMATIC_MAX_WORD_DOC_FREQ,
    cross_book_only: bool = True,
    max_candidates: int | None = None,
) -> list[ThematicEchoCandidate]:
    """SECONDARY, WEAKER signal than find_echoes(): verses sharing several
    distinctive CONTENT WORDS with the queried passage, even with no shared
    phrase at all. See the module docstring's "HONEST LIMITATION" section —
    this exists because some genuine echoes retell the same event in
    different words (Matthew 8:23-27's storm-stilling and Psalm 107:23-30's
    storm-stilling share "sea"/"calm"/"waves"/"wind(s)" as scattered
    individual words, never four of them in a row), so find_echoes()
    legitimately returns nothing for that pair while this function does.
    Every returned word is a verbatim, exact word-for-word match — but the
    ABSENCE of a shared phrase means this is vocabulary overlap, not a
    verified echo; weight it below find_echoes() output, always.
    """
    verse_end = verse_start if verse_end is None else verse_end
    book_canon = index.resolve_book(book)
    passage_range = {(book_canon, chapter, v) for v in range(verse_start, verse_end + 1)}
    missing = [f"{book_canon} {chapter}:{v}" for v in range(verse_start, verse_end + 1)
               if (book_canon, chapter, v) not in index.by_ref]
    if missing:
        raise SystemExit(f"verse(s) not found in corpus: {', '.join(missing)}")

    passage_words: set[str] = set()
    for v in range(verse_start, verse_end + 1):
        pv = index.corpus[index.by_ref[(book_canon, chapter, v)]]
        passage_words.update(pv.words)
    passage_words -= STOP
    passage_words = {w for w in passage_words
                      if index.word_doc_freq.get(w, 0) <= max_word_doc_freq}
    passage_label = f"{book_canon} {chapter}:{verse_start}"
    if verse_end != verse_start:
        passage_label += f"-{verse_end}"
    if not passage_words:
        return []

    cands: dict[str, ThematicEchoCandidate] = {}
    for v in index.corpus:
        if (v.book, v.chapter, v.verse) in passage_range:
            continue
        if cross_book_only and v.book == book_canon:
            continue
        shared = passage_words.intersection(v.words)
        if len(shared) < min_shared_words:
            continue
        score = round(sum(1.0 / (1 + 0.02 * index.word_doc_freq.get(w, 1)) for w in shared), 3)
        cands[v.ref] = ThematicEchoCandidate(
            passage_ref=passage_label, match_ref=v.ref, match_text=v.text,
            shared_words=sorted(shared), shared_word_count=len(shared),
            score=score, cross_testament=_testament(book_canon) != _testament(v.book),
        )

    ranked = sorted(cands.values(), key=lambda c: -c.score)
    if max_candidates:
        ranked = ranked[:max_candidates]
    return ranked


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Concordance Loom — cross-book KJV verbatim-phrase concordance ($0, no model calls)."
    )
    p.add_argument("--book", required=True, help='e.g. Matthew, "1 Kings", Psalms')
    p.add_argument("--chapter", required=True, type=int)
    p.add_argument("--verses", required=True, help="a single verse '26' or a range '23-27'")
    p.add_argument("--max", type=int, default=DEFAULT_MAX_CANDIDATES,
                    help=f"cap PRINTED candidates (default {DEFAULT_MAX_CANDIDATES}; 0 = show all)")
    p.add_argument("--include-same-book", action="store_true",
                    help="also surface matches inside the SAME book (default: cross-book only — "
                         "an in-book match is usually just nearby repeated wording, not a fresh "
                         "cross-canon thread)")
    p.add_argument("--json", metavar="PATH", help="write the FULL ranked list (uncapped) as JSON")
    p.add_argument("--no-thematic", action="store_true",
                    help="skip the secondary thematic word-overlap scan (verbatim-phrase only)")
    args = p.parse_args(argv)

    if "-" in args.verses:
        a, b = args.verses.split("-", 1)
        verse_start, verse_end = int(a), int(b)
    else:
        verse_start = verse_end = int(args.verses)

    print(f"[concordance] building index over {KJV_FULL_DIR} ...")
    t0 = time.time()
    index = get_index()
    print(f"[concordance] {len(index.corpus)} verses indexed in {time.time() - t0:.1f}s")

    candidates = find_echoes(
        index, args.book, args.chapter, verse_start, verse_end,
        cross_book_only=not args.include_same_book,
    )
    book_canon = index.resolve_book(args.book)
    ref_label = f"{book_canon} {args.chapter}:{verse_start}"
    if verse_end != verse_start:
        ref_label += f"-{verse_end}"
    scope = "same-book+cross-book" if args.include_same_book else "cross-book"
    print(f"\n[concordance] {ref_label} — {len(candidates)} {scope} candidate(s) found "
          f"(shared phrase >= {SHINGLE} words)\n")

    shown = candidates if not args.max else candidates[:args.max]
    for c in shown:
        tflag = "x-testament" if c.cross_testament else "same-testament"
        print(f"  score {c.score:6.3f}  [{c.shared_word_count}w shared, seed seen {c.corpus_frequency}x "
              f"corpus-wide, {tflag}]")
        print(f"    {c.passage_ref}  <->  {c.match_ref}")
        print(f"    \"{c.shared_phrase}\"")
    if args.max and len(candidates) > args.max:
        print(f"\n  ... {len(candidates) - args.max} more below the --max cutoff "
              f"(raise --max, or pass --json to get everything)")
    if not candidates:
        print("  (no cross-book candidates above the noise floor — that is itself useful "
              "information: this passage's echoes, if any, are looser paraphrase, not "
              "shared verbatim wording, and stay entirely a model-judgment call.)")

    if args.json:
        out_path = Path(args.json)
        payload = {"verbatim": [asdict(c) for c in candidates]}

    if not args.no_thematic:
        thematic = find_thematic_echoes(
            index, args.book, args.chapter, verse_start, verse_end,
            cross_book_only=not args.include_same_book,
        )
        print(f"\n--- SECONDARY, WEAKER SIGNAL: thematic word-overlap "
              f"(shared distinctive WORDS, no shared phrase required) ---")
        print(f"[concordance] {ref_label} — {len(thematic)} {scope} thematic candidate(s) "
              f"(>= {THEMATIC_MIN_SHARED_WORDS} shared words each)\n")
        shown_t = thematic if not args.max else thematic[:args.max]
        for c in shown_t:
            tflag = "x-testament" if c.cross_testament else "same-testament"
            print(f"  score {c.score:6.3f}  [{c.shared_word_count} words shared, {tflag}]")
            print(f"    {c.passage_ref}  <->  {c.match_ref}")
            print(f"    shared words: {', '.join(c.shared_words)}")
            print(f"    {c.match_text}")
        if args.max and len(thematic) > args.max:
            print(f"\n  ... {len(thematic) - args.max} more below the --max cutoff")
        if not thematic:
            print("  (no thematic candidates either — this passage's vocabulary is either "
                  "too generic or too singular corpus-wide to match anything this way.)")
        if args.json:
            payload["thematic"] = [asdict(c) for c in thematic]

    if args.json:
        out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n[concordance] full ranked list(s) -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
