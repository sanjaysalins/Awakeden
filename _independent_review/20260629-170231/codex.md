# Independent review — codex (OK, 141s)

**Findings**

1. The claim `bible_kb ... already enforces two locked truths: facts are sound (5-CLI panel)` is false against the code. `bible_kb.check_status()` does not hard-gate the fact panel; the code comments say the panel result is recorded as evidence, not a hard gate. `bib_validate.py` also continues on panel errors. So “facts are sound” is not currently enforced.

2. The fix `RUNS bible_kb on every piece (not optional, not bypassable)` contradicts the real gate policy and current runners. `bible_kb.gate()` supports `BIBLE_GATE=off`, `.bible_gate_exempt`, `warn`, and grandfather-skip when `_bible_check/` is absent. The main `pipeline.visual_runner` and `pipeline.orchestrator` paths also do not call `bib_validate` or `bible_gate` before render/animate.

3. `render still = enrich_for_scene() directives + card anchors as --image` assumes integration that does not exist in the default visual path. `pipeline.visual_runner` calls `visual_render.render_scene()` directly; no `enrich_for_scene()`, no `ref_library` lookup, no card coverage gate. Only `longform/_render_world.py` shows a partial pattern.

4. `both already keyed by entity slug (MOSES, BRONZE_SERPENT_STANDARD)` is unsafe. `ref_library` cards use `name`, not `slug`, and uppercase underscore names. `bible_kb` uses lower hyphen slugs such as `day-of-atonement`. Without an explicit normalization and alias map, the plan will miss cards and mint duplicates.

5. `one record per slug carries both its scriptural truth and its locked look` is premature. It couples mutable visual assets to verified fact files. A look reroll should not churn a verified Scripture fact record. The plan names this as an open question, but still presents unification as the “Key architectural decision.”

6. `no named reusable person/object/place is ever drawn without a registered card` has no detection design. The plan does not define how entities are extracted from scene plans, how aliases are resolved, what counts as reusable versus incidental, or how Jesus variants are handled.

7. `audit still BOTH ways: facts ... + identity (matches grid)` assumes an identity-grid audit that is not present. Existing audits cover biblical facts, generic image content, coherence, and clip QC. There is no implemented “matches grid” verifier, calibration set, sidecar schema, or fail policy.

8. `content-hash idempotence: re-animate iff the source still's hash changed` is directionally right but underspecified. Current animation paths skip on `mp4.exists()`. The plan does not say where the still hash is stored, how `.kling.json`, `.animqc.json`, reused clips, and assembly artifacts are invalidated, or how stale clips are detected.

9. `Reuse is the cost engine` is not actually in the consolidated flow. The repo already has `clip_library` and `pipeline.clip_reuse`, but the proposed flow goes from lookup/render to animate without a reuse-before-render or reuse-before-animate decision. That omission preserves the biggest spend risk.

10. The cost claim `Happy-path cost: ~93.5 credits` is incomplete. It excludes grid minting, human approval loops, failed prompt-lint retries, identity audits, fact derivation/panel/audit time, paid SUBTLE test beats, and rerenders. The repo has `pipeline.cost` for estimates/reconciliation, but the plan does not wire it into this new pipeline.

11. `SUBTLE` / `DYNAMIC` presets duplicate and conflict with existing animation controls. The repo already has `video_render.motion_prompt()` and `clip_anim_qc.choose_anim_mode()` with gallery/pushin logic and filmstrip QC. The plan adds new presets without mapping them onto those tools or replacing them deliberately.

12. `prompt lint: ban the trigger noun` is too blunt. In a Bible pipeline, words like “serpent” are often the actual scriptural subject. A blanket ban risks making prompts less auditable and less scripturally transparent unless lint is object-card specific and preserves the fact/audit wording separately.

VERDICT: FAIL
TOP FIXES:
1. Make enforcement real in the actual default runner: auto-run `bib_validate`, call `enrich_for_scene`, require green `bible_gate`, and remove or explicitly scope bypasses for the inked pipeline.
2. Replace “unify by slug” with a concrete migration/API: slug normalization, aliases, separate truth/look storage or versioning, entity extraction, lookup-before-render tests.
3. Add the missing cost/reuse/hash gates: reuse-before-render/animate using existing libraries, stored source-still hashes for clips, identity audit sidecars, and budget preflight via `pipeline.cost`.
