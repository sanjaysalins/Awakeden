# Independent review — grok (OK, 136s)

I'll verify the plan's claims against the real codebase — gates, spend controls, tools, and wave assumptions.Checking the chokepoint wiring and spend/gate implementation against the plan's claims.Verifying remaining risk claims: silent NSFW fallback, disk-count accuracy, piece inventory, and test coverage.Checking disk double-count risk and whether animate without `--only` can overspend.## Independent adversarial review — CORPUS ROLLOUT PLAN v4

Round-3 wiring is real. Several prior FAIL-class claims are now true in code. This is still not a clean GO for paid Wave A(b).

---

### What checks out (so you don't re-litigate dead flags)

- **`pipeline/rollout_gate.py`** matches the machine bar (full-bleed, templates, still uses, adjacent FB, fx %, temp required, cool/warm poles, `motion`/`cut_ticks`, living_light ≥2 + played-not-dyncam, double-lighting, landing lit, slop tokens including `…`).
- **Gate + spend at chokepoint:** `run_piece.run_animate` runs gate on any piece with `livingpage_short.spec.json`, then `rollout_spend.check()`, exit 3/4 — matches lines 16–21 / 97–98.
- **No silent ffmpeg fallback on the `run_piece` path:** `hf_animate` returns `False`; `run_piece` prints `FAILED` and does not call `ffmpeg_fallback`. CLI `main()` still has the silent path — plan correctly bans it (discipline, not enforcement).
- **21 tests** in `pipeline/test_rollout_gate.py` — count claim holds.
- **SFX checklist target** (`cli_livingpage._sfx_builder` / `build_cluster1_sfx.py`) is correct; old `_sfx.py` greps were wrong.
- **`clip_anim_qc` dropped** as cluster QC path — correct; runner is v1 `scene_plan` / `nbp/[0-9][0-9]_*.mp4`.
- **Wave E ref** is real: `it_is_finished` `piece.json` refs `../father_forgive_them/visual/_byteplus/face_on_cross_fix2.png`.
- **BytePlus ARK** at `run_piece.py:34` — gemini round-1 flag stays dead.

---

### Findings (problems that remain)

### 1. Disk cross-check can **over-count** — “unmetered hole fixed” is only half-true  
**Cite:** *"cross-checked against rendered mp4s on disk and charged at the HIGHER number"* / *"Current: 6 clips charged (disk) = 45cr"*

`disk_clip_count()` sums **every** `visual/clips/*.mp4` **and** `visual/_fx_pilot/*.mp4` with mtime ≥ 2026-07-14.

Gold-master path: pilot → `_fx_pilot/*_livinglight.mp4` → `promote_living_light.py` copies into `clips/<slug>.mp4`. Both files exist. **One HF bill can become two disk counts.**

Women already has both:

- `…/_fx_pilot/women_bowed_livinglight.mp4` (+ 2 other pilots)
- `…/clips/women_bowed.mp4` (promoted)

So “6 clips = 45cr” may be **double-count of 3 keepers**, not 6 unique bills. That distorts headroom, forecast, and when exit-4 fires.

Also: disk counts **all** post-cutoff mp4s, not living-light only. Any stale re-animate, touch, or copy bumps the cap.

**Tests:** `test_rollout_spend_tally` only exercises ledger `tally()` — **no test for `disk_clip_count`**.

Limit (c) (billed-but-no-mp4) is still uncovered by disk. Plan admits that; fine. Claiming the unmetered hole is “fixed” oversells a leaky meter.

---

### 2. Stop-loss is **once per `run_animate` call**, not per paid clip  
**Cite:** *"fail-closed AT THE CHOKEPOINT … refuses paid renders (exit 4) when the 485cr cap is reached"*

```339:399:run_piece.py
def run_animate(...):
    ...
    if rollout_spend_check(...): return 4
    ...
    for slug, prompt in animate_prompts(pj).items():
        ...
        ok = hf_animate(...)
```

One green check, then **N** `hf_animate` calls with no recheck. Headroom 50cr + 10 stale slugs × 7.5 = 75cr → can land **past 485** in one invocation.

Parallel agents both seeing “440 headroom” and both spending is also unaddressed (limit (b) excludes reconcile; it does not solve concurrent animate).

---

### 3. A(b) budget assumes 2 clips/piece; **`run_piece --stage animate` defaults to all stale slugs**  
**Cite:** *"Wave A renders: 2 living-light clips/piece (6 total)"* / *"`run_piece --stage animate [--only <slug>]`"*

`animate_prompts` walks **all** `moves` + `living_light`. Without **mandatory** `--only <ll_slug1>,<ll_slug2>`, any hash-stale non-LL clip re-renders and burns the envelope. RESUME already records accidental full animate spend. Plan treats `--only` as optional syntax, not a hard A(b) rule.

---

### 4. A(a) “shared tooling” is mis-aimed and still vapor  
**Cite:** *"generalized `pipeline/living_light_promote.py` from the gold-master script + before/after page builder + backup helper"* / *"filmstrip … shipped as a shared helper"*

- `pipeline/living_light_promote.py` **does not exist**. Only hard-wired  
  `batches/…/women_first_witnesses_luke245/promote_living_light.py` (imports pilot `PILOT`, fixed `LL_TARGETS`).
- A(b) production path is **`run_piece --stage animate` → `clips/{slug}.mp4`**. Promote is for **pilot → copy-in**. Generalizing promote as *the* A(a) deliverable fights the path the plan mandates for spend.
- Filmstrip helper **already exists**: `pipeline.clip_anim_qc.build_filmstrip(mp4, out_dir)` works on any mp4. Plan drops the module, then re-invents “gold-master ffmpeg-strip workflow” instead of reusing that function + a thin cluster wrapper.
- `visual/wave_checklist.json` — no schema, no writer, no example.
- `.bak_prelivinglight` — convention only; no backup helper in repo.

