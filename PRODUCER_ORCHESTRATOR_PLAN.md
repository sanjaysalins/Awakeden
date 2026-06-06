# PRODUCER ORCHESTRATOR — design for review (v0, 2026-06-06)

**Goal (user's words):** run long-form AND short-form creation in parallel via an
orchestrator that handles both together, so the user "just is the quality gate."

This document is the PLAN to be red-teamed BEFORE any build. Nothing here is built yet.

## Problem statement

Today:
- **Shorts** have an orchestrator: `cli_pipeline.py` + `pipeline/orchestrator.py` —
  resumable topic→cut flow, artifact-driven position detection, `pipeline.state.json`,
  3 human gates (audio / images / clips), image-gate-before-Kling cost saver.
- **Long-form** is HAND-CRAFTED: a set of stand-alone driver scripts under `longform/`
  (`_render_images_16x9.py`, `_animate_16x9.py`, `_assemble_16x9.py`, `_soundstage_*.py`,
  `_make_index.py`, `_reanimate_one.py`, the new `_test_gate.py`) that the agent drives
  step by step. There is NO single long-form runner, and the scene plan / narration are
  authored by hand, not by a `runner`.
- The two tracks share: one Anthropic key (agent bridge), one ElevenLabs key, one
  Higgsfield credit pool, one NBP/Gemini key, one local disk, one user.

The user wants to feed a SLATE of topics (mix of shorts + long-form) and only be pulled
in at quality gates, with the machine stages running concurrently between gates.

## Proposed design

A **producer** layer (`producer.py` + `producer_state.json`) that sits ABOVE the existing
runners/drivers and does NOT reimplement them:

1. **Episode queue.** `producer_state.json` holds a list of episodes, each:
   `{id, kind: short|long, topic/ref, stage, status, budget_spent, gate_pending}`.
   `stage` ∈ {script, review, audio, visual_plan, images, animate, assemble, caption, done}.

2. **Stage state-machine per episode**, idempotent + resumable (mirrors how
   `orchestrator.py` already does artifact-driven position detection):
   - SHORTS stages delegate to the existing `orchestrator.py` / stage runners unchanged.
   - LONG-FORM stages shell out to the existing `longform/` driver scripts unchanged
     (with their `--approved` test-gates), plus the hand-authored script/scene-plan steps
     which the AGENT performs (not automatable today).

3. **Free vs gated vs metered classification per stage:**
   - FREE (auto-advance, can parallelize): script draft, red-team, 5-CLI panel,
     scene-plan authoring, assembly planning, caption.
   - METERED (needs budget): audio (ElevenLabs), images (NBP/HF), animation (veo/Kling).
   - QUALITY GATE (needs the user): approve script, listen to audio, image gate,
     clip gate, final watch.

4. **Gate queue.** Instead of blocking on each gate, the producer collects all
   `gate_pending` items across all episodes into ONE review queue and surfaces them
   together: "2 scripts to approve, 1 audio to hear, 3 images to judge." The user clears
   the queue; the producer advances each episode past its cleared gate.

5. **Budget ceiling (the spend-rule change).** A configurable cap, e.g.
   `--budget 90 --per-episode 30`. The producer tracks `budget_spent` and only runs a
   metered batch if it stays under the cap; if a batch would exceed it, that becomes a
   gate ("approve +$12 to animate ep2?"). This REPLACES the locked "ask before every
   metered batch" rule with "ask once for a ceiling, then ask only at the ceiling."

6. **Parallelism model.** Pipelined, capped at 2–3 concurrent metered tracks to respect
   shared credit pools and rate limits. Free stages can fan out wider (the Workflow tool
   or background agents). The agent bridge is serialized, so LLM-bearing steps queue.

7. **Idempotence + crash safety.** Every stage writes its artifact then updates
   `producer_state.json`; re-running the producer resumes from disk (same model as
   `orchestrator.py` + the assembly runner's LOCKED detection).

## What it explicitly REUSES (no duplication)

- `pipeline/orchestrator.py` and all 4 shorts stage runners — unchanged.
- All `longform/` driver scripts — unchanged (now test-gated).
- `independent_review.py` (5-CLI panel), the red-team pattern, `_test_gate.py`.
- `narration_pipeline.py` / `per_turn_synth.py` / `image_to_kling.py` — still subprocessed.

## Known risks (author's own list — red-team should extend/refute)

- **R1 Long-form is not fully automatable.** Script + scene-plan are hand-authored by the
  agent with research + KJV verbatim + red-team. The producer can ORCHESTRATE those steps
  (call the agent, wait) but cannot remove the agent from the loop. "Just the quality gate"
  is only true for the MACHINE stages, not the authoring.
- **R2 Shared credit pools / rate limits.** 2–3 concurrent metered tracks may still
  contend; the bake-off already saw unexplained ~13-credit accounting drift.
- **R3 The budget-cap change weakens a safety rule.** Pre-authorizing spend removes the
  per-batch circuit-breaker that has already caught surprises (~$15–18 Opus surprise).
- **R4 Quality dilution.** Parallelism pressure could tempt skipping red-team/panel. The
  project's entire edge is that discipline.
- **R5 Build cost vs payoff.** The producer is real code (state machine, gate queue,
  budget tracker). Is it worth it for a 1–3 episode/week cadence, or is "agent drives it
  manually in producer mode" enough?
- **R6 Two-repo split.** Shorts runners live in this repo; audio + image_to_kling live in
  `PythonProject1`. The producer spans both via subprocess; path/env coupling is fragile.

## Success criteria

The producer is worth building only if: (a) it measurably reduces the user's touch-points
to gate-clearing, (b) it never spends past the ceiling, (c) it never skips a review pass,
(d) it is strictly thinner than reimplementing any runner, (e) a crash mid-run loses no
paid artifact.

## Alternative considered

**"Producer mode" with NO new code:** the agent manually pipelines 2 tracks today
(as demonstrated: Psalm 22 audio rendering while the next script is drafted), using
background tasks + a simple checklist, and we only build `producer.py` if the manual
cadence proves too heavy. Lower risk, zero build, but no durable/resumable state and the
gate-batching is ad hoc.
