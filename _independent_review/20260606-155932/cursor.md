# Independent review — cursor (OK, 56s)

## Independent adversarial review

This is a **strong catalog and state tracker**, not yet a **sound, complete, buildable production plan**. The funnel logic is coherent on paper; execution assumptions, economics, and several catalog edges do not survive contact with the repo.

---

### Feasibility vs real codebase

**1. “Shorts are distilled cuts” has no implementation.**

The plan states: *“Write the long FIRST as the research foundation; shorts are distilled cuts”* and Priority #2: *“Distill Psalm 22's shorts (its own cuts) from the locked long.”*  
`BATCH_PLAN.md` describes this as stage 5, but there is **no `distill` CLI, script, or pipeline stage** in the codebase — only prose. A repo-wide search finds the word only in `_production_tracker.py` comments.

**2. Batch reuse is planned, not built for long-form.**

*“Reuse: batch audio first, then batch stills with cross-episode reuse — bounded to same-format (16:9 vs 9:16) thread-NEUTRAL plates”* and Priority #3’s passion BATCH assume a **stills reuse audit**. `BATCH_PLAN.md` stage 9 defines it; **no long-form reuse-audit tool exists**. Shorts have `pipeline/hero_library.py`; long-form still uses per-episode hand drivers (`longform/_render_images_16x9.py`, etc.). `_episode.py` is episode-generic now, but scene plans are still hand-authored (*“author the 16:9 scene plan first”*).

**3. Long-form is hand-crafted; the plan scales as if it were orchestrated.**

`PRODUCER_ORCHESTRATOR_PLAN.md` (same date) explicitly says long-form has **no single runner** and script/scene-plan steps are **not automatable**. This plan never references that gap, yet schedules a 21-long slate + passion batch as if batch throughput were already proven.

**4. State is a manual overlay, not disk truth.**

Counts like *“Started 16. Cut+ (POC) 9”* come from a hardcoded `ST` dict in `_production_tracker.py` (lines 51–67), not automated discovery. Drift is guaranteed. Example: Priority #4 says *“Bethesda”* but John 5:6 is cataloged under **Questions Jesus Asked**, not Encounters — the overlay hides series/guardrail context.

**5. “76 episodes” understates real production surface.**

Standing direction (`STATE.md`, `multi-dimension-per-topic`) ships **multiple faithful shorts per catalog episode**. The plan counts one row per `series.json` episode but notes *“3 shipped dims: #34 Hunger · #35 Manna · #36 No Wise Cast Out”* for a single I AM Bread row. Cost, cut counts, and sequencing all **undercount real folders and spend**.

---

### Hidden risks & false assumptions

**6. Funnel is broken in practice: 73/76 shorts have no backing long at mp3+.**

*“Shorts awaiting their long (long not yet mp3+): 73”* with *“COMPLETE (uploaded) 0”* means the stated funnel — *“long-forms = the deep, researched meal that SUPPORTS them”* — is **aspirational**, not operational. Posting more cut POC shorts before any long exists widens the gap the plan claims to fix.

**7. Retrofit is named but not designed.**

