# Independent review — codex (OK, 227s)

**Findings**

1. **The lock is not actually “non-bypassable.”** The plan says “one non-bypassable lock step gates everything,” then concedes “Direct invocation of the foreign script is a documented, discouraged bypass.” That is a contradiction, not a minor caveat. `per_turn_synth.py` currently skips its gate when no `episode.manifest.json` exists, and the Psalm 22 folders lack that manifest. Also `cli_assemble.py` and `pipeline.orchestrator` proceed from an existing `narration.mp3`; `assembly_align` reuses `narration.alignment.json`. A stale MP3/alignment/cut can survive a narration edit unless assembly also validates the lock hash.

2. **The KJV corpus port has a marker trap in the exact Ps 22:7 case.** The plan says “strip only the corpus’s `{…}` markers,” but the HF corpus text is shaped like `shake the head, {saying}, {shoot...: Heb. open}`. `{saying}` is supplied KJV text that must be preserved as `saying`; `{shoot...: Heb. open}` is a note that must be removed. If the strict mode removes all brace groups, it will fail or distort the very comma case this plan is meant to fix.

3. **Quote policy is internally inconsistent.** A1 says untagged inline quotes are “resolved via ... best-effort ref lookup, NOT failed,” but B3 says “Unwitnessed/unmappable ref → BLOCK lock.” Existing Psalm files include spoken non-scripture/rhetorical quoted spans such as `"that the scripture might be fulfilled"` and landing echoes like `"Let him deliver him,"`. The plan needs an explicit quote classifier: tagged KJV blocks, spoken KJV inline echoes, narrator rhetoric, and non-spoken ledger quotes must not all go through the same blocking path.

4. **The registry design conflicts with itself.** A2 says “rebuild the registry from on-disk `.locked` folders at check time,” while C2 says “`cli_lock.py` is the single append point.” Rebuild-from-disk makes append semantics at best a cache write, not the authority. More importantly, a new batch of 8 rewritten shorts could pass one-by-one against only previously locked folders unless the in-flight set is included atomically.

5. **CTA/opener checks are still overfit to this failure.** The phrases “`come to him` matches...” and “`thousand years` + similar stems” catch this cluster, but not equivalent template families: “come unto me,” “bring you home,” “that’s Jesus,” “the door is open,” “reach Him,” etc. The plan needs a general normalized n-gram/fuzzy suffix/opening-family check, with the named Psalm 22 phrases as regression fixtures, not the detection strategy.

6. **The “blocking LLM backstop” is underspecified against the real tool.** The plan says `independent_review.py --type cluster` with blocking verdict and provider-failure tolerance, but the current CLI only accepts `--type narration|plan`. There is no cluster lens, no manifest contract, no verdict aggregation rule, and no fail-closed behavior if fewer than 3 usable reviewers return.

7. **Porting is duplication unless treated as vendoring.** The phrase “Do NOT edit the sibling-repo `short_gate` ... Port the proven logic” does not avoid duplication; it creates a fork. That can be acceptable, but only with provenance, upstream parity tests, and explicit local ownership. Otherwise future fixes to `short_gate` and this repo will diverge silently.

8. **The `.locked` hash must bind the rendered text, not just parsed raw markdown.** The plan says the hash is “A1-parsed spoken text,” but synth and assembly consume `narration-tagged.md` / `<speaker>` chunks. If `narration.md` passes but `narration-tagged.md` is stale or hand-edited, the lock can certify text that is not what gets rendered.

Conceptually, punctuation-strict KJV plus blocking cluster CTA/opener checks addresses the two root causes. As written, the plan is not safe to implement because the lock boundary, corpus normalization, and quote classification are not tight enough.

VERDICT: REVISE
TOP FIXES:
1. Define and enforce a single lock contract across audio, caption, assembly, alignment caches, and existing media reuse; stop calling it non-bypassable while direct synth remains possible.
2. Specify KJV corpus marker normalization with tests for `{saying}` vs `{note: ...}` and make Ps 22:7 a hard regression.
3. Replace best-effort quote handling with explicit spoken quote classification and a witness/manifest schema.
