# Independent review — grok (OK, 190s)

I'll read the full plan and cross-check its claims against the real codebase.Continuing the full plan and verifying the riskiest claims against the repo.# Independent adversarial review — Seed of the Woman LONG spread plan

Stance: this is a *revision* of a prior REVISE panel run, not a blank slate. Several prior fixes are real (`hunt_and_lock` now exists; landing no longer invents `tear_hole`; naming page dropped non-tools; timing honesty + staged build order; Kling/Seedance recount). That does **not** make this plan build-ready. Contradictions, incomplete wiring, and content-timing risk remain.

---

## Feasibility vs real codebase

### 1. Plan-complete / code-incomplete (blocking)

The plan presents a “FULL PLAN AUTHORED” 71-spread table and staged stills order. Executable code still stops at the 5-spread POC:

- `C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_living_sketchbook\seed_of_the_woman\_devices.py` still says remaining spreads are “to be added”; `VERSE_CARDS` only has `s03_verse_card`; `DEVICE_ASSIGNMENTS` only `s01` + `s04`.
- `_s2_stills.py` / `_s4_animate.py` only cover spreads 1–5 (“extend … as the full plan is authored”).
- `_s6_assemble.py`’s `SEGMENT_BUILDERS` has five entries while `_spread_table.py` already lists 71.

A Sonnet “execution pass” cannot build s6–71 from this document alone without inventing device-table rows, builders, lettering overlays, and segment code. That is the same Day-of-Atonement failure class SKILL §8b.4 exists to prevent: blank device entries discovered late.

### 2. Self-contradiction on lettering tools (still live)

§4 correctly revises s34–36 off “Ink Stamp / Typeset” after the prior panel. **§3 still says the opposite:**

> “t20-24 get the Typeset pressed-line register precisely because Scribed Ink cannot letter 46 glyphs in 2.6s”

So the plan both rejects Typeset as non-existent and still uses Typeset as pacing rationale. That is not residual polish — it is two incompatible designs in one artifact. An executor will not know which is law.

### 3. PLAN vs PREFLIGHT disagree on Golgotha reuse

§5 of the plan **rejects** `bronze_serpent_long\stills\s44_shadow_cross.png` as “doctrinally too risky.”  
`_PREFLIGHT.md` E1 still **lists that same path as a reuse-check candidate**. The plan claims “matching pre-designs are in `_PREFLIGHT.md`.” They are not matched. Dual source of truth = wrong still can still be pulled mid-batch.

### 4. Thread Device oversold for this film’s spine

`panel_animator/thread_device.py` really has `make_thread_layer`, `thread_opacity`, `thread_swell`. Proven production use was one climax reprise on Day of Atonement, not ten independent behaviors.

This plan puts the thread on **~10 spreads** (s21/22/25/28/37/45/62/63/64/66) with still-baked strokes, fade-ins, swells, “gleam along the arc,” and “thread emerging FROM … paper fibers.” Those are composition + compositor contracts, not free library calls. There is still **no thread eye-check step** in §7 open questions and no single shared implementation file named for this episode.

### 5. Several “$0 device” rows are not modules

Named as if they are plug-ins:

| Claim | Reality |
|---|---|
| s27 “`$0 drawn-line reveal`” | No shared module; PREFLIGHT only says “thread-code family” |
| s9 gold-fleck breathe, s55 shadow-sweep, s59 dual-glow, s40 “spotlight shift” | Bespoke, unbuilt, “Fable pre-designed” only |
| s23/s40/s60 “grain-boil” | Technique inside assemble paths, not a stand-alone scheduled device API for this episode |
| Grand-Text / Illuminated Rubric live motion | Static lettering patterns exist; episode-local live-write + per-line arrival still has to be **wired** into `_devices.py` / builders (currently empty for 12 lettered spreads) |

`hunt_and_lock` **is** fixed relative to the last panel (`panel_animator/hunt_and_lock.py` exists; test clip under `_device_tests/`). That one prior FAIL is no longer a hard blocker. The rest of the $0 claim surface is still soft.

### 6. s04 table vs device table still drift

Spread table: s4 = “real clip — Seedance.”  
`_devices.py`: `s04_god_walking` → `breath_synced_halo`.  
Built artifact: Seedance clip exists. Cost, motion_lint, and `_layer_check` will disagree until every row is reconciled. Promoting the full plan without fixing this known drift means the same class of bug will spread to 66 new rows.

### 7. Governing skill still DRAFT

