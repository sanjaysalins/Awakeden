# Independent review — cursor (OK, 97s)

## Adversarial review — Fable Round 6: THE KEEPER (revised doc)

This revision fixes several real Round 1 failures (held-breath miswire, unapproved transition siblings, missing regression rule, missing `keeper_lint.py`, forward-only §5 retroactivity). It is materially better. It is still not lock-ready: several claims are ahead of the codebase, and critical integration/verification steps are missing or mis-ordered.

---

### Feasibility vs. real codebase

**1. Engine 1 still misstates its source of truth.**  
> “Promote the proven POC engine (`_keeper_poc/_build_poc.py`)” (engine 1, lines 59–61)

The kept behaviors were built across **four** throwaway scripts (`_keeper_poc`, `_vault_poc`, `_bold_poc`, `_vault2_poc`). `starve=` and `interrupt_at=` are vault POC logic, not `_build_poc.py`. The revised doc adds an honesty fix in build step 1, but engine card 1 still reads like a single-file promotion. That mismatch will cause wrong extraction scope again.

**2. Production assembler already bypasses the five promoted engines.**  
Build step 1 targets `panel_animator/keeper_hand.py` et al., but Storm v6’s live assembler still imports the POC directly:

```72:72:poc_living_sketchbook/storm/_s6_assemble.py
import _build_poc as K  # noqa -- keeper-hand engine (entry_events/compose_at/BOLD=1)
```

Torn page and bleed are re-promoted as local closures in `_s6_assemble.py`, not via `page_transitions.py` / `bleeding_word.py`. The plan never includes a mandatory “swap assembler imports from `_build_*` → `panel_animator/*`” step. You can pass engine self-tests and regression while shipping POC forks forever.

**3. Word-Whole still has no named integration point.**  
> “Not engines: … enforcement lives in the verse-compositing path” (after engine 5)

There are three scribed-ink paths in the wild (`_s4_assemble.scribed_ink_card`, `_vault_poc.scribed_verse_layer`, `_lettering_compare.render_scribed_ink`). The plan does not specify which gets an `arrives_whole` mode, how word timing from alignment is preserved when letter-reveal is removed, or how that mode is selected per spread. Regression even **reads** unmodified `_build_vault.scribed_verse_layer` for `vault_1` — the production hook is still external to the promoted stack.

**4. LAW 2 numbers disagree inside the plan and vs. shipped code.**  
> “Margin-study graphite runs at 1.9–2.3 contrast” (LAW 2, lines 52–53)

`ROUND6_VERDICTS.txt` says “~2x graphite contrast.” Shipped `margin_study.py` uses `CONTRAST_DEFAULT = 2.6`. The plan’s own LAW 2 block is stale relative to both the verdict file and the code it claims to promote.

**5. Candle “energy-driven inverse” oversells what was taste-gated.**  
> “R(t) is energy-driven inverse (fear closes the light down; the turn opens it)” (engine 5)

The approved POC used hand-keyframed timestamps. Promoted `candle_only.py` correctly pushes curve authorship to the caller (`radius_from_keyframes`), but the plan text still implies an automatic fear envelope the user never saw. That is a new design decision smuggled in at promotion time.

**6. Foley cue names don’t match the existing subsystem.**  
Engine 1/2 export `pencil_scratch` / `graphite_scratch`; `scriptorium_foley.py` already maps **`keeper_scratch`** and **`ink_drop`** with explicit substitute honesty and Storm v6 cue timestamps. Build step 4 says “map every cue to EXISTING sound_library assets” but never says “extend `scriptorium_foley.DEVICE_SOUND_MAP` / `storm_cue_list()`” — parallel cue naming invites duplicate or divergent foley buses.

---

### Hidden risks & single points of failure

**7. Build-order step numbers contradict their own gate logic.**  
Step 5: “written into the SKILL **only AFTER the panel passes** this revised doc.”  
Step 6: “Panel round 2 … before production lock.”

Step 5 is numbered **before** step 6 but logically **depends on** step 6. Executed literally, someone amends §5 before Round 2 finishes. The inline “Storm v6 applies it now … pending this gate” (step 5) makes this worse: production is already running under a doctrinal change the panel has not passed.

**8. `margin_sentinel` is still absent from the promotion chain.**  
Engine 1 governor: “check the filmstrip, not just frame 0” on moving clips. The repo already has `margin_sentinel.py` for Kling-invented margin marks (the s09_rebuke class of defect). The plan never requires sentinel **before** keeper ink compositing. You can pass `keeper_lint` lane checks on frame 0 and still paint keeper text over animator hallucinations mid-clip.

**9. LAW 1 vs. landing grammar is named, not reconciled.**  
Naming fix (`torn_out_page` vs `tear_hole`) is good. But engine 5 still says “never the landing spread (**the torn page** owns landing light)” while LAW 1 forbids violent transition of any page carrying the Word. If a landing spread ever carries verse imagery (Illuminated Rubric / Scribed Ink), governors collide. No rule says which device wins or how authors distinguish compositional landing tear from act-turn page rip.

**10. Voice governor still lacks a procedure.**  
`keeper_lint.py` covers counts, zones, verse-card overlap, and keyword **WARNs** — a real improvement. But the POC docstring’s “PLACEHOLDER VOICE — panel review before anything ships” has no build-step counterpart: no keeper-copy authoring pass, no narration panel review, no fail-closed gate on keeper prose content. Keyword WARNs are advisory; doctrine is NON-NEGOTiable both ways in this repo.

---

### Over-engineering / premature lock

**11. Five production engines + five skill registrations before container skill lock.**  
Parent skill header: “**Status: DRAFT** (not yet panel-locked).” Build step 3 registers five keeper skills while the parent lettering/container skill is explicitly not authoritative. That inverts the repo’s gate order.

