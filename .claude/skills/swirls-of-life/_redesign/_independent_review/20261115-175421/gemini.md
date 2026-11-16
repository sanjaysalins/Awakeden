# Independent review — gemini (OK, 59s)

Here is my independent, adversarial review of the design plan. 

### Findings

**1. Verification Gap & Wasted Spend: The Timing Death Loop**
*Citation: Step 2 — Voice... "Too long? Cut words and go back to step 1's lock page." / SWS-G2 voice: "length <= target - 3.0 s"*
You are paying for ElevenLabs generation (~$0.25-0.45) in Step 2, and only then gating the length. If it fails SWS-G2, you throw away paid audio, go back to Step 1, and pay again. A "repeatable pipeline" should not rely on spending money to measure length. You already know the pace is ~2.2 words per second. The strict length gate must happen at Step 1 using a syllable or word-timing estimator *before* any money is spent.

**2. Hidden Risk: Strict OCR Matching on Generative Text**
*Citation: Step 5 — "SWS-G9 still audit... CODE compares that list to the allowed strings (extra, missing, misspelt, doubled = FAIL)."*
AI-generated baked text is notoriously inconsistent, and Claude Vision's OCR of hand-drawn/painted text is not 100% flawless. Doing a strict programmatic exact-match (failing on "misspelt" or "missing" punctuation) will result in massive false positives. You will constantly hit your 2-reroll cap simply because Vision misread an 'l' as an 'I', or the AI stylized a comma into a smudge. 

**3. Over-Engineering: Brittle Pixel-Level Video Heuristics**
*Citation: Step 6 — "SWS-G12 pixels... blue-ink mask area grows <= 15%; hero area keeps moving in the last second (not a dead hold)"*
Writing $0 deterministic OpenCV/FFmpeg scripts to detect semantic concepts like "hero area keeps moving" or "blue-ink mask" in highly stylized, noisy, AI-generated Baroque video is extremely brittle. Video compression artifacts, film grain, or flickering light will trivially defeat a movement threshold, while color bleeding will defeat the ink mask. This is premature optimization that will falsely fail perfectly good Kling clips.

**4. Feasibility / Single Point of Failure: The Agent Bridge**
*Citation: Step 5 — "A live Claude session must service the bridge."*
You are designing an automated CLI runner (`swirls_episode.py <dir> still <id>`), but it relies entirely on a human keeping a secondary, live Claude Code session running in the background just to handle OpenArt OAuth. If that agent dies, times out, or gets stuck in a loop, your entire pipeline hangs indefinitely, burning execution time. It fundamentally compromises the reliability of an unattended pipeline.

**5. False Assumption: Auto-Cropping Generative Borders**
*Citation: Section 3 / SWS-G10 — "If a border sits within the outer 6%: auto-crop inside it and rescale (the 2K source leaves room for 1080x1920)."*
If Kling or nano-banana-pro generates an asymmetrical border (e.g., thicker on the bottom than the top), an auto-crop based on edge detection will shift the center of the image. Rescaling this uneven crop back to a strict 9:16 aspect ratio will introduce stretching/squashing distortion to the artwork.

VERDICT: REVISE
TOP FIXES:
1. Move the hard timing/duration gate into Step 1 as a deterministic calculation (e.g., word/syllable count / 2.2) to prevent spending money on audio that will just be thrown away.
2. Downgrade SWS-G9's exact-match OCR text comparison to use a fuzzy-matching threshold (Levenshtein distance) or keep it as an advisory warning (WARN), as exact matching will fail too often.
3. Remove the over-engineered OpenCV pixel-movement heuristics in SWS-G12 ("hero area keeps moving", "blue-ink mask"), and rely instead on the Vision pass (SWS-G13) and human QC.
