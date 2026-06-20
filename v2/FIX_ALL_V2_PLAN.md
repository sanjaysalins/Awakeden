# FIX-ALL v2 PLAN — bring the whole catalogue to the v2 bar

**Goal:** every narration finished to the full v2 standard — multi-voice, clean + punchy
clips (speed-to-fit), **full Cinematic-Orchestral score that moves the listener deeply**,
ivory caption. Reuse-first to keep spend low.

**Source of truth for state:** `C:/Users/sanjay/CONTENT_AUDIT.html` (42 narrations).
- 🟢 v2-done: 10  ·  🟡 old-bar video: 10  ·  🔵 audio-only: 18  ·  ⚪ text-only: 4
- Remaining to lift: **32** (before triage).

## The standing rules baked into EVERY episode
- Multi-voice (Scripture voice + a voice per quoted speaker); narrator-only is the exception.
- Full Cinematic-Orchestral score, mixed soft, that moves deeply ([[feedback-cinematic-score-standard]]).
- Speed-to-fit / backfill-to-punchy (~4–5s/slot, ~16–20 clips).
- Regen `narration.alignment.json` after ANY audio-length change ([[alignment-cache-staleness]]).
- never-animate-writing; period/reverent image audit; gospel-frame hero close.
- Red-team + (for any LOCK) the external 5-CLI panel; depth-first, no review-diluting parallelism.
- Quote metered spend per phase; log to the ledger; ask before spending.

## 🔴 RED-TEAM (2026-06-20) — plan REVISED; budget was 2-3× under

