# Independent review — grok (OK, 118s)

I'll verify the plan's claims against the actual codebase and tooling before judging.## Plan review (adversarial)

v2 fixed the panel’s big items (re-quote after Wave A, double-lighting / arc / ≥2 LL, human checklist, FFT out of main waves). Those parts match the repo. The remaining holes are real and spend-bearing.

### 1. “HARD STOP-LOSS: 485cr … ledger-checked” is not true in this codebase

**Claim (Budget):** *“HARD STOP-LOSS: 485cr cumulative (ledger-checked at every wave gate)”*

**Reality:** `_hf_animate_short.hf_animate` logs Kling as:

- `est_usd=KLING_USD_PER_CLIP` ($0.65)
- `est_only=True`
- **`est_credits` / `actual_credits` both null**

So `python -m pipeline.cost summary` **cannot** sum HF credits for animate. The credits column for those rows is effectively 0. The only real credit number on the pilot day is a **reconcile** row (`actual_credits: 80.0` for `women_first_witnesses_luke245` on 2026-07-14) — higher than the plan’s “~52.5cr pilot.”

What *does* exist is per-episode **USD** `check_budget(..., "short", ...)` at $25/short — a different unit and scope. Thirteen pieces can each stay under $25 and still burn through 485cr.

**This is a false control.** Stop-loss must use `hf account transactions` / `pipeline.cost reconcile` / balance delta, or fix ledger to write real credits.

### 2. Budget still mixes units and under-counts cascade spend

| Claim | Problem |
|---|---|
| *“24 × 7.5cr = 180cr”* | Only counts living-light. Ignores still-hash invalidation re-animates. |
| *“Wave D stills/clips ≈ 110cr”* | BytePlus stills are **USD** (`SEEDREAM_USD_PER_IMG = 0.05`), not HF cr. |
| *“~525cr worst case”* | Unclear if it includes the pilot’s ~52.5–80cr already spent against the same 485 envelope. |

**Wave D is the landmine:** `empty_tomb` already has `risen_christ_wounds` on **5 beats**. Gate `MAX_STILL_USES = 2` forces de-dup. New stills → new `.src.sha` → **all** clips for those stills go stale → paid re-animate of the **whole move set**, not “2 clips/piece.” That cascade is not in the base 24-clip model.

### 3. “$0 spec upgrade” undersells the real Wave A job

**Per piece flow:** *“(1) $0 spec upgrade → rollout_gate PASS → …”*

Wave A’s first target `it_is_finished` is essentially a classic full-bleed cut: **no** top-level `"motion": "smooth"`, **~100% `tpl: "full"`**, **no `fx` arc**, **no `animate.living_light`**. Getting under ≤60% full-bleed + ≥3 templates is not a light edit — it’s a full re-author of layout/anchors.

Worse, **human checklist #2** (*“Christ/single heroes stay full-bleed”*) fights **machine gate ≤60% full-bleed** on Cross pieces that are Christ-heavy. Without a named SOP (which beats become grids, which multi-figure stills exist, `panel_fit` anchors), Wave A will thrash on authoring risk, not measure re-roll rate.

Also missing: which **two slugs** get living-light on each Wave A piece, and which one is the “Christ-CU/wound proof.” Pilot’s dry-wound lock came from `risen_christ_seeking` re-rolls; Cross wound CUs are a different failure mode — rate measured there may not transfer cleanly to Waves B–D.

### 4. Gate wiring is real but narrower than the sentence sells

**Claim:** *“`run_piece --stage animate` refuses paid renders on any living-light piece until the gate passes”*

**True** when `animate.living_light` is non-empty (`run_piece.py` ~343–353).

**Gaps:**
- Empty `living_light` → gate **skipped**. Classic paid animate still runs.
- `cli_livingpage` has **no** rollout-gate step; it only surfaces pending animate cost.
- Stills stage is not gated by rollout_gate (fine if no new stills on A–C; bad if someone “fixes” crops with paid stills mid-wave).

### 5. Missing procedural tools the plan pretends exist as steps

| Plan step | Repo reality |
|---|---|
| *“BEFORE/AFTER compare page built per piece”* | No named builder for prelivinglight compare pages (pilot has ad-hoc `compare.html` under `_fx_pilot/`). |
| *“Backup … `.bak_prelivinglight`”* | Convention only — no scripted backup/restore. |
| *promote / author living_light* | `promote_living_light.py` exists **only** on the gold master; Wave A path is hand-edit `piece.json` (error-prone). |
| *reuse_check FIRST* | Only called out for Wave D; good that `run_piece.reuse_check` exists — but A–C stills changes (if any) should use it too. |
| *filmstrip QC* | Process discipline, not automated; OK if owned, but no path/tool named per piece. |

### 6. SFX double-audio risk is named, not operationalized

Checklist #3 correctly notes spec beat `sfx` vs `sfx_pilots` bed as separate systems. There is **no** verification step (diff / play / gate) in the per-piece flow after rebuild. On already-shipped Cross finals, doubled sacred accents is a silent quality regression.

### 7. Phase 0 “committed … BEFORE Wave A” is still a claim, not a gate

**Answered objections:** *“Phase 0 pinned: … committed to git BEFORE Wave A”*

That is a precondition sentence, not a verified DoD. Prior panel said gate files were untracked; RESUME still had related work “UNCOMMITTED.” Plan should treat **git pin + green `test_rollout_gate`** as a hard Wave A entry check with evidence, not prose.

### 8. What is actually solid (so this is REVISE, not FAIL)

- `pipeline/rollout_gate.py` now matches the Goal bullets it claims (full-bleed, templates, still-use, adjacent FB, fx %, cool pole ≥7000K, landing warmest ≤5500K, `…` in SLOP, ≥2 living_light, play/dyncam waste, double-lighting, landing light).
- Wiring into `run_piece` animate is real code, not fantasy.
- Wave A as rate-measurement + re-quote before B is the right control if Wave A stays small.
- FFT greenfield split is correct (`father_forgive_them` is mocomic, not livingpage upgrade).
- BytePlus stills path claim is correct (`run_piece.py` `BASE_URL` / `_bp()`); the prior gemini objection was wrong.
- Reuse of `run_piece` / `cli_livingpage` / `_hf_animate_short` (not inventing a second animate path) is right.

### 9. Cost justification

Spend on living-light is justified **after** a measured rate — the plan says that. It is **not** justified to treat 485cr as controlled while the ledger cannot see credits, or to roll Wave D de-dup under a “2 clips/piece” model. Fix the measurement first; then the envelope may still be fine.

---

VERDICT: REVISE  
TOP FIXES:  
1. Make the 485cr stop-loss real: record/reconcile **actual HF credits** (transactions/balance), define whether pilot spend counts, and check cumulative cr at every wave gate — do not rely on `cost summary` as written today.  
2. Re-budget for **still-hash cascade** (esp. Wave D `risen_christ_wounds` 5×): de-dup stills can force full clip re-renders, not 2 LL clips/piece; separate BytePlus USD from HF cr.  
3. Write a Wave A **authoring SOP** before spend: baseline `rollout_gate` FAILs per piece, named LL slug targets (incl. wound CU proof), grid vs full-bleed rules for Christ singles, backup + before/after tooling, then measure re-roll rate.
