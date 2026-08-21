# Independent review — gemini (OK, 155s)

Here are the findings from an independent, adversarial review of the plan:

**1. False Assumption / Over-engineering of the Medium**
- *Citation:* Section 1 ("The cross-episode devices need controlled ordering") and Section 3 ("The season-level second arc: episodes 2, 7, 8, 9, 10, 11 each end with a dried ring... The Isaiah 53 finale (ep 15) answers it").
- *Critique:* This assumes a serialized, sequential viewing experience. YouTube Shorts are algorithmic and ephemeral; viewers do not watch them in order. Building a 15-episode visual IOU that only pays off in the finale is a massive false assumption about how the platform works. The "ink language" must be self-contained per episode, or the payoff is wasted effort.

**2. Feasibility Gap: Long-form Hold Durations vs. Model Limits**
- *Citation:* Section 4 ("Long (6-8 min)... longer holds (~15-25s) with Focal Tour as a primary treatment").
- *Critique:* The operational context (`CLAUDE.md`) explicitly states that `veo3_1_lite` is the mandated long-form model and operates at `VIDEO_DURATION=8`. The plan assumes 15-25s holds but provides no technical mechanism (e.g., looping, slow-mo, or sequential generation) to bridge the 8s model limit to a 25s shot. This will break in production.

**3. Single Point of Failure: Manual Enforcement of Dual-Home Policy**
- *Citation:* Section 1 ("Dual-home policy... Rule: never produce the same episode in two styles at the same time").
- *Critique:* The pipeline relies heavily on deterministic, fail-closed gates (e.g., `SP-G9`, `AS-G6`), yet this critical cost-saving rule is left entirely to human memory. Without a programmatic check in `pipeline/orchestrator.py` or `cli.py` to block duplicate episode generation across series, this is a guaranteed leak for duplicate spend.

**4. Missing Step: The Stage-Cap Lint**
- *Citation:* Section 3 ("It's also deterministic — a $0 lint can check every OT page's dosage line before a credit is spent") and Section 5 (Build 5: "first real test of the Stage-cap law").
- *Critique:* The plan relies on a `$0 lint` to enforce the OT/NT theological spine (capping OT at Stage 1-2), but completely omits the creation of this lint from the "next six builds" sequence. You cannot test a law in Build 5 if the enforcement mechanism was never built.

**5. Hidden Risk: 16:9 Aspect Ratio Unresolved Issues**
- *Citation:* Section 6 ("16:9 at scale... all real, all only partly mitigated. Long-form is 16:9, so build 6 carries this deliberately.")
- *Critique:* Deliberately carrying "partly mitigated" risks (crowd inflation, aspect-dependent prompt reads) into a `$22-30` long-form render is premature building. If the 16:9 gotchas aren't solved, Build 6 will burn credits on hallucinations. The plan accepts the risk without a mitigation strategy.

VERDICT: REVISE
TOP FIXES:
1. Redesign the "season-level second arc" (dried rings) to be self-contained per episode; YouTube Shorts are non-sequential, making cross-episode visual IOUs a false assumption.
2. Define the technical implementation for 15-25s long-form holds given the 8s `veo3_1_lite` model limit, or adjust the pacing design.
3. Add a programmatic, deterministic gate to enforce the "Dual-home policy" instead of relying on a manual human rule.
