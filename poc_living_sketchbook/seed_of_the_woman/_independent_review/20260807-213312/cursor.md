# Independent review — cursor (OK, 147s)

## Independent adversarial review — Seed of the Woman LONG spread plan

### Feasibility vs. real codebase

**1. Plan is authored; the build pipeline is not.** The plan claims a “FULL PLAN AUTHORED” state and that “a Sonnet execution pass builds from this without making composition decisions,” but executable code still stops at spreads 1–5. `_devices.py` explicitly says spreads 6–71 are “to be added”; `_s2_stills.py` and `_s4_animate.py` only define jobs for 1–5; `_s6_assemble.py`’s `SEGMENT_BUILDERS` dict has five entries while `_spread_table.py` already lists 71 spreads. Running assemble today would hit spread 6 with no builder. That is plan-complete / code-incomplete, not production-ready.

**2. `tear_hole` is mandatory in the plan but does not exist in the repo.** s71 specifies `tear_hole (mandatory landing device)`. Day of Atonement’s own `_s76_landing.py` states plainly: “Checked the whole repo for an existing implementation — there isn’t one,” and shipped a `$0` push instead. `page_transitions.py` also separates `torn_out_page` (built) from `tear_hole` (“NOT BUILT IN v1”). The plan treats s71’s landing as a known $0 device; it is an unbuilt compositing pass.

**3. `hunt_and_lock` is billed as `$0` and “the device’s literal design case” (s16) but is not a reusable panel_animator module.** Repo search finds no `hunt_and_lock` implementation in `panel_animator/`. Jericho wired a one-off in `_j5_assemble.py`. s16 is not “plug in existing device”; it is new episode-specific glue.

**4. s04 plan vs. built artifact mismatch.** The spread table says s04 is “real clip — Seedance,” but `_devices.py` assigns `breath_synced_halo` (a $0 device family). `_s4_animate.py` actually paid for Seedance, and `_s6_assemble.py` uses `build_clip_hold` on that clip — not the device table. For spreads 6–71 this drift will break `_layer_check.py`, motion_lint, and cost accounting unless every row is reconciled before batch 2.

**5. Golgotha reuse paths are asserted, not verified.** §5 cites `day_of_atonement\stills\s53_the_cross.png` and `s54_guilt_laid_on_christ.png`. Ledger/HTML references confirm those were rendered, but s54 is explicitly a multi-vignette guilt-laying frame (Aaron + goat memory), not a clean cross plate. Plan mentions “topical-fit gate,” but cost math assumes reuse may work; if s50–56 need fresh stills, the “~$25–45 stills” band is optimistic.

**6. Living-sketchbook skill is still DRAFT.** SKILL.md line 4: “Status: DRAFT… external 5-CLI panel must review this file before it is LOCKED.” The plan promotes this to a real long episode without noting that the governing skill itself is not locked.

---

### Hidden risks and false assumptions

**7. Serpent identity across ~18 appearances, one anchor, many incompatible poses.** §5.1 locks one `serpent_ref.png` for branch serpent, belly-flat curse register, shadow-only, shed skin, etc. The plan applies multi-pose chaining to Jesus (§5) but not to the serpent despite far more pose variance than Jesus. Day of Atonement’s multi-pose lesson is cited for Jesus only; serpent drift is a likely QC cascade.

**8. Study-copy “same overlay params/seed” with no image anchor across six desk spreads (s26/40/46/47/60/66).** §5 and §4 call this a recurring prop with `$0` overlay consistency, but the desk is “re-dressed per spread.” Letterform drift on Gen 3:15 is doctrinally load-bearing (“it shall bruise thy head”). No anchor + changing base stills = the same failure class as face drift, acknowledged for faces but hand-waved for text.

**9. Mary deliberately has no anchor (§5.5) across s30, s31(bg), s42(vignette).** Reasoning is intentional, but ~14s of screen time with no distinctness gate invites figure drift; the plan has no fallback if veiled/averted treatment still reads inconsistent.

