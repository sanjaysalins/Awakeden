# Independent review — grok (OK, 109s)

I'll verify the plan's claims against the real codebase—gates, spend controls, tools, and wave assumptions—before writing the adversarial review.Checking the claimed round-4 code fixes and whether tooling/tests actually exist.## Review: CORPUS ROLLOUT PLAN v5

Round-4 code fixes are mostly real: gate + spend at `run_animate`, exit codes propagate, mid-loop re-check exists, disk de-dup/rejects test exists, re-roll via parked mp4 → `missing` works. The plan is still not ready to green-light paid work as written.

---

### 1. Spend baseline contradicts itself (forecast is untrusted)

**Cite:** Machine bar: *"Current: 6 clips charged (disk) = 45cr, 440 headroom"*  
**Cite:** Budget v5: *"Zero point… **37.5cr**… Remaining envelope ≈ **447.5cr**"*  
**Cite:** Answered objections: *"Live reading now agrees with the ledger (**5 = 5**)"*

Three incompatible baselines (5 / 6 clips; 37.5 / 45cr; 447.5 / 440 headroom) live in one plan. Budget math is keyed off 447.5; the machine bar is keyed off 440. You cannot re-quote B–D or claim “right at the wall” until one number is authoritative and the other lines are deleted.

---

### 2. Stop-loss still allows a one-clip overshoot

**Cite:** *"refuses paid renders (exit 4) when the 485cr cap is reached"* / *"re-check before EVERY paid clip"*

Code (`pipeline/rollout_spend.py`): breach is `credits >= CAP_CREDITS`.  
At 480cr spent, check returns 0, then one 7.5cr clip lands at 487.5. Mid-loop re-check stops *the next* clip, not the one that crosses the wall.

Fail-closed for a HARD 485 envelope means: refuse if `spent + next_clip > CAP` (or headroom < 7.5), not “stop after breach.”

---

### 3. `--only` is prose, not a control — bare animate is still the default path

**Cite:** *"A(b) invocations MUST use `--only <ll_slugs>`"*  
**Cite:** cli path in plan: *"`run_piece --stage animate [--only <slug>]`"*

`it_is_finished` alone has **12** `animate.moves` and no `living_light` yet. Bare animate will pay for every missing/stale move, not 2 LL clips.

`cli_livingpage.py` still suggests:
`run_piece.py … --stage animate` with **no** `--only`.

Nothing refuses a bare rollout animate. At pilot 2.3× this is how you burn the envelope on non-LL work the forecast never counts.

---

### 4. A(a) tooling is still vapor (correctly blocks A(b) — but underspecified)

**Cite:** *"Deliverable: shared tooling… thin cluster wrapper over… `build_filmstrip()` + backup helper + before/after page builder + `wave_checklist.json` writer"*  
**Cite:** *"A(b) is BLOCKED until the A(a) tooling exists"*

Verified: no shared backup helper, no before/after builder, no `wave_checklist.json` writer/schema file anywhere. Re-aiming away from promote and toward `build_filmstrip` is right — but the plan still has:

- no module paths / CLI commands  
- no acceptance tests  
- schema only *"pass/fail + note + reviewer + date"* for a **7-item** checklist  

Wave-gate re-approval is defined as reviewing before/after pages that do not exist yet. That is a single point of failure dressed as a process.

---

### 5. Worst-case budget is already over remaining — and understates A(b) risk

**Cite:** *"Worst case… **~449–483cr vs 447.5 remaining — right at the wall**"*  
**Cite:** limit (c): failed-but-billed NSFW/502s *"leave neither row nor mp4"*  
**Cite:** A(b) first roll = *"wound/CU proof"* on crucifixion pieces

Even on the optimistic 447.5 baseline, worst case ≥ remaining. Limit (c) is *outside* that number, and A(b) deliberately starts on the highest NSFW surface. “HF balance eyeball at each wave gate” is not a stop-loss; it is hope.

Scope cuts exist but are optional user picks after the fact — not a pre-committed reserve before A(b).

---

### 6. “Per-slug roll cap: 3” is not implemented

**Cite:** *"Per-slug roll cap: 3 attempts, then stop and report (pilot precedent)"*

No counter in `run_animate` / `hf_animate` / `rollout_spend`. A stubborn CU can still eat a wave’s budget unless a human remembers. Pilot already showed this (`risen_christ_seeking` multi-roll).

