# Independent review — grok (OK, 103s)

I'll verify the plan's claims against the real codebase — gates, spend controls, tooling, and wave assumptions.Checking the spend gate, animate path, and whether claimed fixes are actually in code.## Adversarial review — CORPUS ROLLOUT PLAN v5

v5 fixed real round-4 holes: projected stop-loss, bulk guard, duration pin, disk de-dup + rejects, exit-code propagation, re-roll via park-to-`_rejected/`. Those claims match code. Remaining problems still block treating this as a clean GO for paid A(b), and some of the “fail-closed” language is still oversold.

---

### 1. Per-slug “3 attempts” is still a false control

**Cite:** *“Per-slug roll cap: 3 attempts, then stop and report (pilot precedent) — one stubborn CU cannot eat a wave's budget.”*

**Reality:** No counter in `run_piece.py`, `rollout_spend.py`, or any wrapper. Parking a reject makes the slug `missing` and re-renderable forever. Combined with limit (c):

> *“failed-but-BILLED rolls (502s, NSFW blocks) leave neither row nor mp4”*

…there is **no durable state for attempts that cost money**. A(b)’s first roll is explicitly the **wound/CU proof** on crucifixion imagery — highest NSFW/502 risk. The forecast already says worst case is **449–483cr vs 447.5 remaining**. A policy cap that cannot see billed failures is not a stop-loss; it is hope.

---

### 2. “All fail-closed” is false; human QC tooling is still vapor

**Cite (machine bar):** *“Machine bar (all fail-closed, tested — 21 gate tests green)”*  
**Cite (checklist):** scale variety · bookend · filmstrip QC · before/after · fit-gate “reviewed by eye”  
**Cite (A(a)):** *“Deliverable: shared tooling… build_filmstrip() + backup helper + before/after page builder + wave_checklist.json writer”* and *“A(b) is BLOCKED until the A(a) tooling exists.”*

**Reality:**
- Gate + spend on animate are fail-closed. The **7-item human checklist is not**.
- No shared backup helper, before/after builder, or `wave_checklist` schema/writer exists under `batches/` or `pipeline/` (only prose + Women’s one-off `promote_living_light.py` and a `.bak_prelivinglight` final).
- `pipeline.clip_anim_qc.build_filmstrip()` exists — good reuse direction — but full `clip_anim_qc` Vision rubric is Baroque gallery-tour, not living-light (frozen figure / dry wound / expression lock). Checklist item 5 without a living-light rubric is a JPEG factory.
- Wave-gate “re-approval of shipped finals” is defined as reviewing before/after pages that **do not exist yet**. Blocking A(b) on tooling is correct; calling the system fail-closed today is not.

Test count is also soft: `pipeline/test_rollout_gate.py` has **22** `test_*` functions, not 21; none assert `run_animate` → exit 3/4/5, projected breach, or bulk guard.

---

### 3. Bulk / `--only` discipline is half-enforced

**Cite:** *“A(b) invocations MUST use `--only <ll_slugs>`”*  
**Code:** bulk guard only when `not only` and `len(pending) > 2` → exit 5.

**Gaps:**
- Bare `--stage animate` with **≤2** pending still spends without naming LL slugs. Those two can be hash-stale *non*-LL moves after a partial rewrite.
- `cli_livingpage.py` still prints:  
  `run_piece.py … --stage animate` (no `--only`) as the paid next step.
- Bypass CLIs (`_hf_animate_short.py` silent ffmpeg fallback; `_animate_rerolls.py`) still exist. Plan bans them by discipline, not by hard block. One wrong CLI path puts a static fake in a living-light slot.

---

### 4. `FAILED` animate still exits 0

**Cite:** *“Verified: `run_piece` prints FAILED and substitutes nothing”* and *“gate/stop-loss refusals now propagate to the shell exit code.”*

**Reality:** Gate/stop-loss/bulk → 3/4/5 is true (`main()` returns `rc` when non-zero).  
But on `hf_animate` failure, `run_animate` prints `FAILED {slug}`, continues, returns **0**. Automation/score/register will treat a missing LL clip as success. That is the same class of “shell lies about paid work” codex already killed for exit 4 — still open for render failure.

---

### 5. Budget is honest about the wall — and still unsafe as a full-corpus plan

**Cite:** *“Worst case (pilot 2.3×/keeper): ~449–483cr vs 447.5 remaining — right at the wall”*  
**Cite:** *“billed possibly ~+15cr in 502s — limit (c), balance eyeball”*