Two hostile reviewers + my own check. Verdict: shape sound, **budget UNDERESTIMATED**, triage needs 3 fixes.
- **CRITICAL — "reuse-first" fails for own-world topics.** The clip library is **116 clips, 100% passion/cross** (Psalm-22/Isaiah/Mockers); the locked **topical-fit gate forbids** importing the ~102 story-specific ones into unrelated episodes (~14 neutral plates are the only legal cross-episode reuse). So storm/well/prodigal/Jonah/Bethesda/bread/Caesarea-Philippi need NEW stills + Kling clips ≈ **$23-30 each** (project's own cost model) + ~30% re-roll buffer. **Real total ≈ $340-580, breaks the $300 ceiling.**
- Stale flag dismissed: the "Eleven Music 401 scope blocker" memory is OUTDATED — 3 scores generated fine today.
- **Triage fixes:** (1) REVERSE cull of `22 He Never Answered Jesus` (distinct "grace-before-yes / man never answers" angle) — keep 22+26+29, cull `18` instead. (2) `Who Do You Say I Am` text is MODERN-ENGLISH not KJV → NOT a cheap pass: drop it (19/24/27 cover Matt 16) OR full KJV re-lock+panel. (3) `#33` is a complementary grace-gap dimension, not a "dupe" (culled for scope, not duplication).
- **Guardrails added:** Door #32 rebuild stays FOLKLORE-FREE (no shepherd-gap custom); `--no-verify` ONLY for the 3 reuse episodes with confirmed clips (every own-world episode = full Vision audit + human GATE 2); any episode whose TEXT changes runs red-team + KJV-strict + 5-CLI panel before re-lock; `/validate` + alignment-regen as mechanical gates; **$200 stop-loss checkpoint**.

## ✅ REVISED SCOPE (user 2026-06-20): "Phase A + reuse-cheap first (~$50); defer own-world."
**DO NOW (cheap, ~$50):**
- **Phase A — 3 old-bar videos** (visuals already exist → upgrade only): `08 The Well That Never Runs Dry`, `16 The Fire Jesus Built`, `32_The_Door_Was_a_Body` (folklore-free).
- **Reuse-cheap audio-only** (passion library genuinely fits): `21 The Pronouns` (Isaiah 53) + `25 The Question on the Gaza Road` (Isaiah 53 / Acts 8). Possibly the Matt-16 / Bethesda abstracts if Christ-face/cross plates carry them.
**DEFER (own-world, expensive ~$23-30 each, separate budget decision):** prodigal `09`, Jonah `23`, Bethesda `22/26/29`, storm `28`, Light `31`, Bread `34/35/36`, Matt-16 set if reuse proves thin.

## ✅ PHASE 0 TRIAGE DONE (2026-06-20) — FINAL REBUILD TARGET = 18 (user chose "Full: cull only true dups, keep multi-dimensions")

**CULLED (13 — not rebuilt, left as-is):**
- Superseded (2): `30 Smitten of God` (= Isaiah 53:5 pilot), `04 psalms 22 part 2` (absorbed by Psalm-22 set)
- Near-identical dupes (11): storm `02`,`20` · Light `06` · Door `07`,`33` · prodigal-bargain `10`,`11`,`12` · Bethesda `18`,`22`

**REBUILD LIST (18):**
*Core best-of-passage (9):* `08 The Well That Never Runs Dry` (Jn4, old-video) · `09 The Father Who Ran` (Lk15, audio) · `16 The Fire Jesus Built` (Jn21, old-video) · `23 The Prepared Belly` (Jonah, audio) · `26 Jesus Walked Past the Pool` (Jn5, audio) · `28 What Manner of Man` (storm, audio) · `31 The Light You Can Stand In` (Jn8, audio) · `32_The_Door_Was_a_Body` (Jn10, old-video) · `Who Do You Say I Am` (Mt16, audio)
*Multi-dimension kept (9):* Matt16 — `19 The Cliff of Rival Gods`, `24 The Answer Was a Gift`, `27 A List of Dead Men` · Isaiah53 — `21 The Pronouns That Preached the Gospel`, `25 The Question on the Gaza Road` · Bethesda — `29 The Race He Could Never Win` · John6 Bread — `34 The Hunger Bread Cant Fill`, `35 Manna Fulfilled`, `36 In No Wise Cast Out`
*(Optional 19th: `05 He Said It Under the Lamps` — Tabernacles/Light dimension, but TEXT-ONLY → needs audio first; Phase C.)*

**Phase split of the 18:** Phase A (already have video) = 3 (Well, Fire, Door). Phase B (audio→full video) = 15. Phase C (text→audio→video) = 1 (05, optional).
**Cost estimate:** A ~$12-15 · B ~$140-180 (reuse-first; own-world topics pricier) · C ~$10 → **~$165-205**, under the $300 ceiling.

## PHASE 0 — TRIAGE (free, do FIRST)
Cull before committing spend. Identify and set aside:
- **Duplicates / superseded:** e.g. "30 Smitten of God" = Isaiah 53:5 (already a v2 pilot);
  "07 I AM the Door" vs "32 The Door Was a Body" (two Door takes — keep the better);
  "04 psalms 22 part 2" vs the Psalm-22 cluster; "Who Do You Say I Am" vs "27 A List of Dead Men"
  (both Matt 16:15?).
- **Orphans / incomplete:** e.g. "05 He Said It Under the Lamps" (flagged orphan).
- Output: a confirmed FINAL target list (likely ~22–26, not 32). User approves the cull.

## PHASE A — 10 old-bar videos (cheapest, fastest wins; visuals already exist)
Per episode: sweep clips (subagent) → fix defects reuse-first → multi-voice wire+synth →
backfill-to-punchy → re-lock → regen alignment → reassemble → SFX → cinematic score → caption.
- Cost ≈ **$2.50–5 each** (synth ~$0.50 + score ~$2 + occasional defect re-render). ≈ **$30–45**.
- Members: Woman at the Well, The Fire Jesus Built (John 21:17), The Kiss/Prodigal, The Door,
  **Zechariah (already mid-build)**, + the rest flagged old-video in the audit.

## PHASE B — 18 audio-only (need video built)
Per episode: scene-plan → stills (REUSE-FIRST from the 116-clip library; metered render only for
gaps) → animate (reuse-first) → assemble → SFX → cinematic score → caption.
- **Passion/cross/Christ topics** = heavy reuse ≈ $2.50–8 each.
- **Own-world topics** (storm, well, bread, prodigal-type) = need their own stills/clips ≈ $10–20 each.
- Cost ≈ **$5–15 each**. ≈ **$120–220** (depends on reuse hit-rate).

## PHASE C — 4 text-only
Add audio (~$0.50) → then Phase B treatment.

## Execution model
- **Sequential per episode** (build is stateful + metered) — same as the 3 pilots.
- **Parallel subagents** for the FREE upfront work only: per-episode defect-sweep + reuse-match
  proposals (collapses N sweeps into one pass). Build + spend stays one-at-a-time with me driving.
- A reusable per-episode checklist (the pilot recipe) keeps each one consistent.

## Rough total budget: **~$150–280** (reuse-first; firms up after Phase 0 triage).
Quote each phase before running. Pace: a few episodes per session (depth-first).

## ✅ APPROVED 2026-06-20: phased triage-first reuse-first plan; **budget ceiling ~$300** pre-approved (proceed phase-to-phase, log each to the ledger, no per-phase re-ask). Start order: finish Zechariah → Phase 0 triage → A → B → C.

## Recommended sequence
1. Finish **Zechariah** (closes the current sweep — already mid-build).
2. **Phase 0 triage** (free) → confirmed target list + budget.
3. **Phase A** (cheap finished-video upgrades, fast visible wins).
4. **Phase B** then **C**.
5. Panel-review this plan before the big Phase-B spend (enforced significant-plan review).
