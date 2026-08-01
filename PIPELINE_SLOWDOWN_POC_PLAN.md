# Fix the slow/expensive/error-prone content pipeline — small POCs, data-driven

## Context

The user (owner/operator of this content engine) reported that content creation
has gotten slower, more mistake-prone, and more expensive, and asked for a
scientific, numbers-backed diagnosis with small, reversible POCs to test any
fix before it touches active production — plus an adversarial review before
anything gets locked in.

Three parallel research agents gathered hard evidence (git history, the spend
ledger, and file-timestamp timing reconstruction). Then, per explicit
instruction, five more independent agents tried to REFUTE each finding. That
red-team caught real mistakes in the first-pass diagnosis. This is the
corrected picture.

**Retracted (first-pass claims that turned out wrong):**
- "Retry spend climbed to 59% of weekly budget" — a regex bug matched pipeline
  stage-names (`stills_v2_period`) and version strings (`eleven_v3`) as if
  they were retries. Correctly-measured retry spend is 3-10% of weekly spend
  and DECLINING, not climbing.
- "CLAUDE.md and v2/SPEC.md are out of sync on INV-26" — false, it's in both,
  verbatim.
- "STATE.md/RESUME.md are stale/neglected" — likely wrong; only the file
  tails were sampled. Deeper entries dated 2026-07-09 and 2026-07-26 exist
  and are current.
- "11 PythonProject1 shorts (episodes 37-47) stalled mid-render" — false.
  They are COMPLETE stills sitting at the pipeline's own by-design human
  checkpoint (GATE 2 image review), not a crash.
- "13 unpublished GREEN packs = neglect" — false. `RESUME.md` and `STATE.md`
  show this is a known, explicitly tracked, deliberately-revisited decision —
  holding launch for a higher visual-quality bar, blocked on outstanding
  launch-prep items (banner/avatar/playlist/date), not a process failure.

**Confirmed (survived the red-team):**
- Skill/gate complexity is genuinely growing fast: 60 pipeline-specific
  skills in `.claude/skills/` (22 added in the final 2 days sampled alone),
  52+ named gates/invariants across `CLAUDE.md` and `v2/SPEC.md`. BUT grep
  confirms zero of the 60 skills are wired into the core pipeline code
  (`cli.py`, `cli_visual.py`, `cli_assemble.py`, `pipeline/*.py`) — they're
  opt-in, each capped by its own spec ("≤1 per episode", "used selectively").
  Real cost = cognitive/tracking load, not extra runtime.
- The agent-bridge (`.agent_bridge/`) had real, currently-live reliability
  debt: 3 abandoned requests sitting 6-16 days old, a crash-dump file, and
  historical evidence of repeated manual firefighting (one episode alone has
  25 retry-related log files).
- Storm and Bronze Serpent (both brand-new "living-sketchbook" format,
  marked DRAFT / not yet panel-locked) really did take far longer than
  earlier builds of the same format (Storm: 6 rebuild versions / 38h; Bronze
  Serpent: 5+ reroll cycles / 14h24m — vs. earlier builds' clean 1.5-2h
  passes). Driven by specific, named, recurring technical failures: identity
  drift, garbled multi-figure motion, provider failures, NSFW blocks. New
  pipeline-wide gates (landing-hold, panel-variety) also added real, dated,
  bounded friction to established styles.

**Bottom line:** this is not "the whole pipeline is decaying." It's two
specific, fixable things: (1) a brand-new experimental format hitting real,
recurring, nameable technical failure modes, and (2) an unreliable
human-serviced call layer with live debris and no instrumentation to measure
whether any fix actually helps. Both are addressable with small, cheap,
reversible POCs that don't touch the stable, unchanged core pipeline (its
per-stage LLM call structure has been byte-identical since May).

## Plan

### Step 0 — immediate $0 cleanup (DONE)

1. Archived the 3 abandoned bridge requests into
   `.agent_bridge/_stale_cleared_20260801/` (moved, not deleted).
