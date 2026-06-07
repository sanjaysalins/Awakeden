# Independent review — cursor (OK, 84s)

## Independent adversarial review

The plan correctly diagnoses the **Psalm 22 cluster templating miss** (per-artifact review, no set-level gate) and the **hand-authored bypass** of `engine.review`. Several fixes are directionally right but the design has feasibility holes, misattributed root causes, and missing wiring that would let the same class of failure recur.

---

### Feasibility against the real codebase

**Fix 2 assumes a spoken extractor that does not work on shorts.**

The plan says to reuse `veed_io/_extract_spoken.py` and “generalize if needed” (Fix 2, line 52). That script only keeps text inside `## MOVEMENT` sections:

```1:8:veed_io/_extract_spoken.py
"""Extract ONLY the spoken narration from a long-form narration.md.

Keeps prose **only while inside a `## MOVEMENT ...` section** — so the trailing
non-spoken sections (`## DEPTH & SOURCING`, `## VOICE PLAN`, doctrine ledgers)
```

Shorts use `**[narrator]**` blocks, not `## MOVEMENT`. Without a specified short-format extractor, Fix 2’s Rule-8 quote count, anchor-verse check, and KJV span audit cannot run on the 8 Psalm 22 shorts — the plan’s own acceptance tests.

**Fix 2’s `engine.review` reuse is underspecified and likely brittle.**