A(b) is **blocked on tooling that is unspecified beyond names**.

---

### 5. Wave A authoring risk is still under-scoped  
**Cite:** A(a) *"full spec rewrite (grid conversion + anchors + …)"* for `it_is_finished`

Current `it_is_finished` spec: **`cut_ticks: true`**, **16/17 beats `tpl: "full"`**, plus `heartbeat`, `punch`, `whip`, `ramp`, `takeover`. Gate will FAIL hard until grids + smooth + living_light exist.

Plan does **not** require:

- baseline `rollout_gate` FAIL dump as a checked-in artifact before rewrite  
- rules for keeping heartbeat / whip / punch when converting full→grid  
- named LL slugs **before** A(a) ends (A(b) still says “names finalized at authoring”)

This is the largest wall-clock and regression surface in the plan. Calling A(a) “$0” is true for API spend; it is **not** a small step.

---

### 6. Wave D de-dup numbers are still soft  
**Cite:** *"empty_tomb ~6 replacement stills → 6 new clips (45cr) + sign_of_jonah ~3 → 3 clips (22.5cr)"*

`empty_tomb` gate-breaker that is clear: **`risen_christ_wounds` ×5** (max uses = 2) → need **≥3** beat reassignments / new stills, not necessarily 6. Other stills sit at exactly 2 (legal). `sign_of_jonah` only shows `risen_christ_wounds` ×2 in-spec — may need **zero** de-dup for that slug.

67.5cr de-dup line is still estimate dressed as derived. Budget cuts at re-quote depend on it.

---

### 7. “One render path” is policy, not control  
**Cite:** *"ALL rollout renders … never the `_hf_animate_short.py` CLI or `_animate_rerolls.py`"*

Both bypassers still exist and still work. `_animate_rerolls.py` is one tab-complete away during QC panic. No shim, warning, or delete. Gate/spend only protect people who obey the plan.

---

### 8. Human checklist is the product gate — and uninstrumented  
Items 1–4, 7 are eye-only. Fit-gate stays advisory (honest). That means a gate-PASS piece can still ship with wrong scale mix, bookend failure, or audio double-hit. Acceptable only if wave-gate **before/after** is real; plan has no command to build that page yet (see #4).

---

### 9. Wound/CU as **first** A(b) roll is the highest NSFW / re-roll risk  
**Cite:** *"first roll = the wound/CU proof"* + forecast *1.5× locks baked in*

`LIVING_LIGHT_BASE` bans blood flow / wound growth — correct locks. Pilot re-roll pain was already on **risen** imagery; cross CU is the HF-hard case. Putting the worst case first is good science, bad envelope if 2.3× is real and A burns re-roll budget before rate is “measured.” Plan’s forecast rule helps **before Wave B**, not if A alone overruns.

---

### 10. Dual ceilings still operator-hostile  
**Cite:** *"`rollout_spend` + `cost summary --episode` pre-flight ($25/short … never silent `override=True`)"*

- Batch: 485cr (`rollout_spend`)  
- Episode: $25 USD (`check_budget` in `hf_animate`)  
- `cost summary` credits column still blind to animate (`est_credits` null) — plan admits this  

Near-ceiling episode still needs a human `override` path that the plan forbids silently — good — but there is no single operator decision surface. Easy to “pass” one meter and blow the other.

---

### Over-engineering / reuse

- **Do not** greenfield a second filmstrip stack; wrap `build_filmstrip`.  
- **Do not** center A(a) on promote-from-pilot unless A(b) explicitly re-adopts the `_fx_pilot` pilot loop (and then fix disk double-count).  
- Machine bar + chokepoint spend are justified. Shared promote of a one-off pilot script is premature if production is cold `run_piece`.

---

### Cost verdict

Base 247.5cr and worst-case 569cr **over 485** are honest. Hope branch 1.5× / 371cr is still hope until A(b) measures **wound CU**, not resurrection glow. Scope cuts at re-quote are the right structure. **Spend controls still have overshoot and over-count bugs** — so “no silent spending through the cap” is not fully earned.

---

### Bottom line

v4 fixed the round-3 structural lies (gate always-on for livingpage specs; spend at `run_animate`; SFX path; clip_anim_qc dropped; render-path ban stated). Remaining failures are **meter integrity**, **batch overshoot**, **default animate scope**, **A(a) tooling design**, and **Wave D arithmetic softness**. Not PASS for Wave A(b). A(a) $0 authoring can proceed after tooling/SOP fixes; paid renders should not.

VERDICT: REVISE  
TOP FIXES:  
1. Fix spend metering: stop double-counting `_fx_pilot` + `clips/`; recheck cap before **each** `hf_animate` (or refuse if remaining headroom < N×7.5 for this invocation); hard-require A(b) `--only` living-light slugs only; add tests for `disk_clip_count`.  
2. Rescope A(a) tooling to the real path: production `run_piece --only` + reuse `clip_anim_qc.build_filmstrip` + real backup/before-after/wave_checklist helpers; treat promote as optional pilot utility, not the main deliverable; write grid-conversion SOP that preserves heartbeat/punch/whip.  
3. Re-derive Wave D from actual gate FAILs (e.g. `risen_christ_wounds` ×5 on empty_tomb), lock exact LL slugs + clip counts in wave_checklist before any re-quote math, and keep B–D blocked until A(b) measured rate exists.
