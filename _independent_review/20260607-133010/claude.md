# Independent review — claude (OK, 190s)

I read the two real narration formats against the code. The em-dash header parses fine (`**[narrator — KJV, Psalm 22:15]**`), and the long-form's multi-paragraph blocks under one `**[narrator]**` header are captured correctly. But the gate's core claim has real holes. Findings:

## Correctness / false-PASS holes

**1. CTA detection keys ONLY on the trailing 3-gram — trivially evaded by varying the tail.**
`cta_repetition` groups by `_cta_suffix(cta, 3)` = last 3 normalized words of the last sentence. The 8 shorts are caught only because the tag is *literally* the final three words ("come to him"). The moment a writer keeps the templated **lead** but varies the tail — "Come to Him, the crucified King." / "Come to Him, the risen Lord." / "Come to Him and live." — every suffix differs, no suffix key equals "come to him", the containment merge (`suf in NP.normalize(cta)`) never fires because no CTA *ends* in "come to him", and the gate returns **zero findings**. The repeated part of a real CTA is the *lead*, not the tail. This is the exact variation a writer adds, and it defeats the whole gate. Openers correctly use content n-grams across the hook (`_content_ngrams`); the CTA path should too — the asymmetry is the hole.

**2. CTA / hook can BE a KJV scripture span → false-BLOCK that tells the writer to alter KJV.**
`Narration.cta`/`hook` ignore block boundaries — they take the last/first sentence of `spoken_text` regardless of whether that block was a `**[... — KJV, ref]**` quote. If two shorts end on the same quoted verse (common in a one-psalm series), the gate emits `cta_repetition` with detail "Vary the closing line per artifact." That is instructing the writer to change **KJV verbatim** — a doctrinal violation per CLAUDE.md. The gate has `b.ref` available and must exclude `tagged_kjv` blocks from CTA/opener shape comparison; it doesn't.

**3. `min_share=2` on a 3-word tail → false-BLOCK on shared doctrinal language.**
Two shorts ending "...died for your sins." and "...paid for your sins." share suffix "for your sins" → BLOCKING. That's normal gospel diction, not templating. CTAs use floor 2 while openers use `max(min_share,3)`=3; the stricter floor is on the noisier signal (short closers are all common words, per the code's own comment).

## Test-suite problems (false confidence)

**4. Acceptance tests read LIVE production files and hard-assert they stay defective.**
`_real_shorts()` reads the actual `narration.md` files and `test_cta_repetition_flagged_8_of_8` asserts `len(members) == 8`. The whole point of this gate is to force the user to **de-duplicate those 8 CTAs**. The instant they do, this "passing" regression test FAILS. The fixtures must be snapshotted into the test, not pulled from the artifacts under remediation.

**5. `assert len(paths) == 8` + glob `0*/narration.md` is brittle against the planned series.**
Memory `psalm22-short-series` says ~12 shorts. Adding #09 breaks the equality assert; #10–12 are silently missed by the `0*` glob.

**6. The "does not ban gospel destination" test only proves *different tails* pass — it never tests the evasion in finding #1.** There is no test for prefix-shared CTAs, no test for a KJV-ending CTA, no test for the 2/8 doctrinal-tail false-block. The suite green-lights exactly the cases that are broken.

## Parser robustness

**7. Header dash variance is unhandled.** `_REF_IN_HEADER` and the speaker split both hard-require the em dash `—`. A hyphen or en-dash header (`**[narrator - KJV, ...]**`) yields `ref=None` and a speaker of `"narrator - kjv, psalm 22:18"`. Real files use `—` today, but there's no normalization, so one typo silently downgrades a tagged KJV span to untagged.

**8. `normalize` folds dashes/quotes but not markdown emphasis.** The long-form spoken text contains `*I*, *me*, *my*` and italic glosses. `normalize` keeps the asterisks, so tokens become `*i*` etc., poisoning n-gram matching (missed repetition / noise). Strip `*_` for fingerprinting.

**9. Silent-drop risk in the parser.** Any spoken paragraph NOT under a `**[speaker]**` header is dropped (not captured, not error — unless the file yields zero blocks). The old `_extract_spoken` keyed on `## MOVEMENT`. If any movement intro line or a header-less paragraph exists, it vanishes from verification with no warning. Fine on today's files; fragile as a contract. Consider a "loose text outside any block" warning.

**10. Minor:** `EmptyNarrationError(ValueError)` — a caller doing broad `except ValueError` swallows the fail-closed signal. `quoted_spans_with_refs` parses the file a *second* time (calls `parse_blocks` again) — wasteful but harmless.

## Verdict rationale
The parser is largely sound on the real formats and the fail-closed contract is good. But findings #1, #2, #4 hit the gate's central purpose: the CTA check is brittle to the obvious evasion, can wrongly demand edits to KJV, and the regression tests are wired to break the moment the defect is fixed. Not safe to build B/C on until the CTA detector matches the opener's n-gram approach, excludes tagged-KJV spans, and the fixtures are snapshotted.

VERDICT: REVISE
TOP FIXES:
1. Make `cta_repetition` use leading + content n-grams across the whole CTA (mirror `_content_ngrams`), not just the trailing 3-gram — otherwise varying the tail ("Come to Him, the risen Lord") evades it entirely; and EXCLUDE `tagged_kjv` blocks (use `b.ref`) from CTA/hook shape comparison so the gate never tells a writer to alter KJV verbatim.
2. Snapshot the test fixtures into the test file instead of reading live `narration.md`, and drop the `len==8`/`0*` coupling — today the regression test will fail the moment the 8 CTAs are de-duplicated (the gate's own goal).
3. Add tests for the real risk cases (prefix-shared CTAs, a KJV-verse-ending CTA, a 2-of-N shared doctrinal tail) and raise the CTA `min_share`/floor off 2; also strip markdown `*_` in `normalize` and normalize header dash variance.
