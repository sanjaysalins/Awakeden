# Independent review — gemini (OK, 122s)

Here are the findings from an independent, adversarial review of the v3.2 design plan:

### 1. Hidden Risks & False Assumptions: The LLM Servicer
**Citation:** Section 5.1 (item 2) "While waiting, the client touches its heartbeat file every 10 s" and Section 5.2 (item 0) "If the rename fails, someone else has it: skip. Never call a generate tool without a claim."
**Finding:** You are relying on an LLM (Claude Code, via `SWIRLS_SHORT_SERVICER.md`) to act as a transactional state machine. LLMs cannot reliably execute atomic file locks (`os.replace`), poll heartbeats while blocked on synchronous MCP generation tools, or guarantee intermediate file writes (`submitted.json`). This is a massive single point of failure. The state machine must be in Python, not a markdown prompt.

### 2. Reuse Violation: Duplicating Pipelines
**Citation:** Section 3.8 "The episode's own `generate_score_piano.py` is a copy of ep16's" and Section 3.9 "The episode's own `build_sfx.py` is a copy of ep13's".
**Finding:** This explicitly violates the `CLAUDE.md` workspace rule: "Reuse downstream pipelines, do not duplicate". Copying and modifying score and SFX scripts per episode creates a maintenance nightmare. Parameterize the existing tools instead.

### 3. Over-engineering / Verification Gap: The R1 Probe Gamble
**Citation:** Section 5.6 "Probe R1: Does `openart_creation_show` return the charged credits and the sent settings...?" and Section 5.3 "after() confirms only if... sent_params from the record equal the priced fields".
**Finding:** The entire automated spend guard (`SWS-G0`) is built on the assumption that an undocumented OpenArt MCP tool returns exact parameters and credit costs. You admit this is unverified. If Probe R1 fails, the massive Section 5 architecture degrades to manual approval anyway. Do not build a complex transactional guard around an unverified API response.

### 4. Hidden Risk: Localizing a Global Doctrinal Bug
**Citation:** Section 3.1 `SWS-G1k KJV (in-lane wrapper)` and Section 13.2 "Fix `REPO\pipeline\kjv_strict.py`: `verify_span` accepts ellipsis splices... Other pipelines use it."
**Finding:** You identified a critical doctrinal bug where the core KJV verifier accepts dropped words, but you are patching it locally with an "in-lane wrapper" for this pilot. A doctrinal guardrail failure must be fixed at the root (`pipeline/kjv_strict.py`) so it protects the entire codebase, not patched in a local silo.

### 5. False Assumption: Static Timing Math
**Citation:** Section 1 "words / 2.2 + 0.4 x (voiced character quotes) ... must be 38.0-42.0 s".
**Finding:** ElevenLabs audio duration varies significantly based on speaker, stability settings, and emotion cues. Relying on a static 2.2 words/sec math formula for the `SWS-G1e` gate will falsely fail perfectly valid audio or pass audio that breaks the strict 45s boundary.

### 6. Missing Step: No Rollback Mechanism
**Citation:** Section 3.5 "Page 4... closes the pictures step: its leftover cap is dead."
**Finding:** If a clip render in Step 6 reveals a fundamental flaw in the still image (e.g., bad anatomy that only becomes obvious in motion), there is no mechanism to go back and fix the picture because the step is permanently closed.

VERDICT: FAIL
TOP FIXES:
1. Move the transactional file-locking and heartbeat state machine out of the LLM prompt (`SWIRLS_SHORT_SERVICER.md`) and into a real Python script.
2. Parameterize the existing score and SFX scripts instead of copying them per episode, respecting the reuse rule.
3. Fix the `kjv_strict.py` ellipsis bug at the root level instead of wrapping it locally, as it affects other pipelines.
