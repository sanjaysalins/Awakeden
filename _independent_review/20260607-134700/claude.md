# Independent review — claude (OK, 143s)

I read all three files: `pipeline/kjv_strict.py`, its dependency `PythonProject1/.../short_gate/kjv.py`, and `pipeline/narration_parse.py`. The core works (the Ps 22:7 comma blocks correctly), but there are real holes.

## FALSE-PASS holes (a real misquote slips through)

**1. Ellipsis splits ignore ORDER and cross verse joins — the headline hole.**
`_fragments_in` (line 111-118) splits on `…`/`...` and checks each fragment as an independent substring, in NO order. Ps 22:1 is `my God, my God, why hast thou forsaken me?`. A quote written `"why hast thou forsaken me … my God, my God"` (clauses reversed) → both fragments are substrings → **OK**. Same across a range ref: `_verse_text` joins vv with a space (line 108), so `"Psalm 22:16-18"` accepts a v18 fragment `…` a v16 fragment in reversed scriptural order. Verbatim should mean order-preserving; this doesn't enforce it.

**2. Empty / punctuation-only fragment passes against ANY ref.**
Line 116: `if f and f not in text`. A fragment that canon+`strip(_TERMINAL)`s to `""` is skipped. So `verify_span("Psalm 999:1", ".")` → fragment `"."` → strip → `""` → loop skips → returns `True` → **OK**. A quote of only `"…"` or `"."` certifies verbatim against anything. Degenerate, but it's a fail-OPEN.

**3. Inline resolution can mask a real misquote by matching a DIFFERENT verse.**
`resolve_inline` → `_chapter_text` (line 138-154) concatenates the WHOLE chapter, then `_fragments_in` substring-matches. Any short phrase is almost certainly a substring of the full chapter — even one that straddles a verse boundary (end of v3 + start of v4). So a phrase that misquotes verse X but happens to be a substring elsewhere in the chapter returns **OK** instead of WARN. Harm is bounded (inline never blocks; worst case is false reassurance, not a false block), but the "verbatim located" claim is overstated.

**4. Inline misquotes never block — including real ones.**
Your own B1 result proves it: the one defect found (`my brethren,` vs KJV `my brethren:`) was a *real* misquote, and it only produced an advisory WARN because it was inline. The blocking power of this gate is limited to **tagged** `— KJV, ref` blocks. If corrupt text lands in an untagged inline echo, it ships. State this limit plainly.

## FALSE-BLOCK / crash holes

**5. Malformed range ref CRASHES the whole audit (not a graceful UNRESOLVED).**
`REF_RX` group 3 is `[\d,–—\- ]+`, so `"Psalm 22:6-"` parses. `_verse_text` (line 105) calls `_SG.verses_for`, which does unguarded `int(start)`/`int(end)` (short_gate line 98-99) → `int("")` → `ValueError` propagates out of `verify_span` → `verify_narration` → `audit_paths`. One typo'd header ref takes down the entire batch instead of reporting a finding. `_verse_text` only try/excepts the chapter int (line 101-104), not `verses_for`.

**6. Hyphen folding can false-block.** `_canon` (line 82) folds dashes to `-` but never removes `-`. short_gate's `norm` strips it entirely. So a hyphenation difference (`loving-kindness` vs corpus `lovingkindness`, or a verse-internal em-dash the author drops) → not a substring → **MISQUOTE** on correct text. Corpus-dependent, but it's an inconsistency between the two canonicalizers.

## Robustness / import

**7. Import-time hard crash = large blast radius.** Line 57 runs `_load_sg_kjv()` at module import. If the sibling repo / corpus is absent, importing `kjv_strict` raises `FileNotFoundError` — so any module that merely imports it (e.g. wired into `runner.py`) crashes at import, taking down the whole text engine, not just the KJV gate. Make the load lazy (first-use), so a missing corpus disables one gate instead of the pipeline.

**8. No corpus integrity check.** The entire premise is "the cached text was corrupt." This verifier then *trusts* `kjv.json` as gold with zero hash/version assertion (`corpus_provenance` records the path but never validates content). If the resolved `kjv.json` (local vs HF-POC fallback, short_gate line 47-57) has its own dropped comma, every misquote there certifies OK. Your only canary is the single Ps 22:7 unit test. Add a few known-verse spot checks or a corpus hash pin.

**9. `EmptyNarrationError` propagates uncaught** through `verify_narration`/`audit_paths` — same batch-killing pattern as #5 for a narration lacking `**[speaker]**` markers.

## Reuse / cost
Reuse is genuinely good — it imports the real `short_gate/kjv.py` (corpus, `REF_RX`, `resolve_book`, `verses_for`) rather than forking, and matches its marker convention. No metered spend; offline. No over-engineering concerns.

## Bottom line
The flagship purpose — catching the corrupt-cache dropped comma on a *tagged* verse — works and is tested. But #5 is a crash bug, #1 is a true false-pass on any multi-fragment quote, and #7 is an avoidable blast-radius risk. Commit-worthy core, not yet sound to rely on as a gate.

VERDICT: REVISE
TOP FIXES:
1. Guard `verses_for`/range parsing so a malformed ref returns UNRESOLVED instead of crashing the audit (#5), and catch `EmptyNarrationError` per-file (#9).
2. Enforce fragment ORDER in `_fragments_in` (match fragments left-to-right with a moving offset, not independent `in` checks) and reject empty/punctuation-only spans as UNRESOLVED, not OK (#1, #2).
3. Make the `short_gate` load lazy (first-use, not import-time) and add a corpus integrity spot-check beyond the single Ps 22:7 test (#7, #8).
