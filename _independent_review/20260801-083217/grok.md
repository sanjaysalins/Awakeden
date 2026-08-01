# Independent review — grok (OK, 127s)

I'll verify this plan's claims against the real codebase before writing the adversarial review.# Independent adversarial review — pipeline slowdown POC plan

Skeptical default. Diagnosis cleanup is better than the first pass; the **fix plan still points at the wrong surface and undermeasures success**.

---

## Critical: instruments the wrong pipeline

**Step 2A** says log at “existing milestone write-points… (narration locked, audio done, scene plan locked, images done, clips done, final cut assembled)” via something like `pipeline/stage_log.py` into `data/stage_timings.jsonl`.

**Confirmed pain (Storm / Bronze Serpent)** lives under `poc_living_sketchbook/` as **per-episode ad-hoc scripts** (`_s2_stills.py`, `_s3_animate.py`, `_s4_assemble.py`, …), not the `cli.py` / `cli_visual.py` / `cli_assemble.py` chain.

- Living-sketchbook skill status: **DRAFT**, build order in skill §8, not core runners.
- Those POC scripts do **not** call a shared “narration locked / scene plan locked” helper you can hang one logger on.
- Spend already timestamps metered work in `data/spend_ledger.jsonl` via `pipeline/cost.record` / `record_hf`. A new `stage_log` that only touches core milestones will **not** show whether Storm-class rebuild pain improved.

So Step 2A as written mostly measures the path the plan itself says is “stable… byte-identical since May,” while the expensive path stays unmeasured. That is a false sense of data-driven rigor.

---

## Critical: Step 2B re-states rules that already failed

Step 2B: pre-flight checklist for multi-figure→Kling / calm→Seedance, character refs, NSFW routing — “audit that the routing is actually applied before first render.”

**Already true in code/docs for the failed episode:**

- `poc_living_sketchbook/bronze_serpent/_s3_animate.py` has an explicit `JOBS` list with per-spread `"kling"` / `"seedance"` (docstring: “Kling for multi-figure/action… Seedance for everything else”).
- Comments show **mid-episode re-routing after failure** (e.g. `s01_wide` Seedance NSFW twice → switched to Kling), not “forgot the locked rule.”
- Living-sketchbook `SKILL.md` §4 already defines Seedance vs Kling tiers; §8a is a full-res still QC checklist written **because Storm already blew up**.

So Step 2B is mostly **process hope**: re-read the same governors, maybe check boxes. It does not add:

- a fail-closed classifier or lint (“multi-figure still on Seedance → block spend”),
- a written pre-flight artifact the next episode must leave on disk,
- or any mechanism that would have stopped Bronze’s real failure modes (false-positive NSFW, Seedance inventing motion **after** correct tiering, identity drift across poses).

Calling that a “POC” oversells it. Without teeth, Step 3’s “if clearly better, lock into CLAUDE.md” just freezes another checklist the agents already had and still burned 14h+.

---

## Critical: baseline / experiment design is confounded

Step 2B/3: measure next episode against “Storm (6 versions / 38h) and Bronze Serpent (5+ rerolls / 14h24m)” vs “earlier builds’ clean 1.5–2h passes.”

Problems:

1. **Storm/Bronze are not pure “forgot routing” runs.** They co-invented devices (keeper hand, wash-creep, inserts, style bakeoffs, Round 6 kills). Wall-clock includes R&D, not only production discipline.
2. **No control.** Next episode + checklist will almost always look “better” because format learning is front-loaded. That does not prove the checklist caused improvement.
3. **No numeric pass bar.** “If clearly better” is not a decision rule. Reroll count, wall-clock, and bridge age are mixed units; wall-clock includes human sleep and human gates.
4. Plan never defines **what the next episode is** (another DRAFT living-sketchbook? a stable Gold Seam short?). Cost gate “rides on the next episode that would be built anyway” can smuggle a large experimental spend under “normal cost.”

---

## Medium: wrong diagnosis of agent-bridge fix

Step 0 + 2C: clear stale requests; run watcher; track time-to-first-notice under 30s/5min vs “6–16 DAYS.”

`watcher_service.py` is explicit: **detect + surface only**, “does not (and cannot) fabricate a real reply.” Stale age = **nobody serviced requests**. A chip that goes yellow at 30s only helps if a human is looking at the statusline. It does not reduce abandonments when the operator is offline for days.

