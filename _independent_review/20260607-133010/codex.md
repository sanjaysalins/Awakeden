# Independent review — codex (OK, 159s)

**Findings**

1. **The new gate is not integrated anywhere.** `cluster_check` is only referenced by [pipeline/test_cluster_gate.py](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/test_cluster_gate.py:44) and review docs. Production flow in [pipeline/runner.py](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/runner.py:115) writes one narration at a time and never calls `cluster_gate`. This means the exact cross-artifact failure can still ship unless someone manually runs the test/module.

2. **The “replaces `veed_io/_extract_spoken.py`” claim is false in the real codebase.** [pipeline/narration_parse.py](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/narration_parse.py:16) says it replaces the old extractor, but the live caption path is still [veed_io/caption.py](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/veed_io/caption.py:42). That parser strips headings/markup and keeps ledger prose; it is not fail-closed and is not unified with verification.

3. **CTA repetition detection is trivially bypassed by punctuation or one added word.** `normalize()` does not strip punctuation ([narration_parse.py:155](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/narration_parse.py:155)), and `_cta_suffix()` only compares the last 3 whitespace tokens ([cluster_gate.py:75](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/cluster_gate.py:75)). `Come to Him.`, `Come to Him!`, `Come to Him today.`, and `Come to Him now.` become different suffixes. That is a core false-pass hole.

4. **The code says “Last spoken sentence/clause” but only extracts the last sentence.** [narration_parse.py:63](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/narration_parse.py:63) documents clause extraction, but [narration_parse.py:167](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/narration_parse.py:167) only splits on sentence punctuation. Repeated CTA wording inside the final sentence, but not at the final 3 words, can pass.

5. **Tagged KJV headers only support em dash.** `_REF_IN_HEADER` requires `— KJV,` ([narration_parse.py:34](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/narration_parse.py:34)) and `_parse_header()` splits only on `—` ([narration_parse.py:75](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/narration_parse.py:75)). `**[narrator - KJV, John 3:16]**` or en dash variants lose `ref`, downgrading KJV verification.

6. **KJV blocks without quotation marks are silently ignored by quote extraction.** `quoted_spans_with_refs()` only returns `_QUOTE.findall(b.text)` ([narration_parse.py:141](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/narration_parse.py:141)). But a `**[speaker — KJV, ref]**` block is itself a KJV claim. If the line lacks double quotes, Phase B would see no span.

7. **Empty cluster input passes.** `cluster_check([])` has no input validation; it returns an empty `ClusterReport`, and `passed` is true via [cluster_gate.py:54](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/cluster_gate.py:54). A bad glob or manifest bug becomes a false pass.

8. **“Density” is implemented as absolute count.** `min_share=2` ([cluster_gate.py:85](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/cluster_gate.py:85)) means 2 repeated CTAs in a 50-short catalogue block the cluster. That is not density and creates avoidable false-blocks.

9. **Opener repetition is noisy and overbroad.** `_content_ngrams()` keeps any n-gram with at least one non-stopword ([cluster_gate.py:69](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/cluster_gate.py:69)), despite the comment saying stopwords are kept out. Then every bigram/trigram anywhere in the first sentence is counted ([cluster_gate.py:127](/C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/cluster_gate.py:127)). Three legitimate hooks sharing “the cross” or “Jesus said” can block.

10. **Test coverage is too fixture-shaped.** The 7 tests prove the Psalm 22 fixture is caught, but there are no tests for punctuation variants, adverb variants, hyphen/en dash headers, inline speaker headers, unquoted KJV blocks, empty manifests, duplicate artifact IDs, large-cluster false blocks, or integration with the actual runner/caption path.

VERDICT: FAIL
TOP FIXES:
1. Wire `cluster_check` into a real non-bypassable pre-lock/pre-audio path and fail closed on empty or malformed cluster input.
2. Replace suffix-only CTA matching with punctuation-stripped, word-boundary phrase/fuzzy matching over the CTA clause, not just the last 3 tokens.
3. Harden `narration_parse`: support dash variants/inline headers, treat tagged KJV blocks as KJV even without quotes, and add regression tests for those formats.
