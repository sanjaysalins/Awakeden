# Independent review — claude (OK, 299s)

## Independent review — Seed of the Woman LONG spread plan (71 spreads)

I verified this against the actual repo rather than taking its self-description at face value — including reading the two prior `_independent_review/` panel runs that this document's own fixes are attributed to.

### 1. [CRITICAL] "FULL PLAN AUTHORED" covers prose only — the executable pipeline still stops at spread 5

Checked directly:
- `poc_living_sketchbook/seed_of_the_woman/_devices.py`: `DEVICE_ASSIGNMENTS` has 2 entries (s01, s04), `VERSE_CARDS` has 1 (s03). Its own docstring: "remaining spreads to be added as the full plan is authored."
- `_s4_animate.py`: `JOBS` has exactly 2 entries (s02, s04). Docstring: "Only 2 clips for this tiny excerpt... extend JOBS as the full plan is authored."
- `_s2_stills.py`: scene list has 4 entries (s01, s02, s04, s05).
- `_s6_assemble.py`: `SEGMENT_BUILDERS` dict has exactly 5 entries (s01–s05).

None of spreads 6–71 exist in code anywhere. Running assembly today hits spread 6 with no builder. This is exactly what round-1 reviewer cursor flagged ("Running assemble today would hit spread 6 with no builder... plan-complete / code-incomplete, not production-ready"). The current §6 "Staged build order" (steps 0–5: alignment pass → serpent anchor → s06 → s16 → s51 → batches of ~10) never lists extending these four files as a step — it assumes the harness that will consume 71 spreads of renders already exists. Three smaller device-existence gaps from the same review round (`tear_hole`, `hunt_and_lock`, Ink Stamp/Typeset) all got fixed in this revision; this larger, more load-bearing one did not.

### 2. [HIGH] Seedance's real duration/loop constraint is invisible in the table and cost model

`day_of_atonement/_s4_animate.py` documents that Seedance jobs are only issued at fixed legal durations, with any longer on-screen hold relying on "assembly looping/hold-extension" (its own comments at lines 119, 392, 529 — e.g. "clip; assembly still needs to loop/extend past 18.3s"). This plan assigns Seedance to 20 spreads with table "Dur" values like 7.2s (s10), 7.7s (s12), 9.0s (s33), 9.5s (s41), 10.4s (s28) — none matching a legal Seedance duration — with no mention anywhere (table, §6 cost, or the staged build order) of a duration-snap or loop/extend step. Round-1 grok flagged this twice (finding #11, and cost finding #19: "Flat Seedance ~$0.65 — 4s vs 8s vs 12s bills differ"); it is not addressed in this revision even though the Kling/Seedance unit *counts* elsewhere in §6 were carefully recounted.

### 3. [HIGH] The "independent-review panel" this plan cites as authority was degraded and was never successfully re-run against the revised text

`_independent_review/20260807-213312/INDEX.md`: "healthy voices: 3/5 (quorum 4) — **DEGRADED PANEL — do not lock on this run**" (codex timed out at 304s; gemini hit a usage-limit error). A follow-up attempt (`_independent_review/20260807-215726/`) contains only `gemini.md`, which also failed on a usage-limit error. So the revised plan in front of me has not been read by a single healthy panel voice since the cited fixes were made — yet the document repeatedly asserts settled authority ("REVISED 2026-08-07 after the independent-review panel found...", used 3+ times). The project's own standing rule enforces this panel on every SIGNIFICANT plan, and its own panel-ops convention is "DEGRADED exits 3; CLEAN before synth" (never lock on a degraded run). This plan's closing line — "should go to the external panel... before the build session starts" — undersells the situation: it reads as a routine next step, not as "the last two attempts at this already failed to reach quorum."

### 4. [MEDIUM] Other identified "gap" assets have no build/approval gate, unlike serpent/s06/s16/s51

§6 explicitly sequences serpent anchor → s06 → s16 → s51 ahead of batching because those are recognized identity/motion risks. But §5 also flags the study desk (8 spreads: s26/32/38/39/40/46/60/66, and doctrinally load-bearing per its own "same failure class as face drift" language on the Gen 3:15b re-study), the tomb plate (s57/64), a new Golgotha wide (s50), and Mary's no-anchor treatment (s30/31/42) as needing a decision or fresh render — none get an explicit "approve before its batch" step. The desk first appears at spread 26 of 71; under a plain "~10 spreads at a time" batch order it could get generated inline rather than approved up front, reintroducing the drift risk the serpent/Jesus gating exists to prevent.

### What's actually solid (not praise, just calibration)
Verified as real and correctly fixed since round 1: `hunt_and_lock.py` now exists and has a test clip; `cast/ADAM.md`+`EVE.md` and `world/SERPENT.md` now exist; Ink Stamp/Typeset replaced with the real Scribed Ink technique; `wash-creep CONVERGE` replaced with the real RETREAT mode; `tear_hole` replaced with the real `torn_out_page`; Kling/Seedance table recount (10/20) is arithmetically correct; the Golgotha reuse section now correctly rejects `bronze_serpent_long/s44` and correctly caveats DoA's `s54`.

VERDICT: REVISE
TOP FIXES:
1. Before any spend approval or build session, extend `_devices.py`, `_s2_stills.py`, `_s4_animate.py`, and `_s6_assemble.py` (or generate them from `_spread_table.py`) through at least spreads 6–16, and prove `_s6_assemble.py` doesn't KeyError past spread 5 — add this as an explicit step in §6's staged build order, not an assumed given.
2. Add a Seedance duration-snap + loop/extend table (mirroring Day of Atonement's own `_s4_animate.py` pattern) covering all 20 Seedance-assigned spreads, and re-derive the §6 cost line once real per-job durations (not table hold-lengths) are known.
3. Re-run the full 5-reviewer independent-review panel against this actual revised document and reach real quorum before treating any of its "the panel found/fixed" claims as settled — the fixes so far rest on a panel run its own tooling marked DEGRADED, plus one failed single-reviewer retry.
