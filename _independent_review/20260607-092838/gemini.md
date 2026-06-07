# Independent review — gemini (OK, 42s)

Here is the independent critique of the `PIPELINE_HARDENING_PLAN.md` artifact.

### Critique

**1. Feasibility & Hidden Risks: The "Perfect" KJV Source Assumption**
*   **Claim:** *"build it with a one-time `pipeline/_build_kjv_canon.py` that pulls a vetted public-domain 1769 KJV... verify integrity (66 books / 31,102 verses / checksum)"*
*   **Finding:** This assumes a perfectly formatted, structured, punctuation-exact 1769 KJV JSON/API is just sitting out there ready to be cleanly pulled. Parsing historical Bible texts from raw sources (like Project Gutenberg or open-source SQL dumps) is notoriously messy (italics for added words, paragraph markers, varying book names). If you write a script to scrape and parse it, *your script will introduce new corruptions*. You should manually download and vet a known-good JSON dataset rather than trusting a one-time build script to magically perfect it.
*   **Claim:** *"fall back to bible-api only when the canon lacks a ref"*
*   **Finding:** This is a logical contradiction and a hidden single point of failure. If your offline canon is the "full Bible," it will never legitimately lack a reference. If it does lack a reference, your canon build is broken. Falling back to the known-corrupt `bible-api.com` (which dropped the comma and elided Acts 8:35) instantly circumvents the entire point of Fix 1. **Fail closed means no fallback.**

**2. Over-engineering: Shingling & Jaccard Math**
*   **Claim:** *"compute pairwise similarity (normalized-exact + token-Jaccard / shingling); flag any hook / CTA..."*
*   **Finding:** This is severe over-engineering for comparing 8 to 20 shorts. Computing Jaccard distances on 10-word CTAs will yield a mess of false positives ("Come to Jesus" vs "Run to Jesus") and miss structural repetitions. You are already passing the entire set to an LLM (`LENS_CLUSTER`). The LLM is vastly superior at detecting "tired/templated" phrasing than a token-shingling algorithm. Drop the deterministic math for semantic text comparisons.

**3. Anti-Pattern: Negative Prompting at Scale**
*   **Claim (Fix 4):** *"engine._episode_block / generate_candidates are fed 'ALREADY-USED hooks/CTAs across the catalogue — diverge from these'"*
*   **Finding:** Feeding an ever-growing ledger of "banned" phrases into an LLM generation prompt is a documented anti-pattern. LLMs struggle severely with extensive negative constraints (the "don't think of an elephant" problem). As your ledger grows to 76 shorts, feeding a wall of 76 banned CTAs will cause the model to hallucinate, hyper-fixate on the banned words, or generate bizarre, unnatural English just to mathematically avoid the list. The ledger should be used strictly for *post-generation review/flagging*, never injected into the generation prompt.

**4. Context / API Bridge Limitations**
*   **Claim:** *"LLM layer (reuse independent_review.py... Local CLIs, no metered API) pass all narrations together"*
*   **Finding:** The `independent_review.py` script appears to orchestrate 5 distinct CLI models (Claude, Gemini, Grok, etc., per the directory structure). These are likely web-automation bridges, not true local models. Trying to pass "all narrations together" (a whole series cluster) into context windows via unmetered CLI scraper-bridges will almost certainly trigger rate limits, context-length truncation, or catastrophic bridge timeouts. Relying on this for a standing programmatic gate is highly brittle.

**5. Missing Edge Case: Cross-Reference Text Variance**
*   **Claim:** *"verify every quoted span against the full-Bible canon... including NT cross-refs"*
*   **Finding:** The New Testament frequently quotes the Septuagint (LXX), not the Masoretic Text (which the KJV OT translates). Therefore, an NT quote of an OT verse *will not match* the KJV OT text verbatim. If your `kjv_check` rigidly verifies "quotes against the canon", you must explicitly clarify whether you are verifying the text against the *local chapter being narrated* or the *historical reference*. A naive verbatim check here will create endless false failures.

VERDICT: REVISE
TOP FIXES:
1. Remove the `bible-api.com` fallback in Fix 1 entirely. If the offline canon is the source of truth, it must be the *only* source; otherwise, corruptions will silently pass.
2. Remove the Fix 4 generation constraint. Do not feed an ever-growing list of "banned phrases" into the LLM prompt. Use the ledger exclusively for post-generation flagging/detection.
3. Drop the token-Jaccard/shingling math from Fix 3. It is premature optimization; rely on the LLM cluster review to identify thematic repetition.
