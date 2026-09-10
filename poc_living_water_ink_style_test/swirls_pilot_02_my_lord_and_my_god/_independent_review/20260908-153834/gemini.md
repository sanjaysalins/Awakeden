# Independent review — gemini (OK, 61s)

Here is the independent, adversarial review of the `FLOW_RUN_SHEET.md` plan.

### 1. Reuse: Massive duplication of existing pipeline (Regression)
**Claim/Step:** The entire document, specifically the manual self-correction instructions like *"Check STILL_01 by looking at it... Any line fails → regenerate S1-A once"* and the sequential generation of images and video.
**Finding:** This plan completely ignores and duplicates the project's existing, highly developed Python orchestration. The repo already has `cli_visual.py`, `pipeline/visual_render.py` (which contains `render_scene` with a built-in retry-on-audit loop), and `verify_image` (a Claude Vision content audit). Re-inventing this robust, idempotent code pipeline as a fragile 6,000-word prompt for a chat UI is a massive architectural regression. 

### 2. Feasibility & False Assumptions: Autonomous execution limits
**Claim/Step:** *"The agent then runs the whole thing itself, start to finish, with no human re-pasting anything in between... 18 generations. You do all 18 in this one conversation, in the order written, without pausing for approval"*
**Finding:** This assumes a chat-based LLM can reliably execute an 18-step multimodal loop (generate image → self-audit via vision → conditionally retry → attach as reference for next prompt → generate video) from a single zero-shot prompt. Current agents will almost certainly suffer from context collapse, skip steps, hallucinate tool calls, or fail to properly attach the specific generated images as "Ingredients" for subsequent steps. It is highly unrealistic to expect 18 flawless sequential multimodal operations without a deterministic code scaffold.

### 3. Hidden Risks & Single Points of Failure: No idempotence
**Claim/Step:** *"If Flow refuses to generate something, write that under Flags and continue. Never fix a defect by editing a prompt. Never stop the run."*
**Finding:** Because this is bundled into a single monolithic chat session, it lacks the idempotence of the Python pipeline (`PNG + passed-audit sidecar = skip on re-run`). If the agent times out, hits a safety filter on Step 14, or loses context, the entire run is compromised and cannot be cleanly resumed from the point of failure without manual human intervention (which the plan explicitly tries to avoid). 

### 4. Cost / Spend: Bypassing established model tiering
**Claim/Step:** *"Generate one video, 8 seconds (or Flow's nearest available length)"* (Repeated in S1-B through S8-B)
**Finding:** This plan destroys the project's strict cost-control model. `CLAUDE.md` explicitly mandates tiering animation models based on content complexity to maintain the ~$23/episode budget (e.g., Seedance for calm panels at ~4.8cr, Kling for action at 7.5cr, Veo for long-form). By blindly commanding a generic "Flow" agent to generate 8 videos, you lose all granular API cost control and model selection, likely resulting in massive overspending or degraded quality.

### 5. Feasibility: Strict gap enforcement via prompt
**Claim/Step:** *"a clear, deliberate, visible GAP remains between his fingertips and Jesus's hands... this gap is a hard rule"*
**Finding:** You are relying entirely on the image generator's prompt adherence to enforce a pixel-perfect spatial relationship ("gap remains... they do not touch"). Diffusion models notoriously struggle with precise multi-character hand interactions. Expecting a single retry (*"regenerate S5-A once"*) to reliably fix a complex hand-interaction hallucination is overly optimistic.

VERDICT: FAIL
TOP FIXES:
1. Discard the monolithic chat-prompt approach and route these exact prompts through the existing `cli_visual.py` / `pipeline/visual_render.py` Python orchestration.
2. Restore the deterministic Claude Vision audit (`verify_image`) instead of asking the generating agent to self-police its own output in the same context window.
3. Re-integrate the strict animation model tiering (Kling/Seedance/Veo) to maintain the established cost model, rather than relying on a generic video generation step.
