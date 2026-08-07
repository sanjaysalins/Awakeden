# Independent review — claude (OK, 240s)

## Review — Seed of the Woman LONG spread plan (71 spreads)

I checked the plan's technical claims against the actual repo rather than taking them at face value. Several load-bearing "$0, already-proven" devices don't match what's actually in the codebase.

**1. Three devices central to the plan don't exist in this repo; a fourth is proven for a far narrower case than claimed.**
- `hunt_and_lock`, used at spread 16 ("hunt_and_lock ($0 — the device's literal design case)"), returns **zero matches anywhere in `JesusInTheBible`**. It isn't built here.
- `Ink Stamp` and `Typeset pressed lines`, used at spreads 34-36 with an implied proven mechanic ("Ink Stamp (1/6)... (2/6)... (3/6)", "≤6 stamp budget"), also return **zero matches**. The closest thing in the repo is an unpromoted prototype (`draw_ref_stamp` in `poc_living_sketchbook/_skill_adaptations/thread_v2/_render.py`) under different naming, never validated at production scale.
- `Thread Device`, called "the episode's signature image" and used at 10 spreads (s21/22/25/28/37/45/62/63/64/66) in four distinct behaviors ("draw-on," "draw-on upward," "gleam-pass," persistent background glow), **does exist** as `panel_animator/thread_device.py` — but per `day_of_atonement/_devices.py` it was proven for exactly **one** use, once, at the climax (`answer_thread_reprise`: two regions swelling into a single Christ-anchor point). None of the plan's other three behavior modes have working code yet.

This matters more than a normal missing-tool gap because the Thread Device is the visual instantiation of the LOCKED "one thread spine" narrative requirement (CLAUDE.md). If it can't actually do "draw-on upward" or "gleam-pass" cleanly across 10 independently-generated stills, that's not a one-spread fix, it's the film's structural spine. None of this appears in §7's open-questions list, even though the document's own closing line says this plan should go to the external panel before the build session starts — as written, the panel would have to independently discover it, same as this review just did by grepping.

**2. The cost estimate (§6) doesn't match the plan's own table.** It counts "9 Kling" clips; the table actually specifies 10 (s2, s6, s11, s17, s24, s30, s43, s48, s51, s69). It counts "19 Seedance"; the table specifies 20 (s4, s8, s10, s12, s18, s20, s28, s33, s41, s44, s46, s50, s54, s57, s58, s62, s64, s65, s67, s70). Kling is the priciest per-unit line item, so the quoted "$50-75, midpoint ~$60" is under-tallied — small in dollars, but it means the estimate wasn't actually computed by counting the table, which undercuts confidence in the framing "below Day of Atonement's ~$80-95 midpoint, as expected."

**3. Build-order gap in the Jesus multi-pose identity lock.** §5 states "the first approved episode appearance (s51, the cross) chains as the SECOND reference into every later Jesus spread." But s42 (vignette) and s43 (feet) are earlier in spread order than s51. If stills render in table order (as the rest of the document's sequencing discipline implies), s42/s43 render and lock in *before* the s51 anchor exists, so they get only the single generic `jesus_ref.png` — exactly the drift risk the multi-pose lock is meant to prevent — while the plan's language implies full protection. The plan never states a render-order override (e.g., render s51 first, out of sequence) to fix this.

**4. Minor: the "chain is CONTINUOUS" claim in the sum-check contradicts the paragraph two above it.** It says "each spread's start = the previous end," but s5 ends at 33.0 and s6 starts at 33.80 — the exact 0.8s seam the "Timing seam note" already discloses and explains. Not hidden, but the blanket claim should be caveated to the one flagged exception.

**5. Premature full-lock.** This document promotes directly from a 5-spread validation slice to a fully locked 71-spread table + cost estimate in one step, with no intermediate checkpoint. Given finding #1 — three unbuilt/narrowly-proven devices sit in the highest-density, most novel stretch (M3-M4, the desk/naming-page argument section) — locking the full table and getting a spend OK before those devices are built and eye-checked on 2-3 real spreads risks sinking 66 spreads of planning into a shape that has to change once the Thread Device's new behaviors or Ink Stamp turn out not to render as described.

VERDICT: REVISE
TOP FIXES:
1. Build and eye-check the three missing/under-proven devices (hunt_and_lock, Ink Stamp/Typeset pressed lines, and the Thread Device's non-reprise behaviors) on real test spreads before locking the full 71-spread table or requesting spend sign-off — add this as an explicit §7 open question.
2. Recount the Kling/Seedance tallies in §6 directly from the table (10 Kling, 20 Seedance, not 9/19) and re-derive the cost range.
3. State an explicit render order for the Jesus spreads so s51's approval actually precedes and anchors s42/s43, or accept and flag that those two spreads render off the single generic reference only.
