# Independent review — grok (OK, 100s)

**Critical review of PIPELINE_HARDENING_PLAN.md (v2)**

The plan correctly sequences "prove the cheap cluster catch first" and lists the v1 panel findings at the top. Several specific fixes from the REVISE (extractor fail-closed contract, Rule-8 scoped to short-only, ledger as post-gen flagging only, Fix 5 deferred, sentence-level not heavy Jaccard, NT verse vs own tagged ref, no five-beat coercion on hand-authored) are written into the text. That is real progress on paper.

It is still not safe to implement.

**v1 convergent findings — not all are genuinely closed in v2**

- "if a narration yields **zero** spoken blocks, the parser raises — callers must ABORT, never silently pass" (A1). The library contract is fail-closed. The workflow is not. C2 still says "Identify the single lock chokepoint (or add one) so future locks append reliably — today `_finalize.py` only renders audio and `handoff.py` only covers engine-generated content; hand-authored folders touch neither." The original defect (the 8 Psalm 22 shorts) was hand-authored. Until the chokepoint is designed and the 8 files are proven to be forced through it, the fail-closed parser does not close the shipped failure mode.

- Witnessed KJV canon with no bible-api fallback is stated (B3: "bible-api is NOT a fallback for lock eligibility", "unverified" text "cannot satisfy a lock", "0 FAIL and 0 unverified to be LOCK-eligible"). B2's construction ("download a known-good structured dataset — do not scrape-and-parse raw text", "Cross-verify per-verse against ≥2 independent public-domain KJV sources; require agreement, **especially punctuation**; route every disagreement to **human adjudication**", "full-Bible canon") remains an unproven, high-human-cost assumption. No actual source is named. No scope reduction to the verses actually used in the 10 artifacts is described. A single-comma bug plus one authoring elision is being answered with a full-Bible punctuation-exact reconciliation project.

- Standing-gate wiring is described as "Wire `cluster_review.py` into the shorts/long-form lock workflow and note it in `RESUME.md` as a required gate before a series/cluster is called done" (A4). "Note in RESUME.md" is the same class of control that already failed ("no one ran a set-level check"). The plan itself documents that hand-authored content has no chokepoint today. Documentation + a standalone harness repeats the org failure.

- Backfill and ledger append are required ("Backfill the 8 shorts + 2 long-forms now"), but the mechanism is deferred to the same unidentified chokepoint. The regression test (C3) is defined; the production path that would have prevented the 9th synthetic short is not.

- "Consolidate deterministic quote logic into `kjv_check`/a single module — do not create a parallel `quote_rules.py`" shows it listened to one reviewer. The rest of the infrastructure assumptions are not similarly grounded.

**New or still-latent problems introduced or exposed by v2**