*“existing shorts get their long retrofitted”* (Priority #4) has **no workflow** for thread alignment, claim reconciliation, or whether retrofitted longs force short re-cuts. Several shipped shorts were authored with **independent threads** (e.g. #32 Door Was a Body vs #33 Shepherd In The Gap). A later I AM anchor long cannot cleanly “back” them without rework the plan does not budget.

**8. Cross-series `primary_ref` collisions are unmapped.**

`FLAG_BY_REF` allows only one flagship per ref. Collisions with **different backing longs and guardrails** are unaddressed:

| Ref | Collision |
|-----|-----------|
| `Luke 23:43` | words-from-cross → Words anchor; Encounters → Encounters anchor (**no cross-file note**, unlike John 19:30) |
| `John 1:29` | types-shadows short → Passover Lamb flagship; names-titles “Lamb of God” → same flagship (**two series, one asset, two guardrails**) |
| `John 11:25` / `John 11:43` | Lazarus flagship claims *“backs Lazarus + I AM Resurrection”* but Miracles *“Raising Lazarus”* is backed by **Miracles anchor**, not Lazarus flagship |
| `John 21:17` | QJA + Encounters share #16 — **conflicting series signatures** (QJA’s three-voice viewer-turn vs Encounters’ anti-psychologising) |

These are doctrinal/framing risks, not cosmetic duplicates.

**9. Tier-1 anchor scope is economically unrealistic.**

Ten anchors like *“Questions Jesus Asked (series deep-dive)”* backing **9 distinct questions**, each with a long guardrail block including *“THREE VOICES… viewer’s own inner response… do NOT compress… repetition IS the restoration”*, implies **~9 mini-episodes inside one ~7 min film**. Same problem for Types & Shadows (8 shorts), I AM (6 shorts on anchor), etc. The tiering model saves flagship count but **concentrates authoring cost into monsters** the plan never scopes.

**10. `BATCH_PLAN.md` and this plan disagree on types-shadows.**

`BATCH_PLAN.md` lists *“Abraham & Isaac (Gen 22)”* as a types-shadows anchor long. This plan’s backlog lists Abraham & Isaac as *“candidate — not yet in series.json”* and only two types flagships (Passover Lamb, Bronze Serpent). **Batch scope is unsettled.**

---

### Over-engineering before proof

**11. Priority order builds inventory before validating publish.**

Isaiah 53 is *“captioned (flagship) FLAGSHIP · READY TO POST”* but Priority puts *“Post Isaiah 53”* at **#5**, after finishing Psalm 22, distilling its shorts, launching a passion batch, and retrofit planning. With *“COMPLETE (uploaded) 0”*, the plan should **prove end-to-end publish** (upload kit, description link to long, analytics feedback) before scaling to 21 longs.

**12. Passion batch (Priority #3) before Psalm 22 long is finished.**

Priority #1 is Psalm 22 scene plan → assemble; #2 is distill its shorts; #3 is *“words-from-cross + types-shadows BATCH.”* Step #2 requires a **locked, assembled long** that does not exist yet (only `_mp3_`). Step #3 expands scope before the flagship template is proven on Psalm 22 the way Isaiah 53 was on Jesus-in-OT.

**13. 21 longs + 76 shorts to cut before a single upload.**

At ~$1940 to cut everything, the plan commits to **~$2k of POC cuts** with zero validated distribution loop. That is production planning without a learning cycle.

---

### Missing steps, verification gaps, done-definitions

**14. Pipeline omits enforced gates and reviews.**

Stages are: *“planned -> narration -> mp3 -> stills -> clips -> cut(POC) -> captioned -> uploaded(COMPLETE)”*. Missing vs repo reality:

- Shorts’ **3 human gates** (audio / images / clips) from `cli_pipeline.py`
- **`independent_review.py`** (mandatory per `CLAUDE.md`) at narration and significant plans
- Long-form **soundstage / caption / final watch** (Isaiah 53 path took many manual steps in `RESUME.md`)
- What “cut (POC)” means for **gold approval** vs upload

*“cut = assembled POC (not yet approved/uploaded)”* appears only in the tracker generator comment, not as a release criterion in the plan body.

**15. No distribution strategy.**

Beyond *“Post Isaiah 53”*, there is no:

- Posting cadence (shorts vs longs)
- Cross-linking (short description → backing long)
- Series rollout order across 3 brands (SLK / Awakeden / Either)
- Platform kits (RESUME.md references upload kits on GDrive; plan does not wire to them)
- `BATCH_PLAN.md` open item: *“Pull GDrive register; finalize slate + episode numbers”*

**16. No multi-dimension policy in the catalog.**

`series.json` is 1:1 episode titles; production is **N dimensions per topic**. The plan does not say whether catalog episodes spawn 1 or N shorts, how dimensions affect tiering, or how to reconcile with *“76 episodes.”*

---

### Reuse: duplicates vs existing tools

**17. Reinvents tracking; underuses existing orchestration.**

`_production_tracker.py` regenerates `PRODUCTION_PLAN.md` — good. But it does not integrate:

- `cli_pipeline.py` / `pipeline/orchestrator.py` for shorts
- `pipeline/hero_library.py` for shorts still reuse (RESUME.md: *“Wire `_library` plates into the engine image stage”* — still queued)
- `BATCH_PLAN.md`’s 13-stage table (richer than this plan’s 8 stages)
- `PRODUCER_ORCHESTRATOR_PLAN.md` for parallel gate batching

Three parallel plans (`PRODUCTION_PLAN`, `BATCH_PLAN`, `PRODUCER_ORCHESTRATOR`) without a single source of truth is a **duplication / drift risk**.

---

### Cost / spend: not justified

**18. ~$1940 is a toy model, not a budget.**

`_production_tracker.py` uses flat `COST = {"long": 30, "short": 20}` × stage remainder factors, rounded to ~$1940. Reality from Isaiah 53 (`RESUME.md`): ~$10 images, ~$11+ animation for **one** long with 21 scenes, plus soundstage, captioning, re-animates. One long ≈ $25–40+ metered; anchors with 15–25 scenes would be higher.

The model **excludes**:

- Multi-dimension inflation (3–4× shorts per catalog row)
- Retrofit rework on already-cut episodes
- Independent review / panel time (not $0 in practice)
- Long-form soundstage and caption passes
- Re-renders from gate failures (common per `STATE.md`)

At 21 longs + 76 catalog shorts + off-catalog Prodigal dims, **$1940 is likely 2–4× low** unless reuse hits the optimistic end of *“~15-25%”* — and reuse tooling for long-form does not exist yet.

**19. Reuse economics are asserted, not gated.**

*“realistic reuse ~15-25%, strong only in the cross/types cluster”* is honest hedging, but Priority #3 treats passion cluster as *“max reuse”* without a reuse audit output or library seed count. Isaiah 53’s library is one episode; banking for a cross-series batch is **unproven**.

---

### Sequencing & tiering economics (summary attack)

| Plan claim | Problem |
|------------|---------|
| Long first, shorts distilled | 9 cut POC shorts + 73 awaiting long; go-forward rule contradicts backlog |
| Tier-1 anchor backs tail | Anchors are huge multi-topic compilations; cost shifted, not removed |
| Tier-2 flagships for rich texts | Lazarus flagship underused; Miracles Lazarus not linked |
| Passion BATCH for reuse | Batch scope unsettled; tooling missing; Psalm 22 not finished |
| Post Isaiah 53 #5 | Only ready asset; should validate funnel first |

---

### Doctrinal framing vs guardrails

**20. Guardrails are copied but not enforced in tiering decisions.**

Examples:

- **names-titles** *“Titles only — not descriptions stretched into titles”* vs backing *“Lamb of God”* by **Passover Lamb** flagship (a type episode, not a titles episode)
- **Resurrection on Trial** *“invitation, not victory”* vs **jesus-in-ot** *“apologetic in tone”* — no rule for tone when shorts from both series funnel to different anchors on the same Passion Week slate
- **Miracles** *“Don't allegorise beyond what the Gospel writer signals”* vs **Feeding 5000** theme *“new Moses, Bread of Life”* overlapping **I AM Bread** shorts already cut — cross-series thread collision unplanned
- **words-from-cross** *“Don't claim the [seven words] order is biblical”* — the anchor long must model that; no check that shorts distilled later preserve it

---

### What is sound (limited credit)

- Building from `data/series.json` (10 series / 76 episode rows) is correct.
- Long tiering (anchor / flagship / short-backed) is a reasonable compression vs strict 1:1.
- Off-catalog + backlog sections show honesty about Prodigal and orphans.
- Retrofit acknowledgment and *“73 shorts awaiting their long”* are honest metrics.
- Reuse constraints (*“same-format… thread-NEUTRAL… topical-fit gate”*) match `BATCH_PLAN.md` and `hero_library.py` intent.

That makes this **REVISE**, not total FAIL — but it is **not buildable as written**.

---

VERDICT: REVISE
TOP FIXES:
1. **Reorder around proof, not inventory:** Post Isaiah 53 immediately; define upload kit + short↔long link + “COMPLETE” criteria; finish Psalm 22 end-to-end as the second template before any passion batch or retrofit slate.
2. **Reconcile catalog with production reality:** Map multi-dimension folders to `series.json` rows; document all `primary_ref` collisions (Luke 23:43, John 1:29, Lazarus trio, John 21:17) with a single canonical backing long and cross-series release rules; automate status from disk instead of the manual `ST` overlay.
3. **Replace the $1940 roll-up with a stage-level budget tied to existing tooling gaps:** Cost per long from scene-count (Isaiah/Psalm actuals), per short including dimensions, retrofit rework line item, human gates + independent review stages, and explicit build-or-defer decisions for distillation workflow, long-form reuse audit, and producer orchestration (merge `BATCH_PLAN` + `PRODUCER_ORCHESTRATOR` into this plan or link them as binding sub-plans).