---

### 7. Bypass paths still live; ban is discipline-only

**Cite:** *"never the `_hf_animate_short.py` CLI or `_animate_rerolls.py`"*  
**Cite:** *"Verified: `run_piece` prints FAILED and substitutes nothing"*

True for the `hf_animate()` import path. False as a system property:

- CLI `main()` still has silent `ffmpeg_fallback`  
- `_animate_rerolls.py` still exists  
- cost ledger can still go dark (`except` → unmetered)  
- `JITB_SKIP_ROLLOUT_GATE=1` still skips the gold-master gate  

Disk cross-check helps under-count; it does not fix unmetered path or silent CLI misuse.

---

### 8. Claimed “tested — 21 gate tests” oversells the risky claims

**Cite:** *"all fail-closed, tested — 21 gate tests green"* / *"now real in code"* for exit 4 + per-clip stop-loss

`pipeline/test_rollout_gate.py` has unit coverage for gate rules, tally, and disk de-dup. **No** test that:

- `run_animate` returns 3/4  
- `main()` propagates those codes to the shell  
- mid-loop stop-loss fires after N successful renders  

Those were the round-4 critical bugs. Unit tests on helpers ≠ integration proof.

---

### 9. Human checklist + fit-gate remain advisory under a “machine bar” brand

**Cite:** items 1–4, 7; *"builder fit-gate warnings… cannot hard-block"*  
**Cite:** *"The wave-gate user review of before/after pages IS the re-approval"*

Machine bar does not check scale variety, Christ full-bleed discipline, audio-diff, or bookend. That’s fine if named as human-only — but then calling the whole system “all fail-closed” is false. Rebuild can change motion, grids, fx, and LL while publish metadata stays green. Without shipped before/after tooling, re-approval is fiction.

---

### 10. Wave D “$0 grid absorbs doubles” understates authoring blast radius

**Cite:** *"most full-bleed doubles are NON-adjacent… fixable by $0 grid conversion"* / *"$15–30cr"*

Baseline dump is real and useful (`risen_christ_wounds` ×5; empty_tomb fullbleed 100%; 8 FB doubles). Grid conversion is **$0 in credits**, not free in wall-clock or risk: `MAX_STILL_USES` counts every use regardless of template, so ×5 still needs reassignment; empty_tomb/sign_of_jonah are full gold-master rewrites, not a still-overuse footnote. 15–30cr for extras is plausible only *after* that rewrite lands gate PASS.

---

### What is actually solid

- Gate rules match `rollout_gate.py` (temp poles, double-lighting, living_light play/dyncam, etc.).  
- Chokepoint wiring in `run_animate` is real.  
- Exit propagation in `main()` is real.  
- Re-roll via park-to-`_rejected/` + leave sha is real in `_clip_state`.  
- Wave D animate → register order is correct.  
- Wave E asset-dependency constraint matches `it_is_finished` → `father_forgive_them` ref.  
- SFX checklist target via `_sfx_builder` / `build_cluster1_sfx.py` is correct.  
- Blocking A(b) on A(a) tooling is the right sequencing.

---

### Bottom line

v5 fixed the round-4 **code lies**. It did not fix **budget arithmetic honesty**, **one-clip overshoot**, **enforced `--only`**, or **tooling acceptance**. A(a) $0 authoring can proceed only after baseline numbers are reconciled and tooling acceptance is concrete. **A(b) paid renders should not.**

VERDICT: REVISE
TOP FIXES:
1. Pick one spend baseline (5 vs 6 clips / 37.5 vs 45cr / 440 vs 447.5), delete the others, and re-run all worst-case math + scope-cut triggers against remaining headroom including limit-(c) NSFW pad for A(b) wound/CU rolls.
2. Make stop-loss refuse when `spent + next_clip > CAP`; enforce A(b)/rollout animate with required `--only <living_light_slugs>` (or refuse bare animate when living_light is set); code the per-slug attempt cap of 3.
3. Ship A(a) tooling with real paths + acceptance tests (filmstrip wrapper over `build_filmstrip`, backup, before/after page, full 7-item `wave_checklist` writer) and add integration tests that `run_piece --stage animate` exits 3/4 on gate/stop-loss — before any paid A(b) credit.