`engine.review` requires `Series`, `Episode`, `Structure`, optional `Thread`, `passage`, and a `Draft` with gospel-five-beat IDs (`pipeline/engine.py:729-756`). Hand-authored shorts have none of that: no `narration.creation.json`, rich markdown with voice tags, and **no entries in `data/series.json`** for 7 of the 8 Psalm 22 shorts (only one generic `"The Crucifixion Foretold"` exists, with `primary_ref: "Psalm 22:16"` while short #1 actually anchors on **22:18**). The optional `[--refs "..."]` flag is a manual escape hatch, not a scalable design for ~76 catalog shorts.

**Fix 1’s KJV canon extension still misses the Acts 8:35 failure mode.**

The plan attributes Acts 8:35 to corrupt cache (“elided Acts 8:35”, Context line 15). The cache already holds the full verse:

```44:44:data/kjv_cache.json
  "Acts 8:35": "Then Philip opened his mouth, and began at the same scripture, and preached unto him Jesus.",
```

The real failure was **interior word elision inside a quoted span** (“Then Philip… began” dropping “opened his mouth, and”), which `kjv_check` never checks today because it only substring-matches against the primary pericope and ignores low-overlap spans:

```13:16:pipeline/kjv_check.py
  - low overlap                                                -> ignored (paraphrase, or a cross-ref
                                                                  quote not in the primary pericope —
                                                                  we can't verify those here, so we
                                                                  do NOT false-flag them)
```

Fix 1’s “compare the whole span’s punctuation, not only the terminal char” (Fix 1, line 40) does not address **interior omission**. A full-Bible canon alone does not fix this unless quotes are mapped to refs and compared as contiguous substrings of the canon verse — which the plan never specifies (no parsing of `**[narrator — KJV, Psalm 22:18]**` tags).

**Ps 22:7 comma example is valid but the plan conflates two different bugs.**

Cache has `"they shake the head saying,"` (no comma after “head”); authoritative KJV requires `"they shake the head, saying,"`. That supports Fix 1. But the plan lists Ps 22:7 and Acts 8:35 as the same class (“corrupt source-of-truth passes deterministic check”) when Acts was an **authoring/elision** bug, not cache corruption.

**Fix 3 long-form “movements” path is undefined.**

Fix 3 says long-form uses “the same engine across its movements (intra-document repetition)” (line 66), but the CLI design extracts hook/CTA **per narration file**. A long-form is one file with seven movements. No algorithm is given for intra-document repetition (movement-level hooks? sliding windows? landing vs movement closers?).

**Fix 4 `append(record)` on lock has no caller for hand-authored content.**

Phrase ledger append is specified (Fix 4, line 77) but hand-authored long-form/shorts never pass through `pipeline/handoff.py`’s engine lock path. Without mandatory wiring in the long-form funnel or a manual backfill step, the ledger stays empty for the content that actually caused the problem.

---

### Hidden risks and false assumptions

**“No metered API” is conditional and batch-hostile.**

Cost section (line 121): “LLM layers run via the agent-bridge (engine) and local CLIs (panel) — no metered API.” Default is `LLM_PROVIDER=agent`, but `agent_bridge` **blocks polling for an in-chat agent** to write each response file — it is not unattended batch automation. Re-verifying 10 narrations through `engine.review` + `independent_review.py` is either heavy human babysitting or real Opus spend if `LLM_PROVIDER=api`. The plan quotes $0–$3 for audio only and hides review cost.

**Fix 3 LLM cluster review will hit context/timeout limits.**

`independent_review.py` accepts a **single file** (`artifact` arg, line 157), embeds the full artifact in one prompt, and uses 300s timeouts. Eight full `narration.md` files plus DEPTH sections could exceed practical limits for grok/codex; the plan does not say to strip to spoken-only for cluster review (even though Fix 2 needs that extractor).

**Fix 3 deterministic Jaccard layer risks false positives without policy.**

“Flag any hook / CTA / opener / bridge that repeats or is near-duplicate” (line 64) has no allowance for **intentional series DNA** (e.g. all Awakeden shorts may share CTA-to-Jesus *structure* but must diverge *wording*). Without thresholds, whitelist, or “same series vs catalogue” scopes, you will flag legitimate gospel invitations or create alert fatigue. Fix 4’s `scope="series"|"catalogue"` is not wired into Fix 3’s deterministic flags.

**Fix 4 feeding the ledger into generation is a known anti-pattern at scale.**

“(a) `engine._episode_block` / `generate_candidates` are fed ‘ALREADY-USED hooks/CTAs across the catalogue — diverge from these’” (line 78). At ~76+ shorts × multi-dimension, this becomes a large negative-constraint wall. LLMs fixate on banned phrases and produce unnatural divergences. The plan should restrict ledger use to **post-generation flagging** unless prompt budget and format are specified.

**Fix 5 “conviction-strength” has no calibration or false-positive control.**

Subjective positive scoring (“holy tension (Heb 4:12)”, Fix 5 line 87) with acceptance test “confirm a flat conviction line is scored low” (line 120) is not reproducible. G8 already partially covers piercing (“conviction beat actually PIERCES”, `engine.py:679`). Adding Fix 5 before proving Fix 3 catches the cluster miss is premature.

**Fail-closed canon vs existing graceful degradation conflict.**

Fix 1: “if canon is missing, verification cannot pass silently” vs `scripture.fetch_kjv` today returning `None` on network failure and letting the engine continue (`scripture.py:59-60`). Migrating without a rollout plan breaks existing runs until `data/kjv_1769.json` exists and every caller is updated.

---

### Over-engineering / build-before-proof

**Five fixes bundled before the cluster acceptance test is proven.**

The plan’s own acceptance test is Fix 3 on 8 shorts (line 118). That requires only: (1) a short-format spoken extractor, (2) hook/CTA extraction, (3) exact/near-duplicate detection OR cluster LLM lens. Fix 1 full-Bible canon (~31k verses), Fix 4 generation-time ledger injection, and Fix 5 conviction dimension are not prerequisites to catching “8/8 Come to Him.” Building all five before validating Fix 3 violates the plan’s own dependency story and increases scope risk.

**Fix 3 deterministic + LLM duplicate work.**

Deterministic Jaccard/shingling (line 64) plus `LENS_CLUSTER` LLM panel (line 65) overlap heavily for 8–20 artifacts. The deterministic layer adds maintenance (threshold tuning, normalization edge cases) with limited upside over a spoken-only cluster prompt — especially when the failure mode is **exact** repetition (“Come to Him” ×8), which is a trivial exact-match check, not Jaccard.

---

### Missing steps, edge cases, verification gaps

**No production integration.**

New CLIs (`verify_narration.py`, `cluster_review.py`) are standalone. Nothing mandates them in `cli_pipeline.py`, long-form lock workflow, or `RESUME.md` standing gates. They can remain optional manual steps — the same organizational failure that shipped templated shorts.

**No backfill plan for `phrase_ledger.jsonl`.**

Fix 4 only appends on lock going forward. The 8 Psalm 22 shorts and 2 long-forms already locked won’t populate the ledger unless explicitly backfilled before Fix 4 checks mean anything.

**Quote-to-ref mapping unspecified.**

Narrations tag refs on the line before quotes (`**[narrator — KJV, Psalm 22:18]**`). Fix 1 “verify every quoted span against the full-Bible canon” and Fix 2 anchor-verse check both need this parser. Neither Fix 1 nor Fix 2 files list it.

**Re-verification scope underestimates long-form cost.**

“Fix 2 harness on all 10 narrations” (line 107): two long-forms are ~1300+ spoken words with 14–17 KJV spans. Full `engine.review` (6 agents + 8 gates + independent path) per long-form is expensive and agent-bridge-blocking. No plan for spoken-only deterministic pass vs full LLM pass tiering.

**G8.6 naming drift.**

Plan cites “G1–G8.6” (Context line 14) but `_review_role` returns **8 gates (G1..G8)** with first-hearing folded into G8 (`engine.py:690`). Minor, but implementers may hunt for a nonexistent G8.6 gate.

**Ellipsis/excerpt convention vs “whole span punctuation”.**

Project convention allows trailing ellipses inside quotes for excerpts (Isaiah 53 narration, independent reviews). Fix 1 “compare the whole span’s punctuation” (line 40) conflicts with excerpt marking unless explicit rules distinguish **interior** punctuation (must match) vs **boundary** ellipsis (allowed). Not specified.

---

### Reuse / duplication

**Good:** Reuses `kjv_check` shape, `engine.review`, `independent_review.py` plumbing, `pipeline/learning.py` append pattern — aligned with CLAUDE.md “do not duplicate downstream pipelines.”

**Bad:** Proposes `pipeline/quote_rules.py` while `kjv_check.py` already owns deterministic quote logic and `defect_classes.json` already documents Rule-8 and anchor-verse proposals. Risk of parallel quote-check modules unless consolidated.

**Bad:** Fix 2 “OR reuse `independent_review.LENS_NARRATION`” (line 52) alongside `engine.review` duplicates review surfaces without defining when each runs — and standing rules already require external panel on every LOCK anyway (triple review stack).

---

### Cost / spend justification

Deterministic layers are truly $0. LLM cost is **understated**: batch re-lock of 10 artifacts through engine review + 5-CLI panel + possible re-renders is non-trivial time and possibly API spend. Fix 5 and Fix 4 generation injection add ongoing Opus tokens every generate/review cycle. The plan should tier: **Phase A** = spoken extractor + exact cluster duplicate gate + KJV canon with ref-tagged span compare (proves the miss is caught); **Phase B** = ledger + conviction dimension + full re-verification gauntlet.

---

### What the plan gets right

- Root cause line is accurate: per-artifact + corrupt-trust-chain + no catalogue memory.
- `tired-landing` is intra-artifact only; static blocklist is one cliché behind (`defect_classes.json` confirms `quote-count-rule8` / `anchor-verse-unquoted` still `status: none`).
- Cluster gate is the actual miss; acceptance test on Psalm 22 shorts is the right proof target.
- Ps 22:7 comma vs cache is a real integrity gap for strict verbatim enforcement.

---

VERDICT: REVISE

TOP FIXES:
1. **Specify short-format spoken extraction and quote-to-ref parsing first** — without it Fix 2/3 cannot run on the 8 shorts; defer full-Bible canon until ref-tagged span compare (including interior elision) is designed, not just “whole punctuation.”
2. **Split Phase A (prove cluster catch) from Phase B (ledger + conviction + generation injection)** — ship exact/near-duplicate hook/CTA/opener detection + optional `LENS_CLUSTER` on spoken-only text as the acceptance test before building all five fixes.
3. **Wire gates into the actual lock paths** (long-form funnel, shorts cluster, `cli_pipeline.py`) and backfill `phrase_ledger.jsonl` from existing locked content; resolve `primary_ref` from narration metadata, not stale `series.json` alone.
