# Independent review — cursor (OK, 98s)

## Independent adversarial review — CORPUS ROLLOUT PLAN v5

### 1. A(a) deliverables are still the critical path — and mostly do not exist

The plan correctly blocks A(b) on A(a) tooling:

> **"A(b) is BLOCKED until the A(a) tooling exists."**

and lists:

> **"thin cluster wrapper over the EXISTING `pipeline.clip_anim_qc.build_filmstrip()` … backup helper + before/after page builder + `wave_checklist.json` writer"**

Verified in repo: `build_filmstrip()` exists in `pipeline/clip_anim_qc.py`, but there is **no** backup helper, **no** before/after page builder, **no** `wave_checklist.json` schema/writer, and **no** shared cluster wrapper module. The only related script is a piece-local pilot: `batches/cluster_02_resurrection/women_first_witnesses_luke245/promote_living_light.py`.

Wave-gate re-approval is defined as:

> **"The wave-gate user review of before/after pages IS the re-approval of shipped finals"**

That step cannot run yet. Calling v5 "ready for Wave A(b) on a clean panel verdict" overstates readiness: the **largest wall-clock block** (A(a) gold-master rewrites ×3) plus its **blocking tooling** are still ahead.

---

### 2. "All fail-closed" is overstated — half the quality bar is honor-system

The machine bar section opens with:

> **"Machine bar (all fail-closed, tested — 21 gate tests green)"**

But the human checklist explicitly admits advisory-only enforcement:

> **"builder fit-gate warnings reviewed and dispositioned by eye (advisory by design — the gold master itself carries 2 accepted warnings, so it cannot hard-block)"**

