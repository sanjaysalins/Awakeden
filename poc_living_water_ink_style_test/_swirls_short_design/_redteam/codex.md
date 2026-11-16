**REVISE. The design cannot enforce the owner’s own priced consent, and several gates can accept materially wrong content.**

References: **D** = [pipeline design v3.1](F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/_swirls_short_design/SWIRLS_SHORT_PIPELINE_DESIGN_v3.md); **P** = [pilot brief](F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/_swirls_short_design/PILOT_BRIEF_isaiah40.md). I distinguish proposed-design holes from current-code defects.

1. **BLOCKER — The worker can manufacture the owner’s priced yes.**  
   The same agent writes `approve`, `ok`, prices and purported owner quotations. After the owner says “I like it,” the worker can record a dated spend approval and satisfy the guard without another owner message. D §5 explicitly acknowledges this; §5.4 requires only a note.  
   **Fix:** Require an owner-issued authorization bound to episode, step, quote, currency and cap, which the production worker cannot create.

2. **BLOCKER — ElevenLabs caps do not constrain the purchases.**  
   `paid` reserves one quoted row, then runs an arbitrary command. The synthesis command makes one purchase per uncached turn; `align(force=True)` can be repeated while that single voice row remains open. No per-call reservation limits the actual bill. D §§3 step 2, 5.5; [synth purchase loop](F:/slk/PycharmProjects/PythonProject1/jesus/narration/per_turn_synth.py:225).  
   **Fix:** Reserve budget at each ElevenLabs request, including retries and alignment, before dispatch.

3. **BLOCKER — Current “$0” operations can spend outside the guard.**  
   Successful scored assembly automatically calls `build_srt.build()`, which forces another paid alignment. Separately, `verify` uses the metered Vision API when `LLM_PROVIDER=api`. Adding the proposed cache helper does not remove these existing routes. D §3 prerequisites and step 9; [automatic SRT call](F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/swirls_episode.py:365), [forced alignment](F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/build_srt.py:51), [Vision API branch](F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/swirls_verify.py:477).  
   **Fix:** Route trim assembly exclusively through cache-only SRT and refuse metered Vision mode before any audit call.

4. **BLOCKER — The selected KJV verifier accepts a reversal of John’s denial.**  
   `verify_span("John 1:20", "I am ... the Christ.")` accepts ordered fragments while omitting **“not.”** It also accepts `"No."` against that verse by matching inside **“not”**, because matching lacks word boundaries. I reproduced both using a read-only port of its matching logic against the local corpus. D SWS-G1k delegates to this verifier; [matching implementation](F:/slk/PycharmProjects/JesusInTheBible/pipeline/kjv_strict.py:171).  
   **Fix:** Require one contiguous, whole-word Scripture span; reject omissions and ellipses on this pipeline.

5. **MAJOR — Guard activation depends on where the output is saved.**  
   Generate into an unmarked temporary folder, then move the result into the episode: D §5.1 explicitly leaves that request unguarded. Episode two also loses protection if its manually created folder lacks the marker. Direct MCP generation remains another acknowledged bypass.  
   **Fix:** Require episode authorization at the provider boundary, independently of output location or marker presence.

6. **MAJOR — Cancellation does not prevent duplicate purchases already dispatched.**  
   A servicer reads a request and starts generation; the client times out and moves the file to `cancelled`. That move cannot cancel the in-flight purchase. Two servicers can also read the same request before either responds. No atomic claim or provider idempotency protocol is specified. D §§5.1–5.3; [servicing sequence](F:/slk/PycharmProjects/JesusInTheBible/AGENT_BRIDGE.md:113).  
   **Fix:** Atomically claim requests, persist dispatch state, enforce idempotency, and reconcile dispatched requests before permitting retries or voids.

7. **MAJOR — Draft approval does not identify the draft actually watched.**  
   `ok draft_cut` stores clip and timing hashes, excluding the draft file, narration and assembly manifest. Change the narration or manifest inputs while preserving those hashes: the score prerequisite remains valid. Current assembly consumes `MANIFEST.units[*].src`, while provenance checks reconstruct canonical filenames separately. D §3 step 7; [assembly inputs](F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/swirls_assemble.py:348), [provenance lookup](F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/swirls_episode.py:308).  
   **Fix:** Bind approval to the rendered draft and its complete input manifest; verify the exact files assembly consumes.

8. **MAJOR — Overrides can neutralize essential correctness gates.**  
   D §5.3 exempts only the spend guard from overrides. It does not protect KJV correctness or provenance. Current `apply_overrides()` downgrades any matching FAIL when given a truthy dictionary, without validating authorization or binding it to asset bytes. An old override can survive another render. [Override implementation](F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/swirls_verify.py:600).  
   **Fix:** Make Scripture and provenance failures non-overridable; require explicit, asset-bound owner exceptions for permitted visual compromises.

