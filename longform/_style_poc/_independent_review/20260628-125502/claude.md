# Independent review — claude (OK, 84s)

I verified the plan's load-bearing claims against the codebase (`config.py`, `pipeline/cost.py`, the renderer modules). Findings below.

## Feasibility — model IDs are unverified, and one is likely wrong
- The plan lists 5 hf models (`recraft_v4_1`, `seedream_v4_5`, `flux_2`, `nano_banana_2`, `gpt_image_2`) as if all are valid `hf` job types. Only `nano_banana_2` is confirmed in the repo (`config.py:251`). The codebase's own A/B note (`config.py:249`) names **`seedream_v5_lite`**, not `seedream_v4_5` — the plan's manga-specialist ID looks made up. If `recraft_v4_1` / `seedream_v4_5` / `flux_2` / `gpt_image_2` aren't real hf job types, Round 1 silently renders fewer than 5 and the "best model" conclusion is drawn from a partial field. There is no validation step. **Fix is cheap and already in the toolbox:** `hf generate cost <model> --json` validates a model and returns exact credits while *creating no job* (`pipeline/cost.py:5,57`). Pre-flight all 5 IDs before spending a credit — the plan should make this step 0.

## Cost math contradicts the codebase's own anchor
- "~5 × ~7cr ≈ 35cr" and the flat ~7cr/still assumption are wrong for at least one model: `config.py:248` and `cost.py:10,35` both anchor **`nano_banana_2` = 2 credits/image**, not 7. Reflection #6 hand-waves "confirm per-model cost" but then the headline "Total ≈ ~104cr / reserve ~39cr" is presented as if real. It's not — it's assumed-flat at a rate the repo contradicts. Run `cost.hf_estimate`/`bundle_estimate` (`cost.py:137`) per model first, then state the budget. Also "Budget remaining ≈143cr" is unsourced.

## Methodology flaw — the two-round factoring confounds the STYLE test
- Round 1 picks the best model **on PG (painted realism) only**, then Round 2 forces all 4 styles through that one winner. But the plan's *own model table* says different models specialize in different styles: `seedream` = "strongest anime/manga," `recraft` = "vector/clean comic," `flux` = "painted-comic & ink." A model that wins painted-realism is not the model that best renders **MI seinen brush-ink** or **NR noir**. So Round 2's "best comic look" is measured through a renderer optimized for the *wrong* style. The style and model axes are not separable the way the plan assumes — that's the central design assumption and it's unsupported.

## The standing reverence/period gate will likely auto-fail every comic still
- The brief and engine memory require the **Christ-face reverence gate** and a fail-closed **period / Old-Master** image audit (memory: `period-reverent-image-audit`, `stills-biblical-period-gate`; `verify_image` check #6). That audit is tuned to FAIL anything not ancient-period painterly Old-Master. A comic look is *by construction* stylized, not Old-Master — so the existing gate may reject all 4 styles regardless of quality. The plan names "the Christ-face reverence gate" as the hard gate but never defines (a) the comic-adapted pass criterion, (b) who judges it, or (c) how it reconciles with the existing fail-closed period audit. This is the single biggest unaddressed risk: the gate as it exists today contradicts the entire experiment.

## The bake-off doesn't test the production path (character-lock)
- Reflection #4 admits only `nano_banana_2`/`soul_v2` give cross-scene face-lock, but Round 3 animates the *still-winner*. If a no-ref model (recraft/flux/seedream) wins, the motion confirm validates a model that **can't be used in production** for a 6–8 scene short. So a "clean" bake-off can still leave the real shipping question (consistent face across scenes, in motion) untested. Round 3 should animate the *production-realistic* config (ref-locked, ≥2 scenes of the same face), not a one-off splash.

## Reuse — `render_comic.py` risks duplicating an existing renderer
- The plan proposes a new `render_comic.py`. The repo already has `pipeline/visual_render.py` (HFProvider subprocess wrapper, `assemble_final_prompt`, `verify_image`, retry loop) and scratch drivers like `longform/_render_world.py` / `_render_images_16x9.py`. A fresh script re-implements the hf subprocess + audit plumbing the project memory explicitly says to reuse, not duplicate. Make `render_comic.py` a thin caller over the existing HFProvider, or this violates the repo's own "do not duplicate downstream pipelines" rule.

## Smaller gaps
- **FACES.html baseline may not exist where claimed.** "Extend FACES.html / apples-to-apples with the 6 prior looks" — I can't find FACES.html in the repo (only `_WORLD_TEST.html`). If the prior POC lived in an out-of-repo scratchpad, the comparison baseline isn't reproducible; say where it is.
- **n=1 per cell.** One still per model, one per style — LLM/vision judging is non-deterministic (engine memory: `gate-calibration-human-authority`). A single render per cell will pick winners on noise. At ~2cr/still the cost of 2–3 seeds per finalist is trivial insurance.
- **No defined judge.** "Judge: comic-fidelity + reverence + period" — by whom? Self-review only, or the 5-CLI panel? The repo's standing rule is *both*; the plan only commits to "review myself."

## What's genuinely good (so REVISE not FAIL)
The two-round factoring (vs full 5×4 grid), the no-panels/splash-frame rule, the anti-childish/anti-text tail, reverence-as-gate framing, and the "user owns the lane fork" humility are all correct and cost-aware. The bones are right; the execution assumptions need verification before spending.

VERDICT: REVISE
TOP FIXES:
1. Add a $0 pre-flight step 0: validate all 5 model IDs and pull real per-model credit costs via `hf generate cost <model> --json` / `cost.hf_estimate` before any render — at least one ID (`seedream_v4_5`) is likely wrong and the flat-7cr/104cr budget contradicts the repo's 2cr anchor.
2. Resolve the reverence/period gate conflict: the existing fail-closed Old-Master period audit will reject stylized comic stills by construction — define the comic-adapted Christ-face pass criterion and judge (self + panel) before Round 1, or the experiment can't pass its own gate.
3. Fix the confounded methodology: don't fix the model on PG then judge all styles through it (your own table says style↔model specialization varies); and run Round 3 motion + character-lock on the *production-realistic* ref-locked config, not the one-off still winner — reuse `pipeline/visual_render.py` instead of a new `render_comic.py`.
