# Independent review — cursor (OK, 99s)

## Independent adversarial review — Seed of the Woman LONG spread plan

The plan is unusually self-critical (timing honesty, staged build order, panel-driven revisions). That raises the bar, not lowers it: several claims still outrun what the repo can execute today.

---

### Feasibility vs. real codebase

**1. “FULL PLAN AUTHORED” ≠ buildable.** The spread table lives in `_spread_table.py` (71 rows), but executable code still stops at spread 5: `_devices.py` says spreads 6–71 are “to be added”; `_s4_animate.py` JOBS has two entries; `_s6_assemble.py` `SEGMENT_BUILDERS` has five entries; `_build_progress.json` is `"total": 5`. Running assemble on spread 6 would fail immediately. The plan reads production-ready; the pipeline is ~7% wired.

**2. Stale timing artifacts contradict the plan.** The plan’s “Timing seam note” fixes s05 at 33.03 → 33.80 and `_spread_table.py` uses 33.80, but `_spread_windows.json` still ends s05 at **33.03**. Same episode, two sources of truth — exactly the drift class DoA’s `_s5b_spread_windows.py` exists to prevent.

**3. s04 is a three-way mismatch.** Table: “real clip — Seedance.” `_devices.py`: `breath_synced_halo`. Built reality: paid Seedance in `_s4_animate.py` + `build_clip_hold` in assemble. For spreads 6–71, `_layer_check.py`, motion_lint, and cost accounting will lie unless every row is reconciled to one authoritative mode before batch 2.

**4. Alignment tooling is scheduled but does not exist for this episode.** Staged build order step 0 correctly calls for `_s5_align.py` / `_s5b_spread_windows.py` “(doesn't exist yet; DoA's own versions are the pattern).” `seed_of_the_woman/` has **no** `_s5*.py`. The pass is real work, not a checkbox.

**5. `hunt_and_lock` exists — on paper only for this content.** `panel_animator/hunt_and_lock.py` is real (Jericho promotion), but staged build step 3 still says “first real-content render as the standard device confirmation.” s16 is not proven on Seed stills; bbox targets in `_PREFLIGHT` are pre-design guesses until a still exists.

**6. Four “$0 proven” climax devices are design specs, not modules.** E6-A (s09 gold-fleck), E6-I (s55 shadow-sweep), s59 dual-glow, and s27 “drawn-line reveal” are detailed in `_PREFLIGHT.md` only. Repo search finds no `panel_animator` implementations (unlike `thread_device.py` or `wash_creep.py`). Calling them “$0 proven” or “pre-designed” masks mid-build invention on M1 and M6 beats.

**7. `wash-creep RETREAT` (s14/s52) assumes storm grammar ports to Eden/cross stills.** Plan correctly notes `wash_creep.py` is edge advance/retreat only — good fix from prior review. But DoA’s own `_devices.py` annotates a spread with **“wash_creep re-anchor tested NOT viable.”** s14→s52 is a designed story pair with **no POC step** in the staged build order and no mask-generation plan for garden/cross plates.

**8. Finish chain still POC-scoped.** `finish_config.py` explicitly covers spreads 1–5 only (“revisit… once the full spread table exists”). Plan mentions INV-26/INV-27 on s71 but staged build order stops at animate batches — no `check_landing_hold.py`, caption pass for 12 lettered spreads, SFX for E6-timed thumps, or score outro extension to 500s+.

**9. Governing skill is still DRAFT.** `living-sketchbook/SKILL.md` line 4: “Status: DRAFT… external 5-CLI panel must review this file before it is LOCKED.” Promoting a 71-spread, ~$65 midpoint spend episode without noting the skill isn’t locked is a process gap.

---

### Hidden risks and false assumptions

