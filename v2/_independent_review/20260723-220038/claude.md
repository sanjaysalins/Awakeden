# Independent review — claude (OK, 201s)

Verified the plan's core technical claims against the actual repo — `render_scene()` in `pipeline/visual_render.py:551-567` does accept `extra_ref_paths` (both providers, lines 157/242), `config.py:540` does have the passion-Christ banned tokens, and `config.py:479-541` confirms no `"retro"` key exists in `STYLE_REGISTRY` (only `baroque`/`graphic_novel`). The `_retro_dna/` artifacts the plan cites all exist on disk. So the plan is not fabricating its evidence — the gaps are elsewhere.

## Findings

**1. Validation gates the plan requires are not actually in the pilot's critical path (§9 vs §1/§10).**
§1 states Aaron's reference is "NOT yet chain-tested for multi-scene consistency the way Christ's ref was" — yet §9's cost table commits $5.10 to 17 character stills treating Christ+Aaron consistency as equally proven. Aaron already has one documented defect ("bare muscular arm," per RESUME.md). If his ref doesn't hold, that's stills money burned before anyone finds out, because there's no cheap 3-scene Aaron pre-flight (mirroring `_prove_it/`) inserted before the real render. Same problem for print-finish-on-animation: §10 says dot-crawl must be resolved "before the pilot renders," but §9.1-9.4's numbered plan never actually schedules that single-clip test — the full $21.25 animation budget is allocated as if it's already answered.

**2. No fallback if HF `nano_banana_pro` refuses the Passion-Christ content.**
§5a requires a marred, possibly-loincloth crucifixion render — exactly the NSFW-adjacent content category this repo's own locked memory (`feedback-hf-video-blocks-cross`) documents HF blocking elsewhere in the pipeline. The video pipeline has an explicit `HybridVideoProvider` fallback for this; §1's still-side plan names none. This is a single point of failure sitting on the hero-bookend image — the one frame the whole cut opens and closes on.

**3. The pilot is built on a code path §1 itself calls pre-production.**
"This is the HF-billed `nano_banana_pro`... a different code path from the existing production `NBPProvider`... The two are not yet reconciled; treat them as separate until one is chosen for production." Fine for R&D, but §9.4 ("wire into `config.py` + skills + gates") never names reconciling the two paths as a required step — risk that whichever path was merely convenient for the pilot gets silently wired in.

**4. A/B protocol (§9.2) is statistically weak and has no time-bound.** Comparing one EW01 retro pilot against "the last 2-3 comparable already-shipped inked/painted longs" is between-subjects with large confounds (different content, publish timing, channel growth, algorithm drift) and n=1 vs n=2-3 is noise-dominated for view-duration/retention. No minimum observation window (e.g. 30 days) is specified before applying the kill criteria — an early read could trigger a false kill or false proceed.

**5. Retry/reroll buffer only covers stills (20%), not animation.** The $21.25 animation subtotal has zero contingency despite the plan's own cited bake-off finding ([[comic-grid-cost-tiered-animation]]) that the 8 Kling-tier scenes were specifically chosen for multi-figure/action content — the exact category shown to invent motion and need rerolls.

**6. Minor — border-crop heuristic validated on one sample.** The "flat ~4.5% inset crop" fix (§1) rescued one image after 2 bad rolls, detects only the left-edge transition, then applies uniformly to all four edges. Not demonstrated across enough samples to trust as a standing mitigation across 25 pilot stills of two different models.

**7. Minor — the two-engine split (§6) has real ongoing duplicate-maintenance cost that isn't sized.** Remotion now needs its own word-alignment consumer, DoD gates, and reuse/richness counters, independent of livingpage's proven ones — acknowledged but not estimated, and no owner is named for keeping shared invariants (e.g. INV-26 hold) from drifting between the two engines over time.

**8. Sequencing tension in the plan's own logic.** §9 states the free kitsch test "runs FIRST, always" and is "still unsent," yet the same-day punch list (§10) shows ref-chain wiring, Aaron's render, and the cost table were all already built ahead of that $0 kill gate. Not fatal, but it undercuts the plan's stated discipline of proving cheaply before building.

VERDICT: REVISE
TOP FIXES:
1. Before any pilot-batch render money moves, insert two cheap pre-flight tests explicitly into §9's numbered steps: an Aaron multi-scene ref-chain proof (mirroring `_prove_it/`) and a single Kling clip run through the print-finish pass to check for dot-crawl — both are currently "should resolve before pilot" prose, not gated steps.
2. Name a fallback provider/path for character stills if `nano_banana_pro` refuses the passion-Christ render, given this pipeline's documented history of NSFW blocks on cross content on the video side.
3. Fix the A/B protocol: set a minimum observation window (e.g. 30 days) before judging kill/proceed, and explicitly caveat that n=1-vs-n=2-3 between-subjects is a noisy signal, not a clean read.
