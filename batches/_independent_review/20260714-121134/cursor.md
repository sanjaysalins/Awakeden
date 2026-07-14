# Independent review — cursor (OK, 147s)

## Findings (adversarial, codebase-checked)

### 1. A(a) deliverables are promised but do not exist — Wave A(b) is blocked on vapor

The plan makes A(a) tooling an explicit gate for paid work:

> **"Deliverable: shared tooling** (generalized `pipeline/living_light_promote.py` … before/after page builder + backup helper). $0"  
> **"A(b) is BLOCKED until the A(a) tooling exists."**

In the repo today:
- Only piece-local `batches/cluster_02_resurrection/women_first_witnesses_luke245/promote_living_light.py` exists (hard-wired to `fx_pilot_kling_living_light.PILOT`).
- No `pipeline/living_light_promote.py`.
- No `visual/wave_checklist.json` anywhere.
- No shared before/after page builder; `.bak_prelivinglight` is prose only (`STATE.md` shows one manual backup on Women).

The plan treats A(a) as done-in-principle while the chokepoint tooling is still unbuilt. That is a single point of failure for Wave A(b).

---

### 2. Wave A pieces still FAIL the machine bar — authoring scope is large, not a “6-clip probe”

Plan Wave A(a): *"baseline gate FAILs logged per piece → full spec rewrite … → gate PASS."*

Current specs are nowhere near PASS. Example `it_is_finished_john1930`:
- `"cut_ticks": true` — gate requires `cut_ticks:false` (`rollout_gate.py:79-80`)
- No `"motion": "smooth"` (gold master has it; gate line 38-39)
- Overwhelmingly `"tpl": "full"` — likely >60% full-bleed (gate line 42-44)
- No `piece.json` `animate.living_light` section at all (gate lines 93-95)

Same pattern on `crucifixion_foretold_ps2218` (`cut_ticks: true`, all-full beats). Wave A is a **full gold-master rewrite × 3**, not a cheap rate measurement. The plan understates calendar/authoring risk while calling A(b) a re-roll-rate probe.

---

### 3. Stop-loss is at the chokepoint — but only once per invoke, and only for spec’d pieces

Plan claims: *"`run_piece --stage animate` calls `pipeline.rollout_spend.check()` … refuses paid renders (exit 4)"*

`run_piece.py:362-366` does call `rollout_spend_check()` before the render loop — good.

**Gap A — single pre-batch check:** After one passing check, the loop at `run_piece.py:372-397` can render many clips. Headroom of 20cr + 6 clips × 7.5cr = 45cr → batch overshoots cap with no mid-loop re-check.

**Gap B — spec-less bypass:** Gate + stop-loss run only inside:

```348:366:run_piece.py
if (piece_dir / "visual" / "livingpage_short.spec.json").is_file():
    ...
    rollout_spend_check(verbose=False)
```

Pieces without a livingpage spec (e.g. `father_forgive_them` in Wave E, or legacy paths) can still hit `hf_animate` with **no rollout gate and no 485cr stop-loss**.

**Gap C — alternate paid paths still live:** Plan says *"never `_hf_animate_short.py` CLI or `_animate_rerolls.py`"* — true that those bypass rollout gate. `batches/cluster_01_cross/_animate_rerolls.py` still calls `hf_animate` directly with no gate. Nothing in code prevents accidental use.

---

### 4. Disk cross-check over-counts and under-specifies what “485cr” buys

Plan: *"charged at the HIGHER number"* via `disk_clip_count`.

`rollout_spend.disk_clip_count()` (`rollout_spend.py:49-65`) counts **every** `*.mp4` in `visual/clips/` **and** `visual/_fx_pilot/` since `2026-07-14` for rollout episodes — not just living-light clips.

Budget line: *"12 pieces × 2 clips = 24 × 7.5cr = **180cr base**"* — scoped to living-light only.

Mismatch: stop-loss meters **all** Kling mp4s (existing dyncam moves, pilot rolls, re-rolls, promoted + unpromoted `_fx_pilot` copies). A full `run_piece --stage animate` (no `--only`) on a piece with 10–12 `animate.moves` can burn cap far faster than the 180cr model. The plan never **requires** `--only <living_light_slugs>` for rollout renders.

Also: no test covers `disk_clip_count()`; only ledger tally is tested (`test_rollout_spend_tally`).

---

### 5. “21 gate tests green” overclaims coverage

`pipeline/test_rollout_gate.py` has ~21 tests, but the machine bar includes rules with **no dedicated test**, e.g.:
- *"landing beat carries no light"* (`rollout_gate.py:112-113`) — no `test_*` for this
- `disk_clip_count` cross-check — untested
- No integration test that `run_piece.run_animate` returns exit 3/4 on gate/stop-loss breach

Calling the bar *"all fail-closed, tested"* is stronger than what the suite actually locks.

---

### 6. Filmstrip QC is still manual / mismatched to cluster layout