**10. Pre-designing all 71 spreads before alignment correction is backwards.** The plan admits turn 27 (s39–42) word-count splits are “meaningfully off” and “s40/s41's actual visual beats may need re-drawing,” and “~15 other multi-spread turns are unexamined.” Yet E6-B through E6-J pin sub-second events (“~163.4s, refine at alignment pass”; s71 “at ~490.4s”). Alignment pass can move spread boundaries by 1–2s+ per clause — enough to break Illuminated Rubric arrivals, annotator’s circle timing, and composite swashes. Scheduling alignment as step 0 helps; **freezing** 71 spreads + seven E6 pre-designs as authoritative before step 0 completes does not.

**11. Serpent is the real identity SPOF — with no render-order fix.** §5 gives Jesus an explicit out-of-table-order render chain (s51 first). The serpent gets one `serpent_ref.png` for ~18 appearances spanning branch serpent, belly-flat curse register, shadow-only, shed skin — far more pose variance than Jesus. Plan applies DoA’s multi-pose lesson to Christ only; serpent drift is the likely QC cascade.

**12. Study-copy KJV drift is hand-waved.** E6-C locks “seed FIXED = 315 for every study-copy appearance,” but §5 says the desk is “re-dressed per spread” across six appearances. “it shall bruise thy head” is doctrinally load-bearing; letterform drift on a re-dressed base is the same failure class as face drift, without a text anchor image.

**13. Mary no-anchor across s30/s31/s42.** Intentional, but ~14s with no distinctness gate and no fallback if veiled treatment still reads inconsistent between annunciation and vignette.

**14. Spreads 1–5 vs full-file boundaries: only s05 is audited.** Turn 1 (scripture) in `_turn_boundaries.json` runs **12.583–24.795**; spread 3 is **11.9–24.0** — 0.68s early start, unaddressed except s05→s06. If 1–5 are “promoted verbatim,” they may not chain cleanly to spread 6’s 33.80 without a full 1–5 re-audit against `_turn_boundaries.json`.

**15. s71 `torn_out_page` is built; the landing composition is not.** Revision correctly drops unbuilt `tear_hole` for `torn_out_page` (`page_transitions.py`). E6-J still requires: transition at a specific word, cut INTO a **new** risen-Christ-in-Eden-light still, hook→landing mirror with s04, fail-closed Jesus QC — a multi-layer assemble pass DoA simplified when `tear_hole` failed. “Real, tested primitive” ≠ proven on this beat.

**16. Promotion narrative undermines spend discipline.** STATUS: “promoted rather than discarded”; `_build_progress.json` 5/5 DONE. §6 correctly demands “explicit OK before any stills batch.” Those two signals conflict — spreads 6–71 should be treated as a **new spend tranche**, not continuation momentum.

---

### Over-engineering / premature scale

**17. 71 spreads / 12 lettered surfaces / 7 E6 pre-designs before spread 6 exists.** Retrospective gates were validated on a 5-spread POC (“this 5-spread slice cost ~$4”). Jumping to 66 new spreads with optional sl13/s16 variant tests, ribbon-marker A/B on s71, and ten thread-device touchpoints scales the full film before serpent anchor, desk base, tomb plate, Golgotha wide, or risen Christ are approved on one beat each — despite staged build order, the **plan surface area** is already at full-episode complexity.

**18. Internal contradiction on naming-page register.** §4 correctly revises s34–36 to Scribed Ink after “Ink Stamp/Typeset… don't exist.” §3 point 1 still says **“t20-24 get the Typeset pressed-line register”** — stale text in the same document undermines trust in the register map.

---

### Missing steps and verification gaps

**19. motion_lint is in staged build step 5 — but no quota strategy at N=71.** At N=5, `_motion_lint_report.md` already shows **6 FAIL** (device quotas, full-scope quotas) plus frozen/cliff WARNs on s04→s05. Plan assigns 26 “$0-device” spreads, 4 bespoke holds, multiple `dramatic_spotlight`/`focal-tour`/`wash-creep` uses. Step 5 says run lint; it does not say what happens when full-scope quotas FAIL (they will).

