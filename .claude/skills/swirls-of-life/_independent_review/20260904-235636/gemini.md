# Independent review — gemini (OK, 70s)

**1. False Assumption & Verification Gap: Assembler Sync is a Prerequisite, not a Follow-up**
*Cite:* "That is a separate `swirls_assemble.py` change — decide it with the user, do not silently accept the mismatch and do not fudge the plan toward the proportional numbers." (Section 8.1)
*Finding:* You are proposing to generate a frame-accurate musical score that will intentionally play up to 1.65s out of sync with the visual page turns because the assembler still uses word-count proportions. A precisely-timed score is useless if the video cuts at the wrong time. Updating `swirls_assemble.py` to use real word boundaries (e.g., via `unit_timing.json`) is a **hard prerequisite** for this pipeline stage, not a downstream "separate change". If you run this plan as-is, the final video is a regression.

**2. False Assumption: The Gospel Pivot Trigger**
*Cite:* "The unit that carries Christ's own word is the ONLY chunk whose direction says 'resolves'." (Section 6.6)
*Finding:* This assumes every episode features a direct quote from Christ at the gospel pivot. This breaks on Old Testament episodes (e.g., *The Bronze Serpent*, *Naaman in the Jordan*) where the gospel pivot exists but Christ does not speak in the narrative text. The rule must be generalized to the "gospel pivot" or "grace turn", not strictly "Christ's own word".

**3. Edge Case / Single Point of Failure: Front Cover Chunk Minimums**
*Cite:* "A unit shorter than 3,000 ms cannot be its own chunk... Episode 11's front cover is 3,139 ms — 139 ms clear." (Section 6.3)
*Finding:* A 3.1s front cover is barely clearing the API limit. A shorter title (e.g., "The Sower") will easily fall under 3.0s. The plan's general rule is to "Merge it into its neighbour and carry its direction as a second clause". But merging the front cover (which requires a "spare, cool, unresolved" identity) into F01 (which starts the narrative "urgency") will compromise the title card's distinct musical opening. You need a specific fallback for title cards < 3s (e.g., padding the front cover hold, or padding the silence before the first word).

**4. Hidden Risk: API Hallucination on `music_v2`**
*Cite:* "The docs say the model writes lyrics when none are given and treats braces as directions, brackets as labels. Anything outside those is a lyric candidate." (Section 6.4) & "Instrumental cannot be forced." (Section 9.1)
*Finding:* ElevenLabs `music_v2` is highly prone to hallucinating vocals (choirs, humming) on classical/ambient prompts when `force_instrumental` is disabled. While your smoke test (Section 7.2) is a good safety net, the plan lacks a fallback strategy if `music_v2` consistently fails the instrumental test (e.g., falling back to `music_v1` with a single prompt, or using a different prompt structure).

**5. Feasibility / Reuse:**
*Cite:* "This stage needs that same call run right after /voice — same function, same cache file, no new code" (Section 2)
*Finding:* Excellent reuse of existing codebase tools. Reusing `pipeline/assembly_align.align()` and caching `narration.alignment.json` for the downstream SRT builder is highly feasible and efficient.

VERDICT: REVISE
TOP FIXES:
1. Make the `swirls_assemble.py` real-time boundary update a hard prerequisite before running this stage.
2. Broaden the "Christ's own word" resolution trigger to support Old Testament gospel pivots.
3. Define a safe fallback for front covers under 3,000 ms that preserves the title card's distinct musical motif.