Even if ledger+disk = **5 × 7.5 = 37.5** (claimed, not re-run here):
- Worst-case model **already overshoots** remaining envelope before limit (c).
- Limit (c) is **outside** max(ledger, disk) by definition.
- HF balance “eyeball at each wave gate” is the same human-discipline control the plan spent four rounds replacing for the animate chokepoint.
- Scope cuts exist (landing-only LL, defer D, drop pieces) — good — but they are **post-breach re-quote options**, not pre-A(b) commitments.

Zero-point story is coherent as a **definition** (rollout starts 2026-07-14; Women Jul 12–13 is separate). Code still says *“PILOT SPEND COUNTS INSIDE IT”* while `ROLLOUT_START` excludes that pilot. Definition works only if operators never confuse “485 total HF” with “485 since Jul 14.”

---

### 6. Wave D “re-derived” is better, still soft

**Cite:** *“the only true still-overuse is empty_tomb's `risen_christ_wounds` ×5 → … Wave D extra ≈ 15–30cr”*

Baseline dump also has **sign_of_jonah**: 5 full-bleed doubles + shared `risen_christ_wounds` landing pair. Grid conversion can fix non-adjacent FB at $0 (same PNG, different `tpl`) — correct. But:
- `risen_christ_wounds` ×5 still needs real reassignment under `MAX_STILL_USES = 2`.
- “~2–3 need NEW stills+clips” is still an estimate; if reassignment needs new plates *and* those plates get LL treatment, 15–30cr is a floor at 1×, not a derived total at 2.3×.
- Wave D stills spend is **not** on `rollout_spend` (animate-only chokepoint). USD is small; still a second meter.

---

### 7. Feasibility of A(a) authoring is understated as a wall-clock risk

**Cite:** *“SPEC AUTHORING (a full gold-master rewrite ×3, NOT a light touch)”* with one-line SOP: *“Christ singles stay full; convert crowd/object/multi-figure; preserve heartbeat/punch/whip.”*

Baseline FAILs for Wave A pieces are severe (e.g. it_is_finished: 94% full-bleed, 0% fx, no temp, cut_ticks, 0 LL). This is not light migration. Missing:
- Named LL slugs **before** A(a) ends (plan says “NAMED per piece before A(a) ends” — good — but no draft table).
- Acceptance test: `python -m pipeline.rollout_gate <piece>` PASS + checklist artifact written.
- Explicit “do not run animate until gate PASS + tooling landed” in the per-piece flow (partially present; `JITB_SKIP_ROLLOUT_GATE=1` still offers a mid-migration fail-open).

---

### What is solid (briefly)

| Claim | Status |
|---|---|
| `rollout_gate` rules (temp poles, double-light, LL play/dyncam, duration≠5) | Match `pipeline/rollout_gate.py` |
| Gate + spend at `run_animate` chokepoint | Real (exit 3/4) |
| Projected stop-loss `spent + 7.5 > 485` | Real (`rollout_spend.check`) |
| Bulk guard exit 5 when pending > 2 | Real |
| Disk de-dup + `_rejected` recursive count + unit test | Real |
| No silent ffmpeg on `run_piece` path | Real (CLI path still dangerous) |
| Baseline dump checked in | Real |
| Wave D animate → register order | Correct vs `register_rows` |
| A(b) blocked on A(a) tooling | Correct process |

---

### Bottom line

v5 is a **serious control plan**, not vapor architecture. It is **not** clean enough for a PASS: the remaining spend-at-the-wall controls (3-attempt cap, limit (c), FAILED→0, bare animate ≤2, human QC tooling) are still prose or partial, and A(b) starts on the riskiest CU.

**A(a) $0 authoring can start only after tooling acceptance criteria are written into the plan (or landed).**  
**Paid A(b) should stay blocked until those + attempt metering are real.**

VERDICT: REVISE  
TOP FIXES:  
1. Enforce the per-slug 3-attempt cap in code (including failed-but-billed attempts under limit (c)); do not treat policy + HF eyeball as a hard envelope control when worst-case already exceeds remaining credits.  
2. Land A(a) tooling with acceptance criteria: backup helper, before/after page, 7-item `wave_checklist` writer, and a **living-light** filmstrip QC rubric (not only `build_filmstrip`); make `hf_animate` failure return non-zero from `run_animate`.  
3. Tighten rollout animate: require `--only` for livingpage pieces (or refuse bare animate when `living_light` is set), fix `cli_livingpage`’s bare animate hint, add integration tests for exit 3/4/5 + projected stop-loss before any A(b) credit.