**10. Timing for spreads 6+ relies on word-proportional ESTIMATES inside long narrator turns, with only one explicit TIMING FLAG.** The header admits sub-turn seams are “word-proportional ESTIMATES flagged for the standard alignment-correction pass,” but only s56 (Col 2:15) is flagged. High-risk unstated cases:
- **s34–36 naming page:** turn 19 is 25.7s spanning s32–s34; stamp + Typeset timing for Rev 12:9 (2.6s fragment) is mostly estimated inside narrator speech.
- **turn 27 → s39–42:** one 36.9s narrator turn split into four spreads (9.5–11.8s each) with no per-word alignment artifact shown.
- **turn 36 → s54–59:** 40.6s for six spreads; s56’s composite is flagged, but the rest are not.

**11. spreads 1–5 vs 6+ use different alignment sources without a full reconciliation plan.** The “Timing seam note” only fixes s05 (33.03 → 33.80). Spread 3 is timed 11.9–24.0 while `_turn_boundaries.json` turn 1 (scripture) runs 12.583–24.795. The handoff is acknowledged for s5→s6, not audited for 1–5 internal consistency against the full-file boundaries.

**12. s05 is a designed frozen hold but already triggers motion-lint warnings.** `_motion_lint_report.md`: `FROZEN-SHORT` on s05 and `MOTION-CLIFF` s04→s05. Plan calls this intentional (“device-only… no camera move”), but at 71 spreads, frozen/device-only density (26 `$0-device` spreads per §6) compounds the cliff problem the linter exists to catch.

---

### Over-engineering / premature scale

**13. 71 spreads / 12 lettered surfaces / 7 bespoke pre-designs (E6 in `_PREFLIGHT`) before a single spread-6 still exists.** Retrospective gates (8b) were validated on a 5-spread POC (~$4). Jumping to 66 new spreads with two style-variant candidates (sl13/s08, sl16/s65), optional ribbon-marker A/B on s71, and ten thread-device touchpoints is scaling the full film before serpent anchor, desk base, tomb plate, risen Christ, or `tear_hole` are proven on one beat each.

**14. s34–36 as “ONE continuous page across 34–36” while also breaking “never two lettered spreads adjacent.”** §4 and open question #2 admit this is a designed exception. It increases compositor complexity (in-page arrivals, three Ink Stamps, three Typeset blocks) and removes the deterministic guard that exists because Scribed Ink cannot hit 2.6s fragments — fine if user approves, but it is structural complexity not yet validated in code.

---

### Missing steps and verification gaps

**15. No `_spread_windows.json`, `_s5_align.py`, finishing chain, or landing-hold verification in the plan.** Day of Atonement longform path is `_s2` → `_s4` → `_s5_align`/`_s5b_spread_windows` → `_s6` → captions/SFX/landing. Plan ends at stills+animate cost; it does not schedule alignment correction (which it admits is needed), spread-window generation, `check_landing_hold.py` (INV-26), or watermark (INV-27).

**16. `_layer_check.py` gate not satisfied for verse spreads beyond s03.** `_devices.py` `VERSE_CARDS` only contains `s03_verse_card`. Twelve additional lettered spreads (s7, s19, s22, s26, s29, s31, s34–36, s47, s53, s56) have no device-table entries. SKILL 8b.4: blank device entries are a known Day-of-Atonement defect class.

**17. `motion_lint.py` after every ~10-spread batch is required (SKILL 8b.3); plan does not include it.** Full-episode device mix (3× `dramatic_spotlight`, 4× bespoke holds, 2× `wash-creep`, 4× `focal-tour`, etc.) has never been linted at N=71. At N=5, lint already FAILs six ways — plan does not say how full-scope quotas will be checked before spend.

**18. Independent review is requested at the end but the run in `_independent_review/20260807-213312/` shows gemini failed (usage limit).** Plan says panel review should happen before build; that gate is not actually closed.

**19. Animation count typo.** §6 says “9 Kling”; the spread table lists ten Kling spreads (s02, s06, s11, s17, s24, s30, s43, s48, s51, s69). Small error, but it undermines the “get a fresh cost quote” discipline the plan itself demands.