- Assumed but undocumented infrastructure. C2 says "Add defect classes `cluster-repetition`, `catalogue-phrase-reuse` to `defect_classes.json`. **Confirm the `panel_misses` writer exists** (the calibration ledger currently has no identified writer — if absent, `learning.py` tracking is inert until one is added)." The session context file map (data/constitution.md, data/series.json, data/structures.json, data/kjv_cache.json, pipeline/*, independent_review.py) lists none of these. If `defect_classes.json`, `learning.py`, or a panel_misses writer do not exist here, this is not a confirmation step; it is new architecture the plan treats as minor.

- No catalogue discovery mechanism. A2 requires across-catalogue checking ("~76 catalog shorts + ~12–21 long-forms", "cross-series migration of a closer is the next failure"). The plan never states how `cluster_review.py` (or the LENS_CLUSTER call) will find prior artifacts. If the operator must supply 76 explicit paths every time, the gate will be skipped under the same time pressure that shipped the Psalm 22 set.

- Parser contract vs real content brittleness. A1 must parse both `## MOVEMENT` long-form and `**[narrator — KJV, <ref>]**` short blocks, strip multiple section types, and produce reliable quote-to-ref maps for B4. The unit test only requires "non-empty spoken text" on the 8+2. It does not require that every KJV quote in those real files is successfully ref-mapped. Unmappable spans become "flagged for human check". The 8 shorts that exposed the original defect are the corpus; any header formatting variance (em-dash, spacing, "KJV," vs "KJV ,", prose attribution instead of block tag) will either raise or generate manual work on every future narration.

- Full-catalogue LLM context risk. "Spoken-only keeps it within CLI context limits." 76 shorts is roughly 12k words of spoken text before the analysis prompt. The plan does not define when or how the LENS_CLUSTER LLM layer is actually invoked on a growing catalogue (every new short? only on deterministic hits? sampled?). Local CLIs used for the panel have their own limits.

- Disproportionate scope on the canon vs the actual defect. B1 ("Fresh audit of what's ACTUALLY still corrupt") is the right first step. The build target is still a full-Bible witnessed `data/kjv_1769.json`. A targeted witness store of only the verses that have actually appeared in shipped narrations, with the same fail-closed rule, would address Ps 22:7 and future authoring elisions at far lower ongoing cost and risk. The "ref missing from a full-Bible canon means the canon build is broken" rule creates a permanent new lock blocker for any new verse.

- Token and process cost realism is only partially addressed. The plan correctly says deterministic layers are $0 and flags that re-verifying 10 artifacts via agent-bridge/Opus or local CLIs is time. It does not surface the human curation hours required for the canon (reconciliation of every punctuation difference + printed-Bible spot checks + future extensions) or the recurring operational load of running set-level cluster review + verify harness + re-panel on every new short or cluster. For the scale of the actual miss (8 templated CTAs), the verification platform is heavy.

- The A3 acceptance test is correctly positioned as the gate for the whole effort ("If A2 fails this, stop and fix A2 before building anything else"). The document still presents the entire B/C/D tower for review before that gate has been built and passed on the real files. The test itself requires the 8 Psalm 22 .md files to be locatable from the test in this repo; the plan does not state whether those sources live here, in the sibling PythonProject1 tree, or must be copied.

**Feasibility, reuse, and over-engineering**

The plan avoids duplicating the downstream audio and Kling pipelines (explicitly listed under "What this plan deliberately does NOT do"). It reuses independent_review.py for the LLM layer and extends kjv_check rather than forking. That is correct.

It still adds: `pipeline/narration_parse.py`, `cluster_review.py`, `verify_narration.py`, `phrase_ledger.py`, `_audit_kjv_cache.py`, `data/kjv_1769.json`, `data/learning/phrase_ledger.jsonl`, new defect classes, new LENS_CLUSTER, standing-gate wiring, RESUME.md updates, and a full witnessed canon. This is a verification platform, not a minimal targeted fix for "no one ever looked at the 8 together and the source was trusted blindly."

The core cheap win (sentence/clause-level exact + normalized cluster detection + the Psalm 22 fixture + regression synthetic) could have been extracted, proven on the real 8 files, wired into whatever handoff already exists for engine content, and then used to decide whether the rest of the tower is worth the process weight. The plan does the opposite: it makes the cheap win Phase A but still asks for approval of the full design.

**Summary of concrete risks if implemented as written**

- The hand-authored path that produced the defect still has no forced chokepoint; "identify or add one" during build leaves the highest-risk case open.
- The catalogue check will be operationally painful or skipped without a discovery/registry design.
- The KJV work is scoped to a full-Bible punctuation reconciliation that is not justified by the one-comma + authoring-elision evidence.
- Supporting machinery (`defect_classes.json`, `learning.py`, panel_misses writer, lock chokepoint) is assumed rather than shown to exist.
- Parser and ref-mapping success on the actual 8 files is not part of the A1 acceptance criteria.
- Enforcement remains partly documentary ("note in RESUME.md").

v2 is a disciplined response to the panel feedback on v1. It is not yet a plan that can be executed without re-introducing the same class of "individually fine, collectively cheesy, source trusted blindly" failure on the next cluster.

VERDICT: REVISE
TOP FIXES:
1. Define the concrete, non-bypassable lock chokepoint (specific CLI step, handoff change, or new lock command) that hand-authored narrations must pass, prove the 8 Psalm 22 sources flow through it, and make ledger append and cluster/verify gates happen there before any other code is written.
2. Reduce B2 canon scope from full-Bible witnessed structured dataset with multi-source punctuation adjudication to a minimal witnessed-verses store containing only verses actually used in shipped narrations (with the same fail-closed unverified rule and the same B1 audit + human spot-check on the real divergences).
3. Specify exact invocation, discovery mechanism (manifest, series index, explicit list file, etc.), and scope policy for cluster_review.py + LENS_CLUSTER (within-series + how many prior catalogue items), plus the required changes to independent_review.py output layout for --type cluster; make the A3 acceptance test runnable without manual path collection.