2. Reviewed and committed the watcher tooling (`watcher_service.py`,
   `start_watcher.vbs`, `AGENT_BRIDGE.md`, `cost_status.py`) — commit
   `d6d2e03`. Added the new runtime-state files to `.gitignore`
   (`data/.turn_state/`, `data/.watcher.pid`, `data/.watcher_status.json`),
   matching the existing `data/.cost_state/` convention.
3. One-line nudge (not a fix, no action taken): the 11 episodes waiting at
   GATE 2 in `PythonProject1\jesus\narration\` and the 13 unpublished GREEN
   packs are open decisions worth revisiting when ready.

### Step 1 — literal AI panel review of this plan (DONE — DEGRADED quorum, 3/5)

Ran `independent_review.py --type plan`. codex and gemini timed out (300s);
cursor, claude, and grok all answered with **VERDICT: REVISE**, independently
converging on the same problems:

1. **Step 2A (as first written) targeted the wrong pipeline.** Storm/Bronze
   Serpent's actual wall-clock lives in ad-hoc `poc_living_sketchbook/*`
   scripts, not the stable `cli.py`/`pipeline/runner.py` core the plan
   itself already says is unchanged since May. Fixed: retargeted (see
   revised Step 2A below).
2. **Step 2B's diagnosis was factually wrong.** Direct code read
   (`poc_living_sketchbook/bronze_serpent/_s3_animate.py`) shows Bronze
   Serpent's Kling/Seedance routing was already correct — failures (s06_forge:
   3 strikes across both providers; s10_golgotha: an NSFW-triggered reroll)
   happened WITH correct routing, from real model nondeterminism, not a
   missed rule. A "re-check the routing" checklist would have fixed nothing.
   What the code actually shows missing: s01_wide needed a human to notice
   an NSFW rejection and hand-edit the JOBS tuple to switch providers — no
   automatic fallback existed. Fixed: built the fallback (see revised
   Step 2B below).
3. **Step 3's comparison was confounded** by the learning-curve effect
   (episode 3 of any new format looks faster than episodes 1-2 regardless of
   any fix). Fixed: revised decision rule below.
4. **The "60 skills, 22 in final 2 days" number used the exact fragile
   mtime-on-a-gitignored-folder method the plan itself calls out elsewhere**
   as unreliable. Correction: live count is 94 directories, a meaningful
   chunk of which are generic Claude Code starter-pack skills, not
   pipeline-specific. The growth-RATE claim is unverified; softened below.

### Step 2A (REVISED) — bridge latency baseline + retargeted stage timing

- Computed a real bridge service-latency baseline directly from the existing
  `.agent_bridge/archive/` request→response mtime pairs (2,340 pairs, no new
  instrumentation needed): **median 27.5s, p90 85s, p99 293s** — when the
  bridge IS being actively serviced, it's fast. This confirms the earlier
  finding: the 6-16 day debris is an abandonment problem (nobody servicing
  the bridge for days), not a slow-service problem.
- Added `pipeline/cost.record_stage(episode, stage, note="")` — a $0
  milestone marker written into the EXISTING `data/spend_ledger.jsonl`
  ledger (not a new parallel file, per the panel's reuse critique),
  try/except-wrapped so a write failure never blocks a run.
- Wired it into `poc_living_sketchbook/storm/_s3_animate.py` and
  `poc_living_sketchbook/bronze_serpent/_s3_animate.py` (`animate_start` /
  `animate_end`) — the actual failure-path files, not the core CLI chain.
  Both episodes' clips already exist (idempotent skip), so this only takes
  effect on future runs (e.g. Bronze Serpent's 9 still-held-back spreads).

### Step 2B (REVISED) — automatic NSFW fallback, not a checklist

Added `run_job_with_fallback()` to the shared driver
`poc_comic_page/_animate_piece1_v2.py` (additive only — `run_job()` itself
is untouched, so no other caller is affected): on failure, retries ONCE with
the OTHER provider (Kling <-> Seedance) instead of blindly retrying the same
one, mirroring the already-proven `HybridVideoProvider` fallback pattern in
`pipeline/video_render.py`. Wired into both episodes' `_s3_animate.py`
`main()` in place of the old blind same-provider retry. Directly targets the
one concrete, evidenced gap (s01_wide) instead of re-stating a rule that was
already being followed.

Deliberately NOT built this round (named, not silently dropped): a
deterministic enforcement of SKILL.md's §8a eye-verify-before-animate
checklist (currently a comment/TODO, not a mechanical gate) — a real
next step, modeled on the proven `panel_variety_lint.py` pattern, that needs
its own scoping pass rather than a rushed marker-file convention.

### Step 2C (REVISED) — rescoped from "reliability" to "detection + alerting"

Per the panel: `watcher_service.py` detects and surfaces, it cannot reduce
stall time when nobody is actively servicing the bridge for days — that's a
session-discipline gap, not a code gap. Honest scope now: track
time-to-first-notice (target: under the watcher's own 30s/5min thresholds)
across the next few sessions; the 27.5s median service-latency baseline
above is the number to watch for regression, not proof of a "fix."

### Step 2A — POC: instrument stage timing ($0, purely additive)

There is currently no reliable way to measure "did a fix help" except
reconstructing timestamps from file mtimes after the fact (fragile — several
episode folders get touched by unrelated later batch jobs). Add one small,
best-effort append-only logger, following the existing try/except-wrapped
pattern already used in `cost_status.py`'s ledger writes:
- New tiny helper (e.g. `pipeline/stage_log.py`) that appends
  `{episode, stage, ts}` to `data/stage_timings.jsonl` at existing milestone
  write-points that already exist in the code (narration locked, audio done,
  scene plan locked, images done, clips done, final cut assembled).
- Failure to write must never block the pipeline — same fire-and-forget
  discipline as the existing spend ledger.
- This alone doesn't fix anything; it makes Step 2B/2C measurable with real
  data instead of guesswork.

### Step 2B — POC: harden the living-sketchbook format's named failure modes

Before the next living-sketchbook (or any new-format) episode, apply a
pre-flight checklist targeting the SPECIFIC failure modes the evidence
named — not a general process change:
- Multi-figure/action panels routed to Kling, calm single-figure to Seedance
  — this rule already exists (locked) but Bronze Serpent's failures suggest
  a gap between the rule and what actually got rendered; audit that the
  routing is actually applied before first render, not discovered after a
  garbled result.
- Every peopled still has its character reference attached before generation
  (existing locked rule) — checked up front, not diagnosed after identity
  drifts.
- Sacred/bare-torso stills identified up front and routed to the NSFW-safe
  fallback provider from the start, not discovered via a failed run.

Cost gate: this rides on the next episode that would be built anyway — no
new spend beyond that episode's normal cost. Still requires an explicit
quote + go-ahead first, per the repo's own locked "ask before spending" rule.

Measure: reroll/reject file count + `data/stage_timings.jsonl` elapsed time
for that episode, compared against the Storm (6 versions/38h) and Bronze
Serpent (5+ rerolls/14h24m) baseline already measured.

### Step 2C — POC: agent-bridge reliability ($0, no new spend)

Run the next 2-3 sessions with the watcher (from Step 0, already committed
and confirmed running) active and track:
- Time-to-first-notice of a stuck request (target: under the watcher's own
  30s/5min thresholds, vs. the 6-16 DAYS observed before cleanup).
- Whether any new stale-request debris accumulates.

### Step 3 (REVISED) — compare with the learning-curve confound named

A single "next episode looked faster" is NOT proof the fallback/instrumentation
caused it — episode 3 of any new format improves on episodes 1-2 just from
the format being better understood by then. Track instead the
mechanism-level signal the fix actually targets, which isn't confounded the
same way:
- Does `run_job_with_fallback` auto-recover at least one real NSFW rejection
  without a human noticing and hand-editing a JOBS tuple (as s01_wide
  needed)? That's directly attributable to the change.
- Secondary/directional only: reroll count and elapsed wall-clock vs. the
  Storm/Bronze Serpent baseline — reported, not treated as proof.
No lock-in into `CLAUDE.md` is proposed from n=1-2 episodes either way.

## Explicit guardrails (things this plan does NOT do)

- Does not touch the 11 GATE-2 episodes or 13 unpublished packs beyond the
  one-line nudge — those stay the owner's explicit call.
- Does not change the core pipeline's LLM call structure — confirmed
  byte-identical since May; no gates added or removed.
- Does not switch `LLM_PROVIDER` away from the agent-bridge default — that
  $-for-speed trade-off (and the fact that the metered-API logging path is
  currently unwired) is flagged as a possible future POC, not in scope now.
- Does not touch any in-progress episode folder.

## Verification

- Step 0: `git status` shows the 3 stale requests moved (not deleted) and
  the watcher files committed; `watcher_service.py` confirmed reporting 0
  stale requests. DONE.
- Step 1: panel verdicts read and addressed. DONE (3/5 quorum, REVISE ->
  Step 2A/2B/2C retargeted per the findings — see above).
- Step 2A/2B code: `py_compile` clean on all 4 files; an isolated $0 mock
  test (no network calls) proved `run_job_with_fallback()`'s three branches
  (primary succeeds / primary fails then fallback succeeds / both fail) and
  confirmed `record_stage()` doesn't disturb `cost.summary()`/
  `today_summary()`. DONE — this proves the CODE is correct, not that it has
  fired in production yet (no living-sketchbook episode has run since the
  change).

## Status as of 2026-08-01 — what's proven vs. what's still open

| Piece | Built? | $0-verified? | Proven in production? |
|---|---|---|---|
| Watcher (Step 0) | yes, running now | yes (reports `ok, count 0`) | live and protecting, but hasn't yet caught a real stall since cleanup |
| Bridge latency baseline | yes | yes — real historical data, done | n/a — this IS the metric, not a thing awaiting proof |
| NSFW auto-fallback (Step 2B) | yes | yes — mock-tested, 3/3 branches pass | **NOT YET** — needs a real NSFW rejection to fire |
| Stage timing (Step 2A) | yes | yes — doesn't break cost reporting | **NOT YET** — 0 real rows exist; needs `_s3_animate.py` to run again |

**Nothing above counts as "fixed and confirmed" in production yet.** The
code is correct; whether it actually helps still needs a real run to watch.
That's the one remaining POC (Step 2C/3), and it isn't optional — it's the
only way to close the loop.

## Concrete metrics to watch on the next real animate run

The natural next trigger already exists and needs no new work invented:
Bronze Serpent has 9 spreads still held back by its own TEST GATE (see
`poc_living_sketchbook/bronze_serpent/_s3_animate.py`'s docstring) — those
still need the SKILL.md §8a full-resolution eye-verify pass first, and
running them is a real spend decision requiring an explicit quote + go-ahead
first, same as any other batch. A fresh new episode's first animate pass
works just as well as the trigger.

Whichever happens first, check:

1. **NSFW auto-recovery** — in the run's console output / final summary,
   look for `retrying with <X> instead of <Y>` followed by
   `clean (fallback:<X>)`. That line appearing and ending in success (not
   `FAILED`) is the fix working — no human had to notice and hand-edit a
   JOBS tuple. Absence of any NSFW rejection this round means the metric
   simply didn't get exercised yet, not that the fix failed.
2. **Stage timing data exists** —
   `.venv\Scripts\python.exe -c "from pipeline import cost; [print(r) for r in cost.load() if r.get('kind')=='milestone']"`
   should show real `animate_start`/`animate_end` rows for the episode, with
   a real elapsed-time gap between them.
3. **Bridge stall detection** — if any bridge request stalls during the
   session, `data/.watcher_status.json`'s `state` should flip to `pending`/
   `stalled` and show up in the statusline chip within the watcher's own
   30s/5min thresholds — not sit silent for days like the 3 cleared ones did.
4. **Reroll count / wall-clock** (secondary, directional only — confounded
   by the format-learning-curve effect per the panel's finding, so this
   alone never proves the fix worked) — compare against Storm (6 versions /
   38h) and Bronze Serpent (5+ rerolls / 14h24m).

None of these four need new tooling — they're all readable from what
already exists (console output, the spend ledger, the watcher status file).
