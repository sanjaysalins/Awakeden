# Independent review — cursor (OK, 131s)

Independent adversarial review of **CORPUS ROLLOUT PLAN v5**, checked against `run_piece.py`, `pipeline/rollout_gate.py`, `pipeline/rollout_spend.py`, `pipeline/clip_anim_qc.py`, `cli_livingpage.py`, `_hf_animate_short.py`, `_animate_rerolls.py`, the baseline gate dump, and ledger/disk layout.

---

## Feasibility vs codebase

**1. A(a) “deliverable” tooling is still mostly plan text, not production code.**

The plan states Wave A(a) ends with: *“thin cluster wrapper over the EXISTING `pipeline.clip_anim_qc.build_filmstrip()` … backup helper + before/after page builder + `wave_checklist.json` writer”* and correctly blocks A(b) on it. In the repo today:

- `build_filmstrip()` exists in `pipeline/clip_anim_qc.py` (lines 69–93).
- There is **no** shared backup helper, **no** before/after page builder, **no** `wave_checklist.json` schema/writer anywhere in Python sources.
- The only promote script is piece-local: `batches/cluster_02_resurrection/women_first_witnesses_luke245/promote_living_light.py` — not a generalized `pipeline/` tool.

Calling this “re-aimed at the production path (round-4 fix)” describes intent, not a landed deliverable. A(b) is blocked for a real reason.

**2. Filmstrip QC reuses the wrong half of `clip_anim_qc`.**

The plan drops full `clip_anim_qc` for cluster pieces (correct — its `run()` expects `visual/scene_plan.json` and `visual/nbp/[0-9][0-9]_*.mp4`, lines 194–205). It keeps only `build_filmstrip()`.

But checklist item 5 still requires *“filmstrip per new clip … rejects parked in `visual/clips/_rejected/`”* with no specified **living-light Vision rubric**. `review_clip()` in `clip_anim_qc.py` is written for Baroque gallery-tour shorts (lines 97–100), not frozen-figure / dry-wound / expression-lock failures that drove the Women pilot. A filmstrip without a matching rubric is a JPEG factory, not QC.

**3. “One render path, no silent fallback” is policy, not enforcement.**

The claim *“ALL rollout renders … go through `run_piece --stage animate` — never the `_hf_animate_short.py` CLI or `_animate_rerolls.py`”* is accurate about intent, but:

- `batches/cluster_01_cross/_animate_rerolls.py` still calls `hf_animate` directly with no rollout gate or stop-loss (lines 10–34).
- `_hf_animate_short.py` CLI still auto-substitutes ffmpeg on HF block (lines 205–207); `run_piece` does not (lines 402–407) — good — but nothing **prevents** someone from running the bypass scripts.

Discipline-only controls are a single human mistake away from breaking the living-light slot guarantee the plan relies on.

**4. `cli_livingpage` undermines the `--only` guard.**

Plan: *“A(b) invocations MUST use `--only <ll_slugs>` — a bare `--stage animate` re-renders every hash-stale clip.”*

`cli_livingpage.detect()` still advertises bare animate with no rollout awareness and no `--only`:

```127:127:cli_livingpage.py
                          f"{PY} run_piece.py {q} --stage animate   [PAID ~${len(pending) * 0.65:.2f} Kling]"))
```

It also has no rollout-gate or stop-loss step. The resumable entry point can burn envelope on stale camera clips while the plan treats `--only` as mandatory.

---

## Hidden risks / false assumptions

**5. Internal budget contradiction (37.5cr vs 45cr).**

Same document, two numbers:

- Stop-loss section: *“Current: 6 clips charged (disk) = 45cr, 440 headroom.”*
- Budget v5: *“Zero point: rollout spend to date = **37.5cr**”* → *“Remaining envelope ≈ **447.5cr**.”*

Those cannot both be true (5 clips vs 6). Worst-case math (*“~449–483cr vs 447.5 remaining — right at the wall”*) sits on the 447.5 figure. If the live number is 45cr / 440 headroom, worst case is already **over** cap before limit (c) (502/NSFW billed-no-mp4). Forecast headroom is not trustworthy until one number is canonical and automated.

**6. The “Women spend is separate from rollout” answer conflicts with `rollout_spend.py`.**

Plan answers gemini: July 12–13 Women production was *“approved and reconciled separately”* and *“485 envelope covers ROLLOUT work, which began 2026-07-14.”*

