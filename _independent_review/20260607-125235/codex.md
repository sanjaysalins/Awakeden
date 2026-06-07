# Independent review — codex (OK, 175s)

**Findings**

1. A4 still does not define a hard standing gate. The phrase “Wire `cluster_review.py` into the shorts/long-form lock workflow and note it in `RESUME.md`” (line 62) is too vague, and C2 punts with “Identify the single lock chokepoint (or add one)” (line 107). In the real repo, `_finalize.py` only renders audio, `handoff.py` only writes generated narration folders, and hand-authored long/short folders bypass both. A `RESUME.md` note is not enforcement.

2. The extractor fix is only partially resolved. A1 creates `pipeline/narration_parse.py` (line 38), but it does not say to retire or rewire `veed_io/_extract_spoken.py`, which is still CLI-only and `## MOVEMENT`-only. Since the plan later requires caption/timing revalidation, this leaves two spoken-text sources that can diverge.

3. The “thousand years hooks” acceptance test is under-specified and likely false as written. A2 says hook = “first spoken sentence” and opener n-gram = “first ~6 tokens” (line 47), but the real shorts vary: some have “thousand years” mid-sentence, some say “a thousand years apart,” some say “before Rome ever raised a cross.” Line 59’s test may pass the CTA catch while missing the hook-family defect.

4. `LENS_CLUSTER` / `--type cluster` is not a concrete reuse plan. Line 52 says to reuse `independent_review.py` with a new cluster type, but the current tool accepts one file and only `--type narration|plan`. The plan needs an input contract, manifest format, combined prompt format, and non-zero exit behavior.

5. B4’s quote-to-ref model does not handle the real long-form shape cleanly. It says each quote is checked against “its own tagged verse” (line 85), but real tags include ranges like `Psalm 22:6-7`, `Isaiah 53:2-3`, and `Isaiah 53:10-11`. The plan must specify range handling, verse-boundary joins, and multiple quoted spans inside one tagged block.

6. The KJV canon step remains a large single point of failure. B2 says “download a known-good structured dataset” and cross-verify against “≥2 independent” sources with “human adjudication” (lines 74-75), but names no dataset, source pair, conflict threshold, adjudication record format, or time budget. This is not yet implementable at the claimed precision level.

7. The whitelist is dangerous. A2 says the whitelist includes `"Come to Him" as a concept` (line 50), while the primary defect is repeated “Come to Him.” Unless exact wording checks always run before concept-whitelisting, the whitelist can suppress the defect it exists to catch.

8. C2 acknowledges the calibration writer may not exist but does not schedule fixing it. “Confirm the `panel_misses` writer exists… if absent, `learning.py` tracking is inert” (line 108) is not enough. The repo has `learning.append_record`, but the actual ledger appears manually maintained.

**Resolved From V1**

Genuinely resolved in v2: no five-beat coercion for hand-authored content, Rule-8 short-only, NT quotes checked against their own NT refs, ledger as post-generation flagging, and Fix 5 deferral for engine-generated content. Partially resolved: extractor fail-closed, witnessed KJV/no API fallback, cluster semantic detection, standing-gate wiring/backfill, and regression coverage.

Not safe to implement as-is. The core direction is sound, but the plan still lacks hard workflow integration and exact parser/KJV/cluster contracts.

VERDICT: REVISE
TOP FIXES:
1. Define one fail-closed lock command/chokepoint that runs C1 + A2 + ledger append for generated, hand-authored, short, and long-form paths.
2. Replace or rewire all spoken-text extraction paths to one shared parser, including `veed_io` caption/timing users.
3. Specify cluster/KJV contracts precisely: opening-window detection, `independent_review --type cluster` input/exit behavior, range-ref quote checks, and canon source/adjudication rules.