**20. `_layer_check.py` / `VERSE_CARDS` gap for 12 lettered spreads.** Only `s03_verse_card` is in `_devices.py`. s7, s19, s22, s26, s29, s31, s34–36, s47, s53, s56 have no device-table entries — known DoA defect class per SKILL 8b.4.

**21. Cost band inconsistency.** §6: “**~$53-80**, midpoint ~$65.” §7 open question #5: “rough **~$50-75**.” Same document, two ranges — undermines the “get a fresh cost quote” discipline the plan demands.

**22. NSFW/fail-closed contingency is thin.** §6 adds “~$3-5 headroom” for s51 cross NSFW fallback. Plan also needs fresh Golgotha wide (s50), new tomb (s57), new risen Christ (s71), serpent anchor with re-roll — generic 20–25% re-roll may not cover action-tier Kling on s06/s48/s69 if stills fail audit loops.

**23. Independent review gate is requested but not closed.** Plan末尾: “should go to the external panel… before the build session starts.” Prior run `20260807-213312` noted gemini failure; this review is one input, not a closed gate.

---

### Reuse

**24. Good reuse where verified:** locked narration/audio, Adam/Eve/Eden POC anchors, `thread_device.py`, Illuminated Rubric patterns from DoA, explicit rejection of `bronze_serpent_long/s44_shadow_cross.png` as “doctrinally too risky.”

**25. Golgotha reuse still optimistic.** §5 lists DoA `s53_the_cross.png` / `s54_guilt_laid_on_christ.png` with topical-fit gate — correct caution — but s54 is a multi-vignette guilt-laying frame, not a clean plate. Cost math “~60-64 new renders” assumes sharing hits; if s50–56 need fresh stills, stills subtotal moves up with no line item.

**26. s27 “drawn-line reveal” does not reuse an existing primitive.** Not `thread_device` (opacity/swell only), not `blue_line` (underdrawing reveal). It’s another unnamed bespoke unless mapped to a built skill.

---

### Cost / spend

**27. Midpoint ~$65 is plausible only in the happy path.** 10 Kling + 20 Seedance counts look correct in the revised plan. But: new serpent anchor × ~18 poses, mandatory new risen Christ + tomb, likely new Golgotha wide, 4 unbuilt bespoke devices (calendar risk, not $0 runtime), alignment-driven spread redraws on M4–M5, and variant test renders (open question #4) can push toward DoA’s ~$80–95 band. Plan’s own “NOT a quote — run the real estimator” is right; the **$50–75** figure in §7 is already stale vs §6.

---

### What improved (credit where due, still not sufficient)

- Honest timing header and turn-27 spot-check with explicit pre-batch alignment step  
- `tear_hole` → `torn_out_page`; bronze serpent cross rejected  
- Kling count corrected to 10; staged build order with serpent/s06/s51 gates  
- `hunt_and_lock` promoted to `panel_animator/`  
- Naming page revised from nonexistent Ink Stamp/Typeset to Scribed Ink  

These are real fixes. They do not close the plan/code schism, unbuilt bespoke devices, or ~15 unverified sub-turn seams.

---

VERDICT: REVISE
TOP FIXES:
1. **Run alignment-correction first and re-derive the spread table** for all ~17 multi-spread turns (priority: turn 27 s39–42, turn 36 s54–59, turn 19 s32–34) before locking E6 pre-designs or approving full-episode still spend — treat current 71-row timings as draft, not authoritative.
2. **POC the unbuilt $0 climax devices on one still each** (s09 gold-fleck, s27 drawn-line, s55 shadow-sweep, s59 dual-glow) plus wash-creep masks on an Eden still — before cost OK; do not price them as proven.
3. **Wire the executable pipeline through at least the step-0–4 gate tranche** (`_s5_align`/`_s5b`, `_devices.py`/`_spread_windows.json`, `SEGMENT_BUILDERS`, animate JOBS) and reconcile the s04 device-table vs clip pattern as the template for every paid-clip spread — plan-complete/code-incomplete is not shippable.