Items 1–4 (scale variety, grid discipline, audio-diff, hook-open/Christ-close bookend) are **not** in `rollout_gate.py`. A piece can PASS the gate and still ship wrong scale mix, wrong bookends, SFX double-hits, or bad living-light *content* (filmstrip QC is human-only). The plan leans on tooling that does not exist (#1).

---

### 3. Chokepoint wiring exists — but lacks integration tests the plan implies

`run_piece.py` does gate (exit 3), stop-loss (exit 4), and bulk guard (exit 5), and `main()` propagates non-zero return codes (lines 805–808). `pipeline/test_rollout_gate.py` has **21** unit tests for gate/spend math.

**Gap:** there are **no** `test_run_piece.py` tests proving `run_piece --stage animate` actually exits 3/4/5 on real rollout pieces. The plan's answered objection *"codex exit 4 never reaches the shell"* is fixed in code, but **not regression-locked**. A refactor could re-swallow refusals without CI catching it.

---

### 4. "One render path, no silent fallback" is policy, not enforcement

The plan states:

> **"ALL rollout renders and re-rolls go through `run_piece --stage animate [--only <slug>]` — never the `_hf_animate_short.py` CLI or `_animate_rerolls.py`"**

Those bypass scripts **still exist and work**:
- `_hf_animate_short.py` (CLI `main()` still does NSFW → ffmpeg fallback)
- `batches/cluster_01_cross/_animate_rerolls.py`
- `sfx_pilots/fx_pilot_kling_living_light.py` (imports `hf_animate` directly)

`run_piece` → `hf_animate()` correctly returns `False` on HF block (no ffmpeg substitute), but **nothing prevents** a tired operator from using the old CLI and silently parking a `$0` ffmpeg clip in a living-light slot — exactly the failure mode the plan names. Discipline-only controls are a single point of failure.

---

### 5. `cli_livingpage` contradicts the bulk guard

Plan:

> **"A(b) invocations MUST use `--only <ll_slugs>`"**

But `cli_livingpage.py` line 127 prints the next animate command as:

```python
f"{PY} run_piece.py {q} --stage animate   [PAID ...]"
```

— **no `--only`**. For post-rewrite pieces with many stale clips, that command hits BULK GUARD (exit 5). The primary resumable entry point steers operators toward the failure mode the plan forbids.

---

### 6. Wave E cross-piece dependency is understated — affects Waves A–D now

The plan scopes Wave E and warns:

> **`it_is_finished` refs `../father_forgive_them/visual/_byteplus/face_on_cross_fix2.png`**

In repo, **six** in-scope pieces reference that path (`it_is_finished`, `pierced`, `into_thy_hands`, `woman_behold`, `watch_one_hour`, `thirty_pieces`). This is not a future Wave E edge case; any still re-render, path move, or Wave E migration breaks multiple rollout pieces **during A(a)**. The plan names one ref and treats the rest as out-of-scope fiction.

---

### 7. Budget math is honest — and still leaves almost zero margin

The plan admits:

> **"Worst case (pilot 2.3×/keeper): ~449–483cr vs 447.5 remaining — right at the wall"**

and documents stop-loss holes:

> **"(c) failed-but-BILLED rolls (502s, NSFW blocks) leave neither row nor mp4 — HF balance eyeball at each wave gate covers them"**

So the fail-closed meter **cannot** see a material spend class; recovery is manual eyeball. Combined with `hf_animate` proceeding **unmetered** if `pipeline.cost` errors (acknowledged in plan + code at `_hf_animate_short.py:135–136`), the 485cr envelope is a **soft** ceiling dressed as hard. Forecast rule (*"B–D forecast at max(Wave A measured, 2.3×)"*) is prudent, but Wave C/D have no **"RE-QUOTE FIRST"** row — only Wave B does — so C/D could proceed on stale math.

---

### 8. A(a) authoring scope is enormous with no executable SOP

Wave A(a):

> **"SPEC AUTHORING (a full gold-master rewrite ×3, NOT a light touch — panel is right that this is the biggest wall-clock block)"**

with:

> **"grid conversion (SOP: Christ singles stay full; convert crowd/object/multi-figure beats; preserve each piece's heartbeat/punch/whip choreography)"**

Baseline dump shows all 12 pieces FAIL on motion, fx arc, living_light, cut_ticks, etc. — e.g. `it_is_finished` at **94% full-bleed**, **0% fx**, **0 living_light**. There is **no checked-in grid-conversion SOP or script**; only deterministic gate rules after the fact. Preserving per-piece "heartbeat/punch/whip" is entirely manual taste with no verification step beyond eyeball + advisory fit-gate.

---

### 9. Reuse discipline for stills is stated — not wired into waves A–C workflow

Plan:

> **"Reuse discipline applies to ANY still work in ANY wave (not only D): fact cards → author jobs → `reuse_check` → render only the gaps"**

`run_piece.reuse_check` exists, but waves A–C are framed as spec upgrade + living-light Kling rolls, not still-gap rendering. Wave D gets the explicit ordering fix (*"animate → register"*). No per-wave command checklist enforces reuse for A–C still touches during grid conversion (which **will** touch still assignments).

---

### 10. Escape hatches undermine "fail-closed"

Two loud overrides remain first-class:
- `JITB_SKIP_ROLLOUT_GATE=1` — bypasses gate entirely
- `JITB_ALLOW_BULK_ANIMATE=1` — bypasses bulk guard

For a plan that markets chokepoint discipline, these are unlogged, un-audited env toggles. One surgical repair becomes six.

---

### 11. Minor code smell in the re-roll fix

`run_piece._clip_state()` has an early `return "missing"` at lines 326–329 **before** the function docstring and size check — dead/unreachable logic below it. Suggests the re-roll fix landed quickly; not a plan defect, but weakens confidence in "round-4 fix — now real in code" without integration tests.

---

### What the plan gets right (so this is not FAIL)

- `rollout_gate.py` rules match stated gold-master bar (temp arc, living_light played-not-dyncam, double-lighting, duration pin).
- `rollout_spend.py` disk cross-check + projected breach + per-clip re-check are real improvements.
- Baseline FAIL artifact exists (`batches/_rollout/baseline_gate_fails_20260714.txt`).
- Wave D ordering fix (animate → register) is correct.
- Budget v5 zero-point / remaining-envelope language is internally consistent.
- `hf_animate()` via `run_piece` does not ffmpeg-substitute on NSFW (unlike the standalone CLI).

---

VERDICT: REVISE
TOP FIXES:
1. **Land A(a) tooling with acceptance tests before any A(b) credit** — shared backup (`.bak_prelivinglight`), before/after page generator, `wave_checklist.json` schema/writer, and a cluster filmstrip wrapper over `build_filmstrip()` (extract from `promote_living_light.py`, don't redesign).
2. **Close enforcement gaps** — add `test_run_piece` integration tests for exit 3/4/5; fix `cli_livingpage` to suggest `--only <ll_slugs>`; block or hard-warn direct `_hf_animate_short` / `_animate_rerolls` on rollout episode paths.
3. **Fix dependency and budget honesty** — document all **six** `face_on_cross_fix2.png` dependents (promote to image_library or pin path now); require re-quote before **every** paid wave (not just B); treat billed-but-failed clips as a ledger row or explicit cap deduction, not eyeball-only.
