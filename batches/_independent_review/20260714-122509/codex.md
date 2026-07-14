# Independent review — codex (OK, 285s)

Findings:

- **Stop-loss can still overshoot the hard cap.** The plan claims “re-check before EVERY paid clip” and “No silent spending through the cap,” but the code only refuses when current spend is already `>= CAP_CREDITS`, not when the next 7.5cr render would exceed it. At 480cr, `run_piece` would still start another clip and land at 487.5cr.

- **The `--only <ll_slugs>` rule is not enforced.** The plan says “A(b) invocations MUST use `--only <ll_slugs>`,” but `run_piece.py` accepts bare `--stage animate`, and `cli_livingpage.py` still prints a bare animate command. This is a live single-point-of-failure for accidental non-living-light renders.

- **The budget state is internally inconsistent.** The plan says “Current: 6 clips charged (disk) = 45cr” but later says “rollout spend to date = 37.5cr” and “Remaining envelope ≈ 447.5cr.” The repo ledger/disk state after the July 14 zero point supports 5 charged clips, not 6. A hard envelope cannot be governed by two baselines.

- **The “Per-slug roll cap: 3 attempts” is only policy text.** I found no enforcement or attempt counter in `run_piece.py` / `rollout_spend.py`; parking a reject simply makes the slug “missing” and rerenderable. This matters because the forecast is already “right at the wall.”

- **Wave D cost is still under-proven.** The phrase “most full-bleed doubles are NON-adjacent repeats fixable by $0 grid conversion” is asserted, but the baseline dump shows many Wave D repeat failures, including `empty_tomb` with 8 full-bleed repeat groups and `sign_of_jonah` with 5. Until edited specs prove those pass without new stills/clips, the 15-30cr estimate is soft.

- **The filmstrip reuse is plausible but understated.** The plan says “thin cluster wrapper over the EXISTING `pipeline.clip_anim_qc.build_filmstrip()`,” but the existing module’s orchestration assumes v1 `scene_plan.json`, `visual/<provider>`, numbered mp4 names, and an oil-painting/gallery-tour rubric. Living-page cluster clips need a real adapter and rubric update, not just a path tweak.

VERDICT: REVISE
TOP FIXES:
1. Make stop-loss project the next paid clip and enforce `--only`/roll caps in code.
2. Resolve the budget baseline inconsistency to one auditable number.
3. Prove Wave D with zero-cost spec edits before quoting 15-30cr.