Code includes Women in the rollout episode set explicitly as *“gold master incl. pilot rolls”*:

```21:22:pipeline/rollout_spend.py
ROLLOUT_EPISODES = {
    "women_first_witnesses_luke245",           # gold master incl. pilot rolls
```

Ledger rows on **2026-07-14** for `women_first_witnesses_luke245` clips exist and **do** satisfy `ts >= ROLLOUT_START`. Disk cross-check also scans `cluster_02_*` and `_fx_pilot/**/*.mp4`. The narrative zero-point definition and the metering code disagree. Either Women post-7/14 pilot rolls belong in the cap (and the prose is wrong) or the code must exclude them (and current 37.5/45cr is wrong).

**7. Stop-loss is animate-only; still spend is uncapped against 485cr.**

Plan: *“BytePlus stills separate USD”* and Wave D *“~15–30cr + ~$0.15 BytePlus.”*

`run_stills()` uses `pipeline.cost.check_budget()` per episode (~$25/short ceiling, line 249) but **never** calls `rollout_spend.check()`. Wave D still reassignments, Wave A grid conversions that need new plates, and any `--stage stills --render` can spend USD in parallel with the credit cap with no unified chokepoint. Limit (a) (*“cost summary credits can't see animate rows”*) is acknowledged; there is no compensating still-side rollout ledger tie-in.

**8. Limit (c) remains a manual, unbudgeted leak at the worst point.**

Plan admits: *“failed-but-BILLED rolls (502s, NSFW blocks) leave neither row nor mp4 — HF balance eyeball at each wave gate covers them.”*

Worst-case forecast already brushes the wall; crucifixion imagery explicitly flags NSFW-block risk. Eyeball reconciliation is not fail-closed and is exactly where the pilot burned surprise credits. The plan names the hole but does not size it into the stop-loss math.

**9. Wave E asset constraint is understated — it binds Wave A today.**

Plan scopes Wave E for `father_forgive_them` but notes `it_is_finished` refs `face_on_cross_fix2.png`. **Six** cluster pieces already reference that path in `piece.json` (`it_is_finished`, `pierced`, `into_thy_hands`, `woman_behold`, `watch_one_hour`, `thirty_pieces`). Wave E migration is not a future edge case; it is a **present** cross-piece dependency during A(a) still work and any Wave E path move breaks multiple in-scope pieces silently.

**10. `JITB_SKIP_ROLLOUT_GATE=1` is a loud but real fail-open.**

Plan: *“loud, discouraged escape for surgical repairs only.”* Code honors it ( `run_piece.py` lines 351–363). Any “surgical” use during A(a) spec migration bypasses both gate and the living-light/dyncam checks the plan treats as non-negotiable.

---

## Over-engineering / premature spend

**11. Wave A(a) scope is correctly identified as the wall-clock bottleneck — but still under-specified.**

*“SPEC AUTHORING (a full gold-master rewrite ×3, NOT a light touch)”* matches baseline FAILs (all three Wave A pieces fail on motion, fullbleed %, fx arc, cut_ticks, living_light, landing light — see `baseline_gate_fails_20260714.txt` lines 1–26).

What is **not** in repo: the promised *“grid conversion (SOP: Christ singles stay full; convert crowd/object/multi-figure beats; preserve heartbeat/punch/whip choreography)”*. That SOP is the actual authoring work; without it, A(a) is “rewrite until gate passes” with no repeatable procedure. High risk of churn or accidental choreography loss across three pieces.

**12. Per-slug roll cap is prose-only.**

*“Per-slug roll cap: 3 attempts, then stop and report”* — not enforced in `run_piece`, `rollout_spend`, or any wrapper. A stubborn wound CU can still eat a wave; only human discipline stops it.

---

## Missing steps / verification gaps

**13. Exit-code propagation is fixed in code but not regression-tested at the integration layer.**

Plan claims round-4 fix: *“`main()` now propagates stage return codes.”* Confirmed in `run_piece.py` lines 791–794. But there is **no** pytest covering `run_piece --stage animate` returning 3 (gate) or 4 (stop-loss). Unit tests cover `rollout_gate` and `rollout_spend` in isolation (`pipeline/test_rollout_gate.py`). Automation could regress and still show “314 passed.”

**14. Human checklist items 1–4 and 7 are unenforceable; item 3’s discovery is fragile.**

Checklist: scale variety, bookends, audio-diff via `_sfx_builder()`, fit-gate warnings *“advisory by design.”*

- Nothing in `rollout_gate` checks scale mix or hook-open/Christ-close bookends.
- `_sfx_builder()` does substring search across `sfx_pilots/build_*.py` file **text** (lines 47–56), not structured lookup into `PIECES` dict keys — false positives/ordering bugs are possible.
- Fit-gate cannot hard-block because *“the gold master itself carries 2 accepted warnings.”* A gate-PASS piece can still ship wrong scale, wrong bookends, or double-hit SFX; the plan leans on before/after pages that **do not exist yet**.

**15. Re-roll mechanic has a subtle stale/unhashed blind spot.**

Parked reject → missing → re-render: fixed (`_clip_state`, lines 326–329).

But pre-hash **unhashed** clips still skip with *“run --stage hash-backfill to bind it”* (lines 384–387). During migration, old camera clips can remain “unhashed” and immune to staleness while living-light slugs get new hashes — inconsistent state the plan does not mention.

**16. Register ordering fix is real but `--stage all` is still a footgun.**

Wave D fix (*“register scans `clips/` … must FOLLOW animate”*) matches `register_rows()` (lines 718–722). Per-piece flow says the right order. But `run_piece --stage all` runs `stills → animate → score → register` — if someone adds `--render` to stills in the same invocation during Wave D, ordering and spend profile differ from the documented per-piece checklist.

---

## Reuse

**17. Good reuse calls that are partially implemented.**

- Reusing `build_filmstrip()` instead of reinventing: correct direction.
- Demoting promote to pilot utility, production via `run_piece --only`: matches `women_first_witnesses_luke245/promote_living_light.py` being piece-local.
- `reuse_check` before still renders: exists in `run_piece.py` (lines 103–120, 258–259).

**18. Bad reuse gap: no shared promote/backup/checklist abstraction.**

Women already solved promote once; plan asks for a second generalized layer without extracting the working script. That is duplicate design work unless A(a) explicitly starts from `promote_living_light.py` as the template.

---

## Cost / spend justification

**19. Forecast discipline improved but still brittle.**

Positives: B–D blocked on re-quote; A(b) as measured rate probe; scope cuts listed if forecast > remaining.

Problems:

- Competing zero points (finding #5).
- Women/gold-master inclusion ambiguity (finding #6).
- Worst case ~449–483cr against 447.5 **before** limit (c) and still USD.
- *“Hoped ~1.5×: ~295–315cr”* is not a plan, it is hope; B–D forecast rule (*“max(Wave A measured, 2.3×)”*) is sane but Wave A measured rate does not exist until A(b), while A(a) authoring is large.

485cr HARD envelope is defensible **if** A(b) truly measures re-roll rate before B–D and re-quote is enforced. Current numbers do not yet support “proceed with confidence.”

---

## What the plan gets right (for balance)

- Deterministic `rollout_gate` matches gold-master bar closely; baseline dump is checked in.
- Gate conditioned on spec presence closes the mid-migration bypass ( `run_piece.py` 352–361).
- Stop-loss at animate chokepoint with per-clip re-check (lines 366–370, 398–401) is real, not a wave-gate script fiction.
- Disk dedup including `_rejected/` is implemented and unit-tested.
- Wave split A(a)/A(b), `--only` for living-light rolls, and Wave D ordering (fact cards → reuse → gaps → animate → register) are structurally sound.
- Blocking paid renders until panel clean verdict on this revision is appropriate.

---

VERDICT: REVISE  
TOP FIXES:  
1. **Land A(a) tooling before any A(b) credits** — shared backup (`.bak_prelivinglight`), before/after page generator, `wave_checklist.json` writer, and a living-light filmstrip rubric (not just `build_filmstrip()`); extract from `women_first_witnesses_luke245/promote_living_light.py` rather than redesigning.  
2. **Reconcile budget zero-point in code and prose** — pick one live tally (37.5 vs 45cr), decide explicitly whether Women 2026-07-14 pilot rolls count toward 485cr, and bake limit (c) billed-no-mp4 into forecast or a hard HF-balance gate before each wave.  
3. **Close bypass and resumable-path holes** — hard-deprecate or gate-wrap `_animate_rerolls.py` / direct `_hf_animate_short` CLI; update `cli_livingpage` to require `--only` for living-light animate and surface rollout gate/stop-loss; add integration tests for exit codes 3/4.
