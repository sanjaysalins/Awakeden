# Independent review — claude (OK, 340s)

I verified this plan against the code — ran the tests and the stop-loss script myself. Most claims check out, which is rare. What survives and what doesn't:

## Verified true (I ran / read it)

- `pipeline/rollout_gate.py` implements **every** listed check (fullbleed ≤60%, ≥3 templates, ≤2 uses, adjacent-pair rule, fx ≥50%, temp-arc poles 7000K/5500K, motion smooth, cut_ticks, living_light ≥2 + played-not-dyncam'd, double-lighting, lit landing, slop captions). **21/21 tests pass** (I ran them).
- `pipeline/rollout_spend.py` runs and prints exactly the plan's numbers: 37.5cr attributed, 447.5cr headroom. Reconcile-row exclusion is real (`rollout_spend.py:38-39`).
- Gate-window fix is real: `run_piece.py:348` conditions on spec-file presence, not living_light entries — and **all 12 rollout pieces already have `visual/livingpage_short.spec.json`**, so no bypass window remains.
- `run_piece.py:34` IS the ARK endpoint — gemini's round-1 objection stays dead.
- Gold-master source for the Wave A tooling exists: `batches/cluster_02_resurrection/women_first_witnesses_luke245/promote_living_light.py`.
- `reuse_check` (`run_piece.py:103`), `cost summary --episode` (`pipeline/cost.py:200`), `pipeline/clip_anim_qc.py` — all exist.
- Budget arithmetic is correct to the credit (247.5 base; ×2.3 = 569.25; ×1.5 = 371.25; scope-cut ranges 52.5–120.75 and 67.5–155.25 match). All 13 piece.json files use `"duration": 5`, so the 7.5cr/clip constant is consistent.

## Findings

**1. The stop-loss's own data source can silently go dark — a fourth "known limit" the plan doesn't state, and the worst one.** `_hf_animate_short.py:135-136`: if `pipeline.cost` fails for ANY reason other than a ceiling breach, the render **proceeds unmetered** (`_cost = None`), and the ledger row at line 149 is only written when `_cost` is truthy — plus `record()` itself is `except: pass` (lines 153-154). Real HF spend, zero attributable rows, `rollout_spend` stays green. Given the user co-edits live (locked/parallel ledger file is a plausible trigger), this is a credible systematic under-count in a plan whose core promise is "no silent spending through the cap." Cheap fix: during the rollout, make ledger failure fail-closed on animate, or have `rollout_spend` cross-check ledger clip-count against `visual/clips/*.mp4` files newer than 2026-07-14 and scream on mismatch.

**2. NSFW fallback can ship a fake "living-light" clip and the gate can't see it.** `_hf_animate_short.py:206-207` silently falls back to $0 ffmpeg crop-cuts when HF blocks a clip. Waves B–C are crucifixion pieces (pierced, it_is_finished — bare-torso cross, the documented HF NSFW failure). The rollout gate checks the **spec**, not the rendered mp4's provenance, so a piece can gate-PASS with a static ffmpeg fallback occupying a living_light slot — defeating the product the 180cr buys. Only human filmstrip QC catches it. The plan should state: ffmpeg fallback on a living_light slug = automatic reject/re-roll decision, and the forecast should carry a line for blocked-but-billed rolls on cross imagery (currently just "eyeball the balance").

**3. Checklist item 3 greps a file that doesn't exist.** No piece has a `_sfx.py`. Beds are built centrally from `sfx_pilots/build_cluster1_sfx.py`'s PIECES dict (see `run_piece.py:47-51`, `cli_livingpage.py` wiring). The $0 audio-diff is feasible, but as written the operator greps nothing. Name the real file.

**4. Minor: legacy re-roll path bypasses the rollout gate.** `batches/cluster_01_cross/_animate_rerolls.py` calls the animate layer directly — it keeps the budget/sidecar gates but not the new rollout gate. Re-rolls during QC are exactly when someone reaches for it. One sentence in the plan: all rollout re-rolls go through `run_piece --stage animate --only <slug>`.

Everything else — wave ordering, zero point, forecast rule, scope cuts, the answered objections — holds up under checking. Findings 1 and 2 both puncture the plan's fail-closed spend story, so it's not a PASS yet, but they're one-day fixes, not structural flaws.

VERDICT: REVISE
TOP FIXES:
1. Close the unmetered-spend hole: fail-closed on ledger failure in `_hf_animate_short.py` (or add an mp4-on-disk cross-check to `rollout_spend`), and add it to the plan's stated limits.
2. Make ffmpeg-fallback on a living_light slug an automatic FAIL/re-roll (gate or QC step checks clip provenance), and budget explicitly for NSFW-blocked-but-billed rolls on the crucifixion pieces.
3. Fix checklist item 3 to grep the real bed builder (`sfx_pilots/build_cluster1_sfx.py` PIECES dict), and route all re-rolls through `run_piece --stage animate` so the rollout gate is never skipped via `_animate_rerolls.py`.