`.claude/skills/living-sketchbook/SKILL.md` line 4/14: **Status: DRAFT**, not panel-locked. STATUS line promotes this to a “real episode.” Feasible as another long sketchbook build; **not** as a locked production standard. Plan never flags that risk.

---

## Hidden risks / false assumptions

### 8. s1–5 vs full-file timing is worse than the “0.8s breathe” story

Plan Timing seam note: only s5 end `33.03 → 33.80`; “no rework.”

Real `_turn_boundaries.json`:

- Turn 1 (scripture Gen 3:8): **12.583–24.795** vs table s3 **11.9–24.0**
- Turn 2 (narrator “God comes looking…”): **24.856–32.476** vs s4 **24.0–30.7**
- Turn 3 (god **“Where art thou?”**): **33.18–33.764** vs s5 **30.7–33.0**

So s5 is designed as the landing on “Where art thou?” **before that line is spoken** on the full file. Extending the hold by 0.8s does **not** put the words on the right picture. That is a content-sync bug, not a breath tweak. Spreads 1–5 were timed to a 33s excerpt; they were not re-cut against the full narration.

### 9. Sub-turn estimates are admitted, still under-scoped as a build gate

Honesty paragraph is good: turn 27 real clauses ≈ 6.0 / 6.3 / 11.3 / 13.3 vs plan 7.7 / 8.0 / 9.5 / 11.8; “may need re-drawing”; remaining ~15 multi-spread turns “unexamined.”

Then staged step 0 says alignment “does not block s06/s16/s51.” True for those three on real turn boundaries — **false** as a go/no-go for the film. The densest argument block (s39–42) and the climax chain (s54–59, including TIMING-FLAG s56) sit on confirmed or unexamined estimate seams. Approving spend “after step 0 for priority turns only” can still buy stills whose beats sit on the wrong words.

### 10. Serpent multi-pose is the real identity SPOF

§5 multi-pose lock + render-order fix for **Jesus** (s51 first) is correct and better than the last draft.

Serpent: **~18 appearances**, branch / belly / shadow / shed-skin / coil / heels — **one** new `serpent_ref.png`, no multi-pose chaining, no “approve pose A before pose B” beyond “s06 first.” DoA’s multi-pose lesson is applied to the lesser-count figure and not the highest-count figure. One bad serpent pose cascades more re-rolls than one bad Jesus pose.

### 11. Study-copy letterforms are load-bearing and unanchored

s26/40/46/47/60/66: “same overlay params/seed,” desk “re-dressed per spread,” KJV **“it shall bruise thy head”** (never “he”). That is face-drift class for doctrine text with **no** letterform still/mask anchor. “$0 prop” is an assumption, not a gate.

### 12. Acting spreads are legal but extreme

SKILL allows 1–2 designed acting spreads. Plan uses them (s6 blame circle; s30 annunciation). s6 is the worst possible first acting beat: Adam + Eve + **first serpent** + arm extend + turn. Staged order (serpent anchor → s06 QC) is necessary, not sufficient. Failure mode is not “tweak timing” — it is re-prompt / re-still / re-Kling on the identity root of ~17 later frames.

### 13. s34–36 naming page is still an unvalidated exception stack

User-open-question is correct. But three lettered adjacent beats + one accumulating page + mid-span narrator lead-ins on estimated seams + empty `VERSE_CARDS` = compositor risk the deterministic “never two lettered adjacent” rule was invented to avoid. Approving the exception without a one-page prototype is premature.

---

## Over-engineering / premature scale

### 14. Full lock before proof on the hard beats

5-spread POC (~$4) validated process gates, not:

- serpent identity,
- thread as film spine,
- naming-page accumulation,
- wash-creep Eden→cross pair,
- Golgotha darkness chain,
- risen Christ s71,
- 12 lettered surfaces beyond s03.

Jumping to 71 spreads + ~$53–80 midpoint before those exist is the same premature lock the prior panel flagged. Staged build order **mitigates** batch risk; it does **not** replace a thin proof gate before spend.

### 15. Style-variant candidates still optional spend with identity debt

s08 sl13 / s65 sl16: plan correctly leaves them open. Adam/Eve never identity-tested in sl13. That belongs behind a hard “no until test passes,” not in the same decision batch as serpent treatment + full spend.

---

## Missing steps / verification gaps

### 16. Device wiring gap ignored in staged order

Staged order: align → serpent → s06 → s16 → s51 → batches of 10 + motion_lint + layer_check.

Missing explicit steps:

