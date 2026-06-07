# Independent review — gemini (OK, 78s)

This Phase A implementation has critical flaws. It introduces a fail-open hole in KJV verification, guarantees false-positive pipeline blockages through sloppy substring matching, and uses naive text segmentation that will break on standard punctuation. 

Here are the specific, line-level findings:

**1. Fail-Open KJV Verification Bypass (Hardcoded Em-Dash)**
In `pipeline/narration_parse.py`, the parser strictly demands an em-dash (`—`):
`_REF_IN_HEADER = re.compile(r"—\s*KJV\s*,\s*(.+?)\s*$", re.IGNORECASE)`
`speaker = re.split(r"—", inner, 1)[0].strip().lower()`
Markdown writers and auto-formatters notoriously swap em-dashes (`—`), en-dashes (`–`), and standard hyphens (`-`). If an editor types `**[narrator - KJV, Psalm 22]**` (standard hyphen), the regex fails to match. `ref` becomes `None`, and the speaker is parsed as `"narrator - kjv, psalm 22"`. 
**Impact:** The block is silently treated as an untagged block. Any quotes inside it will be classed as `inline_kjv` or `rhetoric` instead of `tagged_kjv`, entirely bypassing the strict KJV verbatim gate. This is a critical fail-open vulnerability. The regex must accept `[-—–]`.

**2. Sub-Word Collision False-Blocks (Substring Bug)**
In `pipeline/cluster_gate.py`, when merging short suffixes into the CTA groups:
`if aid not in members and suf and suf in NP.normalize(cta)`
This is a raw, un-bounded substring check. If an artifact has a one-word CTA like "Go.", `suf` becomes `"go"`. The gate then checks if `"go"` is inside the normalized CTA of other artifacts. If another artifact's CTA is "Trust in God.", `"go" in "trust in god"` evaluates to `True` (because of "god"). 
**Impact:** The gate will falsely block artifacts and fail the build because short suffixes will match inside completely unrelated words. It must use token overlap (e.g., `set(suf.split()).issubset(...)`) or regex word boundaries (`\b`).

**3. Broken Sentence Segmentation (Quote Handling)**
In `pipeline/narration_parse.py`:
`_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")`
This regex breaks instantly if a sentence ends with a quotation mark or parenthesis. For example: `"It is finished." Then he died.` The character before the space is `"`, not `.!?`, so the lookbehind fails. 
**Impact:** The parser will merge multiple sentences together. Because `hook` and `cta` are defined as the first and last "sentences", failing to split them means you will ingest massive, multi-sentence paragraphs into the n-gram generator, diluting the suffix logic and creating unpredictable gate behavior.

**4. Naive 2-Grams Guarantee Alert Fatigue**
In `pipeline/cluster_gate.py`:
`_content_ngrams(text, lo=2, hi=3)`
The logic allows 2-grams and only discards them if *all* words are stopwords (`all(w in _STOP for w in words)`). This means "of god", "the cross", "in jesus", and "he wept" are all treated as valid `content_ngrams`. 
**Impact:** The `opener_floor` is set to 3. If any three narrations in a series happen to use the phrase "of god" in their opening sentence, the entire cluster will be hard-blocked for `opener_repetition`. This is unworkable for a religious corpus with a narrow vocabulary. 2-grams are too short; it needs to be constrained to 3-grams minimum or require at least two non-stopwords per gram.

VERDICT: FAIL
TOP FIXES:
1. Fix the `_REF_IN_HEADER` and `re.split` logic in `narration_parse.py` to accept all hyphen/dash variants (`[-—–]`) so KJV tags aren't silently dropped.
2. Replace the unbounded `suf in NP.normalize(cta)` substring check in `cluster_gate.py` with an exact token-sequence check or word-boundary regex to prevent sub-word false positives.
3. Update `_SENT_SPLIT` to handle trailing punctuation (e.g., `(?<=[.!?]['"”’\)]?)\s+`) so quoted sentences aren't merged.