---

### Reuse

**20. Good reuse where it exists:** narration/audio/`_turn_boundaries.json`, Adam/Eve/Eden anchors from POC, cross-import of DOA device renderers in `_s6_assemble.py`, `thread_device.py` promotion from Day of Atonement, Illuminated Rubric in `day_of_atonement/_devices.py`.

**21. Bad reuse assumption:** `bronze_serpent_long/stills/s44_shadow_cross.png` as Golgotha reuse candidate. The project’s own `_build_clips_review.md` flags s44 as “doctrinally too risky.” Listing it alongside DOA crosses without a reject/default wastes review time and invites a wrong reuse.

**22. `wash-creep ADVANCE/CONVERGE` (s14/s52) assumes storm-era grammar ports to Eden→cross stills.** `wash_creep.py` was proven on storm masks; Day of Atonement `_devices.py` notes “wash_creep re-anchor tested NOT viable” for at least one spread. s14→s52 is a designed story pair, but it is not proven $0 on this episode’s stills — plan prices it at $0 with no POC step.

---

### Cost / spend

**23. $50–75 midpoint is plausible only if reuse hits and re-roll stays at 20–25%.** Day of Atonement landed ~$80–95 at 76 spreads with similar unit costs. This episode has more Kling action (heel strike s48, hands s69, blame circle s06), a new serpent anchor with ~18 appearances, mandatory new risen Christ (s71), new tomb, likely new Golgotha wide (s50), and NSFW fail-closed path on s51 (“§5 NSFW fallback note”) — none of which are in the contingency line beyond generic 20–25% re-roll.

**24. “Ask-before-spending” is stated twice but contradicted by promotion narrative.** STATUS line says the POC was “promoted rather than discarded” and `_build_progress.json` shows 5/5 done — reads like momentum to continue, while §6 correctly says real estimator + explicit OK still required. The plan should treat spreads 6–71 as a new spend tranche, not an extension of a validated slice.

**25. Two variant test renders (sl13/s08, sl16/s65) are optional but not priced in §6** beyond “2 variant tests” in gap renders — OK if user says no, but open question #4 leaves branch uncertainty that affects still count and identity QA.

---

### Doctrine / craft (smaller but real)

**26. s45 introduces Golgotha silhouette before the narration names the cross; s50 hard-cuts “That is the cross.”** Coherent artistically, but s45’s “FIRST appearance” cross silhouette plus gold thread across Eden→cross is a strong visual claim before turn 34’s “That is the cross” — worth verifying against narration sync in alignment pass.

**27. Gen 3:14 (s19) uses Scribed Ink live-write at 14.0 g/s; turn 11 is `speaker: scripture`, not `god`.** LAW 1 whole-arrival applies to god/red-letter (s22 correctly uses Illuminated Rubric whole arrival). s19 is probably fine, but s19’s 11.1s spread vs 9.87s voiced turn needs the same alignment scrutiny as s56.

---

VERDICT: REVISE
TOP FIXES:
1. **Close the plan↔code gap before any spread-6 spend:** extend `_devices.py`, `_s2_stills.py`, `_s4_animate.py`, and `_s6_assemble.py` through at least one full movement (or generate them from `_spread_table.py`) and prove assemble doesn’t KeyError on spread 6.
2. **Resolve unbuilt landing/device dependencies:** either POC `tear_hole` + s71 compositing on a still pair first, or revise s71 to ship a proven `$0` landing (DOA/Bronze Serpent precedent) and drop “mandatory tear_hole” until built; same for `hunt_and_lock` (s16) and s55 shadow-sweep.
3. **Run real alignment on the worst seams before the full stills batch:** naming page s34–36, turn-27 block s39–42, turn-36 block s54–59/s56 — produce word-level spread windows (not estimates) and update `_spread_table.py`; fix Kling count and stills budget after reuse eye-check on DOA s54 (likely reject) and bronze s44 (should reject).
