# Independent review — claude (OK, 218s)

Verification done. I checked the plan's factual claims against the repo: the referenced files (`BATCH_PLAN.md`, `batches/batch_manifest.json`, `asset_index.json`, `narration_gate.py`, `_website/build_catalog.py`, `v2/_independent_review/20260703-135242`) all exist, the ~14-short Cross sizing matches BATCH_PLAN, and `/upload` + `/publish` are real skills. But three claims don't survive contact with the code, and the runway rule contradicts the schedule it sits next to.

## Findings

**1. The runway rule is violated by the plan's own Phase 1 schedule (§5 vs §10, HIGH).**
§5 says ≥9 shorts banked "BEFORE launch **and at all times after**" (hard rule). Do the arithmetic on Phase 1: launch with ~14 banked (8 + ~6 new Cross shorts), publish 3/week, and spend weeks 1–3 building the **Jonah long, not shorts** (step 7). Bank: week 1 → 11, week 2 → 8 (**rule broken**), week 3 → 5. The Resurrection shorts (step 9) can't start until the Jonah long is written, so the bank keeps draining into month 2. The plan fixed the *launch-day* runway (panel round 1) but the "at all times after" invariant has no sustaining production rate behind it — nowhere does the plan state the required build throughput (3 shorts/week + 1 long/month, solo, indefinitely) or evidence that cluster 1's actual build pace supports it. Either weaken the rule to launch-only, or schedule short-building alongside the Jonah long.

**2. "feeds the C0 gate weights" is fictional wiring (§5, §10 step 11).**
`narration_gate.py` contains no weights, no learning input, no reference to `yt_analytics.jsonl` — it's a deterministic pattern gate (stock-closer / template-hook regexes). I grepped it: zero hits for weight/learning/analytics. Logging analytics to a JSONL is fine; claiming it "feeds the C0 gate weights" names a mechanism that does not exist and no step builds it. Say "informs manual C0 rule updates" or add the actual build step.

**3. The Read-page generator's input doesn't cover the pilot (§7).**
`livingpage_short.spec.json` exists in **7** cluster-1 pieces — verified. But the plan banks **8** pieces (§3), and the 8th, `father_forgive_them` (the pilot), has only `mocomic.spec.json` / `mocomic_v2.spec.json` — a different, older schema. So `build_readpage.py` as specified skips or breaks on 1 of 8 launch pieces. The §12 "answered" note ("exists in all 7 pieces") quietly papers over that 7 ≠ 8. Needs either a spec migration for the pilot or a stated exclusion.

**4. The hook A/B design is methodologically invalid as written (§5).**
"Publish the loser lane on TikTok only; compare 3-second retention" compares variant A on YouTube against variant B on TikTok — different platforms, different audiences, different swipe mechanics. That's not an A/B; it's two uncontrolled observations. Also uncosted: a different first-3s hook means re-voiced audio (metered ElevenLabs) + re-timed panels + re-assembly per variant — not "cut two hook variants" as a throwaway. Either run both variants on the same platform (TikTok allows near-duplicates; YouTube may flag them) or drop the A/B claim and just track hook archetypes observationally.

**5. Cost-ledger denominator inconsistency (§3).**
The plan says "cluster-1 ledger: ~$31/**6** pieces" (~$5.20/short); the cluster-1 roll memory records ~$31 for the **8**-piece roll (~$3.90/short). Small, but this number gates the "cheapest runway" reasoning in §4/§10 — pin the real denominator from the ledger before budgeting cluster 2.

**6. Minor.** (a) §10 Phase 3 restarts numbering at 10, duplicating Phase 2's steps 10–11 — makes the phases un-referenceable. (b) §11 risks omit the actual single point of failure: one solo operator's one Windows machine holds every asset, spec, and the venv (the polite-CPU memory even notes state is lost if the venv is rebuilt) — no backup/off-machine copy step anywhere, which matters more than "platform risk" for a publishing engine. (c) Email capture (§7) names no provider and no privacy note — small, but it's on the launch path.

**What's sound:** the mission/positioning framing, the tracker-before-Read-pages ordering, gating publication through the existing `/upload`+`/publish` machinery instead of hand-written descriptions, the honest CSS-re-render scoping, the reuse-order cluster sequencing (matches BATCH_PLAN), and the plan's own insistence on a round-2 quorum panel before LOCK. The build-remaining-Cross-shorts-first move is genuinely the cheapest runway available.

VERDICT: REVISE
TOP FIXES:
1. Reconcile §5's "≥9 banked at all times" with Phase 1: either schedule continued short production during weeks 1–3 (state the required build rate and that it's achievable solo) or downgrade the rule to a launch-gate only — as written the plan breaks its own hard rule in week 2.
2. Fix the fictional analytics→gate wiring: `narration_gate.py` has no weights; either add a real step to build that mechanism or restate as "manual C0 rule review from yt_analytics.jsonl".
3. Close the pilot spec gap: `father_forgive_them` has `mocomic*.spec.json`, not `livingpage_short.spec.json`, so the Read-page generator misses 1 of 8 launch pieces — migrate its spec or state the exclusion; and fix the invalid cross-platform hook A/B (same-platform variants or drop the A/B claim).