Also incomplete cleanup narrative: `_stale_cleared_20260801/` exists, but the bridge tree still has other `_stale_*`, `_orphaned/`, `bash.exe.stackdump`, large `archive/`, leftover `responses/` for cleared IDs. Step 0 is not a full reliability reset; calling watcher “confirmed running” is environment-local and not part of the plan’s durable verification.

---

## Medium: skill complexity named, then ignored

Confirmed finding: ~60 skills, cognitive load, **not** core Python imports.

Then every Step 2 action is instrumentation + sketchbook checklist + bridge watch. **Nothing** addresses skill sprawl (freeze new skills, skill inventory, “don’t add devices mid-episode,” panel-lock living-sketchbook before more episodes).

That undercuts the bottom line “two specific fixable things.” The evidence section itself lists a third real cost (tracking load) with no POC.

Claim “zero of the 60 skills are wired into core pipeline code” is true as a grep of imports and **misleading as operational risk**: living-sketchbook, animate, stills, etc. **are** the path agents run. Pain is agent procedure, not `cli_visual` imports. Treating “not imported” as “low cost” is how this plan under-scopes the fix.

---

## Medium: reuse / overbuild on 2A

- `pipeline/cost.py` already append-only JSONL with `ts`, `episode`, `stage`, `note` for metered ops.
- Spend + clip/still filenames + reject folders already support **post-hoc** reroll counts for POC folders without new infrastructure.

New `pipeline/stage_log.py` + hooks into multiple runners is more surface area than needed **unless** it is explicitly designed for **poc_living_sketchbook ad-hoc stages** (and human-gate wait vs work time). Plan follows `cost_status` fire-and-forget but does not reuse `cost.record` or extend the existing ledger schema.

---

## Smaller but real

| Claim / step | Problem |
|---|---|
| “Core pipeline LLM call structure byte-identical since May” | May be true for a narrow chokepoint; **operator cost** is dominated by living-sketchbook / panel devices / gates added since then. Guardrail comfort ≠ problem isolation. |
| NSFW “routed up front” | Bronze already documents empirical NSFW failures; moderation is non-deterministic. “Identify sacred/bare-torso up front” does not equal reliable provider routing. |
| Character ref “checked up front” | Skill already requires multi-pose dual-ref (found 2026-07-28). No new enforcement. |
| Step 1 panel before Step 2 | Good. Step 2A still risks code landing before the surface mismatch is fixed. |
| “Does not touch in-progress episode folders” | Fine; does not stop **building another** unfixed DRAFT format episode. |
| Verification 2A: “spot-check against mtimes” | Plan already called mtimes fragile; verifying the new log against the broken method is circular. |

---

## What is solid (brief)

- Retracting bad first-pass metrics (retry 59%, “stalled” GATE 2, etc.) is honest and useful.
- Guardrails (don’t force GATE-2 backlog, don’t rewire LLM provider yet, no production core surgery) are right.
- Prefer small reversible POCs over a big rewrite.
- Step 0 archive-not-delete for bridge debris is the right shape of cleanup.

None of that rescues Step 2A’s target surface, Step 2B’s lack of teeth, or Step 3’s confounded “clearly better.”

---

## Verdict reasoning

Not **PASS**: experiment cannot falsify the fix as written.  
Not **FAIL**: direction (measure, small POCs, don’t torch production) is sound; Step 0 is mostly fine.  
**REVISE**: re-aim instrumentation and define a real pre-flight gate + valid comparison before any lock-in.

VERDICT: REVISE
TOP FIXES:
1. Point Step 2A at the actual failure path (`poc_living_sketchbook/*` stage scripts + human-wait vs work time), or reuse/extend `spend_ledger.jsonl` — do not only hook `cli_*` milestones that Storm/Bronze never used.
2. Replace Step 2B’s soft checklist with a fail-closed, on-disk pre-flight (e.g. per-spread model + ref + NSFW flags that block animate until present) — rules already in SKILL/`_s3_animate.py` JOBS already failed without enforcement.
3. Redesign Step 3: fix comparison confounds (don’t treat Storm 38h as pure process baseline), name the next episode type, and set numeric go/no-go thresholds before locking anything into CLAUDE.md.
