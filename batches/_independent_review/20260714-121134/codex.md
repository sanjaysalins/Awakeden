# Independent review — codex (OK, 364s)

**Findings**

1. The claim “refuses paid renders (exit 4)” is false at the CLI boundary. `run_animate()` returns `4`, but `main()` ignores it and always returns `0`: [run_piece.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/run_piece.py:363), [run_piece.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/run_piece.py:767), [run_piece.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/run_piece.py:780). Same issue for rollout gate return `3`. Automation would see success.

2. “Stop-loss is fail-closed AT THE CHOKEPOINT” is overstated. The cap check runs once before the loop, then every pending slug renders: [run_piece.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/run_piece.py:362), [run_piece.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/run_piece.py:372), [run_piece.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/run_piece.py:392). If spend is just under 485cr, a multi-clip run can overshoot the cap.

3. “Charged at the HIGHER number” via disk cross-check is not a reliable render count. `disk_clip_count()` counts both `visual/clips` and `visual/_fx_pilot`: [rollout_spend.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/rollout_spend.py:58). Current repo state has three promoted pilot clips duplicated in both folders, producing the stated “6 clips charged” without six paid renders.

4. “21 gate tests green” does not cover the risky claims. The tests exercise `check_piece()`, tally basics, and prompt generation, but not `run_piece` exit-code propagation, per-clip stop-loss, or disk de-duping: [test_rollout_gate.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/test_rollout_gate.py:47). Also, `.venv\Scripts\python.exe` would not launch in this environment, so “green” was not independently verifiable.

5. Wave D’s budget claim “empty_tomb ~6 replacement stills → 6 new clips + sign_of_jonah ~3 → 3 clips” is under-supported. Current manifests are much larger and unmigrated: `empty_tomb` has 9 still jobs/9 moves and 20/20 full beats; `sign_of_jonah` has 15 still jobs/15 moves and 19/20 full beats. The plan gives no mapping from actual failing beats to the 6/3 clip estimate.

6. The plan depends on tooling that does not exist yet: `pipeline/living_light_promote.py`, before/after builder, backup helper, and `visual/wave_checklist.json`. Calling these “A(a) deliverables” is fine, but the plan lacks acceptance tests/schema for them, so later human gates are underspecified.

VERDICT: REVISE
TOP FIXES:
1. Propagate `run_animate()` return codes and enforce projected/per-clip 485cr stop-loss before any paid render.
2. Fix spend accounting to count paid render attempts, not duplicate mp4 artifacts, and reconcile the 6-disk/5-ledger/billed-502 inconsistency.
3. Add regression tests for the chokepoint path and replace Wave D’s estimate with a manifest-backed quote before rendering.
