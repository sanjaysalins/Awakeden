# Independent review — codex (OK, 236s)

**Findings**
- **The plan does not meet its own goal.** It claims “BAKED-IN, fail-closed” and “no still that contradicts Scripture gets animated or shipped,” but the gate is only wired in `longform/_animate_16x9.py` and `_animate_directional.py`. Main paths still animate without it: `pipeline.visual_runner` calls `run_kling_pipeline`, `pipeline.orchestrator` calls `run_kling_pipeline` / `video_render.animate_scenes`, and `_hf_animate_short.py` has no Bible gate. `cli_publish.py` only runs `publish_check.report`, not `bible_kb.gate`.

- **“every rendered still has…” is not true for the real provider-folder layout.** `check_status` and `bib_validate` set `images_dir = scene_plan.parent`, but the visual pipeline writes stills to `visual/<provider>` (`visual/nbp`, etc.). If this is wired into `cli_visual` or orchestrator as-is, it can miss the actual rendered PNGs and falsely go green.

- **The escape hatches contradict “fail-closed.”** The policy explicitly allows `BIBLE_GATE=off`, `.bible_gate_exempt`, grandfather-skip, and `warn`. Worse, the CLI claim “exit 3 = not green” is false under `--warn`: `bible_gate.py` returns `0` for not-green warn mode.

- **Layer 2 is not a regression gate.** The phrase “it is a real regression when expanded / run cross-model” is premature. `bible_calibrate.py` prints a warning on false negatives but still returns `0`; there is no threshold, no CI assertion, and the current `P=1.00 R=1.00 (n=8)` is same-model, tiny-sample calibration, not enforcement.

- **“every commit” is unsupported.** I found no `.github` workflow and only sample git hooks. Also, `test_bible_kb_regression.py` has 18 tests, not “25 tests”; the count reaches 25 only if you include separate tests in `test_bible_kb.py`.

- **Layer 1 overstates its precision.** The phrase “COLOUR / NUMBER / MATERIAL absent from its cited KJV is flagged” is only token-presence checking. With multiple cited verses, a word can appear somewhere in the KJV bundle while not supporting the actual claim-object relationship. That needs explicit adversarial fixtures before relying on it as “deterministic teeth.”

VERDICT: FAIL
TOP FIXES:
1. Wire a provider-aware Bible gate into the central animation and publish paths, not just two longform scripts.
2. Remove or tightly govern bypass modes, and make non-green status fail in CLI/CI.
3. Turn calibration into a real regression: independent model/labels, expanded fixtures, thresholds, and nonzero exit on false negatives.