**12. Engines + lint exist; assembler proof does not.**  
`living-sketchbook/SKILL.md` §5b still notes ADOPTs not wired into a real assembler. This plan adds engines and `keeper_lint` but **no** “one full episode cut through promoted modules” gate before skill registration. Demos and pairwise regression ≠ episode-level timing, overlay exit margins (§5 letterer laws), or cross-spread governor budgets.

---

### Missing steps, edge cases, verification gaps

**13. Regression list is incomplete for two KEEP devices.**  
Step 1 pairs: `keeper_A/B`, `vault_1`, `vault_4`, `v2_05`, `bold_2`, `bold_3`. Missing:
- **`keeper_C_lamp_studies.mp4`** (Margin Studies — explicit KEEP)
- **Two Hands at Once** (KEEP; vault2 has a reference clip)

“Nine survivors → five engines” is directionally right, but the regression rule does not cover two of nine approved devices.

**14. `keeper_lint` manifest has no producer step.**  
Step 2 defines a JSON schema and says “runs before any episode lock,” but build order never says **who writes the manifest** (assembler? hand-authored sidecar? generated from beat table?). Without that, the governor is dead code in practice.

**15. Episode-level device budgets are not linted.**  
Scattered governors: “≤1 cluster … margin study”, “≤1 per episode” bleed/candle, “never two [transitions] inside 10s”. `keeper_lint.py` only counts keeper-hand entries. Nothing fail-closed enforces bleed/candle/transition/margin-study caps across an episode — exactly the collision class Storm v6 already hit (Margin Studies fallback from s07 → s05, raking-light dropped).

**16. Margin studies on moving clips remain unspecified.**  
Engine 2: “Studies derive ONLY from the spread's own approved art.” POC crops a **still** lamp region. Storm v6 score documents s07’s window was too short and geometry wrong on a moving clip; studies moved to s05. The plan’s inline “filmstrip check” answer applies to engine 1 lanes, not engine 2 crop stability on Two Hands spreads.

**17. Self-tests don’t cover the plan’s central laws.**  
Listed tests: jitter ordering, byte-stability, starve alpha, interrupt. Not tested: Word never bleeds/torn/starves, face/lane safety on moving clips, watermark/UI band survival, §7 near-silence foley conflict, phone-scale legibility. Those are the failures §5 documents as having shipped twice.

**18. `ROUND6_VERDICTS.txt` lock note conflicts with the plan’s own gate.**  
Verdicts file (lines 37–42): user approved regression pairs and ordered lock; panel round 2 “launched.” Plan step 6 still pending. The artifact presents itself as pre-lock revision while downstream state may already be treating Round 6 as locked — governance drift, not a minor doc nit.

---

### Reuse

**19. Foley should extend `scriptorium_foley`, not parallel it.**  
Step 4 is improved (“EXISTING sound_library first”), but engine cards still describe per-entry cue export without mandating registration in the existing cue map / `build_foley_bus()` path. Storm v6 already wired `keeper_scratch` and `ink_drop` there.

**20. `page_transitions.py` coexistence is asserted, not proven.**  
> “wires through the same assembler TRANSITIONS mechanism, not a parallel path” (engine 3)

`_s4_assemble.py` still uses `TRANSITIONS = {23.55: "paperRip"}` with `scriptorium_foley`’s `paper_tear` cue. No step defines when an episode uses `paperRip` vs `torn_out_page`, whether both can fire within 10s, or how foley avoids double-tear. Coexistence is a sentence, not a migration rule.

---

### Cost / spend

**21. “$0 … entire round … spent nothing” is false in context.**  
Engine runtime is $0, but the 22 POCs depended on generated stills/clips. Step 4 correctly gates ElevenLabs, but the footer erases all upstream production cost and implies the taste gate itself was free — misleading for ROI justification.

**22. Foley substitutes are already flagged weak — ear gate missing.**  
`scriptorium_foley.py` documents no real stationery scratch assets (`keeper_scratch` = high-pass dirt substitute). Step 4’s library-first rule is right, but there is no mandatory A/B ear gate before lock (unlike nib_scratch’s explicit toggle in scriptorium’s own docstring).

---

### What the revision genuinely fixed (for balance)

- Held-breath removed as hand energy source; authored per-beat energy is correct.
- `torn_out_page` only in v1; siblings demoted to gated candidates.
- Regression rule + `_round6_regression/_build_regression.py` exist and match the panel ask.
- `keeper_lint.py` exists and follows house lint pattern.
- §5 forward-only grandfathering is stated.
- Inline answers for candle anchors, pencil_study math, and filmstrip lane check are grounded in real POC code.

---

VERDICT: REVISE  
TOP FIXES:  
1. Add a mandatory assembler-integration step: migrate `_s6_assemble.py` (and document the pattern for future assemblers) from `_build_*` imports to `panel_animator/*` engines; require `margin_sentinel.py` on animated clips before keeper compositing.  
2. Fix governance sequencing: renumber so panel round 2 completes before any §5 SKILL amendment; do not treat Storm v6 as demonstrating LAW 1 until that panel passes; publish an explicit four-POC → five-engine consolidation map in the plan body (not just build step 1 footnote).  
3. Complete verification and reuse: extend regression to `keeper_C_lamp_studies` + Two Hands; define manifest production for `keeper_lint`; extend lint or add a scheduler for episode-level bleed/candle/transition/margin budgets; wire all foley through `scriptorium_foley` device keys (`keeper_scratch`/`ink_drop`), with a mandatory ear A/B gate on substitutes before lock.