9. **MAJOR — A missing denial becomes a permissible text warning.**  
   Expected caption **“I am not”**, rendered **“I am”**: similarity is approximately 0.67, above the 0.6 acceptance floor. It becomes a near-match warning rather than missing or invented text. That changes meaning precisely where the pilot needs John’s denial. D SWS-G9; [text judge](F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/swirls_verify.py:429).  
   **Fix:** Block unresolved textual differences, especially negation, names and Scripture; clear OCR uncertainty through a recorded human check.

10. **MAJOR — The moving-hold formula can accept a dead ending.**  
    With zero motion in both measured spans, the specified comparison is `0 ≥ 0`. An averaged score can also pass a brief movement followed by a frozen ending, or register flicker instead of scene motion. Repeating the same measurement on the final film preserves the weakness. D SWS-G15h and T8.  
    **Fix:** Require meaningful motion above an absolute floor throughout consecutive hold windows, including the final window.

11. **MAJOR — The writer packet contains a wrong exact-quotation attribution.**  
    P §7 attributes **“the voice of one crying in the wilderness”** to Isaiah 40:3. That is John 1:23 wording; Isaiah reads **“The voice of him that crieth…”**. A writer following this sentence can produce a wrongly referenced span despite the correct table elsewhere. [Isaiah 40:3](https://www.biblegateway.com/passage/?search=Isaiah+40%3A3&version=KJV), [John 1:23](https://www.biblegateway.com/passage/?search=John+1%3A23&version=KJV).  
    **Fix:** Attribute the quotation to John 1:23 and describe it as John applying Isaiah’s prophecy.

12. **MAJOR — The strongest Christology is absent from the restricted writer handoff.**  
    P §2 explicitly connects Jesus with Isaiah’s LORD and with taking away sin. Writers receive only §§1 and 7 plus the length table. The line jobs allow the short Lamb quotation and an ending built around “voice,” without explicitly requiring sin removal or explaining whose way John prepares. A generic lesson about humble voices can satisfy the mechanical checks. [Narration gate](F:/slk/PycharmProjects/JesusInTheBible/narration_gate.py:175) checks shared vocabulary, not those meanings.  
    **Fix:** Put mandatory propositions in the writer packet: John points to Jesus; Jesus is the Lord whose way is prepared; the Lamb takes away sin.

13. **MAJOR — References can be declared without being used.**  
    The new plan uses `subjects`; retained code reads `recurring`, so it can report zero recurring subjects and PASS. Even after that rename, declared files merely existing does not prove the generation request includes them: submitted refs come separately from `spec.refs`. Episode two can therefore lose character continuity while its reference gates pass. D SWS-G7a/G7b and §9.1; [declaration checker](F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/swirls_short.py:399), [submitted refs](F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/test_the_cross/swirls_page.py:377).  
    **Fix:** Validate one subject schema and require the appropriate reference hashes in every generation payload.

14. **MAJOR — A hand-fixed pilot would conceal episode-two failures.**  
    The mandated music copy still reads `EP16_REMOTION_v1.mp4`; changing only turning points and the split leaves that input nonexistent. The SFX copy retains episode-13 filenames and soldiers/gate sounds. T12 substitutes synthetic music and does not exercise the actual SFX script, so it can pass despite these failures. D steps 8–9, T12 and §9.4; [music input](F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/swirls_episode_16_let_the_little_children/generate_score_piano.py:21), [SFX inputs and layers](F:/slk/PycharmProjects/JesusInTheBible/poc_living_water_ink_style_test/swirls_episode_13_the_cross_that_wasnt_his/build_sfx.py:50).  
    **Fix:** Parameterize episode inputs and exercise the real music/SFX plumbing on a second episode fixture.

15. **MAJOR — The final film panel has no explicit acceptance threshold.**  
    D step 10 collects clarity and curiosity scores, permits two rounds, then presents a “still weak” list. It defines no minimum score or explicit terminal failure condition. A technically clean, confusing film can complete the documented process without the panel establishing a quality pass.  
    **Fix:** Define mandatory comprehension and Bible-correctness acceptance criteria, and stop when they remain unmet after round two.

16. **MINOR — Advertised reroll allowances do not fit the reserved caps.**  
    Test clips costing 595 cr plus the advertised 350-cr back-cover reroll require **980 cr** at dispatch under the 110% rule, exceeding the 945-cr cap. The sixth 40-cr north-star/ref/reroll request similarly needs **244**, exceeding 240. D §§5.3 and 8.  
    **Fix:** Calculate displayed caps using the reservation rule so the promised rerolls actually fit.

Read-only throughout; no excluded files were opened and no paid calls were made. The native Python executable could not launch, so I have not claimed a passing test suite.
