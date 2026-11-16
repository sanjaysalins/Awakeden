# Independent review — gemini (OK, 88s)

Here is the review of the proposed red team plan based on the requested lenses:

### 1. Feasibility & Hidden Risks: Massive Vision Context Overload
**Claim:** *"Pull frames with ffmpeg (e.g. 1 frame/second, plus extra around every cut) from BOTH old and new into %TEMP%, and look at them with your Read tool."*
**Finding:** While `CLAUDE.md` instructs the AI to *"look at images yourself with the Read tool"* rather than blindly trusting the SDK, doing this for 7 entire ~60-second films at 1 fps across two versions (840+ images) in a single session is completely unfeasible. Passing 840 images through the `Read` tool will instantly exhaust the token context window, trigger API rate limits, and cause the LLM to lose the cross-frame memory required to verify that *"recurring people keep the same face and clothes"*. 

### 2. False Assumptions: Fragile Audio Hashing
**Claim:** *"Check audio with `ffmpeg -i f -map 0:a -c copy -f md5 -`"*
**Finding:** Comparing the MD5 hash of a *compressed bitstream* (`-c copy`) is a false assumption. If the uplift pipeline simply re-muxed the container, changed encoder metadata, or re-encoded the AAC track to bake in the piano/SFX mix, the stream hashes will fail—even if the acoustic waveform is 100% identical. The validation should decode to raw PCM first (e.g., `-c:a pcm_s16le -f md5`) to check actual audio parity.

### 3. Missing Steps & Verification Gaps: Ignored Locked Invariants
**Claim:** *"Owner rules to judge against..."*
**Finding:** The plan entirely misses two critical locked invariants for finished videos documented in `CLAUDE.md`:
1. **INV-26 (Landing hold):** Every finished cut must have a ≥3.0s landing hold. The plan fails to instruct the use of the existing `check_landing_hold.py` tool.
2. **Score Fade:** The newly added rule (2026-11-16) requires *"Score end = slow ~2.5 s fade to the last frame."* A visual frame-by-frame check will not catch an abrupt audio drop.

### 4. Reuse: Bypassing the Enforced Multi-Agent Panel
**Claim:** *"YOUR job: independently judge each NEW film against its OLD one..."*
**Finding:** This plan asks a single AI session to manually perform a massive QA loop, which bypasses the mandatory `independent_review.py` script. The repo rules explicitly state: *"EXTERNAL independent review is ENFORCED... via independent_review.py BEFORE it is called done,"* which correctly parallelizes this across a 5-CLI multi-agent panel (`cursor primary + claude + gemini + codex + grok`).

### 5. Cost / Spend: Unjustified Token Burn
**Claim:** *"look at them with your Read tool."*
**Finding:** Brute-forcing 840+ frames through a live chat vision model is an extremely expensive token spend. The existing `verify_cut` pipeline (in `pipeline/assembly_render.py`) is already designed to perform per-slot Vision audits intelligently and idempotently, avoiding the massive cost overhead of re-auditing unaltered identical frames in bulk.

VERDICT: FAIL
TOP FIXES:
1. Replace the manual 840+ frame `Read` extraction with the existing `verify_cut` Vision pipeline and `independent_review.py` panel.
2. Fix the audio validation command to hash decoded PCM audio (`-c:a pcm_s16le`), not fragile compressed bitstreams (`-c copy`).
3. Add mandatory automated checks for INV-26 (using `check_landing_hold.py`) and verify the 2.5s score fadeout rule.