Human checklist item 5: *"filmstrip per new clip via the gold-master ffmpeg-strip workflow, shipped as a shared helper in the A(a) tooling"*

Round-3 fix correctly drops `pipeline/clip_anim_qc.py` for cluster pieces — it only scans `visual/<provider>/[0-9][0-9]_*.mp4` from scene plans (`clip_anim_qc.py:205`), not `visual/clips/<slug>.mp4`. `build_filmstrip()` exists but is **not wired** into `run_piece`, rollout gate, or any cluster workflow. Item 5 is a human step with no enforced artifact or fail-closed hook.

---

### 7. Budget math does not close under stated worst case — “GO at 485cr” conflicts with own forecast

Plan admits:
- Base **247.5cr**
- Worst case **569cr — over the 485 envelope**
- Hoped case **371cr — inside**

User approval is *"GO at 485cr HARD envelope"* while the plan’s own 2.3× re-roll model exceeds it. Mitigation is *"re-quote before Wave B either way"* and scope cuts — but Wave A(b) spend starts before that re-quote, and pilot spend already counts inside 485 (*"zero point: pilot + promotion spend counts INSIDE 485"*). You can breach the hard envelope during the very wave meant to measure the rate.

Per-episode pre-flight (*"`cost summary --episode` … $25/short ceiling"*) is weak here: `hf_animate` checks `check_budget(ep, "short", KLING_USD_PER_CLIP)` per clip (~$0.65). Twelve episodes can each stay under $25 while the **batch** blows past 485cr — exactly the dual-ceiling tension prior panel reviews flagged.

---

### 8. `father_forgive_them` dependency is understated and mis-scoped

Plan Wave E: *"`it_is_finished` refs `../father_forgive_them/.../face_on_cross_fix2.png`"*

At least **six** Wave A–C pieces reference that still (`it_is_finished`, `pierced`, `into_thy_hands`, `thirty_pieces`, `woman_behold`, `watch_one_hour` — all in `piece.json`). Wave E is “scoped separately,” but Waves A–C already depend on an unmigrated asset tree. A greenfield Wave E migration can break multiple in-flight pieces silently.

---

### 9. Human checklist items lack machine enforcement

Items 1–7 in *"Human checklist per piece (recorded as `visual/wave_checklist.json`)"* are entirely advisory:
- **Audio-diff (item 3):** Correct target after round-3 fix (`cli_livingpage._sfx_builder()` at `cli_livingpage.py:47-57`), but diffing spec `"sfx"` beats vs `build_cluster1_sfx.py` PIECES dict is manual; no validator.
- **Fit-gate (item 7):** *"advisory by design — the gold master itself carries 2 accepted warnings, so it cannot hard-block"* — known bad crops can ship on 10 rollout finals.
- **Before/after re-approval:** *"wave-gate user review … IS the re-approval of shipped finals"* — waives `independent_review.py` on deterministic rebuilds while `motion`, grid crops, fx arc, and living-light clips materially change viewer-facing output. That conflicts with the standing enforced-review rule for significant spend-bearing work.

---

### 10. Status vs start condition is internally inconsistent

Header: *"DEGRADED 2/5 — cursor REVISE + claude REVISE … grok/codex/gemini being revived via panel_doctor for round 4"* and *"Wave A starts only on a clean panel verdict for this revision."*

This artifact is explicitly post-round-3 with degraded panel status. It should not be treated as execution-ready even if the user gave a credit envelope GO.

---

### 11. What the plan gets right (for balance)

- `pipeline/rollout_gate.py` matches most stated rules (temp arc, living_light play/dyncam waste, double-lighting).
- `run_piece` path does **not** call `ffmpeg_fallback` on NSFW — only `FAILED` (`run_piece.py:392-397`); the silent downgrade is confined to `_hf_animate_short.py` CLI `main()` (`_hf_animate_short.py:205-207`).
- BytePlus path is real (`run_piece.py:34`, ARK endpoint).
- Wave D ordering fix (fact cards → jobs → `reuse_check` → render gaps) matches `run_piece.reuse_check` at line 103.

Those are real improvements; they do not close the gaps above.

---

VERDICT: REVISE  
TOP FIXES:  
1. Build and land A(a) tooling (`pipeline/living_light_promote.py`, backup helper, before/after page generator, `wave_checklist.json` schema) and add an integration test proving `run_piece --stage animate` returns exit 3/4 on gate/stop-loss breach — before any Wave A(b) credits.  
2. Fix stop-loss semantics: per-clip re-check (or pre-flight `pending × 7.5cr` against headroom), count only attributable living-light/paid slugs (not all `clips/*.mp4`), and mandate `run_piece --stage animate --only <ll_slugs>` for rollout renders.  
3. Reconcile budget with control: either lower the approved envelope, defer Wave A(b) until panel round 4 is clean, or pre-commit scope-cut triggers when forecast uses `max(Wave A rate, 2.3×)` and document the six-piece `father_forgive_them` still dependency as a hard cross-wave invariant before Wave A still work.
