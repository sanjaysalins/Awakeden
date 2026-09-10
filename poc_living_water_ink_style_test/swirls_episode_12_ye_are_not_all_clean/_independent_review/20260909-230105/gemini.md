# Independent review — gemini (OK, 46s)

Here is the independent, adversarial review of the `FLOW_RUN_SHEET.md` plan.

### Findings

**1. Reuse & Architecture: Bypassing the established automated pipeline**
*   **Claim/Quote:** *"Paste it into a FRESH Google Flow project as one message... The agent then runs the whole thing itself, start to finish"*
*   **Problem:** This plan completely abandons the project's established Python orchestration. The workspace rules explicitly mandate: *"Reuse downstream pipelines, do not duplicate"* and define a strict pipeline using `cli_visual.py` (Phase A/B) and `image_to_kling.py` (Phase C). Attempting to manually orchestrate 20+ media generations via a massive, brittle copy-paste prompt into a chat UI bypasses local idempotence, automated cut-hint sidecars, and the established Claude Vision content audits. 

**2. False Assumption: Impossible agent self-evaluation**
*   **Claim/Quote:** *"watch it end to end AND listen to its audio track... Check the compact SUCCESS line first, then go through the full checklist below it"* and *"ZONE check: no blue ink anywhere near Judas"*
*   **Problem:** You are assuming an LLM chat agent can accurately perform zero-shot multimodal self-evaluation on its own generated video and audio. Current agents cannot reliably parse their own generated video frames to verify strict spatial constraints (e.g., measuring if a blue thread is "at least an arm's length away" from a specific character) or listen to audio to ensure "lips stay closed". The agent will hallucinate compliance, blindly output "Yes, all checks passed," and proceed. The self-correction loop is a false safety net.

**3. Cost & Missing Steps: Destroying the cost-control image gate**
*   **Claim/Quote:** *"You do all 20 in this one conversation, in the order written, without pausing for approval and without asking me anything. I am not watching between steps."*
*   **Problem:** This "unattended" design violates the project's primary cost-control lever. The workspace rules state: *"excluding a bad image at the image gate skips paying Kling to animate it."* By chaining Phase 2 (stills) directly into Phase 3 (animation) without a human gate, any defective still that the agent hallucinates as a "PASS" will automatically consume expensive video generation credits. You are guaranteeing wasted spend.

**4. Feasibility: Session limits and context degradation**
*   **Claim/Quote:** *"Total generations | 4 refs + 8 stills + 8 clips = 20 (up to 45 attempts with retries)"*
*   **Problem:** Expecting a single web-based agent session to synchronously orchestrate up to 45 heavy media generations from a single 6,000+ word prompt is highly vulnerable to rate limits, session timeouts, and context window degradation. If the session crashes at generation 18, there is no programmatic resume state.

**5. Feasibility: Tool capabilities regarding input chaining**
*   **Claim/Quote:** *"Inputs: REF: REF_JESUS (uploaded), REF_SUPPER_ROOM, REF_BASIN_TOWEL, REF_JUDAS"*
*   **Problem:** You are assuming the "Flow" chat agent has the backend capability to programmatically pipe 3-4 specific images it *just generated* in the chat history as strict structural/character reference inputs for the next generation. Most conversational AI UIs do not support seamless multi-image reference chaining from their own un-downloaded output history without human re-uploading.

VERDICT: FAIL
TOP FIXES:
1. Scrap the chat-UI prompt approach and orchestrate this through the existing `cli_visual.py` and `image_to_kling.py` pipeline.
2. Re-insert the mandatory human Image Gate between Phase 2 and Phase 3 to prevent wasting video credits on defective stills.
3. Remove the autonomous multimodal self-evaluation loop; agents cannot reliably audit their own video/audio outputs for strict spatial constraints.