- expand `_devices.py` / `VERSE_CARDS` / `DEVICE_ASSIGNMENTS` for all 71 **before** any new still is called done,
- extend `SEGMENT_BUILDERS` and stills/animate job tables,
- bbox_sheet for every device that needs a bbox (not only “when we get there”),
- full-film DEVICE-QUOTA math (N=5 already FAILed six ways in `_motion_lint_report.md`; SKILL says quota math is noisy at small N, but the full mix is never pre-checked).

### 17. Finishing chain almost absent from cost/go-no-go

SKILL §8b.5–6 require `finish_config.py` + `finish_check.py` (score → sfx → cc → watermark → INV-26). Plan §6 is stills+animate only; s71 mentions INV-26/INV-27 in prose. No schedule for SFX cue table, score recipe, or `finish_check` before “episode done.” Day of Atonement was falsely “locked” with finishing missing — this plan does not close that hole.

### 18. Cost double-count + stale open question

- s2 Kling + s4 Seedance **already exist** under `clips/`; §6 still prices all 10 Kling + 20 Seedance as new.
- §6 midpoint ~$65 / range ~$53–80; §7 Q5 still says “rough ~$50–75.”
- No estimator run (admitted). “Ask-before-spending” is correct in principle; the numbers presented for user OK are still inconsistent and incomplete.

### 19. Prior independent review was DEGRADED

`_independent_review/20260807-213312/INDEX.md`: **3/5 healthy voices, quorum 4, “do not lock on this run.”** This revision answers several findings; it is not yet a clean panel close. The artifact’s closing line correctly demands another panel — that gate is open, not passed.

---

## Reuse

**Good:** locked narration/audio; Adam/Eve/Eden anchors; real `_turn_boundaries.json`; reuse of DoA assemble helpers; `thread_device` / `wash_creep` / `torn_out_page` / `annotators_circle` / `focal_tour` as real modules; reject of bad bronze-cross reuse **in the plan text**.

**Bad / incomplete:**

- PREFLIGHT still offers the rejected bronze cross.
- Golgotha reuse still assumed helpful for stills band; s54 DoA is multi-vignette, not a clean plate (plan half-admits this).
- wash-creep ADVANCE/RETREAT priced $0 with no Eden/cross POC; DoA notes wash re-anchor “NOT viable” on at least one spread.
- Cost does not credit already-paid s2/s4.

---

## Cost / spend

Rough $53–80 is in the same order as a 71-spread long sketchbook, **if**:

- reuse hits,
- re-roll stays 20–25%,
- NSFW on s51 is only +$3–5,
- no thread/naming/acting redesign.

That package of “ifs” is optimistic for: multi-figure acting, hands (s69), serpent×18, Jesus cross fail-closed, risen Christ new, tomb new, likely new Golgotha wide, 12 lettered composites. Contingency lines underprice the identity cascade, not the unit rates.

Spend is **not justified** until: (1) real estimator, (2) plan/PREFLIGHT/code one source of truth, (3) alignment pass that re-cuts s1–5 and high-risk multi-spread turns, (4) thin proof on serpent + s06 + one thread beat + naming-page prototype, (5) user answers §7 1–4. Right now the plan asks for approval of a coherent *storyboard*, not a production-ready *build package*.

---

## What improved since the last REVISE (credit, not praise)

- `hunt_and_lock` promoted and claimed honestly as tested.
- Landing uses real `torn_out_page` + held frame, not unbuilt `tear_hole`.
- Naming page no longer depends on non-tools (except §3 leftover Typeset language).
- Timing honesty + explicit pre-batch alignment step.
- Jesus render-order override for s51.
- Animation tally 10 Kling / 20 Seedance.
- Staged risk-tier build order.

Those are necessary; they are not sufficient.

---

VERDICT: REVISE  
TOP FIXES:  
1. Re-time s1–5 (and high-risk multi-spread turns) against full-file word alignment so “Where art thou?” and verse cards land on the real spoken windows — then freeze `_spread_windows.json` before any new stills spend.  
2. Make one source of truth: delete residual Typeset language in §3; sync PREFLIGHT Golgotha reuse with the bronze-cross reject; expand `_devices.py` / builders / VERSE_CARDS for all lettered and device spreads before batch stills.  
3. Gate spend on thin proofs (serpent multi-pose chain plan + s06 acting QC + one thread-device eye-check + naming-page prototype) + a real estimator that subtracts already-paid s2/s4 and uses the §6 range consistently in §7.
